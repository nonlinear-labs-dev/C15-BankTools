import sys
import os
import NonlinearLabsBankTools

def parseAll():
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".xml"):
            parseAsCSV(filename)
            print("\n")
            continue
        else:
            continue

def parseAsCSV(filename):
    parser = NonlinearLabsBankTools.NLParser(filename)

    for bank in parser.getBanks():
        numPresets = 0
        for preset in bank.getPresets():
            numPresets += 1
            print("%i,%s,%s,%s" % (numPresets, preset.getNodeValue("name"), preset.getNodeValue("color"), preset.getNodeValue("comment")))

if len(sys.argv) >= 2:
    parseAsCSV(sys.argv[1])
else:
    print("Usage: ./parseBank <FILENAME>")
