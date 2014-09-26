#!/bin/python
import csv
import StringIO
from math import *
from scipy.signal import butter, filtfilt

class CSVData(object):
    def __init__(self, filename = "motor.txt"):
        self.data = list()

        #open file and get string data of file
        with open(filename) as f:
            buf = f.read()

        # transform csv format string
        buf = buf.replace(':', ',')
        buf = buf.replace(';', ',')
        buf = buf.replace('R', '1')
        buf = buf.replace('L', '0')

        # transform string to file object
        fbuf = StringIO.StringIO(buf)
        self.data = list(csv.reader(fbuf, quoting=csv.QUOTE_NONNUMERIC))

    def getElement(self, x, y):
        return self.data[x][y]

class Motor(object):

    def __init__(self):
        self.dat = CSVData()

        #list for data
        #Format: time[s] velocity[m/s] torque[N m] power[W]
        self.left_front = [[],[],[],[]]
        self.right_front = [[],[],[],[]]
        self.left_rear = [[],[],[],[]]
        self.right_rear = [[],[],[],[]]


        self.Rfirst = float()
        self.Lfirst = float()

        for i in self.dat.data:
            if i[0] == 0:
                """
                Calculate left side wheels
                """
                if self.Rfirst == 0.0:
                    self.Rfirst = i[3] + i[4] * pow(10, -6)
                time = i[3] + i[4] * pow(10, -6) - self.Rfirst
                self.left_front[0].append(time)
                self.left_rear[0].append(time)

                """
                calculate wheel speed[m/s]
                v = (diameter of wheel[mm]) * pow(10, -3) * pi * i[rev/min] / 60 / (Reduction ratio)
                """
                front_angular_velocity = 2 * pi * i[7] / 60
                front_speed = 250 * pow(10, -3) * pi * i[7] / 60 / 690
                rear_angular_velocity = 2 * pi * i[8] / 60
                rear_speed = 250 * pow(10, -3) * pi * i[8] / 60 / 690
                self.left_front[1].append(front_speed)
                self.left_rear[1].append(rear_speed)

                front_torque = i[9] * pow(10, -3)
                rear_torque = i[10] * pow(10, -3)
                self.left_front[2].append(front_torque)
                self.left_rear[2].append(front_torque)

                """
                Calculate Power
                """
                self.left_front[3].append(front_torque * front_angular_velocity)
                self.left_rear[3].append(rear_torque * rear_angular_velocity)

            else:
                """
                Calculate right side wheels
                """
                if self.Lfirst == 0.0:
                    self.Lfirst = i[3] + i[4] * pow(10, -6)
                time = i[3] + i[4] * pow(10, -6) - self.Lfirst
                self.right_front[0].append(time)
                self.right_rear[0].append(time)

                front_angular_velocity = 2 * pi * i[7] / 60
                front_speed = 250 * pow(10, -3) * pi * i[7] / 60 / 690
                rear_angular_velocity = 2 * pi * i[8] / 60
                rear_speed = 250 * pow(10, -3) * pi * i[8] / 60 / 690
                self.right_front[1].append(front_speed)
                self.right_rear[1].append(rear_speed)

                front_torque = i[9] * pow(10, -3)
                rear_torque = i[10] * pow(10, -3)
                self.right_front[2].append(front_torque)
                self.right_rear[2].append(rear_torque)

                """
                Calculate Power
                """
                self.right_front[3].append(front_torque * front_angular_velocity)
                self.right_rear[3].append(rear_torque * rear_angular_velocity)

        num, den = butter(2, 0.1, 'low')

        buff = filtfilt(num, den, self.left_front[1])
        self.left_front[1] = buff
        buff = filtfilt(num, den, self.left_rear[1])
        self.left_rear[1] = buff
        buff = filtfilt(num, den, self.right_front[1])
        self.right_front[1] = buff
        buff = filtfilt(num, den, self.right_rear[1])
        self.right_rear[1] = buff

        buff = filtfilt(num, den, self.left_front[2])
        self.left_front[2] = buff
        buff = filtfilt(num, den, self.left_rear[2])
        self.left_rear[2] = buff
        buff = filtfilt(num, den, self.right_front[2])
        self.right_front[2] = buff
        buff = filtfilt(num, den, self.right_rear[2])
        self.right_rear[2] = buff

        buff = filtfilt(num, den, self.left_front[3])
        self.left_front[3] = buff
        buff = filtfilt(num, den, self.left_rear[3])
        self.left_rear[3] = buff
        buff = filtfilt(num, den, self.right_front[3])
        self.right_front[3] = buff
        buff = filtfilt(num, den, self.right_rear[3])
        self.right_rear[3] = buff


if __name__ == '__main__':
    import sys

    motor = Motor()

    buf = float(0)

    for i in (motor.right_front, motor.right_rear, motor.left_front, motor.left_rear):
        for j in xrange(len(i[0])):
            if j == 0: dt = 0.0
            else: dt = i[0][j] - i[0][j-1]
            buf = buf + i[1][j] * dt

    print buf / 4

