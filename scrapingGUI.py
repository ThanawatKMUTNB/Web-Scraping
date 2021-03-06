from ast import keyword
import encodings
from msilib.schema import ListView
from tabnanny import check
from tkinter.messagebox import NO
#from typing_extensions import Self
from xml.etree.ElementTree import tostring
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtCore import Qt, QDate
import pandas as pd
import os
import sqlite3
import glob
from os.path import dirname, realpath, join
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QTableWidget, QTableWidgetItem,QMessageBox, QProgressBar
import numpy as np
from datetime import datetime, timedelta
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import functools
import numpy as np
from regex import W
from tqdm import tqdm
from requests import delete
import Web_thread as WebThread
import importWin as windo 
import time
import threading
import nltk
import string
from nltk.corpus import stopwords
from pythainlp.corpus import thai_stopwords

import DataManager 
import twitter_scrap
import webNewNew
from Tw_Thread import *

#Test        
#ยังไม่แก้ช่วงวันที่ที่เลือกได้ใน tab 2 และ 3
class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

class Ui_MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        #self.calendarDateClick = cn.qDateBegin()
        self.table = QtWidgets.QTableView()
        self.filename = glob.glob(str(str(os.getcwd())+"\\Backup_Data\\*.csv"))

        self.df = dm.newUnion()
        

        self.dt = None

        self.getSince = str
        self.getUntil = str
        '''self.getSince_2 = str
        self.getUntil_2 = str'''
        self.getSince_3 = str
        self.getUntil_3 = str
        self.earliest = None
        self.lasted = None
        self.getDataDate1 = None
        self.getDataDate2 = None
        self.model = TableModel(self.df)
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.model)
        
        self.processWord = str
        #self.modelWeb = TableModel(dm.startSearch(["16-04-2022","17-04-2022"],['anime','animation']))
        self.modelWeb = None
        self.tableWeb = QtWidgets.QTableView()
        self.tableWeb.setModel(self.modelWeb)
        #self.maxDate()
        #self.setDate()
        self.keywords = self.df['Keyword'].tolist()
        self.keywords = list(set(self.keywords))
        self.tw_worddf = None

        self.th_stopwords = list(thai_stopwords())
        nltk.download('stopwords')
        self.en_stops = set(stopwords.words('english'))
        self.en_stops.update(list(string.ascii_lowercase))                  #add alphabet lower and upper for not collect
        self.en_stops.update(list(string.ascii_uppercase))
        self.en_stops.update(['0','1','2','3','4','5','6','7','8','9'])     #add number for not collect


    def showCalenderWin(self):
        self.MainWindow2 = QtWidgets.QMainWindow()
        self.ui2 = webNewNew.Ui_MainWindowSecond()
        self.ui2.setupUi(self.MainWindow2)
        self.MainWindow2.show()
        
    def dateSet(self) :
        #date = (datetime.now()).date() #แปลงวันที่มีเวลาติดมาด้วยเป็นวันเฉยๆ อันนี้ตั้งให้เป็นเวลาปัจจุบัน
        dm.formatdatetime('Time')
        since = dm.df['Time'].min().strftime('%Y/%m/%d')
        date = (datetime.strptime(since,'%Y/%m/%d')).date()
        self.dateEdit_1.setDate(date) #เอาเวลาที่ตั้งไว้ไปโชว์ใน GUI
        self.dateEdit_1.dateChanged.connect(self.dateSinceReturn) #ถ้าวันที่มีการเปลี่ยนแปลง จะเรียกฟังก์ชั้นมาใช้

        #date2 = (datetime.now()).date() #แปลงวันที่มีเวลาติดมาด้วยเป็นวันเฉยๆ อันนี้ตั้งให้เป็นเวลาปัจจุบัน
        until = dm.df['Time'].max().strftime('%Y/%m/%d')
        date2 = (datetime.strptime(until,'%Y/%m/%d')).date()
        self.dateEdit_2.setDate(date2) #เอาเวลาที่ตั้งไว้ไปโชว์ใน GUI
        self.dateEdit_2.dateChanged.connect(self.dateUntilReturn) #ถ้าวันที่มีการเปลี่ยนแปลง จะเรียกฟังก์ชั้นมาใช

    def dateSet_3(self) :
        #date = (datetime.now()).date() #แปลงวันที่มีเวลาติดมาด้วยเป็นวันเฉยๆ อันนี้ตั้งให้เป็นเวลาปัจจุบัน
        dm.formatdatetime('Time')
        since = dm.df['Time'].min()#.strftime('%Y-%m-%d')
        date = (datetime.strptime(since,'%Y-%m-%d')).date()
        self.dateEdit_5.setDate(date) #เอาเวลาที่ตั้งไว้ไปโชว์ใน GUI
        self.dateEdit_5.dateChanged.connect(self.dateSinceReturnWeb) #ถ้าวันที่มีการเปลี่ยนแปลง จะเรียกฟังก์ชั้นมาใช้

        #date2 = (datetime.now()).date() #แปลงวันที่มีเวลาติดมาด้วยเป็นวันเฉยๆ อันนี้ตั้งให้เป็นเวลาปัจจุบัน
        until = dm.df['Time'].max()#.strftime('%Y-%m-%d')
        date2 = (datetime.strptime(str(until),'%Y-%m-%d')).date()
        self.dateEdit_6.setDate(date2) #เอาเวลาที่ตั้งไว้ไปโชว์ใน GUI
        self.dateEdit_6.dateChanged.connect(self.dateUntilReturnWeb) #ถ้าวันที่มีการเปลี่ยนแปลง จะเรียกฟังก์ชั้นมาใช้

    '''def dateSet_3(self) :
        #date = (datetime.now()).date() #แปลงวันที่มีเวลาติดมาด้วยเป็นวันเฉยๆ อันนี้ตั้งให้เป็นเวลาปัจจุบัน
        dm.formatdatetime('Time')
        since = dm.df['Time'].min().to_pydatetime()#.date()#.strftime('%Y/%m/%d')
        print(type(since))
        #date = (datetime.strptime(since,'%Y-%m-%d %H:%M:%S')).date()
        date = since.date()
        self.dateEdit_5.setDate(date) #เอาเวลาที่ตั้งไว้ไปโชว์ใน GUI
        self.dateEdit_5.dateChanged.connect(self.dateSinceReturnWeb) #ถ้าวันที่มีการเปลี่ยนแปลง จะเรียกฟังก์ชั้นมาใช้

        #date2 = (datetime.now()).date() #แปลงวันที่มีเวลาติดมาด้วยเป็นวันเฉยๆ อันนี้ตั้งให้เป็นเวลาปัจจุบัน
        until = dm.df['Time'].max().to_pydatetime()#.strftime('%Y/%m/%d')
        #date2 = (datetime.strptime(str(until),'%Y-%m-%d %H:%M:%S')).date()
        date2 = until.date()
        self.dateEdit_6.setDate(date2) #เอาเวลาที่ตั้งไว้ไปโชว์ใน GUI
        self.dateEdit_6.dateChanged.connect(self.dateUntilReturnWeb) #ถ้าวันที่มีการเปลี่ยนแปลง จะเรียกฟังก์ชั้นมาใช้'''

    def dateSinceReturn(self) :
        self.getSince = self.dateEdit_1.date().toPyDate() #เป็นการอ่านค่าจากวันที่ที่ปรับไว้ในตัววันที่ของ GUI
        #print(self.getSince)
        return self.getSince

    def dateUntilReturn(self) :
        self.getUntil = self.dateEdit_2.date().toPyDate() #เป็นการอ่านค่าจากวันที่ที่ปรับไว้ในตัววันที่ของ GUI
        #print(self.getUntil)
        return self.getUntil

    def dateSinceReturnWeb(self) :
        dateChange = self.dateEdit_5.date().toPyDate()
        self.getSince_3 = dateChange.strftime('%d-%m-%Y') #เป็นการอ่านค่าจากวันที่ที่ปรับไว้ในตัววันที่ของ GUI
        #print(self.getSince)
        return self.getSince_3

    def dateUntilReturnWeb(self) :
        dateChange = self.dateEdit_6.date().toPyDate()
        self.getUntil_3 = dateChange.strftime('%d-%m-%Y') #เป็นการอ่านค่าจากวันที่ที่ปรับไว้ในตัววันที่ของ GUI
        #print(self.getUntil)
        return self.getUntil_3

    def showRealtime(self) : #BUTTON (search new) key in until time
        self.progressTime(0)
        print('real time')
        if self.dateSinceReturn()>self.dateUntilReturn():                               #return when until date greater than since date
            self.showErrorDialog()  
            return
        if datetime.now().date() <= self.dateUntilReturn():
            pass
        elif int(str(datetime.now().date()-self.dateUntilReturn())[0]) > 7:             #can not search tweet until greater than 7 day
            self.showErrorDialog2()
            return
        keywords = self.SearchBox1.text()                                               #get keyword from entry box
        keywords = keywords.split(',')                                                  #split text
        keywords = list(map(lambda x: x.lower(), keywords))                             #change all keywords to lower
        self.df = dm.getperiod(str(self.dateSinceReturn()),str(self.dateUntilReturn())) #set datafram from date range
        self.t1 = TwitterThread(parent=None,df=self.df)                                 #create thread
        tw.setdataframe(self.df)                                                        #set dataframe same with self.df
        self.t1.setdataframe(self.df)
        self.t1.until = str(self.dateUntilReturn())
        self.t1.Ans = 'real'
        if "" not in keywords:
            if self.showDialog() == 'Yes':

                self.t1.key = keywords                                                  #set keyword for search to thread
                dhave = []
                for keyword in keywords:
                    if keyword not in self.keywords:
                        dhave.append(keyword)
                self.keywords.extend(dhave)                                             #add new keyword
                self.t1.start()
                self.t1.countkeys.connect(self.progressTime)                            #get progreassbar value from thread to set
                self.t1.dataframe.connect(self.setTableTab1)                            #get df to set

            else:
                return
        else:                                                                           #search all key
            print('search new all keys')
            if self.showDialog() == 'Yes':                                              #r u sure for search all?
                self.t1.key = self.keywords

                self.t1.start()
                self.t1.countkeys.connect(self.progressTime)
                self.t1.dataframe.connect(self.setTableTab1)

                
            else:
                return
        #self.progressBar.value(0)

    def showDefaultFileTweetW(self) :                                                   #Refresh BUTTON for show collectkey(Tab2)
        self.model = TableModel(self.tw_worddf) 
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.model)
        self.tableView_2.setModel(self.model)
        return

    def ExportTab1(self):
        fname = 'Tweetcsv.csv'
        self.df['Time'] = pd.to_datetime(self.df['Time']).dt.strftime('%d/%m/%Y')
        if fname in glob.glob('*.csv'):
            os.remove(fname)
        self.df.to_csv(fname,index=False)
        print('Export Complete')
        self.showExportDialog()

    def button1(self):          #Search BUTTON Tab1
        print("\n\n")
        self.progressTime(0)
        print(len(self.df.index),'rows')
        print(self.dateSinceReturn(),self.dateUntilReturn())
        if self.dateSinceReturn()>self.dateUntilReturn():
            self.showErrorDialog()
            return
        self.df = dm.getperiod(str(self.dateSinceReturn()),str(self.dateUntilReturn()))     #set datafram from date range
        self.t1 = TwitterThread(parent=None,df=self.df)                                     #startThread
        self.t1.setdataframe(self.df)
        self.t1.oldkey = self.keywords                                                      #add old key to Thread
        self.t1.until = str(self.dateUntilReturn())                                         #set until date for search
        tw.setdataframe(self.df)                                                            #set same dataframe for search 
        keywords = self.SearchBox1.text()
        keywords = keywords.split(',')
        keywords = list(map(lambda x: x.lower(), keywords))                                  #change all keyword to lower
        if "" not in keywords:
            self.t1.key = keywords                                                           #set keyword for search
            print(len(keywords),self.t1.key)
            dhave = []
            for keyword in keywords:
                if keyword not in self.keywords:
                    dhave.append(keyword)                                                     #add new keyword
            if len(dhave) > 0:                                                                #have new keyword
                if datetime.now().date() <= self.dateUntilReturn():                           #for search until day greater than today
                    pass
                elif int(str(datetime.now().date()-self.dateUntilReturn())[0]) > 7:           #cannot search twitter new keyword greater than 7 day
                    self.showErrorDialog2()
                    return
                if self.showDialog() == 'Yes':                                                #search new keyword 
                    self.t1.Ans = 'yes'                                                       #set answer to thread
                    print('check\t',self.t1.oldkey)
                    self.t1.start()
                    self.t1.countkeys.connect(self.progressTime)                              #set progress bar value from thread for set
                    self.t1.dataframe.connect(self.setTableTab1)                                            
                    self.keywords.extend(dhave)                                               #add new keyword to self
                    
                else:                                                                         #choose NO

                    return
                    
            else:                                                                             #search old keyword

                self.t1.start()
                self.t1.dataframe.connect(self.setTableTab1)

                
            self.t1.setdataframe(self.df)                                                       #set dataframe for do before thread   ###if delete u can not search new word because self.oldkey get bug
            tw.setdataframe(self.df)
        else:                                                                                   #search all old keywords

            self.setTableTab1(self.df)


    


    def setPolarityTab1(self,df):
        polarity = df['Polarity'].value_counts()
        allrow = df.shape[0]
        if allrow == 0:
            allrow = 1
        pola = {'positive':0,'negative':0,'neutral':0}
        for p in pola:
            if p in polarity:
                pola[p] = int(polarity[p])                          #set polarity
        self.Tw_Positive = (pola['positive']/allrow)*100            #persentage
        self.Tw_Negative = (pola['negative']/allrow)*100
        self.Tw_Neutral = (pola['neutral']/allrow)*100
        self.Tw_Positive_Total = str(pola['positive'])              #total
        self.Tw_Negative_Total = str(pola['negative'])
        self.Tw_Neutral_Total = str(pola['neutral'])
        _translate = QtCore.QCoreApplication.translate
        self.labelPosTotal.setText(_translate("MainWindow", "Total " + self.Tw_Positive_Total + " tweets"))
        self.labelNegaTotal.setText(_translate("MainWindow", "Total " + self.Tw_Negative_Total + " tweets"))
        self.labelNeutralTotal.setText(_translate("MainWindow", "Total " + self.Tw_Neutral_Total + " tweets"))
        self.pushButtonPos.setText(_translate("MainWindow", f"{self.Tw_Positive :.3f}" + "%"))
        self.pushButtonNeu.setText(_translate("MainWindow", f"{self.Tw_Neutral:.3f}" + "%"))
        self.pushButtonNega.setText(_translate("MainWindow", f"{self.Tw_Negative:.3f}" + "%"))
        #print(self.Tw_Neutral,self.Tw_Positive,self.Tw_Negative)
    
    def setTableTab1(self,df):
        self.df = df
        self.model = TableModel(df) 
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.model)
        self.tableView.setModel(self.model)
        self.setPolarityTab1(df)                            #set GUI polarity
        self.labelShowKeywords()
        dm.concatfile(df)                                   #concat new search file to main df
        
        self.addlist()                                      #set keyword list tab1 in GUI
        self.progressTime(100)                              #set 100% progreassbar
        self.t1.stop()
        time.sleep(1)                                       #for can change tab
        self.t2 = CollectWordThread(parent=None,df=df,en_stops=self.en_stops,th_stopwords=self.th_stopwords)         #use df from tab1 to data processing tab2
        self.t2.start()
        self.t2.count.connect(self.progressTime_2)                  #set progressbar2 value from thread
        self.t2.dataframe.connect(self.CollectwordTab2)             #use dataframe from ThreadClass to setupDataframe
        #self.progressTime(0)
         
    
    def CollectwordTab2(self,df):
        self.tw_worddf = df
        self.addlist_2()                                            #set keyword list tab2 in GUI
        self.model2 = TableModel(self.tw_worddf) 
        self.table2 = QtWidgets.QTableView()
        self.table2.setModel(self.model2)
        self.tableView_2.setModel(self.model2)
        #print('tab2 finish')
        self.t2.stop()
        #self.progressTime_2(0)
        
    def button2(self) :                                                         # TAB2 BUTTON for seach collect word[:10]

        tw.setdataframe(dm.df)
        tenwords = self.tw_worddf['Word'].tolist()[:10]                         #get only top ten words in df
        tenwords = list(map(lambda x: x.lower(), tenwords))                     #set all word to lower
        self.t1 = TwitterThread(parent=None,df=self.df)                         #start thread for search
        self.t1.until = str(self.dateUntilReturn())
        self.t1.Ans = 'yes'
        if self.showDialog() == 'Yes':
            
            self.dateSet()
            dhave = []
            for keyword in tenwords:
                if keyword not in self.keywords:
                    dhave.append(keyword)                                          
            if len(dhave) > 0:
                self.keywords.extend(dhave)                                       #add new keywords
                self.t1.key = tenwords                                            #set keyword to tenword
                self.t1.start()
                self.t1.countkeys.connect(self.progressTime_2)
                self.t1.dataframe.connect(self.searchCollectTab)
                
                
                
            else:
                self.t1.Ans = 'no'
                self.t1.key = tenwords
                self.t1.start()
                self.t1.dataframe.connect(self.searchCollectTab)
        else:
            return
        #self.addlist_2()    
        self.addlist() 
        self.model = TableModel(self.df) 
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.model)
        self.tableView_2.setModel(self.model)                                       #set df to tab2
    
    def searchCollectTab(self,df):
        dm.concatfile(df)                               #concat new search file to main dataframe
        self.addlist()                                  #set keyword list to GUI
        self.t1.stop()
        self.model2 = TableModel(df) 
        self.table2 = QtWidgets.QTableView()
        self.table2.setModel(self.model2)
        self.tableView_2.setModel(self.model2)

    def refreshButton_1(self) :#
        self.progressTime(0)
        print('refresh')
        self.SearchBox1.clear()
        self.dateSet()
        self.df = dm.setdefaultDF()

        print(len(self.df.index),tw.keys)
        self.model = TableModel(self.df) 
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.model) #เอา df แปลงเป็นตารางเรียบร้อย
        self.tableView.setModel(self.model) #เอาตารางไปโชว์เลย
        self.setPolarityTab1(self.df)
        self.progressTime(100)
        return

    

    def deleteButton_1(self) : #สำหรับปุ่ม delete tab tweet
        if self.showDeleteDialog() == "Yes":
            keywords = self.SearchBox1.text()
            keywords = keywords.split(',')
            keywords = list(map(lambda x: x.lower(), keywords))
            for key in keywords:
                if key not in self.keywords:                        #delete keys that never existed. 
                    print('Key not found')
                    return
            if "" not in keywords:
                self.progressTime(0)
                self.dateSet()
                self.SearchBox1.clear()                              #clear entry box
                self.df = dm.deletekeyword(keywords)
                self.keywords = self.df['Keyword'].tolist()
                self.keywords = list(set(self.keywords))
                self.addlist()
                self.model = TableModel(self.df) 
                self.table = QtWidgets.QTableView()
                self.table.setModel(self.model)
                self.tableView.setModel(self.model)
                self.setPolarityTab1(self.df)
                self.progressTime(100)
            else:                                                       #do not add keyword
                print('nonKeyword')
                return
        return 

    def refreshButton_2(self) : 
        return
    

    def labelShowKeywords(self) :  #เอาไว้โชว์ label ตาม keyword ที่ใส่เข้าไปในตัว entry
        keywordShow = self.SearchBox1.text().lower()
        _translate = QtCore.QCoreApplication.translate
        self.labelShow.setText(_translate("MainWindow", keywordShow)) #ให้โชว์ข้อความ
        

    def addKeywordToList(self,listName) : #วน add keywords 
        for i in range(len(self.keywords)) :
            item = QtWidgets.QListWidgetItem(self.keywords)
            listName.addItem(item[i])

    def readFile(self,path):
        #path = win.path
        isdir = os.path.isdir(path)
        if isdir == False:
            fileExtension = path.split(".")
            # print(fileExtension[-1])
            if fileExtension[-1] == "csv":
                df = pd.read_csv(path)
            else:
                print("Excel ",path)
                #print(fileExtension[-1])
                df = pd.read_excel(path, engine = "openpyxl")
            return df

    def showDialog(self): #ไว้เด้งข้อความขึ้นมา ถ้าตัวที่ป้อนเข้ามาใน entry ไม่มีอยู่ใน keywords ที่กำหนด
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Do you want to search?") #แสดงข้อความ
        msgBox.setWindowTitle("Warning") #Title
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No) #มีปุ่ม yes และ no
        #ถ้าอยากเปลี่ยนปุ่ทเป็นแบบอื่น เปลี่ยนจากพวก yes หรือ no ได้เลย เช่น Save Cancel Ok Close Open
        #msgBox.buttonClicked.connect(msgButtonClick) ไม่มีไร เป็นการเชื่อมเวลากดปุ่ม ซึ่งในตอนนี้ไม่ได้เชื่อมฟังก์ชั่นอะไรไว้ 
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Yes: #ถ้ากด yes จะทำอะไร
            return 'Yes'
        elif returnValue == QMessageBox.No: #ถ้ากด no จะทำอะไร
            return 'No'
    
    def showDeleteDialog(self): #ไว้เด้งข้อความขึ้นมา ถ้าตัวที่ป้อนเข้ามาใน entry ไม่มีอยู่ใน keywords ที่กำหนด
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Are you sure?") #แสดงข้อความ
        msgBox.setWindowTitle("Warning") #Title
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No) #มีปุ่ม yes และ no
        #ถ้าอยากเปลี่ยนปุ่ทเป็นแบบอื่น เปลี่ยนจากพวก yes หรือ no ได้เลย เช่น Save Cancel Ok Close Open
        #msgBox.buttonClicked.connect(msgButtonClick) ไม่มีไร เป็นการเชื่อมเวลากดปุ่ม ซึ่งในตอนนี้ไม่ได้เชื่อมฟังก์ชั่นอะไรไว้ 
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Yes: #ถ้ากด yes จะทำอะไร
            return 'Yes'
        elif returnValue == QMessageBox.No: #ถ้ากด no จะทำอะไร
            return 'No'

    def showSearchDialogWeb(self): #ไว้เด้งข้อความขึ้นมา ถ้าตัวที่ป้อนเข้ามาใน entry ไม่มีอยู่ใน keywords ที่กำหนด
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Do you want to search?") #แสดงข้อความ
        msgBox.setWindowTitle("Warning") #Title
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No) #มีปุ่ม yes และ no
        #ถ้าอยากเปลี่ยนปุ่ทเป็นแบบอื่น เปลี่ยนจากพวก yes หรือ no ได้เลย เช่น Save Cancel Ok Close Open
        #msgBox.buttonClicked.connect(msgButtonClick) ไม่มีไร เป็นการเชื่อมเวลากดปุ่ม ซึ่งในตอนนี้ไม่ได้เชื่อมฟังก์ชั่นอะไรไว้ 
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Yes: #ถ้ากด yes จะทำอะไร
            return 'Yes'
        elif returnValue == QMessageBox.No: #ถ้ากด no จะทำอะไร
            return 'No'
    
    def showDialogWebForNew(self): #ไว้เด้งข้อความขึ้นมา ถ้าตัวที่ป้อนเข้ามาใน entry ไม่มีอยู่ใน keywords ที่กำหนด
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Do you want to search?") #แสดงข้อความ
        msgBox.setWindowTitle("Warning") #Title
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No) #มีปุ่ม yes และ no
        #ถ้าอยากเปลี่ยนปุ่ทเป็นแบบอื่น เปลี่ยนจากพวก yes หรือ no ได้เลย เช่น Save Cancel Ok Close Open
        #msgBox.buttonClicked.connect(msgButtonClick) ไม่มีไร เป็นการเชื่อมเวลากดปุ่ม ซึ่งในตอนนี้ไม่ได้เชื่อมฟังก์ชั่นอะไรไว้ 
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Yes: #ถ้ากด yes จะทำอะไร
            return 'Yes'
        elif returnValue == QMessageBox.No: #ถ้ากด no จะทำอะไร
            return 'No'

    def showTableWeb(self) :
        # print("\n\n")
        # print(len(self.dt.index),'rows')
        # print(self.dateSinceReturnWeb(),self.dateUntilReturnWeb())
        '''if self.dateSinceReturnWeb()>self.dateUntilReturnWeb():
            self.showErrorDialog()
            return'''
        self.dt = dm.getperiod(str(self.dateSinceReturnWeb()),str(self.dateUntilReturnWeb()))
        # print(list(set(self.dt['Keyword'].tolist())))
        tw.setdataframe(self.dt)
        keywords = self.SearchBox_3.text()
        keywords = keywords.split(',')
        keywords = list(map(lambda x: x.lower(), keywords))   #change to lower
        if "" not in keywords:
            print(len(keywords),keywords)
            dhave = []
            for keyword in keywords:
                if keyword not in self.keywords:
                    dhave.append(keyword)
            if len(dhave) > 0:
                if self.showDialogWebForNew() == 'Yes':      #search new 
                    self.keywords.extend(dhave)
                    self.dt = dm.startSearch([self.dateSinceReturnWeb(),self.dateUntilReturnWeb()],[keyword])
                    dm.concatfile(self.dt)
                    #print(list(set(dm.df['Keyword'].tolist())))
                    self.addlist()
                else:
                    self.dt = dm.startSearch([self.dateSinceReturnWeb(),self.dateUntilReturnWeb()],[keyword])
                    
                #dm.concatfile(self.dt)
            else:
                # print("Am here")
                # self.wt.start()
                # self.wt.any_signal.connect(self.upgradeProgressWeb)
                self.wt.start()
                self.wt.any_signal.connect(self.upgradeProgressWeb)
                self.dt = self.wt.getDf()
                # print(len(self.dt))
                # self.wt.any_signal.connect(self.upgradeProgressWeb)
        
                # dm.concatfile(self.dt)
                self.wt.stop()
                # self.upgradeProgressWeb(0)
            #self.dateSet()    
            #tw.setdataframe(self.dt)
        # self.wt.stop()
        # self.upgradeProgressWeb(0)
        
        print(self.SearchBox_3.text())
        print(len(self.dt.index),tw.keys)
        
        self.modelNew = TableModel(self.dt) 
        self.table2 = QtWidgets.QTableView()
        self.table2.setModel(self.modelNew)
        self.tableView_3.setModel(self.modelNew)

        #self.labelShowKeywords()
        #dm.startSearch(["16-04-2022","17-04-2022"],['anime','animation'])

    def searchNewWebButton(self) :
        keywords = webNewNew.Ui_MainWindowSecond().enterMassage()
        keywords = keywords.split(',')
        keywords = list(map(lambda x: x.lower(), keywords))
        dm.addNewWordToAll(keywords)
        #self.addlist_2()    
        self.addlist_3() 
        self.modelNew = TableModel(self.dt) 
        self.table2 = QtWidgets.QTableView()
        self.table2.setModel(self.modelNew)
        self.tableView_3.setModel(self.modelNew)

    def showErrorDialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Since date less than Until date")
        #msg.setInformativeText('More information')
        msg.setWindowTitle("Period time Error")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    
    def showExportDialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Export file Complete")
        #msg.setInformativeText('More information')
        msg.setWindowTitle("Export to CSV")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    
    def showErrorDialog2(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Can not search new keyword after 7 days")
        #msg.setInformativeText('More information')
        msg.setWindowTitle("Period time Error")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    
    

    def addlist(self): #ของ tab Tweet
        self.listView.clear()
        self.listView_3.clear()
        self.keywords = list(set(np.array(self.keywords,dtype=str)))
        self.keywords.sort()
        print(self.keywords)
        for i in range(len(self.keywords)) :
            item = QtWidgets.QListWidgetItem(self.keywords[i])
            self.listView.addItem(item)
        for i in range(len(self.keywords)) :
            item = QtWidgets.QListWidgetItem(self.keywords[i])
            self.listView_3.addItem(item)
            #self.listView_3.addItem(item)

    def addlist_2(self): #ไว้ add ค่าลงในตารางทางซ้าย (ที่ไว้โชว์ keyword) ของ tab TweetW
        self.listView_2.clear()
        words = self.tw_worddf['Word'].tolist()
        for i in words:
            self.listView_2.addItem(i)
        # for i in range(len(self.keywords)) :
        #     item = QtWidgets.QListWidgetItem(self.keywords[i])
        #     self.listView_2.addItem(item)

    def addlist_3(self): #ของ tab Web scraping
        keywordsWeb = os.listdir('collectkeys')
        self.listView_3.clear()
        #self.keywords.sort()
        for i in keywordsWeb :
            item = QtWidgets.QListWidgetItem(i)
            self.listView_3.addItem(item)
        return              

    

    def enterMassage(self) :
        
        enterM = self.SearchBox_3.text()
        enterM = enterM.split(',')
        
        keyword = list(map(lambda x: x.lower(), enterM))
        #print(keyword)
        DataManager.DataManager().addNewWordToAll(keyword)
        #self.addlist_3()

    def deleteButton_3(self) : #สำหรับปุ่ม delete tab tweet
        
        keywords = self.SearchBox_3.text()
        keywords = keywords.split(',')
        keywords = list(map(lambda x: x.lower(), keywords))
        if "" not in keywords:
            #self.progressTime(0)
            #self.dateSet()
            self.SearchBox_3.clear()
            self.dt = dm.delWordAllFile(keywords)
            self.keywords = self.df['Keyword'].tolist()
            self.keywords = list(set(self.keywords))
            self.listView_3.takeItem(keywords)
            self.model = TableModel(self.dt) 
            self.table = QtWidgets.QTableView()
            self.table.setModel(self.model) #เอา df แปลงเป็นตารางเรียบร้อย
            self.tableView_3.setModel(self.model) #เอาตารางไปโชว์เลย
            #self.progressTime(100)
        
        return 

    def deleteButton_3(self) : #สำหรับปุ่ม delete tab web
        deleteKey = self.SearchBox_3.text()
        deleteKey = deleteKey.split(',')
        deleteKey = list(map(lambda x: x.lower(), deleteKey))
        #print(deleteKey)
        self.dt = dm.deletekeyword(deleteKey)
        return
    
    

        

    def progressTime(self,counter): #สำหรับให้ Progress bar ทำงานในช่วงฟังก์ชั่นไหนทำงาน #
                            #ฉะนั้นเวลากดปุ่ม ก็จะเรียกใช้ฟังก์ชั่นนี้แทนการเรียกฟังก์ชั่นปกติตรงๆแทน
        self.progressBar.setValue(counter) #ให้ Progress bar เป็น 100 เมื่อมีการทำงานของฟังก์ชั่นนั้น
        #self.progressBar.setValue(0)
    
    def progressTime_2(self,counter) : #For Tab 2
        self.progressBar_2.setValue(counter)

    def progressTimeWeb(self) :
        keywords = self.SearchBox_3.text()
        keywords = keywords.split(',')
        keywords = list(map(lambda x: x.lower(), keywords)) 
        self.progressBar_3.setValue(0)
        sd = self.dateSinceReturnWeb()
        ed = self.dateUntilReturnWeb()
        
        self.wt = WebThread.WebThread(None,sd,ed,keywords)
        # print(sd,ed,keywords)
        self.wt.start()
        self.wt.any_signal.connect(self.upgradeProgressWeb)
        # self.wt.finished.connect(self.finishedThread)
        # self.wt.start()
        
        self.showTableWeb()
        
        # self.wt.stop()
        # self.progressBar_3.setValue(0)
        
    def upgradeProgressWeb(self,val):
        # print("\nupgradeProgressWeb : ",val,'\n')
        # val = dm.test()          
        self.progressBar_3.setValue(val)
    
    def exportWeb(self) :
        fname = 'Webcsv.csv'
        if self.dt == None :
            print("Not have data")
            pass
        else :
            file_filter = 'Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls)'
            response = QFileDialog.getSaveFileName(
            parent=self,
            caption='Select a data file',
            directory= 'Data File.dat',
            filter=file_filter,
            initialFilter='Excel File (*.xlsx *.xls)'
            )
            self.dt.to_csv(response, index = False, header=True)
            #print(response)



    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1000, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setTextFormat(QtCore.Qt.AutoText)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 8, 1, 1)
        self.dateEdit_1 = QtWidgets.QDateEdit(self.tab)
        self.dateEdit_1.setObjectName("dateEdit_1")
        self.gridLayout.addWidget(self.dateEdit_1, 0, 7, 1, 1)
        self.dateEdit_2 = QtWidgets.QDateEdit(self.tab)
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.gridLayout.addWidget(self.dateEdit_2, 0, 9, 1, 1)

        #self.settime = self.df['Keywords'].apply(lambda x:x**3) #มันเรียกเอา column ทั้งหมดมานับแล้วำนวณเป็นเวลาออกมา
        self.progressBar = QProgressBar(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 7, 1, 1, 9) 

        self.tableView = QtWidgets.QTableView(self.tab)
        self.tableView.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 3, 1, 1, 9)
        self.tableView.setModel(self.model) #show table in pyqt5
        #self.progressBar.setMaximum(1)


        self.line = QtWidgets.QFrame(self.tab)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 4, 3, 3, 1)
        self.line_2 = QtWidgets.QFrame(self.tab)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 4, 6, 3, 1)
        self.labelPosTotal = QtWidgets.QLabel(self.tab)
        self.labelPosTotal.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPosTotal.setObjectName("labelPosTotal")
        
        self.gridLayout.addWidget(self.labelPosTotal, 6, 1, 1, 2)
        self.labelPos = QtWidgets.QLabel(self.tab)
        self.labelPos.setAlignment(QtCore.Qt.AlignCenter)
        self.labelPos.setObjectName("labelPos")
        self.labelPos.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        self.gridLayout.addWidget(self.labelPos, 4, 1, 1, 2)
        self.pushButtonPos = QtWidgets.QPushButton(self.tab)
        self.pushButtonPos.setObjectName("pushButtonPos")
        self.gridLayout.addWidget(self.pushButtonPos, 5, 1, 1, 2)
        self.pushButtonNeu = QtWidgets.QPushButton(self.tab)
        self.pushButtonNeu.setObjectName("pushButtonNeu")
        self.gridLayout.addWidget(self.pushButtonNeu, 5, 7, 1, 3)
        self.pushButtonNega = QtWidgets.QPushButton(self.tab)
        self.pushButtonNega.setObjectName("pushButtonNega")
        self.gridLayout.addWidget(self.pushButtonNega, 5, 4, 1, 2)
        self.labelNega = QtWidgets.QLabel(self.tab)
        self.labelNega.setAlignment(QtCore.Qt.AlignCenter)
        self.labelNega.setObjectName("labelNega")
        self.labelNega.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        self.gridLayout.addWidget(self.labelNega, 4, 4, 1, 2)
        self.labelNegaTotal = QtWidgets.QLabel(self.tab)
        self.labelNegaTotal.setAlignment(QtCore.Qt.AlignCenter)
        self.labelNegaTotal.setObjectName("labelNegaTotal")
        self.gridLayout.addWidget(self.labelNegaTotal, 6, 4, 1, 2)
        self.labelNeutral = QtWidgets.QLabel(self.tab)
        self.labelNeutral.setAlignment(QtCore.Qt.AlignCenter)
        self.labelNeutral.setObjectName("labelNeutral")
        self.labelNeutral.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        self.gridLayout.addWidget(self.labelNeutral, 4, 7, 1, 3)
        self.labelNeutralTotal = QtWidgets.QLabel(self.tab)
        self.labelNeutralTotal.setAlignment(QtCore.Qt.AlignCenter)
        self.labelNeutralTotal.setObjectName("labelNeutralTotal")
        self.gridLayout.addWidget(self.labelNeutralTotal, 6, 7, 1, 3)
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_2.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.PushButton_2 = QtWidgets.QPushButton(self.tab)
        self.PushButton_2.setObjectName("PushButton_2")
        self.PushButton_2.clicked.connect(self.showRealtime)
        self.gridLayout.addWidget(self.PushButton_2, 2, 9, 1, 1)

        self.PushButton_1 = QtWidgets.QPushButton(self.tab)
        self.PushButton_1.setObjectName("PushButton_1")
        self.gridLayout.addWidget(self.PushButton_1, 2, 7, 1, 1)

        self.exportButton = QtWidgets.QPushButton(self.tab)
        self.exportButton.setObjectName("exportButton")
        self.exportButton.clicked.connect(self.ExportTab1)
        self.gridLayout.addWidget(self.exportButton, 7, 0, 1, 1)
        

        #เป็นวิธีการใส่พารามิเตอร์ลงไปในฟังก์ชั่นที่ต้องการเชื่อมกับปุ่ม
        #คือเวลาเชื่อมกับปุ่มมันใส่พารามิเตอร์ลงไปแบบ self.PushButton_1.clicked.connect(self.showSecondFile("WebScrapingData24.csv")) 
        #ถ้าใส่แบบนั้นมันจะบัค เลยต้องใช้ functools มาช่วย
        #btm1 = functools.partial()
        #self.PushButton_1.clicked.connect(self.progressTime)
        self.PushButton_1.clicked.connect(self.button1)

        #สร้างไว้สำหรับรีเฟรช
        btmRefresh_1 = functools.partial(self.refreshButton_1)   
        self.PushButtonRefresh = QtWidgets.QPushButton(self.tab)
        self.PushButtonRefresh.setObjectName("PushButtonRefresh")
        self.PushButtonRefresh.setGeometry(QtCore.QRect(10, 10, 30, 30))
        self.PushButtonRefresh.setIcon(QtGui.QIcon('reload_update_refresh_icon_143703.png')) #ไว้เชือมรูป
        self.PushButtonRefresh.clicked.connect(btmRefresh_1) #เชื่อมปุ่มได้แบบปกติเลย

        self.PushButtonDelete = QtWidgets.QPushButton(self.tab)
        self.PushButtonDelete.setObjectName("PushButtonDelete")
        self.PushButtonDelete.setGeometry(QtCore.QRect(50, 10, 30, 30))
        self.PushButtonDelete.setIcon(QtGui.QIcon('3481306.png')) #ไว้เชือมรูป
        self.PushButtonDelete.clicked.connect(self.deleteButton_1) #เชื่อมปุ่มได้แบบปกติเลย

        self.listView = QtWidgets.QListWidget(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView.sizePolicy().hasHeightForWidth())
        self.listView.setSizePolicy(sizePolicy)
        self.listView.setMidLineWidth(0)
        self.listView.setObjectName("listView")
        self.gridLayout.addWidget(self.listView, 2, 0, 4, 1)
        #self.addlist()

        self.SearchBox1 = QtWidgets.QLineEdit(self.tab)
        self.SearchBox1.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SearchBox1.sizePolicy().hasHeightForWidth())
        self.SearchBox1.setSizePolicy(sizePolicy)
        self.SearchBox1.setObjectName("SearchBox1")
        self.gridLayout.addWidget(self.SearchBox1, 2, 1, 1, 6)
        #test = self.SearchBox1.text() #text
        #checkNew1 = functools.partial(self.checkInput,self.SearchBox1.text())
        #self.PushButton_1.clicked.connect(checkNew1)

        self.label_1 = QtWidgets.QLabel(self.tab)
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1.setObjectName("label_1")
        self.label_1.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.gridLayout.addWidget(self.label_1, 1, 2, 1, 1)
        #self.processBarGUI()
        self.tabWidget.addTab(self.tab, "")
        self.setPolarityTab1(self.df)
        

        #tab2 
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout.setObjectName("gridLayout")
        
        '''self.dateEdit_3 = QtWidgets.QDateEdit(self.tab_2)
        self.dateEdit_3.setObjectName("dateEdit_3")
        self.gridLayout.addWidget(self.dateEdit_3, 0, 3, 1, 1)
        self.dateEdit_4 = QtWidgets.QDateEdit(self.tab_2)
        self.dateEdit_4.setObjectName("dateEdit_4")
        self.gridLayout.addWidget(self.dateEdit_4, 0, 5, 1, 1)'''
        #เผื่อใช้ เป็นวันที่ของ tab tweetw

        self.tableView_2 = QtWidgets.QTableView(self.tab_2)
        self.tableView_2.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView_2.sizePolicy().hasHeightForWidth())
        self.tableView_2.setSizePolicy(sizePolicy)
        self.tableView_2.setObjectName("tableView_2")
        self.gridLayout.addWidget(self.tableView_2, 3, 1, 1, 5)
        ################# โชว์ df ใน tab tweetw
        self.tableView_2.setModel(self.model) #show table in pyqt5
        #################

        self.progressBar_2 = QProgressBar(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar_2.sizePolicy().hasHeightForWidth())
        self.progressBar_2.setSizePolicy(sizePolicy)
        self.progressBar_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.progressBar_2.setTextVisible(True)
        self.progressBar_2.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar_2.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar_2.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar_2, 4, 4, 1, 2)

        self.label_4 = QtWidgets.QLabel(self.tab_2) #แสดงคำว่า "Tweeter keyword"
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label1")
        self.label_4.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 6)
        self.label_5 = QtWidgets.QLabel(self.tab_2) #แสดงคำว่า "Keyword"
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label2")
        self.label_5.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        '''self.label_6 = QtWidgets.QLabel(self.tab_2) #แสดงคำว่า "to"
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 4, 1, 1, QtCore.Qt.AlignHCenter)'''

        self.PushButton_4 = QtWidgets.QPushButton(self.tab_2)
        self.PushButton_4.setObjectName("PushButton_4")
        self.PushButton_4.clicked.connect(self.showDefaultFileTweetW)

        self.gridLayout.addWidget(self.PushButton_4, 2, 5, 1, 1)
        self.PushButton_3 = QtWidgets.QPushButton(self.tab_2)
        self.PushButton_3.setObjectName("PushButton_3")
        self.gridLayout.addWidget(self.PushButton_3, 2, 4, 1, 1)
        

        #เป็นวิธีการใส่พารามิเตอร์ลงไปในฟังก์ชั่นที่ต้องการเชื่อมกับปุ่ม
        #คือเวลาเชื่อมกับปุ่มมันใส่พารามิเตอร์ลงไปแบบ self.PushButton_1.clicked.connect(self.showSecondFile("WebScrapingData24.csv")) 
        #ถ้าใส่แบบนั้นมันจะบัค เลยต้องใช้ functools มาช่วย
        btm2 = functools.partial(self.button2)   
        self.PushButton_3.clicked.connect(btm2)

        self.listView_2 = QtWidgets.QListWidget(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView_2.sizePolicy().hasHeightForWidth())
        self.listView_2.setSizePolicy(sizePolicy)
        self.listView_2.setMidLineWidth(0)
        self.listView_2.setObjectName("listView_2")
        self.gridLayout.addWidget(self.listView_2, 3, 0, 1, 1)
        #self.addlist_2()
        
        self.labelShow = QtWidgets.QLabel(self.tab_2)
        self.labelShow.setEnabled(True)
        self.labelShow.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelShow.sizePolicy().hasHeightForWidth())
        self.labelShow.setSizePolicy(sizePolicy)
        self.labelShow.setObjectName("labelShow")
        self.gridLayout.addWidget(self.labelShow, 2, 1, 1, 3, QtCore.Qt.AlignHCenter)
        #test = self.SearchBox1.text() #text
        #checkNew1 = functools.partial(self.checkInput,self.SearchBox1.text())
        #self.PushButton_1.clicked.connect(checkNew1)
        self.tabWidget.addTab(self.tab_2, "")


        #tab3 
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout.setObjectName("gridLayout")
        self.label_9 = QtWidgets.QLabel(self.tab_3)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 0, 4, 1, 1, QtCore.Qt.AlignHCenter)
        self.dateEdit_5 = QtWidgets.QDateEdit(self.tab_3)
        self.dateEdit_5.setObjectName("dateEdit_5")
        self.gridLayout.addWidget(self.dateEdit_5, 0, 3, 1, 1)
        self.dateEdit_6 = QtWidgets.QDateEdit(self.tab_3)
        self.dateEdit_6.setObjectName("dateEdit_6")
        self.gridLayout.addWidget(self.dateEdit_6, 0, 5, 1, 1)

        self.tableView_3 = QtWidgets.QTableView(self.tab_3)
        self.tableView_3.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView_3.sizePolicy().hasHeightForWidth())
        self.tableView_3.setSizePolicy(sizePolicy)
        self.tableView_3.setObjectName("tableView_3")
        self.gridLayout.addWidget(self.tableView_3, 3, 1, 1, 5)
        self.tableView_3.setModel(self.modelWeb) #show table in pyqt5

        self.label_8 = QtWidgets.QLabel(self.tab_3)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label2")
        self.label_8.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.gridLayout.addWidget(self.label_8, 2, 0, 1, 1)

        self.PushButton_6 = QtWidgets.QPushButton(self.tab_3)
        self.PushButton_6.setObjectName("PushButton_6")
        self.PushButton_6.clicked.connect(self.enterMassage)

        self.gridLayout.addWidget(self.PushButton_6, 2, 5, 1, 1)
        self.PushButton_5 = QtWidgets.QPushButton(self.tab_3)
        self.PushButton_5.setObjectName("PushButton_5")
        self.gridLayout.addWidget(self.PushButton_5, 2, 4, 1, 1)
        self.PushButton_5.clicked.connect(self.progressTimeWeb)
        

        #เป็นวิธีการใส่พารามิเตอร์ลงไปในฟังก์ชั่นที่ต้องการเชื่อมกับปุ่ม
        #คือเวลาเชื่อมกับปุ่มมันใส่พารามิเตอร์ลงไปแบบ self.PushButton_1.clicked.connect(self.showSecondFile("WebScrapingData24.csv")) 
        #ถ้าใส่แบบนั้นมันจะบัค เลยต้องใช้ functools มาช่วย
        #btm1 = functools.partial(self.button1)   
        #self.PushButton_6.clicked.connect(btm1)

        self.progressBar_3 = QProgressBar(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar_3.setSizePolicy(sizePolicy)
        self.progressBar_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.progressBar_3.setTextVisible(True)
        self.progressBar_3.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar_3.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar_3.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar_3, 7,1, 1, 5) 

        self.exportButtonWeb = QtWidgets.QPushButton(self.tab)
        self.exportButtonWeb.setObjectName("exportButtonWeb")
        self.exportButtonWeb.clicked.connect(self.exportWeb)
        self.gridLayout.addWidget(self.exportButtonWeb, 7, 0, 1, 1)

        self.listView_3 = QtWidgets.QListWidget(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView_3.sizePolicy().hasHeightForWidth())
        self.listView_3.setSizePolicy(sizePolicy)
        self.listView_3.setMidLineWidth(0)
        self.listView_3.setObjectName("listView_3")
        self.gridLayout.addWidget(self.listView_3, 3, 0, 1, 1)
        #self.addlist_3()
        self.addlist()
        self.SearchBox_3 = QtWidgets.QLineEdit(self.tab_3)
        self.SearchBox_3.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SearchBox_3.sizePolicy().hasHeightForWidth())
        self.SearchBox_3.setSizePolicy(sizePolicy)
        self.SearchBox_3.setObjectName("SearchBox1")
        self.gridLayout.addWidget(self.SearchBox_3, 2, 1, 1, 3)
        #test = self.SearchBox1.text() #text
        #checkNew1 = functools.partial(self.checkInput,self.SearchBox1.text())
        #self.PushButton_1.clicked.connect(checkNew1)

        self.PushButtonRefresh_3 = QtWidgets.QPushButton(self.tab_3)
        self.PushButtonRefresh_3.setObjectName("PushButtonRefresh_3")
        self.PushButtonRefresh_3.setGeometry(QtCore.QRect(10, 10, 30, 30))
        self.PushButtonRefresh_3.setIcon(QtGui.QIcon('reload_update_refresh_icon_143703.png')) #ไว้เชือมรูป
        self.PushButtonRefresh_3.clicked.connect(self.addlist_3) 

        #btmRefresh_2 = functools.partial(self.refreshButton)   
        #self.PushButtonRefresh_3.clicked.connect(btmRefresh_2)

        self.PushButtonDelete_3 = QtWidgets.QPushButton(self.tab_3)
        self.PushButtonDelete_3.setObjectName("PushButtonDelete_3")
        self.PushButtonDelete_3.setGeometry(QtCore.QRect(50, 10, 30, 30))
        self.PushButtonDelete_3.setIcon(QtGui.QIcon('3481306.png')) #ไว้เชือมรูป
        self.PushButtonDelete_3.clicked.connect(self.deleteButton_3) 

        self.label_7 = QtWidgets.QLabel(self.tab_3)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label1")
        self.label_7.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 6)
        
        self.dateSet() #เรียกใช้ฟังก์ชั่นที่ตัดเวลาออก และคืนค่าวันที่ออกมา หากมีการเปลี่ยนแปลงวันที่ผ่านตัว GUI
        #self.dateSet_3()
        self.tabWidget.addTab(self.tab_3, "")


        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 812, 26))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menubar.sizePolicy().hasHeightForWidth())
        self.menubar.setSizePolicy(sizePolicy)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Main"))
        self.label_1.setText(_translate("MainWindow", "Twitter keyword"))
        self.label_2.setText(_translate("MainWindow", "Keyword"))
        self.label_3.setText(_translate("MainWindow", "to"))
        self.labelPos.setText(_translate("MainWindow", "Positive"))
        self.labelNega.setText(_translate("MainWindow", "Negative"))
        self.labelNeutral.setText(_translate("MainWindow", "Neutral"))
        self.PushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.PushButton_1.setText(_translate("MainWindow", "Search"))
        self.PushButton_2.setText(_translate("MainWindow", "Search new"))
        self.exportButton.setText(_translate("MainWindow", "Export"))
        self.PushButtonRefresh.setText(_translate("MainWindow", ""))
        self.PushButtonDelete.setText(_translate("MainWindow", ""))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tweet"))

        self.PushButton_3.setText(_translate("MainWindow", "Search"))
        self.PushButton_4.setText(_translate("MainWindow", "Default"))
        self.label_4.setText(_translate("MainWindow", "Twitter keyword"))
        self.label_5.setText(_translate("MainWindow", "Keyword"))
        #self.label_6.setText(_translate("MainWindow", "to"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "WordTweet"))

        self.PushButton_5.setText(_translate("MainWindow", "Search"))
        self.PushButton_6.setText(_translate("MainWindow", "Search new"))
        self.PushButtonRefresh_3.setText(_translate("MainWindow", ""))
        self.PushButtonDelete_3.setText(_translate("MainWindow", ""))
        self.exportButtonWeb.setText(_translate("MainWindow", "Export"))
        self.label_7.setText(_translate("MainWindow", "Web scraping"))
        self.label_8.setText(_translate("MainWindow", "Keyword"))
        self.label_9.setText(_translate("MainWindow", "to"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Webscraping"))

        self.dateEdit_1.setDisplayFormat(_translate("MainWindow", "yyyy/M/d")) #format ของวันที่ที่แสดง
        self.dateEdit_2.setDisplayFormat(_translate("MainWindow", "yyyy/M/d"))
        self.dateEdit_5.setDisplayFormat(_translate("MainWindow", "yyyy/M/d"))
        self.dateEdit_6.setDisplayFormat(_translate("MainWindow", "yyyy/M/d"))


if __name__ == "__main__":
    dm = DataManager.DataManager()
    tw = twitter_scrap.Twitter_Scrap()
    #Dialog = QtWidgets.QDialog()
    cn = webNewNew.Ui_MainWindowSecond()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
