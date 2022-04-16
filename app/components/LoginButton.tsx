import { StyleSheet, Pressable, Text, Image, GestureResponderEvent } from "react-native";

interface Props {
  brand: "google" | "kakao";
  onPress?: ((event: GestureResponderEvent) => void)
}

const LoginButton: React.FC<Props> = ({brand, onPress}) => {
  return (
    <Pressable
      style={[styles.button, brand === "google" ? styles.google : styles.kakao]}
      onPress={onPress}
    >
      <Image
        style={styles.logo}
        source={brand === "google" ? require("@assets/google-logo.png") : require("@assets/kakao-logo.png")}
      />
      <Text
        style={brand === "google" ? styles.google_text : styles.kakao_text}
      >
        {brand === "google" ? "Sign in with Google" : "Login with Kakao"}
      </Text>
    </Pressable>
  )
}

const styles = StyleSheet.create({
  button: {
    height: 40,
    width: "100%",
    display: "flex",
    flexDirection: "row",
    alignItems: 'center',
    marginVertical: 6,
    paddingHorizontal: 8,
  },
  logo: {
    width: 18,
    height: 18,
  },
  google: {
    backgroundColor: "#FFFFFF",
    borderRadius: 1,
    boxShadow: "rgb(0 0 0 / 25%) 0 2px 4px 0"
  },
  google_text: {
    fontFamily: "Roboto, arial, sans-serif",
    fontSize: 14,
    fontWeight: "500",
    textAlign: "center",
    color: "rgba(0, 0, 0, .54)",
    width: "100%",
    paddingLeft: 24,
  },
  kakao: {
    backgroundColor: "#FEE500",
    borderRadius: 1,
    boxShadow: "rgb(0 0 0 / 25%) 0 2px 4px 0"
  },
  kakao_text: {
    fontFamily: "Roboto, arial, sans-serif",
    fontSize: 14,
    fontWeight: "500",
    textAlign: "center",
    color: "rgba(0, 0, 0, .54)",
    width: "100%",
    paddingLeft: 24,
  },
});

export default LoginButton