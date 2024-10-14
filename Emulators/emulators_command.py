class CommandEmulators:

    def __init__(self, socket):
        # Инициализация объекта класса CommandEmulators
        # socket - сокетное соединение, через которое будут отправляться команды эмулятору
        self.socket = socket
        # Список допустимых источников сигналов, которые могут быть установлены
        self.validSrcList = ["front", "web", "seq", "eth", "slot1", "slot2", "slot3", "slot4", "loc", "rem"]

    def send_command(self, msg):
        # Метод для отправки команды через сокетное соединение
        # msg - строка с командой для отправки
        try:
            print(f"Calling command: {msg}")
            # Добавление символа новой строки в конец команды
            msg = msg + "\n"
            # Отправка команды через сокетное соединение
            self.socket.sendall(msg.encode("UTF-8"))
        except Exception as e:
            # Обработка возможных исключений при отправке команды
            print(e)

    def set_prog_source_v(self, src):
        # Метод для установки источника напряжения (Voltage) для программного управления
        # src - строка, указывающая на источник (должен быть в списке validSrcList)
        retval = 0
        if src in self.validSrcList:
            # Если источник валиден, отправляем команду на установку источника напряжения
            self.send_command("SYST:REM:CV {0}".format(src))
        else:
            # Если источник не валиден, возвращаем -1 как ошибку
            retval = -1
        return retval

    def set_prog_source_i(self, src):
        # Метод для установки источника тока (Current) для программного управления
        # src - строка, указывающая на источник (должен быть в списке validSrcList)
        retval = 0
        if src.lower() in self.validSrcList:
            # Если источник валиден, отправляем команду на установку источника тока
            self.send_command("SYST:REM:CC {0}".format(src))
        else:
            # Если источник не валиден, возвращаем -1 как ошибку
            retval = -1
        return retval
