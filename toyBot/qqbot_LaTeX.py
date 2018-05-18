# -*- coding: utf-8 -*-  
from qqbot import QQBotSlot as qqbotslot, RunBot
import urllib.request as req
import re
import random

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


def QQGroupName():
    return ['LaTeX 学习交流群','书籍分享群','SUSTech_MATLAB']

def getDictLaTeX():
    # key为回答，value为关键词
    dic = {'Happy LaTeXing!~':                                                                                       ['hello','hi','你好'],
           'TeX Live 2018下载：http://mirrors.ustc.edu.cn/CTAN/systems/texlive/Images/':                             ['下载','安装'],
           'LaTeX简历：http://www.latexstudio.net/archives/12402':                                                   ['简历'],
           'Tikz&PGF：http://www.latexstudio.net/archives/category/tex-graphics/tikz-example':                       ['tikz','pgf'],
           'lshort到这里下载：http://www.latexstudio.net/tex-documents':                                             ['lshort'],
           'sustc.edu.cn':                                                                                           ['南方科技大学'],
           '南方科技大学beamer主题模板：http://www.latexstudio.net/archives/11443':                                  ['beamer'],
           '南方科技大学毕业论文LaTeX模板：http://www.latexstudio.net/archives/8440':                                ['毕业','论文'],
           '尝试在命令行使用texdoc查看帮助文档，或者登陆网站查看宏包帮助：https://ctan.org/topic。新手请先看lshort~':['帮助'],
           'metapost, pstricks, Tikz&pgf：http://www.latexstudio.net/archives/category/tex-graphics':                ['绘图'],
           'TeX字体：http://www.latexstudio.net/archives/category/tex-resource/tex-fonts-resource':                  ['字体'],
           '学术海报：http://www.latexstudio.net/archives/category/tex-slides/latex-poster':                         ['海报'],
           'LaTeX工作室：http://www.latexstudio.net':                                                                ['网站'],
           '插图整理下载：http://www.latexstudio.net/archives/1010':                                                 ['历史','狮子'],
           'Overleaf: Real-time Collaborative Writing and Publishing Tools：https://www.overleaf.com/':              ['在线','实时','overleaf']
           }
    return dic

def getDictMATLAB():
    dic = {}
    return dic

def getDictBook():
    dic = {'忙(玩)完这阵就更新，不好意思~':['~'],
           'http://www.yooread.com/8/4548/':['左心房漩涡']}
    return dic


def OR(lst, content):
    # 内容中是否包含lst中任意字符串
    flag = False
    for v in lst:
        flag = flag or v in content
    return flag



@qqbotslot

def onQQMessage(bot, contact, member, content):  
    #if getattr(member, 'uin', None) != bot.conf.qq:
    if not bot.isMe(contact, member):
        content  = content.lower()

        # LaTeX
        if contact.name == QQGroupName()[0]:
            DicLaTeX = getDictLaTeX()
            keyLaTeX = list(DicLaTeX.keys())
            valLaTeX = list(DicLaTeX.values())
            if '李未晏' in content:
                bot.SendTo(contact, '谁？')
            for v in keyLaTeX:
                if OR(list(DicLaTeX[v]),content):
                    bot.SendTo(contact, v)
            if '文章' in content:
                bot.SendTo(contact, getNews())
            # 关键词
            if '关键词' in content:
                keywords = str(valLaTeX).replace('[','').replace(']','').replace('\'','')
                bot.SendTo(contact, str(keywords)+'\nhttps://github.com/Iydon/LaTeX-Group_Keywords')
        # Book
        if contact.name == QQGroupName()[1]:
            DicBook = getDictBook()
            keyBook = list(DicBook.keys())
            valBook = list(DicBook.values())
            for v in keyBook:
                if OR(list(DicBook[v]),content):
                    bot.SendTo(contact, v)
            if '关键词' in content:
                keywords = str(valBook).replace('[','').replace(']','').replace('\'','')
                bot.SendTo(contact, str(keywords))
        # MATLAB
        if contact.name == QQGroupName()[2]:
            DicMATLAB = getDictMATLAB()
            keyMATLAB = list(DicMATLAB.keys())
            valMATLAB = list(DicMATLAB.values())
            for v in keyMATLAB:
                if OR(list(DicBook[v]),content):
                    bot.SendTo(contact, v)
            if '关键词' in content:
                keywords = str(valBook).replace('[','').replace(']','').replace('\'','')
                bot.SendTo(contact, str(keywords))


if __name__ == '__main__':  
    RunBot()  
