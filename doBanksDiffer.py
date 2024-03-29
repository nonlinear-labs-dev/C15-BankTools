#!/usr/bin/python3
# coding=UTF8
import sys
import lib.NonlinearLabsBankTools as NonlinearLabsBankTools
import lib.ids

def readable(id: str) -> str:
    if id.find("-") != -1:
        number = id.split("-")[1]
        return str(lib.ids.ParameterNumber(int(number)))
    else:
        return str(lib.ids.ParameterNumber(int(id)))

def banksDiffer(bank1: NonlinearLabsBankTools.NLParser, bank2: NonlinearLabsBankTools.NLParser, verbose: bool = False) -> bool:
    hadDiff = False

    banks1 = bank1.getBanks()
    banks2 = bank2.getBanks()

    if len(banks1) != 1 or len(banks2) != 1:
        if verbose:
            print(f"banks have different sizes: {len(banks1)} != {len(banks2)}")
        hadDiff |= True
        return True

    banks1 = banks1[0]
    banks2 = banks2[0]

    if banks1.getVersion() != banks2.getVersion():
        if verbose:
            print(f"banks have different versions: {banks1.getVersion()} != {banks2.getVersion()}")
        hadDiff |= True
        
    print(f"banks1: {banks1.getName()}")
    print(f"banks2: {banks2.getName()}")

    for preset in banks1.getPresets():
        presetHadDiff = False
    
        otherPreset = banks2.findPreset(preset.getName())

        if otherPreset == None:
            if verbose:
                print(f"{banks1.getName()}-{preset.getName()} not found in {banks2.getName()}")
            hadDiff |= True
            presetHadDiff |= True
            continue
            
        for parameter in preset.getParameters():
            otherParameter = otherPreset.findParameter(parameter.getID())

            if otherParameter == None:
                if verbose:
                    print(f"{banks1.getName()}: {preset.getName()} Parameter with ID: {parameter.getID()} not found in {otherPreset.getName()}")
                hadDiff |= True
                presetHadDiff |= True
                continue

            doKeyCheck = False

            if doKeyCheck:
                myKeyCount = len(parameter.getKeys())
                otherKeyCount = len(otherParameter.getKeys())

                if myKeyCount != otherKeyCount:
                    if verbose:
                        print(f"{banks1.getName()}: {preset.getName()} Parameter-Keys for {parameter.getID()} differ: {myKeyCount} != {otherKeyCount}. This is most likely a redefinition of a parameter (Modulate/Unmodulateable).")
                    
                    myKeys = " ".join(parameter.getKeys())
                    otherKeys  = " ".join(otherParameter.getKeys())
                    
                    if verbose:
                        print(f"keys for parameter of the first argument: {myKeys}")
                        print(f"keys for parameter of the second argument: {otherKeys}")
                    
                    hadDiff |= True
                    presetHadDiff |= True
        
            myValue = parameter.getNodeValue("value")
            otherValue = otherParameter.getNodeValue("value")
            
            if myValue != otherValue:
                if verbose:
                    print(f"{preset.getName()}: {readable(parameter.getID())} Parameter-Value: {myValue} != {otherValue}")
                
                hadDiff |= True
                presetHadDiff |= True
        
            if otherParameter.getNodeValue("pedalMode") != parameter.getNodeValue("pedalMode"):
                if verbose:
                    print(f"{preset.getName()}: {parameter.getID()} Pedal-Mode: {parameter.getNodeValue('pedalMode')} != {otherParameter.getNodeValue('pedalMode')}")
                
                hadDiff |= True
                presetHadDiff |= True
        
            if otherParameter.getNodeValue("modSrc") != parameter.getNodeValue("modSrc"):
                if verbose:
                    print(f"{preset.getName()}: {parameter.getID()} mod-source: {parameter.getNodeValue('modSrc')} != {otherParameter.getNodeValue('modSrc')}")
                
                hadDiff |= True
                presetHadDiff |= True
        
            if otherParameter.getNodeValue("modAmount") != parameter.getNodeValue("modAmount"):
                if verbose:
                    print(f"{preset.getName()}: {parameter.getID()} modulation-amount: {parameter.getNodeValue('modAmount')} != {otherParameter.getNodeValue('modAmount')}")
                
                hadDiff |= True
                presetHadDiff |= True
        
        if presetHadDiff:
            print(f"{preset.getName()} has differences!")

    return hadDiff

if len(sys.argv) < 2:
    print("use: ./doBanksDiffer.py bank1 bank2")
    exit(1)


import os
verbose = os.environ.get('VERBOSE', False)

bank1 = sys.argv[1]
bank2 = sys.argv[2]

b1 = NonlinearLabsBankTools.NLParser(bank1)
b2 = NonlinearLabsBankTools.NLParser(bank2)

print(f"Banks differ: {banksDiffer(b1, b2, verbose)}")