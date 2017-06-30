import requests
import time
import json
import os
f=open('config.json',encoding='utf-8')
config=json.load(f)
list=[]
for x in config:
    if x.get('tags')==None:
        content1=x.get('subs')
        for y in content1:
            if y.get('tags')==None:
                content3=y.get('secsub')
                for z in content3:
                    zz=z.get('tags')
                    for zzz in zz:
                        ct1=zzz.get('keywords')
                        for key1 in ct1:
                            list.append(key1)

            else:
                content4=y.get('tags')
                for a in content4:
                    ct2=a.get('keywords')
                    for key2 in ct2:
                        list.append(key2)
    else:
        content2=x.get('tags')
        for a in content2:
            ct3=a['keywords']
            for b in ct3:
                key3=b
                list.append(key3)


def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print(path + ' 创建成功')
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False



def get_list(company,keyword,begin_time,final_time):
    mkdir('get_file/'+company)
    path=os.getcwd()+'/'+'get_file'+'/'+company

    url = 'http://www.cninfo.com.cn/cninfo-new/fulltextSearch/full?searchkey=' + company+keyword + \
          '&isfulltext=false&sortType=desc&pageNum=1'
    r = requests.get(url)
    ans = r.json()['announcements']
    for an in ans:
        # 格式化标题
        an['announcementTitle']=an['announcementTitle'].replace('<em>', '').replace('</em>', '')

        # 时间比较
        my_time = str(an['announcementTime'])[:-3]
        # print(my_time)
        # timeArray1 = time.strptime(my_time, "%Y-%m-%d")
        # timeStamp = int(time.mktime(timeArray1))
        timeArray2 = time.strptime(begin_time, "%Y-%m-%d")
        b_time = str(time.mktime(timeArray2))
        timeArray3 = time.strptime(final_time, "%Y-%m-%d")
        f_time = str(time.mktime(timeArray3))

        if my_time > b_time and my_time < f_time :
            print(an['announcementTitle']+'OK~~~')


            down_url='http://www.cninfo.com.cn/'+an['adjunctUrl']
            rr=requests.get(down_url)
            with open(path+'/'+an['announcementTitle']+'.pdf','wb') as f:
                f.write(rr.content)

        else:
            print(an['announcementTitle']+'不合条件!!!')


for x in list:
    # print(x[0])
    get_list('五洋科技',x[0],'2016-01-01','2017-05-30')