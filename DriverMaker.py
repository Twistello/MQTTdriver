from json import load, dump
from bs4 import BeautifulSoup

dptMapping = {'1':'1','5':'3','6':'2','9':'8','17':'10'}

class Channels:

    def __init__(self, filename='MqttDriverTemplate.json',newFileName = 'MqttDriver.json', xmlFile = 'StressTestK301.xml', objectName = 'K301-302'):
        self.__filename = filename
        self.__newFileName = newFileName
        self.__xmlFile = xmlFile
        self.__object = objectName
        self.loadTemplate()                  # не забыть убрать и потом вызвать когда нужно

    def setObjectName(self, name):
        self.__object = name

    def setXmlFileName(self, name):
        self.__xmlFile = name

    def setNewFileName(self, name):
        self.__newFileName = name

    def loadTemplate(self):

        try:
            with open(self.__filename,encoding='utf-8') as driver:
                self.__driverTemplate = load(driver)
        except FileNotFoundError:
            self.__driverTemplate = {}

    def __save(self):

        with open(self.__newFileName, 'w') as driver:
            dump(self.__driverTemplate, driver)

    def __addChannels(self, data): #добавление комманд в шаблон драйвера

        self.__driverTemplate['Devices'][0]['Commands'] = data  # Массив словарей с коммандами
        self.__save()

    def loadXml(self):

        try:
            with open(self.__xmlFile, encoding='utf-8') as fp:
                self.__soupData = BeautifulSoup(fp.read(), "xml")
                self.__xmlData = self.__soupData.find_all('GroupAddress')

        except FileNotFoundError:
            self.__xmlData = {}

        self.__dataExtract()


    def __dataExtract(self):

        self.__dptMapping = {'1':'1','5':'3','6':'2','9':'8','17':'10'}
        self.__dpt = []
        self.__names = []
        groupAddressArray = self.__xmlData

        for address in groupAddressArray:
            try:
                addressName = address['Name'].replace('.', '_')
                addressType = self.__dptMapping[address['DPTs'].split('-')[1]]
                self.__dpt.append(addressType)
                self.__names.append(addressName)
            except:
                continue
        self.__makeCommands()


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

    



newMqttDriver = Channels()



newMqttDriver.loadXml()

