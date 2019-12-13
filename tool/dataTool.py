

import json
import os

from data import requirement
from xml.dom.minidom import parse, parseString


def jsonFile2JsonDict(filePath):
    jsonDict = json.load(open(filePath, "r", encoding="utf-8"))
    return jsonDict


def jsonDict2Requirement(jsonDaict):
    req = requirement.Requirement()

    # read factors
    factors = jsonDaict["factors"]
    for factor in factors:
        req.addFactor(factor["name"], factor["level"])
    req.updateFactorsNumber()
    # req.showFactors()

    strength = jsonDaict["strength"]
    req.setStrength(strength["default"])
    varStrengths = strength["var_strengh"]
    for varStrength in varStrengths:
        req.addVarFactor(varStrength["factor"], varStrength["strength"])

    seeds = jsonDaict["seeds"]
    for seed in seeds:
        # print( seed )
        req.addSeedByFactorDict(seed)

    return req


def xmlFile2JsonDict(filePath):
    jsonDict = {}
    xml = None
    with open( filePath, "r", encoding="utf-8" ) as fin:
        xml = parseString(fin.read())
    rootNode = xml.documentElement

    # factors
    jsonDict["factors"] = []
    for factorNode in rootNode.getElementsByTagName("factor"):
        factor = {}
        # name, level, type
        factor["name"] = factorNode.getAttribute("name")
        factor["type"] = factorNode.getAttribute("type")
        factor["level"] = []

        for valueNode in factorNode.getElementsByTagName("value"):
            factor["level"].append( valueNode.childNodes[0].data )

        jsonDict["factors"].append(factor)

    # strength
    jsonDict["strength"] = {}
    jsonDict["strength"]["default"] = int(rootNode.getElementsByTagName("strength")[0].getAttribute("default"))
    jsonDict["strength"]["var_strengh"] = []
    for varStrenghNode in rootNode.getElementsByTagName("var_strengh"):
        varStrengthDict = {}
        varStrengthDict["factor"] = []
        varStrengthDict["strength"] = int( varStrenghNode.getAttribute("strength"))
        for pNode in varStrenghNode.getElementsByTagName("p"):
            varStrengthDict["factor"].append( pNode.getAttribute("name"))

        jsonDict["strength"]["var_strengh"].append( varStrengthDict)

    # seeds
    jsonDict["seeds"] = []
    for seedNode in rootNode.getElementsByTagName("seed"):
        seed = []
        for factNode in seedNode.getElementsByTagName("fact"):
            fact = {}
            fact["name"] = factNode.getAttribute("name")
            fact["value"] = factNode.getAttribute("value")
            seed.append( fact )

        jsonDict["seeds"].append( seed )

    return jsonDict


def resolveFactorInTxt(line):
    index = line.index(':')
    name = line[:index]
    level = line[index+1:]
    level = level.split(",")
    return name, level


def resolveVarStrengthInTxt(line):
    index = line.index('@')
    strength = int( line[index+1:])
    factors = line[1:index-1]
    factors = factors.split(',')
    return factors, strength


def txtFile2JsonDict(filePath):
    jsonDict = {}
    jsonDict["factors"] = []
    jsonDict["strength"] = {}
    jsonDict["strength"]["var_strengh"] = []
    jsonDict["seeds"] = []

    lines = None
    with open( filePath, "r", encoding='UTF-8' ) as fin:
        lines = fin.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace("\n", "").replace(" ","")

    for line in lines:
        if line[0] == '#':
            continue

        if line[0] == '@':
            jsonDict["strength"]["default"] = int( line[1:] )
            continue
        if line[0] == '{':
            if line[line.__len__()-1] == '@':
                levels = line[1:line.__len__()-2].split(',')
                seed = []
                for i in range(len(levels)):
                    if levels[i] == '@':
                        continue
                    seed.append( {"name": jsonDict["factors"][i]["name"], "value": levels[i] } )
                jsonDict["seeds"].append( seed )
                continue
            else:
                varStrength = {}
                factors, strength = resolveVarStrengthInTxt(line)
                varStrength["factor"] = factors
                varStrength["strength"] = strength
                jsonDict["strength"]["var_strengh"].append( varStrength )
                continue

        factor = {}
        name, level = resolveFactorInTxt( line )
        factor["name"] = name
        factor["level"] = level
        jsonDict["factors"].append( factor )
        continue

    return jsonDict


if __name__ == "__main__":
    command = "generate.exe tmp.txt"
    result = os.popen(command)
    for r in result:
        print( r )
    # jsonDict2Requirement( xmlFile2JsonDict("../input/input.xml"))
    # jsonDict2Requirement(txtFile2JsonDict("../input/input.txt")).print( "../input/tmp.txt" )
