#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 11:46:02 2020

@author: numata
"""

import tkinter as tk
from Utils.utils import import_config
from Pipeline import mainPipeline

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.master = master
        
        self.config = import_config()
        self.create_widgets()
        
        self.keys= []
        self.type_holder = []
        keys=list(self.config['setting'].keys())
        self.tex_instances = self.config['setting'].copy()
        
        self.keys2 = []
#        self.type_holder2 = []
        keys2= list(self.config['feature_freqs'].keys())
        self.tex_instances2 = self.config['feature_freqs'].copy()

        self.keys3 = []
#        self.type_holder3 = []
        keys3= list(self.config['Decoding'].keys())        
        self.tex_instances3 = self.config['Decoding'].copy()
        
        self.keys4 = []
#        self.type_holder4 = []        
        keys4= list(self.config['Subject'].keys())
        self.tex_instances4 = self.config['Subject'].copy()

        for k in range(len(list(self.config['setting'].keys()))):
            if (type(self.config['setting'][keys[k]]) == list)==True:
                ret=self.create_textbox(self.config['setting'][keys[k]][0])
                
                self.tex_instances[keys[k]+'_s'] = ret
                self.keys.append(keys[k]+'_s')
                self.type_holder.append('float')
                ret=self.create_textbox(self.config['setting'][keys[k]][1])
                self.tex_instances[keys[k]+'_e'] = ret
                self.keys.append(keys[k]+'_e')
                self.type_holder.append('float')
            elif (type(self.config['setting'][keys[k]]) == int)==True:
#                print(keys[k])
                ret=self.create_textbox(float(self.config['setting'][keys[k]]))
                self.tex_instances[keys[k]] = ret
                self.keys.append(keys[k])
                self.type_holder.append('float')
            else:
                ret=self.create_textbox(self.config['setting'][keys[k]])
                self.tex_instances[keys[k]] = ret
                self.keys.append(keys[k])
                self.type_holder.append('str')
        
        for k in range(len(list(self.config['feature_freqs'].keys()))):
                ret=self.create_textbox(self.config['feature_freqs'][keys2[k]][0])
                
                self.tex_instances2[keys2[k]+'_s'] = ret
                self.keys2.append(keys2[k]+'_s')
                ret=self.create_textbox(self.config['feature_freqs'][keys2[k]][1])
                self.tex_instances2[keys2[k]+'_e'] = ret
                self.keys2.append(keys2[k]+'_e')

        for k in range(len(list(self.config['Decoding'].keys()))):
  
                ret=self.create_textbox(float(self.config['Decoding'][keys3[k]]))
                self.tex_instances3[keys3[k]] = ret
                self.keys3.append(keys3[k])
                
        for k in range(len(list(self.config['Subject'].keys()))):
  
                ret=self.create_textbox(float(self.config['Subject'][keys4[k]]))
                self.tex_instances4[keys4[k]] = ret
                self.keys4.append(keys4[k])
            
    def create_widgets(self):

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "run analysis"
        self.hi_there["command"] = self.runDecoding
        self.hi_there.pack(side="top")
        
        self.update = tk.Button(self)
        self.update["text"] = "Update"
        self.update["command"] = self.Update
        self.update.pack(side="top")

        self.update = tk.Button(self)
        self.update["text"] = "test"
        self.update["command"] = self.freq_window
        self.update.pack(side="top")
        
        self.quit = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        self.quit.pack(side="bottom")

    def create_textbox(self, data, window=None):
        
        if window is None:
            self.textbox = tk.Entry()
        else:
            self.textbox = tk.Entry(window)
        self.textbox.insert(tk.END, data)
        self.textbox.pack(side="bottom")
        
        return self.textbox

    def freq_window(self):
        self.window_param =[]
        self.window = tk.Toplevel()
        add_param = tk.Button(self.window)
        add_param["text"] = "+"
        add_param["command"] = self.addlabel
        add_param.pack(side="top")

        add_param = tk.Button(self.window)
        add_param["text"] = "-"
        add_param["command"] = self.remlabel
        add_param.pack(side="top")
        
        self.quit = tk.Button(self.window, text="QUIT", fg="red", command=self.window.destroy)
        self.quit.pack(side="bottom")

    def addlabel(self):
        print('add')
        ret=self.create_textbox('test',self.window)
        self.window_param.append(ret)

    def remlabel(self):
        print('rem')
#        ret=self.create_textbox('test',self.window)
        if len(self.window_param)>0:
            for i in range(len(self.window_param)):
                self.window_param[i].destroy()
#                self.window_param[i].pack(side="bottom")

    def runDecoding(self):
        self.Update()
        mainPipeline(self.config)
        
    def Update(self):

        for ins in range(len(self.keys)):
            if self.type_holder[ins] == 'float':
                self.config['setting'][self.keys[ins]] = int(float(self.tex_instances[self.keys[ins]].get()))
            elif self.type_holder[ins] == 'str':
                self.config['setting'][self.keys[ins]] = self.tex_instances[self.keys[ins]].get()
        
        self.config['setting']['epoch_range'] = [float(self.config['setting']['epoch_range_s']), float(self.config['setting']['epoch_range_e'])]
        self.config['setting']['filter_band'] = [float(self.config['setting']['filter_band_s']), float(self.config['setting']['filter_band_e'])]
        self.config['setting']['baseline'] = [float(self.config['setting']['baseline_s']), float(self.config['setting']['baseline_e'])]

        freqs=list(self.config['feature_freqs'].keys())
        n=0
        for ins in range(len(freqs)):
            self.config['feature_freqs'][freqs[ins]] = [float(self.tex_instances2[self.keys2[n]].get()), float(self.tex_instances2[self.keys2[n+1]].get())]
            n=n+2
        
        for ins in range(len(self.keys3)):
            self.config['Decoding'][self.keys3[ins]] = int(float(self.tex_instances3[self.keys3[ins]].get()))

        for ins in range(len(self.keys4)):
            self.config['Subject'][self.keys4[ins]] = int(float(self.tex_instances4[self.keys4[ins]].get()))
        
#        print(self.config)

root = tk.Tk()
root.title('Decoding anlysis')
root.geometry("400x750")
app = Application(master=root)
app.mainloop()