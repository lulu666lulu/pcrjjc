import requests
import time
import json

apiroot = 'https://help.tencentbot.top'

def getprofile(viewer_id: int, interval: int = 1) -> dict:
    reqid = json.loads(requests.get(f'{apiroot}/enqueue?target_viewer_id={viewer_id}').content.decode('utf8'))['reqeust_id']

    if reqid is None:
        return "id err"

    while True:
        query = json.loads(requests.get(f'{apiroot}/query?request_id={reqid}').content.decode('utf8'))
        status = query['status']
        if status == 'done':
            return query['data']
        elif status == 'queue':
            time.sleep(interval)
        else: # notfound or else
            return "queue"
