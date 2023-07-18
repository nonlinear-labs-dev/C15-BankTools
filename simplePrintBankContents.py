#!/usr/bin/python3
# coding=UTF8
import sys
import lib.NonlinearLabsBankTools as NonlinearLabsBankTools

def prettyPrintBank(filename):
    presets = list()
    bankName = ""
    parser = NonlinearLabsBankTools.NLParser(filename)
    bankNum = 0
    numPresets = 0
    for bank in parser.getBanks():
        bankNum += 1
        bankName = bank.getNodeValue("name")
        
        presetNum = 0
        for preset in bank.getPresets():
            presetNum += 1
            numPresets += 1
            presets.append('%i\t %s' % (presetNum, preset.getNodeValue("name")))

    print(str(bankName) + " - " + str(numPresets) + " presets")
    for p in presets:
        print(p)
    

if len(sys.argv) < 2:
    print("use: ./prettyPrintBank.py <BANK>.xml")
    exit(1)

inFile = sys.argv[1]
prettyPrintBank(inFile)
