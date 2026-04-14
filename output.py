# from FlatfileDatabase import DatabaseReadWrite
from application import ApplicationProperty
import os

class output:
    listOfSiteSpecificCategory = []
    listOfVegSpecificCategory = []
    listOfSiteSpecificVariable = []
    listOfVegSpecificVariable = []
    listOfLayerSpecificVariable = []

    def __init__(self):
        if not output.listOfSiteSpecificCategory:
            output.listOfSiteSpecificCategory = output.siteSpecificOutputCategoryList()  #[{},{},{}..]

        if not output.listOfVegSpecificCategory:
            output.listOfVegSpecificCategory = output.vegetationSpecificOutputCategoryList()

        #reading site specific variables
        if not output.listOfSiteSpecificVariable:
            for catItem in output.listOfSiteSpecificCategory:
                catid = catItem["catid"]
                varList = output.siteSpecificOutputVariableList(catid)

                for var in varList:
                    output.listOfSiteSpecificVariable.append(var)

        #reading vegetation specific variables
        if not output.listOfVegSpecificVariable:
            for catItem in output.listOfVegSpecificCategory:
                catid = catItem["catid"]
                varList = output.vegetationSpecificOutputVariableList(catid)

                for var in varList:
                    output.listOfVegSpecificVariable.append(var)

        #reading layer specific variables
        if not output.listOfLayerSpecificVariable:
            output.listOfLayerSpecificVariable = output.layerSpecificOutputVariableList()

        #selected output list
        self.listOfSelectedSiteSpecificVariable_Annual = []     #structure [{"catid": 13, "varid": '01'},{}]
        self.listOfSelectedSiteSpecificVariable_Daily = []      #structure [{"catid": 13, "varid": '11'},{}]
        self.listOfSelectedVegSpecificVariable_Annual = []      #structure [{"catid": 13, "varid": '101'},{}]
        self.listOfSelectedVegSpecificVariable_Daily = []       #structure [{"catid": 13, "varid": '23'},{}]
        self.listOfSelectedTotalLayerVariable = []              #structure ['12', '13',...]
        self.selectedDailyVarLayerList = []                     #structure [{"varid": "34", "laylist": ["12", "23"]}, {}]
        self.selectedAnnualVarLayerList = []                    #structure [{"varid": "34", "laylist": []},{}]
        self.selectedDailyLayerVarList = []                     #sturcture [{"layer": "20", "varlist": []},{}]
        self.selectedAnnualLayerVarList = []                    #sturcture [{"layer": "20", "varlist": []},{}]

    @staticmethod
    def siteSpecificOutputCategoryList():
        categoryList = []
        tarDir = ApplicationProperty().getScriptPath() + "/variablelist/sitespecific/site_variable_list.txt"
        try:
            file = open(tarDir)
            for line in file.readlines():
                temp = line.replace("\n","").split(", ")
                var = {"catid": temp[0], "catname": temp[1]}
                categoryList.append(var)
            #categoryList.append(file.readlines())
            file.close()
        except Exception as ex:
            return None

        return  categoryList

    @staticmethod
    def vegetationSpecificOutputCategoryList():
        categoryList = []
        tarDir = ApplicationProperty().getScriptPath() + "/variablelist/vegspecific/veg_variable_list.txt"

        try:
            file = open(tarDir)
            for line in file.readlines():
                if line:
                    temp = line.replace("\n","").split(",")
                    if temp:
                        var = {"catid": temp[0], "catname": temp[1]}
                        categoryList.append(var)
            file.close()
        except Exception as Ex:
            return None

        return  categoryList

    @staticmethod
    def siteSpecificOutputVariableList(categoryId):
        varList = []
        tarDir = os.path.join(ApplicationProperty().getScriptPath(), "variablelist", "sitespecific", categoryId + ".txt")

        try:
            file = open(tarDir)
            for line in file.readlines():
                if line:
                    temp = line.replace("\n","").split(",")
                    var = {"catid": categoryId, "varid": int(temp[0].strip()),
                           "varname": temp[1].strip(), "vardesc": temp[2].strip()}
                    varList.append(var)
            file.close()
        except Exception as Ex:
            pass
        return varList

    @staticmethod
    def vegetationSpecificOutputVariableList(categoryId):
        varList = []
        tarDir = ApplicationProperty().getScriptPath() + "/variablelist/vegspecific/" + categoryId + ".txt"

        try:
            file = open(tarDir)
            for line in file.readlines():
                if line:
                    temp = line.replace("\n","").split(",")
                    var = {"catid": categoryId, "varid": int(temp[0].strip()),
                           "varname": temp[1].strip(), "vardesc": temp[2].strip()}
                    varList.append(var)
            file.close()
        except Exception as Ex:
            pass
        return varList

    @staticmethod
    def layerSpecificOutputVariableList():
        varList = []
        tarDir = ApplicationProperty().getScriptPath() + "/variablelist/layerspecific/layer_variable_list.txt"

        try:
            file = open(tarDir)
            for line in file.readlines():
                if line:
                    temp = line.replace("\n","").split(",")
                    var = {"varid": temp[0].strip(), "varname": temp[1].strip(), "vardesc": temp[2].strip()}
                    varList.append(var)
        except: pass
        finally:
            try: file.close()
            except: pass

        return varList

