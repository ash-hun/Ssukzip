import * as React from 'react'
import { GetServerSideProps, NextPage } from "next"
import axios from 'axios'
import { useRouter } from 'next/router'
import { setCookies } from 'cookies-next';
import { server } from '../../constants/env';

interface Response {
  access_token: string
}

const AuthKakao: NextPage<Response> = ({access_token}) => {
  const router = useRouter()
  React.useEffect(() => {
    setCookies('access_token', access_token)
    router.push('/map')
  }, [])

  return (
    <div>
    </div>
  )
}

export const getServerSideProps: GetServerSideProps = async ({query}) => {
  const { code } = query
  const REDIRECT_URL = process.env.NODE_ENV === 'development' ?
    'http://localhost:3000/auth/kakao' : 'https://ssukzip-nextjs.vercel.app/auth/kakao'
  const res = await axios.get(`${server}/auth/kakao`, {
    params: {
      code,
      redirectUri: REDIRECT_URL
    }
  })
  .then(res => res.data)
  .catch(err => console.error(err))

  if(!res) {
    return {
      redirect: {
        destination: '/',
        permanent: false
      }
    }
  }

  return {
    props: {
      access_token: res.access_token
    }
  }
}

export default AuthKakao