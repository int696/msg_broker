import time

from Connected.connection_db import add_user
from Connected.contact_mqtt import connection
from Diesel.diesel_command import DieselCommand
from Diesel.diesel_callback import DieselCallbackBD
from Connected.diesel_contact import diesel_contact
from Request.command_operator import Command


def init_start():
    mqttc = connection()
    connect = add_user()
    operator = Command(mqttc, connect)
    diesel = diesel_contact()
    diesel_command = DieselCommand(diesel)
    diesel_callback = DieselCallbackBD(diesel_command)
    flag_start_stop_all = False
    diesel_command.command_write_coil(27, 1, slave=3)

    while True:
        while operator.check_connections("start_stop_all"):
            if operator.check_connections("start_stop_diesel"):
                # diesel_callback.checking_work_status(slave=3, address=7, count=1)
                # diesel_callback.checking_work_status(slave=3, address=19, count=1)
                diesel_callback.command_processing_diesel(operator.get_excluded_engines())
                diesel_callback.get_power_dgu(2)
                diesel_callback.get_power_dgu(3)
                diesel_callback.get_current_dgu(2)
                diesel_callback.get_current_dgu(3)
                operator.update_current_power(diesel_callback.get_power_current())
            else:
                operator.update_excluded_engines(operator.get_excluded_engines(), 0)
                diesel_callback.command_processing_diesel(operator.get_excluded_engines())
            flag_start_stop_all = True

        else:
            if flag_start_stop_all:
                operator.update_excluded_engines(operator.get_excluded_engines(), 0)
                operator.update_control_signal('start_stop_diesel', 0)
                diesel_callback.command_processing_diesel(operator.get_excluded_engines())
                operator.update_current_power(diesel_callback.get_power_current())
                flag_start_stop_all = False


if __name__ == '__main__':
    init_start()
