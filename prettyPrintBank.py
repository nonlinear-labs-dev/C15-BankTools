#!/usr/bin/python3
# coding=UTF8
import sys
import NonlinearLabsBankTools

def prettyPrintBank(filename):
    parser = NonlinearLabsBankTools.NLParser(filename)
    bankNum = 0
    for bank in parser.getBanks():
        bankNum += 1
        print('\t%i - %s' % (bankNum, bank.getNodeValue("name")))
        print("-"*len(bank.getNodeValue("name"))*(3))
        presetNum = 0
        for preset in bank.getPresets():
            presetNum += 1
            print('%s\t %i\t %s' % (preset.getNodeValue("color"), presetNum, preset.getNodeValue("name")))

if len(sys.argv) < 2:
    print("use: ./prettyPrintBank.py <BANK>.xml")
    exit(1)

inFile = sys.argv[1]
prettyPrintBank(inFile)
