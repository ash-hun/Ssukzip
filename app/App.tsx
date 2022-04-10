import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';

import Navigation from '@components/Navigation';

export default function App() {
  return (
    <SafeAreaProvider>
      <Navigation />
      <StatusBar style="auto" />
    </SafeAreaProvider>
  );
}