#clear all list
    def clear(self):
        self.listOfSelectedSiteSpecificVariable_Annual = []
        self.listOfSelectedSiteSpecificVariable_Daily = []
        self.listOfSelectedVegSpecificVariable_Annual = []
        self.listOfSelectedVegSpecificVariable_Daily = []
        self.listOfSelectedTotalLayerVariable = []
        self.selectedDailyVarLayerList = []
        self.selectedAnnualVarLayerList = []
        self.selectedDailyLayerVarList = []
        self.selectedAnnualLayerVarList = []

    def clearSiteSpecificSelectedList(self, dailyVar=False, annualVar=False):
        if dailyVar: self.listOfSelectedSiteSpecificVariable_Daily = []
        if annualVar: self.listOfSelectedSiteSpecificVariable_Annual = []

    def clearVegSpecificSelectedList(self,dailyVar=False, annualVar=False):
        if dailyVar: self.listOfSelectedVegSpecificVariable_Daily = []
        if annualVar: self.listOfSelectedVegSpecificVariable_Annual = []

#sorting list of dictionary
    def sortListOfSelectedSiteSpecificVariable_Annual(self):
        varidList = []
        for var in self.listOfSelectedSiteSpecificVariable_Annual:
            varidList.append(var["varid"])
        varidList.sort()
        tempList = []
        for varid in varidList:
            for var in self.listOfSelectedSiteSpecificVariable_Annual:
                if var["varid"] == varid:
                    tempList.append(var)
                    break
        self.listOfSelectedSiteSpecificVariable_Annual = tempList

    def sortListOfSelectedSiteSpecificVariable_Daily(self):
        varidList = []
        for var in self.listOfSelectedSiteSpecificVariable_Daily:
            varidList.append(var["varid"])
        varidList.sort()
        tempList = []
        for varid in varidList:
            for var in self.listOfSelectedSiteSpecificVariable_Daily:
                if var["varid"] == varid:
                    tempList.append(var)
                    break
        self.listOfSelectedSiteSpecificVariable_Daily = tempList

    def sortListOfSelectedVegSpecificVariable_Annual(self):
        varidList = []
        for var in self.listOfSelectedVegSpecificVariable_Annual:
            varidList.append(var["varid"])
        varidList.sort()
        tempList = []
        for varid in varidList:
            for var in self.listOfSelectedVegSpecificVariable_Annual:
                if var["varid"] == varid:
                    tempList.append(var)
                    break
        self.listOfSelectedVegSpecificVariable_Annual = tempList

    def sortListOfSelectedVegSpecificVariable_Daily(self):
        varidList = []
        for var in self.listOfSelectedVegSpecificVariable_Daily:
            varidList.append(var["varid"])
        varidList.sort()
        tempList = []
        for varid in varidList:
            for var in self.listOfSelectedVegSpecificVariable_Daily:
                if var["varid"] == varid:
                    tempList.append(var)
                    break
        self.listOfSelectedVegSpecificVariable_Daily = tempList

    def sortListOfSelectedTotalLayerVariable(self):
        intList = []
        strList = []
        for varid in self.listOfSelectedTotalLayerVariable:
            try:
                intList.append(int(varid))
            except:
                strList.append(varid)

        temp = []
        if len(intList) > 0:
            intList.sort()
            for item in intList:
                temp.append(str(item))
        if len(strList) > 0:
            strList.sort()
            for item in strList:
                temp.append(item)

        self.listOfSelectedTotalLayerVariable = temp

    def sortSelectedDailyVarLayerList(self):
        varidList = []
        for item in self.selectedDailyVarLayerList:
            varidList.append(item["varid"])
            item["laylist"] = self.sortAlphaNumericList(item["laylist"])

        varidList.sort()
        temp = []
        for varid in varidList:
            for item in self.selectedDailyVarLayerList:
                if item["varid"] == varid:
                    temp.append(item)
                    break

        self.selectedDailyVarLayerList = temp

    def sortSelectedAnnualVarLayerList(self):
        varidList = []
        for item in self.selectedAnnualVarLayerList:
            varidList.append(item["varid"])
            item["laylist"] = self.sortAlphaNumericList(item["laylist"])

        varidList.sort()
        temp = []
        for varid in varidList:
            for item in self.selectedAnnualVarLayerList:
                if item["varid"] == varid:
                    temp.append(item)
                    break

        self.selectedAnnualVarLayerList = temp

    def sortSelectedDailyLayerVarList(self):
        layerList = []
        for item in self.selectedDailyLayerVarList:
            layerList.append(item["layer"])
            item["varlist"] = self.sortAlphaNumericList(item["varlist"])

        layerList.sort()
        temp = []
        for layer in layerList:
            for item in self.selectedDailyLayerVarList:
                if item["layer"] == layer:
                    temp.append(item)
                    break

        self.selectedDailyLayerVarList = temp

    def sortSelectedAnnualLayerVarList(self):
        layerList = []
        for item in self.selectedAnnualLayerVarList:
            layerList.append(item["layer"])
            item["varlist"] = self.sortAlphaNumericList(item["varlist"])

        layerList.sort()
        temp = []
        for layer in layerList:
            for item in self.selectedAnnualLayerVarList:
                if item["layer"] == layer:
                    temp.append(item)
                    break

        self.selectedAnnualLayerVarList = temp

    def sortAlphaNumericList(self, alphaNumbericList):
        numericList = []
        textList = []
        for item in alphaNumbericList:
            try:
                numericList.append(int(item))
            except:
                textList.append(item)

        temp = []
        numericList.sort()
        textList.sort()

        for item in numericList:
            temp.append(str(item))

        for text in textList:
            temp.append(text)

        return temp

