import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';

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
                  Navigator.pushNamed(
                      context,
                      '/map',
                    arguments: [
                      "test"
                    ]
                  );
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

  _checkPermission() async {
    LocationPermission permission = await Geolocator.checkPermission();

    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        debugPrint('Location permissions are denied');
        return false;
      }else if(permission == LocationPermission.deniedForever){
        debugPrint("'Location permissions are permanently denied");
        return false;
      }else{
        debugPrint("GPS Location service is granted");
        return true;
      }
    }else{
      debugPrint("GPS Location permission granted.");
      return true;
    }
  }
}