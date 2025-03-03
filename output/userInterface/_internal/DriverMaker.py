from json import load, dump
from bs4 import BeautifulSoup
import os

dptMapping = {'1':'1','5':'3','6':'2','9':'8','17':'10'}


class Channels:

    def __init__(self, filename='MqttDriverTemplate.json',newFileName = 'MqttDriver.json', xmlFile = 'StressTestK301.xml', objectName = 'DefaultObject'):
        username = os.getlogin()
        self.__xmlFileSavePath = fr'C:\Users\{username}\Desktop\MqttDriver.json'
        self.__filename = filename
        self.__newFileName = newFileName
        self.__xmlFile = xmlFile
        self.__object = objectName

    def setObjectName(self, name):
        self.__object = name

    def setXmlFileSaveDir(self, pathDir):
        self.__xmlFileSavePath = pathDir

    def setNewFileName(self, name):
        self.__newFileName = name

    def loadTemplate(self):

        try:
            with open(r'./MqttDriverTemplate.json',encoding='utf-8') as driver:
                self.__driverTemplate = load(driver)
        except FileNotFoundError:
            self.__driverTemplate = {}

    def save(self,savePath):

        with open(savePath, 'w') as driver:
            dump(self.__driverTemplate, driver)

    def __addChannels(self, data):

        self.__driverTemplate['Devices'][0]['Commands'] = data


    def loadXml(self, pathXml):

        try:
            with open(fr"{pathXml}", encoding='utf-8') as fp:
                self.__soupData = BeautifulSoup(fp.read(), "xml")
                self.__xmlData = self.__soupData.find_all('GroupAddress')

        except FileNotFoundError:
            self.__xmlData = {}

        self.__dataExtract()
        return self.__xmlData


    def __dataExtract(self):

        self.__dptMapping = {'1':'1','5':'3','6':'2','9':'8','17':'10'}
        self.__dpt = []
        self.__names = []
        groupAddressArray = self.__xmlData

        for address in groupAddressArray:
            try:
                addressName = address['Name'].replace('.', '_').strip(' ')
                addressType = self.__dptMapping[address['DPTs'].split('-')[1]]
                self.__dpt.append(addressType)
                self.__names.append(addressName)
            except:
                continue
        self.__makeCommands()

    def getAddresses(self):

        return self.__names


    def __makeCommands(self):

        self.__commands = []
        for name in self.__names:
            command = {
                    "Direction": 1,
                    "Name": name,
                    "Params":
                    {
                        "Topic": f'{self.__object}_{name}',
						"ValueType": self.__dpt[self.__names.index(name)],
						"QoS": 0,
						"Retain": 1
                    }
                }

            self.__commands.append(command)
        self.__addChannels(self.__commands)

        return self.__commands


