#!/usr/bin/python3
# coding=UTF8
import sys
import NonlinearLabsBankTools

def parseAsCSV(filename):
    lines = list()
    parser = NonlinearLabsBankTools.NLParser(filename)                          #Startet den Lesevorgang, bietet eingelesene Bänke mit 'getBanks()' an
    for bank in parser.getBanks():                                              #Schleife über alle Bänke des eingelesenen XML's
        numPresets = 0
        for preset in bank.getPresets():                                        #Schleife über alle Presets der aktuellen Bank
            numPresets += 1
            mc1 = ""
            mc2 = ""
            mc3 = ""
            mc4 = ""
            mc5 = ""
            mc6 = ""


            mcAssignments = [[], [], [], [], [], []]

            for param in preset.getParameters():
                modSrc = param.getNodeValue("modSrc")
                if modSrc != "None":
                    mcAssignments[int(modSrc) - 1].append(param.getNodeValue("id"))                    

            for param in preset.getParameters():
                if param.getNodeValue("id") == "243":
                    mc1 = param.getNodeValue("givenName")
                if param.getNodeValue("id") == "244":
                    mc2 = param.getNodeValue("givenName")
                if param.getNodeValue("id") == "245":
                    mc3 = param.getNodeValue("givenName")
                if param.getNodeValue("id") == "246":
                    mc4 = param.getNodeValue("givenName")
                if param.getNodeValue("id") == "369":
                    mc5 = param.getNodeValue("givenName")
                if param.getNodeValue("id") == "371":
                    mc6 = param.getNodeValue("givenName")
                
                                                                                            #Formatierte Ausgabe der für den User relevanten Daten

            lines.append("%i,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (numPresets,                     #%i - Integer, %s - String
            preset.getNodeValue("name"),
            preset.getNodeValue("uuid"),
            preset.getNodeValue("color"),
            preset.getNodeValue("Comment"),
            mc1, mc2, mc3, mc4, mc5, mc6))
    return lines
#end parseAsCSV

def writeListOfLinesToFile(file, lines):
    file = open(file, "w")
    for line in lines:
        file.write(line)
    file.close()
#end writeListOfLinesToFile

                                                                                #Programmeinstieg
#main
if len(sys.argv) < 2:
    print("use: ./bankToCsv <BANK>.xml <OUT>.csv")
    exit(1)

inFile = sys.argv[1]
outFile = inFile + ".csv"

if len(sys.argv) >= 3:
    outFile = sys.argv[2]

lines = parseAsCSV(inFile)
writeListOfLinesToFile(outFile, lines)
#endmain
