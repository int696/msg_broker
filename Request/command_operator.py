

class Command:

    def __init__(self, mqttc, connect):
        self.parsed_data = None
        self.mqttc = mqttc
        self.connect = connect

    def callback_data(self, topic='mpei/command/on_off'):
        self.mqttc.message_callback_add(topic, self.get_data)

    def get_data(self, client, userdata, data):
        try:
            self.parsed_data = int(data.payload.decode())
            if self.parsed_data:
                print("Команда вкл.", self.parsed_data)
            else:
                print('Команды выкл', self.parsed_data)
        except Exception as e:
            print(f"Ошибка при обработке данных: {e}")

    def validate_data(self, data):
        pass


    def check_connections(self, column):
        cursor = self.connect.cursor()
        cursor.execute("SELECT * FROM control_signal WHERE id ='1'")
        start_stop = cursor.fetchone()[column]
        cursor.close()
        return start_stop

    def get_param_em(self, tables):
        cursor = self.connect.cursor()
        cursor.execute(f"SELECT * FROM {tables} WHERE id ='1'")

        param_em = list(cursor.fetchall()[0].values())
        cursor.close()
        return param_em

    def get_available_dgu(self):
        cursor = self.connect.cursor()
        cursor.execute("SELECT * FROM control_dgu")
        excluded_engines = list(cursor.fetchall()[0].values())[2:]
        return excluded_engines

    def update_current_power(self, data, dgu):
        cursor = self.connect.cursor()
        query = (f"UPDATE ДГУ_текущее_состояние_параметров "
                 f"SET "
                 f"P_L1_DG = %s, "
                 f"P_L2_DG = %s, "
                 f"P_L3_DG = %s, "
                 f"I_L1_DG = %s, "
                 f"I_L2_DG = %s, "
                 f"I_L3_DG = %s "
                 f"WHERE slave = {dgu}")

        cursor.execute(query, list(data))
        cursor.close()

    def get_excluded_engines(self):
        cursor = self.connect.cursor()
        cursor.execute("SELECT * FROM control_dgu_new")
        excluded_engines = cursor.fetchall()
        cursor.close()
        return excluded_engines

    def update_excluded_engines(self, available_dgu, status):
        cursor = self.connect.cursor()
        for dgu in available_dgu:
            cursor.execute(f"UPDATE control_dgu_new SET control_dgu = {status} WHERE slave = {dgu['slave']}")
        cursor.close()

    def update_control_signal(self, column, status):
        cursor = self.connect.cursor()
        cursor.execute(f"UPDATE control_signal SET {column} = {status} WHERE id = 1")
        cursor.close()

    # def update_param_em(self, params):
    #     c = ["power_sum_1", "voltage_1", "current_1"]
    #     cursor = self.connect.cursor()
    #     for i in range(len(params)):
    #         cursor.execute(f"UPDATE solar_station SET {c[i]} = {params[i]}")
    #
    #     cursor.close()

    def update_param_em(self, params, c):
        cursor = self.connect.cursor()
        query = (f"UPDATE solar_station "
                 f"SET "
                 f"{c[0]} = %s, "
                 f"{c[1]} = %s, "
                 f"{c[2]} = %s")
        cursor.execute(query, params)
        cursor.close()

    def update_param_victron(self, c, params):
        print(c, len(c))
        print(params, len(params))
        cursor = self.connect.cursor()
        print('update')
        query = (f"UPDATE energy_storage_system "
                 f"SET "
                 f"{c[0]} = %s,"
                 f"{c[1]} = %s,"
                 f"{c[2]} = %s,"
                 f"{c[3]} = %s,"
                 f"{c[4]} = %s,"
                 f"{c[5]} = %s,"
                 f"{c[6]} = %s,"
                 f"{c[7]} = %s,"
                 f"{c[8]} = %s,"
                 f"{c[9]} = %s,"
                 f"{c[10]} = %s,"
                 f"{c[11]} = %s,"
                 f"{c[12]} = %s,"
                 f"{c[13]} = %s")
        cursor.execute(query, params)
        cursor.close()

    def get_setting(self):
        cursor = self.connect.cursor()
        cursor.execute("SELECT * FROM settings")
        setting = cursor.fetchall()[0]
        cursor.close()
        return setting
