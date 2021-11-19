import subprocess
import os
import signal

'''
function that scans through a list of services
and runs the relevant scripts based on the state of the dictionary.
Arguments are:
- services_list: a list of dictionaries for each service updated via RESTful API
- running_services: key/value pairs of currently running service names and their PID's

'''


def run_services (services_list: list):

    for service in services_list:

        if not service.get('pid'):
            service['pid'] = 0

        name = service['name']
        APIstatus = service['status']
        isRunning = service['pid'] != 0

        #if there's a discrepancy between the API status and what is actually running
        #then this code block will fix that.
        if APIstatus == 'on' and isRunning == False:
            print(f'starting up {name}...')
            process = subprocess.Popen(['python3', f'{name}/{name}.py'])
            service['pid'] = process.pid
        elif APIstatus == 'off' and isRunning == True:
            print(f'killing {name}...')
            os.kill(service['pid'], signal.SIGTERM)
            service['pid'] = 0

    
    return services_list


if __name__ == '__main__':
    services_example = [
        {'name': 'autocharge', 'status': 'off', 'pid': 46031},
        {'name': 'aircon', 'status': 'on', 'pid': 3789}
    ]

    print(run_services(services_example))