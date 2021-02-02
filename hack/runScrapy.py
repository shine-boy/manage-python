# coding=utf-8
import datetime
from hack.util import isNull
import pymongo
import threading
from wsgiref.simple_server import make_server
import json
import math
from hack.include import Stock,Page
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import time
from flask import Response, Flask, request
from flask_cors import CORS
import os
import hack.include.rili as rili
app = Flask(__name__)
myclient = pymongo.MongoClient("mongodb://192.168.142.1:27017/")
mydb = myclient["local"]
projectExam=myclient["projectExam"]
wednesdayList=['jiangxicq_sw_dl','changjianghouse_dl','nmgcq_dl','xj_cq_dl2','guizhoucq_sw_dl']
thursdayList=['jsgq_dl_new']
scrapyEvery=['anjuke_update_second3','anjuke_update_second2']
sched = BackgroundScheduler()

def job(name):
    os.system("scrapy crawl "+name)

def doWeek(lis):
    for i in lis:
        threading.Thread(target=job,args=(i,)).start()
    pass

# 获取重启后的首次执行时间
def getStartTime(startTime,day=0,hours=0,minute=0,second=0):
    today = datetime.datetime.today()
    if startTime > today:
        return startTime
    interval=(second+60*(minute+60*(hours+day*24)))
    if interval==0:
        interval=1
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

@sched.scheduled_job('interval',days=1,misfire_grace_time=3600,start_date=getStartTime(datetime.datetime(2021, 2, 2, 18, 0, 0),day=1))
def dowangyiyun():
    print('rere')
    # os.system("cd E:\git\/bigData && scrapy crawl wangyiyun")
    os.system("scrapy crawl wangyiyun")


def dongfangcaifu():
    print('tests')

    if not rili.isStockDeal():
        return
    stock = Stock()
    times = ['9:30', "11:31", "13:00", '15:01']
    now = datetime.datetime.now()
    for i in range(len(times)):
        temp = times[i].split(":")

        times[i] = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=int(temp[0]),
                                     minute=int(temp[1]))

    def test():
        print('time')
        # os.system("scrapy crawl dongfangcaifu")
        ti=time.time()
        stock.do(stock.insert_mongo)
        stock.waiter()
        print(time.time()-ti)
    for i in range(0, len(times), 2):
        if times[i+1] < now:
            continue
        if times[i] < now:
            times[i] = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=now.hour,
                                         minute=now.minute+1)
        sched.add_job(test, 'interval', minutes=2, end_date=times[i + 1], start_date=times[i],max_instances=10,misfire_grace_time=3600)
    # os.system("cd E:\git\/bigData && scrapy crawl dongfangcaifu")

@sched.scheduled_job('cron',day_of_week="0-4",misfire_grace_time=3600)
def do_dongfangcaifu():
    dongfangcaifu()



def doSched():
    print('start')
    # threading.Thread(target=dowangyiyun).start()
    threading.Thread(target=dongfangcaifu).start()
    sched.start()


@app.before_first_request
def before_first_request():
    pass
    # data={"cmd":"scrapy crawl wangyiyun"}
    # threading.Thread(target=cmd_job, args=(data,)).start()
    # print('start')
    # threading.Thread(target=doSched).start()


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

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

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
    page=Page(data.get("page")).page

    comments = mydb["comments"]
    query = {"comments.likedCount":{"$gt":2}}
    sort=[]
    sortType = data.get("sort")
    if sortType is None:
        sort=[("comments.likedCount", -1)]
    else:
        sort=[(sortType,-1)]
    lis = comments.find(query, { "_id":0}).sort(sort).limit(page.get("pageSize")).skip(page.get("pageSize")*(page.get("current")-1))
    lis = list(lis)
    #
    result={
        'data':lis,
        'total':comments.estimated_document_count()
    }
    print(len(lis))
    response=Response()
    response.headers={"Access-Control-Allow-Origin":"*"}
    response.data=json.dumps(result,cls=DateEncoder)
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
    page=Page(data.get("page")).page
    type_=data.get("questionType","choice")
    comments = projectExam[type_]
    query = {}
    if isNull(data.get("content")) is False:
        query['content']={'$regex':".*"+data.get("content")+".*"}
    if isNull(data.get("type")) is False:
        query['type']={'$regex':".*"+data.get("type")+".*"}
    print(page)
    lis = comments.find(query,{"_id":0}).limit(page.get("pageSize")).skip(page.get("pageSize")*(page.get("current")-1))
    lis = list(lis)
    #
    # print(comments.count_documents(filter=query))
    result = {
        'data': lis,
        'total': comments.count_documents(filter=query)
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
    threading.Thread(target=doSched).start()
    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()


    # pass