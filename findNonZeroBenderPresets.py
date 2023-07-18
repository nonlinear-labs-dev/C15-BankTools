#!/usr/bin/python3
# coding=UTF8
import sys
import lib.NonlinearLabsBankTools as NonlinearLabsBankTools
import glob

def findNonZeroPresetsInBankFile(filename):
    parser = NonlinearLabsBankTools.NLParser(filename)
    for bank in parser.getBanks():
        for preset in bank.getPresets():

            newBender = preset.getParameter("Global-274")
            oldBender = preset.getParameter("274")
            
            bender = None

            if newBender == None and oldBender != None:
                bender = oldBender
            
            if oldBender == None and newBender != None:
                bender = newBender

            if oldBender != None and newBender != None:
                print(f"{bank.getName()}-{preset.getName()} ambiguous bender id! found both new and old id in same preset!")
                continue

            benderValue = bender.getNodeValue("value")
            if float(benderValue) >= 0.1 or float(benderValue) <= -0.1:
                print(f"{bank.getName()}-{preset.getName()} has bender value: {benderValue}")
        break

if len(sys.argv) < 2:
    print("use: ./findNonZeroBenderPresets.py <directory>")
    exit(1)

inFile = sys.argv[1]

files = glob.glob(f'{inFile}/**/*.xml', recursive=True)
for f in files:
    findNonZeroPresetsInBankFile(f)