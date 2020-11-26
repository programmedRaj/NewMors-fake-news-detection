import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:newmours/global_widgets/news_showing_widget.dart';
import 'dart:convert';
import 'dart:io';
import 'package:dio/dio.dart';

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  getNews() async {
    var dio = Dio();
    var url = 'http://127.0.0.1:5000';
    var resp = await dio.post(url, data: {"topic": "कोरोना"});
    var decodedResp = json.decode(resp.data);
    print(decodedResp);
  }

  @override
  Widget build(BuildContext context) {
    getNews();
    return DefaultTabController(
      length: 7,
      child: Scaffold(
          appBar: AppBar(
            backgroundColor: Colors.green,
            centerTitle: true,
            leading: Icon(Icons.person_outline),
            title: Text(
              'NewMours',
              style: TextStyle(fontSize: 16.0),
            ),
            bottom: PreferredSize(
                child: TabBar(
                    isScrollable: true,
                    unselectedLabelColor: Colors.white.withOpacity(0.3),
                    indicatorColor: Colors.white,
                    tabs: [
                      Tab(
                        child: Text('tab 1'),
                      ),
                      Tab(
                        child: Text('Entertainment'),
                      ),
                      Tab(
                        child: Text('Corona'),
                      ),
                      Tab(
                        child: Text('Lifestyle'),
                      ),
                      Tab(
                        child: Text('Current Balance'),
                      ),
                      Tab(
                        child: Text('Election'),
                      ),
                      Tab(
                        child: Text('India'),
                      ),
                    ]),
                preferredSize: Size.fromHeight(30.0)),
            actions: <Widget>[
              Padding(
                padding: const EdgeInsets.only(right: 16.0),
                child: Icon(Icons.add_alert),
              ),
            ],
          ),
          body: TabBarView(
            children: <Widget>[
              Container(
                child: Center(
                  child: Text('tab 1'),
                ),
              ),
              Container(
                child: Center(
                  child: Text('Tab 2'),
                ),
              ),
              Container(
                child: Center(
                  child: Text('Tab 3'),
                ),
              ),
              Container(
                child: Center(
                  child: Text('Tab 4'),
                ),
              ),
              Container(
                child: Center(
                  child: Text('Tab 5'),
                ),
              ),
              Container(
                child: Center(
                  child: Text('Tab 6'),
                ),
              ),
              Container(
                child: Center(
                  child: Text('Tab 6'),
                ),
              ),
            ],
          )),
    );
  }
}
