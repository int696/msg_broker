# Импортируем необходимые модули и функции для работы с базой данных, MQTT, эмуляторами и командными операциями.
from Connected.connection_db import add_user
from Connected.contact_mqtt import connection
from Connected.emulators_connect import ContactEmulators
from Emulators.emulators_command import CommandEmulators
from Emulators.emulators_callback import EmCallback
from Request.command_operator import Command
from utils.create_file_and_path import Util
from utils.publish import Publish


def init_start():
    # Устанавливаем соединение с MQTT-брокером
    mqttc = connection()

    # Подключаемся к БД
    connect = add_user()

    # Инициализируем объект для обработки команд
    operator = Command(mqttc, connect)

    # Инициализируем объект для работы с файловыми путями и данными
    data_path = Util()

    # Создаем объект для публикации данных в MQTT
    publish = Publish(mqttc)

    # Устанавливаем соединение с первым эмулятором
    emulators_contact_one = ContactEmulators("EM_ONE")
    emulators_contact_one.connection_sim(data_path.get_data_path("setting.ini"))
    emulators_command_one = CommandEmulators(emulators_contact_one.socket)
    emulators_callback_one = EmCallback(mqttc, emulators_contact_one, emulators_command_one)

    # Устанавливаем соединение со вторым эмулятором
    emulators_contact_two = ContactEmulators("EM_TWO")
    emulators_contact_two.connection_sim(data_path.get_data_path("setting.ini"))
    emulators_command_two = CommandEmulators(emulators_contact_two.socket)
    emulators_callback_two = EmCallback(mqttc, emulators_contact_two, emulators_command_two)

    # Отправляем в MQTT информацию о сокетах эмуляторов
    publish.push_name_socket(emulators_contact_one, "em_1")
    publish.push_name_socket(emulators_contact_two, "em_2")

    # Получаем параметры для эмуляторов из базы данных
    em_param = operator.get_param_em(tables="Параметры_имитатора")

    # Отправляем команды на настройку параметров первого эмулятора
    emulators_callback_one.push_command({
        "SYST:INT:SIM:SET VOC_STC,": em_param[1],
        "SYST:INT:SIM:SET ISC_STC,": em_param[2],
        "SYST:INT:SIM:SET VMPP_STC,": em_param[3],
        "SYST:INT:SIM:SET IMPP_STC,": em_param[4],
        "SYST:INT:SIM:SET ALPHA,": em_param[5],
        "SYST:INT:SIM:SET BETA,": em_param[6],
        "SYST:INT:SIM:SET TSTC,": 25,
        "SYST:INT:SIM:SET GSTC,": 1000
    })

    print()  # Выводим пустую строку для разделения вывода

    # Отправляем команды на настройку параметров второго эмулятора
    emulators_callback_two.push_command({
        "SYST:INT:SIM:SET VOC_STC,": em_param[1],
        "SYST:INT:SIM:SET ISC_STC,": em_param[2],
        "SYST:INT:SIM:SET VMPP_STC,": em_param[3],
        "SYST:INT:SIM:SET IMPP_STC,": em_param[4],
        "SYST:INT:SIM:SET ALPHA,": em_param[5],
        "SYST:INT:SIM:SET BETA,": em_param[6],
        "SYST:INT:SIM:SET TSTC,": 25,
        "SYST:INT:SIM:SET GSTC,": 1000
    })

    print()  # Выводим пустую строку для разделения вывода

    # Получаем обратную связь от первого и второго эмуляторов
    emulators_callback_one.callback_data()
    emulators_callback_two.callback_data()

    # Основной цикл для обработки команд управления эмуляторами
    while True:
        # Проверяем состояние всех подключений
        while operator.check_connections("start_stop_all"):
            # Проверка на запуск скрипта ДГУ
            if operator.check_connections("start_stop_em"):
                # Обрабатываем команду управления эмулятором 1: установка температуры и солнечной радиации
                emulators_callback_one.command_processing_em(
                    operator.check_connections("start_stop_em"),
                    "SYST:INT:SIM:SET TPV,",
                    operator.get_param_em(tables="sim_TG")[1]
                )

                emulators_callback_one.command_processing_em(
                    operator.check_connections("start_stop_em"),
                    "SYST:INT:SIM:SET GPV,",
                    operator.get_param_em(tables="sim_TG")[2]
                )

                # Обрабатываем команду управления эмулятором 2: установка температуры и солнечной радиации
                emulators_callback_two.command_processing_em(
                    operator.check_connections("start_stop_em"),
                    "SYST:INT:SIM:SET TPV,",
                    operator.get_param_em(tables="sim_TG")[1]
                )

                emulators_callback_two.command_processing_em(
                    operator.check_connections("start_stop_em"),
                    "SYST:INT:SIM:SET GPV,",
                    operator.get_param_em(tables="sim_TG")[2]
                )

                # Получаем данные от эмуляторов и публикуем их через MQTT
                emulators_contact_one.get_data_emulators()
                emulators_contact_two.get_data_emulators()
                publish.publish_data_emulators(emulators_contact_one)
                publish.publish_data_emulators(emulators_contact_two)

                # Обновляем параметры для первого эмулятора в базе данных
                c = ["power_sum_1", "voltage_1", "current_1"]
                operator.update_param_em([
                    emulators_contact_one.power,
                    emulators_contact_one.result[0],
                    emulators_contact_one.result[1]
                ], c)

                # Обновляем параметры для второго эмулятора в базе данных
                c = ["power_sum_2", "voltage_2", "current_2"]
                operator.update_param_em([
                    emulators_contact_two.power,
                    emulators_contact_two.result[0],
                    emulators_contact_two.result[1]
                ], c)

                # Обновляем суммарные параметры для обоих эмуляторов в базе данных
                c = ['power_sum', 'voltage', 'current']
                operator.update_param_em([
                    float(emulators_contact_one.power) + float(emulators_contact_two.power),
                    float(emulators_contact_one.result[0]) + float(emulators_contact_two.result[0]),
                    float(emulators_contact_one.result[1]) + float(emulators_contact_two.result[1])
                ], c)

            else:
                # Если управление эмуляторами отключено, посылаем команду отключения
                emulators_callback_one.command_processing_em(False, "OUTPUT, ", 0)
                emulators_callback_two.command_processing_em(False, "OUTPUT, ", 0)
        else:
            # Отключаем эмуляторы и закрываем соединения, если управление всеми эмуляторами остановлено
            emulators_callback_one.command_processing_em(False, "OUTPUT, ", 0)
            emulators_callback_two.command_processing_em(False, "OUTPUT, ", 0)
            emulators_contact_one.close_socket()  # Закрываем сокет для первого эмулятора
            emulators_contact_two.close_socket()  # Закрываем сокет для второго эмулятора
            break  # Прерываем цикл, завершая выполнение программы


if __name__ == '__main__':
    # Запускаем основную функцию при запуске скрипта
    init_start()

