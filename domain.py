from application import ApplicationProperty
import os

class ParamDomain:
    @staticmethod
    def readInitialParameterLabelList():
        paramList = {}
        fileName = ApplicationProperty.getScriptPath() + "/paramdomain/" + "initial.prm"
        if os.path.exists(fileName):
            try:
                file = open(fileName, 'r')
                for line in file.readlines():
                    temp = line.strip().split("\t")
                    key = int(temp[0])
                    value = temp[1].strip().split(":")[0].strip()
                    if key > -1 and len(value) > 0: paramList[key] = value
                file.close()
            except: pass
        else: pass
        return paramList

    @staticmethod
    def readInitialParameterDomainList():
        domainList = {}
        fileName = ApplicationProperty.getScriptPath() + "/paramdomain/" + "initial.prm"
        if os.path.exists(fileName):
            try:
                file = open(fileName, 'r')
                for line in file.readlines():
                    temp = line.strip().split("\t")[-1].strip().split(":")
                    key = temp[0]
                    value = []
                    if len(temp[1].strip()) > 0: value = temp[1].strip().split(",")
                    if len(value) > 0 and len(key) > 0:
                        for i in range(len(value)): value[i] = value[i].strip()
                        domainList[key] = value
                file.close()
            except: pass
        else: pass

        return domainList

    @staticmethod
    def readGisParameterLabelList():
        paramList = {}
        fileName = ApplicationProperty.getScriptPath() + "/paramdomain/" + "gis.prm"
        if os.path.exists(fileName):
            try:
                file = open(fileName, 'r')
                for line in file.readlines():
                    temp = line.strip().split("\t")
                    key = int(temp[0])
                    value = temp[1].strip().split(":")[0].strip()
                    if key > -1 and len(value) > 0: paramList[key] = value
                file.close()
            except: pass
        else: pass
        return paramList

    @staticmethod
    def readGisParameterDomainList():
        domainList = {}
        fileName = ApplicationProperty.getScriptPath() + "/paramdomain/" + "gis.prm"
        if os.path.exists(fileName):
            try:
                file = open(fileName, 'r')
                for line in file.readlines():
                    temp = line.strip().split("\t")[-1].strip().split(":")
                    key = temp[0]
                    value = []
                    if len(temp) > 1:
                        if len(temp[1].strip()) > 0: value = temp[1].strip().split(",")
                    if len(value) > 0 and len(key) > 0:
                        for i in range(len(value)): value[i] = value[i].strip()
                        domainList[key] = value
                file.close()
            except: pass
        else: pass

        return domainList

    @staticmethod
    def readVegetationParameterLabelList():
        paramList = {}
        fileName = ApplicationProperty.getScriptPath() + "/paramdomain/" + "veg.prm"
        if os.path.exists(fileName):
            try:
                file = open(fileName, 'r')
                for line in file.readlines():
                    temp = line.strip().split("\t")
                    key = int(temp[0])
                    value = temp[1].strip().split(":")[0].strip()
                    if key > -1 and len(value) > 0: paramList[key] = value
                file.close()
            except: pass
        else: pass
        return paramList

    @staticmethod
    def readVegetationParameterDomainList():
        domainList = {}
        fileName = ApplicationProperty.getScriptPath() + "/paramdomain/" + "veg.prm"
        if os.path.exists(fileName):
            try:
                file = open(fileName, 'r')
                for line in file.readlines():
                    temp = line.strip().split("\t")[-1].strip().split(":")
                    key = temp[0]
                    value = []
                    if len(temp) > 1:
                        if len(temp[1].strip()) > 0: value = temp[1].strip().split(",")
                    if len(value) > 0 and len(key) > 0:
                        for i in range(len(value)): value[i] = value[i].strip()
                        domainList[key] = value
                file.close()
            except: pass
        else: pass

        return domainList

    @staticmethod
    def readEpcParameterLabelList():
        paramList = {}
        fileName = ApplicationProperty.getScriptPath() + "/paramdomain/" + "epc.prm"
        if os.path.exists(fileName):
            try:
                file = open(fileName, 'r')
                for line in file.readlines():
                    temp = line.strip().split("\t")
                    key = int(temp[0])
                    value = temp[1].strip().split(":")[0].strip()
                    if key > -1 and len(value) > 0: paramList[key] = value
                file.close()
            except: pass
        else: pass
        return paramList

    @staticmethod
    def readEpcParameterDomainList():
        domainList = {}
        fileName = ApplicationProperty.getScriptPath() + "/paramdomain/" + "epc.prm"
        if os.path.exists(fileName):
            try:
                file = open(fileName, 'r')
                for line in file.readlines():
                    temp = line.strip().split("\t")[-1].strip().split(":")
                    key = temp[0]
                    value = []
                    if len(temp) > 1:
                        if len(temp[1].strip()) > 0: value = temp[1].strip().split(",")
                    if len(value) > 0 and len(key) > 0:
                        for i in range(len(value)): value[i] = value[i].strip()
                        domainList[key] = value
                file.close()
            except: pass
        else: pass

        return domainList

    @staticmethod
    def readSoilParameterLabelList():
        paramList = {}
        fileName = ApplicationProperty.getScriptPath() + "/paramdomain/" + "soil.prm"
        if os.path.exists(fileName):
            try:
                file = open(fileName, 'r')
                for line in file.readlines():
                    temp = line.strip().split("\t")
                    key = int(temp[0])
                    value = temp[1].strip().split(":")[0].strip()
                    if key > -1 and len(value) > 0: paramList[key] = value
                file.close()
            except: pass
        else: pass
        return paramList

    @staticmethod
    def readSoilTextureList():
        paramList = []  #structure: [texture1, texture2, texture3, ....]
        fileName = ApplicationProperty.getScriptPath() + "/paramdomain/" + "soiltexture.prm"
        if os.path.exists(fileName):
            try:
                file = open(fileName, 'r')
                for line in file.readlines():
                    temp = str(line.strip().strip("/n"))
                    paramList.append(temp)
            except: pass

        return paramList

