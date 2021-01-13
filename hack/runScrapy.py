
import datetime
from hack.include.util import isNull
import pymongo
import schedule
import threading
import requests
from wsgiref.simple_server import make_server
import json
import math
from apscheduler.schedulers.blocking import BlockingScheduler
import time
from flask import Response, Flask, request
from flask_cors import CORS
import os
app = Flask(__name__)
myclient = pymongo.MongoClient("mongodb://192.168.142.1:27017/")
mydb = myclient["local"]
projectExam=myclient["projectExam"]
wednesdayList=['jiangxicq_sw_dl','changjianghouse_dl','nmgcq_dl','xj_cq_dl2','guizhoucq_sw_dl']
thursdayList=['jsgq_dl_new']
scrapyEvery=['anjuke_update_second3','anjuke_update_second2']
sched = BlockingScheduler()
def job(name):
    os.system("scrapy crawl "+name)

def doWeek(lis):
    for i in lis:
        threading.Thread(target=job,args=(i,)).start()
    pass

# 获取重启后的首次执行时间
def getStartTime(startTime,day=0,hours=0,minute=0,second=0):
    today = datetime.datetime.today()
    if startTime:
        return today
    interval=(second+60*(minute+60*(hours+day*24)))
    print(interval)
    space=today.timestamp() - startTime.timestamp()
    print(space)
    print(math.ceil(space/interval))
    result=interval*math.ceil(space/interval)+startTime.timestamp()
    return datetime.datetime.fromtimestamp(result)

# @sched.scheduled_job('interval',days=1,hours=12,start_date=getStartTime(datetime.datetime(2020, 10, 31, 8, 0, 0),day=1,hours=12),misfire_grace_time=3600)
# def doEvery():
#     for i in scrapyEvery[0:1]:
#         threading.Thread(target=job,args=(i,)).start()
#     pass

# @sched.scheduled_job('interval',days=1,hours=12,start_date=getStartTime(datetime.datetime(2020, 10, 30, 20, 0, 0),day=1,hours=12),misfire_grace_time=3600)
# def doEvery():
#     for i in scrapyEvery[1:]:
#         threading.Thread(target=job,args=(i,)).start()
#     pass

# @sched.scheduled_job('cron',day_of_week='0',misfire_grace_time=3600)
# def doquery():
#     os.system("cd /d E:\git\spider\community && scrapy crawl anjuke_xq")
#     time.sleep(10)
#     os.system("cd /d E:\git\spider\houseNew && scrapy crawl anjuke_kpsj")

@sched.scheduled_job('interval',days=1)
def dowangyiyun():
    print('rere')
    os.system("cd E:\git\/bigData && scrapy crawl wangyiyun")



@sched.scheduled_job('cron',day_of_week="0-4")
def dongfangcaifu():
    print('tests')
    times = ['9:00', "11:30", "13:00", '15:00']
    now = datetime.datetime.now()
    for i in range(len(times)):
        temp = times[i].split(":")
        times[i] = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=int(temp[0]),
                                     second=int(temp[1]))

    def test():
        print('test')
    for i in range(0,len(times),2):
        sched.add_job(test, 'interval', seconds=10,end_date=times[i+1],start_date=times[i])
    # os.system("cd E:\git\/bigData && scrapy crawl dongfangcaifu")

def doSched():
    sched.start()

@app.before_first_request
def before_first_request():
    # data={"cmd":"scrapy crawl wangyiyun"}
    # threading.Thread(target=cmd_job, args=(data,)).start()
    print('start')
    threading.Thread(target=doSched).start()

def cmd_job(data):
    print("start%s"%data.get("url"))
    time.sleep(60)
    if data.get("url"):
        os.chdir(data.get("url"))
    if data.get("cmd"):
        time.sleep(60)
        os.system(data.get("cmd"))


@app.route('/runcmd', methods=['POST','GET'])
def runcmd():
    if request.method == 'POST':
        data = json.loads(request.data)
    else:
        data = request.args

    threading.Thread(target=cmd_job,args=(data,)).start()

    return ""

CORS(app,resources=r"/*")
@app.route('/deleteWangyiyun', methods=['POST','GET'])
def deleteWangyiyun():
    if request.method == 'POST':
        if request.data:
            data = json.loads(request.data)
        else:
            data=request.form
    else:
        data = request.args
    comments = mydb["comments"]
    
    query = {'id':data["id"]}
    comments.delete_one(query)
    response=Response()
    response.headers={"Access-Control-Allow-Origin":"*"}
    response.data=json.dumps({'data':"success"})
    return response

CORS(app,resources=r"/*")
@app.route('/wangyiyun', methods=['POST','GET'])
def seachWangyiyun():
    if request.method == 'POST':
        if request.data:
            data = json.loads(request.data)
        else:
            data=request.form
    else:
        data = request.args
    page=data.get("page")
    if page is None:
        page={
            "pageSize":10,
            "current":1
        }
    else:
        if page.get("pageSize") is None:
            page["pageSize"]=10
        if page.get("current") is None or page.get("current")==0:
            page["current"]=1
        page["pageSize"]=int(page.get("pageSize"))
        page["current"] = int(page.get("current"))
        print(page)
    comments = mydb["comments"]
    query = {"comments.likedCount":{"$gt":2}}

    lis = comments.find(query, { "comments.$": 1,"type": 1, "name": 1, "artists": 1, "url": 1,"id":1,"_id":0}).sort(
        "comments.likedCount", -1).limit(page.get("pageSize")).skip(page.get("pageSize")*page.get("current"))
    lis = list(lis)
    #
    result={
        'data':lis,
        'total':comments.estimated_document_count()
    }
    response=Response()
    response.headers={"Access-Control-Allow-Origin":"*"}
    response.data=json.dumps(result)
    return response



CORS(app,resources=r"/*")
@app.route('/projectExam', methods=['POST','GET'])
def seachprojectExam():
    if request.method == 'POST':
        if request.data:
            data = json.loads(request.data)
        else:
            data=request.form
    else:
        data = request.args
    page=data.get("page")
    if page is None:
        page={
            "pageSize":10,
            "current":1
        }
    else:
        if page.get("pageSize") is None:
            page["pageSize"]=10
        if page.get("current") is None or page.get("current")==0:
            page["current"]=1
        page["pageSize"]=int(page.get("pageSize"))
        page["current"] = int(page.get("current"))
        print(page)
    type_=data.get("questionType","choice")
    comments = projectExam[type_]
    query = {}
    if isNull(data.get("content")) is False:
        query['content']={'$regex':".*"+data.get("content")+".*"}
    if isNull(data.get("type")) is False:
        query['type']={'$regex':".*"+data.get("type")+".*"}
    lis = comments.find(query,{"_id":0}).limit(page.get("pageSize")).skip(page.get("pageSize")*page.get("current"))
    lis = list(lis)
    #
    result = {
        'data': lis,
        'total': comments.estimated_document_count()
    }
    response=Response()
    response.headers={"Access-Control-Allow-Origin":"*"}
    response.data=json.dumps(result)
    return response
# schedule.every().wednesday.at("15:50").do(doWeek,wednesdayList)
# schedule.every().thursday.at("15:50").do(doWeek,thursdayList)
# schedule.every().day.at("20:00").do(doEvery)
# schedule.every().day.at("09:58").do(test)
if __name__ == '__main__':

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    print("start")
    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()
    # sched.start()

    # pass