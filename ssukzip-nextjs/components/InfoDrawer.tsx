import * as React from 'react'
import useSWR from 'swr'
import axios from 'axios'
import {
  Box,
  Button,
  Center,
  Drawer,
  DrawerBody,
  DrawerCloseButton,
  DrawerContent,
  DrawerHeader,
  DrawerOverlay,
  Heading,
  Icon,
  List,
  ListIcon,
  ListItem,
  Stack,
  StackDivider,
  Text,
  Textarea,
  useToast,
} from '@chakra-ui/react'
import {
  MdLocalPhone,
  MdOutlineLocationOn,
  MdThumbDown,
  MdThumbDownOffAlt,
  MdThumbUp,
  MdThumbUpOffAlt
} from 'react-icons/md'
import PhoneLink from './PhoneLink'
import { Rating } from '@mui/material'
import { getCookie } from 'cookies-next'
import { server } from '../constants/env'
import {AiOutlineFrown, AiOutlineSmile} from 'react-icons/ai'

interface Marker {
  position: {
    lat: number
    lng: number
  },
  content: kakao.maps.services.PlacesSearchResultItem
}

interface Reply {
  comment: string
  filtering_comment: string
  id: number
  market_id: number
  rate: number
  recommend: number
  solution: string
  user_id: number
  user_nickname: string
}

interface Props {
  marker: Marker
  isOpen: boolean
  onOpen?: () => void
  onClose: () => void
}

const ReviewMapping = ({review}: {review: string}) => {
  const reviewPer = React.useMemo(() => {
    if(review.includes("비속어")) {
      return "비속어"
    } else {
      return Number(review.split(']는')[1].split('%')[0]).toFixed(3) + "%"
    }
  },
    [review],
  )
  if (review.includes("긍정")) {
    return (
      <div>
        <AiOutlineSmile color='green' style={{ display: 'inline' }}/>
        {' '}
        <Text color='green' style={{ display: 'inline' }}>{reviewPer}</Text>
      </div>
    )
  } else {
    return (
      <div>
        <AiOutlineFrown color='red' style={{ display: 'inline' }}/>
        {' '}
        <Text color='red' style={{ display: 'inline' }}>{reviewPer}</Text>
      </div>
    )
  }
}

