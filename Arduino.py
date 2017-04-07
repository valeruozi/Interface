# -*- coding: utf-8 -*-
"""
Created on Thu Apr 06 12:15:37 2017

@author: valeruozi
"""

import serial
import time

port = "COM26"
baudrate = 115200

MSG_OK = "ok"
MSG_ERROR = "error"
MSG_DELIMITER = " \r\n"
NCMD = 9

TRAP_LEFT = 'l'
TRAP_RIGHT = 'r'
TRAP_LEFT_MAX = 20
TRAP_RIGHT_MAX = 19
TRAP_ID_A = 'a'
TRAP_ID_B = 'b'
TRAP_N = (2*(TRAP_LEFT_MAX+TRAP_RIGHT_MAX))
TRAP_CMD_ALL = "all"


class PCB:
    def __init__(self,port):
        self.port = port
        self.baudrate = 115200

    def open_serial(self):
        self.arduino = serial.Serial(self.port, self.baudrate)

    def close_serial(self):
        self.arduin.close()

    def get_command(self):
        self.command = raw_input('Command? ')

        if self.command[0:3] == 'on ': #lo spazio basta per distinguerlo da only
            self.action = self.command[0:2]  # per ora comincio con on (2 caratteri), ma deve funzionare con on off only...
            self.state = get_on()       # todo-vale devo anche fare on all
            if self.command[3:6] == 'all':
                set_on(1)
            i = 3
            self.side = []
            self.num = []
            self.id = []
            if len(self.command) > i:
                self.side.append(self.command[3])  # se il comando è solo on senza l12b questi non ci sono
                self.num.append(self.command[4:6])
                self.id.append(self.command[8])
                if self.side[i] != ('l' or 'r') or self.num == '-1' or self.id != ('a' or 'b'):
                    print MSG_ERROR
                i+5
                set_on(0)
        elif self.command[0:3] == 'off':
            self.action = self.command[0:2]
            get_off()  # todo-vale ...etc per tutti cambiando la dimensione di command per comandi come abus e only


        else:
            print "Unknown command"


    def get_abus(self):  # todo-vale per tutti devo fare set e get, la cosa è comunque descritta sia nell'help che nella funzione stessa
                    #di solito se scrivo solo get l12a ottengo lo status attuale, se scrivo set l12a setto i relativi switch

    def set_abus(self):


    def get_acon(self):
    def set_acom(self):

    def get_bias(self):
    def set_bias(self):

    def get_on(self):
        return self.arduino.read_until(MSG_DELIMITER)  # todo-vale o \n devo provare

    def set_on(self, value):
        if value == 1: # all
            self.arduino.write('on all')
        if value == 0:
            self.str = []
            self.arduino.write('on ')
            for i in range(0,len(self.side))
                self.str.append(' ' + self.side[i] + self.command[i] + self.id[i])
                self.arduino.write(self.str)


port = 'COM26'
board = PCB(port)
board.open_serial()

while True:
    board.get_command()

board.close_serial()
