import 'package:flutter/material.dart';
import 'package:ssukzip/login.dart';
import 'package:ssukzip/map.dart';
import 'package:kakao_flutter_sdk_common/kakao_flutter_sdk_common.dart';

void main() {
  KakaoSdk.init(nativeAppKey: '1635d7e45ebcc7bd3771caa3d8e2e80c');

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