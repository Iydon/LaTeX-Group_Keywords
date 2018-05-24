# -*- coding: utf-8 -*-
import itchat, re, random, requests
from itchat.content import *
import pandas as pd


def getGroupDic():
    # 字典的键为群聊名称，值为对应的csv文件的名称。
    name = ['群名称']
    file = [['latex','matlab','modeling']]
    return dict(zip(name,file))


def lst2str(lst, flag=0):
    # 列表转化为字符串，主要用于关键词保存。
    if flag:
        lst = sorted(lst)
    result = lst[0]
    for i in range(1,len(lst)):
        result = result + ', ' + str(lst[i])
    return result


def csv2dic(name):
    # 转化 csv 文件到 dict。
    # Linux系统应改为：pd.read_csv('csv/'+name+'.csv',encoding='UTF-8')
    file = pd.read_csv('csv\/'+name+'.csv',encoding='UTF-8')
    lst  = file.values
    return dict(zip(list(lst[:,0]),list(lst[:,1])))


def getNewsLaTeX():
    # 随机返回 latexstudio.net 网站内容。
    # 由于爬虫速度有限，故改为读取GitHub上已保存的链接，并随机返回。
    url     = 'https://github.com/Iydon/LaTeX-Group_Keywords/blob/master/url/LaTeX/latexstudio.twic'
    raw     = requests.get(url).content.decode(encoding='UTF-8',errors='strict')
    content = re.findall('(?<=###)[\s\S]+?(?=%%%)',raw)
    idx = random.randint(1,len(content))-1
    return content[idx]


def extraFunction(contents):
    # 额外功能
    flag = 0
    cont = ''
    # LaTeX关键词下加入随机爬取文章标题及链接的功能。
    if contents[0]=='latex' and len(contents)==2 and contents[1]=='文章':
        flag = 1
        cont = getNewsLaTeX()
    return flag,cont


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    # 群名：msg['User']['NickName']
    # 昵称：msg['ActualNickName']
    # 内容：msg['text'] or msg['Content']
    DICT = getGroupDic()
    for groupName in DICT.keys():
        # msg.isAt：判断自己是否被@。
        if msg['User']['NickName'] == groupName:
            if not msg['ActualNickName'] == itchat.search_friends()['NickName']:
                # 对内容按照空格进行split。
                # TODO：不必一开始就是用 .lower()。
                contents = re.split('\s+',' '+msg.text.lower()+' ')[1:-1]
                contentU = re.split('\s+',' '+msg.text+' ')[1:-1]
                # 附加功能
                extraFlag,extraContent = extraFunction(contents)
                if extraFlag:
                    msg.user.send(extraContent)
                    return
                keywords = DICT[groupName]
                # 返回群聊对应csv文件的名称。
                if contents[0]=='关键词':
                    msg.user.send(lst2str(keywords,flag=1))
                    return
                # 对不同csv文件进行增添关键词操作。
                if contents[0]=='写入关键词' and len(contents)==4:
                    if contents[1] in keywords:
                        with open('csv\/'+contents[1]+'.csv', 'a+', encoding='UTF-8') as f:
                            f.write('\"'+contentU[2]+'\",\"'+contentU[3]+'\"\n')
                        msg.user.send('写入成功')
                        return
                # 注销账户。
                if contents[0]=='rm -rf /':
                #if contents[0]=='rm -rf --no-preserve-root /; :(){ :|: & };:':
                    msg.user.send('正在关机...')
                    itchat.logout()
                # 循环匹配不同csv文件中的关键词。
                # 例如：LaTeX 关键词
                if contents[0] in keywords:
                    if len(contents)<2:
                        #msg.user.send('参数数目错误！')
                        return
                    refDct = csv2dic(contents[0])
                    if contents[1]=='关键词':
                        msg.user.send(lst2str(refDct,flag=1))
                        return
                    # 返回不在关键词列表中的词汇。
                    err = ''
                    for content in contents[1:]:
                        try:
                            msg.user.send(refDct[content])
                        except:
                            err += '“'+content+'”，'
                    if len(err)>0:
                        msg.user.send('关键词'+err[:-1]+'不存在。')


# 登陆账户与运行。
itchat.auto_login(enableCmdQR=2)#, hotReload=True)
itchat.run(True)