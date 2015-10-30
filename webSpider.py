import urllib.request
import re
import os
##简书爬虫
class Spider:
    def __init__(self):
        self.__page=''
        self.__urlList=[]
        self.__url=''
        self.__storagePath='F:\spiderStorage'
        self.__articlePath='F:\spiderStorage\Articles'
        self.__picturePath='F:\spiderStorage\Pictures'
    def setURl(self,url):
        self.__url=url
    def openUrl(self,url):
        response=urllib.request.urlopen(url)
        self.__page=response.read()
    def getPage(self):
        return self.__page
    def geturlList(self,string):
        urllist=[]
        pattern=re.compile(b'<h4 class="title"><a target="_blank" href="/(\w/\w+)">')
        urls=re.findall(pattern,string)
        for url in urls:
            temp=url.decode('utf-8')
            urllist.append(self.__page+'/'+temp)
        self.__urlList=urllist
        print(self.__urlList[0])
    def getContent(self,page):
        titlePattern=re.compile(b'class="title">(\w+)<')
        authorPattern=re.compile(b'"author-name blue-link".*?<span>(\w+)</span>')
        contentPattern=re.compile(b'<p>(\w+)</p>')
        picturePattern=re.compile(b'<img src="(.*?)"')
        imageChaptionPattern=re.compile(b'<div class="image-caption">(\w+)</div>')
        title=re.findall(titlePattern,page)
        f=open(self.__articlePath+'\\'+title.decode('utf-8')+'.md','wb')
        author=re.findall(authorPattern,page)
        contents=re.findall(contentPattern,page)
        pictures=re.findall(picturePattern,page)
        imageChaptions=re.findall(imageChaptionPattern,page)
        f.write('##'+title.decode('utf-8')+'\n###'+author.decode('utf-8')+'\n')
        for item in contents:
            f.write(item.decode('utf-8')+'\n')
        for pic,chap in pictures,imageChaptions:
            f.write(self.getImage(pic.decode('utf-8'),chap.decode('utf-8')))
            f.close()
        self.saveImage(pictures,author)
    def getImage(self,picture,imageChaption):
        return '!['+imageChaption+']('+picture+')'

    def saveImage(self,pictures,author):
        i=1
        for item in pictures:
            temp=item.decode('utf-8')
            pic=urllib.request.urlopen(temp)
            f=open(self.__picturePath+'\\'+author+i+'.jpg','wb')
            f.write(pic.read())
            f.close()
            i=i+1
    def start(self,url):
        os.mkdir(self.__storagePath)
        os.mkdir(self.__articlePath)
        os.mkdir(self.__picturePath)
        self.setURl(url)
        self.openUrl(self.__url)
        self.geturlList(self.getPage())
        for item in self.__urlList:
            response=urllib.request.urlopen(item)
            page=response.read()
            self.getContent(page)
