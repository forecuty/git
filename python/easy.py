#!/usr/bin/env python3
#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.request import Request
from urllib.parse import quote
import re
import os
import time


#*************爬取章节URL**************
def getChapterUrl(homeUrl, chapterUrl, headers):

    req = Request(homeUrl, headers = headers)
    html = urlopen(req).read()

    soup = BeautifulSoup(html, "lxml")
    tempChapterUrl = soup.find_all("a", href = re.compile("http:\/\/comic3+[\S]*\.htm"))
    pattern=re.compile("http:\/\/comic3+[\S]*\.htm")         #获得正则表达式pattern对象
    for t in tempChapterUrl:
        chapterUrl.append(t['href'])                #find_all返回的是bs对象，它将href变成了一个数据成员，可以直接调用

    return
#***************************************

#*************获取章节页码数，章节名称**************
def getNothing(pageUrl, pages, names, manga, headers):

    req = Request(pageUrl, headers =headers)
    html = urlopen(req).read().decode('gbk')
    soup = BeautifulSoup(html, "lxml")
    tText = soup.get_text()                                 #get_text方法返回str，然后用正则表达式匹配
    patternPage = re.compile("共[0-9]+")
    t1 = patternPage.findall(tText)                      #匹配后的页码数字符串
    for x in t1[:-1]:                   #一页只保存一个
        pages.append(x[1:])             #去掉前面的中文,获得页码数
    patternName = re.compile("\/[0-9]+\/[0-9]+\/[0-9]+\/" + manga + '_' +"[\\u4e00-\\u9fa5]+[0-9]+[\\u4e00-\\u9fa5]?") #拼接字符串时，先转义\
    t2 = patternName.findall(tText)
    for x in t2[:-1]:         
        names.append(x)                 #获得漫画当前话名称

    print("获得章节页码数，章节名称")

    return

#***************************************
#**************爬取JPG******************

def getJpg(pageUrl, pages, jpgs, headers):

    n = 0
   # for pageUrl in chapterUrl:
    #print("now getting chapter", n + 1)
    for i in range(int(pages[n])):
        tUrl = pageUrl[:-5] + str(i+1) + ".htm"        #当前页的URL
        req = Request(tUrl, headers =headers)
        #html = urlopen(tUrl)
        html = urlopen(req).read().decode('gbk')
        soup = BeautifulSoup(html, "lxml")
        tText = soup.get_text() 
        patternJpg = re.compile("\/00[0-9]+[\S]*\.jpg")
        t = patternJpg.findall(tText)                   #只保留一个（一页html里有两个）
        for x in t[:-1]:
            jpgs.append(x)                 #获得漫画图片JPG名称
     #   n += 1
        time.sleep(1)
    print("获得JPG名称")

    return
#************拼接真·URL****************
def getMangaUrl(relUrl, names, jpgs, mangaHead, headers):

    for name in names:
        word = quote(name)              #中文转码
        tempUrl = mangaHead + word
        for jpg in jpgs:                     #页码
            relUrl.append(tempUrl + jpg)   #不同页码的URL
    print("获得真·URL")

    return
#***************************************

#*****************下载图片**************
def downloadManga(relUrl, names, jpgs):

    name = names[0]
    name = name[-4:]
    print("Now downloading:", name)
    if os.path.isdir(name) == False:         #没有同名文件夹
        os.mkdir(name)
    n = 0
    for url in relUrl:
        jpg = jpgs[n]
        path = name + "/" + jpg[:5] + jpg[-4:]
        if os.path.exists(path) == False:     #没有同名图片
            urlretrieve(url, path)
            print(jpgs[n]," is alerady downloaded")
        n += 1
    print(name,"was downloaded\nPrepare to download next chapter")
    return
#*******************************

#**************test*************

def main():
    #chapterUrl = ["http://comic.kukudm.com/comiclist/2246/53762/1.htm","http://comic.kukudm.com/comiclist/2246/53763/1.htm"]
    manga = "关于我转生后成为史莱姆的那件事"
    #headers = {'User-Agent':'Mozilla/5.0(Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}#浏览器头
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}  
    homeUrl = "http://comic.kukudm.com/comiclist/2246/index.htm"#史莱姆主页
    mangaHead = "http://n.1whour.com/newkuku"     #漫画网站的头

    chapterUrl = []
    pages= []
    names = []
    jpgs = []
    relUrl = []
    print("我不是一只坏的史莱姆哟")
    getChapterUrl(homeUrl, chapterUrl, headers)
    print("获得所有章节URL")
    for pageUrl in chapterUrl[4:6]:
        getNothing(pageUrl, pages, names, manga, headers)
        getJpg(pageUrl, pages, jpgs, headers)
        getMangaUrl(relUrl, names, jpgs, mangaHead, headers)
        downloadManga(relUrl, names, jpgs)
        
        relUrl.clear()          #清除列表以便下次继续增加
        pages.clear()
        names.clear()
        jpgs.clear()




if __name__ == "__main__":
    main();
 


