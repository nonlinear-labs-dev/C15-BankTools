#!/usr/bin/python
# coding=UTF8
import sys
import os
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
            mc1 = ""
            mc2 = ""
            mc3 = ""
            mc4 = ""
            for param in preset.getParameters():
                if param.getNodeValue("id") == "243":
                    mc1 = param.getNodeValue("givenName")
                if param.getNodeValue("id") == "244":
                    mc2 = param.getNodeValue("givenName")
                if param.getNodeValue("id") == "245":
                    mc3 = param.getNodeValue("givenName")
                if param.getNodeValue("id") == "246":
                    mc4 = param.getNodeValue("givenName")

            lines.append("%i,%s,%s,%s,%s,%s,%s,%s,%s,\n" % (numPresets,
            preset.getNodeValue("name"),
            preset.getNodeValue("uuid"),
            preset.getNodeValue("color"),
            preset.getNodeValue("comment"),
            mc1, mc2, mc3, mc4))
    return lines

def writeListOfLinesToFile(file, lines):
    file = open(file, "w")
    for line in lines:
        file.write(line)
    file.close()

if len(sys.argv) > 1:
    print("use: ./allBanksToCSV.py")
    exit(1)
for inFile in getAllXML():
    outFile = inFile + ".csv"
    lines = parseAsCSV(inFile)
    writeListOfLinesToFile(outFile, lines)
