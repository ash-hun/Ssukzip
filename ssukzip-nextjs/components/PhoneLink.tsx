import { Link, TypographyProps } from "@chakra-ui/react"
import { useRouter } from "next/router"

interface Props {
  phone: string
}
const PhoneLink: React.FC<Props & TypographyProps> = ({phone, fontSize}) => {
  const router = useRouter()
  const handleLink: React.MouseEventHandler<HTMLAnchorElement> = (e) => {
    e.stopPropagation()
    router.push(`tel:${phone}`)
  }
  return (
    <Link
      color='blue.400'
      onClick={handleLink}
      isExternal
      fontSize={fontSize}
    >
      {phone}
    </Link>
  )
}

export default PhoneLink