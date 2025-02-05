import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from tkinter import filedialog as fd
from tkinter import *
from DriverMaker import *

class App(tk.Tk):
  def __init__(self):
    super().__init__()

    self.__pathFile = ''

    # configure the root window
    self.title('ETS to IridiMQTT converter')
    self.geometry('700x350')
    self.columnconfigure(index=0, weight=1)
    self.rowconfigure(index=0, weight=1)
    self.rowconfigure(index=1, weight=1)
    self.rowconfigure(index=2, weight=1)

    # label
    self.objectNameLabel = ttk.Label(self, text='Ведите название объекта:')
    self.objectNameLabel.grid(row=0, column=0,pady=20, sticky=N)

    # entry
    self.objectName = ttk.Entry(self)
    self.objectName.grid(row=0, column=0,pady=50, sticky=N)

    # label
    self.labelChoose = ttk.Label(self, text='Выберите файл групповых адресов формата XML')
    self.labelChoose.grid(row=0, column=0,pady=35,sticky=S)

    # button
    self.buttonLoadXml = ttk.Button(self, text='Выбрать')
    self.buttonLoadXml['command'] = self.__callback
    self.buttonLoadXml.grid(row=0, column=0, sticky=S)

    # label
    self.labelSaveDirectory = ttk.Label(self, text='Выберите директорию для сохранения')
    self.labelSaveDirectory.grid(row=1, column=0,pady=35,sticky=S)

    # button
    self.buttonSaveDirectory = ttk.Button(self, text='Выбрать')
    self.buttonSaveDirectory['command'] = self.__saveAs
    self.buttonSaveDirectory.grid(row=1, column=0, sticky=S)

    self.buttonConvert = ttk.Button(self, text='Конвертировать')
    self.buttonConvert['command'] = self.__convertMqttDriver
    self.buttonConvert.grid(row=2, column=0, padx=20, pady=20, sticky=SE)

  def __callback(self):
      self.__pathFile = fd.askopenfilename(defaultextension='.xml', filetypes=[('XML files','*.xml')])

  def __saveAs(self):
      self.__saveAs = fd.asksaveasfilename(defaultextension='.xml', filetypes=[('JSON files','*.json')])

  def __open_error(self):
    showerror(title="Ошибка", message="Выбран неверный XML файл!")

  def __show_info(self):
    showinfo(title="Info", message="Успешно!")

  def __convertMqttDriver(self):
    newMqttDriver = Channels()
    newMqttDriver.loadTemplate()
    newMqttDriver.setObjectName(self.objectName.get().strip())
    validData = newMqttDriver.loadXml(self.__pathFile)
    if not validData:
      self.__open_error()
    else:
      newMqttDriver.save(self.__saveAs)
      self.__show_info()
if __name__ == "__main__":
  app = App()
  app.mainloop()