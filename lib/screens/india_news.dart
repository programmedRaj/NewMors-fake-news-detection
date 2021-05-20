import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:newmours/constants/api_const.dart';
import 'package:newmours/global_widgets/news_showing_widget.dart';
import 'dart:convert';
import 'dart:io';
import 'package:dio/dio.dart';
import 'package:newmours/screens/corona.dart';
import 'package:newmours/screens/detailed_news.dart';
import 'package:newmours/screens/entertainment.dart';
import 'package:newmours/screens/home.dart';
import 'package:newmours/utils.dart';

class India extends StatefulWidget {
  @override
  _IndiaState createState() => _IndiaState();
}

class _IndiaState extends State<India> {
  bool isLoaded = false;
  List<String> headLines = [];
  List<String> link = [];
  List<String> imgLink = [];
  List<String> prediction = [];

  @override
  void initState() {
    super.initState();
    //testing();
    getNews('भारत');
  }

  testing() async {
    var dio = Dio();
    print('ent testing');
    var url = 'http://192.168.43.169:5000/';
    print('sending req');
    var resp = await dio.post(
      url,
      queryParameters: {
        "topic": 'कोरोना',
      },
    );
    print(resp);
  }

  Future<List> getNews(String params) async {
    var url = ApiConst.baseUrl;
    //'http://10.0.2.2:5000/';
    var resp = await http.post(
      url,
      body: {
        "topic": params,
      },
    );
    List decodedResp = json.decode(resp.body);
    //print(decodedResp[1][0].toString() + '=======');
    for (var item in decodedResp) {
      headLines.add(item[0]);
      link.add(item[1]);
      imgLink.add(item[3]);
      prediction.add(item[2]);
    }
    for (var item in headLines) {
      print(item + '---');
    }
    setState(() {
      isLoaded = true;
    });
    return decodedResp;
  }

  @override
  Widget build(BuildContext context) {
    print('corona');
    return Container(
      child: Container(
        child: Center(
            child: isLoaded
                ? ListView.builder(
                    itemCount: headLines.length,
                    itemBuilder: (context, i) {
                      return Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: InkWell(
                          onTap: () {
                            Navigator.push(
                                context,
                                MaterialPageRoute(
                                    builder: (context) => DetailedNews(
                                        heading: headLines[i], url: link[i])));
                          },
                          child: Card(
                            elevation: 10,
                            child: Padding(
                              padding: const EdgeInsets.all(4.0),
                              child: Column(
                                children: [
                                  Container(
                                    child: Row(
                                      children: [
                                        Container(
                                            width: 120,
                                            child: Image.network(imgLink[i])),
                                        SizedBox(
                                          width: 8,
                                        ),
                                        Container(
                                          width: 200,
                                          child: AutoSizeText(
                                            headLines[i],
                                            style: TextStyle(fontSize: 12),
                                            maxLines: 6,
                                            overflow: TextOverflow.clip,
                                          ),
                                        )
                                      ],
                                    ),
                                  ),
                                  Row(
                                    mainAxisSize: MainAxisSize.max,
                                    mainAxisAlignment: MainAxisAlignment.end,
                                    children: [
                                      prediction[i] == 'FAKE'
                                          ? Container(
                                              padding:
                                                  const EdgeInsets.symmetric(
                                                      horizontal: 5,
                                                      vertical: 3),
                                              color: Colors.red,
                                              child: Text(
                                                'Rumour',
                                                style: TextStyle(
                                                    color: Colors.white),
                                              ),
                                            )
                                          : Container(
                                              padding:
                                                  const EdgeInsets.symmetric(
                                                      horizontal: 5,
                                                      vertical: 3),
                                              color: Colors.green,
                                              child: Text(
                                                'Real',
                                                style: TextStyle(
                                                    color: Colors.white),
                                              ),
                                            )
                                    ],
                                  )
                                ],
                              ),
                            ),
                          ),
                        ),
                      );
                    },
                  )
                : CircularProgressIndicator()),
      ),
    );
  }
}
