# Valve Control GUI for Advanced Automation Automtaic Ball Valves**************
# ----------------------------------------------------------------------------#

# Last edited 4/26/2023 by KJM
# No longer true, see git log for revision history after 4/26/2023 -JC
# version 4 updated to prevent threading errors caused by reading/writing to
# labjack simultaneously

# Instructions for Setting Up LabJack U12
#   You must use a U12, the python commands will not work with the U6 or
#   other versions.
#   Connect the trigger wires from the power supply as follows:
#      Yellow (valve 1) to AO0
#      Orange (valve 2) to AO1
#      Grey (ground) to any GND
#   Connect the position indicator wires from valve 1 as follows:
#       Orange to any GND
#       Purple to AI0
#       Brown to AI1
#   Connect the position indicator wires from valve 1 as follows:
#       Orange to any GND
#       Purple to AI2
#       Brown to AI3

# To sample, Valve 2 is open and Valve 1 is closed.
# For filter, valve 2 is closed and valve 1 is open.

# Data will automatically save to the folder where the .py file is stored,
# unless you uncomment lines 171 and 172
#   You need to define the path where you want the data to save in line 171

# ----------------------------------------------------------------------------#

# Import Packages
import tkinter as tk
import datetime
import time
import os
from os.path import exists
from threading import Thread, Lock
import sys
import u12

# Initialize LabJack U12 (note: will not work with the U6)
d = u12.U12()

# A mutex is a synchronization primative that ensures that two threads cannot
# access a variable at the *exact same* time. This is a common cause of
# sporadic and serious software bugs - if thread A writes to location that
# thread B reads from at the *exact same* CPU cycle, then all kinds of
# catastrophic failures can occur. Acquiring a mutex tells the CPU to
# essentially stop multithreading - only one thread can run while the mutex is
# acquired. Because of this, it is crucial that the processing time of whatever
# happens between "acquire" and "release" is as short as possible - no other
# processing can occur on the CPU while the mutex is locked.
mutex = Lock()

# Create variables for AO0 and AO1 Voltages
AO0_volts = 0.00  # initialize with CO2 valve closed
AO1_volts = 0.0

mutex.acquire()
d.eAnalogOut(AO0_volts, AO1_volts)  # Sets analog outputs on Labjack
mutex.release()

# Create main window
root = tk.Tk()

root.title('Valve Control')

# Define geometry of main window
root.geometry("600x400")


# Define function for button 1 command (sets valves to filter)
def btn1_click():
    canvas.itemconfig(box1, fill='gold')  # change box color to gold
    canvas.itemconfig(boxlabel, text='Open CO2')  # change text in box

    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    log_entry = ('\n' + current_time + ' CO2 Open\r')  # Valve1
    txt.configure(state='normal')  # enable editing of text log
    txt.insert(tk.END, log_entry)  # write to text log
    txt.configure(state='disabled')  # disable editing of text log
    # declare global variable so value carries over with button callback
    global AO0_volts
    # declare global variable so value carries over with button callback
    global AO1_volts
    # set the variable which determined when the valve will be closed
    tEnd = time.time() + 20
    while time.time() < tEnd:
        # Change AO0 Voltage
        AO0_volts = 5.00
        mutex.acquire()
        # set output voltage on LabJack - open filter valve
        d.eAnalogOut(AO0_volts, AO1_volts)
        mutex.release()

        # Change AO1 Voltage
        AO1_volts = 0.0
        time.sleep(1)  # waiting period when both valves are open
        mutex.acquire()
        # set output voltage on LabJack - close sample valve
        d.eAnalogOut(AO0_volts, AO1_volts)
        mutex.release()
        # time.sleep
        time.sleep(.1)  # buffer to stop buttons from being pressed too quickly


