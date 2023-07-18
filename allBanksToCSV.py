#!/usr/bin/python3
# coding=UTF8
import sys
import os
import lib.NonlinearLabsBankTools as NonlinearLabsBankTools

def getAllXML():
    ret = list()
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".xml"):
            ret.append(filename)
    return ret

def parseAsCSV(filename):
    lines = list()
    parser = NonlinearLabsBankTools.NLParser(filename)
    lines.append(NonlinearLabsBankTools.CSVTools.getCSVHeader())

    for bank in parser.getBanks():
        numPresets = 0
        for preset in bank.getPresets():
            numPresets += 1
            lines.append(NonlinearLabsBankTools.CSVTools.toCSV(preset, numPresets))
    return lines

if len(sys.argv) > 1:
    print("use: ./allBanksToCSV.py")
    exit(1)

for inFile in getAllXML():
    outFile = inFile + ".csv"
    lines = parseAsCSV(inFile)
    NonlinearLabsBankTools.CSVTools.writeListOfLinesToFile(outFile, lines)
