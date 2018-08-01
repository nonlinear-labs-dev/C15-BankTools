#!/usr/local/bin/python
# coding=UTF8
import sys
import os
import NonlinearLabsBankTools

#Methode welche aus dem aktuellen Working-directory alle .xml Dateien sammelt
#und filenamen als liste zurückgibt
def getAllXML():
    ret = list()
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".xml"):
            ret.append(filename)
    return ret

#Codebeispiele um alle Keys, und entsprechende Werte anzuzeigen
#Soll nützlich sein um eigenen Usercode programmieren zu können ohne ins XML
#schauen zu müssen
def printAllValues(object, keysOnly):
    ret = list()
    for key in object.getKeys():
        if keysOnly == False:
            ret.append("%s, %s\n" % (key, object.getNodeValue(key)))
        else:
            ret.append("%s\n" % (key))
    return ret

def parseFull(filename):
    ret = list()
    parser = NonlinearLabsBankTools.NLParser(filename)
    for bank in parser.getBanks():
        ret.append("-----Bank------\n")
        ret += printAllValues(bank, False)
        for preset in bank.getPresets():
            ret.append("-----Preset-----\n")
            ret += printAllValues(preset, False)
            #for parameter in preset.getParameters():
            #    ret.append("------Parameter-----\n")
            #    ret += printAllValues(parameter, False)
    return ret
#ENDE Codebeispiel

#Bank -> Liste<Preset> -> Liste<Parameter>
#Jedes Objekt enthaelt eine Map aus XML tag <-> Inhalt
#Achtung: Untertags im <attributes> Knoten sind mit ihrem 'name' attribute addressierbar

def parseAsCSV(filename):
    lines = list()
    parser = NonlinearLabsBankTools.NLParser(filename)                          # Startet den Lesevorgang, bietet eingelesene Bänke mit 'getBanks()' an
    for bank in parser.getBanks():                                              #Schleife über alle Bänke des eingelesenen XML's
        numPresets = 0
        #print("%s" % (bank.getNodeValue("Date of Import File")))               #BSP für das Auslesen eines Attributes
        for preset in bank.getPresets():                                        #Schleife über alle Presets der aktuellen Bank
            numPresets += 1
            #Formatierte Ausgabe der für den User interessanten Daten           #HIER daten die ausgegeben werden sollen auswählen und definieren wie diese formatiert werden sollen!
            lines.append("%i,%s,%s,%s,%s,\n" % (numPresets,                     #%i - Integer, %s - String
            preset.getNodeValue("name"),
            preset.getNodeValue("uuid"),
            preset.getNodeValue("color"),
            preset.getNodeValue("comment")))
    return lines

#Hilfsmethode zum schreiben von Dateien
def writeListOfLinesToFile(file, lines):
    file = open(file, "w")
    for line in lines:
        file.write(line)
    file.close()

def printLines(lines):
    for line in lines:
        line.rstrip('\n')
        line.rstrip('\n')
        print(line)

#Programm runner!
#Shell Ausgabe und parsen der Argumente
def printHelp():
    print("USAGE:")
    print("./script <FILENAME>")
    print(" --csv | -c")
    print(" specifies format to be comma seperated")
    print(" (if not defined - all keys that were found will be printed)")
    print(" --print | -p")
    print(" prints result to console")
    print(" --out | -o")
    print(" writes result to <INPUTFILE>.csv")
    print(" --all | -a")
    print(" ignores inputfile and parses all .xml files in current directory")

def handleFile(file, csvFlag, printFlag, outFlag):
    if csvFlag:
        csv = parseAsCSV(file)
        if printFlag:
            printLines(csv)
        else:
            writeListOfLinesToFile(file + ".csv", csv)
    else:
        content = parseFull(file)
        if printFlag:
            printLines(content)
        else:
            writeListOfLinesToFile(file + ".tags", content)

def main():
    argC = len(sys.argv)
    if argC == 1:
        printHelp()
    else:
        filename = sys.argv[1]
        csvFlag = "--csv" in sys.argv or "-c" in sys.argv
        printFlag = "--print" in sys.argv or "-p" in sys.argv
        outFlag = "--out" in sys.argv or "-p" in sys.argv and not printFlag
        allFiles = "--all" in sys.argv or "-a" in sys.argv

        if allFiles:
            for file in getAllXML():
                handleFile(file, csvFlag, printFlag, outFlag)
        else:
            handleFile(filename, csvFlag, printFlag, outFlag)


main()                                                                          #Programmeinstieg!
