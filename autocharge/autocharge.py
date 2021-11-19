from BlueMaestroAPI import scan_for_data
from BlueMaestroAPI import translate
from SolaxCloudAPI import solax_request
from merossAPI import turn_onoff
from datetime import datetime
import time


while True:

    #start check
    start_tme = datetime.now()
    print(f'\nCheck started at {start_tme.strftime("%H:%M:%S")}')

    #initialise variables
    turn_plug_on = False        #this is so if temp/power is not obtained the switch is turned off
    temp = None
    power = None
    err = False

    #get temperature from BLE sensor
    try:
        raw_data = scan_for_data(307)
        BLE_info = translate(raw_data[0])
        temp = BLE_info['temperature']
        print(f'Water temperature: {temp}°C')
    except:
        print('ERROR: BLE device unreachable')
        err = True

    #get power from solax cloud
    try:
        token = '<insert your API token here>'
        sn = '<insert your sn here>'
        solax_info = solax_request(token, sn)
        power = solax_info['acpower']
        print(f'AC Power: {round(power)}W')
    except:
        print('ERROR: Solax cloud unreachable')
        err = True

    #decide whether to turn the plug on or off
    try:
            if temp > 35 and power > 1950:
                turn_plug_on = True
            else:
                turn_plug_on = False
    except:
        print('ERROR: Data retrieval error')
        err = True

    #turn plug on or off
    try:
        email = '<insert your Meross email here>'
        password = '<insert your Meross password here>'
        uuid = '<insert your Meross plug uuid here>'
        turn_onoff(email, password, uuid, turn_on=turn_plug_on)

        if turn_plug_on:
            print('Plug status: ON')
        else:
            print('Plug status: OFF')
    except:
        print('ERROR: Meross device unreachable')
        err = True

    #end check
    end_tme = datetime.now()
    print(f'Check completed at {end_tme.strftime("%H:%M:%S")}\n')


    #if an error occured retry in 5 seconds
    #if not then wait the standard 60 seconds before rechecking
    if err == True:
        time.sleep(5)
    else:
        time.sleep(60)