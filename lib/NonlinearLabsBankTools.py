from xml.sax import make_parser, handler
import sys
import os

class CSVTools():
    @staticmethod
    def writeListOfLinesToFile(file, lines):
        file = open(file, "w")
        for line in lines:
            file.write(line)
        file.close()

    @staticmethod
    def getCSVHeader():
     return "NR,Name,UUID,Color,Comment,MC A Name,MC A Target,MC B Name,MC B Target,MC C Name,MC C Target,MC D Name,MC D Target,MC E Name,MC E Target,MC F Name,MC F Target\n"

    @staticmethod
    def toCSV(preset, numPresets):
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

        return ("%i,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % 
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

class Parameter():
    def __init__(self):
        self.attributes = dict()

    def setNodeValue(self, key, value):
        self.attributes[key] = value

    def getNodeValue(self, key):
        if key in self.attributes:
            return self.attributes[key]
        elif "meta"+key in self.attributes:
            return self.attributes["meta"+key]
        return "None"

    def getKeys(self):
        return list(self.attributes.keys())
    
    def getID(self):
        return self.getNodeValue("id")

class Preset():
    def __init__(self):
        self.attributes = dict()
        self.parameters = list()

    def getParameters(self):
        return self.parameters

    def getParameter(self, id):
        for i in self.parameters:
            if i.getNodeValue("id") == id:
                return i
        return None

    def getName(self):
        return self.getNodeValue("name")

    def addParameter(self, parameter):
        self.parameters.append(parameter)

    def findParameter(self, id):
        for i in self.parameters:
            if i.getNodeValue("id") == id:
                return i
        return None
    
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
    
    def findPreset(self, name):
        for i in self.presets:
            if i.getName() == name:
                return i
        return None

    def getName(self):
        return self.getNodeValue("name")

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
