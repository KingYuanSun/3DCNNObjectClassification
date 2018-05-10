#!/usr/bin/env python

import csv
import os
import inspect

CleaningProcess = 'rm -f *.pcd data.csv ObjectLiDAR.npz'
import subprocess as sub
output = sub.check_output([CleaningProcess], shell=True)
print output


# CSV to PCD types  transformation
extensionCSV = '.csv'

myList = ["ObjectLiDAR/"]

for root, dirs, files in os.walk(myList[0]):
    for name in files:

        if os.path.splitext(name)[-1] == extensionCSV:
            namelist = name.split('.')

            InputFileName = root+'/' + name
            OutputFileName = root + '/' + namelist[0]+'.'+namelist[1]+'.pcd'

            print root

            print InputFileName
            print OutputFileName

            f = open(InputFileName)
            # csvdata = ["# .PCD v.7 - Point Cloud Data file format"]
            firstlinePre = True
            EffectiveRowCount = 0
            for row in csv.reader(f):

                EffectiveRowCount = EffectiveRowCount+1

            print(EffectiveRowCount)
            f.close()

            with open(OutputFileName, "w") as myfile:

                writer = csv.writer(myfile)
                # writer.writerow(('Title 1', 'Title 2', 'Title 3'))
                writer.writerow(["# .PCD v.7 - Point Cloud Data file format"])
                writer.writerow(["VERSION .7"])
                writer.writerow(["FIELDS x y z"])
                writer.writerow(["SIZE 4 4 4"])
                writer.writerow(["TYPE F F F"])
                writer.writerow(["COUNT 1 1 1"])
                writer.writerow(['WIDTH ' + str(EffectiveRowCount)])
                writer.writerow(["HEIGHT 1"])
                writer.writerow(["VIEWPOINT 0 0 0 1 0 0 0"])
                writer.writerow(['POINTS ' + str(EffectiveRowCount)])
                writer.writerow(["DATA ascii"])

            f = open(InputFileName)

            print("I am here!")
            for row in csv.reader(f):
                print(row)
                with open(OutputFileName, "a") as myfile:
                    writer = csv.writer(myfile, delimiter=" ")
                    writer.writerow(row[3:6])




# PCD to binvox transformation
VoxNumbers = 32
extensionPCD = '.pcd'

myList = ["ObjectLiDAR/"]

for root, dirs, files in os.walk(myList[0]):
    for name in files:

        if os.path.splitext(name)[-1] == extensionPCD:
            namelist = name.split('.')

            InputFileName = root+'/' + name
            OutputFileName = root + '/' + namelist[0]+'.'+namelist[1]+'.binvox'

            CurrentProcessedFileName = OutputFileName
            CMDString = './pcd2binvox/build/pcd2binvox -d '+ str(VoxNumbers) + ' ' + InputFileName + ' ' + OutputFileName
            print CMDString
            import subprocess as sub

            output = sub.check_output([CMDString], shell=True)
            print output
            print CMDString
