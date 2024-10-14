class DieselCommand:
    def __init__(self, client):
        # Инициализация объекта класса DieselCommand
        # client - объект для взаимодействия с модулем Modbus
        self.client = client

    def command_read_holding_registers(self, address, count, slave):
        # Чтение удерживаемых регистров (holding registers)
        # address - начальный адрес регистра
        # count - количество регистров для чтения
        # slave - идентификатор ведомого устройства (slave)
        data = self.client.read_holding_registers(address=address, count=count, slave=slave)
        print(data.registers, address, slave)  # Вывод данных регистров, адреса и идентификатора slave
        if not data.registers:
            return 0  # Если данные отсутствуют, возвращаем 0
        return data.registers  # Возвращаем список значений регистров

    def command_read_input_registers(self, address, count, slave):
        # Чтение входных регистров (input registers)
        # address - начальный адрес регистра
        # count - количество регистров для чтения
        # slave - идентификатор ведомого устройства (slave)
        data = self.client.read_input_registers(address=address, count=count, slave=slave)
        if not data.registers:
            return 0  # Если данные отсутствуют, возвращаем 0
        return data.registers  # Возвращаем список значений регистров

    def get_data_bool(self, address, count, slave):
        # Чтение дискретных входов (discrete inputs)
        # address - начальный адрес дискретного входа
        # count - количество входов для чтения
        # slave - идентификатор ведомого устройства (slave)
        data = self.client.read_discrete_inputs(address=address, count=count, slave=slave)
        return data.bits  # Возвращаем список значений дискретных входов (булевы значения)

    def command_write_coil(self, address, value, slave):
        # Запись значения в один дискретный выход (coil)
        # address - адрес дискретного выхода
        # value - значение для записи (True или False)
        # slave - идентификатор ведомого устройства (slave)
        self.client.write_coil(address=address, value=value, slave=slave)

    def command_write_registers(self, address, value, slave):
        # Запись значений в несколько регистров
        # address - начальный адрес регистра
        # value - список значений для записи
        # slave - идентификатор ведомого устройства (slave)
        self.client.write_registers(address=address, values=value, slave=slave)

