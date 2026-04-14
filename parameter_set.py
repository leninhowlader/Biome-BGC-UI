import file_io
import os
from parameter import *


class BiomeBGCParameterSet:
    def __init__(self):
        self.initParam = InitialParameter()
        self.gisParam = []                      #structure: [{"siteIndex": siteIndex, "gis": gisObject}, {}]
        self.vegParam = []                      #structure: [{"siteIndex": siteIndex, "vegid": vegetationNumber, "veg": vegObject}, {}]
        self.vegEpc = []                        #structure: [{"siteIndex": siteIndex, "vegid": vegetationNumber, "epcid": epcid}, {}]
        self.epcParam = []                      #structure: [{"epcid": epcid, "epc": epcObject, "updateFlag": True/False}, {}]

        #it is possible that different soil profile filenames can be used in gis file for different sites. At the same time,
        #because horizon files are managed separately, there can be situations that for multiple profile files only one
        #horizon file is used; or multiple horizon files can also be used. The situation becomes further complex, if
        #the same profile is listed in different profile files used. For this reason, a decision has been taken, if there
        #exists multiple soil profile files and/or horizon files in a single version, a new version of soil profile file and
        #horizon file will be created. On the other hand, if single soil profile file and a single horizon file is used
        #abd if the profiles are changed, only updated profiles will be written in the file.

        self.gisSoil = []                       #structure: [{"siteIndex": siteIndex, "spfid": soilProfileFileId}, {}]
        self.soilParam = []                     #structure: [{"spfid": soilProfileFileId, "sp": soilProfile}, {}]




        self.updatedSoilProfiles = []           #structure: [spfid, spfid2,...]


        #file name change flag
        self.fileNameChangeFlag = True          #if the flag is set False, file name will not be changed


        #change tracking flag
        self.updateFlag_gis = False
        self.updateFlag_veg = False
        self.updateFlag_soil = False

    @staticmethod
    def ReadBBGCParameterSet(modelDirectory, initialFilename):
        modelParam = None

        if initialFilename.find('/ini/') == -1: initialFilename = os.path.join(modelDirectory, 'ini', initialFilename)

        initParam = file_io.FileReadWrite.readInitialFile(initialFilename)
        if initParam is not None:
            #reading gis file
            gisParam = []
            filename = modelDirectory + "/" + initParam.gis_file_name
            gisList = file_io.FileReadWrite.readGisFile(filename)
            for gis in gisList:
                gisItem = {"siteIndex": gis.siteIndex, "gis": gis}
                gisParam.append(gisItem)

            if len(gisParam) > 0:
                #reading veg files and epc files
                vegParam = []
                filename = modelDirectory + "/" + initParam.veg_file_name
                vegList = file_io.FileReadWrite.readVegFile(filename)

                vegEpc = []             #structure: [{"siteIndex": siteIndex, "epcid": epcid}, {}]
                epcParam = []           #structure: [{"epcid": epcid, "epc": epcObject}, {}]
                temp = []               #structure: [{"epcid": epcid, "fileName": epcFileName}, {}]
                epcid = 0

                for veg in vegList:
                    vegItem = {"siteIndex": veg.siteIndex, "vegid": veg.vegetationNumber, "veg": veg}
                    vegParam.append(vegItem)

                    #because epc parameters were separated from initial parameter in order to
                    #allow using the same epc for different sites, here all distinct epc objects
                    #will be stored in dictionary and an array of index is used to maintain
                    #the relation between site and epc object.

                    for i in range(len(temp)):
                        if temp[i]["fileName"] == veg.epcFileName: break
                    else:
                        epcid += 1
                        epcFileNameItem = {"epcid": epcid, "fileName": veg.epcFileName}
                        temp.append(epcFileNameItem)

                    vegEpcItem = {"siteIndex": veg.siteIndex, "vegid": veg.vegetationNumber, "epcid": epcid}
                    vegEpc.append(vegEpcItem)

                for epcFileNameItem in temp:
                    filename = modelDirectory + "/epc/" + epcFileNameItem["fileName"]
                    epc = file_io.FileReadWrite.readEpcFile(filename)
                    epcItem = {"epcid": epcFileNameItem["epcid"], "epc": epc, "updateFlag": False}
                    epcParam.append(epcItem)

                #read soil profile files and soil horizon files
                temp = []   #structure: [{"siteIndex": profileFileId, "pFileName": profileFileName, "hFileName": horizonFileName,
                                        # "profileName": profileName},{}]
                gisSoil = []
                soilParam = []
                for gpo in gisParam:
                    for i in range(len(temp)):
                        if temp[i]["siteIndex"] == gpo["gis"].siteIndex: break
                    else:
                        gis = gpo["gis"]
                        soilFileItem = {"siteIndex": gis.siteIndex, "pFileName": gis.soilProfileFileName,
                                               "hFileName": gis.soilHorizonFileName, "profileName": gis.profileName}
                        temp.append(soilFileItem)

                if len(temp) > 0:
                    spfid = 0
                    for sp in temp:
                        profileList = file_io.FileReadWrite.readSoilProfile(modelDirectory + "/soil/" + sp["pFileName"],
                                                                        modelDirectory + "/soil/" + sp["hFileName"])
                        for profile in profileList:
                            if profile.profileName == sp["profileName"]:
                                spfid += 1
                                gisSoilItem = {"siteIndex": sp["siteIndex"], "spfid": spfid}
                                gisSoil.append(gisSoilItem)

                                soilParamItem = {"spfid": spfid, "sp": profile}
                                soilParam.append(soilParamItem)

                if (len(vegParam) > 0 and len(vegEpc) > 0 and len(epcParam) > 0 and
                    len(gisSoil) > 0 and len(soilParam) > 0):
                    modelParam = BiomeBGCParameterSet()
                    modelParam.initParam = initParam
                    modelParam.gisParam = gisParam
                    modelParam.vegParam = vegParam
                    modelParam.vegEpc = vegEpc
                    modelParam.epcParam = epcParam
                    modelParam.gisSoil = gisSoil
                    modelParam.soilParam = soilParam

        return modelParam

    def getSiteIndexList(self):
        index_list = []
        for g in self.gisParam: index_list.append(g['siteIndex'])
        return index_list

    def getVegNoList(self, site_index):
        vegid_list = []
        for v in self.vegParam:
            if v['siteIndex'] == site_index: vegid_list.append(v['vegid'])
        return vegid_list

    def getProfileName(self, site_index):
        for g in self.gisParam:
            if g['siteIndex'] == site_index:
                return g['gis'].profileName
        return None

    def getHorizonNameList(self, site_index):
        horizon_list = []

        sp = self.findSoilProfile(site_index)
        if sp:
            for l in sp.soilLayerList:
                horizon_list.append(l.horizonName)

        return horizon_list

    def getSoilProfileList(self):
        soilProfileList = []
        for sp in self.soilParam:
            for profile in soilProfileList:
                if profile.profileName == sp["sp"].profileName: break
            else: soilProfileList.append(sp["sp"])

        return soilProfileList

    #find soil profile
    def findSoilProfile(self, siteIndex):
        spfid = -1
        for gs in self.gisSoil:
            if gs["siteIndex"] == siteIndex:
                spfid = gs["spfid"]

        profile = None
        if spfid != -1:
            for sp in self.soilParam:
                if sp["spfid"] == spfid:
                    profile = sp["sp"]

        return profile
    #get list of soilprofile filename(s)
    def getSoilProfileFilenames(self):
        soilProfileFilenameList = []
        for gpo in self.gisParam:
            if gpo["gis"].soilProfileFileName in soilProfileFilenameList: break
        else: soilProfileFilenameList.append(gpo["gis"].soilProfileFileName)

        return soilProfileFilenameList

    #get list of soil horizon filename(s)
    def getSoilHorizonFilenames(self):
        soilHorizonFilenameList = []
        for gpo in self.gisParam:
            if gpo["gis"].soilHorizonFileName in soilHorizonFilenameList: break
        else: soilHorizonFilenameList.append(gpo["gis"].soilHorizonFileName)

        return soilHorizonFilenameList

    #update soil profile
    def updateSoilProfile(self, siteIndex, parameterName, parameterValue, layerIndex, versionText = "", tailReplace = False):
        result = None
        profile = self.findSoilProfile(siteIndex)

        if parameterName == "Profile Name":
            if profile.profileName != parameterValue:
                profile.profileName = parameterValue
                self.updateFlag_soil = True
                #update inside gis file
                self.updateGisObject(siteIndex, parameterName, parameterValue, versionText, tailReplace)
        else:
            if layerIndex > -1:
                layer = profile.soilLayerList[layerIndex]
                if parameterName in ["Horizon Name", "Lower Horizon Border", "Layer Thickness","Correction Factor"]:
                    result = layer.setParameterValue(parameterName, parameterValue)
                else:
                    #search each profile to find the horizons with same name
                    horizonName = layer.horizonName
                    for spo in self.soilParam:
                        for l in spo["sp"].soilLayerList:
                            if l.horizonName == horizonName:
                                result = l.setParameterValue(parameterName, parameterValue)
                                if result is not None: break
                if result is None:
                    self.updateFlag_soil = True
                    if len(versionText) > 0:
                        # #change soil profile filename and soil horizon filename
                        # self.updateSoilProfileFilename(versionText, tailReplace)

                        #updating gis filename in init file
                        self.updateGisfilename(versionText, tailReplace)
        return result


    #find gis parameter object using index
    def findGisObject(self, siteIndex):
        for gpo in self.gisParam:
            if gpo["siteIndex"] == siteIndex: return gpo["gis"]
        else: return None

    #find veg parameter object using indices
    def findVegObject(self, siteIndex, vegid):
        for vpo in self.vegParam:
            if vpo["siteIndex"] == siteIndex and vpo["vegid"] == vegid: return vpo["veg"]
        else: return None

    #find epc parameter object using indices
    def findEpcObject_indices(self, siteIndex, vegid):
        epcid = -1
        for ve in self.vegEpc:
            if ve["siteIndex"] == siteIndex and ve["vegid"] == vegid:
                epcid = ve["epcid"]
                break
        if epcid > -1:
            for epo in self.epcParam:
                if epo["epcid"] == epcid: return epo["epc"]
            else: return None
        else: return None

    #find epc parameter object using filename
    def findEpcObject_filename(self, filename):
        for vpo in self.vegParam:
            if vpo["veg"].epcFileName == filename:
                siteIndex = vpo["siteIndex"]
                vegid = vpo["vegid"]
                return self.findEpcObject_indices(siteIndex, vegid)
        else: return None

    def findEpcSiteIndexAndVegid_filename(self, filename):
        item = {}
        for vpo in self.vegParam:
            if vpo["veg"].epcFileName == filename:
                item["siteIndex"] = vpo["siteIndex"]
                item["vegid"] = vpo["vegid"]
                break
        return item

    def findUpdatedEpcFiles(self):
        updateFileList = []

        for epo in self.epcParam:
            if epo["updateFlag"] == True:
                epcid = epo["epcid"]
                for ve in self.vegEpc:
                    if ve["epcid"] == epcid:
                        siteIndex = ve["siteIndex"]
                        vegid = ve["vegid"]
                        vegObject = self.findVegObject(siteIndex, vegid)
                        if vegObject.epcFileName not in updateFileList:
                            updateFileList.append(vegObject.epcFileName)

        return updateFileList

    def findEpcUpdateFlag(self, siteIndex, vegid):
        epcid = -1
        for ve in self.vegEpc:
            if ve["siteIndex"] == siteIndex and ve["vegid"] == vegid:
                epcid = ve["epcid"]
                break

        for epo in self.epcParam:
            if epo["epcid"] == epcid:
                return epo["updateFlag"]
        return None

    def setEpcUpdateFlag(self, siteIndex, vegid, flag):
        epcid = -1
        for ve in self.vegEpc:
            if ve["siteIndex"] == siteIndex and ve["vegid"] == vegid:
                epcid = ve["epcid"]
                break
        for epo in self.epcParam:
            if epo["epcid"] == epcid:
                epo["updateFlag"] = flag

    def resetEpcUpdateFlag(self):
        for epo in self.epcParam:
            epo["updateFlag"] = False

    def resetAllUpdateFlag(self):
        self.updateFlag_gis = False
        self.updateFlag_veg = False
        self.updateFlag_soil = False
        self.resetEpcUpdateFlag()

    def updateGisObject(self, siteIndex, parameterName, parameterValue, versionText = "", tailReplace = False):
        result = None
        gis = self.findGisObject(siteIndex)

        if gis is not None:
            result = gis.setParameterValue(parameterName, parameterValue)
            if result is None:
                #update profile object if the profileName is changed inside the gis object
                if parameterName == "Profile Name":
                    self.updateSoilProfile(siteIndex, parameterName, parameterValue, -1, versionText, tailReplace)
                elif parameterName == "Site Index":
                    counter = 0
                    for vpo in self.vegParam:
                        if vpo["siteIndex"] == siteIndex:
                            vpo["veg"].siteIndex = parameterValue
                            vpo["siteIndex"] = parameterValue
                            counter += 1
                    if counter > 0: self.updateVegFilename(versionText, tailReplace)

                    for ve in self.vegEpc:
                        if ve["siteIndex"] == siteIndex:
                            ve["siteIndex"] = parameterValue

                    for gs in self.gisSoil:
                        if gs["siteIndex"] == siteIndex:
                            gs["siteIndex"] = parameterValue

                    for gpo in self.gisParam:
                        if gpo["siteIndex"] == siteIndex:
                            gpo["siteIndex"] = parameterValue

                if len(versionText) > 0:
                    # self.isModified = True
                    #update gis filename in initial file
                    self.updateGisfilename(versionText, tailReplace)
        return result

    #update veg object
    def updateVegObject(self, siteIndex, vegid, parameterName, parameterValue, versionText = "", tailReplace = False):
        result = None
        veg = self.findVegObject(siteIndex, vegid)
        if veg is not None:
            result = veg.setParameterValue(parameterName, parameterValue)
            if result is None:
                if parameterName == "Site Index":
                    counter = 0
                    for gpo in self.gisParam:
                        if gpo["siteIndex"] == siteIndex:
                            gpo["gis"].siteIndex = parameterValue
                            gpo["siteIndex"] = parameterValue
                            counter += 1
                    if counter > 0: self.updateGisfilename(versionText, tailReplace)

                    for vpo in self.vegParam:
                        if vpo["siteIndex"] == siteIndex:
                            vpo["veg"].siteIndex = parameterValue
                            vpo["siteIndex"] = parameterValue

                    for ve in self.vegEpc:
                        if ve["siteIndex"] == siteIndex:
                            ve["siteIndex"] = parameterValue

                    for gs in self.gisSoil:
                        if gs["siteIndex"] == siteIndex:
                            gs["siteIndex"] = parameterValue
                elif parameterName == "Vegetation No.":
                    for vpo in self.vegParam:
                        if vpo["siteIndex"] == siteIndex and vpo["vegid"] == vegid:
                            vpo["vegid"] == int(parameterValue)

                    for ve in self.vegEpc:
                        if ve["siteIndex"] == siteIndex and ve["vegid"] == vegid:
                            ve["vegid"] == int(parameterValue)

                if len(versionText) > 0:
                    # self.isModified = True
                    #update veg filename in initial file
                    self.updateVegFilename(versionText, tailReplace)

    #update epc object
    def updateEpcObject(self, siteIndex, vegid, parameterNumber, parameterName, parameterValue,
                        versionText = "", tailReplace = False):
        result = None
        epc = self.findEpcObject_indices(siteIndex, vegid)
        if epc is not None:
            result = epc.setParameterValue(parameterNumber, parameterName, parameterValue)
            if result is None:
                # self.isModified = True
                if versionText != "":
                    #update epc file name in vegetation file
                    self.updateEpcFilename(siteIndex, vegid, versionText, tailReplace)
                    #update vegetation filename in initial file
                    self.updateVegFilename(versionText, tailReplace)
        return result

    def updateGisfilename(self, versionText, tailReplace):
        if self.fileNameChangeFlag:
            if not self.updateFlag_gis:
                gisFileName = self.initParam.gis_file_name.replace(".TXT", ".txt")
                if tailReplace:
                    temp = gisFileName.split("_")[-1]
                    gisFileName = gisFileName.replace(temp, versionText + ".txt")
                else:
                    gisFileName = gisFileName.replace(".txt", "_" + versionText + ".txt")

                self.initParam.gis_file_name = gisFileName
                self.updateFlag_gis = True

    def updateVegFilename(self, versionText, tailReplace):
        if self.fileNameChangeFlag:
            if not self.updateFlag_veg:
                vegFileName = self.initParam.veg_file_name.replace(".TXT", ".txt")
                if tailReplace:
                    temp = vegFileName.split("_")[-1]
                    vegFileName = vegFileName.replace(temp, versionText + ".txt")
                else:
                    vegFileName = vegFileName.replace(".txt", "_" + versionText + ".txt")

                self.initParam.veg_file_name = vegFileName
                self.updateFlag_veg = True

    def updateEpcFilename(self, siteIndex, vegid, versionText, tailReplace):
        if self.fileNameChangeFlag:
            updateFlag = self.findEpcUpdateFlag(siteIndex, vegid)
            if updateFlag == False:
                veg = self.findVegObject(siteIndex, vegid)
                epcFileName = veg.epcFileName.replace(".EPC", ".epc")
                # versionText += "_" + str(vegid).rjust(2,"0")
                if tailReplace:
                    temp = epcFileName.split("_")
                    repText = ""
                    if len(temp[-1]) > 0:
                        repText = temp[-1]
                        if len(temp[-2]) == 2:
                            repText = temp[-2] + "_" + temp[-1]
                    epcFileName = epcFileName.replace(repText, versionText + ".epc")
                else:
                    epcFileName = epcFileName.replace(".epc", "_" + versionText + ".epc")

                veg.epcFileName = epcFileName
                self.setEpcUpdateFlag(siteIndex, vegid, True)
                # if epcFileName not in self.updatedEpcFiles: self.updatedEpcFiles.append(epcFileName)

    def updateSoilProfileAndHorizonFileNameInGISObjects(self, profileFilename = "", horizonFilename = ""):
        if len(profileFilename) > 0:
            for gpo in self.gisParam:
                gpo["gis"].soilProfileFileName = profileFilename

        if len(horizonFilename) > 0:
            for gpo in self.gisParam:
                gpo["gis"].soilHorizonFileName = horizonFilename

    def updateSoilProfileFilename(self, versionText, tailReplace):
        if self.fileNameChangeFlag:
            #reading file names
            soilProfileFilename = ""
            soilHorizonFilename = ""

            for gpo in self.gisParam:
                if len(soilProfileFilename) == 0: soilProfileFilename = gpo["gis"].soilProfileFileName
                if len(soilHorizonFilename) == 0: soilHorizonFilename = gpo["gis"].soilHorizonFileName

                if len(soilHorizonFilename) > 0 and len(soilProfileFilename) > 0: break

            #changing file names
            if tailReplace:
                temp = soilProfileFilename.split("_")[-1]
                soilProfileFilename = soilProfileFilename.replace(temp, versionText + ".txt")

                temp = soilHorizonFilename.split("_")[-1]
                soilHorizonFilename = soilHorizonFilename.replace(temp, versionText + ".txt")
            else:
                soilProfileFilename = soilProfileFilename.replace(".txt", "_" + versionText + ".txt")
                soilHorizonFilename = soilHorizonFilename.replace(".txt", "_" + versionText + ".txt")

            #updating filenames in gis objects
            for gpo in self.gisParam:
                gpo["gis"].soilProfileFileName = soilProfileFilename
                gpo["gis"].soilHorizonFileName = soilHorizonFilename

            #updating gis filename in init file
            self.updateGisfilename(versionText, tailReplace)

    #find all linked filenames
    def findLinkedFiles(self):
        linkedFileList = []             #structure: [{"fileType": "Initial File", "fileName": ini_90_09.ini}, {}]
        item = {"type": "GIS Parameter", "fileName": self.initParam.gis_file_name}
        linkedFileList.append(item)
        item = {"type": "VEG Parameter", "fileName": self.initParam.veg_file_name}
        linkedFileList.append(item)
        item = {"type": "Restart File", "fileName": self.initParam.restart_read_file_name}
        linkedFileList.append(item)
        item = {"type": "CO2 Datafile", "fileName": self.initParam.carbon_file}
        linkedFileList.append(item)

        #soil profile
        profileFileList = self.getSoilProfileFilenames()
        if len(profileFileList) > 1:
            item = {"type": "Soil Profile", "fileName": "(Multiple files exist)"}
            linkedFileList.append(item)

        elif len(profileFileList) == 1:
            item = {"type": "Soil Profile", "fileName": profileFileList[0]}
            linkedFileList.append(item)

        horizonFileList = self.getSoilHorizonFilenames()
        if len(horizonFileList) > 1:
            item = {"type": "Soil Horizon", "fileName": "(Multiple files exist)"}
            linkedFileList.append(item)
        elif len(horizonFileList) == 1:
            item = {"type": "Soil Horizon", "fileName": horizonFileList[0]}
            linkedFileList.append(item)

        #met file
        distinctList = []
        for gis in self.gisParam:
            temp = gis["gis"].meteorologicalFileName
            if temp not in distinctList:
                distinctList.append(temp)

        for metfile in distinctList:
            item = {"type": "MET File", "fileName": metfile}
            linkedFileList.append(item)

        #ndep file
        distinctList = []
        for gis in self.gisParam:
            temp = gis["gis"].ndepFileName
            if temp not in distinctList:
                distinctList.append(temp)

        for ndepFile in distinctList:
            item = {"type": "NDEP File", "fileName": ndepFile}
            linkedFileList.append(item)

        #epc files
        distinctList = []
        for veg in self.vegParam:
            temp = veg["veg"].epcFileName
            if temp not in distinctList:
                distinctList.append(temp)

        for epcFile in distinctList:
            item = {"type": "EPC Parameter", "fileName": epcFile}
            linkedFileList.append(item)

        #ss file
        distinctList = []
        for veg in self.vegParam:
            temp = veg["veg"].speciesSeqFile
            if temp not in distinctList:
                distinctList.append(temp)

        for ssFile in distinctList:
            item = {"type": "SS File", "fileName": ssFile}
            linkedFileList.append(item)

        #harvest file
        distinctList = []
        for epc in self.epcParam:
            temp = epc["epc"].thinningRuleFileName
            if temp not in distinctList:
                distinctList.append(temp)

        for harvest in distinctList:
            item = {"type": "HAR Parameter", "fileName": harvest}
            linkedFileList.append(item)

        return linkedFileList

    # @staticmethod
    # def ReadModelParameter(initialFilename, modelDirectory):
    #     modelParameter = None
    #
    #     initParam = DatabaseReadWrite.readInitialFile(initialFilename)
    #     if initParam is not None:
    #         #reading gis file
    #         gisParam = []
    #         filename = modelDirectory + "/" + initParam.gis_file_name
    #         gisList = DatabaseReadWrite.readGisFile(filename)
    #         for gis in gisList:
    #             gisItem = {"siteIndex": gis.siteIndex, "gis": gis}
    #             gisParam.append(gisItem)
    #
    #         if len(gisParam) > 0:
    #             #reading veg files and epc files
    #             vegParam = []
    #             filename = modelDirectory + "/" + initParam.veg_file_name
    #             vegList = DatabaseReadWrite.readVegFile(filename)
    #
    #             vegEpc = []             #structure: [{"siteIndex": siteIndex, "epcid": epcid}, {}]
    #             epcParam = []           #structure: [{"epcid": epcid, "epc": epcObject}, {}]
    #             temp = []               #structure: [{"epcid": epcid, "fileName": epcFileName}, {}]
    #             epcid = 0
    #
    #             for veg in vegList:
    #                 vegItem = {"siteIndex": veg.siteIndex, "vegid": veg.vegetationNumber, "veg": veg}
    #                 vegParam.append(vegItem)
    #
    #                 #because epc parameters were separated from initial parameter in order to
    #                 #allow using the same epc for different sites, here all distinct epc objects
    #                 #will be stored in dictionary and an array of index is used to maintain
    #                 #the relation between site and epc object.
    #
    #                 for i in range(len(temp)):
    #                     if temp[i]["fileName"] == veg.epcFileName: break
    #                 else:
    #                     epcid += 1
    #                     epcFileNameItem = {"epcid": epcid, "fileName": veg.epcFileName}
    #                     temp.append(epcFileNameItem)
    #
    #                 vegEpcItem = {"siteIndex": veg.siteIndex, "vegid": veg.vegetationNumber, "epcid": epcid}
    #                 vegEpc.append(vegEpcItem)
    #
    #             for epcFileNameItem in temp:
    #                 filename = modelDirectory + "/epc/" + epcFileNameItem["fileName"]
    #                 epc = DatabaseReadWrite.readEpcFile(filename)
    #                 epcItem = {"epcid": epcFileNameItem["epcid"], "epc": epc}
    #                 epcParam.append(epcItem)
    #
    #             #read soil profile files and soil horizon files
    #             temp = []   #structure: [{"siteIndex": profileFileId, "pFileName": profileFileName, "hFileName": horizonFileName,
    #                                     # "profileName": profileName},{}]
    #             gisSoil = []
    #             soilParam = []
    #             for gpo in gisParam:
    #                 for i in range(len(temp)):
    #                     if temp[i]["siteIndex"] == gpo["gis"].siteIndex: break
    #                 else:
    #                     gis = gpo["gis"]
    #                     soilFileItem = {"siteIndex": gis.siteIndex, "pFileName": gis.soilProfileFileName,
    #                                            "hFileName": gis.soilHorizonFileName, "profileName": gis.profileName}
    #                     temp.append(soilFileItem)
    #
    #             if len(temp) > 0:
    #                 spfid = 0
    #                 for sp in temp:
    #                     profileList = DatabaseReadWrite.readSoilProfile(sp["pFileName"], sp["hFileName"])
    #                     for profile in profileList:
    #                         if profile.profileName == sp["profileName"]:
    #                             spfid += 1
    #                             gisSoilItem = {"siteIndex": sp["siteIndex"], "spfid": spfid}
    #                             gisSoil.append(gisSoilItem)
    #
    #                             soilParamItem = {"spfid": soilFileItem["spfid"], "sp": profile}
    #                             soilParam.append(soilParamItem)
    #
    #             if (len(vegParam) > 0 and len(vegEpc) > 0 and len(epcParam) > 0 and
    #                 len(gisSoil) > 0 and len(soilParam) > 0):
    #                 modelParam = ModelParameter()
    #                 modelParam.initParam = initParam
    #                 modelParam.gisParam = gisParam
    #                 modelParam.vegParam = vegParam
    #                 modelParam.vegEpc = vegEpc
    #                 modelParam.epcParam = epcParam
    #                 modelParam.gisSoil = gisSoil
    #                 modelParam.soilParam = soilParam
    #
    #     return modelParam

    @staticmethod
    def versionComparison(listOfModelParam, listOfVersion):
        #listOfModelParam contains the different version of model parameters while
        #listOfVersion contain concerning version numbers. Both the list should have
        #same length.
        compResult = []         #compResult [[header, {param1: [val1, val2,..], param2: [val1, val2..],..}],[]..]
        if len(listOfModelParam) == len(listOfVersion):
            versionCount = len(listOfModelParam)

            #comparing parameters in initial file
            paramCount = len(InitialParameter.paramLabelList)
            paramList = InitialParameter.paramLabelList

            groupTitle = "Init file"
            groupResult = {}
            for i in range(paramCount):
                paramName = paramList[i]
                paramValueList = []
                firstValue = listOfModelParam[0].initParam.getParameterValue(paramName)
                paramValueList.append(firstValue)

                found = False
                for j in range(1, versionCount):
                    value = listOfModelParam[j].initParam.getParameterValue(paramName)
                    if value != firstValue: found = True
                    paramValueList.append(value)
                if found:
                    groupResult[paramName] = paramValueList
            if len(groupResult) > 0:
                compResult.append([groupTitle, groupResult])

            #compare gis parameters
            #step-01: Find gis objects in first version
            #step-02: find if gis object is present in other versions; if gis object for a site is not present in another
            #version, the comparison will be made only among those version where the gis object for the same site was
            #found. If there is no gis object found in other version for the same site, skip comparison; a line should be
            #appear in the table showing that this gis object doesn't found in other versions.
            #step-03: If two or more gis objects for same site are found, compare the objects.

            gisCluster = []         #structure: [[gisVer01site1, gisVer02site1, gisVer03site1...],[],..]

            #finding all site indices
            siteIndexList = []
            for i in range(versionCount):
                gisParam = listOfModelParam[i].gisParam
                for j in range(len(gisParam)):
                    siteIndex = gisParam[j]["siteIndex"]
                    if siteIndex not in siteIndexList: siteIndexList.append(siteIndex)

            #creating gis cluster or groups
            for i in range(len(siteIndexList)):
                siteIndex = siteIndexList[i]
                for j in range(versionCount):
                    gisParam = listOfModelParam[j].gisParam
                    for gpo in gisParam:
                        gis = None
                        if gpo["siteIndex"] == siteIndex: gis = gpo["gis"]
                        if len(gisCluster) > i:
                            gisCluster[i].append(gis)
                        else:
                            gisCluster.append([gis])

            #processing each group
            paramCount = len(GisParameter.paramLabelList)
            paramList = GisParameter.paramLabelList
            for i in range(len(siteIndexList)):
                gisGroup = gisCluster[i]
                groupTitle = "Gis (" + str(siteIndexList[i]) + ")"
                groupResult = {}
                for j in range(paramCount):
                    paramName = paramList[j]
                    paramValueList = []
                    found = False
                    for k in range(len(gisGroup)):
                        if gisGroup[k] is None: paramValueList.append("NA")
                        else: paramValueList.append(gisGroup[k].getParameterValue(paramName))

                    for k in range(len(paramValueList) - 1):
                        if paramValueList[k] != paramValueList[k + 1]:
                            found = True
                            break
                    if found:
                        groupResult[paramName] = paramValueList
                if len(groupResult) > 0: compResult.append([groupTitle, groupResult])

            #comparing vegetation object
            #creating cluster of veg objects
            vegCluster = []     #structure: [[veg1, veg2..], [], ..]

            #creating distinct list for all veg object in all versions
            vegIdList = []   #structure: [[siteIndex, vegNumber],[],,]
            for i in range(versionCount):
                vegParam = listOfModelParam[i].vegParam
                for vpo in vegParam:
                    for j in range(len(vegIdList)):
                        if vpo["siteIndex"] == vegIdList[j][0] and vpo["vegid"] == vegIdList[j][1]: break
                    else:
                        vegIdList.append([vpo["siteIndex"], vpo["vegid"]])

            #creating veg groups
            for i in range(len(vegIdList)):     #vilItem = vegIdListItem
                siteIndex = vegIdList[i][0]
                vegid = vegIdList[i][1]
                for j in range(versionCount):
                    vegParam = listOfModelParam[j].vegParam
                    veg = None
                    for vpo in vegParam:
                        if vpo["siteIndex"] == siteIndex and vpo["vegid"] == vegid:
                            veg = vpo["veg"]
                    if len(vegCluster) > i: vegCluster[i].append(veg)
                    else: vegCluster.append([veg])

            #processing each group
            paramCount = len(VegetationParameter.paramLabelList)
            paramList = VegetationParameter.paramLabelList
            for i in range(len(vegIdList)):
                vegGroup = vegCluster[i]
                groupTitle = "Veg (" + str(vegIdList[i][0]) + ":" + str(vegIdList[i][1]) + ")"
                groupResult = {}
                for j in range(paramCount):
                    paramName = paramList[j]
                    paramValueList = []
                    found = False
                    for k in range(len(vegGroup)):
                        if vegGroup[k] is None: paramValueList.append("NA")
                        else: paramValueList.append(vegGroup[k].getParameterValue(paramName))

                    for k in range(len(paramValueList) - 1):
                        if paramValueList[k] != paramValueList[k + 1]:
                            found = True
                            break
                    if found:
                        groupResult[paramName] = paramValueList
                if len(groupResult) > 0: compResult.append([groupTitle, groupResult])

            #comparing epc parameters

            epcCluster = []     #structure: [[veg1, veg2..], [], ..]
            #creating epc groups
            for i in range(len(vegIdList)):     #vilItem = vegIdListItem
                siteIndex = vegIdList[i][0]
                vegid = vegIdList[i][1]
                for j in range(versionCount):
                    epc = listOfModelParam[j].findEpcObject_indices(siteIndex, vegid)
                    if len(epcCluster) > i: epcCluster[i].append(epc)
                    else: epcCluster.append([epc])

            #processing each group
            paramCount = len(EpcParameter.paramLabelList)
            paramList = EpcParameter.paramLabelList
            for i in range(len(vegIdList)):
                epcGroup = epcCluster[i]
                groupTitle = "Epc (" + str(vegIdList[i][0]) + ":" + str(vegIdList[i][1]) + ")"
                groupResult = {}
                for j in range(paramCount):
                    paramName = paramList[j]
                    paramValueList = []
                    found = False
                    for k in range(len(epcGroup)):
                        if epcGroup[k] is None: paramValueList.append("NA")
                        else: paramValueList.append(epcGroup[k].getParameterValue(paramName))

                    for k in range(len(paramValueList) - 1):
                        if paramValueList[k] != paramValueList[k + 1]:
                            found = True
                            break
                    if found:
                        groupResult[paramName] = paramValueList
                if len(groupResult) > 0: compResult.append([groupTitle, groupResult])

            #comparing soil parameters
            #get unique profile names
            profileLayerNameList = [] #structure: [[siteIndex, profileName, profileLayerName],[],,]

            for i in range(versionCount):
                for siteIndex in siteIndexList:
                    profile = listOfModelParam[i].findSoilProfile(siteIndex)
                    if profile is not None:
                        for layer in profile.soilLayerList:
                            for j in range(len(profileLayerNameList)):
                                if (profileLayerNameList[j][0] == siteIndex and profileLayerNameList[j][1] == profile.profileName
                                    and profileLayerNameList[j][2] == layer.horizonName): break
                            else:
                                profileLayerNameList.append([siteIndex, profile.profileName, layer.horizonName])

            #creating soil profile groups
            soilLayerCluster = []   #structure: [[profileLayer1, profileLayer2,..],[]..]

            for i in range(len(profileLayerNameList)):
                siteIndex = profileLayerNameList[i][0]
                profileName = profileLayerNameList[i][1]
                layerName = profileLayerNameList[i][2]
                for j in range(versionCount):
                    profile = listOfModelParam[j].findSoilProfile(siteIndex)
                    layer = None
                    if profile is not None and profile.profileName == profileName:
                        for lr in profile.soilLayerList:
                            if lr.horizonName == layerName:
                                layer = lr
                                break
                    if len(soilLayerCluster) > i: soilLayerCluster[i].append(layer)
                    else: soilLayerCluster.append([layer])

            paramList = SoilLayer.paramLabelList
            paramCount = len(paramList)
            for i in range(len(profileLayerNameList)):
                layerGroup = soilLayerCluster[i]
                groupTitle = ("Soil [" + str(profileLayerNameList[i][0]) + "(S):" + str(profileLayerNameList[i][1]) +
                              "(P):" + str(profileLayerNameList[i][2]) + "(H)]")
                groupResult = {}
                for j in range(paramCount):
                    paramName = paramList[j]
                    paramValueList = []
                    found = False
                    for k in range(len(layerGroup)):
                        if layerGroup[k] is None: paramValueList.append("NA")
                        else: paramValueList.append(layerGroup[k].getParameterValue(paramName))

                    for k in range(len(paramValueList) - 1):
                        if paramValueList[k] != paramValueList[k + 1]:
                            found = True
                            break
                    if found:
                        groupResult[paramName] = paramValueList
                if len(groupResult) > 0: compResult.append([groupTitle, groupResult])

        return compResult

    @staticmethod
    def save_parameter_set(modelParam, modelDirectory, initialFileName, version_text):
        versionSaveResult = True

        #saving epc file(s)
        updatedEpcFileList = modelParam.findUpdatedEpcFiles()
        if len(updatedEpcFileList) > 0:
            for fileName in updatedEpcFileList:
                epc = modelParam.findEpcObject_filename(fileName)

                #saving epc file
                epcFileName = modelDirectory + "/epc/" + fileName
                versionSaveResult = file_io.FileReadWrite.writeEpcFile(epcFileName, epc)

            if versionSaveResult: modelParam.resetEpcUpdateFlag()

        #saving veg file
        if versionSaveResult:
            if modelParam.updateFlag_veg:
                vegFileName = modelParam.initParam.veg_file_name

                vegList = []
                for veg in modelParam.vegParam:
                    vegList.append(veg["veg"])

                versionSaveResult = file_io.FileReadWrite.writeVegFile(modelDirectory + "/" + vegFileName, vegList)

                if versionSaveResult: modelParam.updateFlag_veg = False

        #saving soil files
        if versionSaveResult:
            if modelParam.updateFlag_soil:
                profileList = modelParam.getSoilProfileList()
                profileFileName = ""
                horizonFileName = ""

                fileName = modelParam.getSoilProfileFilenames()
                if len(fileName) == 1:
                    profileFileName = fileName[0]
                elif len(fileName) > 1:
                    profileFileName = fileName[0].replace(".txt", "_" + version_text + ".txt")
                    modelParam.updateSoilProfileAndHorizonFileNameInGISObjects(profileFilename=profileFileName)

                fileName = modelParam.getSoilHorizonFilenames()
                if len(fileName) == 1:
                    horizonFileName = fileName[0]
                elif len(fileName) > 1:
                    horizonFileName = fileName[0].replace(".txt", "_" + version_text + ".txt")
                    modelParam.updateSoilProfileAndHorizonFileNameInGISObjects(horizonFilename=horizonFileName)

                if len(profileList) > 0 and len(profileFileName) > 0 and len(horizonFileName) > 0:
                    profileFileName = modelDirectory + "/soil/" + profileFileName
                    horizonFileName = modelDirectory + "/soil/" + horizonFileName
                    versionSaveResult = file_io.FileReadWrite.writeSoilProfile(profileList, profileFileName, horizonFileName)

                if versionSaveResult: modelParam.updateFlag_soil = False

        #saving gis file
        if versionSaveResult:
            if modelParam.updateFlag_gis:
                gisFileName = modelParam.initParam.gis_file_name

                gisList = []
                for gis in modelParam.gisParam:
                    gisList.append(gis["gis"])
                versionSaveResult = file_io.FileReadWrite.writeGisFile(modelDirectory + "/" + gisFileName, gisList)

                if versionSaveResult: modelParam.updateFlag_gis = False

        #saving init file
        if versionSaveResult:
            if initialFileName.find('/ini/') == -1: initialFileName = os.path.join(modelDirectory, 'ini', initialFileName)
            versionSaveResult = file_io.FileReadWrite.writeInitialFile(modelParam.initParam, initialFileName)

        return versionSaveResult