# Define function for button 2 command (sets valves to sample)
def btn2_click():
    canvas.itemconfig(box1, fill='cyan')  # change box color to blue
    canvas.itemconfig(boxlabel, text="CO2 Closed")  # change text in box
    # convert time to string
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    log_entry = ('\n' + current_time + ' CO2 Closed\r')  # Valve2
    txt.configure(state='normal')  # enable editing of text log
    txt.insert(tk.END, log_entry)  # write to text log
    txt.configure(state='disabled')  # disable editing of text log
    # declare global variable so value carries over with button callback
    global AO0_volts
    # declare global variable so value carries over with button callback
    global AO1_volts
    # Change AO1 Voltage
    AO1_volts = 0.00

    mutex.acquire()
    # set output voltage on LabJack - open sample valve
    d.eAnalogOut(AO0_volts, AO1_volts)
    mutex.release()
    time.sleep(1)  # waiting period when both valves are open

    # Change AO0 Voltage
    AO0_volts = 0.0
    mutex.acquire()
    # set output voltage on LabJack - close filter valve
    d.eAnalogOut(AO0_volts, AO1_volts)
    mutex.release()
    time.sleep(.1)  # buffer to stop buttons from being pressed too quickly


# Define function for exit button command
def exit_click():
    root.destroy()
    # convert time to string
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print('Program stopped by user at ' + current_time)
    sys.exit()


# Create canvas for trigger indicator boxes
canvas = tk.Canvas(root, width=100, height=100, bg='gray65')

# Create trigger indicator boxes
# initialize with filter valve open
box1 = canvas.create_rectangle(25, 25, 85, 50, fill='gold')

boxlabel = canvas.create_text((55, 37), text='Filter')
lab3 = canvas.create_text((50, 10), text='Trigger')

# Create canvas for status indicator boxes
canvas2 = tk.Canvas(root, width=100, height=100, bg='gray65')

# Create status indicator boxes
box1 = canvas2.create_rectangle(25, 25, 50, 50, fill='gray')
box2 = canvas2.create_rectangle(60, 25, 85, 50, fill='gray')

# Label status indicator boxes
lab1 = canvas2.create_text((37, 37), text='V1')
lab2 = canvas2.create_text((72, 37), text='V2')
lab3 = canvas2.create_text((50, 10), text='Status')

# Add buttons
btn1 = tk.Button(root, text='Open CO2', command=btn1_click)
btn2 = tk.Button(root, text='Close CO2', command=btn2_click)


# Create text box for output log
lab4 = tk.Label(text='Activity Log')
txt = tk.Text(root, bg='white', width=40, height=20)


# Exit button
exit_btn = tk.Button(root, text='Exit', command=exit_click)

# Pack widgets
canvas.pack(side='left')
canvas2.pack(side='left')
btn2.pack(side='right')
btn1.pack(side='right')
lab4.pack(side='top')
txt.pack()
exit_btn.pack()

# Grid widgets (Needs work)
# canvas.grid(row=1, column=0)
# canvas2.grid(row=2, column=0)
# lab4.grid(row=0, column=2)
# txt.grid(row=1, column=2)
# exit_btn.grid(row=3, column=2)
# btn1.grid(row=1, column=3)
# btn2.grid(row=2, column=3)

# ----------------------------------------------------------------------------#
# Write Data to File

# Initialize Save File
# define path to save data
# path = ("C:/Users/AMS/Documents/Filter Valve Control")
# os.chdir(path) #change working directory to path

# print current directory
print("Current working directory: {0}".format(os.getcwd()))

start_date = datetime.date.today()  # get today's date
file_date = start_date.strftime("%Y%m%d")
file_name = ("valve_data_" + file_date + ".txt")

file_exists = exists(file_name)  # check to see if filename exists in directory
n = 1  # number to be appended to new filename

while file_exists:  # loop until filename does not exist in directory
    # create new filename with _n
    file_name = ("valve_data_" + file_date + "_" + str(n) + ".txt")
    n += 1  # add 1 to n for next loop
    file_exists = exists(file_name)  # check to see if new filename exists

