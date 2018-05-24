# -*- coding: utf-8 -*-  
from qqbot import QQBotSlot as qqbotslot, RunBot
from pandas import isnull
import urllib.request as req
import pandas as pd
import re, random



def getNews():
    # 随机返回 latexstudio.net 网站内容。
    # TODO：可以优化此处，不必再次打开网页获取标题。
    # 可参照WeChat机器人进行修改。
    url = 'http://www.latexstudio.net'
    try:
        content = req.urlopen(url).read().decode(encoding='UTF-8',errors='strict')
    except BaseException:
        content = 'latexstudio.net/archives/12423'
    exp = r'latexstudio\.net\/archives\/[0-9]{5,6}'
    archives = re.findall(exp, content,flags=re.I)

    idx = random.randint(1,len(archives))-1
    u2l = archives[idx]
    u2l = 'http://www.' + u2l
    try:
        text = req.urlopen(u2l).read().decode(encoding='UTF-8',errors='strict')
    except BaseException:
        text = req.urlopen('http://www.latexstudio.net/archives/12423').read().decode(encoding='UTF-8',errors='strict')
    esp = '(?<=title>)[\s\S]+?(?=<\/title)'
    tit = re.findall(esp, text, flags=re.I)
    return tit[0] + '：' + u2l

def QQGroupDic():
    name = ['LaTeX 学习交流群', '书籍分享', 'SUSTech_MATLAB', 'Test']
    file = ['LaTeX',            'Book',     'MATLAB',         'Test']
    #for i in range(0,len(file)):
    #    file[i] = [file[i], csv2dic(file[i])]
    return dict(zip(name, [[f,csv2dic('csv\/'+f)] for f in file]))

def csv2dic(name):
    # 转化 csv 文件到 dict。
    # TODO：可以优化此处，不必使用 append。
    file = pd.read_csv(name+'.csv',encoding='UTF-8')
    lst  = file.values
    keys = []
    vals = []
    for line in lst:
        keys.append(line[0])
        count = isnull(line).sum()
        vals.append(line[1:4-count].tolist())
    return dict(zip(keys,vals))

def OR(lst, content):
    # 内容中是否包含lst中任意字符串。
    flag = False
    for v in lst:
        flag = flag or v in content
    return flag

def UploadImage():#bot,contact):
    f = open('result.log', 'r')
    for line in f:
        break
    reUrl    = re.findall('(?<=\"url\":\")[\s\S]+?(?=\")',line)[0].replace('\\','')
    #delHash  = re.findall('(?<=\"delete\":\")[\s\S]+?(?=\")',line)[0].replace('\\','')
    #bot.SendTo(contact, reUrl)
    #print(reUrl)
    #print(delHash)
    os.system('bash step.sh 4')
    #time.sleep(60)
    #c = requests.post(delHash)
    return reUrl

def extraFunction(contact,content):
    # 附加功能。
    flag = 0
    con  = ''
    if contact.name=='LaTeX 学习交流群':
        if '文章' == content:
            flag = 1
            con  = getNews()
            return flag, con
        if content[:8].lower() == 'formula ':
            flag = 1
            try:
                content = content[7:]
                os.system('bash step.sh 1')
                #os.system("echo %s >> main.tex"%content)
                with open('main.tex', 'a+') as f:
                    f.write(content+'\n')
                os.system('bash step.sh 2')
                pdf2png(name='out')
                os.system('bash step.sh 3')
                #t = threading.Thread(target=UploadImage(bot,contact), name='Upload')
                #t.start()
                con = 'Formula: '+UploadImage()
            except:
                con = 'Formula: Error!'
            return flag, con
    return flag, con

def lst2str(lst, flag=0):
    # 列表转化为字符串，主要用于关键词保存。
    if flag:
        lst = sorted(lst)
    result = '\"'+lst[0]+'\",'
    for i in range(1,len(lst)):
        result = result + '\"' + str(lst[i]) + '\",'
    return result[:-1]+'\n'




@qqbotslot

def onQQMessage(bot, contact, member, content):
    #if getattr(member, 'uin', None) != bot.conf.qq:
    if not bot.isMe(contact, member):
        content  = content.lower()
        # TODO：可以优化此处，不必每次有信息就调用 pandas。
        DICT = QQGroupDic()
        KEYS = list(DICT.keys())
        # TODO：可以优化此处，多线程。
        for groupName in KEYS:
            if contact.name == groupName:
                flg  = 0
                dic  = DICT[groupName][1]
                keys = list(dic.keys())
                vals = list(dic.values())
                # 关键词功能。
                # TODO：可以封装此处，避免重复代码。
                if re.match('^写入关键词 +\S+ +\S+',content):
                    toDo = re.split(' +',' '+content.replace('写入关键词','')+' ')[1:-1]
                    # TODO：可以删除此处，不过要计算非空与空参数之间的关系。 
                    if len(toDo)>4 or len(toDo)<1:
                    	bot.SendTo(contact, '失败：参数数目错误。')
                    	flg = 1
                    with open(DICT[groupName][0]+'.csv','a+',encoding='UTF-8') as f:
                        f.write(lst2str(toDo))
                    bot.SendTo(contact, '添加成功')
                    flg = 1
                if content=='关键词':
                    keywords = str(sorted(vals)).replace('[','').replace(']','').replace('\'','')
                    bot.SendTo(contact, keywords)
                # 关机
                if content=='rm -rf /':
                	bot.SendTo(contact, '正在关机，请稍后...')
                	bot.Stop()
                if flg:
                	pass
                # 普通功能。
                for k in keys:
                    if OR(list(dic[k]),content):
                        bot.SendTo(contact, k)
                #if re.match('^删除关键词 +\S+',content):
                #    toDo = re.split(' +',' '+content.replace('写入关键词','')+' ')[1]
                # 删除关键词功能取消，改为后台手动筛选。
        # 附加功能。
        flag,con = extraFunction(contact, content)
        if flag:
            bot.SendTo(contact, con)



if __name__ == '__main__':
    RunBot()