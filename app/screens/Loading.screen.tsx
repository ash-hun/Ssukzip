import React from "react";
import { StyleSheet, View, Text } from "react-native";
import { MainDrawerScreenProps } from "@constants/LinkingConfiguration";

export default function LoadingScreen({ navigation }: MainDrawerScreenProps<'Loading'>) {

  React.useEffect(() => {
    /*
      import zustand logic
    */
    setTimeout(() => {navigation.navigate('Login')}, 3000)
  }, [])

  return (
    <View style={styles.container}>
      <Text>Loading...</Text>
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});