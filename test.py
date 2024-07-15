from Connected.connection_db import add_user
from Request.command_operator import Command
from Connected.contact_mqtt import connection

connect = add_user()
mqttc = connection()
operator = Command(mqttc, connect)

operator.update_param_em((178, 2, 3))