file1 = open(file_name, "w")  # open text file in write-only mode

file1.write("Valve Position and Trigger Data\n")  # write header line
# write header line
file1.write("Assured Automation V4 Electric Ball Valves\n")
# file1.write("Date, Time, Valve 1 Output, Valve 2 Output, Valve 1 Position,
#             Valve 2 Position\n") #write column headers

file1.write("DateTime, Valve 1 Output, Valve 2 Output, Valve 1 Position,"
            "Valve 2 Position, Vaisala_CH1V, Vaisala_CH2V, Temp, RH n")


# write data to file
def write_data_bkgd():
    while True:
        try:
            time_now = datetime.datetime.now()  # get current date and time
            # convert time to string
            current_time = time_now.strftime("%H:%M:%S")
            # convert time to string
            current_date = time_now.strftime("%m/%d/%Y")

            # current_datetime = time_now.strftime("%m/%d/%Y %H:%M:%S")

            # get valve 1 position (AI0 =
            valve1 = -999  # set -999 as no data
            mutex.acquire()
            AI0 = d.eAnalogIn(0)['voltage']  # Get AI0 voltage
            AI1 = d.eAnalogIn(1)['voltage']  # Get AI1 voltage
            mutex.release()

            if AI0 < 1 and AI1 > 1:
                valve1 = 0  # valve 1 is closed
            elif AI0 > 1 and AI1 < 1:
                valve1 = 1  # valve 1 is open

            # get valve 2 position (pin 18 = open = 1, pin 16 = closed = 0,
            # no data = -999)
            valve2 = -999  # set -999 as no data
            mutex.acquire()
            AI2 = d.eAnalogIn(2)['voltage']  # Get AI0 voltage
            AI3 = d.eAnalogIn(3)['voltage']  # Get AI1 voltage
            mutex.release()

            if AI2 < 1 and AI3 > 1:
                valve2 = 0  # valve 1 is closed
            elif AI2 > 1 and AI3 < 1:
                valve2 = 1  # valve 1 is open
# these lines of code are needed if you connect a T and/or RH probe************
            # get RH probe data
            # mutex.acquire()
            # AI4 = d.eAnalogIn(4)['voltage']  # Get AI4 voltage
            # AI5 = d.eAnalogIn(5)['voltage']  # Get AI5 voltage
            # mutex.release()

            # Temp = AI4*100-40
            # RH = AI5*100
# *****************************************************************************
            # Get analog output data
            AO0 = AO0_volts
            AO1 = AO1_volts

            # Create string of data
            rowData = [current_date, current_time, str(AO0), str(AO1),
                       str(valve1), str(valve2), "\n"]  # create a row of data

            # rowData = [current_datetime, str(AO0), str(AO1), str(valve1),
            #            str(valve2), str(AO2), str(AO3), str(Temp), str(RH),
            #            "\n"] #create a row of data

            rowString = ", ".join(rowData)  # create a string from row data

            file1.write(rowString)  # write row of data to file

            time.sleep(1)  # time.sleep 1 second
            file1.flush()  # flush internal buffer

            # Change indicator boxes on GUI
            if valve1 == 0:
                canvas2.itemconfig(box1, fill='red')
            elif valve1 == 1:
                canvas2.itemconfig(box1, fill='green')
            elif valve1 == -999:
                canvas2.itemconfig(box1, fill='grey')

            if valve2 == 0:
                canvas2.itemconfig(box2, fill='red')
            elif valve2 == 1:
                canvas2.itemconfig(box2, fill='green')
            elif valve2 == -999:
                canvas2.itemconfig(box2, fill='grey')

        except Exception as ex:
            # convert time to string
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            print('Program stopped unexpectedly at ' + current_time)
            print(ex)
            file1.close()  # close file
            sys.exit()


daemon = Thread(target=write_data_bkgd, daemon=True, name='Monitor')
daemon.start()

root.mainloop()  # Open window