class ParamOption:
    #the structure of option list looks complex at the beginning
    #but to enable reading value by key and reading key by value
    #list of 'dictionaries' is used here.
    #Nitrogen deposition options for init file
    nitrogenDepositionOptionList = [{'param': '0. Constant', 'val': 0},
                  {'param': '1. Varying with File Value', 'val': 1}, #File name is mentioned in GIS file
                  {'param': '2. Ramped N-deposition run', 'val': 2}] #Only with CO2 flag = 1

    #Daily output option list for init file
    dailyOutputOptionList = [{'param': '0. No daily output', 'val': 0},
                                  {'param': '1. Write daily output', 'val': 1},
                                  {'param': '2. Depth and corresponding variables', 'val': 2},
                                  {'param': '3. Variable and corresponding depths', 'val': 3},
                                  {'param': '4. Both depth and variables', 'val': 4}]

    #Yearly output option list for init file
    annualOutputOptionList = [{'param': '0. No annual output', 'val': 0},
                                  {'param': '1. Write annual output', 'val': 1},
                                  {'param': '2. Depth and corresponding variables', 'val': 2},
                                  {'param': '3. Variable and corresponding depths', 'val': 3},
                                  {'param': '4. Both depth and variables', 'val': 4}]

    #Output template list
    outputTemplateList = []

    @staticmethod
    def getOutputTemplateList():
        templateList = []
        tarDir = ApplicationProperty().getScriptPath() + "/outputtemplate"

        fileList = [f for f in os.listdir(tarDir) if os.path.isfile(os.path.join(tarDir,f)) ]
        for item in fileList:
            templateList.append(item.replace(".txt",""))

        return templateList

    @staticmethod
    def getAnnualOutputOption(val):
        paramName = ""
        for item in ParamOption.annualOutputOptionList:
            if item['val'] == val:
                paramName = ""
                break
        return paramName

    @staticmethod
    def getAnnualOutputOptionValue(param):
        paramValue = -1
        for item in ParamOption.annualOutputOptionList:
            if item['param'] == param:
                paramValue = item['val']
                break
        return paramValue

    @staticmethod
    def getDailyOutputOption(val):
        paramName = ""
        for item in ParamOption.dailyOutputOptionList:
            if item['val'] == val:
                paramName = item['param']
                break
        return paramName

    @staticmethod
    def getDailyOutputOptionValue(param):
        paramValue = -1
        for item in ParamOption.dailyOutputOptionList:
            if item['param'] == param:
                paramValue = item['val']
                break
        return paramValue

    @staticmethod
    def getNitrogenDepositionOption(val):
        paramName = ""
        for item in ParamOption.nitrogenDepositionOptionList:
            if item['val'] == val:
                paramName = item['param']
                break
        return paramName

    @staticmethod
    def getNitrogenDepositionOptionValue(param):
        paramValue = -1
        for item in ParamOption.nitrogenDepositionOptionList:
            if item['param'] == param:
                paramValue = item['val']
                break
        return paramValue

