from pymodbus.client.serial import ModbusSerialClient  # Импортируем класс (библиотека) для работы с Modbus по последовательному порту


# Функция для создания подключения к дизельному генератору через Modbus
def diesel_contact():

    try:
        # Инициализируем Modbus-клиент для работы через последовательный порт (RTU)
        client = ModbusSerialClient(
            method='rtu',  # Указываем метод передачи данных - RTU
            port='COM3',  # порт машины на которой работает скрипт
            baudrate=19200,  # Устанавливаем скорость передачи данных (19200 бод)
            bytesize=8,  # Устанавливаем размер байта (8 бит)
            parity='N',  # Устанавливаем проверку четности (нет)
            stopbits=1  # Устанавливаем количество стоп-битов (1)
        )
        return client  # Возвращаем объект клиента для дальнейшего использования

    except Exception as e:  # Обработка исключений в случае ошибки при подключении
        print(e)  # Выводим сообщение об ошибке