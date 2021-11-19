import asyncio
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
import time

def scan_for_data(manufac_num: int, timeout = 30):
    data_lst = [None, None]

    def callback(device: BLEDevice, advertisement_data: AdvertisementData):
        data = advertisement_data.manufacturer_data.get(manufac_num)

        if not data:
            return
        elif len(data) == 14:
            data_lst[0] = data
        elif len(data) == 25:
            data_lst[1] = data


    async def run(timeout):
        scanner = BleakScanner()
        scanner.register_detection_callback(callback)

        t_end = time.time() + timeout
        while data_lst[0]==None and data_lst[1]==None and time.time() < t_end:
            await scanner.start()
            await asyncio.sleep(5.0)
            await scanner.stop()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(timeout))
    loop.stop()

    if len(data_lst) > 0:
        return data_lst
    else:
        raise RuntimeError('ERROR: BLE device unreachable')

def translate(pckt: bytes):
    info = {}
    
    info["version"] = int.from_bytes(pckt[0:1], byteorder='big')
    info["batt_lvl"] = int.from_bytes(pckt[1:2], byteorder='big')
    info["interval"] = int.from_bytes(pckt[2:4], byteorder='big')
    info["log_count"] = int.from_bytes(pckt[4:6], byteorder='big')
    info["temperature"] = int.from_bytes(pckt[6:8], byteorder='big', signed=True) / 10
    info["humidity"] = int.from_bytes(pckt[8:10], byteorder='big', signed=True) / 10
    info["dew_point"] = int.from_bytes(pckt[10:12], byteorder='big', signed=True) / 10

    return info

if __name__ == '__main__':
    raw_data = scan_for_data(307)
    info = translate(raw_data[0])
    print(raw_data)
    print(info)