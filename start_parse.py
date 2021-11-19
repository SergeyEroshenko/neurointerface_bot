import asyncio
from argparse import ArgumentParser
from neurointerface_lib.connector import Connector
from neurointerface_lib.parser import Parser, DBWriter
from clickhouse_driver import Client


async def timer(seconds: int):
    await asyncio.sleep(seconds)
    exit()
    # loop = asyncio.get_event_loop()
    # tasks = asyncio.all_tasks(loop)
    # for task in tasks:
    #     task.done()
    # await loop.close()


async def main(human_id, label):
    conn = Connector(device_id="0446", freq=5)
    parser = Parser()
    db_conn = Client(
        host='135.181.250.122',
        port='9090',
        password='',
        database=f'human_{human_id}')
    db_writer = DBWriter(db_conn, label)

    conn.attach(db_writer)
    conn.attach(parser)
    await conn.connect()
    # await conn.enable_data_grab_mode()
    tasks = [
        conn.handler(),
        conn.rhythms_history(),
        # conn.rhythms(),
        timer(10)
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

    client = Client(host='135.181.250.122', port='9090', password='')
    database_name = f"human_{human_id}"
    client.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    client.disconnect()
    print(f"Database name is: {database_name}\nAction label is: {label}")
    asyncio.run(main(human_id, label))
