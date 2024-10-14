
# Импортируем необходимые модули и функции для работы с базой данных, MQTT, управления дизельными генераторами и обработки команд.
from Connected.connection_db import add_user
from Connected.contact_mqtt import connection
from Diesel.diesel_command import DieselCommand
from Diesel.diesel_callback import DieselCallbackBD
from Connected.diesel_contact import diesel_contact
from Request.command_operator import Command
from utils.control_err import control_f


def init_start():
    # Устанавливаем соединение с MQTT-брокером
    mqttc = connection()

    # Подключаемся к БД
    connect = add_user()

    # Инициализируем объект для обработки команд
    operator = Command(mqttc, connect)

    # Устанавливаем соединение со всеми дизельными генераторами
    diesel = diesel_contact()

    # Создаем объект для отправки команд дизельным генераторам
    diesel_command = DieselCommand(diesel)

    # Создаем объект для обработки обратной связи от дизельных генераторов
    diesel_callback = DieselCallbackBD(diesel_command)

    # Флаг для отслеживания поступления команд об остановки работы всех ДГУ
    # Если приходит команда на останов всех ДГУ флаг меняет свое значение, запускается логическая часть остановки
    # всех ДГУ
    flag_start_stop_all = True

    while True:
        # Проверяем состояние всех подключений
        while operator.check_connections("start_stop_all"):
            flag_start_stop_all = True
            # Проверка на запуск скрипта ДГУ
            if operator.check_connections("start_stop_diesel"):
                # Обрабатываем команды для дизельного генератора, исключая определенные двигатели
                diesel_callback.command_processing_diesel(operator.get_excluded_engines())

                # Получаем текущую мощность и ток для генератора с номером 3
                power_dgu3 = diesel_callback.get_power_dgu(3)
                current_dgu3 = diesel_callback.get_current_dgu(3)

                # Обновляем текущие параметры мощности и тока для генератора 3 в БД
                operator.update_current_power(power_dgu3 + current_dgu3, 3)
            else:
                # Обновляем список исключенных двигателей и устанавливаем флаг остановки всех генераторов
                operator.update_excluded_engines(operator.get_excluded_engines(), 0)
        else:
            # Если был установлен флаг остановки всех генераторов
            if flag_start_stop_all:
                # Обновляем список исключенных двигателей и сигнал управления дизельными генераторами
                operator.update_excluded_engines(operator.get_excluded_engines(), 0)
                operator.update_control_signal('start_stop_diesel', 0)

                # Сбрасываем флаг остановки всех генераторов, чтобы исключить повтор выполнения логики 58-59 строки
                flag_start_stop_all = False


if __name__ == '__main__':
    # Запускаем основную функцию при запуске скрипта
    init_start()
