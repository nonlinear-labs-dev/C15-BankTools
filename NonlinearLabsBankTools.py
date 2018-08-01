from xml.sax import make_parser, handler
import sys
import os

class Preset():
    def __init__(self):
        self.attributes = dict()

    def setNodeValue(self, key, value):
        self.attributes[key] = value

    def getNodeValue(self, key):
        if key in self.attributes:
            return self.attributes[key]
        if "meta"+key in self.attributes:
            return self.attributes["meta"+key]
        return "None"

class Bank():
    def __init__(self):
        self.attributes = dict()
        self.presets = list()

    def setNodeValue(self, key, value):
        self.attributes[key] = value

    def addPreset(self, preset):
        self.presets.append(preset)

    def getPresets(self):
        return self.presets

    def getNodeValue(self, key):
        if key in self.attributes:
            return self.attributes[key]
        if "meta"+key in self.attributes:
            return self.attributes["meta"+key]
        return "None"

class BankHandler(handler.ContentHandler):
        def __init__(self):
            self.banks = list()
            self.currentContent = ""
            self.currentPreset = Preset()
            self.currentBank = Bank()
            self.currentKey = ""
            self.activeObject = None
            self.currentAttribute = ""

        def startElement(self, name, attrs):
            self.currentKey = name
            self.currentContent = ""

            if name == "bank":
                self.currentBank = Bank()
                self.activeObject = self.currentBank
            elif name == "preset":
                self.currentPreset = Preset()
                self.activeObject = self.currentPreset
            elif name == "attribute":
                self.currentAttribute = attrs["name"]

        def characters(self, content):
            self.currentContent += content.strip()

        def endElement(self, name):
            if name == "bank":
                self.banks.append(self.currentBank)
            elif name == "preset":
                self.currentBank.addPreset(self.currentPreset)
            else:
                if name != "attribute":
                    self.activeObject.setNodeValue(name, self.currentContent)
                else:
                    self.activeObject.setNodeValue("meta"+self.currentAttribute, self.currentContent)

        def getBanks(self):
            return self.banks

class NLParser():
    def __init__(self, filename):
        self.filename = filename
        self.parser = make_parser()
        self.b = BankHandler()
        self.parser.setContentHandler(self.b)
        self.parser.parse(filename)

    def getBanks(self):
        return self.b.getBanks()
