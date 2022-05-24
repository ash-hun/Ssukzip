import 'package:flutter/material.dart';

class LoginScreen extends StatelessWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              ElevatedButton(
                onPressed: () {
                  Navigator.pushNamed(context, '/map');
                },
                child: const Text('Sign in with Google'),
              ),
              ElevatedButton(
                onPressed: () {
                  Navigator.pushNamed(context, '/map');
                },
                child: const Text('Login with Kakao'),
                style: ElevatedButton.styleFrom(
                  primary: const Color.fromRGBO(254, 229, 0, 1),
                ),
              ),
            ],
          )
      ),
    );
  }
}