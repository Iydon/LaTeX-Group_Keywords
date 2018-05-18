# -*- coding: utf-8 -*-  
from qqbot import QQBotSlot as qqbotslot, RunBot
from pandas import isnull
import urllib.request as req
import pandas as pd
import re, random



def getNews():
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
    return {'LaTeX 学习交流群':['LaTeX',csv2dic('LaTeX')],
            '书籍分享':['Book',csv2dic('Book')],
            'SUSTech_MATLAB':['MATLAB',csv2dic('MATLAB')],
            'Test':['LaTeX',csv2dic('LaTeX')]}

def csv2dic(name):
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
    # 内容中是否包含lst中任意字符串
    flag = False
    for v in lst:
        flag = flag or v in content
    return flag

def extraFunction(contact,content):
    flag = 0
    con  = ''
    if contact.name=='Test':#'LaTeX 学习交流群':
        if '文章' in content:
            flag = 1
            con  = getNews()
    return flag, con

def lst2str(lst):
    result = '\"'+lst[0]+'\",'
    for i in range(1,len(lst)):
        result = result + '\"' + str(lst[i]) + '\",'
    return result[:-1]+'\n'




@qqbotslot

def onQQMessage(bot, contact, member, content):
    #if getattr(member, 'uin', None) != bot.conf.qq:
    if not bot.isMe(contact, member):
        content  = content.lower()
        DICT = QQGroupDic()
        KEYS = list(DICT.keys())
        for groupName in KEYS:
            if contact.name == groupName:
                dic  = DICT[groupName][1]
                keys = list(dic.keys())
                vals = list(dic.values())
                for k in keys:
                    if OR(list(dic[k]),content):
                        bot.SendTo(contact, k)
                # 加入pass，改变顺序
                if re.match('^写入关键词 +\S+ +\S+',content):
                    toDo = re.split(' +',' '+content.replace('写入关键词','')+' ')[1:-1]
                    with open(DICT[groupName][0]+'.csv','a+',encoding='UTF-8') as f:
                        f.write(lst2str(toDo))
                    bot.SendTo(contact, '添加成功')
                if re.match('^删除关键词 +\S+',content):
                    toDo = re.split(' +',' '+content.replace('写入关键词','')+' ')[1]
                if content=='关键词':
                    keywords = str(vals).replace('[','').replace(']','').replace('\'','')
                    bot.SendTo(contact, keywords)
        flag,con = extraFunction(contact, content)
        if flag:
            bot.SendTo(contact, con)


if __name__ == '__main__':
    #DICT = QQGroupDic()
    #KEYS = list(DICT.keys())
    RunBot()