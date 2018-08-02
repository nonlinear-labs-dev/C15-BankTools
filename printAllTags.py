#!/usr/bin/python
# coding=UTF8
import sys
import NonlinearLabsBankTools

def printAllTags(filename):
    parser = NonlinearLabsBankTools.NLParser(filename)
    for bank in parser.getBanks():
        print("Bank Tags:")
        print('%s' % ', '.join(map(str, bank.getKeys())))
        for preset in bank.getPresets():
            print("Preset Tags:")
            print('%s' % ', '.join(map(str, preset.getKeys())))
            break
        break
#end printAllTags

#main
if len(sys.argv) < 2:
    print("use: ./printAllTags.py <BANK>.xml")
    exit(1)

inFile = sys.argv[1]
printAllTags(inFile)
#endmain
