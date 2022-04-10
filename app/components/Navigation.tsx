import { LinkingOptions, NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import LoginScreen from '@screens/Login.screen';

export type StackParamList = {
  LogIn: undefined;
  NotFound: undefined;
};

const Stack = createNativeStackNavigator<StackParamList>();

export default function Navigation() {
  return (
    <NavigationContainer linking={link}>
      <Stack.Navigator>
        <Stack.Screen name="LogIn" component={LoginScreen} options={{ headerShown: false }}/>
      </Stack.Navigator>
    </NavigationContainer>
  )
}

const link: LinkingOptions<StackParamList> = {
  prefixes: ['myapp://'],
  config: {
    screens: {
      LogIn: "login"
    }
  }
}