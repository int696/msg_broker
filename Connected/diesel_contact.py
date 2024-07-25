from pymodbus.client.serial import ModbusSerialClient


def diesel_contact():
    try:
        client = ModbusSerialClient(method='rtu', port='COM4', baudrate=19200,
                                         bytesize=8, parity='N', stopbits=1)
        return client
    except Exception as e:
        print(e)

