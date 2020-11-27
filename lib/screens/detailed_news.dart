import 'dart:ui';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter/material.dart';

class DetailedNews extends StatefulWidget {
  final String heading;
  final String url;

  DetailedNews({@required this.heading, @required this.url});

  @override
  _DetailedNewsState createState() => _DetailedNewsState();
}

class _DetailedNewsState extends State<DetailedNews> {
  String detailedNews;
  bool isLoaded = false;

  @override
  void initState() {
    getDetailedNews();
    super.initState();
  }

  getDetailedNews() async {
    var url = 'http://192.168.43.182:5000/details';
    //'http://10.0.2.2:5000/';
    var resp = await http.post(
      url,
      body: {
        "url": widget.url,
      },
    );
    var decodedResp = json.decode(resp.body);
    detailedNews = decodedResp;
    //print(decodedResp[1][0].toString() + '=======');
    setState(() {
      isLoaded = true;
    });
    return decodedResp;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.green,
        title: Text('NewMours'),
      ),
      body: SafeArea(
          child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 8),
              child: isLoaded
                  ? SingleChildScrollView(
                      child: Column(
                        children: [
                          SizedBox(
                            height: 50,
                          ),
                          Text(
                            widget.heading,
                            style: TextStyle(
                                color: Colors.black,
                                fontSize: 18,
                                fontWeight: FontWeight.bold),
                          ),
                          SizedBox(
                            height: 50,
                          ),
                          Text(detailedNews),
                        ],
                      ),
                    )
                  : Center(child: CircularProgressIndicator()))),
    );
  }
}
