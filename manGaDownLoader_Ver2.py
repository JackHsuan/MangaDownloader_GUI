#!/usr/bin/env python
# coding: utf-8

# In[1]:


# from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QPushButton,QLineEdit,QMessageBox, QScrollArea, QVBoxLayout,QRadioButton,QListWidget,QListWidgetItem ,QHBoxLayout, QFormLayout, QGroupBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import requests
# import time
# import pandas as pd
# import datetime
from bs4 import BeautifulSoup
# from openpyxl import load_workbook
import os
import re
import urllib
import threading
from functools import partial
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


# In[5]:


#myLabel 製作Qlabel可以被點集發送訊號
class myLabel(QLabel):
    clicked = pyqtSignal()
    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit()

class App(QWidget):
    
    def __init__(self):
        super().__init__()
        self.title = 'MangaDownloader'
        self.left = 10
        self.top = 10
        self.width = 600
        self.height = 800

        self.my_list = QListWidget()
        self.whole_layout = QVBoxLayout()
        self.mangaInfo = QVBoxLayout()
        self.manga_layout = QHBoxLayout()
        self.bt_layout = QHBoxLayout()
        self.setLayout(self.whole_layout)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.count = 1
        self.pageSize = 10
        
        #取得漫畫資訊
        data_dict = self.Manga_info(self.count,self.pageSize)
        
#         #取得漫畫集數
#         chapter = self.Manga_chapterList(data_dict['UpdateComicItems'][0]['UrlKey'])
        
        formLayout = QFormLayout()
        self.groupBox = QGroupBox()
        
        for manga in data_dict['UpdateComicItems']:
        # Create widget 製作漫畫圖框
            label = myLabel()
            pixmap = QPixmap(str('./photo/%s.jpg'%str(manga['ID'])))
            label.setFixedSize(200,300)
            label.setPixmap(pixmap)
            label.clicked.connect(partial(self.myLabel_clicked,manga))
            # Create widget 製作漫畫名稱框
            textbox = QLabel(manga['Title'])
            formLayout.addRow(textbox, label)
        self.groupBox.setLayout(formLayout)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.groupBox)
        self.scroll.setWidgetResizable(True)
        
        self.manga_layout.addWidget(self.scroll)

#         self.mangaInfo.addWidget(self.label)
#         self.mangaInfo.addWidget(self.textbox)
#         self.my_widget_1 = QWidget()
#         self.my_widget_1.setLayout(self.mangaInfo)
        
        #將漫畫資訊 漫畫有幾集 傳入create_chapter_list 添加至layout內
#         self.create_chapter_list(data_dict,chapter)
        
        self.my_widget = QWidget()
        self.my_widget.setLayout(self.manga_layout)
        
        self.whole_layout.addWidget(self.my_widget)

        self.create_pre_nex_bt()
        self.resize(800, 600)
        
        self.show()
    
    def create_pre_nex_bt(self):
        try:
            self.my_widget_2.close()
        except:
            pass
        self.page_text = QLabel(str(self.count))
        self.page_text.setParent(self)
        self.page_text.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

        self.prev_button = QPushButton('<')
        self.prev_button.setParent(self)
        self.next_button = QPushButton('>')
        self.next_button.setParent(self)
        self.prev_button.clicked.connect(self.preb_button_click)
        self.next_button.clicked.connect(self.next_button_click)
        self.bt_layout.addWidget(self.prev_button)
        self.bt_layout.addWidget(self.page_text)
        self.bt_layout.addWidget(self.next_button)
        self.my_widget_2 = QWidget()
        self.my_widget_2.setLayout(self.bt_layout)
        self.whole_layout.addWidget(self.my_widget_2)
    
    def create_chapter_list(self,data_dict,chapter):
        try:
            self.my_list.close()
        except:
            pass
        self.my_list = QListWidget()
        self.my_list.setParent(self)
