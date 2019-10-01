# Shania Ie and Pooja Pathak 
# CIS 41B
# Lab 4 
'''
This is a job listing application that lets the user checks for jobs that are posted at the job page of Github
lab4process.py works with multiprocessing, instead of threading. 
'''
import requests
import re
import tkinter as tk
import multiprocessing as mp
import tkinter.messagebox as tkmb
import tkinter.filedialog
import os
import sys
import time

def processData(getData, selectTup, index):
    '''
    processData:
    Creates as many processes as the number of languages/skills the user clicks. 
    Append each process to the processList and start each process at the same time.
    The procceses run in parallel, similar to threads. 
    Set the timer to run right before all the processes start, 
    and end the timer immediately after the last process is done. 
    It prints to console the elapsed time.
    Arguments: getData, selectTup, index
    Returns : None
    '''
    processList = []
    start = time.time()
    
    for i in range(len(selectTup)):
        p = mp.Process(target=getData, args=(selectTup[i], index))
        processList.append(p)
        p.start()
        
    for p in processList:
        p.join()
    
    print("Total elapsed time: {:.2f}s".format(time.time()-start)) 
        
class ExtractData:
    def __init__(self):
        '''
        Constructor 
        Declare class variables for the 5 skills and 2 locations
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
        Returns : None
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
        Constructor 
        Creates a GUI window that contains a title, an explanation label, 2 buttons, a listbox, and an OK button.
        The text for the 2 buttons are "Northern CA" "Southern CA".
        The location 'San Francisco' actually represents the Bay Area wide location and simplified to Northern CA. 
        Similarly, the LA-wide area is simplified to "Southern CA".
        When the user clicks on either button:
             A label shows up above the listbox to ask the user to select one or more skills in the listbox.
             The label acknowledges which button was clicked by the user (Northern CA or Southern CA)
        The user can select one or more skills and then clicks OK to commit the selection. 
        
        '''
        super().__init__(*args, **kwargs)
        self.E = ExtractData()
        self.index = -1
        self.title("Job Listing")
        tk.Label(self, text = 'Select Region').grid(columnspan = 2)
        tk.Button(self, text = 'Northern CA', command=lambda:self.lbFunc('Northern CA', 0)).grid(row = 1, column = 0)
        tk.Button(self, text = 'Southern CA', command=lambda:self.lbFunc('Southern CA', 1)).grid(row = 1, column = 1)
        self.LB = tk.Listbox(self, height = 5, width = 30, selectmode= 'multiple')
        self.LB.grid(row = 3, columnspan = 2)   
        tk.Button(self, text = 'OK', command= self.callbackfct).grid(row = 4,columnspan = 2)
        
    def lbFunc(self, region, index):
        '''
        lbFunc:
        Display the label that acknowledges which button was clicked by the user (Northern or Southern CA)
        Displays the 5 languages in the listbox
        Store the index of the language selected in class variable index 
        Arguments : region, index
        '''
        tk.Label(self, text = "Select skill(s) for "+ region + " and click OK").grid(row = 2, columnspan = 2)
        self.index = index
        self.LB.delete(0, tk.END)            
        self.LB.insert(tk.END, *self.E.language)
        
    def callbackfct(self):
        ''' 
        callbackfct:
        Once the user clicks OK, checks to make sure the user clicked at least one language. 
        Displays an error messagebox if user did not make a choice. 
        If there are user selections in the lisbox when the OK is clicked, then a file dialog window pops up to ask the user 
        to choose a directory. 
        The default directory that shows up at first is the user's current directory.
        This directory lets the user save the extracted data.
        When the data is retrieved from the API and stored in a file (see part 3), pop up an acknowledgment with the user's chosen directory name
        It creates a subdirectory under the user's chosen directory, the name of the subdirectory is "lab4output". 
        If a "lab4output" directory already exists in the user's chosen directory, then it doesn't create it again.
        Calls the processData function to create multiple processes
        '''
        if len(self.LB.curselection()) == 0:
            tkmb.showerror("Selection Error", "Please make a selection before clicking OK", parent=self)
        else:
            directory = tk.filedialog.askdirectory(initialdir = os.getcwd())
            if directory!= '':
                if not os.path.isdir('lab4output'):
                    os.mkdir('lab4output')
                os.chdir('lab4output')
                tkmb.showinfo("Save", "File saved in "+ os.getcwd(), parent= self) 
                processData(self.E.getData, self.LB.curselection(), self.index)
                os.chdir('..')
        

if __name__  ==  '__main__':
    mp.set_start_method('spawn') #to support spawning of child process
    win = MainWin()  #create a main Window 
    win.mainloop()

'''
PART C (Comparing Threads and Process):
Data Sets are tested according to the order (Northern CA)
Data sets       Threads         Process
    1           1.01 s          2.04 s
    2           1.17 s          2.28 s
    3           1.42 s          2.74 s
    4           1.07 s          2.22 s
    5           1.68 s          2.87 s
    
From the table above, we could see that threading is faster than processes.
Threads run in the same memory space while processes uses a separate memory. In threading,
the tasks run concurrently which may affect the run time. Also because they are in the
same memory, it is easier to access data. 
In processes, the tasks also runs in parallel, however with the usage of different memory space, 
it makes communication between the processes hard and needs more time. 
'''
    
