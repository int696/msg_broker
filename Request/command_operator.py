class Command:
    def __init__(self, mqttc, connect):
        """
        Инициализация объекта Command.

        :param mqttc: Объект клиента MQTT для работы с брокером.
        :param connect: Объект подключения к базе данных.
        """
        self.parsed_data = None
        self.mqttc = mqttc
        self.connect = connect

    def callback_data(self, topic='mpei/command/on_off'):
        """
        Настройка колбэка для обработки сообщений MQTT на указанном топике.

        :param topic: Топик для подписки.
        """
        self.mqttc.message_callback_add(topic, self.get_data)

    def get_data(self, client, userdata, data):
        """
        Обработка входящих данных MQTT.

        :param client: Клиент MQTT.
        :param userdata: Пользовательские данные.
        :param data: Сообщение MQTT.
        """
        try:
            self.parsed_data = int(data.payload.decode())
            if self.parsed_data:
                print("Команда включена.", self.parsed_data)
            else:
                print('Команда выключена', self.parsed_data)
        except Exception as e:
            print(f"Ошибка при обработке данных: {e}")

    def validate_data(self, data):
        """
        Проверка данных. На данный момент метод не используется.

        :param data: Данные для проверки.
        """
        pass

    def check_connections(self, column):
        """
        Проверка значения в колонке таблицы управления сигналами.

        :param column: Название колонки для проверки.
        :return: Значение в указанной колонке.
        """
        cursor = self.connect.cursor()
        cursor.execute("SELECT * FROM Сигнал_управления WHERE id = '1'")
        start_stop = cursor.fetchone()[column]
        cursor.close()
        return start_stop

    def get_param_em(self, tables):
        """
        Получение параметров из указанной таблицы.

        :param tables: Название таблицы.
        :return: Список параметров.
        """
        cursor = self.connect.cursor()
        cursor.execute(f"SELECT * FROM {tables} WHERE id = '1'")
        param_em = list(cursor.fetchall()[0].values())
        cursor.close()
        return param_em

    def get_available_dgu(self):
        """
        Получение списка исключенных дизельных генераторов.

        :return: Список исключенных генераторов.
        """
        cursor = self.connect.cursor()
        cursor.execute("SELECT * FROM Управление_ДГУ")
        excluded_engines = list(cursor.fetchall()[0].values())[2:]
        return excluded_engines

    def update_current_power(self, data, dgu):
        """
        Обновление данных о текущей мощности и токе для указанного дизельного генератора.

        :param data: Данные о мощности и токе.
        :param dgu: Идентификатор дизельного генератора.
        """
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
        """
        Получение списка исключенных дизельных генераторов.

        :return: Список исключенных генераторов.
        """
        cursor = self.connect.cursor()
        cursor.execute("SELECT * FROM control_dgu_new")
        excluded_engines = cursor.fetchall()
        cursor.close()
        return excluded_engines

    def update_excluded_engines(self, available_dgu, status):
        """
        Обновление статуса для исключенных дизельных генераторов.

        :param available_dgu: Список доступных генераторов.
        :param status: Новый статус.
        """
        cursor = self.connect.cursor()
        for dgu in available_dgu:
            cursor.execute(f"UPDATE control_dgu_new SET control_dgu = {status} WHERE slave = {dgu['slave']}")
        cursor.close()

    def update_control_signal(self, column, status):
        """
        Обновление сигнала управления в таблице control_signal.

        :param column: Название колонки для обновления.
        :param status: Новый статус.
        """
        cursor = self.connect.cursor()
        cursor.execute(f"UPDATE control_signal SET {column} = {status} WHERE id = 1")
        cursor.close()

    def update_param_em(self, params, c):
        """
        Обновление параметров в таблице solar_station.

        :param params: Список значений для обновления.
        :param c: Список названий колонок.
        """
        cursor = self.connect.cursor()
        query = (f"UPDATE Мониторинг_СЭС "
                 f"SET "
                 f"{c[0]} = %s, "
                 f"{c[1]} = %s, "
                 f"{c[2]} = %s")
        cursor.execute(query, params)
        cursor.close()

    def update_param_victron(self, c, params):
        """
        Обновление параметров в таблице energy_storage_system.

        :param c: Список названий колонок.
        :param params: Список значений для обновления.
        """
        print(c, len(c))
        print(params, len(params))
        cursor = self.connect.cursor()
        print('update')
        query = (f"UPDATE energy_storage_system "
                 f"SET "
                 f"{c[0]} = %s, "
                 f"{c[1]} = %s, "
                 f"{c[2]} = %s, "
                 f"{c[3]} = %s, "
                 f"{c[4]} = %s, "
                 f"{c[5]} = %s, "
                 f"{c[6]} = %s, "
                 f"{c[7]} = %s, "
                 f"{c[8]} = %s, "
                 f"{c[9]} = %s, "
                 f"{c[10]} = %s, "
                 f"{c[11]} = %s, "
                 f"{c[12]} = %s, "
                 f"{c[13]} = %s")
        cursor.execute(query, params)
        cursor.close()

    def get_setting(self):
        """
        Получение настроек из таблицы settings.

        :return: Настройки.
        """
        cursor = self.connect.cursor()
        cursor.execute("SELECT * FROM settings")
        setting = cursor.fetchall()[0]
        cursor.close()
        return setting