#functions for finding category name using category id
    @staticmethod
    def getSiteSpecificCategoryName(catid):
        for catItem in output.listOfSiteSpecificCategory:
            if catItem["catid"] == catid:
                return catItem["catname"]
        return None

    @staticmethod
    def getVegetationSpecificCategoryName(catid):
        for catItem in output.listOfVegSpecificCategory:
            if catItem["catid"] == catid:
                return catItem["catname"]
        return None


#functions for annual_output [layer~variable]
    def addVariableToAnnualLayerVarList_VarId(self, layer, varid):
        count = len(self.selectedAnnualLayerVarList)
        for i in range(count):
            if self.selectedAnnualLayerVarList[i]["layer"] == layer:
                for item in self.selectedAnnualLayerVarList[i]["varlist"]:
                    if item == varid: break
                else:
                    self.selectedAnnualLayerVarList[i]["varlist"].append(varid)
                break
        else:
            newItem = {"layer": layer, "varlist": [varid]}
            self.selectedAnnualLayerVarList.append(newItem)

    def addVariableToAnnualLayerVarList(self, layer, varname):
        varid = self.getLayerSpecificVarialbleId(varname)

        count = len(self.selectedAnnualLayerVarList)
        for i in range(count):
            if self.selectedAnnualLayerVarList[i]["layer"] == layer:
                for item in self.selectedAnnualLayerVarList[i]["varlist"]:
                    if item == varid: break
                else:
                    self.selectedAnnualLayerVarList[i]["varlist"].append(varid)
                break
        else:
            newItem = {"layer": layer, "varlist": [varid]}
            self.selectedAnnualLayerVarList.append(newItem)

    def removeVariableFromAnnualLayerVarList(self, layer):
        count = len(self.selectedAnnualLayerVarList)
        for i in range(count):
            if self.selectedAnnualLayerVarList[i]["layer"] == layer:
                self.selectedAnnualLayerVarList.pop(i)
                break

    def getTextLinesFromAnnualLayerVarList(self):
        self.sortSelectedAnnualLayerVarList()
        lines = []
        for item in self.selectedAnnualLayerVarList:
            temp = str(item["layer"]) + ":"
            for var in item["varlist"]:
                temp += str(var) + ", "
            lines.append(temp[:-2])
        return lines

