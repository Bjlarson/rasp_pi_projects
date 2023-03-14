import React, { useState, useEffect } from 'react';
import { View, Text, Button } from 'react-native';
import BluetoothSerial from 'react-native-bluetooth-serial';

const App = () => {
  const [device, setDevice] = useState();
  const [connection, setConnection] = useState();

  useEffect(() => {
    BluetoothSerial.list().then(devices => {
      setDevice(devices[0]);
    });
  }, []);

  const connect = async () => {
    if (!device) return;

    try {
      const connection = await BluetoothSerial.connect(device.id);
      setConnection(connection);
    } catch (e) {
      console.error(e);
    }
  };

  const sendMessage = async message => {
    if (!connection) return;

    try {
      await connection.write(message);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <View>
      <Text>Bluetooth device: {device ? device.name : 'None found'}</Text>
      {device && (
        <Button title="Connect" onPress={connect} />
      )}
      {connection && (
        <>
          <Button title="Send Message" onPress={() => sendMessage('Hello, Bluetooth!')} />
        </>
      )}
    </View>
  );
};

export default App;