#         self.my_list.move(300,100)
        for i,key in zip(range(len(chapter)),chapter):
            download_dict = {"manga_src":chapter[key][0],
                             "manga_name":data_dict['Title'],
                             "manga_pic":data_dict['ShowPicUrlB'],
                             "manga_chap":key}
            #新建个Item
            item = QListWidgetItem()
            #将item添加到list
            self.my_list.addItem(item)
            
            button = QPushButton(key)
#             button.setFixedSize(50,100)
            button.clicked.connect(partial(self.onClicked,download_dict))
            self.my_list.setItemWidget(item,button)
#         self.my_list.setFixedSize(200,100)
        self.manga_layout.addWidget(self.my_list)
        self.my_list.show()
    
    def next_button_click(self):
#         self.create_pre_nex_bt()
        self.count = self.count+1
        self.groupBox.close()

        #取得漫畫資訊
        data_dict = self.Manga_info(self.count,self.pageSize)
        
        #取得漫畫集數
        chapter = self.Manga_chapterList(data_dict['UpdateComicItems'][0]['UrlKey'])
        
        formLayout = QFormLayout()
        self.groupBox = QGroupBox()
        
        for manga in data_dict['UpdateComicItems']:
        # Create widget 製作漫畫圖框
            label = myLabel()
            pixmap = QPixmap(str('./photo/%s.jpg'%str(manga['ID'])))
            label.setFixedSize(200,300)
            label.setPixmap(pixmap)
            label.clicked.connect(partial(self.myLabel_clicked,manga))
            # Create widget 製作漫畫名稱框
            textbox = QLabel(manga['Title'])
            formLayout.addRow(textbox, label)
        self.groupBox.setLayout(formLayout)
#         self.groupBox.show()
#         self.scroll = QScrollArea()
        self.scroll.setWidget(self.groupBox)
#         self.scroll.setWidgetResizable(True)
        self.groupBox.show()
        
#         data_dict = self.Manga_info(self.count,self.pageSize)

#         chapter = self.Manga_chapterList(data_dict['UpdateComicItems'][0]['UrlKey'])
#         self.create_chapter_list(data_dict,chapter)

#         pixmap = QPixmap(str('%s.jpg'%str(self.count)))
#         self.label.setPixmap(pixmap)
        self.page_text.setText(str(self.count))
#         self.textbox.setText(data_dict['UpdateComicItems'][0]['Title'])

    def preb_button_click(self):
#         self.create_pre_nex_bt()
        if(self.count>1):
            self.count = self.count-1
            self.groupBox.close()

            #取得漫畫資訊
            data_dict = self.Manga_info(self.count,self.pageSize)

            #取得漫畫集數
            chapter = self.Manga_chapterList(data_dict['UpdateComicItems'][0]['UrlKey'])

            formLayout = QFormLayout()
            self.groupBox = QGroupBox()

            for manga in data_dict['UpdateComicItems']:
            # Create widget 製作漫畫圖框
                label = myLabel()
                pixmap = QPixmap(str('./photo/%s.jpg'%str(manga['ID'])))
                label.setFixedSize(200,300)
                label.setPixmap(pixmap)
                label.clicked.connect(partial(self.myLabel_clicked,manga))
                # Create widget 製作漫畫名稱框
                textbox = QLabel(manga['Title'])
                formLayout.addRow(textbox, label)
            self.groupBox.setLayout(formLayout)
    #         self.groupBox.show()
    #         self.scroll = QScrollArea()
            self.scroll.setWidget(self.groupBox)
    #         self.scroll.setWidgetResizable(True)
            self.groupBox.show()
#             data_dict = self.Manga_info(self.count)
#             chapter = self.Manga_chapterList(data_dict['UpdateComicItems'][0]['UrlKey'])
#             self.create_chapter_list(data_dict,chapter)

#             pixmap = QPixmap(str('%s.jpg'%str(self.count)))
#             self.label.setPixmap(pixmap)
            self.page_text.setText(str(self.count))
