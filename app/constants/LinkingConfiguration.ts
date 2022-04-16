import { LinkingOptions, NavigatorScreenParams } from '@react-navigation/native';
import { NativeStackScreenProps } from '@react-navigation/native-stack';

export const linking: LinkingOptions<RootStackParamList> = {
  prefixes: [],
  config: {
    screens: {
      Root: {
        screens: {
          Loading: 'loading',
          Login: 'login',
          Map: 'map',
          StoreList: 'storelist',
        }
      }
    }
  }
}

export type RootStackParamList = {
  Root: NavigatorScreenParams<MainDrawerParamList> | undefined;
  NotFound: undefined;
}

export type RootStackScreenProps<Screen extends keyof RootStackParamList> = NativeStackScreenProps<
  RootStackParamList,
  Screen
>;

export type MainDrawerParamList = {
  Loading: undefined;
  Login: undefined;
  Map: undefined;
  StoreList: undefined;
}

export type MainDrawerScreenProps<Screen extends keyof MainDrawerParamList> = NativeStackScreenProps<
  MainDrawerParamList,
  Screen
>;