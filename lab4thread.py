# Shania Ie and Pooja Pathak
# CIS 41B
# Lab 4

# Description:
# This is a job listing application that lets the user checks for jobs that are posted at the job page of Github.
# It uses threading to get data according to the user selection

import requests
import re
import tkinter as tk
import threading
import tkinter.messagebox as tkmb
import tkinter.filedialog
import os
import sys
import time

class ExtractData:
    def __init__(self):
        '''
        Constructor:
        Declaring class variables for the 5 skills and the 2 locations
        '''
        self.place = ['San Francisco','Los Angeles']
        self.language = ['C++','Java','Python','Ruby','Javascript']
        
    def getData(self, userChoice, index):
        '''
        getData:
        Request data from the API with the given location and skill
        With the JSON data received, extract the company name, location, and job title for each matching job posting.
        Write the data to an output text file
        Arguments: userChoice, index
        Returns: None
        '''
        page = requests.get('https://jobs.github.com/positions.json?description='+ self.language[userChoice] +'&location='+ self.place[index])
        
        resultList = page.json()
        self.jobList = []
        for d in resultList:
            m = re.search('(\w+\s?)*',d['location'])
            self.jobList.append((d['company'], m.group(), d['title']))
        
        with open(self.language[userChoice]+'_job.txt','w') as outfile:
            for i in range(len(self.jobList)):
                outfile.write("{:50s} {:40s} {:40s} {:s}".format(self.jobList[i][0], self.jobList[i][1],self.jobList[i][2],'\n'))
        

class MainWin(tk.Tk):
    def __init__(self, *args, **kwargs):
        '''
        Constructor:
        Creates a GUI window that contains a title, an explanation label, 2 buttons, a listbox, and an OK button.
        The text for the 2 buttons are "Northern CA" "Southern CA". The location 'San Francisco' actually represents 
        the Bay Area wide location and simplified to Northern CA. Similarly, the LA-wide area is simplified to "Southern CA".
        When the user clicks on either button: A label shows up above the listbox to ask the user to select one or more skills
        in the listbox. The label acknowledges which button was clicked by the user (Northern CA or Southern CA)
        '''
        super().__init__(*args, **kwargs)
        self.E = ExtractData()
        self.index = -1
        self.title("Job Listing")
        tk.Label(self, text = 'Select Region').grid(columnspan = 2)
        tk.Button(self, text = 'Northern CA', command=lambda:self.lbFunc('Northern CA',0)).grid(row = 1, column = 0)
        tk.Button(self, text = 'Southern CA', command=lambda:self.lbFunc('Southern CA',1)).grid(row = 1, column = 1)
        self.LB = tk.Listbox(self, height = 5, width = 30, selectmode= 'multiple')
        self.LB.grid(row = 3, columnspan = 2)   
        tk.Button(self, text = 'OK', command= self.callbackfct).grid(row = 4,columnspan = 2)
        
    def lbFunc(self,region,index):
        '''
        lbFunc:
        Displays 5 skills or descriptions in the listbox.
        User can select one or more skills and then clicks OK to commit the selection. 
        Arguments = region, index
        Returns = None
        '''
        tk.Label(self, text = 'Select skill(s) for '+ region +' and click OK').grid(row = 2, columnspan = 2)
        self.index = index
        self.LB.delete(0, tk.END)            
        self.LB.insert(tk.END, *self.E.language)
        
    def callbackfct(self):
        '''
        callbackfct:
        Pop up a file dialog window to let the user choose a directory to save the extracted data.
        Create a subdirectory under the user's chosen directory, the name of the subdirectory is "lab4output". 
        If a "lab4output" directory already exists in the user's chosen directory, then it will not create a new one.
        If the user selects a directory, then store the extracted information in a new text file in the "lab4output"
        directory, which is under the user's chosen directory. 
        Arguments = None
        Returns = None
        '''
        if len(self.LB.curselection()) == 0:
            tkmb.showerror("Selection Error", "Please make a selection before clicking OK", parent=self)
        else:
            directory = tk.filedialog.askdirectory(initialdir = os.getcwd())
            if directory != '':
                if not os.path.isdir('lab4output'):
                    os.mkdir('lab4output')
                os.chdir('lab4output')
                state = tkmb.showinfo("Save", "File saved in "+ os.getcwd(), parent= self) 
                self.threadingData()
                os.chdir('..')
                
    def threadingData(self):
        '''
        threadingData:
        Creates a list of threads according to the user selection. Each selected skills are passed
        into the thread and it runs at the same time and independently from each other. 
        Set a timer to run right before all the threads start, and end the timer immediately after the last thread is done.
        Print to console the elapsed time.
        Arguments = None
        Return = None
        '''
        threads = []
        start = time.time()
        for i in range(len(self.LB.curselection())):
            t = threading.Thread(target=self.E.getData, args=(self.LB.curselection()[i], self.index))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
            
        print("Total elapsed time: {:.2f}s".format(time.time()-start))
        
def main():
    win = MainWin()
    win.mainloop()
main()