class input_package:

    @staticmethod
    def check_input_file_linkage(model_directory, initial_file):
        result = [] #item=[file_type, address, file_exist, validity]

        if os.path.exists(model_directory):
            #initial file
            file_type = "Initial File"
            address = initial_file
            file_exist = os.path.exists(address)
            validity = False
            if not file_exist:
                item = [file_type, address, file_exist, validity]
                result.append(item)

            else:
                init_param = file_io.FileReadWrite.readInitialFile(address)
                if init_param is None:
                    item = [file_type, address, file_exist, validity]
                    result.append(item)
                else:
                    validity = True
                    item = [file_type, address, file_exist, validity]
                    result.append(item)

                    #Restart Read File
                    if len(init_param.restart_read_file_name) > 0:
                        file_type = "Restart Read File"
                        address = os.path.join(model_directory, init_param.restart_read_file_name)
                        item = [file_type, address, os.path.exists(address), None]
                        result.append(item)

                    #CO2 File
                    file_type = "Cabor-di-oxide File"
                    address = os.path.join(model_directory, init_param.carbon_file)
                    item = [file_type, address, os.path.exists(address), None]
                    result.append(item)


                    #validitating GIS file
                    file_type = "GIS File"
                    address = os.path.join(model_directory, init_param.gis_file_name)
                    file_exist = os.path.exists(address)
                    validity = False

                    if not file_exist:
                        item = [file_type, address, file_exist, validity]
                        result.append(item)
                    else:
                        gisList = file_io.FileReadWrite.readGisFile(address)
                        if len(gisList) > 0:
                            validity = True
                            item = [file_type, address, file_exist, validity]
                            result.append(item)
                        else:
                            item = [file_type, address, file_exist, validity]
                            result.append(item)

                        for gis in gisList:
                            soil_profile_file = os.path.join(model_directory, "soil", gis.soilProfileFileName)
                            soil_horizon_file = os.path.join(model_directory, "soil", gis.soilHorizonFileName)
                            file_exist = False
                            validity = False

                            if not os.path.exists(soil_profile_file) or not os.path.exists(soil_horizon_file):
                                file_type = "(" + str(gis.siteIndex) + ") Soil Profile File"
                                item = [file_type, soil_profile_file, os.path.exists(soil_profile_file), validity]
                                result.append(item)

                                file_type = "(" + str(gis.siteIndex) + ") Soil Horizon File"
                                item = [file_type, soil_profile_file, os.path.exists(soil_horizon_file), validity]
                                result.append(item)
                            else:
                                file_exist = True

                                soil_profile_list = file_io.FileReadWrite.readSoilProfile(soil_profile_file, soil_horizon_file)
                                if len(soil_profile_list) > 0:
                                    for sp in soil_profile_list:
                                        if sp.profileName == gis.profileName:
                                            validity = True
                                            break
                                    else: validity = False

                                file_type = "(" + str(gis.siteIndex) + ") Soil Profile File"
                                item = [file_type, soil_profile_file, file_exist, validity]
                                result.append(item)

                                file_type = "(" + str(gis.siteIndex) + ") Soil Horizon File"
                                item = [file_type, soil_horizon_file, file_exist, validity]
                                result.append(item)

                            #NDEP File
                            file_type = "(" + str(gis.siteIndex) + ") NDEP File"
                            address = os.path.join(model_directory, "co2", gis.ndepFileName)

                            item = [file_type, address, os.path.exists(address), None]
                            result.append(item)

                            #MET File
                            file_type = "(" + str(gis.siteIndex) + ") MET File"
                            address = os.path.join(model_directory, "met", gis.meteorologicalFileName)

                            item = [file_type, address, os.path.exists(address), None]
                            result.append(item)

                    #VEG file validation
                    file_type = "Vegetation File"
                    address = os.path.join(model_directory, init_param.veg_file_name)
                    file_exist = os.path.exists(address)
                    validity = False

                    if not file_exist:
                        item = [file_type, address, file_exist, None]
                        result.append(item)
                    else:
                        veg_list = file_io.FileReadWrite.readVegFile(address)

                        if len(veg_list) > 0:
                            validity = True
                            item = [file_type, address, file_exist, validity]
                            result.append(item)

                            for veg in veg_list:
                                if len(veg.speciesSeqFile) > 0:
                                    file_type = "("+ str(veg.siteIndex) + ":" + str(veg.vegetationNumber) +")Species Sequence File"
                                    address = os.path.join(model_directory, "spseq", veg.speciesSeqFile)
                                    file_exist = os.path.exists(address)

                                    item = [file_type, address, file_exist, None]
                                    result.append(item)

                                #epc file
                                file_type = "("+ str(veg.siteIndex) + ":" + str(veg.vegetationNumber) +") EPC File"
                                address = os.path.join(model_directory, "epc", veg.epcFileName)
                                file_exist = os.path.exists(address)
                                validity = False

                                if not file_exist:
                                    item = [file_type, address, file_exist, validity]
                                    result.append(item)
                                else:
                                    epc_param = file_io.FileReadWrite.readEpcFile(address)
                                    if  epc_param is None:
                                        item = [file_type, address, file_exist, validity]
                                        result.append(item)
                                    else:
                                        validity = True
                                        item = [file_type, address, file_exist, validity]
                                        result.append(item)

                                        if len(epc_param.thinningRuleFileName) > 0:
                                            file_type = "("+ str(veg.siteIndex) + ":" + str(veg.vegetationNumber) +") Harvest File"
                                            address = os.path.join(model_directory, epc_param.thinningRuleFileName)
                                            file_exist = os.path.exists(address)

                                            item = [file_type, address, file_exist, None]
                                            result.append(item)

        return result

    @staticmethod
    def change_restart_read_file(initial_filename, new_restart_read_filename):
        result = False

        init_param = file_io.FileReadWrite.readInitialFile(initial_filename)
        if init_param is not None:
            init_param.restart_read_file_name = "restart/" + new_restart_read_filename.split("/")[-1].split("\\")[-1]
            result = file_io.FileReadWrite.writeInitialFile(init_param, initial_filename)

        return result

    @staticmethod
    def change_carbon_file(initial_filename, new_carbon_filename):
        result = False

        init_param = file_io.FileReadWrite.readInitialFile(initial_filename)
        if init_param is not None:
            init_param.carbon_file = "co2/" + new_carbon_filename.split("/")[-1].split("\\")[-1]
            result = file_io.FileReadWrite.writeInitialFile(init_param, initial_filename)

        return result

    @staticmethod
    def change_gis_file(initial_filename, new_gis_filename):
        result = False

        init_param = file_io.FileReadWrite.readInitialFile(initial_filename)
        if init_param is not None:
            init_param.gis_file_name = "ini/" + new_gis_filename.split("/")[-1].split("\\")[-1]
            result = file_io.FileReadWrite.writeInitialFile(init_param, initial_filename)
        return result

    @staticmethod
    def change_veg_file(initial_filename, new_veg_filename):
        result = False

        init_param = file_io.FileReadWrite.readInitialFile(initial_filename)
        if init_param is not None:
            init_param.veg_file_name = "ini/" + new_veg_filename.split("/")[-1].split("\\")[-1]
            result = file_io.FileReadWrite.writeInitialFile(init_param, initial_filename)

        return result

    @staticmethod
    def change_soil_profile_file(gis_file_name, site_index, new_soil_profile_filename):
        result = False

        site_list = file_io.FileReadWrite.readGisFile(gis_file_name)
        for site in site_list:
            if site.siteIndex == site_index:
                site.soilProfileFileName = new_soil_profile_filename.split("/")[-1].split("\\")[-1]
                result = file_io.FileReadWrite.writeGisFile(gis_file_name, site_list)
                break

        return result

    @staticmethod
    def change_soil_horizon_file(gis_file_name, site_index, new_soil_horizon_filename):
        result = False

        site_list = file_io.FileReadWrite.readGisFile(gis_file_name)
        for site in site_list:
            if site.siteIndex == site_index:
                site.soilHorizonFileName = new_soil_horizon_filename.split("/")[-1].split("\\")[-1]
                result = file_io.FileReadWrite.writeGisFile(gis_file_name, site_list)
                break

        return result

    @staticmethod
    def change_met_file(gis_file_name, site_index, new_met_filename):
        result = False

        site_list = file_io.FileReadWrite.readGisFile(gis_file_name)
        for site in site_list:
            if site.siteIndex == site_index:
                site.meteorologicalFileName = new_met_filename.split("/")[-1].split("\\")[-1]
                result = file_io.FileReadWrite.writeGisFile(gis_file_name, site_list)
                break

        return result

    @staticmethod
    def change_ndep_file(gis_file_name, site_index, new_ndep_filename):
        result = False

        site_list = file_io.FileReadWrite.readGisFile(gis_file_name)
        for site in site_list:
            if site.siteIndex == site_index:
                site.ndepFileName = new_ndep_filename.split("/")[-1].split("\\")[-1]
                result = file_io.FileReadWrite.writeGisFile(gis_file_name, site_list)
                break

        return result

    @staticmethod
    def change_epc_input_file(veg_filename, site_index, vegetation_number, new_epc_filename):
        result = False

        vegList = file_io.FileReadWrite.readVegFile(veg_filename)

        for veg in vegList:
            if veg.siteIndex == site_index and veg.vegetationNumber == vegetation_number:
                veg.epcFileName = new_epc_filename.split("/")[-1].split("\\")[-1]
                result = file_io.FileReadWrite.writeVegFile(veg_filename, vegList)
                break

        return result

    @staticmethod
    def change_harvest_file(epc_filename, new_harvest_filename):
        result = False

        epc_param = file_io.FileReadWrite.readEpcFile(epc_filename)
        if epc_param is not None:
            epc_param.thinningRuleFileName = "har/" + new_harvest_filename.split("/")[-1].split("\\")[-1]
            result = file_io.FileReadWrite.writeEpcFile(epc_filename, epc_param)

        return result