#functions for daily_output [layer~variable]
    def addVariableToDailyLayerVarList_VarId(self, layer, varid):
        count = len(self.selectedDailyLayerVarList)
        for i in range(count):
            if self.selectedDailyLayerVarList[i]["layer"] == layer:
                for item in self.selectedDailyLayerVarList[i]["varlist"]:
                    if item == varid: break
                else:
                    self.selectedDailyLayerVarList[i]["varlist"].append(varid)
                break
        else:
            newItem = {"layer": layer, "varlist": [varid]}
            self.selectedDailyLayerVarList.append(newItem)

    def addVariableToDailyLayerVarList(self, layer, varname):
        varid = self.getLayerSpecificVarialbleId(varname)

        count = len(self.selectedDailyLayerVarList)
        for i in range(count):
            if self.selectedDailyLayerVarList[i]["layer"] == layer:
                for item in self.selectedDailyLayerVarList[i]["varlist"]:
                    if item == varid: break
                else:
                    self.selectedDailyLayerVarList[i]["varlist"].append(varid)
                break
        else:
            newItem = {"layer": layer, "varlist": [varid]}
            self.selectedDailyLayerVarList.append(newItem)

    def removeVariableFromDailyLayerVarList(self, layer):
        count = len(self.selectedDailyLayerVarList)
        for i in range(count):
            if self.selectedDailyLayerVarList[i]["layer"] == layer:
                self.selectedDailyLayerVarList.pop(i)
                break

    def getTextLinesFromDailyLayerVarList(self):
        self.sortSelectedDailyLayerVarList()
        lines = []
        for item in self.selectedDailyLayerVarList:
            temp = str(item["layer"]) + ":"
            for var in item["varlist"]:
                temp += str(var) + ", "
            lines.append(temp[:-2])
        return lines

#function for annual_output [varirable~layer]
    def addVariableToAnnualVarLayList_VarId(self, varid, layer):
        count = len(self.selectedAnnualVarLayerList)
        for i in range(count):
            if self.selectedAnnualVarLayerList[i]["varid"] == varid:
                for item in self.selectedAnnualVarLayerList[i]["laylist"]:
                    if item == layer: break
                else:
                    self.selectedAnnualVarLayerList[i]["laylist"].append(layer)
                break
        else:
            newItem = {"varid": varid, "laylist": [layer]}
            self.selectedAnnualVarLayerList.append(newItem)

    def addVariableToAnnualVarLayList(self, varname, layer):
        varid = self.getLayerSpecificVarialbleId(varname)

        count = len(self.selectedAnnualVarLayerList)
        for i in range(count):
            if self.selectedAnnualVarLayerList[i]["varid"] == varid:
                for item in self.selectedAnnualVarLayerList[i]["laylist"]:
                    if item == layer: break
                else:
                    self.selectedAnnualVarLayerList[i]["laylist"].append(layer)
                break
        else:
            newItem = {"varid": varid, "laylist": [layer]}
            self.selectedAnnualVarLayerList.append(newItem)

    def removeVariableFromAnnualVarLayList(self, varid):
        count = len(self.selectedAnnualVarLayerList)
        for i in range(count):
            if self.selectedAnnualVarLayerList[i]["varid"] == varid:
                self.selectedAnnualVarLayerList.pop(i)
                break

    def getTextLinesFromAnnualVarLayerList(self):
        self.sortSelectedAnnualVarLayerList()
        lines = []
        for item in self.selectedAnnualVarLayerList:
            temp = str(item["varid"]) + ":"
            for var in item["laylist"]:
                temp += str(var) + ", "
            lines.append(temp[:-2])
        return lines

