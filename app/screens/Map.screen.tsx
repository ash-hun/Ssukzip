import React from "react";
import { StyleSheet, View, Text } from "react-native";
import { MainDrawerScreenProps } from "@constants/LinkingConfiguration";

export default function MapScreen({ navigation }: MainDrawerScreenProps<'Map'>) {

  return (
    <View style={styles.container}>
      <Text>Map</Text>
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