import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'cam2.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';
//import 'package:dio/dio.dart';
import 'dart:convert' as convert;
import 'package:camera/camera.dart';
import 'package:path/path.dart';
import 'package:path_provider/path_provider.dart';
import 'dart:convert';
import 'dart:typed_data';
import 'main.dart';

class Display extends StatefulWidget {
  String imagePathReceived1;
  String imagePathReceived2;

  Display({this.imagePathReceived1, this.imagePathReceived2});
  @override
  _DisplayState createState() => _DisplayState();
}

class _DisplayState extends State<Display> {
  String something = "";
  Uint8List bytes;
  String yo = "";
  TextEditingController inputController = new TextEditingController();
  Future _getImage() async {
    String base64Image1;
    String base64Image2;
    setState(() {
      yo = 'Wait some time!';
    });
    //Response response;
    File _image1 = File(widget.imagePathReceived1);
    File _image2 = File(widget.imagePathReceived2);
    List<int> imageBytes1 = await _image1.readAsBytes();
    base64Image1 = base64Encode(imageBytes1);
    List<int> imageBytes2 = await _image2.readAsBytes();
    base64Image2 = base64Encode(imageBytes2);
    // print(base64Image);
    /* response =+
        await dio.post("http://127.0.0.1:5000/", data: {"image": base64Image});*/

    var url = 'http://192.168.1.7:5000/';
    //'http://10.0.2.2:5000/';
    var response = await http.post(
      url,
      body: {
        "image1": " ${base64Image1}",
        "image2": " ${base64Image2}",
        "iter": inputController.text,
      },
    );
    var jsonResponse = convert.jsonDecode(response.body);
    //print(jsonResponse['total_experience']);

    setState(() {
      something = jsonResponse;
      something = something.substring(2, something.length - 1);
      //Uint8List byteso = utf8.encode(something);

      bytes = Base64Codec().decode(something);
    });
  }

  @override
  Widget build(BuildContext context) {
    if (bytes == null)
      return Scaffold(
        appBar: AppBar(
          title: Text('Lets Style'),
        ),
        body: Column(children: <Widget>[
          Flexible(
            fit: FlexFit.tight,
            child: Text(yo),
          ),
          Container(
              color: Colors.blueGrey,
              alignment: Alignment.bottomCenter,
              height: 60,
              child: Row(children: <Widget>[
                RaisedButton(
                  onPressed: this._getImage,
                  child: Container(
                    // decoration: const BoxDecoration(color: Colors.teal),
                    child: const Text('GO', style: TextStyle(fontSize: 20)),
                  ),
                ),
                SizedBox(
                  width: 40,
                ),
                Expanded(
                    child: Container(
                  width: 0.2,
                  height: 10000,
                  child: TextField(
                    style: TextStyle(
                        fontSize: 45.0, height: 2.0, color: Colors.black),
                    controller: inputController,
                    keyboardType: TextInputType.number,
                    decoration: InputDecoration(
                      hintText: '   Iterations?',
                      hintStyle:
                          TextStyle(fontSize: 20.0, color: Colors.redAccent),
                    ),
                  ),
                )),
                RaisedButton(
                  onPressed: () {
                    restart(context);
                  },
                  child: Container(
                    // decoration: const BoxDecoration(color: Colors.teal),

                    child: const Text('Again?', style: TextStyle(fontSize: 20)),
                  ),
                ),
              ]))
        ]),
      );
    return Scaffold(
        appBar: AppBar(
          title: Text('Lets Style'),
        ),
        body: Column(children: <Widget>[
          Flexible(
              flex: 10,
              fit: FlexFit.tight,
              child: Container(child: Image.memory(bytes, fit: BoxFit.cover))),
          Container(
              color: Colors.blueGrey,
              alignment: Alignment.bottomCenter,
              height: 60,
              child: Row(children: <Widget>[
                RaisedButton(
                  onPressed: this._getImage,
                  child: Container(
                    // decoration: const BoxDecoration(color: Colors.teal),
                    child: const Text('GO', style: TextStyle(fontSize: 20)),
                  ),
                ),
                SizedBox(
                  width: 40,
                ),
                Expanded(
                    child: Container(
                  width: 0.2,
                  height: 10000,
                  child: TextField(
                    style: TextStyle(
                        fontSize: 45.0, height: 2.0, color: Colors.black),
                    controller: inputController,
                    keyboardType: TextInputType.number,
                    decoration: InputDecoration(
                      hintText: '   Iterations?',
                      hintStyle: TextStyle(fontSize: 20.0, color: Colors.white),
                    ),
                  ),
                )),
                RaisedButton(
                  onPressed: () {
                    restart(context);
                  },
                  child: Container(
                    // decoration: const BoxDecoration(color: Colors.teal),

                    child: const Text('Again?', style: TextStyle(fontSize: 20)),
                  ),
                ),
              ]))
        ]));
  }
}

void restart(context) async {
  Navigator.push(
      context, MaterialPageRoute(builder: (context) => CameraScreen()));
}