#function for daily_output [varirable~layer]
    def addVariableToDailyVarLayList_VarId(self, varid, layer):
        count = len(self.selectedDailyVarLayerList)
        for i in range(count):
            if self.selectedDailyVarLayerList[i]["varid"] == varid:
                for item in self.selectedDailyVarLayerList[i]["laylist"]:
                    if item == layer: break
                else:
                    self.selectedDailyVarLayerList[i]["laylist"].append(layer)

                break
        else:
            newItem = {"varid": varid, "laylist": [layer]}
            self.selectedDailyVarLayerList.append(newItem)

    def addVariableToDailyVarLayList(self, varname, layer):
        varid = self.getLayerSpecificVarialbleId(varname)

        if varid:
            count = len(self.selectedDailyVarLayerList)
            for i in range(count):
                if self.selectedDailyVarLayerList[i]["varid"] == varid:
                    for item in self.selectedDailyVarLayerList[i]["laylist"]:
                        if item == layer: break
                    else:
                        self.selectedDailyVarLayerList[i]["laylist"].append(layer)

                    break
            else:
                newItem = {"varid": varid, "laylist": [layer]}
                self.selectedDailyVarLayerList.append(newItem)

    def removeVariableFromDailyVarLayList(self, varid):
        count = len(self.selectedDailyVarLayerList)
        for i in range(count):
            if self.selectedDailyVarLayerList[i]["varid"] == varid:
                self.selectedDailyVarLayerList.pop(i)
                break

    def getTextLinesFromDailyVarLayerList(self):
        self.sortSelectedDailyVarLayerList()
        lines = []
        for item in self.selectedDailyVarLayerList:
            temp = str(item["varid"]) + ":"
            for var in item["laylist"]:
                temp += str(var) + ", "
            lines.append(temp[:-2])
        return lines

#functions for layer specific variables
    @staticmethod
    def getLayerSpecificVarialbleId(varname):
        varid = -1
        for var in output.listOfLayerSpecificVariable:
            if var["varname"] == varname:
                varid = var["varid"]

        return  varid

    @staticmethod
    def getLayerSpecificVariableName(varid):
        varname = ""
        for var in output.listOfLayerSpecificVariable:
            if var["varid"] == varid:
                varname = var["varname"]

        return varname

    @staticmethod
    def getLayerSpecificVariable(varid):
        var = None
        for item in output.listOfLayerSpecificVariable:
            if item["varid"] == varid:
                var = item

        return var

    @staticmethod
    def getLayerSpecificVariableList():
        return output.listOfLayerSpecificVariable


#functions for total layer variables
    def addVariableToSelectedTotalLayer_ByVarId(self, varid):
        self.listOfSelectedTotalLayerVariable.append(varid)

    def addVariableToSelectedTotalLayer_ByVarName(self, varname):
        varid = self.getLayerSpecificVarialbleId(varname)
        self.listOfSelectedTotalLayerVariable.append(varid)

    def removeVariableFromSelectedTotalLayer_ByVarName(self, varname):
        varid = self.getLayerSpecificVarialbleId(varname)
        self.listOfSelectedTotalLayerVariable.remove(varid)

    def getSelectedTotalLayerVariableList(self):
        self.sortListOfSelectedTotalLayerVariable()

        varList = []
        for varid in self.listOfSelectedTotalLayerVariable:
            varList.append(self.getLayerSpecificVariable(varid))
        return varList

    def getUnselectedTotalLayerVariableList(self):
        
        varList = []
        for var in output.listOfLayerSpecificVariable:
            for varid in self.listOfSelectedTotalLayerVariable:
                if var["varid"] == varid: break
            else:
                varList.append(var)
        return varList

