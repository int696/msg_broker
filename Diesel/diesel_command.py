
class DieselCommand:
    def __init__(self, client):
        self.client = client

    def command_read_holding_registers(self, address, count, slave):
        data = self.client.read_holding_registers(address=address, count=count, slave=slave)
        return int(''.join(map(str, data.registers)))

    def command_read_input_registers(self, address, count, slave):
        data = self.client.read_input_registers(address=address, count=count, slave=slave)
        return int(''.join(map(str, data.registers)))

    def get_data_bool(self, address, count, slave):
        data = self.client.read_discrete_inputs(address=address, count=count, slave=slave)
        return data.bits

    def command_write_coil(self, address, value, slave):

        self.client.write_coil(address=address, value=value, slave=slave)

    def command_write_registers(self, address, value, slave):
        self.client.write_registers(address=address, values=value, slave=slave)

