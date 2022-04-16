import LoginButton from "@components/LoginButton";
import { MainDrawerScreenProps } from "@constants/LinkingConfiguration";
import { StyleSheet, View } from "react-native";

export default function LoginScreen({ navigation }: MainDrawerScreenProps<'Login'>) {
  
  const handleLogin = () => {
    navigation.navigate('Map')
  }

  return (
    <View style={styles.container}>
      <View style={styles.button_wrapper}>
        <LoginButton brand="google" onPress={handleLogin}/>
        <LoginButton brand="kakao" />
      </View>
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 24,
  },
  button_wrapper: {
    width: "100%"
  }
});