#functions for site specific daily variables
    def addVariableToSelectedSiteSpecificList_Daily_ByVarId(self, varid):
        catid = self.getSiteSpecificVarCategoryId_VarId(varid)

        var = {"catid": catid, "varid": varid}
        self.listOfSelectedSiteSpecificVariable_Daily.append(var)

    def addVariableToSelectedSiteSpecificList_Daily_ByVarName(self, category, varname):
        catid = self.getSiteSpecificVarCategoryId(category)
        varid = self.getSiteSpecificVariableId(catid, varname)

        var = {"catid": catid, "varid": varid}
        self.listOfSelectedSiteSpecificVariable_Daily.append(var)

    def removeVariableFromSelectedSiteSpecificList_Daily_ByVarName(self, category, varname):
        catid = self.getSiteSpecificVarCategoryId(category)
        varid = self.getSiteSpecificVariableId(catid,varname)
        count = len(self.listOfSelectedSiteSpecificVariable_Daily)

        for i in reversed(range(count)):
            if (self.listOfSelectedSiteSpecificVariable_Daily[i].get('catid') == catid and
                self.listOfSelectedSiteSpecificVariable_Daily[i].get('varid') == varid):
                self.listOfSelectedSiteSpecificVariable_Daily.pop(i)

    def getSelectedSiteSpecificVariableList_Daily(self, categoy):
        self.sortListOfSelectedSiteSpecificVariable_Daily()
        catid = self.getSiteSpecificVarCategoryId(categoy)

        listOfVariable = []

        for item in self.listOfSelectedSiteSpecificVariable_Daily:
            if item["catid"] == catid:

                listOfVariable.append(self.getSiteSpecificVariable(catid,item["varid"]))

        return listOfVariable

    def getAllSelectedSiteSpecificVariableList(self, daily=False, annual=False):
        listOfVariable = []
        if daily:
            for item in self.listOfSelectedSiteSpecificVariable_Daily:
                varid = item["varid"]
                catid = self.getSiteSpecificVarCategoryId_VarId(varid)
                var = self.getSiteSpecificVariable(catid, varid)
                var["catname"] = self.getSiteSpecificCategoryName(catid)
                listOfVariable.append(var)

        if annual:
            for item in self.listOfSelectedSiteSpecificVariable_Annual:
                varid = item["varid"]
                catid = self.getSiteSpecificVarCategoryId_VarId(varid)
                var = self.getSiteSpecificVariable(catid, varid)
                var["catname"] = self.getSiteSpecificCategoryName(catid)
                listOfVariable.append(var)

        return listOfVariable

    def getUnselectedSiteSpecificVariableList_Daily(self, category):
        catid = self.getSiteSpecificVarCategoryId(category)

        selVarIdList = []
        for item in self.listOfSelectedSiteSpecificVariable_Daily:
            if item["catid"] == catid:
                selVarIdList.append(item["varid"])

        varCatList = self.getSiteSpecificVarriableList(catid)

        unselList = []
        for var in varCatList:
            for item in selVarIdList:
                if var["varid"] == item: break
            else: unselList.append(var)

        return unselList

#functions for site specific annual variables
    def addVariableToSelectedSiteSpecificList_Annual_ByVarId(self, varid):
        catid = self.getSiteSpecificVarCategoryId_VarId(varid)

        var = {"catid": catid, "varid": varid}
        self.listOfSelectedSiteSpecificVariable_Annual.append(var)

    def addVariableToSelectedSiteSpecificList_Annual_ByVarName(self, category, varname):
        catid = self.getSiteSpecificVarCategoryId(category)
        varid = self.getSiteSpecificVariableId(catid, varname)

        var = {"catid": catid, "varid": varid}
        self.listOfSelectedSiteSpecificVariable_Annual.append(var)

    def removeVariableFromSelectedSiteSpecificList_Annual_ByVarName(self, category, varname):
        catid = self.getSiteSpecificVarCategoryId(category)
        varid = self.getSiteSpecificVariableId(catid,varname)
        count = len(self.listOfSelectedSiteSpecificVariable_Annual)

        for i in reversed(range(count)):
            if (self.listOfSelectedSiteSpecificVariable_Annual[i].get('catid') == catid and
                self.listOfSelectedSiteSpecificVariable_Annual[i].get('varid') == varid):
                self.listOfSelectedSiteSpecificVariable_Annual.pop(i)

    def getSelectedSiteSpecificVariableList_Annual(self, categoy):
        self.sortListOfSelectedSiteSpecificVariable_Annual()

        catid = self.getSiteSpecificVarCategoryId(categoy)

        listOfVariable = []

        for item in self.listOfSelectedSiteSpecificVariable_Annual:
            if item["catid"] == catid:
                listOfVariable.append(self.getSiteSpecificVariable(catid,item["varid"]))

        return listOfVariable


    def getUnselectedSiteSpecificVariableList_Annual(self, category):
        catid = self.getSiteSpecificVarCategoryId(category)

        selVarIdList = []
        for item in self.listOfSelectedSiteSpecificVariable_Annual:
            if item["catid"] == catid:
                selVarIdList.append(item["varid"])

        varCatList = self.getSiteSpecificVarriableList(catid)

        unselList = []
        for var in varCatList:
            for item in selVarIdList:
                if var["varid"] == item: break
            else: unselList.append(var)

        return unselList

    @staticmethod
    def getSiteSpecificVariableId(catid, varname):
        varid = -1

        for var in output.listOfSiteSpecificVariable:
            if var["catid"] == catid and var["varname"] == varname:
                varid = var["varid"]
                break

        return varid

    @staticmethod
    def getSiteSpecificVariableName(catid, varid):
        varname = ""

        for var in output.listOfSiteSpecificVariable:
            if var["catid"] == catid and var["varid"] == varid:
                varname = var["varname"]
                break

        return varname

    @staticmethod
    def getSiteSpecificVariable(catid, varid):
        var = None

        for item in output.listOfSiteSpecificVariable:
            if item["catid"] == catid and item["varid"] == varid:
                var = item
                break

        return var

    @staticmethod
    def getSiteSpecificVarCategoryId_VarId(varid):
        catId = ""
        for item in output.listOfSiteSpecificVariable:
            if item["varid"] == int(varid):
                catId = item["catid"]
                break
        return  catId

    @staticmethod
    def getSiteSpecificVarCategoryId(category):
        catId = ""

        for item in output.listOfSiteSpecificCategory:
            if item["catname"] == category:
                catId = item["catid"]
                break

        return catId

    @staticmethod
    def getSiteSpecificVarriableList(catid):
        varList = []
        for var in output.listOfSiteSpecificVariable:
            if var["catid"] == catid:
                varList.append(var)

        return varList

