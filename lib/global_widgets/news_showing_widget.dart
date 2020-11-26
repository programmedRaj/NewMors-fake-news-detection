import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:newmours/global_widgets/news_showing_widget.dart';
import 'dart:convert';
import 'dart:io';
import 'package:dio/dio.dart';

class NewsShower extends StatefulWidget {
  final String params;
  NewsShower({@required this.params});

  @override
  _NewsShowerState createState() => _NewsShowerState();
}

class _NewsShowerState extends State<NewsShower> {
  @override
  void initState() {
    super.initState();
    getNews();
    print(widget.params);
  }

  Future<List> getNews() async {
    var url = 'http://192.168.43.182:5000/';
    //'http://10.0.2.2:5000/';
    var resp = await http.post(
      url,
      body: {
        "topic": 'कोरोना',
      },
    );
    var decodedResp = json.decode(resp.body);
    print(decodedResp[0][0].toString() + '=======');

    return decodedResp;
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.blue,
    );
  }
}
