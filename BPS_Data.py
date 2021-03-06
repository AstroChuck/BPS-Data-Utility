#Author: Charlie Garcia
#Written for Barnard Propulsion Systems
#November 23, 2017
#License: Beerware until you make your first million dollars

import csv

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt

import shutil
import os


def data_import(filename):
    datafile = "fl82.csv"
    if filename is not None:
        datafile = filename

    first_row = True

    timeon = []
    flighttime = []
    eulerx = []
    eulery = []
    eulerz = []
    accelx = []
    accely = []
    accelz = []
    tvcx = []
    tvcy = []
    setx = []
    sety = []
    state = []
    temp = []
    alt = []
    pyro1 = []
    pyro2 = []
    pyro3 = []
    pyro4 = []
    abort = []
    batv = []
    sysstate = []

    with open(datafile) as csvfile:
        contents = csv.reader(csvfile, delimiter = ',')
        for row in contents:
            if first_row:
                first_row = False
            else:
                timeon.append(row[0])
                flighttime.append(row[1])
                eulerx.append(row[2])
                eulery.append(row[3])
                eulerz.append(row[4])
                accelx.append(row[5])
                accely.append(row[6])
                accelz.append(row[7])
                tvcx.append(row[8])
                tvcy.append(row[9])
                setx.append(row[10])
                sety.append(row[11])
                state.append(row[12])
                temp.append(row[13])
                alt.append(row[14])
                pyro1.append(row[15])
                pyro2.append(row[16])
                pyro3.append(row[17])
                pyro4.append(row[18])
                abort.append(row[19])
                batv.append(row[20])
                sysstate.append(row[21])
    data =[timeon,flighttime,eulerx,eulery,eulerz,accelx,accely,accelz,tvcx,tvcy,setx,sety,state,temp,alt,pyro1,pyro2,pyro3,pyro4,abort,batv,sysstate]
    return data