#functions for vegetable specific Daily variable list
    def addVariableToSelectedVegetationSpecificList_Daily_ByVarId(self, varid):
        catid = self.getVegetationSpecificVarCategoryId_VarId(varid)

        var = {"catid": catid, "varid": varid}
        self.listOfSelectedVegSpecificVariable_Daily.append(var)

    def addVariableToSelectedVegetationSpecificList_Daily_ByVarName(self, category, varname):
        catid = self.getVegetationSpecificVarCategoryId(category)
        varid = self.getVegetationSpecificVariableId(catid, varname)

        var = {"catid": catid, "varid": varid}
        self.listOfSelectedVegSpecificVariable_Daily.append(var)

    def removeVariableFromSelectedVegetationSpecificList_Daily_ByVarName(self, category, varname):
        catid = self.getVegetationSpecificVarCategoryId(category)
        varid = self.getVegetationSpecificVariableId(catid,varname)
        count = len(self.listOfSelectedVegSpecificVariable_Daily)

        for i in reversed(range(count)):
            if (self.listOfSelectedVegSpecificVariable_Daily[i].get('catid') == catid and
                self.listOfSelectedVegSpecificVariable_Daily[i].get('varid') == varid):
                self.listOfSelectedVegSpecificVariable_Daily.pop(i)

    def getSelectedVegetationSpecificVariableList_Daily(self, categoy):
        self.sortListOfSelectedVegSpecificVariable_Daily()
        catid = self.getVegetationSpecificVarCategoryId(categoy)

        listOfVariable = []

        for item in self.listOfSelectedVegSpecificVariable_Daily:
            if item["catid"] == catid:
                listOfVariable.append(self.getVegetationSpecificVariable(catid,item["varid"]))

        return listOfVariable

    def getAllSelectedVegetationSpecificVariableList(self, daily=False, annual=False):
        listOfVariable = []
        if daily:
            for item in self.listOfSelectedVegSpecificVariable_Daily:
                varid = item["varid"]
                catid = self.getVegetationSpecificVarCategoryId_VarId(varid)
                var = self.getVegetationSpecificVariable(catid, varid)
                var["catname"] = self.getVegetationSpecificCategoryName(catid)
                listOfVariable.append(var)
        if annual:
            for item in self.listOfSelectedVegSpecificVariable_Annual:
                varid = item["varid"]
                catid = self.getVegetationSpecificVarCategoryId_VarId(varid)
                var = self.getVegetationSpecificVariable(catid, varid)
                var["catname"] = self.getVegetationSpecificCategoryName(catid)
                listOfVariable.append(var)
        return listOfVariable

    def getUnselectedVegetationSpecificVariableList_Daily(self, category):
        catid = self.getVegetationSpecificVarCategoryId(category)

        selVarIdList = []
        for item in self.listOfSelectedVegSpecificVariable_Daily:
            if item["catid"] == catid:
                selVarIdList.append(item["varid"])

        varCatList = self.getVegetationSpecificVariableList(catid)

        unselList = []
        for var in varCatList:
            for item in selVarIdList:
                if var["varid"] == item: break
            else: unselList.append(var)

        return unselList

