import { linking, MainDrawerParamList, RootStackParamList } from '@constants/LinkingConfiguration';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createDrawerNavigator } from '@react-navigation/drawer';

import LoginScreen from '@screens/Login.screen';
import LoadingScreen from '@screens/Loading.screen';
import NotFoundScreen from '@screens/NotFound.screen';
import MapScreen from '@screens/Map.screen';

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function Navigation() {
  return (
    <NavigationContainer linking={linking}>
      <Stack.Navigator>
        <Stack.Screen name="Root" component={DrawerNavigator} options={{ headerShown: false }}/>
        <Stack.Screen name="NotFound" component={NotFoundScreen} options={{ headerShown: false }}/>
      </Stack.Navigator>
    </NavigationContainer>
  )
}

const Drawer = createDrawerNavigator<MainDrawerParamList>();

function DrawerNavigator() {
  return (
    <Drawer.Navigator
      initialRouteName='Loading'
    >
      <Drawer.Screen name="Loading" component={LoadingScreen} options={{ headerShown: false }}/>
      <Drawer.Screen name="Login" component={LoginScreen} options={{ headerShown: false }}/>
      <Drawer.Screen name="Map" component={MapScreen} options={{ headerShown: false }}/>
    </Drawer.Navigator>
  )
}