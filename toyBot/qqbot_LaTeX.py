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


def getKeywords():
    lst1 = ['hello','hi','你好','下载','安装','简历','tikz','lshort','南方科技大学','beamer','毕业','论文','帮助','绘图','字体']
    lst2 = ['海报','网站','历史','狮子','在线','实时','overleaf','文章']
    return lst1+lst2


@qqbotslot

def onQQMessage(bot, contact, member, content):  
    #if getattr(member, 'uin', None) != bot.conf.qq:
    if not bot.isMe(contact, member):
        content = content.lower()
        key = getKeywords()
        
        if contact.name == 'LaTeX 学习交流群':
            if '李未晏' in content:
                bot.SendTo(contact, '谁？')
            if key[0] in content or key[1] in content or key[2] in content:
                bot.SendTo(contact, 'Happy LaTeXing!~')
            if key[3] in content or key[4] in content:
                bot.SendTo(contact, 'TeX Live 2018下载：http://mirrors.ustc.edu.cn/CTAN/systems/texlive/Images/')
            if key[5] in content:
                bot.SendTo(contact, 'LaTeX简历：http://www.latexstudio.net/archives/12402')
            if key[6] in content or 'pgf' in content:
                bot.SendTo(contact, 'Tikz&PGF：http://www.latexstudio.net/archives/category/tex-graphics/tikz-example')
            if key[7] in content:
                bot.SendTo(contact, 'lshort到这里下载：http://www.latexstudio.net/tex-documents')
            if key[8] in content:
                bot.SendTo(contact, 'sustc.edu.cn')
            if key[9] in content:
                bot.SendTo(contact, '南方科技大学beamer主题模板：http://www.latexstudio.net/archives/11443')
            if key[10] in content or key[11] in content:
                bot.SendTo(contact, '南方科技大学毕业论文LaTeX模板：http://www.latexstudio.net/archives/8440')
            if key[12] in content:
                bot.SendTo(contact, '尝试在命令行使用texdoc查看帮助文档，或者登陆网站查看宏包帮助：https://ctan.org/topic。新手请先看lshort~')
            if key[13] in content:
                bot.SendTo(contact, 'metapost, pstricks, Tikz&pgf：http://www.latexstudio.net/archives/category/tex-graphics')
            if key[14] in content:
                bot.SendTo(contact, 'TeX字体：http://www.latexstudio.net/archives/category/tex-resource/tex-fonts-resource')
            if key[15] in content:
                bot.SendTo(contact, '学术海报：http://www.latexstudio.net/archives/category/tex-slides/latex-poster')
            if key[16] in content:
                bot.SendTo(contact, 'LaTeX工作室：http://www.latexstudio.net')
            if key[17] in content or key[18] in content:
                bot.SendTo(contact, '插图整理下载：http://www.latexstudio.net/archives/1010')
            if key[19] in content or key[20] in content or key[21] in content:
                bot.SendTo(contact, 'Overleaf: Real-time Collaborative Writing and Publishing Tools：https://www.overleaf.com/')
            if key[22] in content:
                bot.SendTo(contact, getNews())
            # 关键词
            if '关键词' in content:
                keywords  = ''
                for k in sorted(key):
                    keywords += str(k)+', '

                bot.SendTo(contact, keywords[:-2]+'\nhttps://github.com/Iydon/LaTeX-Group_Keywords')

if __name__ == '__main__':  
    RunBot()  
