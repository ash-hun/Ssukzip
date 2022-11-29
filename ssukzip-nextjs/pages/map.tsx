import * as React from 'react'
import type { GetServerSideProps, NextPage } from 'next'
import { Map as KaKaoMap, MapMarker } from 'react-kakao-maps-sdk'
import {
  Icon,
  IconButton
} from '@chakra-ui/react'
import { MdList, MdMyLocation, MdPerson } from "react-icons/md";
import MenuDrawer from '../components/MenuDrawer'
import InfoDrawer from '../components/InfoDrawer'
import axios from 'axios';
import MyPageDrawer from '../components/MyPageDrawer';
import { server } from '../constants/env';

interface Marker {
  position: {
    lat: number
    lng: number
  },
  content: kakao.maps.services.PlacesSearchResultItem
}

interface User {
  email: string
  name: string
  img_url: string
  id: number
  nickname: string
  token: string
}

interface Props {
  user: User
}

const Map: NextPage<Props> = ({user}) => {
  const [ isMenuOpen, setIsMenuOpen ] = React.useState(false)
  const [ isInfoOpen, setIsInfoOpen ] = React.useState(false)
  const [ isMyOpen, setIsMyOpen ] = React.useState(false)
  const [ map, setMap ] = React.useState<kakao.maps.Map>()
  const [ markers, setMarkers ] = React.useState<Array<Marker>>([])
  const [ selectedMarker, setSelectedMarker ] = React.useState<Marker>()

  React.useEffect(() => {
    if(!map) return
    gotoMyLocation()
  }, [map])

  const onMenuOpen = () => setIsMenuOpen(true)
  const onMenuClose = () => setIsMenuOpen(false)
  const onInfoOpen = () => setIsInfoOpen(true)
  const onInfoClose = () => setIsInfoOpen(false)
  const onMyOpen = () => setIsMyOpen(true)
  const onMyClose = () => setIsMyOpen(false)


  const gotoMyLocation = () => {
    if(navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        const latlng = new kakao.maps.LatLng(
          position.coords.latitude,
          position.coords.longitude
        )
        map?.setCenter(latlng)
        searchNearbyRestaurant()
      }, (error) => {
        console.log(error)
      }, {
        enableHighAccuracy: true
      })
    }
  }

  const searchNearbyRestaurant = () => {
    const ps = new kakao.maps.services.Places(map)
    ps.categorySearch('FD6', (data, status, _pagination) => {
      if(status === kakao.maps.services.Status.OK){
        const markers = data.map<Marker>(item => ({
          position: {
            lat: Number(item.y),
            lng: Number(item.x)
          },
          content: {
            ...item,
            category_name: item.category_name.split('>')[item.category_name.split('>').length-1].trim()
          }
        }))
        console.log(markers)
        setMarkers(markers)
      }
    }, {
      useMapCenter: true,
      useMapBounds: true,
    });
  }

  return (
    <div style={{
      width: "100vw",
      height: "100vh",
      position: 'relative'
    }}>
      <KaKaoMap
        style={{
          width: "100vw",
          height: "100vh",
          position: 'absolute'
        }}
        center={{ lat: 37.555946, lng: 126.972317 }}
        level={4}
        onCreate={setMap}
        onDragEnd={(map) => {
          searchNearbyRestaurant()
        }}
      >
        {markers.map(marker => (
          <MapMarker
            key={`marker-${marker.content}-${marker.position.lat},${marker.position.lng}`}
            position={marker.position}
            onClick={(m) => {
              map?.panTo(new kakao.maps.LatLng(
                m.getPosition().getLat(),
                m.getPosition().getLng()
              ))
              setSelectedMarker(marker)
              onInfoOpen()
            }}
          />
        ))}
      </KaKaoMap>
      <IconButton
        bgColor='white'
        boxShadow='base'
        size='sm'
        style={{
          position: 'absolute',
          right: 12,
          top: 7,
          zIndex: 100
        }}
        fontSize={20}
        aria-label='Menu'
        icon={<Icon as={MdList} />}
        onClick={onMenuOpen}
      />
      <IconButton
        bgColor='white'
        boxShadow='base'
        size='sm'
        style={{
          position: 'absolute',
          right: 12,
          bottom: 7,
          zIndex: 100
        }}
        aria-label='MyLocation'
        icon={<Icon as={MdMyLocation} />}
        onClick={gotoMyLocation}
      />
      <IconButton
        bgColor='white'
        size='sm'
        aria-label='MyPage'
        style={{
          position: 'absolute',
          left: 12,
          top: 7,
          zIndex: 100
        }}
        fontSize={20}
        icon={<Icon as={MdPerson} />}
        onClick={onMyOpen}
      />
      <MenuDrawer
        markers={markers}
        isOpen={isMenuOpen}
        onClose={onMenuClose}
        onSelected={(marker) => {
          map?.panTo(new kakao.maps.LatLng(
            marker.position.lat,
            marker.position.lng
          ))
          setSelectedMarker(marker)
          onInfoOpen()
        }}
      />
      { selectedMarker ? (
        <InfoDrawer
          marker={selectedMarker}
          isOpen={isInfoOpen}
          onClose={onInfoClose}
        />
      ) : null}
      <MyPageDrawer
        user={user}
        isOpen={isMyOpen}
        onClose={onMyClose}
      />
    </div>
  )
}

export const getServerSideProps: GetServerSideProps = async ({req}) => {
  const { access_token } = req.cookies
  if(!access_token) {
    return {
      redirect: {
        destination: '/',
        permanent: false
      }
    }
  }

  const user = await axios.get(`${server}/user/me`, {
    headers: {
      "Authorization": `Bearer ${access_token}`
    }
  }).then(res => res.data)
  
  return {
    props: {
      user: user
    }
  }
}

export default Map
