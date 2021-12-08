import asyncio
from argparse import ArgumentParser
from neurointerface_lib.connector import Connector
from neurointerface_lib.parser import Parser, DBWriter
from db_settings import db_conn_params
from clickhouse_driver import Client


async def inspector(time: int):
    await asyncio.sleep(time)
    print("close all coro ")
    # for task in asyncio.all_tasks():
    #     print(task)
    tasks = asyncio.all_tasks()
    for task in tasks:
        task_name = task.get_name()
        coro_type = str(task.get_coro())
        if ("main()" not in coro_type) | ("inspector()" not in coro_type):
            # task.cancel()
            print(task_name, " is closed. ", len(list(asyncio.all_tasks())))
        await asyncio.sleep(0.01)
    list(asyncio.all_tasks())[0].cancel()
    

async def main(human_id, label):
    conn = Connector(device_id="0446", freq=5)
    parser = Parser()
    db_conn = Client(database=f'human_{human_id}', **db_conn_params)
    db_writer = DBWriter(db_conn, label)

    conn.attach(db_writer)
    conn.attach(parser)
    await conn.connect()
    await conn.enable_data_grab_mode()
    tasks = [
        conn.handler(),
        conn.rhythms_history(),
        # conn.rhythms(),
        inspector(time=1)
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    argparser = ArgumentParser()
    argparser.add_argument("--id", help="Human id")
    argparser.add_argument(
        "--label", help="Label for data sample. Coded action name.")
    args = argparser.parse_args()
    human_id = args.id
    label = args.label

    client = Client(**db_conn_params)
    database_name = f"human_{human_id}"
    client.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    client.disconnect()
    print(f"Database name is: {database_name}\nAction label is: {label}")
    asyncio.run(main(human_id, label))
