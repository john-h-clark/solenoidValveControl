# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 08:02:17 2024

@author: jclark6
"""
# IMPORT NECESSARY PACKAGES ***************************************************
import tkinter as tk
import datetime
import time
import os
from os.path import exists
from threading import Thread, Lock
import sys
import u12
import sched
# INITIALIZE VARIABLES
injectTimes = {
    'time1': '00:00',
    'time2': '04:00',
    'time3': '08:00',
    'time4': '12:00',
    'time6': '16:00',
    'time7': '20:00'
    }
AO0_volts = 0.00
AO1_volts = 0.00
mutex = Lock()
# Initialize LabJack U12 (note: will not work with the U6)
d = u12.U12()

# DEFINE FUNCTIONS ************************************************************
# def switchOn():
#     AO0_volts = 5.00
#     AO1_volts = 0.00
#     print(f'ON:\nAO0 Voltage = {AO0_volts}\nAO1 Voltage = {AO1_volts}')
#     time.sleep(5)
#     switchOff()


# def switchOff():
#     AO0_volts = 0.00
#     AO1_volts = 0.00
#     print(f'OFF:\nAO0 Voltage = {AO0_volts}\nAO1 Voltage = {AO1_volts}')


def timedInjection():
    # define end time to be 30 seconds from current time
    tEnd = time.time() + 20
    while time.time() < tEnd:
        # Change AO0 Voltage
        AO0_volts = 5.00
        AO1_volts = 0.00
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
        # Change AO0 Voltage
        AO0_volts = 0.0
        mutex.acquire()
        # set output voltage on LabJack - close filter valve
        d.eAnalogOut(AO0_volts, AO1_volts)
        mutex.release()


# ----------------------------------------------------------------------------#
# event loop
while True:
    timedInjection()
    time.sleep(14400)
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

        except Exception as ex:
            # convert time to string
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            print('Program stopped unexpectedly at ' + current_time)
            print(ex)
            file1.close()  # close file
            sys.exit()


daemon = Thread(target=write_data_bkgd, daemon=True, name='Monitor')
daemon.start()