#             self.textbox.setText(data_dict['UpdateComicItems'][0]['Title'])
        else:
            buttonReply = QMessageBox.question(self, '提醒', "已經在最前面了", QMessageBox.Ok, QMessageBox.Ok)
            if buttonReply == QMessageBox.Ok:
                print('Yes clicked.')
    
    def myLabel_clicked(self,manga):
        #取得漫畫集數
        chapter = self.Manga_chapterList(manga['UrlKey'])
        self.create_chapter_list(manga,chapter)
        
    def Manga_info(self,pageindex,pagesize):
        Web_Site_URL = "http://www.manhuaren.com/manhua-list-area36-s2/dm5.ashx?"
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
        headers = { 'User-Agent' : user_agent }
        form_data = {
            'action':'getclasscomics',
            'pageindex':pageindex,
            'pagesize':pagesize,
            'categoryid':0,
            'tagid':0,
            'status':0,
            'usergroup':0,
            'pay':-1,
            'areaid':36,
            'sort':2,
            'iscopyright':0}

        data_dict = requests.post(Web_Site_URL,headers=headers,data=form_data,verify = False).json()
        for manga in data_dict['UpdateComicItems']:
            threading.Thread(target = self.Manga_make_jpg,args = (manga,)).start()
        return data_dict

    def Manga_make_jpg(self,manga):
        img_url = manga['ShowPicUrlB']
        try:
            os.mkdir('./photo')
        except:
            pass
        if (os.path.exists('./photo/%s.jpg'%str(manga['ID']))):
            pass
        else:
            res = requests.get(img_url,verify = False).content
            with open('./photo/%s.jpg'%str(manga['ID']),'wb') as f:     #二進位制寫入
                f.write(res)
            
    def Manga_chapterList(self,manga_UrlKey):
#         manga_index = 'http://www.manhuaren.com/%s/?from=/manhua-list-area36-s2/'%manga_UrlKey
        manga_index = 'http://www.manhuaren.com/%s/'%manga_UrlKey
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
        headers = { 'User-Agent' : user_agent }
        index = requests.get(manga_index,headers=headers, verify = False)
        soup = BeautifulSoup(index.text,"lxml")
        chapterRawLists = soup.find_all('a',class_='chapteritem')
        chapter_list = {}
        for i in chapterRawLists:
            chapter_list[i.text] = i.get_attribute_list('href')
        return chapter_list
    
    def onClicked(self,download_dict):
        button = self.sender()
        button.close()
        threading.Thread(target = self.download_manga,args = (download_dict,)).start()
        
    def download_manga(self,download_dict):
        print(download_dict)
        manga_src = download_dict['manga_src']
        manga_name = download_dict['manga_name']
        img_url = download_dict['manga_pic']
        manga_chap = download_dict['manga_chap']
        manga_index = ('https://www.manhuaren.com/%s/'%(manga_src))
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
        headers = { 'User-Agent' : user_agent }
        index = requests.get(manga_index,headers=headers)
        soup = BeautifulSoup(index.text,"lxml")
        Episode = soup.find_all('script')
        image_URL_part = str(Episode[-3]).split("'")[-4].split("|")
        try:
            os.mkdir(("./manga"))
        except Exception as e:
            pass
        try:
            os.mkdir(("./manga/%s/")%(manga_name))
            if (os.path.exists('./manga/%s/index.jpg'%(manga_name))):
                pass
            else:
                res = requests.get(img_url,verify = False).content
                with open('./manga/%s/%s.jpg'%(manga_name,'index'),'wb') as f:     #二進位制寫入
                    f.write(res)
        except Exception as e:
            pass
        pages = []
        for pt in image_URL_part:
            if (pt.find("_")!= (-1)):
                pages.append(pt)

        url_base = re.split('\.|/|-|://|\?|=|&',str(Episode[-3]).split("'")[-7])
        print(url_base)
        print(image_URL_part)
        # a = 10
        url_sample = []
        for i in range(len(url_base)):
            if( i == 11):
                url_sample.append("Pages_number")
                continue
            if(url_base[i].isdigit()):
