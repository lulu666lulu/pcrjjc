import aiohttp
import asyncio

import time
import json

apiroot = 'https://help.tencentbot.top'

check_time_dict={}

async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()
            return json.loads(content)

def isInPeriod(viewer_id: int) -> bool:
    value = check_time_dict[viewer_id] # exist by Branch statements in "getprofile"
    period = value.split()[1]

    if float(period)>time.time():
        return True
    return False

async def getprofile(viewer_id: int, interval: int = 1, full: bool = False) -> dict:
    reqid:int
    if not viewer_id in check_time_dict or not isInPeriod(viewer_id):
        response=await get(f'{apiroot}/enqueue?full={full}&target_viewer_id={viewer_id}')
        reqid = response['reqeust_id']

        if reqid is None:
            return "id err"
        check_time_dict[viewer_id] = f"{reqid} {time.time()+180}" #秒的格式 # id 过期时间
    reqid = check_time_dict[viewer_id].split()[0]
    while True:
        query= await get(f'{apiroot}/query?request_id={reqid}')
        status = query['status']
        if status == 'done':
            del check_time_dict[viewer_id]
            return query['data']
        elif status == 'queue':
            time.sleep(interval)
        else: # notfound or else
            return "queue"
'''
def queryarena(defs: list, page: int) -> dict:
    return json.loads(requests.get(f'{apiroot}/arena?def={",".join([str(x) for x in defs])}&page={page}').content.decode('utf8'))

print(queryarena([101001,102601,107601,102101,100701], 0))#page must under 9'''
