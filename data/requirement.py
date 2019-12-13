import json
from xml.dom import minidom


class Requirement:
    def __init__(self):
        self.factors = []
        self.factorNames = []
        self.factorsNumber = []
        self.strength = None

        self.varFactors = []
        self.varStrengths = []

        self.seeds = []
        self.addValue = 0 # 种子中的缺省项

        self.testcases = []

    def addFactor(self,name,factor):
        self.factorNames.append(name)
        self.factors.append(factor)

    def showFactors(self):
        print("self.factors:")
        print( self.factors )
        print( "self.factorNames:" )
        print( self.factorNames )
        print("self.factorsNumber:")
        print( self.factorsNumber )

    def updateFactorsNumber(self):
        self.factorsNumber = []
        for i in range(len(self.factors)):
            self.factorsNumber.append( len(self.factors[i]) )

    def setStrength(self,strength):
        self.strength = strength

    def getFactorIndex(self, name):
        for i in range(len(self.factorNames)):
            if name == self.factorNames[i]:
                return i
        raise Exception("cannot find this factor: " + name)

    def name2index(self,factors):
        for i in range(len(factors)):
            factors[i] = self.getFactorIndex(factors[i])
        return factors

    def addVarFactor(self,factors,varStrength):
        factors = self.name2index(factors)
        self.varFactors.append(factors)
        self.varStrengths.append(varStrength)

    def addSeed(self,seed):
        self.seeds.append(seed)

    def addTestcase(self,testcase):
        """
        :param testcase: [ 0, 1, 1, 2 ]
        :return:
        """
        for i in range(len(testcase)):
            testcase[i] = self.factors[i][int(testcase[i])]
        self.testcases.append( testcase )

    def addSeedByFactorDict(self, factorsDict):
        for i in range(len(factorsDict)):
            factorsDict[i]["name"] = self.getFactorIndex(factorsDict[i]["name"])
        for i in range(len(factorsDict)):
            factorsDict[i]["value"] = self.getValueIndex( factorsDict[i]["name"], factorsDict[i]["value"])
        factorsDict.sort(key=lambda obj:(obj.get("name")))
        j = 0
        for i in range(len(self.factorNames)):
            if j < len(factorsDict) and factorsDict[j]["name"] == i:
                j += 1
                i += 1
            else:
                factorsDict.append( { "name": i, "value": self.addValue } )
                i += 1
        factorsDict.sort(key=lambda obj: (obj.get("name")))

        seed = []
        for factorDict in factorsDict:
            seed.append( factorDict["value"] )

        self.seeds.append( seed )

    def getValueIndex(self, factorIndex, value):
        for i in range(len(self.factors[factorIndex])):
            if value == self.factors[factorIndex][i]:
                return i
        raise Exception("cannot find this value " + value + " in " + self.factorNames[factorIndex])

    def print(self,filePath=None):
        seperateNum = -2

        content = ""

        # factors
        for num in self.factorsNumber:
            content += str(num) + " "
        content += str(seperateNum) + "\n"

        # strength
        content += str(self.strength) + " " + str(seperateNum) + "\n"

        # var strength
        for i in range(len(self.varFactors)):
            factors = self.varFactors[i]
            strength = int( self.varStrengths[i] )
            for factor in factors:
                content += str(factor) + " "
            content += str(seperateNum) + " "

            content += str(strength) + " " + str(seperateNum) + "\n"
        content += str(seperateNum) + "\n"

        # seeds
        for seed in self.seeds:
            for s in seed:
                content += str(s) + " "
            content += str( seperateNum ) + "\n"
        content += str(seperateNum) + "\n"

        if filePath is not None:
            with open(filePath,"w") as fout:
                fout.write(content)
        else:
            print( content )

    def write2JsonFile(self,filePath):
        testcases = {"testcases": []}
        for t in self.testcases:
            testcase = { "testcase": [] }
            for i in range(len(t)):
                testcase["testcase"].append( {"name":self.factorNames[i], "value": t[i] })
            testcases["testcases"].append( testcase )
        json.dump( testcases, open(filePath,"w",encoding="utf-8"), indent=2, ensure_ascii=False )

    def write2XmlFile(self,filePath):
        xml = minidom.Document()
        rootNode = xml.createElement("testcases")
        xml.appendChild( rootNode )
        for testcase in self.testcases:
            testcaseNode = xml.createElement("testcase")
            rootNode.appendChild( testcaseNode )
            for i in range(len(testcase)):
                factNode = xml.createElement("fact")
                factNode.setAttribute("name",self.factorNames[i])

                factTextNode = xml.createTextNode(testcase[i])
                factNode.appendChild(factTextNode)

                testcaseNode.appendChild(factNode)

        with open( filePath, "w", encoding="utf-8" ) as fout:
            xml.writexml( fout, indent="\n", addindent="\t", encoding="UTF-8" )

    def write2TxtFile(self,filePath):
        lines = []
        for i in range(len(self.testcases)):
            line = str(i) + ":\t" + "\t".join(self.testcases[i]) + "\n"
            lines.append(line)
        with open( filePath, "w", encoding="utf-8" ) as fout:
            fout.writelines( lines )

    def getJsonOutput(self):
        testcases = {"testcases": []}
        for t in self.testcases:
            testcase = {"testcase": []}
            for i in range(len(t)):
                testcase["testcase"].append({"name": self.factorNames[i], "value": t[i]})
            testcases["testcases"].append(testcase)
        return json.dumps(testcases, indent=2, ensure_ascii=False)

    def getXmlOutput(self):
        xml = minidom.Document()
        rootNode = xml.createElement("testcases")
        xml.appendChild(rootNode)
        for testcase in self.testcases:
            testcaseNode = xml.createElement("testcase")
            rootNode.appendChild(testcaseNode)
            for i in range(len(testcase)):
                factNode = xml.createElement("fact")
                factNode.setAttribute("name", self.factorNames[i])

                factTextNode = xml.createTextNode(testcase[i])
                factNode.appendChild(factTextNode)

                testcaseNode.appendChild(factNode)

        with open("tmpXml", "w", encoding="utf-8") as fout:
            xml.writexml(fout, indent="\n", addindent="\t", encoding="UTF-8")
        with open("tmpXml", "r", encoding="utf-8" ) as fin:
            content = fin.read()
        return content

    def getTxtOutput(self):
        lines = []
        for i in range(len(self.testcases)):
            line = str(i) + ":\t" + "\t".join(self.testcases[i]) + "\n"
            lines.append(line)
        return "".join( lines )