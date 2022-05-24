import 'package:flutter/material.dart';
import 'package:ssukzip/login.dart';
import 'package:ssukzip/map.dart';

void main() {
  runApp(
    MaterialApp(
      initialRoute: '/',
      routes: {
        '/': (context) => const LoginScreen(),
        '/map': (context) => const MapScreen(),
      },
    ),
  );
}