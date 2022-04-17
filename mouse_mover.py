import pyautogui, sys, time
import win32api
import tkinter as tk
from tkinter import messagebox
import threading
import logging

#Define function for logging

def log():
    logging.basicConfig(filename = 'log.log',level=logging.DEBUG, format='\n%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.error("Exception occurred", exc_info=True)


#Create the main window
root = tk.Tk()

#Create labels and define the position

tk.Label(root, text="Idle Time (Seconds)").grid(row=0)
tk.Label(root, text="Move Distance").grid(row=1)



#Declare user input variables and set position


idle_time_input = tk.Entry(root)
move_distance = tk.Entry(root)

idle_time_input.grid(row=0, column=1)
move_distance.grid(row=1, column=1)


#set default for both idle time and move distance

default1=10
default2=50

idle_time_input.insert(0,default1)
move_distance.insert(0,default2)




#list to control execution (start/stop)

state=[0,0]



#Function for threading

  
def thread1():
    # Call mouse_move function
    t1=threading.Thread(target=mouse_move)
    t1.setDaemon(True)
    t1.start()
    b1["state"] = "disabled"
    

def thread2():
    # Call stop function
    t2=threading.Thread(target=stop)
    t2.setDaemon(True)
    t2.start()
    b1["state"] = "normal"
    t2.join()
    

#Funtion to move mouse pointer and middle click

def mouse_move():
    
    try:

        #get input and convert to int

        idle = idle_time_input.get()
        int_idle = int(idle)

        move = move_distance.get()
        int_move = int(move)

        while (state[0]==0 & state[1]==0):
            idle_time = (win32api.GetTickCount() - win32api.GetLastInputInfo())/ 1000.0
        
            if idle_time >=int_idle :
                
                #print('moving mouse...')
                pyautogui.move(int_move,0)
                pyautogui.click(button='middle') 
                time.sleep(int_idle)
                pyautogui.move(-int_move,0)
            else:
                #print('sleeping until idle time')
                time.sleep(int_idle)
            if state[1]==1:
                reset_state = state
                reset_state[1] = 0
                #print('stopping...')
                break
            else:
                continue
    except :
        tk.messagebox.showerror("Error","An Error has occured")
        log()

#Funtion to pause mouse mover

def stop():
    
    stop_state = state
    stop_state[1]=1
    #print('stop function called')
    

#Create buttons to start and stop

b1=tk.Button(root,text='Start', command=thread1)

b1.grid(row=4,column=1,sticky=tk.W,pady=4)

b2=tk.Button(root,text='Stop', command=thread2)

b2.grid(row=4,column=2,sticky=tk.W,pady=4)

    

root.mainloop()           