#functions for vegetable specific Annual variable list
    def addVariableToSelectedVegetationSpecificList_Annual_ByVarId(self, varid):
        catid = self.getVegetationSpecificVarCategoryId_VarId(varid)

        var = {"catid": catid, "varid": varid}
        self.listOfSelectedVegSpecificVariable_Annual.append(var)

    def addVariableToSelectedVegetationSpecificList_Annual_ByVarName(self, category, varname):
        catid = self.getVegetationSpecificVarCategoryId(category)
        varid = self.getVegetationSpecificVariableId(catid, varname)

        var = {"catid": catid, "varid": varid}
        self.listOfSelectedVegSpecificVariable_Annual.append(var)

    def removeVariableFromSelectedVegetationSpecificList_Annual_ByVarName(self, category, varname):
        catid = self.getVegetationSpecificVarCategoryId(category)
        varid = self.getVegetationSpecificVariableId(catid,varname)
        count = len(self.listOfSelectedVegSpecificVariable_Annual)

        for i in reversed(range(count)):
            if (self.listOfSelectedVegSpecificVariable_Annual[i].get('catid') == catid and
                self.listOfSelectedVegSpecificVariable_Annual[i].get('varid') == varid):
                self.listOfSelectedVegSpecificVariable_Annual.pop(i)

    def getSelectedVegetationSpecificVariableList_Annual(self, categoy):
        self.sortListOfSelectedVegSpecificVariable_Annual()
        catid = self.getVegetationSpecificVarCategoryId(categoy)

        listOfVariable = []

        for item in self.listOfSelectedVegSpecificVariable_Annual:
            if item["catid"] == catid:
                listOfVariable.append(self.getVegetationSpecificVariable(catid,item["varid"]))

        return listOfVariable

    def getUnselectedVegetationSpecificVariableList_Annual(self, category):
        catid = self.getVegetationSpecificVarCategoryId(category)

        selVarIdList = []
        for item in self.listOfSelectedVegSpecificVariable_Annual:
            if item["catid"] == catid:
                selVarIdList.append(item["varid"])

        varCatList = self.getVegetationSpecificVariableList(catid)

        unselList = []
        for var in varCatList:
            for item in selVarIdList:
                if var["varid"] == item: break
            else: unselList.append(var)

        return unselList

    @staticmethod
    def getVegetationSpecificVariableId(catid, varname):
        varid = -1

        for var in output.listOfVegSpecificVariable:
            if var["catid"] == catid and var["varname"] == varname:
                varid = var["varid"]
                break

        return varid

    @staticmethod
    def getVegetationSpecificVariableName(catid, varid):
        varname = ""

        for var in output.listOfVegSpecificVariable:
            if var["catid"] == catid and var["varid"] == varid:
                varname = var["varname"]
                break

        return varname

    @staticmethod
    def getVegetationSpecificVariable(catid, varid):
        var = None

        for item in output.listOfVegSpecificVariable:
            if item["catid"] == catid and item["varid"] == varid:
                var = item
                break

        return var

    @staticmethod
    def getVegetationSpecificVarCategoryId(category):
        catId = ""
        for item in output.listOfVegSpecificCategory:
            if item["catname"] == category:
                catId = item["catid"]
                break

        return  catId

    @staticmethod
    def getVegetationSpecificVarCategoryId_VarId(varid):
        catId = ""
        for item in output.listOfVegSpecificVariable:

            if item["varid"] == int(varid):

                catId = item["catid"]
                break
        return  catId

    @staticmethod
    def getVegetationSpecificVariableList(catid):
        varList = []
        for var in output.listOfVegSpecificVariable:
            if var["catid"] == catid:
                varList.append(var)

        return varList