const InfoDrawer: React.FC<Props> = ({marker, isOpen, onClose}) => {
  const [ rate, setRate ] = React.useState<number>(2.5)
  const [ comment, setComment ] = React.useState<string>("")
  const [ solution, setSolution ] = React.useState<string>("")
  const [ loading, setLoading ] = React.useState(false)
  const toast = useToast()

  const fetcher = (url: string) => {
    const access_token = getCookie('access_token')
    return axios.get(url, {
      headers: {
        "Authorization": `Bearer ${access_token}`
      }
    }).then(res => res.data)
  }

  const { data, error } = useSWR<Array<Reply>>(
    () => `${server}/review/info/${marker.content.id}`,
    fetcher,
    { refreshInterval: 1000 }
  )

  const clearForm = () => {
    setComment("")
    setSolution("")
    setRate(2.5)
  }

  const handleSubmit: React.MouseEventHandler<HTMLButtonElement> = async (e) => {
    e.preventDefault()
    const access_token = getCookie('access_token')
    const data = {
      review_id: 0,
      market_id: marker.content.id,
      rate,
      comment,
      solution
    }

    setLoading(true)
    const res = await axios.post(`${server}/review/create`, data, {
      headers: {
        "Authorization": `Bearer ${access_token}`
      }
    })
    .then(res => {
      toast({
        title: "성공",
        description: res.data.msg,
        status: 'success',
        duration: 1000,
        isClosable: true,
        position: 'top'
      })
      return res.data
    })
    .catch(err => console.error(err))
    clearForm()
    setLoading(false)

    console.log(res)
  }

  return (
    <Drawer
      isOpen={isOpen}
      placement='bottom'
      size='xs'
      onClose={() => {
        onClose()
        clearForm()
      }}
    >
      <DrawerOverlay />
      <DrawerContent>
        <DrawerCloseButton />
        {marker && (
          <Box>
            <DrawerHeader>{marker.content.place_name}</DrawerHeader>
            <DrawerBody
              bgColor='blackAlpha.100'
              overscrollY='auto'
              maxH='55vh'
            >
              <List
                spacing={2}
                p={4}
                borderWidth='1px'
                borderRadius='lg'
                bgColor='white'
              >
                <ListItem>
                  <Stack direction='row'>
                    <Center>
                      <ListIcon as={MdOutlineLocationOn} fontSize={20}/>
                    </Center>
                    <Box>
                      <Text fontSize='sm'>{marker.content.road_address_name}</Text>
                      <Text fontSize='sm'>지번: {marker.content.address_name}</Text>
                    </Box>
                  </Stack>
                </ListItem>
                <ListItem>
                  <Stack direction='row'>
                    <Center><ListIcon as={MdLocalPhone} fontSize={20}/></Center>
                    <PhoneLink phone={marker.content.phone} fontSize='sm'/>
                  </Stack>
                </ListItem>
              </List>
              <Box
                mt={2}
                p={4}
                borderWidth='1px'
                borderRadius='lg'
                bgColor='white'
              >
                <Stack>
                  <Stack direction='row'>
                    <Text as='legend'>썩점:</Text>
                    <Rating
                      defaultValue={2.5}
                      precision={0.5}
                      color='#000000'
                      icon={<Icon as={MdThumbDown} />}
                      emptyIcon={<Icon as={MdThumbDownOffAlt} />}
                      value={rate}
                      onChange={(_, nextV) => {if(nextV) setRate(nextV)}}
                    />
                  </Stack>
                  <Textarea
                    placeholder='비판 리뷰'
                    value={comment}
                    onChange={e => setComment(e.currentTarget.value)}
                  />
                  <Textarea
                    placeholder='개선점'
                    value={solution}
                    onChange={e => setSolution(e.currentTarget.value)}
                    isRequired
                  />
                  <Button isLoading={loading} onClick={handleSubmit}>리뷰 작성</Button>
                </Stack>
              </Box>
              <Box
                mt={2}
                p={4}
                borderWidth='1px'
                borderRadius='lg'
                bgColor='white'
              >
                <Stack
                  direction='column'
                  divider={<StackDivider borderColor='gray.200' />}
                >
                  {data && data.map((reply) => (
                    <Box key={reply.id}>
                      <Rating
                        size='small'
                        value={reply.rate}
                        readOnly
                      />
                      <Heading fontSize='sm'>{reply.user_nickname}</Heading>
                      <Text>{reply.comment}</Text>
                      <Text>{reply.solution}</Text>
                      <Stack
                        direction='row'
                        mt={2}
                      >
                        <Text>{reply.recommend}</Text>
                        <LikeButton id={reply.id}/>
                        <Text fontSize='sm'>좋아요</Text>
                      </Stack>
                      <ReviewMapping review={reply.filtering_comment} />
                    </Box>
                  ))}
                </Stack>
              </Box>
            </DrawerBody>
          </Box>
        )}
      </DrawerContent>
    </Drawer>
  )
}

function LikeButton({id}: {id: number}) {
  const [ like, setLike ] = React.useState(false)

  const onLike = () => setLike(true)
  const onUnLike = () => setLike(false)

  const handleLike = async () => {
    const access_token = getCookie('access_token')
    const data = await axios.get(`${server}/review/recommend/${id}`, {
      headers: {
        "Authorization": `Bearer ${access_token}`
      }
    }).then(res => res.data)

    console.log(data)
  }

  return (
    <Center>
      { like ? (
        <Icon
          onClick={onUnLike}
          fontSize={14}
          as={MdThumbUp}
          _hover={{
            cursor: 'pointer'
          }}
        />
      ) : (
        <Icon
          onClick={() => {
            onLike()
            handleLike()
          }}
          fontSize={14}
          as={MdThumbUpOffAlt}
          _hover={{
            cursor: 'pointer'
          }}
        />
      )}
    </Center>
  )
}

export default InfoDrawer