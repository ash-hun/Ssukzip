import * as React from 'react'
import {
  Avatar,
  Button,
  Drawer,
  DrawerBody,
  DrawerCloseButton,
  DrawerContent,
  DrawerFooter,
  DrawerHeader,
  DrawerOverlay,
  Editable,
  EditableInput,
  EditablePreview,
  Icon,
  Text,
  useEditableState,
} from '@chakra-ui/react'
import { MdModeEdit } from 'react-icons/md'
import axios from 'axios'
import { getCookie, removeCookies } from 'cookies-next'
import { server } from '../constants/env'
import { useRouter } from 'next/router'

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
  isOpen: boolean
  onOpen?: () => void
  onClose: () => void
}

const MyPageDrawer: React.FC<Props> = ({user, isOpen, onClose}) => {
  const route = useRouter()
  const handleSubmit = async (nextValue: string) => {
    const access_token = getCookie('access_token')
    const data = await axios.post(`${server}/user/update/nickname`, {
      nickname: nextValue
    }, {
      headers: {
        "Authorization": `Bearer ${access_token}`
      },
      params: {
        nickname: nextValue
      }
    }).then(res => res.data)
    .catch(err => console.error(err))

    console.log(data)
  }

  const handleLogout = () => {
    removeCookies('access_token')
    route.push('/')
  }

  return (
    <Drawer
      isOpen={isOpen}
      placement='bottom'
      size='xl'
      onClose={onClose}
    >
      <DrawerOverlay />
        <DrawerContent position='relative'>
          <DrawerCloseButton />
          <DrawerHeader>
            <Avatar
              size="xl"
              name={user.nickname}
              src={user.img_url}
              position='absolute'
              top="-50"
              left='5'
            />
          </DrawerHeader>
          <DrawerBody pt='6'>
            <Editable
              defaultValue={user.nickname}
              onSubmit={handleSubmit}
            >
              <EditablePreview
                textDecoration='underline'
                _hover={{
                  cursor: 'pointer'
                }}
              />
              <EditableInput width='auto'/>
              <EditableControls />
            </Editable>
            <Text>{user.email}</Text>
            <Button onClick={handleLogout}>로그아웃</Button>
          </DrawerBody>
        </DrawerContent>
    </Drawer>
  )
}

function EditableControls() {
  const {
    isEditing,
  } = useEditableState()

  return isEditing ? null : <Icon as={MdModeEdit} />;
}

export default MyPageDrawer