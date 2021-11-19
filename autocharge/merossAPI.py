import asyncio
from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager
import logging

def turn_onoff(email: str, password: str, uuid: str, turn_on: bool):

    meross_root_logger = logging.getLogger("meross_iot")
    meross_root_logger.setLevel(logging.CRITICAL)
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    async def main():
        http_api_client = await MerossHttpClient.async_from_user_password(email=email, password=password)

        manager = MerossManager(http_client=http_api_client)
        await manager.async_init()

        await manager.async_device_discovery()
        plugs = manager.find_devices(device_uuids=uuid)

        if len(plugs) < 1:
            raise RuntimeError('ERROR: Meross device unreachable')
        else:
            dev = plugs[0]
            await dev.async_update()

            if turn_on == True:
                await dev.async_turn_on(channel=0)
            elif turn_on == False:
                await dev.async_turn_off(channel=0)
        
        manager.close()
        await http_api_client.async_logout()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.stop()

if __name__ == '__main__':
    email = 'ricky_barry@hotmail.com'
    password = 'Cyber001'
    uuid = '20051817743225251h4048e1e91c57c2'
    turn_onoff(email, password, uuid, turn_on=True)