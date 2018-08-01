from xml.sax import make_parser, handler
import sys
import os

class Parameter():
    def __init__(self):
        self.attributes = dict()

    def setNodeValue(self, key, value):
        self.attributes[key] = value

    def getNodeValue(self, key):
        if key in self.attributes:
            return self.attributes[key]
        return "None"

    def getKeys(self):
        return list(self.attributes.keys())

class Preset():
    def __init__(self):
        self.attributes = dict()
        self.parameters = list()

    def getParameters(self):
        return self.parameters

    def addParameter(self, parameter):
        self.parameters.append(parameter)

    def setNodeValue(self, key, value):
        self.attributes[key] = value

    def getNodeValue(self, key):
        if key in self.attributes:
            return self.attributes[key]
        if "meta"+key in self.attributes:
            return self.attributes["meta"+key]
        return "None"

    def getKeys(self):
        return list(self.attributes.keys())

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

    def getKeys(self):
        return list(self.attributes.keys())

class BankHandler(handler.ContentHandler):
        def __init__(self):
            self.banks = list()
            self.currentContent = ""
            self.currentPreset = Preset()
            self.currentBank = Bank()
            self.currentParameter = Parameter()
            self.activeObject = None
            self.currentAttribute = ""

        def startElement(self, name, attrs):
            self.currentContent = ""

            if name == "bank":
                self.currentBank = Bank()
                self.activeObject = self.currentBank
            elif name == "preset":
                self.currentPreset = Preset()
                self.activeObject = self.currentPreset
            elif name == "parameter":
                self.currentParameter = Parameter()
                self.activeObject = self.currentParameter
                self.currentParameter.setNodeValue("id", attrs["id"])
            elif name == "attribute":
                self.currentAttribute = attrs["name"]

        def characters(self, content):
            self.currentContent += content.strip()

        def endElement(self, name):
            if name == "bank":
                self.banks.append(self.currentBank)
            elif name == "preset":
                self.currentBank.addPreset(self.currentPreset)
            elif name == "parameter":
                self.currentPreset.addParameter(self.currentParameter)
            else:
                if name != "attribute":
                    self.activeObject.setNodeValue(name, self.currentContent)
                else:
                    self.activeObject.setNodeValue("meta"+self.currentAttribute, self.currentContent)

            self.currentContent = ""

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
