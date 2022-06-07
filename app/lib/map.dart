import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:kakaomap_webview/kakaomap_webview.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:geolocator/geolocator.dart';

const String kakaoMapKey = '34c385f85c12d6b6fa19a40539c67b02';

class MapScreen extends StatefulWidget {
  const MapScreen({Key? key}) : super(key: key);

  @override
  State<StatefulWidget> createState() {
    return _MapScreenState();
  }
}

class _MapScreenState extends State<MapScreen> {
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();
  late WebViewController _mapController;
  double _lat = 37.553881;
  double _lng = 126.970488;

  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;

    return Scaffold(
      key: _scaffoldKey,
      body: Stack(
        children: [
          KakaoMapView(
            width: size.width,
            height: size.height,
            kakaoMapKey: kakaoMapKey,
            lat: _lat,
            lng: _lng,
            mapType: MapType.TERRAIN,
            mapController: (controller) {
              _mapController = controller;
            },
            polyline: KakaoFigure(
              path: []
            ),
            polygon: KakaoFigure(
              path: []
            ),
            customScript: '''
              map.setCenter(new kakao.maps.LatLng(37.553881, 126.970488));
              var markers = [];

              function addMarker(position) {
                var marker = new kakao.maps.Marker({position: position});
                marker.setMap(map);
                markers.push(marker);
              }

              function removeAllMarker() {
                marker.setMap(null);
                markers = [];
              }
            ''',
            // markerImageURL:
            // 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png',
            onTapMarker: (message) async {
              ScaffoldMessenger.of(context)
                  .showSnackBar(SnackBar(content: Text(message.message)));
              _getLocation();
            },
            zoomChanged: (message) {
              debugPrint('[zoom] ${message.message}');
            },
            cameraIdle: (message) {
              KakaoLatLng latLng =
              KakaoLatLng.fromJson(jsonDecode(message.message));
              debugPrint('[idle] ${latLng.lat}, ${latLng.lng}');
            },
            boundaryUpdate: (message) {
              KakaoBoundary boundary =
              KakaoBoundary.fromJson(jsonDecode(message.message));
              debugPrint(
                  '[boundary] ne : ${boundary.neLat}, ${boundary.neLng}, sw : ${boundary.swLat}, ${boundary.swLng}');
            },
          ),
          searchButton(),
          returnLocationButton(),
          menuButton(),
        ],
      ),
      endDrawer: SizedBox(
        width: size.width,
        child: drawerMenu()
      ),
    );
  }

  void _openEndDrawer() {
    _scaffoldKey.currentState!.openEndDrawer();
  }

  void _closeEndDrawer() {
    Navigator.pop(context);
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

  _getLocation () async {
    if(await _checkPermission()){
      Position position = await Geolocator.getCurrentPosition(desiredAccuracy: LocationAccuracy.high);
      debugPrint(position.latitude.toString());
      debugPrint(position.longitude.toString());

      try {
        setState(() {
          _lat = position.latitude;
          _lng = position.longitude;
        });
      } catch (e) {
        debugPrint(e.toString());
      }


      // _mapController.runJavascript('''
      //   map.setCenter(new kakao.maps.LatLng($_lat, $_lng));
      // ''');
    }
  }

  drawerMenu() {
    return Drawer(
      child: ListView(
        // Important: Remove any padding from the ListView.
        padding: EdgeInsets.zero,
        children: [
          const DrawerHeader(
            decoration: BoxDecoration(
              color: Colors.blue,
            ),
            child: Text('Drawer Header'),
          ),
          for (int index = 1; index < 21; index++)
            ListTile(
              leading: ExcludeSemantics(
                child: CircleAvatar(child: Text('$index')),
              ),
              title: Text('$index 맛집'),
              subtitle: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: const [
                  Text('첫째줄'),
                  Text('둘째줄')
                ],
              ),
              onTap: _closeEndDrawer,
            ),
        ],
      ),
    );
  }

  returnLocationButton() {
    return Align(
      alignment: Alignment.bottomLeft,
      child: GestureDetector(
        onTap: () async {await _getLocation();},
        child: Container(
          margin: const EdgeInsets.only(left: 16, bottom: 44),
          decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(2),
              color: Colors.white,
              boxShadow: const [
                BoxShadow(
                  color: Colors.black45,
                  blurRadius: 1,
                )
              ]),
          padding: const EdgeInsets.all(10),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: const <Widget>[
              Icon(
                Icons.my_location,
                color: Colors.black54,
              ),
            ],
          ),
        ),
      ),
    );
  }

  searchButton() {
    return Align(
      alignment: Alignment.bottomRight,
      child: GestureDetector(
        onTap: () {},
        child: Container(
          margin: const EdgeInsets.only(right: 16, bottom: 44),
          decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(2),
              color: Colors.white,
              boxShadow: const [
                BoxShadow(
                  color: Colors.black45,
                  blurRadius: 1,
                )
              ]),
          padding: const EdgeInsets.all(10),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: const <Widget>[
              Icon(
                Icons.search,
                color: Colors.black54,
              ),
            ],
          ),
        ),
      ),
    );
  }

  menuButton() {
    return Align(
      alignment: Alignment.topRight,
      child: GestureDetector(
        onTap: _openEndDrawer,
        child: Container(
          margin: const EdgeInsets.only(right: 16, top: 44),
          decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(2),
              color: Colors.white,
              boxShadow: const [
                BoxShadow(
                  color: Colors.black45,
                  blurRadius: 1,
                )
              ]),
          padding: const EdgeInsets.all(10),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: const <Widget>[
              Icon(
                Icons.menu,
                color: Colors.black54,
              ),
            ],
          ),
        ),
      ),
    );
  }
}