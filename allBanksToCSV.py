#!/usr/bin/python
# coding=UTF8
import sys
import NonlinearLabsBankTools

def getAllXML():
    ret = list()
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".xml"):
            ret.append(filename)
    return ret

def parseAsCSV(filename):
    lines = list()
    parser = NonlinearLabsBankTools.NLParser(filename)
    for bank in parser.getBanks():
        numPresets = 0
        for preset in bank.getPresets():
            numPresets += 1

            lines.append("%i,%s,%s,%s,%s,\n" % (numPresets,
            preset.getNodeValue("name"),
            preset.getNodeValue("uuid"),
            preset.getNodeValue("color"),
            preset.getNodeValue("comment")))
    return lines

def writeListOfLinesToFile(file, lines):
    file = open(file, "w")
    for line in lines:
        file.write(line)
    file.close()

if len(sys.argv) > 1:
    print("use: ./allBanksToCSV.py")
    exit(1)
for infile in getAllXML():
    outFile = inFile + ".csv"
    lines = parseAsCSV(inFile)
    writeListOfLinesToFile(outFile, lines)
