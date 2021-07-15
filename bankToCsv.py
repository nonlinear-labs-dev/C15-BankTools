#!/usr/bin/python3
# coding=UTF8
import sys
import NonlinearLabsBankTools

def parseAsCSV(filename):
    lines = list()
    lines.append("NR,Name,UUID,Color,Comment,MC A Name,MC A Target,MC B Name,MC B Target,MC C Name,MC C Target,MC D Name,MC D Target,MC E Name,MC E Target,MC F Name,MC F Target\n")
    
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
                if modSrc != "None" and int(modSrc) != 0:
                    mcAssignments[int(modSrc) - 1].append(param.getNodeValue("id"))                    

            for param in preset.getParameters():
                idSplit = param.getNodeValue("id").split("-")
                parameterNumber = idSplit[1]

                if parameterNumber == "243":
                    mc1 = param.getNodeValue("givenName")
                    if mc1 == "None" or mc1 == "":
                        mc1 = "MC A"
                elif parameterNumber == "244":
                    mc2 = param.getNodeValue("givenName")
                    if mc2 == "None" or mc2 == "":
                        mc2 = "MC B"
                elif parameterNumber == "245":
                    mc3 = param.getNodeValue("givenName")
                    if mc3 == "None" or mc3 == "":
                        mc3 = "MC C"
                elif parameterNumber == "246":
                    mc4 = param.getNodeValue("givenName")
                    if mc4 == "None" or mc4 == "":
                        mc4 = "MC D"
                elif parameterNumber == "369":
                    mc5 = param.getNodeValue("givenName")
                    if mc5 == "None" or mc5 == "":
                        mc5 = "MC E"
                elif parameterNumber == "371":
                    mc6 = param.getNodeValue("givenName")
                    if mc6 == "None" or mc6 == "":
                        mc6 = "MC F"
                
            mc1Targets = ""
            mc2Targets = ""
            mc3Targets = ""
            mc4Targets = ""
            mc5Targets = ""
            mc6Targets = ""

            index = 0
            for assignments in mcAssignments:
                if assignments:
                    string = ' '.join(str(e) for e in assignments)
                    if index == 0:
                        mc1Targets = string
                    elif index == 1:
                        mc2Targets = string
                    elif index == 2:
                        mc3Targets = string
                    elif index == 3:
                        mc4Targets = string
                    elif index == 4:
                        mc5Targets = string
                    elif index == 5:
                        mc6Targets = string
                index += 1
                                                                                            

            rawComment = preset.getNodeValue("Comment")
            for c in [',', ';']:
                rawComment = rawComment.replace(c, ' ')
            cleanComment = rawComment

            #Formatierte Ausgabe der für den User relevanten Daten
            #%i - Integer, %s - String

            lines.append("%i,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % 
                (
                    numPresets,
                    preset.getNodeValue("name"),
                    preset.getNodeValue("uuid"),
                    preset.getNodeValue("color"),
                    cleanComment,
                    mc1, mc1Targets, 
                    mc2, mc2Targets, 
                    mc3, mc3Targets, 
                    mc4, mc4Targets, 
                    mc5, mc5Targets, 
                    mc6, mc6Targets
                )
            )
    return lines
#end parseAsCSV

def writeListOfLinesToFile(file, lines):
    file = open(file, "w")
    for line in lines:
        file.write(line)
    file.close()


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