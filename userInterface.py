import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo


class App(tk.Tk):
  def __init__(self):
    super().__init__()

    # configure the root window
    self.title('ETS to IridiMQTT converter')
    self.geometry('700x300')

    # label
    self.objectNameLabel = ttk.Label(self, text='Ведите название объекта:')
    self.objectNameLabel.pack()

    # entry
    self.objectName = ttk.Entry(self, text='Выберите XML файл ->')
    self.objectName.pack()

    # label
    self.label = ttk.Label(self, text='Выберите XML файл ->')
    self.label.pack()

    # button
    self.button = ttk.Button(self, text='Выбрать')
    self.button['command'] = self.callback
    self.button.pack()

  def button_clicked(self):
    showinfo(title='Information', message='Hello, Tkinter!')

  def callback(self):
      name = fd.askopenfilename()
      print(name)


if __name__ == "__main__":
  app = App()
  app.mainloop()