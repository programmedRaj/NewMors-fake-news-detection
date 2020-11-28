import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:newmours/global_widgets/news_showing_widget.dart';
import 'dart:convert';
import 'dart:io';
import 'package:dio/dio.dart';
import 'package:newmours/screens/corona.dart';
import 'package:newmours/screens/entertainment.dart';
import 'package:newmours/screens/home.dart';
import 'package:newmours/screens/india_news.dart';

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  bool isLoaded = false;
  List<String> headLines = [];
  List<String> link = [];
  List<String> imgLink = [];
  int _currentIndex = 0;

  @override
  void initState() {
    super.initState();
    getNews('कोरोना');
  }

  Future<List> getNews(String params) async {
    var url = 'http://192.168.43.169:5000/';
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
    }
    for (var item in headLines) {
      print(item + '---');
    }
    setState(() {
      isLoaded = true;
    });
    return decodedResp;
  }

  onTapped(index) {
    print(index);
    setState(
      () {
        _currentIndex = index;
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final List _children = [Home(), Entertainment(), Corona(), India()];
    return DefaultTabController(
      length: 7,
      child: Scaffold(
        appBar: AppBar(
          backgroundColor: Colors.lightBlue[900],
          centerTitle: true,
          leading: Icon(Icons.person_outline),
          title: Text(
            'NewMours',
            style: TextStyle(fontSize: 16.0),
          ),
          /* bottom: PreferredSize(
              child: TabBar(
                  isScrollable: true,
                  unselectedLabelColor: Colors.white.withOpacity(0.3),
                  indicatorColor: Colors.white,
                  tabs: [
                    Tab(
                      child: Text('Home'),
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
              preferredSize: Size.fromHeight(30.0)), */
          actions: <Widget>[
            Padding(
              padding: const EdgeInsets.only(right: 16.0),
              child: Icon(Icons.add_alert),
            ),
          ],
        ),
        body: Container(
          child: _children[_currentIndex],
        ),
        /* TabBarView(
          children: <Widget>[
            Container(
              child: Center(
                child: Text('Home'),
              ),
            ),
            Container(
              child: Center(child: Text('ent')),
            ),
            Container(
              child: Center(
                  child: isLoaded
                      ? ListView.builder(
                          itemCount: 6,
                          itemBuilder: (context, i) {
                            return Padding(
                              padding: const EdgeInsets.all(8.0),
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
                                                child:
                                                    Image.network(imgLink[i])),
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
                                      AutoSizeText(
                                        link[i],
                                        style: TextStyle(
                                            color: Colors.blue,
                                            decoration:
                                                TextDecoration.underline),
                                        // maxFontSize: 25,
                                        minFontSize: 16,
                                        maxLines: 1,
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                            );
                          },
                        )
                      : CircularProgressIndicator()),
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
        ), */
        bottomNavigationBar: BottomNavigationBar(
          backgroundColor: Colors.lightBlue[900],
          unselectedLabelStyle:
              TextStyle(color: Colors.blue, decorationColor: Colors.black),
          selectedItemColor: Colors.greenAccent,
          currentIndex: _currentIndex,
          showUnselectedLabels: true,
          items: [
            BottomNavigationBarItem(
              backgroundColor: Colors.lightBlue[900],
              icon: Icon(Icons.search),
              title: Text(
                'Home',
                style: TextStyle(color: Colors.white),
              ),
              // label: 'Home',
            ),
            BottomNavigationBarItem(
              icon: Icon(
                Icons.monetization_on,
              ),
              title: Text(
                'Entertainment',
                style: TextStyle(color: Colors.white),
              ),
              //label: 'Entertainment',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.pie_chart),
              title: Text(
                'Corona',
                style: TextStyle(color: Colors.white),
              ),
              // label: 'Corona',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.pie_chart),
              title: Text(
                'India',
                style: TextStyle(color: Colors.white),
              ),
              //label: 'Corona',
            ),
          ],
          onTap: onTapped,
        ),
      ),
    );
  }
}
