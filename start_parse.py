import asyncio
from neurointerface_lib.connector import Connector
from neurointerface_lib.parser import Parser


async def main(conn: Connector):
    parser = Parser()
    conn.attach(parser)
    await conn.connect()
    await conn.enable_data_grab_mode()
    tasks = [
        conn.handler(),
        conn.subscribe_rhytms(),
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':

    conn = Connector(device_id="0446", freq=200)
    asyncio.run(main(conn))