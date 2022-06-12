import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

void main() => {
  runApp(const MaterialApp(home: WebViewWidget()))
};

class WebViewWidget extends StatefulWidget {
  const WebViewWidget({Key? key, this.cookieManager}) : super(key: key);

   final CookieManager? cookieManager;

  @override
  State<WebViewWidget> createState() => _WebViewState();
 }

class _WebViewState extends State<WebViewWidget> {

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      backgroundColor: Colors.green,
      body: SafeArea(
        child: WebView(
          initialUrl: 'http://localhost:3000/',
          javascriptMode: JavascriptMode.unrestricted,
        )
      //   onWebViewCreated: (WebViewController webViewController) {
      //     _controller.complete(webViewController);
      //   },
      //   onProgress: (int progress) {
      //     print('WebView is loading (progress : $progress%)');
      //   },
      //   javascriptChannels: <JavascriptChannel>{
      //     _toasterJavascriptChannel(context),
      //   },
      //   navigationDelegate: (NavigationRequest request) {
      //     if (request.url.startsWith('https://www.youtube.com/')) {
      //       print('blocking navigation to $request}');
      //       return NavigationDecision.prevent;
      //     }
      //     print('allowing navigation to $request');
      //     return NavigationDecision.navigate;
      //   },
      //   onPageStarted: (String url) {
      //     print('Page started loading: $url');
      //   },
      //   onPageFinished: (String url) {
      //     print('Page finished loading: $url');
      //   },
      //   gestureNavigationEnabled: true,
      //   backgroundColor: const Color(0x00000000),
      // ),
      // floatingActionButton: favoriteButton(),
      )
    );
  }
}