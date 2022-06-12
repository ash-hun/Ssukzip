import {
  Head,
  Html,
  Main,
  NextScript
} from "next/document"
import Script from "next/script"

const Document = () => {
  const KAKAO_MAP_KEY = "34c385f85c12d6b6fa19a40539c67b02"
  const KAKAO_LIBRARY = "services"

  return (
    <Html>
      <Head />
      <body>
        <Main />
        <NextScript />
        <script
          src={`//dapi.kakao.com/v2/maps/sdk.js?appkey=${KAKAO_MAP_KEY}&libraries=${KAKAO_LIBRARY}`}
        />
      </body>
    </Html>
  )
}

export default Document