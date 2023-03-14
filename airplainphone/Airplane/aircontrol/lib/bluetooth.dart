import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:flutter_bluetooth_serial/flutter_bluetooth_serial.dart';

class MyBluetoothPage extends StatefulWidget {
  @override
  _MyBluetoothPageState createState() => _MyBluetoothPageState();
}

class _MyBluetoothPageState extends State<MyBluetoothPage> {
  BluetoothState _bluetoothState = BluetoothState.UNKNOWN;
  String _address = "...";
  String _name = "...";
  BluetoothConnection? _connection;
  String receivedMessage = "";
  List<BluetoothDevice> _devices = [];
  BluetoothDevice? _selected_device;

  @override
  void initState() {
    super.initState();

    // Request permissions to use Bluetooth
    FlutterBluetoothSerial.instance.state.then((state) {
      setState(() {
        _bluetoothState = state;
  });});

  Future.doWhile(() async {
    //Wait if adapter not enabled
    if (await FlutterBluetoothSerial.instance.isEnabled?? false) {
      return false;
    }
    await Future.delayed(Duration(microseconds: 0xDD));
    return true;
  }).then((_) {
    //Update the address field
    FlutterBluetoothSerial.instance.address.then((address) {
      setState(() {
        _address = address!;
      });
    });
  });

  FlutterBluetoothSerial.instance.name.then((name) {
    setState(() {
      _name = name!;
    });
  });

  FlutterBluetoothSerial.instance.onStateChanged().listen((BluetoothState state) {
    setState(() {
      _bluetoothState = state;
    });
   });
  }
  

  void scanForDevices() async {
    // Get a list of available Bluetooth devices
    List<BluetoothDevice> devices = await FlutterBluetoothSerial.instance.getBondedDevices();
    setState(() {
      _devices = devices;
    });
  }

  void connectToDevice(BluetoothDevice device) async {
    // Connect to a Bluetooth device
    BluetoothConnection.toAddress(device.address).then((value) => {
    setState(() {
      _connection = value;
      _selected_device = device;
    }),

    // Start listening for incoming data
    startListening(),
    });
  }

  void startListening() {
    _connection?.input?.listen((Uint8List data) {
      // Decode the received data as a string
      String message = utf8.decode(data);

      // Update the received message
      setState(() {
        receivedMessage = message;
      });
    });
  }

  void sendData(String message) async {
    // Send data to the connected Bluetooth device
    _connection?.output.add([utf8.encode(message)] as Uint8List);
    await _connection?.output.allSent;
  }
  @override
  void dispose() {
    FlutterBluetoothSerial.instance.setPairingRequestHandler(null);
    super.dispose();
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            SwitchListTile(title: const Text('Enable Bluetooth'),
             value: _bluetoothState.isEnabled,
             onChanged: (bool value) {
               future() async {
                if (value)
                  await FlutterBluetoothSerial.instance.requestEnable();
                else {
                  await FlutterBluetoothSerial.instance.requestDisable();
                }
               }

               future().then((_) {
                setState(() {});
               });
             }),
             ListTile(
              title: const Text('Local adapter address'),
              subtitle: Text(_address),
             ),
             ListTile(title: const Text('Local adapter name'),
              subtitle: Text(_name),
              onLongPress: null,
             ),
            ElevatedButton(
              onPressed: scanForDevices,
              child: Text("Scan for Devices"),
            ),
            _devices.length == 0 && _selected_device == null
                ? Text("No Devices Found")
                : Expanded(
                    child: ListView.builder(
                      itemCount: _devices.length,
                      itemBuilder: (context, index) {
                        return ListTile(
                          title: Text(_devices[index].name.toString()),
                          subtitle: Text(_devices[index].address),
                          onTap: () {
                            connectToDevice(_devices[index]);
                          },
                        );
                      },
                    ),
                  ),
            _selected_device == null
                ? Text("No Device Connected")
                : Column(
                    children: <Widget>[
                      Text('Connected Device: $_selected_device?.name'),
                      ElevatedButton(
                        onPressed: () {
                          sendData("Hello");
                        },
                      child: Text("Send Data"),
                    ),
                    Text("Received Message: $receivedMessage"),
                    ],
                  ),
            ],
        ),
      ),
    );
  }
}
