import * as React from 'react'
import {
  Box,
  Button,
  Drawer,
  DrawerBody,
  DrawerCloseButton,
  DrawerContent,
  DrawerFooter,
  DrawerHeader,
  DrawerOverlay,
  Heading,
  Icon,
  IconButton,
  Link,
  Stack,
  StackDivider,
  Text
} from '@chakra-ui/react'
import { useRouter } from 'next/router'
import PhoneLink from './PhoneLink'

interface Marker {
  position: {
    lat: number
    lng: number
  },
  content: kakao.maps.services.PlacesSearchResultItem
}

interface Props {
  markers: Array<Marker>
  isOpen: boolean
  onOpen?: () => void
  onClose: () => void
  onSelected: (marker: Marker) => void
}

const MenuDrawer: React.FC<Props> = ({markers, isOpen, onClose, onSelected}) => {
  return (
    <Drawer
      isOpen={isOpen}
      placement='right'
      size='full'
      onClose={onClose}
    >
      <DrawerOverlay />
      <DrawerContent>
        <DrawerCloseButton />
        <DrawerBody>
          <Stack
            direction='column'
            h="100%"
            overflowY='auto'
          >
            {markers.map((marker) => (
              <Box
                key={marker.content.id}
                mt={5}
                _hover={{
                  backgroundColor: 'blackAlpha.100'
                }}
                onClick={() => {
                  onClose()
                  onSelected(marker)
                }}
              >
                <Stack direction='row' align='center'>
                  <Heading fontSize='md'>{marker.content.place_name}</Heading>
                  <Text color="blackAlpha.500" fontSize='xs'>
                    {marker.content.category_name}
                  </Text>
                </Stack>
                <Stack
                  direction='row'
                  align='center'
                  divider={<StackDivider borderColor='gray.200' />}
                >
                  <Text>{marker.content.address_name}</Text>
                  <Text fontSize='xs'>
                    {marker.content.distance}
                  </Text>
                </Stack>
                <PhoneLink phone={marker.content.phone}/>
              </Box>
            ))}
          </Stack>
        </DrawerBody>
      </DrawerContent>
    </Drawer>
  )
}

export default MenuDrawer