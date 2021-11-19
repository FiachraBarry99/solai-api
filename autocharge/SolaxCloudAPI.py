import requests
import json

def solax_request(tokenID: str, sn: str):
    
    info = requests.get(f'https://www.solaxcloud.com:9443/proxy/api/getRealtimeInfo.do?tokenId={tokenID}&sn={sn}')
    data = json.loads(info.text)
    if data['success'] == True:
        return data['result']
    else:
        raise RuntimeError('ERROR: Solax Cloud unreachable')

if __name__ == '__main__':
    token = '<token>'
    sn = '<serial number>'
    print(solax_request(token, sn))