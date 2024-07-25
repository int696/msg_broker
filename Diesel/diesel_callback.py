from datetime import datetime


class DieselCallbackBD:

    def __init__(self, diesel):

        self.flag = True
        self.diesel = diesel
        self.old_command = 0
        self.old_list_command = []

    def checking_work_status(self, address=3, count=1, slave=2):
        status = self.diesel.get_data_bool(address, count, slave)
        print("Статус работы:", status)

    def ready_auto_launch(self, address=31, count=1, slave=2):
        status = self.diesel.get_data_bool(address, count, slave)

    def get_power_current(self):
        print(f"Мощность ДЭС {self.diesel.command_read_input_registers(address=519, count=1, slave=3)}")

    # def on_off(self, available_dgu, slave, value=True):
    #     if available_dgu:
    #         address = 0
    #     else:
    #         address = 3
    #     self.diesel.command_write_coil(address, value, slave)
    #     print(f"Отправлена команда на slave {slave} address {address} {datetime.now()}")

    # def command_processing_diesel(self, available_dgu):
    #     for dgu in available_dgu:
    #         if dgu not in self.old_list_command:
    #             self.on_off(dgu['control_dgu'], slave=dgu['slave'])
    #     self.old_list_command = available_dgu

    def get_power_dgu(self, slave):
        power = self.diesel.command_read_input_registers(address=516, count=3, slave=slave)
        return power

    def get_current_dgu(self, slave):
        current = self.diesel.command_read_input_registers(address=513, count=3, slave=slave)
        return current