#                 if((i)==5):
#                     url_sample.append(url_base[i])
#                 else:
                url_sample.append(image_URL_part[int(url_base[i])])
            elif(url_base[i].islower()):
                url_sample.append(image_URL_part[int((ord(url_base[i])-87))])
            else:
                url_sample.append(url_base[i][0])
        print(url_sample)
        for i in pages:
            url_sample[11] = i
            url = ('%s://%s-%s-%s-%s-%s.%s.%s/%s/%s/%s/%s.%s?%s=%s&%s=%s&%s=%s')%tuple(url_sample)
            print(url)
#             self.download_manga_page(url,manga_name,manga_chap,str(i),img_tp)
            
            try:
                
                try:
                    os.mkdir(("./manga/%s/%s/")%(manga_name,manga_chap))
                except Exception as e:
                    pass
#                     print(e)
                if (os.path.exists('./manga/%s/%s/%s.%s'%(manga_name,manga_chap,str(i),url_sample[12]))):
                    continue
                else:
                    res = requests.get(url,verify = False).content
                    with open('./manga/%s/%s/%s.%s'%(manga_name,manga_chap,str(i),url_sample[12]),'wb') as f:     #二進位制寫入
                        f.write(res)
            except Exception as e:
                print(e)
                continue
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
#     app.exec_()
    sys.exit(app.exec_())


# In[3]:


Web_Site_URL = "http://www.manhuaren.com/manhua-list-area36-s2/dm5.ashx?"
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
headers = { 'User-Agent' : user_agent }
form_data = {
    'action':'getclasscomics',
    'pageindex':1,
    'pagesize':1,
    'categoryid':0,
    'tagid':0,
    'status':0,
    'usergroup':0,
    'pay':-1,
    'areaid':36,
    'sort':2,
    'iscopyright':0}

data_dict = requests.post(Web_Site_URL,headers=headers,data=form_data,verify = False).json()
print(data_dict)


# In[ ]:


data_dict


# In[ ]:


img_url = data_dict['UpdateComicItems'][0]['ShowPicUrlB']

# 弄圖片
# res = requests.get(img_url).content
# with open('美女.jpg','wb') as f:     #二進位制寫入
#     f.write(res)


# In[6]:


# manga_index = 'https://www.manhuaren.com/%s/?from=/manhua-list-area36-s2/'%data_dict['UpdateComicItems'][0]['UrlKey']
manga_index = 'https://www.manhuaren.com/m1036548/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
headers = { 'User-Agent' : user_agent }
index = requests.get(manga_index,headers=headers)
soup = BeautifulSoup(index.text,"lxml")
Episode = soup.find_all('script')


# In[33]:


Episode = soup.find_all('a',class_='chapteritem')
# print(Episode)
# print(Episode.get_attribute_list('href'))
data_dict = {}
for i in Episode:
    data_dict[i.text] = i.get_attribute_list('href')
print(data_dict)


# In[39]:


for i in data_dict:
    print(i)
    print(data_dict[i][0])


# In[46]:


# print(str(Episode[-3]).split("'"))
for i in str(Episode[-3]).split("'"):
    if ("|") in i :
        print(i)


# In[47]:


m1036548 = str(Episode[-3]).split("'")[-4]
print(m1036548)


# In[44]:


m1032707= str(Episode[-3]).split("'")[-4]
print(m1032707)


# In[41]:


m1036643 = str(Episode[-3]).split("'")[-4]
print(m1036643)


# In[37]:


for i,URL_pt in zip(range(len(str(Episode[-3]).split("'")[-4].split('|'))),str(Episode[-3]).split("'")[-4].split('|')):
    print("index:",i)
    print(URL_pt)


# In[31]:


