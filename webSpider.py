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
        self.__page=response.read().decode('utf-8')
    def getPage(self):
        return self.__page
    def geturlList(self,string):
        urllist=[]
        pattern=re.compile('<h4 class="title"><a target="_blank" href="/(\w/\w+)">')
        urls=re.findall(pattern,string)
        for url in urls:
            urllist.append(self.__url+'/'+url)
        self.__urlList=urllist
    def getContent(self,page):
        ##print(page)
        titlePattern=re.compile('<h1 class="title">(.*)</h1>')
        authorPattern=re.compile('<a class="author-name blue-link".*?>\s*<span>(.*)</span>\s*</a>')
        contentPattern=re.compile('<p>(.*)</p>')
        picturePattern=re.compile('<img.*?src="(.*?)"')
        imageChaptionPattern=re.compile('<div class="image-caption">(\w+)</div>')
        title=re.search(titlePattern,page)
        title=re.sub('\s+','',title.groups()[0])
        ##print(title)
        f=open(self.__articlePath+'\\'+title+'.md','w',encoding='utf-8')
        author=re.search(authorPattern,page)
        contents=re.findall(contentPattern,page)
        pictures=re.findall(picturePattern,page)
        ##print(author.groups()[0])
        f.write('##'+title+'\n###'+author.groups()[0]+'\n')
        for item in contents:
            item=item.replace('<p>','  ').replace('</p>','\n\n').replace('<br>','\n\n')
            item=re.sub('<[ /]?b>','**',item)
            ##print(item)
            f.write(item)
        for i in range(0,len(pictures)):
            f.write(self.getImage(pictures[i])+'\n\n')
        f.close()
        self.saveImage(pictures,author.groups()[0])
    def getImage(self,picture):
        return '![picture]('+picture+')'
    def saveImage(self,pictures,author):
        i=1
        for item in pictures:
            pic=urllib.request.urlopen(item)
            f=open(self.__picturePath+'\\'+author+str(i)+'.jpg','wb')
            f.write(pic.read())
            f.close()
            i=i+1
    def start(self,url):
        if not os.path.exists(self.__storagePath):
            os.mkdir(self.__storagePath)
            os.mkdir(self.__articlePath)
            os.mkdir(self.__picturePath)
        self.setURl(url)
        self.openUrl(self.__url)
        self.geturlList(self.getPage())
        for item in self.__urlList:
            response=urllib.request.urlopen(item)
            page=response.read().decode('utf-8')
            self.getContent(page)
            ##print(page)