class BPSUtility(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Barnard Propulsion Systems Utility")
        self.geometry('900x700')

        notebook = ttk.Notebook(self)
        notebook.grid(row=1,column=0,columnspan=10,rowspan=10,sticky='NESW')

        self.home = Home(notebook)        
        self.plotter = Plotter(notebook)
        self.tuner = Tuner(notebook)
        self.config = Config(notebook)

        notebook.add(self.home, text="Home")
        notebook.add(self.plotter, text="Data Review")
        notebook.add(self.tuner, text="Tune Controller")
        notebook.add(self.config, text="Write Config")


class Home(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self,parent)
        button = ttk.Button(self, text="Exit",command=BPSUtility.destroy)
        button.pack()
        

class Plotter(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self,parent)

        self.data_dict = {'Time On':0,'Flight Time':1,'Euler X':2,'Euler Y':3,'Euler Z':4,
                          'Acceleration X':5, 'Acceleration Y':6, 'Acceleration Z':7, 'TVC X':8, 'TVC Y':9,
                          'Set X':10, 'Set Y':11, 'State':12, 'Temperature':13, 'Altitude':14,
                          'Pyro 1':15, 'Pyro 2':16, 'Pyro 3':17, 'Pyro 4':18, 'Abort':19,
                          'Battery Voltage':20,'System State':21}
        self.data = data_import(None)
        self.draw_plot()
        self.v = tk.StringVar()
        self.v.trace('w', self.update_plot)
        self.box = ttk.Combobox(self, textvariable=self.v)
        self.box['values'] = ('Altitude', 'Euler Angles', 'TVC X Performance','TVC Y Performance',"Pyro Channel Performance")
        self.box.current(0)
        self.box.pack()
        self.button = ttk.Button(self, text="Choose File", command=self.change_data)
        self.button.pack()

    def draw_plot(self):
        self.f = Figure(figsize=(5,5), dpi=100)
        self.a = self.f.add_subplot(111)
        self.a.plot(self.data[self.data_dict['Flight Time']],self.data[self.data_dict['Altitude']])
        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
    def update_plot(self, index, value, op):
        if self.box.get() == 'Altitude':
            self.a.clear()
            self.a.set_title("Altitude")
            self.a.plot(self.data[self.data_dict['Flight Time']],self.data[self.data_dict['Altitude']])
        if self.box.get() == 'Euler Angles':
            self.a.clear()
            self.a.plot(self.data[self.data_dict['Flight Time']],self.data[self.data_dict['Euler X']])
            self.a.plot(self.data[self.data_dict['Flight Time']],self.data[self.data_dict['Euler Y']])
            self.a.plot(self.data[self.data_dict['Flight Time']],self.data[self.data_dict['Euler Z']])
        if self.box.get() == "TVC X Performance":
            self.a.clear()
            self.a.plot(self.data[self.data_dict['Flight Time']],self.data[self.data_dict['Euler X']])
            self.a.plot(self.data[self.data_dict['Flight Time']],self.data[self.data_dict['Set X']])
        if self.box.get() == "TVC Y Performance":
            self.a.clear()
            self.a.plot(self.data[self.data_dict['Flight Time']],self.data[self.data_dict['Euler Y']])
            self.a.plot(self.data[self.data_dict['Flight Time']],self.data[self.data_dict['Set Y']])
        if self.box.get() == "Pyro Channel Performance":
            self.a.clear()
            self.a.plot(self.data[self.data_dict['Flight Time']],self.data[self.data_dict['Pyro 1']])
            self.a.plot(self.data[self.data_dict['Flight Time']],self.data[self.data_dict['Pyro 2']])
            self.a.plot(self.data[self.data_dict['Flight Time']],self.data[self.data_dict['Pyro 3']])
            self.a.plot(self.data[self.data_dict['Flight Time']],self.data[self.data_dict['Pyro 4']])
            self.a.plot(self.data[self.data_dict['Flight Time']],self.data[self.data_dict['Abort']])
            
        self.canvas.draw()

    def change_data(self):
        self.data_file = tk.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
        self.data = data_import(self.data_file)


class Tuner(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self,parent)

class Config(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self,parent)

        self.working_file = "CONFIG1.txt"

        self.reset_button = ttk.Button(self, text = "Reset Config", command= self.reset_file)
        self.reset_button.pack()
        
        self.VCAL_mode = tk.StringVar()
        self.VCAL_mode.trace('w', self.write_config_file)
        self.VCAL_box = ttk.Combobox(self, textvariable=self.VCAL_mode)
        self.VCAL_box['values'] = ('Off','1','2','3','4','5','6','7')
        self.VCAL_box.current(0)
        self.VCAL_box.pack()

        self.XCAL_mode = tk.StringVar()
        self.XCAL_mode.trace('w', self.write_config_file)
        self.XCAL_box = ttk.Combobox(self, textvariable=self.XCAL_mode)
        self.XCAL_box['values'] = ('Off','1','2','3','4','5','6','7')
        self.XCAL_box.current(0)
        self.XCAL_box.pack()

        self.YCAL_mode = tk.StringVar()
        self.YCAL_mode.trace('w', self.write_config_file)
        self.YCAL_box = ttk.Combobox(self, textvariable=self.YCAL_mode)
        self.YCAL_box['values'] = ('Off','1','2','3','4','5','6','7')
        self.YCAL_box.current(0)
        self.YCAL_box.pack()

        self.party_mode = tk.StringVar()
        self.party_mode.trace('w', self.write_config_file)
        self.party_mode_box = ttk.Combobox(self, textvariable=self.party_mode)
        self.party_mode_box['values'] = ('Off','1','2','3','4','5','6','7')
        self.party_mode_box.current(0)
        self.party_mode_box.pack()
        

    def reset_file(self):
        os.remove("CONFIG1.txt")
        shutil.copy("CONFIG_template.txt", "CONFIG1.txt")

    def write_config_file(self):
        os.remove(self.working_file)
        with open(self.working_file, 'w', encoding = 'utf-8') as file:
            file.writeline(self.VCAL_box.get())
            file.writeline(self.XCAL_box.get())
            file.writeline(self.YCAL_box.get())
            file.writeline(self.PCC0_box.get())
            file.writeline(self.PC1_box.get())
            file.writeline(self.PC2_box.get())
            file.writeline(self.PC3_box.get())
            file.writeline(self.PC4_box.get())
        #newfile
        #write VCAL
        #write XCAL
        #write YCAL
        #etc


app = BPSUtility()
app.mainloop()
