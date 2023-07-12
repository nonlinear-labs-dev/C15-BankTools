#!/usr/bin/python3
# coding=UTF8
import sys
import NonlinearLabsBankTools
import glob

def banksDiffer(bank1, bank2) -> bool:
    
    banks1 = bank1.getBanks()
    banks2 = bank2.getBanks()


    if len(banks1) != 1 or len(banks2) != 1:
        print(f"banks have different sizes: {len(banks1)} != {len(banks2)}")
        return True

    banks1 = banks1[0]
    banks2 = banks2[0]

    for preset in banks1.getPresets():
        otherPreset = banks2.findPreset(preset.getName())

        if otherPreset == None:
            print(f"{banks1.getName()}-{preset.getName()} not found in {banks2.getName()}")
            return True

        for parameter in preset.getParameters():
            otherParameter = otherPreset.findParameter(parameter.getID())
            if otherParameter == None:
                return True
            
            if otherParameter.getNodeValue("value") != parameter.getNodeValue("value"):
                print(f"{preset.getName()}-{parameter.getID()}: {parameter.getNodeValue('value')} != {otherParameter.getNodeValue('value')}")
                return True
            
            if otherParameter.getNodeValue("pedalMode") != parameter.getNodeValue("pedalMode"):
                print(f"{preset.getName()}-{parameter.getID()}: {parameter.getNodeValue('pedalMode')} != {otherParameter.getNodeValue('pedalMode')}")
                return True
            
            if otherParameter.getNodeValue("modSrc") != parameter.getNodeValue("modSrc"):
                print(f"{preset.getName()}-{parameter.getID()}: {parameter.getNodeValue('modSrc')} != {otherParameter.getNodeValue('modSrc')}")
                return True
            
            if otherParameter.getNodeValue("modAmount") != parameter.getNodeValue("modAmount"):
                print(f"{preset.getName()}-{parameter.getID()}: {parameter.getNodeValue('modAmount')} != {otherParameter.getNodeValue('modAmount')}")
                return True

    return False

if len(sys.argv) < 2:
    print("use: ./doBanksDiffer.py bank1 bank2")
    exit(1)

bank1 = sys.argv[1]
bank2 = sys.argv[2]

b1 = NonlinearLabsBankTools.NLParser(bank1)
b2 = NonlinearLabsBankTools.NLParser(bank2)

print(f"Banks differ: {banksDiffer(b1, b2)}")