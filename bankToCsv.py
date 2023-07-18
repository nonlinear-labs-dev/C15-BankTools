#!/usr/bin/python3
# coding=UTF8
import sys
import lib.NonlinearLabsBankTools as NonlinearLabsBankTools

def parseAsCSV(filename):
    lines = list()
    lines.append(NonlinearLabsBankTools.CSVTools.getCSVHeader())
    
    parser = NonlinearLabsBankTools.NLParser(filename)                          #Startet den Lesevorgang, bietet eingelesene Bänke mit 'getBanks()' an
    for bank in parser.getBanks():                                              #Schleife über alle Bänke des eingelesenen XML's
        numPresets = 0
        for preset in bank.getPresets():                                        #Schleife über alle Presets der aktuellen Bank
            numPresets += 1
            lines.append(NonlinearLabsBankTools.CSVTools.toCSV(preset, numPresets))
    return lines

if len(sys.argv) < 2:
    print("use: ./bankToCsv <BANK>.xml <OUT>.csv")
    exit(1)

inFile = sys.argv[1]
outFile = inFile + ".csv"

if len(sys.argv) >= 3:
    outFile = sys.argv[2]

lines = parseAsCSV(inFile)
NonlinearLabsBankTools.CSVTools.writeListOfLinesToFile(outFile, lines)