from xml.sax import make_parser, handler
import sys
import os

class Preset():
    def __init__(self):
        self.name = ""
        self.uuid = ""

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def setUuid(self, uuid):
        self.uuid = uuid

    def getUuid(self):
        return self.uuid

class Bank():
    def __init__(self):
        self.presets = list()
        self.name = ""
        self.uuid = ""
        self.exportDate = ""
        self.comment = ""

    def setName(self, name):
        self.name = name

    def addPreset(self, preset):
        self.presets.append(preset)

    def getName(self):
        return self.name

    def getPresets(self):
        return self.presets

    def setUuid(self, uuid):
        self.uuid = uuid

    def getUuid(self):
        return self.uuid

    def setExportDate(self, date):
        self.exportDate = date

    def getExportDate(self):
        return self.exportDate

    def setComment(self, com):
        self.comment = com

    def getComment(self):
        return self.comment

class BankHandler(handler.ContentHandler):
        def __init__(self):
            self.banks = list()
            self.current_content = ""
            self.currentPreset = Preset()
            self.currentBank = Bank()
            self.inPresetTag = False
            self.inBankComment = False
            self.inExportDate = False

        def startElement(self, name, attrs):
            self.inExportDate = False
            self.inBankComment = False
            self.current_content = ""
            if name == "bank":
                self.currentBank = Bank()
            elif name == "preset":
                self.inPresetTag = True
                self.currentPreset = Preset()
            elif name == "attribute":
                if attrs["name"] == "Comment":
                    self.inBankComment = True
                elif attrs["name"] == "Date of Export File":
                    self.inExportDate = True

        def characters(self, content):
            self.current_content += content.strip()

        def endElement(self, name):
            if name == "bank":
                self.banks.append(self.currentBank)
            elif name == "preset":
                self.currentBank.addPreset(self.currentPreset)
                self.inPresetTag = False
            elif name == "name":
                if self.inPresetTag == True:
                    self.currentPreset.setName(self.current_content)
                else:
                    self.currentBank.setName(self.current_content)
            elif name == "uuid":
                if self.inPresetTag == True:
                    self.currentPreset.setUuid(self.current_content)
                else:
                    self.currentBank.setUuid(self.current_content)
            elif name == "attribute":
                if self.inBankComment == True:
                    self.inBankComment = False
                    self.currentBank.setComment(self.current_content)
                elif self.inExportDate == True:
                    self.inExportDate = False
                    self.currentBank.setExportDate(self.current_content)

        def getBanks(self):
            return self.banks

def printHelp():
    print("NL - C15 BankHandler")
    print("usage:")
    print("     --all")
    print("         attempts to parse all .xml files in current directory")
    print("     help")
    print("         prints this")
    print("     <filename>")
    print("         parses specified file")

def parseAll():
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".xml"):
            parseOne(filename)
            print("\n")
            continue
        else:
            continue

def parseOne(filename):
    print("FILE: %s:" % (filename))

    parser = make_parser()
    b = BankHandler()
    parser.setContentHandler(b)
    parser.parse(filename)

    for bank in b.getBanks():
        print("%-40s - %s:" % (bank.getName(), bank.getUuid()))
        print("Preset count: %i\nComment: %s\nExport Date: %s" % (len(bank.getPresets()), bank.getComment(), bank.getExportDate()))
        for preset in bank.getPresets():
            print("\t%-40s - %s" % (preset.getName(), preset.getUuid()))


if len(sys.argv) != 2:
    printHelp()
    exit(-1)
elif sys.argv[1] == "help":
    printHelp()
elif sys.argv[1] == "--all":
    parseAll()
else:
    parseOne(sys.argv[1])