for i,URL_pt in zip(range(len(str(Episode[-3]).split("'")[-4].split('|'))),str(Episode[-3]).split("'")[-4].split('|')):
    print("index:",i)
    print(URL_pt)


# In[63]:


# print(max(len(m1036548.split('|')),len(m1032707.split('|')),len(m1036643.split('|'))))
for i in range(max(len(m1036548),len(m1032707),len(m1036643))):
    print(i)
    print(m1032707.split('|')[i])
    print(m1032707.split('|')[i].isdigit())
    
    print(m1036548.split('|')[i],m1032707.split('|')[i],m1036643.split('|')[i])
    print()


# In[61]:


url = '%s://%s-%s-%s-%s-%s.%s.%s/%s/%s/%s/'%(m1032707.split('|')[8],
                                    m1032707.split('|')[7],
                                    m1032707.split('|')[6],
                                    m1032707.split('|')[9],
                                    m1032707.split('|')[12],
                                    m1032707.split('|')[3],
                                    m1032707.split('|')[2],
                                    m1032707.split('|')[5],
                                    m1032707.split('|')[4],
                                    m1032707.split('|')[14],
                                    m1032707.split('|')[0],)
print(url)
# https://manhua1034-104-250-139-219.cdnmanhua.net/42/41644/1032707/5_2455.jpg?cid=1032707&type=1


# In[54]:


print(m1032707.split('|'))


# In[15]:


manga_src = 'm1036695'
# manga_src = 'm1036643'
# manga_src = 'm1036548'

manga_index = ('https://www.manhuaren.com/%s/'%(manga_src))
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
headers = { 'User-Agent' : user_agent }
index = requests.get(manga_index,headers=headers)
soup = BeautifulSoup(index.text,"lxml")
Episode = soup.find_all('script')

image_URL_part = str(Episode[-3]).split("'")[-4].split("|")
pages = []
Numbers = []
for pt in image_URL_part[:14]:
#     print(pt)
    if(pt.isdigit()):
        Numbers.append(pt)
    elif (pt.find('manhua')!= (-1)):
        first_domain = pt
    else:
        continue
print(first_domain)
print("**********")
for pt in image_URL_part[14:]:
    print(pt)
    if(pt == 'cid'):
        continue
    elif (pt.find("_")!= (-1)):
#         print("頁碼：",pt) 1_xxx
        pages.append(pt)
    elif (pt.isdigit()):
#         print("sid:",pt) 41644
        sid = pt
    elif (pt == 'newImgs'):
        continue
    elif (pt == 'var'):
        continue
    else:
        img_tp = pt #jpg/png/...
        print("unknow:",pt)
for i in pages:
    url = '%s://%s-%s-%s-%s-%s.%s.%s/%s/%s/%s/%s.%s?cid=%s&type=1'%('https',)
    print(url)
#     res = requests.get(url,verify = True).content
#     with open('%s.jpg'%str(i),'wb') as f:     #二進位制寫入
#         f.write(res)
#https://manhua1034-104-250-139-219.cdnmanhua.net/62/61646/1036695/6_1094.jpg?cid=1036695&type=1
# https://manhua1034-104-250-139-219.cdnmanhua.net/42/41644/1032707/5_2455.jpg?cid=1032707&type=1


# In[13]:


Numbers


# In[3]:


#https://manhua1034-104-250-139-219.cdnmanhua.net/62/61646/1036695/6_1094.jpg?cid=1036695&type=1
imgurl = "https://manhua1034-104-250-139-219.cdnmanhua.net/42/41644/1032707/5_2455.jpg?cid=1032707&type=1"
# os.mkdir(os.path.dirname("./%s/%s/"%("海盗高达dust",'第26話')))


# In[27]:


if not os.path.exists(os.path.dirname('./学妹前世是你妈/第16话')):
    os.mkdir(('./学妹前世是你妈/'))
    os.mkdir(('./学妹前世是你妈/第16话/'))
