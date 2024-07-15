import asyncio
from asyncio import CancelledError
from Connected.contact_mqtt import connection
from Victron.victron_contact import VictronCommand
from utils.create_file_and_path import Util
from Connected.connection_db import add_user
from Request.command_operator import Command

async def delay(victron):
    while True:
        victron.survey_victron()
        await asyncio.sleep(15)


async def init_start():
    mqttc = connection()
    connect = add_user()
    operator = Command(mqttc, connect)

    data_path = Util()
    victron = VictronCommand(mqttc)
    # topic_victron = data_path.open_json("data_topics_client.json")
    victron.callback_data(data_path.open_json("data_topics_victron.json"))
    # victron.callback_data_all(data_path.open_csv)
    survey = asyncio.create_task(delay(victron))
    while not survey.done():
        operator.update_param_victron(
            list(victron.dict_msg.keys()), list(victron.dict_msg.values()))

        await asyncio.sleep(1)
    try:
        await survey
    except CancelledError:
        print('Задача survey была снята')


if __name__ == '__main__':
    asyncio.run(init_start())