# os.path.exists(os.path.dirname('./学妹前世是你妈/第16话/'))


# In[5]:


import urllib


# In[7]:


opener=urllib.request.build_opener()


opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

urllib.request.urlretrieve(imgurl,'pic.jpg')


# In[ ]:





# In[2]:


manga_index = ('https://www.manhuaren.com/m1036911/')
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
headers = { 'User-Agent' : user_agent }
index = requests.get(manga_index,headers=headers)
soup = BeautifulSoup(index.text,"lxml")
Episode = soup.find_all('script')
# print(index.text)
image_URL_part = str(Episode[-3]).split("'")[-4].split("|")
print(image_URL_part)


# In[30]:


url_base = re.split('\.|/|-|://|\?|=|&',str(Episode[-3]).split("'")[-7])
print(url_base)
# a = 10
url_sample = []
for i in range(len(url_base)):
    if( i == 11):
        url_sample.append("Pages_number")
        continue
    if(url_base[i].isdigit()):
        if((i)==5):
            url_sample.append(url_base[i])
        else:
            url_sample.append(image_URL_part[int(url_base[i])])
    elif(url_base[i].islower()):
        url_sample.append(image_URL_part[int((ord(url_base[i])-87))])
    else:
        url_sample.append(url_base[i][0])
print(url_sample)
# print(re.split('\.|/',url_sample))
# page_url = re.split('\.|/',url_sample)
# del page_url[1]
# print(page_url)
print(('%s://%s-%s-%s-%s-%s.%s.%s/%s/%s/%s/%s.%s?%s=%s&%s=%s&%s=%s')%tuple(url_sample))


# In[31]:


# https://manhua1034-104-250-139-219.cdnmanhua.net/62/61646/1036695/6_1094.jpg?cid=1036695&type=1
# 0://1-2-3-4-5.6.7/8/9/10/11.12?13=14&15=16
url_sample


# In[32]:


url_sample[11] = '1_1234'
print(url_sample)


# In[4]:


def Manga_info(pageindex,pagesize):
    Web_Site_URL = "http://www.manhuaren.com/manhua-list-area36-s2/dm5.ashx?"
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
    headers = { 'User-Agent' : user_agent }
    form_data = {
        'action':'getclasscomics',
        'pageindex':pageindex,
        'pagesize':pagesize,
        'categoryid':0,
        'tagid':0,
        'status':0,
        'usergroup':0,
        'pay':-1,
        'areaid':36,
        'sort':2,
        'iscopyright':0}

    data_dict = requests.post(Web_Site_URL,headers=headers,data=form_data,verify = False).json()
#     threading.Thread(target = Manga_make_jpg,args = (data_dict,)).start()
    return data_dict
data_dict = Manga_info(1,10)


# In[5]:


data_dict


# In[7]:


def Manga_info(pageindex,pagesize):
    Web_Site_URL = "http://www.manhuaren.com/manhua-list-area36-s2/dm5.ashx?"
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
    headers = { 'User-Agent' : user_agent }
    form_data = {
        'action':'getclasscomics',
        'pageindex':pageindex,
        'pagesize':pagesize,
        'categoryid':0,
        'tagid':0,
        'status':0,
        'usergroup':0,
        'pay':-1,
        'areaid':36,
        'sort':2,
        'iscopyright':0}

    data_dict = requests.post(Web_Site_URL,headers=headers,data=form_data,verify = False).json()
    for manga in data_dict['UpdateComicItems']:
        threading.Thread(target = Manga_make_jpg,args = (manga,)).start()
    return data_dict

def Manga_make_jpg(manga):
    img_url = manga['ShowPicUrlB']
    res = requests.get(img_url,verify = False).content
    try:
        os.mkdir('./photo')
    except:
        pass
    with open('./photo/%s.jpg'%str(manga['ID']),'wb') as f:     #二進位制寫入
        f.write(res)
data_dict = Manga_info(1,10)


# In[ ]:




