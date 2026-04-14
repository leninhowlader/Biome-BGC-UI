from domain import ParamDomain
from output import output

class InitialParameter:
    #static/class variable
    paramLabelList = ParamDomain.readInitialParameterLabelList()    #structure: {0: paramName1, 1: paramName2, ...}
    paramDomain = ParamDomain.readInitialParameterDomainList()      #structure: {paramName1: domainList, paramName2: domainList,..}

    def __init__(self):
        self.gis_file_name = ""
        self.veg_file_name = ""

        self.restart_read_flag = -1
        self.restart_write_flag = -1
        self.restart_metyear_use_flag = -1
        self.restart_read_file_name = ""
        self.restart_write_file_name = ""

        self.no_of_sim_year = -1
        self.sim_start_year = -1
        self.sim_spinup_flag = -1
        self.no_of_spinup_year = -1

        self.Tmax_offset = -1
        self.Tmin_offset = -1
        self.precipitation_multiplier = -1
        self.vpd_multiplier = -1
        self.swave_multiplier = -1

        self.carbon_variability_flag = -1
        self.air_constant_carbon = -1
        self.carbon_file = ""

        self.nitrogen_depo_option_flag = -1
        self.industrial_ref_year = -1

        self.output_file_prefix = ""
        self.daily_output_flag = -1
        self.monthly_average_flag = -1
        self.annual_average_flag = -1
        self.annual_output_flag = -1
        self.display_flag = -1

        self.output = output()
        self.output_template_save_flag = -1
        self.output_template_save_fileName = ""

    def setParameterValue(self, paramName, paramValue):
        if len(self.paramLabelList) == 27:
            if paramName == self.paramLabelList[0]:
                self.gis_file_name = paramValue
            elif paramName == self.paramLabelList[1]:
                self.veg_file_name = paramValue
            elif paramName == self.paramLabelList[2]:
                val = -99999
                try: val = int(paramValue)
                except: return self.restart_read_flag
                if int(paramValue) in [0,1]:
                    self.restart_read_flag = val
                else: return self.restart_read_flag
            elif paramName == self.paramLabelList[3]:
                val = -99999
                try: val = int(paramValue)
                except: return self.restart_write_flag
                if int(paramValue) in [0,1]:
                    self.restart_write_flag = val
                else: return self.restart_write_flag
            elif paramName == self.paramLabelList[4]:
                val = -9999
                try: val = int(paramValue)
                except: return self.restart_metyear_use_flag
                if int(paramValue) in [0,1]:
                    self.restart_metyear_use_flag = val
                else: return self.restart_metyear_use_flag
            elif paramName == self.paramLabelList[5]:
                self.restart_read_file_name = paramValue
            elif paramName == self.paramLabelList[6]:
                self.restart_write_file_name = paramValue
            elif paramName == self.paramLabelList[7]:
                val = -9999
                try: val = int(paramValue)
                except: return self.no_of_sim_year
                if val > 0:
                    self.no_of_sim_year = val
                else: return self.no_of_sim_year
            elif paramName == self.paramLabelList[8]:
                val = -9999
                try: val = int(paramValue)
                except: return self.sim_start_year
                if val > 1900 and val <2500:
                    self.sim_start_year = val
                else: return self.sim_start_year
            elif paramName == self.paramLabelList[9]:
                val = -9999
                try: val = int(paramValue)
                except: return self.sim_spinup_flag
                if val in [1, 0]:
                    self.sim_spinup_flag = val
                else: return self.sim_spinup_flag
            elif paramName == self.paramLabelList[10]:
                val = -9999
                try: val = int(paramValue)
                except: return self.no_of_spinup_year
                if val > 0:
                    self.no_of_spinup_year = val
                else: return self.no_of_spinup_year
            elif paramName == self.paramLabelList[11]:
                val = -9999
                try: val = float(paramValue)
                except: return self.Tmax_offset
                # if val > 0:
                self.Tmax_offset = val
                # else: return False
            elif paramName == self.paramLabelList[12]:
                val = -9999
                try: val = float(paramValue)
                except: return self.Tmin_offset
                self.Tmin_offset = val
            elif paramName == self.paramLabelList[13]:
                val = -9999
                try: val = float(paramValue)
                except: return self.precipitation_multiplier
                self.precipitation_multiplier = val
            elif paramName == self.paramLabelList[14]:
                val = -9999
                try: val = float(paramValue)
                except: return self.vpd_multiplier
                self.vpd_multiplier = val
            elif paramName == self.paramLabelList[15]:
                val = -9999
                try: val = float(paramValue)
                except: return self.swave_multiplier
                self.swave_multiplier = val
            elif paramName == self.paramLabelList[16]:
                val = -9999
                try: val = int(paramValue)
                except: return self.carbon_variability_flag
                if val in [0,1]:
                    self.carbon_variability_flag = val
                else: return self.carbon_variability_flag
            elif  paramName == self.paramLabelList[17]:
                val = -9999
                try: val = float(paramValue)
                except: return self.air_constant_carbon
                self.air_constant_carbon = val
            elif paramName == self.paramLabelList[18]:
                self.carbon_file = paramValue
            elif paramName == self.paramLabelList[19]:
                val = -9999
                try: val = int(paramValue)
                except: return self.nitrogen_depo_option_flag
                if val in [0, 1, 2]:
                    self.nitrogen_depo_option_flag = val
                else: return self.nitrogen_depo_option_flag
            elif paramName == self.paramLabelList[20]:
                val = -9999
                try: val = int(paramValue)
                except: return self.industrial_ref_year
                if val > 1900:
                    self.industrial_ref_year = val
                else: return self.industrial_ref_year
            elif paramName == self.paramLabelList[21]:
                self.output_file_prefix = paramValue
            elif paramName == self.paramLabelList[22]:
                val = -9999
                try: val = int(paramValue)
                except: return self.daily_output_flag
                if val in [0, 1, 2, 3, 4]:
                    self.daily_output_flag = val
                else: return self.daily_output_flag
            elif paramName == self.paramLabelList[23]:
                val = -9999
                try: val = int(paramValue)
                except: return self.monthly_average_flag
                if val in [0,1]:
                    self.monthly_average_flag = val
                else: return self.monthly_average_flag
            elif paramName == self.paramLabelList[24]:
                val = -9999
                try: val = int(paramValue)
                except: return self.annual_average_flag
                if val in [0,1]:
                    self.annual_average_flag = val
                else: return self.annual_average_flag
            elif paramName == self.paramLabelList[25]:
                val = -9999
                try: val = int(paramValue)
                except: return self.annual_output_flag
                if val in [0,1,2,3,4]:
                    self.annual_output_flag = val
                else: return self.annual_output_flag
            elif paramName == self.paramLabelList[26]:
                val = -9999
                try: val = int(paramValue)
                except: return self.display_flag
                if val in [0,1]:
                    self.display_flag = val
                else: return self.display_flag
        return None

    def compare(initParamList):
        indic = {}           #input dictionary; structure: {parameterName1: valueList1, parameterName2: valueList2}

        for item in initParamList:
            #gis_file_name
            pname = "GIS File Name"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.gis_file_name]
            else: temp.append(item.gis_file_name)

            #veg_file_name
            pname = "Veg File Name"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.veg_file_name]
            else: temp.append(item.veg_file_name)

            #restart_read_flag
            pname = "Restart Read Flag"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.restart_read_flag]
            else: temp.append(item.restart_read_flag)

            #restart_write_flag
            pname = "Restart Write Flag"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.restart_write_flag]
            else: temp.append(item.restart_write_flag)

            #restart_metyear_use_flag
            pname = "Restart Metyear Use Flag"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.restart_metyear_use_flag]
            else: temp.append(item.restart_metyear_use_flag)

            #restart_read_file_name
            pname = "Restart Read File Name"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.restart_read_file_name]
            else: temp.append(item.restart_read_file_name)

            #restart_write_file_name
            pname = "Restart Write File Name"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.restart_write_file_name]
            else: temp.append(item.restart_write_file_name)

            #no_of_sim_year
            pname = "No of Sim Year"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.no_of_sim_year]
            else: temp.append(item.no_of_sim_year)

            #sim_start_year
            pname = "Sim Start Year"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.sim_start_year]
            else: temp.append(item.sim_start_year)

            #sim_spinup_flag
            pname = "Sim Spinup Flag"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.sim_spinup_flag]
            else: temp.append(item.sim_spinup_flag)

            #no_of_spinup_year
            pname = "No of Spinup Year"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.no_of_spinup_year]
            else: temp.append(item.no_of_spinup_year)

            #Tmax_offset
            pname = "Tmax Offset"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.Tmax_offset]
            else: temp.append(item.Tmax_offset)

            #Tmin_offset
            pname = "Tmin Offset"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.Tmin_offset]
            else: temp.append(item.Tmin_offset)

            #precipitation_multiplier
            pname = "Precipitation Multiplier"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.precipitation_multiplier]
            else: temp.append(item.precipitation_multiplier)

            #vpd_multiplier
            pname = "VPD Multiplier"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.vpd_multiplier]
            else: temp.append(item.vpd_multiplier)

            #swave_multiplier
            pname = "Radiation Multiplier"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.swave_multiplier]
            else: temp.append(item.swave_multiplier)

            #carbon_variability_flag
            pname = "CO2 Control Flag"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.carbon_variability_flag]
            else: temp.append(item.carbon_variability_flag)

            #air_constant_carbon
            pname = "Air Constant Carbon"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.air_constant_carbon]
            else: temp.append(item.air_constant_carbon)

            #carbon_file
            pname = "Carbon File"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.carbon_file]
            else: temp.append(item.carbon_file)

            #nitrogen_depo_option_flag
            pname = "Nitrogen Depo Option Flag"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.nitrogen_depo_option_flag]
            else: temp.append(item.nitrogen_depo_option_flag)

            #industrial_ref_year
            pname = "Industrial Ref. Year"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.industrial_ref_year]
            else: temp.append(item.industrial_ref_year)

            #output_file_prefix
            pname = "Output File Prefix"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.output_file_prefix]
            else: temp.append(item.output_file_prefix)

            #daily_output_flag
            pname = "Daily Output Flag"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.daily_output_flag]
            else: temp.append(item.daily_output_flag)

            #monthly_average_flag
            pname = "Monthly Average Flag"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.monthly_average_flag]
            else: temp.append(item.monthly_average_flag)

            #annual_average_flag
            pname = "Annual Average Flag"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.annual_average_flag]
            else: temp.append(item.annual_average_flag)

            #annual_output_flag
            pname = "Annual Output Flag"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.annual_output_flag]
            else: temp.append(item.annual_output_flag)

            #display_flag
            pname = "Display Flag"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.display_flag]
            else: temp.append(item.display_flag)

        outdic = {}         #output dictionary; structure={parameter1: valueList1, parameter2: valueList2, ...}
        for param, value in indic.items():
            if len(set(value)) > 1:
                outdic[param] = value

        return outdic

    def showParameterValue(self):
        valueList = []      #structure: [{"pname": "Gis file Name", "pvalue": gis_08.txt}, {}]

        if len(self.paramLabelList) == 27:
            #gis_file_name
            pname = self.paramLabelList[0]        #parameter name
            item = {"pname": pname, "pvalue": self.gis_file_name}
            valueList.append(item)

            #veg_file_name
            pname = self.paramLabelList[1]       #parameter name
            item = {"pname": pname, "pvalue": self.veg_file_name}
            valueList.append(item)

            #restart_read_flag
            pname = self.paramLabelList[2]         #parameter name
            item = {"pname": pname, "pvalue": self.restart_read_flag}
            valueList.append(item)

            #restart_write_flag
            pname = self.paramLabelList[3]         #parameter name
            item = {"pname": pname, "pvalue": self.restart_write_flag}
            valueList.append(item)

            #restart_metyear_use_flag
            pname = self.paramLabelList[4]         #parameter name
            item = {"pname": pname, "pvalue": self.restart_metyear_use_flag}
            valueList.append(item)

            #restart_read_file_name
            pname = self.paramLabelList[5]         #parameter name
            item = {"pname": pname, "pvalue": self.restart_read_file_name}
            valueList.append(item)

            #restart_write_file_name
            pname = self.paramLabelList[6]         #parameter name
            item = {"pname": pname, "pvalue": self.restart_write_file_name}
            valueList.append(item)

            #no_of_sim_year
            pname = self.paramLabelList[7]         #parameter name
            item = {"pname": pname, "pvalue": self.no_of_sim_year}
            valueList.append(item)

            #sim_start_year
            pname = self.paramLabelList[8]         #parameter name
            item = {"pname": pname, "pvalue": self.sim_start_year}
            valueList.append(item)

            #sim_spinup_flag
            pname = self.paramLabelList[9]         #parameter name
            item = {"pname": pname, "pvalue": self.sim_spinup_flag}
            valueList.append(item)

            #no_of_spinup_year
            pname = self.paramLabelList[10]        #parameter name
            item = {"pname": pname, "pvalue": self.no_of_spinup_year}
            valueList.append(item)

            #Tmax_offset
            pname = self.paramLabelList[11]         #parameter name
            item = {"pname": pname, "pvalue": self.Tmax_offset}
            valueList.append(item)

            #Tmin_offset
            pname = self.paramLabelList[12]         #parameter name
            item = {"pname": pname, "pvalue": self.Tmin_offset}
            valueList.append(item)


            #precipitation_multiplier
            pname = self.paramLabelList[13]         #parameter name
            item = {"pname": pname, "pvalue": self.precipitation_multiplier}
            valueList.append(item)


            #vpd_multiplier
            pname = self.paramLabelList[14]         #parameter name
            item = {"pname": pname, "pvalue": self.vpd_multiplier}
            valueList.append(item)

            #swave_multiplier
            pname = self.paramLabelList[15]         #parameter name
            item = {"pname": pname, "pvalue": self.swave_multiplier}
            valueList.append(item)

            #carbon_variability_flag
            pname = self.paramLabelList[16]         #parameter name
            item = {"pname": pname, "pvalue": self.carbon_variability_flag}
            valueList.append(item)

            #air_constant_carbon
            pname = self.paramLabelList[17]         #parameter name
            item = {"pname": pname, "pvalue": self.air_constant_carbon}
            valueList.append(item)

            #carbon_file
            pname = self.paramLabelList[18]        #parameter name
            item = {"pname": pname, "pvalue": self.carbon_file}
            valueList.append(item)

            #nitrogen_depo_option_flag
            pname = self.paramLabelList[19]         #parameter name
            item = {"pname": pname, "pvalue": self.nitrogen_depo_option_flag}
            valueList.append(item)

            #industrial_ref_year
            pname = self.paramLabelList[20]         #parameter name
            item = {"pname": pname, "pvalue": self.industrial_ref_year}
            valueList.append(item)

            #output_file_prefix
            pname = self.paramLabelList[21]         #parameter name
            item = {"pname": pname, "pvalue": self.output_file_prefix}
            valueList.append(item)

            #daily_output_flag
            pname = self.paramLabelList[22]         #parameter name
            item = {"pname": pname, "pvalue": self.daily_output_flag}
            valueList.append(item)

            #monthly_average_flag
            pname = self.paramLabelList[23]        #parameter name
            item = {"pname": pname, "pvalue": self.monthly_average_flag}
            valueList.append(item)

            #annual_average_flag
            pname = self.paramLabelList[24]         #parameter name
            item = {"pname": pname, "pvalue": self.annual_average_flag}
            valueList.append(item)

            #annual_output_flag
            pname = self.paramLabelList[25]        #parameter name
            item = {"pname": pname, "pvalue": self.annual_output_flag}
            valueList.append(item)

            #display_flag
            pname = self.paramLabelList[26]        #parameter name
            item = {"pname": pname, "pvalue": self.display_flag}
            valueList.append(item)

        return valueList

    def getParameterValue(self, paramName):
        if len(self.paramLabelList) == 27:
            if paramName == self.paramLabelList[0]:
                return self.gis_file_name
            elif paramName == self.paramLabelList[1]:
                return self.veg_file_name
            elif paramName == self.paramLabelList[2]:
                return self.restart_read_flag
            elif paramName == self.paramLabelList[3]:
                return self.restart_write_flag
            elif paramName == self.paramLabelList[4]:
                return self.restart_metyear_use_flag
            elif paramName == self.paramLabelList[5]:
                return self.restart_read_file_name
            elif paramName == self.paramLabelList[6]:
                return self.restart_write_file_name
            elif paramName == self.paramLabelList[7]:
                return self.no_of_sim_year
            elif paramName == self.paramLabelList[8]:
                return self.sim_start_year
            elif paramName == self.paramLabelList[9]:
                return self.sim_spinup_flag
            elif paramName == self.paramLabelList[10]:
                return self.no_of_spinup_year
            elif paramName == self.paramLabelList[11]:
                return self.Tmax_offset
            elif paramName == self.paramLabelList[12]:
                return self.Tmin_offset
            elif paramName == self.paramLabelList[13]:
                return self.precipitation_multiplier
            elif paramName == self.paramLabelList[14]:
                return self.vpd_multiplier
            elif paramName == self.paramLabelList[15]:
                return self.swave_multiplier
            elif paramName == self.paramLabelList[16]:
                return self.carbon_variability_flag
            elif  paramName == self.paramLabelList[17]:
                return self.air_constant_carbon
            elif paramName == self.paramLabelList[18]:
                return self.carbon_file
            elif paramName == self.paramLabelList[19]:
                return self.nitrogen_depo_option_flag
            elif paramName == self.paramLabelList[20]:
                return self.industrial_ref_year
            elif paramName == self.paramLabelList[21]:
                return self.output_file_prefix
            elif paramName == self.paramLabelList[22]:
                return self.daily_output_flag
            elif paramName == self.paramLabelList[23]:
                return self.monthly_average_flag
            elif paramName == self.paramLabelList[24]:
                return self.annual_average_flag
            elif paramName == self.paramLabelList[25]:
                return self.annual_output_flag
            elif paramName == self.paramLabelList[26]:
                return self.display_flag
        return None

    @staticmethod
    def hasDomain(paramName):
        for key in InitialParameter.paramDomain:
            if key == paramName: return True
        return False

    @staticmethod
    def getDomain(paramName):
        domain = InitialParameter.paramDomain.get(paramName)
        return domain

class GisParameter:
    #static/class level variables
    paramLabelList = ParamDomain.readGisParameterLabelList()
    paramDomain = ParamDomain.readGisParameterDomainList()

    @staticmethod
    def hasDomain(paramName):
        for key in GisParameter.paramDomain:
            if key == paramName: return True
        return False

    @staticmethod
    def getDomain(paramName):
        domain = GisParameter.paramDomain.get(paramName)
        return domain

    def __init__(self):
        self.siteIndex = -1                         #1
        self.noOfVegetation = 0                     #2
        self.soilProfileFileName = ""               #3
        self.soilHorizonFileName = ""               #4
        self.profileName = ""                       #5
        self.groundWaterDepth = -1                  #6
        self.groundWaterFlag = -1                   #7
        # self.StaticGroundWater = -1
        self.reductionFactor = -1                   #8
        self.zetaParameter = -1                     #9
        self.depthOfDehumidification = -1           #10
        self.yearDay = -1                           #11
        self.temperatureTimeLag = -1                #12
        self.amplitudeOfSoilTemperature = -1        #13
        self.increaseOfTemperature = -1             #14
        self.siteElevation = -1                     #15
        self.siteLatitude = -1                      #16
        self.meteorologicalFileName = -1            #17
        self.noOfMeteorologicalYear = -1            #18
        self.ndepFileName = -1                      #19
        self.ndepRate = -1                          #20
        self.industrialNdepRate = -1                #21
        self.snowWaterPool = -1                     #22
        self.fastMicrobialFraction = -1             #23
        self.mediumMicrobialFraction = -1           #24
        self.slowMicrobialFraction = -1             #25
        self.recalcitrantSom = -1                   #26
        self.soilMineralNitrogenPool = -1.0         #27

    def compare(gisParamList):
        indic = {}           #input dictionary; structure: {parameterName1: valueList1, parameterName2: valueList2}

        for gis in gisParamList:
            #siteIndex
            pname = "Site Index"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.siteIndex]
            else: temp.append(gis.siteIndex)

            #noOfVegetation
            pname = "No. Of Vegetation"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.noOfVegetation]
            else: temp.append(gis.noOfVegetation)

            #soilProfileFileName
            pname = "Soil Profile File"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.soilProfileFileName]
            else: temp.append(gis.soilProfileFileName)

            #soilHorizonFileName
            pname = "Soil Horizon File"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.soilHorizonFileName]
            else: temp.append(gis.soilHorizonFileName)

            #profileName
            pname = "Profile Name"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.profileName]
            else: temp.append(gis.profileName)

            #groundWaterDepth
            pname = "Ground Water Depth"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.groundWaterDepth]
            else: temp.append(gis.groundWaterDepth)

            #groundWaterFlag
            pname = "Ground Water Flag"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.groundWaterFlag]
            else: temp.append(gis.groundWaterFlag)

            #reductionFactor
            pname = "Reduction Factor (infiltration)"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.reductionFactor]
            else: temp.append(gis.reductionFactor)

            #zetaParameter
            pname = "Zeta Parameter"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.zetaParameter]
            else: temp.append(gis.zetaParameter)

            #depthOfDehumidification
            pname = "Depth of Dehumidification"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.depthOfDehumidification]
            else: temp.append(gis.depthOfDehumidification)

            #yearDay
            pname = "Year Day"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.yearDay]
            else: temp.append(gis.yearDay)

            #temperatureTimeLag
            pname = "Temp Time Lag"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.temperatureTimeLag]
            else: temp.append(gis.temperatureTimeLag)

            #amplitudeOfSoilTemperature
            pname = "Amplitude of Soil Temperature"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.amplitudeOfSoilTemperature]
            else: temp.append(gis.amplitudeOfSoilTemperature)

            #increaseOfTemperature
            pname = "Increase of Temperature"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.increaseOfTemperature]
            else: temp.append(gis.increaseOfTemperature)

            #siteElevation
            pname = "Site Elevation"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.siteElevation]
            else: temp.append(gis.siteElevation)

            #siteLatitude
            pname = "Site Latitude"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.siteLatitude]
            else: temp.append(gis.siteLatitude)

            #meteorologicalFileName
            pname = "Meteorological File Name"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.meteorologicalFileName]
            else: temp.append(gis.meteorologicalFileName)

            #noOfMeteorologicalYear
            pname = "No. of Meteorological Year"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.noOfMeteorologicalYear]
            else: temp.append(gis.noOfMeteorologicalYear)

            #ndepFileName
            pname = "NDEP File Name"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.ndepFileName]
            else: temp.append(gis.ndepFileName)

            #ndepRate
            pname = "NDEP Rate"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.ndepRate]
            else: temp.append(gis.ndepRate)

            #industrialNdepRate
            pname = "Industrial NDEP Rate"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.industrialNdepRate]
            else: temp.append(gis.industrialNdepRate)

            #snowWaterPool
            pname = "Snow Water Pool"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.snowWaterPool]
            else: temp.append(gis.snowWaterPool)

            #fastMicrobialFraction
            pname = "Fast Microbial Fraction"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.fastMicrobialFraction]
            else: temp.append(gis.fastMicrobialFraction)

            #mediumMicrobialFraction
            pname = "Medium Microbial Fraction"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.mediumMicrobialFraction]
            else: temp.append(gis.mediumMicrobialFraction)

            #slowMicrobialFraction
            pname = "Slow Microbial Fraction"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.slowMicrobialFraction]
            else: temp.append(gis.slowMicrobialFraction)

            #recalcitrantSom
            pname = "Recalcitrant SOM"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.recalcitrantSom]
            else: temp.append(gis.recalcitrantSom)

            #soilMineralNitrogenPool
            pname = "Soil Mineral Nitrogen Pool"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [gis.soilMineralNitrogenPool]
            else: temp.append(gis.soilMineralNitrogenPool)

        outdic = {}         #output dictionary; structure={parameter1: valueList1, parameter2: valueList2, ...}
        for param, value in indic.items():
            if len(set(value)) > 1:
                outdic[param] = value

        return outdic

    def setParameterValue(self, pname, pval):
        if len(GisParameter.paramLabelList) == 27:
            if pname == GisParameter.paramLabelList[0]: #
                self.siteIndex = pval
            elif pname == GisParameter.paramLabelList[1]:
                val = -9999
                try: val = int(pval)
                except: return self.noOfVegetation
                if val > 0:
                    self.noOfVegetation = val
                else: return self.noOfVegetation
            elif pname == GisParameter.paramLabelList[2]:
                self.soilProfileFileName = pval
            elif pname == GisParameter.paramLabelList[3]:
                self.soilHorizonFileName = pval
            elif pname == GisParameter.paramLabelList[4]:
                self.profileName = pval
            elif pname == GisParameter.paramLabelList[5]:
                val = -9999
                try: val = float(pval)
                except: return self.groundWaterDepth
                self.groundWaterDepth = val
            elif pname == GisParameter.paramLabelList[6]:
                val = -9999
                try: val = int(pval)
                except: return self.groundWaterFlag
                if val in [0,1]:
                    self.groundWaterFlag = val
                else: return self.groundWaterFlag
            elif pname == GisParameter.paramLabelList[7]:
                val = -9999
                try: val = float(pval)
                except: return self.reductionFactor
                self.reductionFactor = val
            elif pname == GisParameter.paramLabelList[8]:
                val = -9999
                try: val = float(pval)
                except: return self.zetaParameter
                self.zetaParameter = val
            elif pname == GisParameter.paramLabelList[9]:
                val = -9999
                try: val = float(pval)
                except: return self.depthOfDehumidification
                self.depthOfDehumidification = val
            elif pname == GisParameter.paramLabelList[10]:
                val = -9999
                try: val = int(pval)
                except: return self.yearDay
                if val > -1 and val < 365:
                    self.yearDay = val
                else: return self.yearDay
            elif pname == GisParameter.paramLabelList[11]:
                val = -9999
                try: val = float(pval)
                except: return self.temperatureTimeLag
                self.temperatureTimeLag = val
            elif pname == GisParameter.paramLabelList[12]:
                val = -9999
                try: val = float(pval)
                except: return self.amplitudeOfSoilTemperature
                self.amplitudeOfSoilTemperature = val
            elif pname == GisParameter.paramLabelList[13]:
                val = -9999
                try: val = float(pval)
                except: return self.increaseOfTemperature
                self.increaseOfTemperature = val
            elif pname == GisParameter.paramLabelList[14]:
                val = -9999
                try: val = float(pval)
                except: return self.siteElevation
                self.siteElevation = val
            elif pname == GisParameter.paramLabelList[15]:
                val = -9999
                try: val = float(pval)
                except: return self.siteLatitude
                self.siteLatitude = val
            elif pname == GisParameter.paramLabelList[16]:
                self.meteorologicalFileName = pval
            elif pname == GisParameter.paramLabelList[17]:
                val = -9999
                try: val = int(pval)
                except: return self.noOfMeteorologicalYear
                self.noOfMeteorologicalYear = val
            elif pname == GisParameter.paramLabelList[18]:
                self.ndepFileName = pval
            elif pname == GisParameter.paramLabelList[19]:
                val = -9999
                try: val = float(pval)
                except: return self.ndepRate
                self.ndepRate = val
            elif pname == GisParameter.paramLabelList[20]:
                val = -9999
                try: val = float(pval)
                except: return self.industrialNdepRate
                self.industrialNdepRate = val
            elif pname == GisParameter.paramLabelList[21]:
                val = -9999
                try: val = float(pval)
                except: return self.snowWaterPool
                self.snowWaterPool = pval
            elif pname == GisParameter.paramLabelList[22]:
                val = -9999
                try: val = float(pval)
                except: return self.fastMicrobialFraction
                self.fastMicrobialFraction = val
            elif pname == GisParameter.paramLabelList[23]:
                val = -9999
                try: val = float(pval)
                except: return self.mediumMicrobialFraction

                self.mediumMicrobialFraction = val
            elif pname == GisParameter.paramLabelList[24]:
                val = -9999
                try: val = float(pval)
                except: return self.slowMicrobialFraction
                self.slowMicrobialFraction = val
            elif pname == GisParameter.paramLabelList[25]:
                val = -9999
                try: val = float(pval)
                except: return self.recalcitrantSom
                self.recalcitrantSom = val
            elif pname == GisParameter.paramLabelList[26]:
                val = -9999
                try: val = float(pval)
                except: return self.soilMineralNitrogenPool
                self.soilMineralNitrogenPool = val
        return None

    def showParameterValue(self):
        valueList = []      #structure: [{"pname": "Gis file Name", "pvalue": gis_08.txt}, {}]

        if len(GisParameter.paramLabelList) == 27:
            pname = GisParameter.paramLabelList[0] #"Site Index"
            item = {"pname": pname, "pvalue": self.siteIndex}
            valueList.append(item)

            #noOfVegetation
            pname = GisParameter.paramLabelList[1] #"No. Of Vegetation"
            item = {"pname": pname, "pvalue": self.noOfVegetation}
            valueList.append(item)

            #soilProfileFileName
            pname = GisParameter.paramLabelList[2] #"Soil Profile File"
            item = {"pname": pname, "pvalue": self.soilProfileFileName}
            valueList.append(item)

            #soilHorizonFileName
            pname = GisParameter.paramLabelList[3] #"Soil Horizon File"
            item = {"pname": pname, "pvalue": self.soilHorizonFileName}
            valueList.append(item)

            #profileName
            pname = GisParameter.paramLabelList[4] #"Profile Name"
            item = {"pname": pname, "pvalue": self.profileName}
            valueList.append(item)

            #groundWaterDepth
            pname = GisParameter.paramLabelList[5] #"Ground Water Depth"
            item = {"pname": pname, "pvalue": self.groundWaterDepth}
            valueList.append(item)

            #groundWaterFlag
            pname = GisParameter.paramLabelList[6] #"Ground Water Flag"
            item = {"pname": pname, "pvalue": self.groundWaterFlag}
            valueList.append(item)

            #reductionFactor
            pname = GisParameter.paramLabelList[7] #"Reduction Factor (infiltration)"
            item = {"pname": pname, "pvalue": self.reductionFactor}
            valueList.append(item)

            #zetaParameter
            pname = GisParameter.paramLabelList[8] #"Zeta Parameter"
            item = {"pname": pname, "pvalue": self.zetaParameter}
            valueList.append(item)

            #depthOfDehumidification
            pname = GisParameter.paramLabelList[9] #"Depth of Dehumidification"
            item = {"pname": pname, "pvalue": self.depthOfDehumidification}
            valueList.append(item)

            #yearDay
            pname = GisParameter.paramLabelList[10] #"Year Day"
            item = {"pname": pname, "pvalue": self.yearDay}
            valueList.append(item)

            #temperatureTimeLag
            pname = GisParameter.paramLabelList[11] #"Temp Time Lag"
            item = {"pname": pname, "pvalue": self.temperatureTimeLag}
            valueList.append(item)

            #amplitudeOfSoilTemperature
            pname = GisParameter.paramLabelList[12] #"Amplitude of Soil Temperature"
            item = {"pname": pname, "pvalue": self.amplitudeOfSoilTemperature}
            valueList.append(item)

            #increaseOfTemperature
            pname = GisParameter.paramLabelList[13] #"Increase of Temperature"
            item = {"pname": pname, "pvalue": self.increaseOfTemperature}
            valueList.append(item)

            #siteElevation
            pname = GisParameter.paramLabelList[14] #"Site Elevation"
            item = {"pname": pname, "pvalue": self.siteElevation}
            valueList.append(item)

            #siteLatitude
            pname = GisParameter.paramLabelList[15] #"Site Latitude"
            item = {"pname": pname, "pvalue": self.siteLatitude}
            valueList.append(item)

            #meteorologicalFileName
            pname = GisParameter.paramLabelList[16] #"Meteorological File Name"
            item = {"pname": pname, "pvalue": self.meteorologicalFileName}
            valueList.append(item)

            #noOfMeteorologicalYear
            pname = GisParameter.paramLabelList[17] #"No. of Meteorological Year"
            item = {"pname": pname, "pvalue": self.noOfMeteorologicalYear}
            valueList.append(item)

            #ndepFileName
            pname = GisParameter.paramLabelList[18] #"NDEP File Name"
            item = {"pname": pname, "pvalue": self.ndepFileName}
            valueList.append(item)

            #ndepRate
            pname = GisParameter.paramLabelList[19] #"NDEP Rate"
            item = {"pname": pname, "pvalue": self.ndepRate}
            valueList.append(item)

            #industrialNdepRate
            pname = GisParameter.paramLabelList[20] #"Industrial NDEP Rate"
            item = {"pname": pname, "pvalue": self.industrialNdepRate}
            valueList.append(item)

            #snowWaterPool
            pname = GisParameter.paramLabelList[21] #"Snow Water Pool"
            item = {"pname": pname, "pvalue": self.snowWaterPool}
            valueList.append(item)

            #fastMicrobialFraction
            pname = GisParameter.paramLabelList[22] #"Fast Microbial Fraction"
            item = {"pname": pname, "pvalue": self.fastMicrobialFraction}
            valueList.append(item)

            #mediumMicrobialFraction
            pname = GisParameter.paramLabelList[23] #"Medium Microbial Fraction"
            item = {"pname": pname, "pvalue": self.mediumMicrobialFraction}
            valueList.append(item)

            #slowMicrobialFraction
            pname = GisParameter.paramLabelList[24] #"Slow Microbial Fraction"
            item = {"pname": pname, "pvalue": self.slowMicrobialFraction}
            valueList.append(item)

            #recalcitrantSom
            pname = GisParameter.paramLabelList[25] #"Recalcitrant SOM"
            item = {"pname": pname, "pvalue": self.recalcitrantSom}
            valueList.append(item)

            #soilMineralNitrogenPool
            pname = GisParameter.paramLabelList[26] #"Soil Mineral Nitrogen Pool"
            item = {"pname": pname, "pvalue": self.soilMineralNitrogenPool}
            valueList.append(item)

        return valueList

    def getParameterValue(self, pname):
        if len(GisParameter.paramLabelList) == 27:
            if pname == GisParameter.paramLabelList[0]: #
                return self.siteIndex
            elif pname == GisParameter.paramLabelList[1]:
                return self.noOfVegetation
            elif pname == GisParameter.paramLabelList[2]:
                return self.soilProfileFileName
            elif pname == GisParameter.paramLabelList[3]:
                return self.soilHorizonFileName
            elif pname == GisParameter.paramLabelList[4]:
                return self.profileName
            elif pname == GisParameter.paramLabelList[5]:
                return self.groundWaterDepth
            elif pname == GisParameter.paramLabelList[6]:
                return self.groundWaterFlag
            elif pname == GisParameter.paramLabelList[7]:
                return self.reductionFactor
            elif pname == GisParameter.paramLabelList[8]:
                return self.zetaParameter
            elif pname == GisParameter.paramLabelList[9]:
                return self.depthOfDehumidification
            elif pname == GisParameter.paramLabelList[10]:
                return self.yearDay
            elif pname == GisParameter.paramLabelList[11]:
                return self.temperatureTimeLag
            elif pname == GisParameter.paramLabelList[12]:
                return self.amplitudeOfSoilTemperature
            elif pname == GisParameter.paramLabelList[13]:
                return self.increaseOfTemperature
            elif pname == GisParameter.paramLabelList[14]:
                return self.siteElevation
            elif pname == GisParameter.paramLabelList[15]:
                return self.siteLatitude
            elif pname == GisParameter.paramLabelList[16]:
                return self.meteorologicalFileName
            elif pname == GisParameter.paramLabelList[17]:
                return self.noOfMeteorologicalYear
            elif pname == GisParameter.paramLabelList[18]:
                return self.ndepFileName
            elif pname == GisParameter.paramLabelList[19]:
                return self.ndepRate
            elif pname == GisParameter.paramLabelList[20]:
                return self.industrialNdepRate
            elif pname == GisParameter.paramLabelList[21]:
                return self.snowWaterPool
            elif pname == GisParameter.paramLabelList[22]:
                return self.fastMicrobialFraction
            elif pname == GisParameter.paramLabelList[23]:
                return self.mediumMicrobialFraction
            elif pname == GisParameter.paramLabelList[24]:
                return self.slowMicrobialFraction
            elif pname == GisParameter.paramLabelList[25]:
                return self.recalcitrantSom
            elif pname == GisParameter.paramLabelList[26]:
                return self.soilMineralNitrogenPool
        return None

class VegetationParameter:
    #static/class level variable
    paramLabelList = ParamDomain.readVegetationParameterLabelList()
    paramDomain = ParamDomain.readVegetationParameterDomainList()

    @staticmethod
    def hasDomain(paramName):
        for key in VegetationParameter.paramDomain:
            if key == paramName: return True
        return False

    @staticmethod
    def getDomain(paramName):
        domain = VegetationParameter.paramDomain.get(paramName)
        return domain

    def __init__(self):
        self.siteIndex = -1
        self.vegetationNumber = -1
        self.epcFileName = ""
        self.standDensity = -1
        self.startingTreeAge = -1
        self.startingRootDepth = -1
        self.treeGrowthClass = -1
        self.treeHeight = -1
        self.speciesSeqFile = ""
        self.leafCarbon = -1
        self.stemCarbon = -1
        self.debrisCarbon = -1
        self.labilePool = -1
        self.unshieldedCellulosePool = -1
        self.shieldedCellulosePool = -1
        self.ligninPool = -1
        self.nitrogenLabilePool = -1

    def compare(vegParamList):
        indic = {}           #input dictionary; structure: {parameterName1: valueList1, parameterName2: valueList2}

        for item in vegParamList:
            #siteIndex
            pname = "Site Index"        #parameter name
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.siteIndex]
            else: temp.append(item.siteIndex)

            #vegetationNumber
            pname = "Vegetation No."
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.vegetationNumber]
            else: temp.append(item.vegetationNumber)

            #epcFileName
            pname = "EPC File Name"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.epcFileName]
            else: temp.append(item.epcFileName)

            #standDensity
            pname = "Stand Density"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.standDensity]
            else: temp.append(item.standDensity)

            #startingTreeAge
            pname = "Starting Tree Age"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.startingTreeAge]
            else: temp.append(item.startingTreeAge)

            #startingRootDepth
            pname = "Starting Root Depth"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.startingRootDepth]
            else: temp.append(item.startingRootDepth)

            #treeGrowthClass
            pname = "Tree Growth Class"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.treeGrowthClass]
            else: temp.append(item.treeGrowthClass)

            # #reductionFactor
            # pname = "Reduction Factor (infiltration)"
            # temp = indic.get(pname)
            # if temp is None: indic[pname] = [item.reductionFactor]
            # else: temp.append(item.treeGrowthClass)

            #treeHeight
            pname = "Tree Height"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.treeHeight]
            else: temp.append(item.treeHeight)

            #speciesSeqFile
            pname = "Species Seq. File"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.speciesSeqFile]
            else: temp.append(item.speciesSeqFile)

            #leafCarbon
            pname = "Leaf Carbon"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.leafCarbon]
            else: temp.append(item.leafCarbon)

            #stemCarbon
            pname = "Stem Carbon"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.stemCarbon]
            else: temp.append(item.stemCarbon)

            #debrisCarbon
            pname = "Debris Carbon"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.debrisCarbon]
            else: temp.append(item.debrisCarbon)

            #labilePool
            pname = "Labile Pool"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.labilePool]
            else: temp.append(item.labilePool)

            #unshieldedCellulosePool
            pname = "Unshielded Cellulose Pool"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.unshieldedCellulosePool]
            else: temp.append(item.unshieldedCellulosePool)

            #shieldedCellulosePool
            pname = "Shielded Cellulose Pool"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.shieldedCellulosePool]
            else: temp.append(item.shieldedCellulosePool)

            #ligninPool
            pname = "Lignin Pool"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.ligninPool]
            else: temp.append(item.ligninPool)

            #nitrogenLabilePool
            pname = "Nitrogen Labile Pool"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.nitrogenLabilePool]
            else: temp.append(item.nitrogenLabilePool)

        outdic = {}         #output dictionary; structure={parameter1: valueList1, parameter2: valueList2, ...}
        for param, value in indic.items():
            if len(set(value)) > 1:
                outdic[param] = value

        return outdic

    def setParameterValue(self, pname, pval):
        if len(VegetationParameter.paramLabelList) == 17:
            if pname == VegetationParameter.paramLabelList[0]: #"Site Index":
                    self.siteIndex = pval
            elif pname == VegetationParameter.paramLabelList[1]: #"Vegetation No.":
                val = -9999
                try: val = int(pval)
                except: return self.vegetationNumber
                self.vegetationNumber = val
            elif pname == VegetationParameter.paramLabelList[2]: #"EPC File Name":
                self.epcFileName = pval
            elif pname == VegetationParameter.paramLabelList[3]: #"Stand Density":
                val = -9999
                try: val = float(pval)
                except: return self.standDensity
                self.standDensity = val
            elif pname == VegetationParameter.paramLabelList[4]: #"Starting Tree Age":
                val = -9999
                try: val = int(pval)
                except: return self.startingTreeAge
                self.startingTreeAge = val
            elif pname == VegetationParameter.paramLabelList[5]: #"Starting Root Depth":
                val = -9999
                try: val = float(pval)
                except: return self.startingRootDepth
                self.startingRootDepth = val
            elif pname == VegetationParameter.paramLabelList[6]: #"Tree Growth Class":
                val = -9999
                try: val = int(pval)
                except: return self.treeGrowthClass
                self.treeGrowthClass = val
            elif pname == VegetationParameter.paramLabelList[7]: #"Tree Height":
                val = -9999
                try: val = float(pval)
                except: return self.treeHeight
                self.treeHeight = val
            elif pname == VegetationParameter.paramLabelList[8]: #"Species Seq. File":
                self.speciesSeqFile = pval
            elif pname == VegetationParameter.paramLabelList[9]: #"Leaf Carbon":
                val = -9999
                try: val = float(pval)
                except: return self.leafCarbon
                self.leafCarbon = val
            elif pname == VegetationParameter.paramLabelList[10]: #"Stem Carbon":
                val = -9999
                try: val = float(pval)
                except: return self.stemCarbon
                self.stemCarbon = val
            elif pname == VegetationParameter.paramLabelList[11]: #"Debris Carbon":
                val = -9999
                try: val = float(pval)
                except: return self.debrisCarbon
                self.debrisCarbon = val
            elif pname == VegetationParameter.paramLabelList[12]: #"Labile Pool":
                val = -9999
                try: val = float(pval)
                except: return self.labilePool
                self.labilePool = val
            elif pname == VegetationParameter.paramLabelList[13]: #"Unshielded Cellulose Pool":
                val = -9999
                try: val = float(pval)
                except: return self.unshieldedCellulosePool
                self.unshieldedCellulosePool = val
            elif pname == VegetationParameter.paramLabelList[14]: #"Shielded Cellulose Pool":
                val = -9999
                try: val = float(pval)
                except: return self.shieldedCellulosePool
                self.shieldedCellulosePool = val
            elif pname == VegetationParameter.paramLabelList[15]: #"Lignin Pool":
                val = -9999
                try: val = float(pval)
                except: return self.ligninPool
                self.ligninPool = val
            elif pname == VegetationParameter.paramLabelList[16]: #"Nitrogen Labile Pool":
                val = -9999
                try: val = float(pval)
                except: return self.nitrogenLabilePool
                self.nitrogenLabilePool = val
        return None

    def showParameterValue(self):
        valueList = []

        if len(VegetationParameter.paramLabelList) == 17:
            #siteIndex
            pname = VegetationParameter.paramLabelList[0] #"Site Index"        #parameter name
            item = {"pname": pname, "pvalue": self.siteIndex}
            valueList.append(item)

            #vegetationNumber
            pname = VegetationParameter.paramLabelList[1] #"Vegetation No."
            item = {"pname": pname, "pvalue": self.vegetationNumber}
            valueList.append(item)

            #epcFileName
            pname = VegetationParameter.paramLabelList[2] #"EPC File Name"
            item = {"pname": pname, "pvalue": self.epcFileName}
            valueList.append(item)

            #standDensity
            pname = VegetationParameter.paramLabelList[3] #"Stand Density"
            item = {"pname": pname, "pvalue": self.standDensity}
            valueList.append(item)

            #startingTreeAge
            pname = VegetationParameter.paramLabelList[4] #"Starting Tree Age"
            item = {"pname": pname, "pvalue": self.startingTreeAge}
            valueList.append(item)

            #startingRootDepth
            pname = VegetationParameter.paramLabelList[5] #"Starting Root Depth"
            item = {"pname": pname, "pvalue": self.startingRootDepth}
            valueList.append(item)

            #treeGrowthClass
            pname = VegetationParameter.paramLabelList[6] #"Tree Growth Class"
            item = {"pname": pname, "pvalue": self.treeGrowthClass}
            valueList.append(item)

            #treeHeight
            pname = VegetationParameter.paramLabelList[7] #"Tree Height"
            item = {"pname": pname, "pvalue": self.treeHeight}
            valueList.append(item)

            #speciesSeqFile
            pname = VegetationParameter.paramLabelList[8] #"Species Seq. File"
            item = {"pname": pname, "pvalue": self.speciesSeqFile}
            valueList.append(item)

            #leafCarbon
            pname = VegetationParameter.paramLabelList[9] #"Leaf Carbon"
            item = {"pname": pname, "pvalue": self.leafCarbon}
            valueList.append(item)

            #stemCarbon
            pname = VegetationParameter.paramLabelList[10] #"Stem Carbon"
            item = {"pname": pname, "pvalue": self.stemCarbon}
            valueList.append(item)

            #debrisCarbon
            pname = VegetationParameter.paramLabelList[11] #"Debris Carbon"
            item = {"pname": pname, "pvalue": self.debrisCarbon}
            valueList.append(item)

            #labilePool
            pname = VegetationParameter.paramLabelList[12] #"Labile Pool"
            item = {"pname": pname, "pvalue": self.labilePool}
            valueList.append(item)

            #unshieldedCellulosePool
            pname = VegetationParameter.paramLabelList[13] #"Unshielded Cellulose Pool"
            item = {"pname": pname, "pvalue": self.unshieldedCellulosePool}
            valueList.append(item)

            #shieldedCellulosePool
            pname = VegetationParameter.paramLabelList[14] #"Shielded Cellulose Pool"
            item = {"pname": pname, "pvalue": self.shieldedCellulosePool}
            valueList.append(item)

            #ligninPool
            pname = VegetationParameter.paramLabelList[15] #"Lignin Pool"
            item = {"pname": pname, "pvalue": self.ligninPool}
            valueList.append(item)

            #nitrogenLabilePool
            pname = VegetationParameter.paramLabelList[16] #"Nitrogen Labile Pool"
            item = {"pname": pname, "pvalue": self.nitrogenLabilePool}
            valueList.append(item)

        return valueList

    def getParameterValue(self, pname):
        if len(VegetationParameter.paramLabelList) == 17:
            if pname == VegetationParameter.paramLabelList[0]: #"Site Index":
                    return self.siteIndex
            elif pname == VegetationParameter.paramLabelList[1]: #"Vegetation No.":
                return self.vegetationNumber
            elif pname == VegetationParameter.paramLabelList[2]: #"EPC File Name":
                return self.epcFileName
            elif pname == VegetationParameter.paramLabelList[3]: #"Stand Density":
                return self.standDensity
            elif pname == VegetationParameter.paramLabelList[4]: #"Starting Tree Age":
                return self.startingTreeAge
            elif pname == VegetationParameter.paramLabelList[5]: #"Starting Root Depth":
                return self.startingRootDepth
            elif pname == VegetationParameter.paramLabelList[6]: #"Tree Growth Class":
                return self.treeGrowthClass
            elif pname == VegetationParameter.paramLabelList[7]: #"Tree Height":
                return self.treeHeight
            elif pname == VegetationParameter.paramLabelList[8]: #"Species Seq. File":
                return self.speciesSeqFile
            elif pname == VegetationParameter.paramLabelList[9]: #"Leaf Carbon":
                return self.leafCarbon
            elif pname == VegetationParameter.paramLabelList[10]: #"Stem Carbon":
                return self.stemCarbon
            elif pname == VegetationParameter.paramLabelList[11]: #"Debris Carbon":
                return self.debrisCarbon
            elif pname == VegetationParameter.paramLabelList[12]: #"Labile Pool":
                return self.labilePool
            elif pname == VegetationParameter.paramLabelList[13]: #"Unshielded Cellulose Pool":
                return self.unshieldedCellulosePool
            elif pname == VegetationParameter.paramLabelList[14]: #"Shielded Cellulose Pool":
                return self.shieldedCellulosePool
            elif pname == VegetationParameter.paramLabelList[15]: #"Lignin Pool":
                return self.ligninPool
            elif pname == VegetationParameter.paramLabelList[16]: #"Nitrogen Labile Pool":
                return self.nitrogenLabilePool
        return None

class EpcParameter:
    #class level variables
    paramLabelList = ParamDomain.readEpcParameterLabelList()
    paramDomain = ParamDomain.readEpcParameterDomainList()

    @staticmethod
    def hasDomain(paramName):
        for key in EpcParameter.paramDomain:
            if key == paramName: return True
        return False

    @staticmethod
    def getDomain(paramName):
        domain = EpcParameter.paramDomain.get(paramName)
        return domain

    def __init__(self):
        self.growthForm = -1						    #2
        self.leafHabit = -1						        #3
        self.photosyntheticPathway = -1					#4
        self.phenologicalControlOption = -1				#5
        self.dayOfYearForStartOfNewLeafGrowth = -2		#6
        self.dayOfYearForMaxLitterFall = -1				#7
        self.growthPeriodDurationFraction = -1			#8
        self.litterfallPeriodDurationFraction = -1		#9
        self.offsetValueForParallelShift = -1			#10
        self.interceptConstantForLeafUnfolding = 0		#11
        self.slopeConstantForLeafUnfolding = 0			#12
        self.tempThresholdForChillDay = 0 				#13
        self.tempThresholdForThermalTime = 0 			#14
        self.criticalDayLengthForLitterfall = -1		#15
        self.soilTempForLitterfall = -273				#16
        self.prolongLitterfallFactor = -1				#17
        self.annualLeafTurnoverFraction = -1			#18
        self.annualFineRootTurnoverFraction = -1		#19
        self.annualCoarseRootTurnoverFraction = -1		#20
        self.annualLiveWoodTurnoverFraction = -1		#21
        self.annualWholePlantMortalityFraction = -1 	#22
        self.annualFireMortalityFraction = -1			#23
        self.ratioOfFineRootToLeafGrowth = -1			#24
        self.ratioOfStemToLeafGrowth = -1				#25
        self.ratioOfLiveWoodToTotalWood = -1			#26
        self.ratioOfCoarseRootToStemGrowth = -1			#27
        self.dailyGrowthProportion = -1					#28
        self.leafCarbonNitrogenMassRatio = -1			#29
        self.leafLitterCarbonNitrogenMassRatio = -1		#30
        self.fineRootCarbonNitrogenMassRatio = -1		#31
        self.coarseRootCarbonNitrogenMassRatio = -1		#32
        self.liveWoodCarbonNitrogenMassRatio = -1		#33
        self.deadWoodCarbonNitrogenMassRatio = -1		#34
        self.stemCoarseRootLitterFraction = -1			#35
        self.leafLitterLabileProportion = -1			#36
        self.leafLitterCelluloseProportion = -1			#37
        self.leafLitterLigninProportion = -1			#38
        self.fineRootLabileProportion = -1				#39
        self.fineRootCelluloseProportion = -1			#40
        self.fineRootLigninProportion = -1				#41
        self.deadWoodCelluloseProportion = -1			#42
        self.deadWoodLigninProportion = -1				#43
        self.canopyWaterInterceptionHeight = -1			#44
        self.stemWaterInterceptionHeight = -1			#45
        self.albedo = -1						        #46
        self.canopyLightExtinctionCoefficient = -1		#47
        self.allsidedToProjectedLeafAreaRatio = -1		#48
        self.canopyAverageSecificLeafArea = -1			#49
        self.ratioOfShadedToSunlitSLA = -1				#50
        self.maximumTreeHeight = -1					    #51
        self.stemWoodMassAtMaxHeight = -1				#52
        self.fractionOfLeafNitrogenInRubisco = -1		#53
        self.startAgeGrowthReduction = -1				#54
        self.endAgeGrowthReduction = -1					#55
        self.growthReductionFactor = -1					#56
        self.allocationReductionFactor = -1				#57
        self.nitrogenFixation = -1					    #58
        self.maxStomatalConductance = -1				#59
        self.cuticularConductance = -1					#60
        self.boundaryLayerConductance = -1				#61
        self.availableSoilWaterFactor = -1				#62
        self.wiltingPointFactor = -1					#63
        self.startOfConductanceReductionForVpd = -1		#64
        self.completeConductanceReductionForVpd = -1	#65
        self.thinningRuleOption = -1					#66
        self.thinningRuleFileName = ""					#67
        self.stemCarbonThresholdFor1stThinning = -1		#68
        self.firstThinningFraction = -1 				#69
        self.thinningRuleCoefficientB00 = -1			#70
        self.thinningRuleCoefficientB01 = -1			#71
        self.thinningRuleCoefficientB10 = -1			#72
        self.thinningRuleCoefficientB11 = -1			#73
        self.thinningRuleCoefficientB12 = -1			#74
        self.startHarvestCoefficientIntercept = -1		#75
        self.startHarvestCoefficientSlope = -1			#76
        self.thinningPeriod = -1					    #77
        self.ageOfClearCut = -1						    #78
        self.harvestCorrectionFactor = -1				#79
        self.exportFractionCoefficientIntercept = -1	#80
        self.exportfractionCoefficientSlope = -1		#81
        self.optimumTempForRootGrowth = -1				#82
        self.minimumTempForRootGrowth = -1				#83
        self.bdCoefForMaxRootGrowth = -1 				#84
        self.criticalPorosity = -1					    #85
        self.minPhAllowingRootGrowth = -1				#86
        self.maxPhAllowingRootGrowth = -1				#87
        self.minPhForOptimumRootGrowth = -1				#88
        self.maxPhForOptimumRootGrowth = -1				#89
        self.waterSaturationStress = -1					#90
        self.potentialVerticalRootGrowthRate = -1		#91
        self.maxAgeOfRootGrowth = -1					#92
        self.zetaPlantParameter = -1					#93

    def setParameterValue(self, posIndex, paramdesc, paramValue):
        if posIndex < 0:
            for key, value in EpcParameter.paramLabelList.items():
                if value == paramdesc:
                    posIndex = key + 1
                    break
	    
            if posIndex < 0: return None

        if len(EpcParameter.paramLabelList) == 92:
            ndx1 = int((posIndex-1)/27)
            ndx2 = posIndex % 27
            if ndx2 == 0: ndx2 = 27
            ndx3 = int((ndx2-1)/9)

            if ndx1 == 0:
                if ndx3 == 0:
                    if ndx2 <= 3:
                        if paramdesc == EpcParameter.paramLabelList[0]: # "Growth Form":
                            val = -9999
                            try: val = int(paramValue)
                            except: return self.growthForm
                            if val in [0,1]:
                                self.growthForm = val
                            else: return self.growthForm
                        elif paramdesc == EpcParameter.paramLabelList[1]: #"Leave Habit":
                            val = -9999
                            try: val = int(paramValue)
                            except: return self.leafHabit
                            if val in [0,1]:
                                self.leafHabit = val
                            else: return self.leafHabit
                        elif paramdesc == EpcParameter.paramLabelList[2]:
                            val = -9999
                            try: val = int(paramValue)
                            except: return self.photosyntheticPathway
                            if val in [0,1]:
                                self.photosyntheticPathway = val
                            else: return self.photosyntheticPathway
                    elif ndx2 <= 6:
                        if paramdesc == EpcParameter.paramLabelList[3]: #"Simulation Control Option for Phenology":
                            val = -9999
                            try: val = int(paramValue)
                            except: return self.phenologicalControlOption
                            if val in [0,1,2]:
                                self.phenologicalControlOption = val
                            else: return self.phenologicalControlOption
                        elif paramdesc == EpcParameter.paramLabelList[4]: #"Year-Day for Start of New Leaf Growth":
                            val = -9999
                            try: val = int(paramValue)
                            except: return self.dayOfYearForStartOfNewLeafGrowth
                            if val == -1 or (val > -1 and val < 365):
                                self.dayOfYearForStartOfNewLeafGrowth = val
                            else: return self.dayOfYearForStartOfNewLeafGrowth
                        elif paramdesc == EpcParameter.paramLabelList[5]:
                            val = -9999
                            try: val = int(paramValue)
                            except: return self.dayOfYearForMaxLitterFall
                            if val == -1 or (val > -1 and val < 365):
                                self.dayOfYearForMaxLitterFall = val
                            else: return self.dayOfYearForMaxLitterFall
                    else:
                        if paramdesc == EpcParameter.paramLabelList[6]: #"Growth Period Duration Fraction":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.growthPeriodDurationFraction
                            if val >= 0 and val <=1:
                                self.growthPeriodDurationFraction = val
                            else: return self.growthPeriodDurationFraction
                        elif paramdesc == EpcParameter.paramLabelList[7]: #"Litterfall Duration Fraction":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.litterfallPeriodDurationFraction
                            if val >= 0 and val <=1:
                                self.litterfallPeriodDurationFraction = val
                            else: return self.litterfallPeriodDurationFraction
                        elif paramdesc == EpcParameter.paramLabelList[8]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.offsetValueForParallelShift
                            self.offsetValueForParallelShift = val
                if ndx3 == 1:
                    if ndx2 <= 12:
                        if paramdesc == EpcParameter.paramLabelList[9]: #"Intercept Constant for Leaf Unfolding":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.interceptConstantForLeafUnfolding
                            self.interceptConstantForLeafUnfolding = val
                        elif paramdesc == EpcParameter.paramLabelList[10]: #"Slope Constant for Leaf Unfolding":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.slopeConstantForLeafUnfolding
                            self.slopeConstantForLeafUnfolding = val
                        elif paramdesc == EpcParameter.paramLabelList[11]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.tempThresholdForChillDay
                            self.tempThresholdForChillDay = paramValue
                    elif ndx2 <= 15:
                        if paramdesc == EpcParameter.paramLabelList[12]: #"Temp Threshold for Thermal Time":
                            val = -9999
                            try: val = float(paramValue)
                            except: return  self.tempThresholdForThermalTime
                            self.tempThresholdForThermalTime = paramValue
                        elif paramdesc == EpcParameter.paramLabelList[13]: #"Critical Day-length for Litterfall":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.criticalDayLengthForLitterfall
                            self.criticalDayLengthForLitterfall = paramValue
                        elif paramdesc == EpcParameter.paramLabelList[14]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.soilTempForLitterfall
                            self.soilTempForLitterfall = paramValue
                    else:
                        if paramdesc == EpcParameter.paramLabelList[15]: #"Prolong Litterfall Factor":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.prolongLitterfallFactor
                            self.prolongLitterfallFactor = paramValue
                        elif paramdesc == EpcParameter.paramLabelList[16]: #"Annual Leaf Turnover Fraction":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.annualLeafTurnoverFraction
                            self.annualLeafTurnoverFraction = val
                        elif paramdesc == EpcParameter.paramLabelList[17]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.annualFineRootTurnoverFraction
                            self.annualFineRootTurnoverFraction = val
                if ndx3 == 2:
                    if ndx2 <= 21:
                        if paramdesc == EpcParameter.paramLabelList[18]: #"Annual Coarse Root Turnover Fraction":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.annualCoarseRootTurnoverFraction
                            self.annualCoarseRootTurnoverFraction = val
                        elif paramdesc == EpcParameter.paramLabelList[19]: #"Annual Live Wood Turnover Fraction":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.annualLiveWoodTurnoverFraction
                            self.annualLiveWoodTurnoverFraction = val
                        elif paramdesc == EpcParameter.paramLabelList[20]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.annualWholePlantMortalityFraction
                            self.annualWholePlantMortalityFraction = val
                    elif ndx2 <= 24:
                        if paramdesc == EpcParameter.paramLabelList[21]: #"Annual Fire Mortality Fraction":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.annualFireMortalityFraction
                            self.annualFireMortalityFraction = val
                        elif paramdesc == EpcParameter.paramLabelList[22]: #"Fine Root to Leaf Growth Ratio":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.ratioOfFineRootToLeafGrowth
                            self.ratioOfFineRootToLeafGrowth = val
                        elif paramdesc == EpcParameter.paramLabelList[23]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.ratioOfStemToLeafGrowth
                            self.ratioOfStemToLeafGrowth = val
                    else:
                        if paramdesc == EpcParameter.paramLabelList[24]: #"Live Wood to Total Wood Ratio":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.ratioOfLiveWoodToTotalWood
                            self.ratioOfLiveWoodToTotalWood = val
                        elif paramdesc == EpcParameter.paramLabelList[25]: #"Coarse Root to Stem Growth Ratio":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.ratioOfCoarseRootToStemGrowth
                            self.ratioOfCoarseRootToStemGrowth = val
                        elif paramdesc == EpcParameter.paramLabelList[26]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.dailyGrowthProportion
                            self.dailyGrowthProportion = val
            elif ndx1 == 1:
                if ndx3 == 0:
                    if ndx2 <= 3:
                        if paramdesc == EpcParameter.paramLabelList[27]: #"C-N Mass Ratio in Leaf":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.leafCarbonNitrogenMassRatio
                            self.leafCarbonNitrogenMassRatio = val
                        elif paramdesc == EpcParameter.paramLabelList[28]: #"C-N Mass Ratio in Leaf Litter":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.leafLitterCarbonNitrogenMassRatio
                            self.leafLitterCarbonNitrogenMassRatio = val
                        elif paramdesc == EpcParameter.paramLabelList[29]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.fineRootCarbonNitrogenMassRatio
                            self.fineRootCarbonNitrogenMassRatio = val
                    elif ndx2 <= 6:
                        if paramdesc == EpcParameter.paramLabelList[30]: #"C-N Mass Ratio in Coarse Root":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.coarseRootCarbonNitrogenMassRatio
                            self.coarseRootCarbonNitrogenMassRatio = val
                        elif paramdesc == EpcParameter.paramLabelList[31]: #"C-N Mass Ratio in Live Wood":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.liveWoodCarbonNitrogenMassRatio
                            self.liveWoodCarbonNitrogenMassRatio = val
                        elif paramdesc == EpcParameter.paramLabelList[32]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.deadWoodCarbonNitrogenMassRatio
                            self.deadWoodCarbonNitrogenMassRatio = val
                    else:
                        if paramdesc == EpcParameter.paramLabelList[33]: #"Litter Fraction of Stem/Coarse Root":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.stemCoarseRootLitterFraction
                            self.stemCoarseRootLitterFraction = val
                        elif paramdesc == EpcParameter.paramLabelList[34]: #"Leaf Litter Labile Proportion":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.leafLitterLabileProportion
                            self.leafLitterLabileProportion = val
                        elif paramdesc == EpcParameter.paramLabelList[35]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.leafLitterCelluloseProportion
                            self.leafLitterCelluloseProportion = val
                elif ndx3 == 1:
                    if ndx2 <= 12:
                        if paramdesc == EpcParameter.paramLabelList[36]: #"Leaf Litter Lignin Proportion":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.leafLitterLigninProportion
                            self.leafLitterLigninProportion = val
                        elif paramdesc == EpcParameter.paramLabelList[37]: #"Fine Root Labile Proportion":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.fineRootLabileProportion
                            self.fineRootLabileProportion = val
                        elif paramdesc == EpcParameter.paramLabelList[38]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.fineRootCelluloseProportion
                            self.fineRootCelluloseProportion = val
                    elif ndx2 <= 15:
                        if paramdesc == EpcParameter.paramLabelList[39]: #"Fine Root Lignin Proportion":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.fineRootLigninProportion
                            self.fineRootLigninProportion = val
                        elif paramdesc == EpcParameter.paramLabelList[40]: #"Dead Wood Cellulose Proportion":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.deadWoodCelluloseProportion
                            self.deadWoodCelluloseProportion = val
                        elif paramdesc == EpcParameter.paramLabelList[41]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.deadWoodLigninProportion
                            self.deadWoodLigninProportion = val
                    else:
                        if paramdesc == EpcParameter.paramLabelList[42]: #"Canopy Water Interception Height":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.canopyWaterInterceptionHeight
                            self.canopyWaterInterceptionHeight = val
                        elif paramdesc == EpcParameter.paramLabelList[43]: #"Stem Water Interception Height":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.stemWaterInterceptionHeight
                            self.stemWaterInterceptionHeight = val
                        elif paramdesc == EpcParameter.paramLabelList[44]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.albedo
                            self.albedo = val
                else:
                    if ndx2 <= 21:
                        if paramdesc == EpcParameter.paramLabelList[45]: #"Canopy Light Extinction Coefficient":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.canopyLightExtinctionCoefficient
                            self.canopyLightExtinctionCoefficient = val
                        elif paramdesc == EpcParameter.paramLabelList[46]: #"All-sided to Projected Leaf Area Ratio":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.allsidedToProjectedLeafAreaRatio
                            self.allsidedToProjectedLeafAreaRatio = val
                        elif paramdesc == EpcParameter.paramLabelList[47]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.canopyAverageSecificLeafArea
                            self.canopyAverageSecificLeafArea = val
                    elif ndx2 <= 24:
                        if paramdesc == EpcParameter.paramLabelList[48]: #"Ratio of Shaded to Sunlit SLA":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.ratioOfShadedToSunlitSLA
                            self.ratioOfShadedToSunlitSLA = val
                        elif paramdesc == EpcParameter.paramLabelList[49]: #"Maximum Tree Height":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.maximumTreeHeight
                            self.maximumTreeHeight = val
                        elif paramdesc == EpcParameter.paramLabelList[50]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.stemWoodMassAtMaxHeight
                            self.stemWoodMassAtMaxHeight = val
                    else:
                        if paramdesc == EpcParameter.paramLabelList[51]: #"Fraction of Leaf Nitrogen in Rubisco":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.fractionOfLeafNitrogenInRubisco
                            self.fractionOfLeafNitrogenInRubisco = val
                        elif paramdesc == EpcParameter.paramLabelList[52]: #"Start of Age Growth Reduction":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.startAgeGrowthReduction
                            self.startAgeGrowthReduction = val
                        elif paramdesc == EpcParameter.paramLabelList[53]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.endAgeGrowthReduction
                            self.endAgeGrowthReduction = val
            elif ndx1 == 2:
                if ndx3 == 0:
                    if ndx2 <= 3:
                        if paramdesc == EpcParameter.paramLabelList[54]: #"Growth Reduction Factor":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.growthReductionFactor
                            self.growthReductionFactor = val
                        elif paramdesc == EpcParameter.paramLabelList[55]: #"Allocation Reduction Factor":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.allocationReductionFactor
                            self.allocationReductionFactor = val
                        elif paramdesc == EpcParameter.paramLabelList[56]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.nitrogenFixation
                            self.nitrogenFixation = val
                    elif ndx2 <= 6:
                        if paramdesc == EpcParameter.paramLabelList[57]: #"Maximum Stomatal Conductance":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.maxStomatalConductance
                            self.maxStomatalConductance = val
                        elif paramdesc == EpcParameter.paramLabelList[58]: #"Cuticular Conductance":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.cuticularConductance
                            self.cuticularConductance = val
                        elif paramdesc == EpcParameter.paramLabelList[59]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.boundaryLayerConductance
                            self.boundaryLayerConductance = val
                    else:
                        if paramdesc == EpcParameter.paramLabelList[60]: #"Available Soil Water Factor":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.availableSoilWaterFactor
                            self.availableSoilWaterFactor = val
                        elif paramdesc == EpcParameter.paramLabelList[61]: #"Wilting Point Factor":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.wiltingPointFactor
                            self.wiltingPointFactor = val
                        elif paramdesc == EpcParameter.paramLabelList[62]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.startOfConductanceReductionForVpd
                            self.startOfConductanceReductionForVpd = val
                if ndx3 == 1:
                    if ndx2 <= 12:
                        if paramdesc == EpcParameter.paramLabelList[63]: #"Complete Conductance Reduction for Vpd":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.completeConductanceReductionForVpd
                            self.completeConductanceReductionForVpd = val
                        elif paramdesc == EpcParameter.paramLabelList[64]: #"Thinning Rule Option":
                            val = -9999
                            try: val = int(paramValue)
                            except: return self.thinningRuleOption
                            self.thinningRuleOption = val
                        elif paramdesc == EpcParameter.paramLabelList[65]:
                            self.thinningRuleFileName = paramValue
                    elif ndx2 <= 15:
                        if paramdesc == EpcParameter.paramLabelList[66]: #"First Thinning Stem Carbon Threshold":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.stemCarbonThresholdFor1stThinning
                            self.stemCarbonThresholdFor1stThinning = val
                        elif paramdesc == EpcParameter.paramLabelList[67]: #"First Thinning Fraction":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.firstThinningFraction
                            self.firstThinningFraction = val
                        elif paramdesc == EpcParameter.paramLabelList[68]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.thinningRuleCoefficientB00
                            self.thinningRuleCoefficientB00 = val
                    else:
                        if paramdesc == EpcParameter.paramLabelList[69]: #"Thinning Rule Coefficient B01":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.thinningRuleCoefficientB01
                            self.thinningRuleCoefficientB01 = val
                        elif paramdesc == EpcParameter.paramLabelList[70]: #"Thinning Rule Coefficient B10":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.thinningRuleCoefficientB10
                            self.thinningRuleCoefficientB10 = val
                        elif paramdesc == EpcParameter.paramLabelList[71]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.thinningRuleCoefficientB11
                            self.thinningRuleCoefficientB11 = val
                else:
                    if ndx2 <= 21:
                        if paramdesc == EpcParameter.paramLabelList[72]: #"Thinning Rule Coefficient B12":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.thinningRuleCoefficientB12
                            self.thinningRuleCoefficientB12 = val
                        elif paramdesc == EpcParameter.paramLabelList[73]: #"Start Harvest Coefficient - Intercept":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.startHarvestCoefficientIntercept
                            self.startHarvestCoefficientIntercept = val
                        elif paramdesc == EpcParameter.paramLabelList[74]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.startHarvestCoefficientSlope
                            self.startHarvestCoefficientSlope = val
                    if ndx2 <= 24:
                        if paramdesc == EpcParameter.paramLabelList[75]: #"Thinning Period":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.thinningPeriod
                            self.thinningPeriod = val
                        elif paramdesc == EpcParameter.paramLabelList[76]: #"Age of Clear Cut":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.ageOfClearCut
                            self.ageOfClearCut = val
                        elif paramdesc == EpcParameter.paramLabelList[77]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.harvestCorrectionFactor
                            self.harvestCorrectionFactor = val
                    else:
                        if paramdesc == EpcParameter.paramLabelList[78]: #"Export Fraction Coefficient - Intercept":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.exportFractionCoefficientIntercept
                            self.exportFractionCoefficientIntercept = val
                        elif paramdesc == EpcParameter.paramLabelList[79]: #"Export Fraction Coefficient Slope":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.exportfractionCoefficientSlope
                            self.exportfractionCoefficientSlope = val
                        elif paramdesc == EpcParameter.paramLabelList[80]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.optimumTempForRootGrowth
                            self.optimumTempForRootGrowth = val
            else:
                if ndx3 == 0:
                    if ndx2 <= 3:
                        if paramdesc == EpcParameter.paramLabelList[81]: #"Minimum Temp for Root Growth":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.minimumTempForRootGrowth
                            self.minimumTempForRootGrowth = val
                        elif paramdesc == EpcParameter.paramLabelList[82]: #"Bulk Density Coef. for Max Root Growth":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.bdCoefForMaxRootGrowth
                            self.bdCoefForMaxRootGrowth = val
                        elif paramdesc == EpcParameter.paramLabelList[83]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.criticalPorosity
                            self.criticalPorosity = val
                    elif ndx2 <= 6:
                        if paramdesc == EpcParameter.paramLabelList[84]: #"Minimum pH allowing Root Growth":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.minPhAllowingRootGrowth
                            self.minPhAllowingRootGrowth = val
                        elif paramdesc == EpcParameter.paramLabelList[85]: #"Maximum pH allowing Root Growth":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.maxPhAllowingRootGrowth
                            self.maxPhAllowingRootGrowth = val
                        elif paramdesc == EpcParameter.paramLabelList[86]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.minPhForOptimumRootGrowth
                            self.minPhForOptimumRootGrowth = val
                    else:
                        if paramdesc == EpcParameter.paramLabelList[87]: #"Maximum pH for Optimum Root Growth":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.maxPhForOptimumRootGrowth
                            self.maxPhForOptimumRootGrowth =  val
                        elif paramdesc == EpcParameter.paramLabelList[88]: #"Water Saturation Stress":
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.waterSaturationStress
                            self.waterSaturationStress = val
                        elif paramdesc == EpcParameter.paramLabelList[89]:
                            val = -9999
                            try: val = float(paramValue)
                            except: return self.potentialVerticalRootGrowthRate
                            self.potentialVerticalRootGrowthRate = val
                else:
                    # if ndx2 < 12:
                    if paramdesc == EpcParameter.paramLabelList[90]: #"Maximum Age of Root Growth":
                        val = -9999
                        try: val = float(paramValue)
                        except: return self.maxAgeOfRootGrowth
                        self.maxAgeOfRootGrowth = val
                    elif paramdesc == EpcParameter.paramLabelList[91]:
                        val = -9999
                        try: val = float(paramValue)
                        except: return self.zetaPlantParameter
                        self.zetaPlantParameter = val
        return None

    def compare(vegParamList):
        indic = {}           #input dictionary; structure: {parameterName1: valueList1, parameterName2: valueList2}

        for item in vegParamList:
            #growthForm
            pname = "Growth Form"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.growthForm]
            else: temp.append(item.growthForm)

            #leafHabit
            pname = "Leave Habit"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.leafHabit]
            else: temp.append(item.leafHabit)

            #photosyntheticPathway
            pname = "Photosynthetic Pathway"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.photosyntheticPathway]
            else: temp.append(item.photosyntheticPathway)

            #phenologicalControlOption
            pname = "Simulation Control Option for Phenology"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.phenologicalControlOption]
            else: temp.append(item.phenologicalControlOption)

            #dayOfYearForStartOfNewLeafGrowth
            pname = "Year-Day for Start of New Leaf Growth"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.dayOfYearForStartOfNewLeafGrowth]
            else: temp.append(item.dayOfYearForStartOfNewLeafGrowth)

            #dayOfYearForMaxLitterFall
            pname = "Year-Day for Max Litter Fall"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.dayOfYearForMaxLitterFall]
            else: temp.append(item.dayOfYearForMaxLitterFall)

            #growthPeriodDurationFraction
            pname = "Growth Period Duration Fraction"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.growthPeriodDurationFraction]
            else: temp.append(item.growthPeriodDurationFraction)

            #litterfallPeriodDurationFraction
            pname = "Litterfall Duration Fraction"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.litterfallPeriodDurationFraction]
            else: temp.append(item.litterfallPeriodDurationFraction)

            #offsetValueForParallelShift
            pname = "Offset Value for Parallel Shift"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.offsetValueForParallelShift]
            else: temp.append(item.offsetValueForParallelShift)

            #interceptConstantForLeafUnfolding
            pname = "Intercept Constant for Leaf Unfolding"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.interceptConstantForLeafUnfolding]
            else: temp.append(item.interceptConstantForLeafUnfolding)

            #slopeConstantForLeafUnfolding
            pname = "Slope Constant for Leaf Unfolding"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.slopeConstantForLeafUnfolding]
            else: temp.append(item.slopeConstantForLeafUnfolding)

            #tempThresholdForChillDay
            pname = "Temperature Threshold for Chill Day"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.tempThresholdForChillDay]
            else: temp.append(item.tempThresholdForChillDay)

            #tempThresholdForThermalTime
            pname = "Temp Threshold for Thermal Time"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.tempThresholdForThermalTime]
            else: temp.append(item.tempThresholdForThermalTime)

            #criticalDayLengthForLitterfall
            pname = "Critical Day-length for Litterfall"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.criticalDayLengthForLitterfall]
            else: temp.append(item.criticalDayLengthForLitterfall)

            #soilTempForLitterfall
            pname = "Soil Temp. for Litterfall"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.soilTempForLitterfall]
            else: temp.append(item.soilTempForLitterfall)

            #prolongLitterfallFactor
            pname = "Prolong Litterfall Factor"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.prolongLitterfallFactor]
            else: temp.append(item.prolongLitterfallFactor)

            #annualLeafTurnoverFraction
            pname = "Annual Leaf Turnover Fraction"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.annualLeafTurnoverFraction]
            else: temp.append(item.annualLeafTurnoverFraction)

            #annualFineRootTurnoverFraction
            pname = "Annual Fine Root Turnover Fraction"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.annualFineRootTurnoverFraction]
            else: temp.append(item.annualFineRootTurnoverFraction)

            #annualCoarseRootTurnoverFraction
            pname = "Annual Coarse Root Turnover Fraction"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.annualCoarseRootTurnoverFraction]
            else: temp.append(item.annualCoarseRootTurnoverFraction)

            #annualLiveWoodTurnoverFraction
            pname = "Annual Live Wood Turnover Fraction"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.annualLiveWoodTurnoverFraction]
            else: temp.append(item.annualLiveWoodTurnoverFraction)

            #annualWholePlantMortalityFraction
            pname = "Annual Whole Plant Mortality Fraction"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.annualWholePlantMortalityFraction]
            else: temp.append(item.annualWholePlantMortalityFraction)

            #annualFireMortalityFraction
            pname = "Annual Fire Mortality Fraction"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.annualFireMortalityFraction]
            else: temp.append(item.annualFireMortalityFraction)

            #ratioOfFineRootToLeafGrowth
            pname = "Fine Root to Leaf Growth Ratio"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.ratioOfFineRootToLeafGrowth]
            else: temp.append(item.ratioOfFineRootToLeafGrowth)

            #ratioOfStemToLeafGrowth
            pname = "Stem to Leaf Growth Ratio"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.ratioOfStemToLeafGrowth]
            else: temp.append(item.ratioOfStemToLeafGrowth)

            #ratioOfLiveWoodToTotalWood
            pname = "Live Wood to Total Wood Ratio"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.ratioOfLiveWoodToTotalWood]
            else: temp.append(item.ratioOfLiveWoodToTotalWood)

            #ratioOfCoarseRootToStemGrowth
            pname = "Coarse Root to Stem Growth Ratio"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.ratioOfCoarseRootToStemGrowth]
            else: temp.append(item.ratioOfCoarseRootToStemGrowth)

            #dailyGrowthProportion
            pname = "Daily Growth Proportion"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.dailyGrowthProportion]
            else: temp.append(item.dailyGrowthProportion)

            #leafCarbonNitrogenMassRatio
            pname = "C-N Mass Ratio in Leaf"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.leafCarbonNitrogenMassRatio]
            else: temp.append(item.leafCarbonNitrogenMassRatio)

            #leafLitterCarbonNitrogenMassRatio
            pname = "C-N Mass Ratio in Leaf Litter"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.leafLitterCarbonNitrogenMassRatio]
            else: temp.append(item.leafLitterCarbonNitrogenMassRatio)

            #fineRootCarbonNitrogenMassRatio
            pname = "C-N Mass Ratio in Fine Root"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.fineRootCarbonNitrogenMassRatio]
            else: temp.append(item.fineRootCarbonNitrogenMassRatio)

            #coarseRootCarbonNitrogenMassRatio
            pname = "C-N Mass Ratio in Coarse Root"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.coarseRootCarbonNitrogenMassRatio]
            else: temp.append(item.coarseRootCarbonNitrogenMassRatio)
            #liveWoodCarbonNitrogenMassRatio
            pname = "C-N Mass Ratio in Live Wood"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.liveWoodCarbonNitrogenMassRatio]
            else: temp.append(item.liveWoodCarbonNitrogenMassRatio)

            #deadWoodCarbonNitrogenMassRatio
            pname = "C-N Mass Ratio in Dead Wood"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.deadWoodCarbonNitrogenMassRatio]
            else: temp.append(item.deadWoodCarbonNitrogenMassRatio)

            #stemCoarseRootLitterFraction
            pname = "Litter Fraction of Stem/Coarse Root"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.stemCoarseRootLitterFraction]
            else: temp.append(item.stemCoarseRootLitterFraction)

            #leafLitterLabileProportion
            pname = "Leaf Litter Labile Proportion"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.leafLitterLabileProportion]
            else: temp.append(item.leafLitterLabileProportion)

            #leafLitterCelluloseProportion
            pname = "Leaf Litter Cellulose Proportion"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.leafLitterCelluloseProportion]
            else: temp.append(item.leafLitterCelluloseProportion)

            #leafLitterLigninProportion
            pname = "Leaf Litter Lignin Proportion"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.leafLitterLigninProportion]
            else: temp.append(item.leafLitterLigninProportion)

            #fineRootLabileProportion
            pname = "Fine Root Labile Proportion"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.fineRootLabileProportion]
            else: temp.append(item.fineRootLabileProportion)

            #fineRootCelluloseProportion
            pname = "Fine Root Cellulose Proportion"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.fineRootCelluloseProportion]
            else: temp.append(item.fineRootCelluloseProportion)

            #fineRootLigninProportion
            pname = "Fine Root Lignin Proportion"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.fineRootLigninProportion]
            else: temp.append(item.fineRootLigninProportion)

            #deadWoodCelluloseProportion
            pname = "Dead Wood Cellulose Proportion"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.deadWoodCelluloseProportion]
            else: temp.append(item.deadWoodCelluloseProportion)

            #deadWoodLigninProportion
            pname = "Dead Wood Lignin Proportion"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.deadWoodLigninProportion]
            else: temp.append(item.deadWoodLigninProportion)

            #canopyWaterInterceptionHeight
            pname = "Canopy Water Interception Height"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.canopyWaterInterceptionHeight]
            else: temp.append(item.canopyWaterInterceptionHeight)

            #stemWaterInterceptionHeight
            pname = "Stem Water Interception Height"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.stemWaterInterceptionHeight]
            else: temp.append(item.stemWaterInterceptionHeight)

            #albedo
            pname = "Albedo"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.albedo]
            else: temp.append(item.albedo)

            #canopyLightExtinctionCoefficient
            pname = "Canopy Light Extinction Coefficient"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.canopyLightExtinctionCoefficient]
            else: temp.append(item.canopyLightExtinctionCoefficient)

            #allsidedToProjectedLeafAreaRatio
            pname = "All-sided to Projected Leaf Area Ratio"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.allsidedToProjectedLeafAreaRatio]
            else: temp.append(item.allsidedToProjectedLeafAreaRatio)

            #canopyAverageSecificLeafArea
            pname = "Canopy Average Secific Leaf Area"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.canopyAverageSecificLeafArea]
            else: temp.append(item.canopyAverageSecificLeafArea)

            #ratioOfShadedToSunlitSLA
            pname = "Ratio of Shaded to Sunlit SLA"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.ratioOfShadedToSunlitSLA]
            else: temp.append(item.ratioOfShadedToSunlitSLA)

            #maximumTreeHeight
            pname = "Maximum Tree Height"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.maximumTreeHeight]
            else: temp.append(item.maximumTreeHeight)

            #stemWoodMassAtMaxHeight
            pname = "Stem Wood Mass at Max Height"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.stemWoodMassAtMaxHeight]
            else: temp.append(item.stemWoodMassAtMaxHeight)

            #fractionOfLeafNitrogenInRubisco
            pname = "Fraction of Leaf Nitrogen in Rubisco"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.fractionOfLeafNitrogenInRubisco]
            else: temp.append(item.fractionOfLeafNitrogenInRubisco)

            #startAgeGrowthReduction
            pname = "Start of Age Growth Reduction"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.startAgeGrowthReduction]
            else: temp.append(item.startAgeGrowthReduction)

            #endAgeGrowthReduction
            pname = "End of Age Growth Reduction"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.endAgeGrowthReduction]
            else: temp.append(item.endAgeGrowthReduction)

            #growthReductionFactor
            pname = "Growth Reduction Factor"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.growthReductionFactor]
            else: temp.append(item.growthReductionFactor)

            #allocationReductionFactor
            pname = "Allocation Reduction Factor"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.allocationReductionFactor]
            else: temp.append(item.allocationReductionFactor)

            #nitrogenFixation
            pname = "Nitrogen Fixation"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.nitrogenFixation]
            else: temp.append(item.nitrogenFixation)

            #maxStomatalConductance
            pname = "Maximum Stomatal Conductance"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.maxStomatalConductance]
            else: temp.append(item.maxStomatalConductance)

            #cuticularConductance
            pname = "Cuticular Conductance"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.cuticularConductance]
            else: temp.append(item.cuticularConductance)

            #boundaryLayerConductance
            pname = "Boundary Layer Conductance"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.boundaryLayerConductance]
            else: temp.append(item.boundaryLayerConductance)

            #availableSoilWaterFactor
            pname = "Available Soil Water Factor"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.availableSoilWaterFactor]
            else: temp.append(item.availableSoilWaterFactor)

            #wiltingPointFactor
            pname = "Wilting Point Factor"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.wiltingPointFactor]
            else: temp.append(item.wiltingPointFactor)

            #startOfConductanceReductionForVpd
            pname = "Start of Conductance Reduction for Vpd"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.startOfConductanceReductionForVpd]
            else: temp.append(item.startOfConductanceReductionForVpd)

            #completeConductanceReductionForVpd
            pname = "Complete Conductance Reduction for Vpd"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.completeConductanceReductionForVpd]
            else: temp.append(item.completeConductanceReductionForVpd)

            #thinningRuleOption
            pname = "Thinning Rule Option"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.thinningRuleOption]
            else: temp.append(item.thinningRuleOption)

            #thinningRuleFileName
            pname = "File Containing Thinning Rule Table"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.thinningRuleFileName]
            else: temp.append(item.thinningRuleFileName)

            #stemCarbonThresholdFor1stThinning
            pname = "First Thinning Stem Carbon Threshold"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.stemCarbonThresholdFor1stThinning]
            else: temp.append(item.stemCarbonThresholdFor1stThinning)

            #firstThinningFraction
            pname = "First Thinning Fraction"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.firstThinningFraction]
            else: temp.append(item.firstThinningFraction)

            #thinningRuleCoefficientB00
            pname = "Thinning Rule Coefficient B00"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.thinningRuleCoefficientB00]
            else: temp.append(item.thinningRuleCoefficientB00)

            #thinningRuleCoefficientB01
            pname = "Thinning Rule Coefficient B01"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.thinningRuleCoefficientB01]
            else: temp.append(item.thinningRuleCoefficientB01)

            #thinningRuleCoefficientB10
            pname = "Thinning Rule Coefficient B10"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.thinningRuleCoefficientB10]
            else: temp.append(item.thinningRuleCoefficientB10)

            #thinningRuleCoefficientB11
            pname = "Thinning Rule Coefficient B11"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.thinningRuleCoefficientB11]
            else: temp.append(item.thinningRuleCoefficientB11)

            #thinningRuleCoefficientB12
            pname = "Thinning Rule Coefficient B12"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.thinningRuleCoefficientB12]
            else: temp.append(item.thinningRuleCoefficientB12)

            #startHarvestCoefficientIntercept
            pname = "Start Harvest Coefficient - Intercept"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.startHarvestCoefficientIntercept]
            else: temp.append(item.startHarvestCoefficientIntercept)

            #startHarvestCoefficientSlope
            pname = "Start Harvest Coefficient - Slope"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.startHarvestCoefficientSlope]
            else: temp.append(item.startHarvestCoefficientSlope)

            #thinningPeriod
            pname = "Thinning Period"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.thinningPeriod]
            else: temp.append(item.thinningPeriod)

            #ageOfClearCut
            pname = "Age of Clear Cut"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.ageOfClearCut]
            else: temp.append(item.ageOfClearCut)

            #harvestCorrectionFactor
            pname = "Harvest Correction Factor"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.harvestCorrectionFactor]
            else: temp.append(item.harvestCorrectionFactor)

            #exportFractionCoefficientIntercept
            pname = "Export Fraction Coefficient - Intercept"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.exportFractionCoefficientIntercept]
            else: temp.append(item.exportFractionCoefficientIntercept)

            #exportfractionCoefficientSlope
            pname = "Export Fraction Coefficient Slope"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.exportfractionCoefficientSlope]
            else: temp.append(item.exportfractionCoefficientSlope)

            #optimumTempForRootGrowth
            pname = "Optimum Temp for Root Growth"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.optimumTempForRootGrowth]
            else: temp.append(item.optimumTempForRootGrowth)

            #minimumTempForRootGrowth
            pname = "Minimum Temp for Root Growth"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.minimumTempForRootGrowth]
            else: temp.append(item.minimumTempForRootGrowth)

            #bdCoefForMaxRootGrowth
            pname = "Bulk Density Coef. for Max Root Growth"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.bdCoefForMaxRootGrowth]
            else: temp.append(item.bdCoefForMaxRootGrowth)

            #criticalPorosity
            pname = "Critical Porosity"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.criticalPorosity]
            else: temp.append(item.criticalPorosity)

            #minPhAllowingRootGrowth
            pname = "Minimum pH allowing Root Growth"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.minPhAllowingRootGrowth]
            else: temp.append(item.minPhAllowingRootGrowth)

            #maxPhAllowingRootGrowth
            pname = "Maximum pH allowing Root Growth"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.maxPhAllowingRootGrowth]
            else: temp.append(item.maxPhAllowingRootGrowth)

            #minPhForOptimumRootGrowth
            pname = "Minimum pH for Optimum Root Growth"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.minPhForOptimumRootGrowth]
            else: temp.append(item.minPhForOptimumRootGrowth)

            #maxPhForOptimumRootGrowth
            pname = "Maximum pH for Optimum Root Growth"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.maxPhForOptimumRootGrowth]
            else: temp.append(item.maxPhForOptimumRootGrowth)

            #waterSaturationStress
            pname = "Water Saturation Stress"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.waterSaturationStress]
            else: temp.append(item.waterSaturationStress)

            #potentialVerticalRootGrowthRate
            pname = "Potential Vertical Root Growth Rate"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.potentialVerticalRootGrowthRate]
            else: temp.append(item.potentialVerticalRootGrowthRate)

            #maxAgeOfRootGrowth
            pname = "Maximum Age of Root Growth"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.maxAgeOfRootGrowth]
            else: temp.append(item.maxAgeOfRootGrowth)

            #zetaPlantParameter
            pname = "Zeta Coefficient"
            temp = indic.get(pname)
            if temp is None: indic[pname] = [item.zetaPlantParameter]
            else: temp.append(item.zetaPlantParameter)

        outdic = {}         #output dictionary; structure={parameter1: valueList1, parameter2: valueList2, ...}
        for param, value in indic.items():
            if len(set(value)) > 1:
                outdic[param] = value

        return outdic

    def showParameterValue(self):
        valueList = []

        if len(EpcParameter.paramLabelList) == 92:
            #growthForm
            pname = EpcParameter.paramLabelList[0] # "Growth Form"
            item = {"pname": pname, "pvalue": self.growthForm}
            valueList.append(item)

            #leafHabit
            pname = EpcParameter.paramLabelList[1] #"Leave Habit"
            item = {"pname": pname, "pvalue": self.leafHabit}
            valueList.append(item)

            #photosyntheticPathway
            pname = EpcParameter.paramLabelList[2] #"Photosynthetic Pathway"
            item = {"pname": pname, "pvalue": self.photosyntheticPathway}
            valueList.append(item)

            #phenologicalControlOption
            pname = EpcParameter.paramLabelList[3] #"Simulation Control Option for Phenology"
            item = {"pname": pname, "pvalue": self.phenologicalControlOption}
            valueList.append(item)

            #dayOfYearForStartOfNewLeafGrowth
            pname = EpcParameter.paramLabelList[4] #"Year-Day for Start of New Leaf Growth"
            item = {"pname": pname, "pvalue": self.dayOfYearForStartOfNewLeafGrowth}
            valueList.append(item)

            #dayOfYearForMaxLitterFall
            pname = EpcParameter.paramLabelList[5] #"Year-Day for Max Litter Fall"
            item = {"pname": pname, "pvalue": self.dayOfYearForMaxLitterFall}
            valueList.append(item)

            #growthPeriodDurationFraction
            pname = EpcParameter.paramLabelList[6] #"Growth Period Duration Fraction"
            item = {"pname": pname, "pvalue": self.growthPeriodDurationFraction}
            valueList.append(item)

            #litterfallPeriodDurationFraction
            pname = EpcParameter.paramLabelList[7] #"Litterfall Duration Fraction"
            item = {"pname": pname, "pvalue": self.litterfallPeriodDurationFraction}
            valueList.append(item)

            #offsetValueForParallelShift
            pname = EpcParameter.paramLabelList[8] #"Offset Value for Parallel Shift"
            item = {"pname": pname, "pvalue": self.offsetValueForParallelShift}
            valueList.append(item)

            #interceptConstantForLeafUnfolding
            pname = EpcParameter.paramLabelList[9] #"Intercept Constant for Leaf Unfolding"
            item = {"pname": pname, "pvalue": self.interceptConstantForLeafUnfolding}
            valueList.append(item)

            #slopeConstantForLeafUnfolding
            pname = EpcParameter.paramLabelList[10] #"Slope Constant for Leaf Unfolding"
            item = {"pname": pname, "pvalue": self.slopeConstantForLeafUnfolding}
            valueList.append(item)

            #tempThresholdForChillDay
            pname = EpcParameter.paramLabelList[11] #"Temperature Threshold for Chill Day"
            item = {"pname": pname, "pvalue": self.tempThresholdForChillDay}
            valueList.append(item)

            #tempThresholdForThermalTime
            pname = EpcParameter.paramLabelList[12] #"Temp Threshold for Thermal Time"
            item = {"pname": pname, "pvalue": self.tempThresholdForThermalTime}
            valueList.append(item)

            #criticalDayLengthForLitterfall
            pname = EpcParameter.paramLabelList[13] #"Critical Day-length for Litterfall"
            item = {"pname": pname, "pvalue": self.criticalDayLengthForLitterfall}
            valueList.append(item)

            #soilTempForLitterfall
            pname = EpcParameter.paramLabelList[14] #"Soil Temp. for Litterfall"
            item = {"pname": pname, "pvalue": self.soilTempForLitterfall}
            valueList.append(item)

            #prolongLitterfallFactor
            pname = EpcParameter.paramLabelList[15] #"Prolong Litterfall Factor"
            item = {"pname": pname, "pvalue": self.prolongLitterfallFactor}
            valueList.append(item)

            #annualLeafTurnoverFraction
            pname = EpcParameter.paramLabelList[16] #"Annual Leaf Turnover Fraction"
            item = {"pname": pname, "pvalue": self.annualLeafTurnoverFraction}
            valueList.append(item)

            #annualFineRootTurnoverFraction
            pname = EpcParameter.paramLabelList[17] #"Annual Fine Root Turnover Fraction"
            item = {"pname": pname, "pvalue": self.annualFineRootTurnoverFraction}
            valueList.append(item)

            #annualCoarseRootTurnoverFraction
            pname = EpcParameter.paramLabelList[18] #"Annual Coarse Root Turnover Fraction"
            item = {"pname": pname, "pvalue": self.annualCoarseRootTurnoverFraction}
            valueList.append(item)

            #annualLiveWoodTurnoverFraction
            pname = EpcParameter.paramLabelList[19] #"Annual Live Wood Turnover Fraction"
            item = {"pname": pname, "pvalue": self.annualLiveWoodTurnoverFraction}
            valueList.append(item)

            #annualWholePlantMortalityFraction
            pname = EpcParameter.paramLabelList[20] #"Annual Whole Plant Mortality Fraction"
            item = {"pname": pname, "pvalue": self.annualWholePlantMortalityFraction}
            valueList.append(item)

            #annualFireMortalityFraction
            pname = EpcParameter.paramLabelList[21] #"Annual Fire Mortality Fraction"
            item = {"pname": pname, "pvalue": self.annualFireMortalityFraction}
            valueList.append(item)

            #ratioOfFineRootToLeafGrowth
            pname = EpcParameter.paramLabelList[22] #"Fine Root to Leaf Growth Ratio"
            item = {"pname": pname, "pvalue": self.ratioOfFineRootToLeafGrowth}
            valueList.append(item)

            #ratioOfStemToLeafGrowth
            pname = EpcParameter.paramLabelList[23] #"Stem to Leaf Growth Ratio"
            item = {"pname": pname, "pvalue": self.ratioOfStemToLeafGrowth}
            valueList.append(item)

            #ratioOfLiveWoodToTotalWood
            pname = EpcParameter.paramLabelList[24] #"Live Wood to Total Wood Ratio"
            item = {"pname": pname, "pvalue": self.ratioOfLiveWoodToTotalWood}
            valueList.append(item)

            #ratioOfCoarseRootToStemGrowth
            pname = EpcParameter.paramLabelList[25] #"Coarse Root to Stem Growth Ratio"
            item = {"pname": pname, "pvalue": self.ratioOfCoarseRootToStemGrowth}
            valueList.append(item)

            #dailyGrowthProportion
            pname = EpcParameter.paramLabelList[26] #"Daily Growth Proportion"
            item = {"pname": pname, "pvalue": self.dailyGrowthProportion}
            valueList.append(item)

            #leafCarbonNitrogenMassRatio
            pname = EpcParameter.paramLabelList[27] #"C-N Mass Ratio in Leaf"
            item = {"pname": pname, "pvalue": self.leafCarbonNitrogenMassRatio}
            valueList.append(item)

            #leafLitterCarbonNitrogenMassRatio
            pname = EpcParameter.paramLabelList[28] #"C-N Mass Ratio in Leaf Litter"
            item = {"pname": pname, "pvalue": self.leafLitterCarbonNitrogenMassRatio}
            valueList.append(item)

            #fineRootCarbonNitrogenMassRatio
            pname = EpcParameter.paramLabelList[29] #"C-N Mass Ratio in Fine Root"
            item = {"pname": pname, "pvalue": self.fineRootCarbonNitrogenMassRatio}
            valueList.append(item)

            #coarseRootCarbonNitrogenMassRatio
            pname = EpcParameter.paramLabelList[30] #"C-N Mass Ratio in Coarse Root"
            item = {"pname": pname, "pvalue": self.coarseRootCarbonNitrogenMassRatio}
            valueList.append(item)

            #liveWoodCarbonNitrogenMassRatio
            pname = EpcParameter.paramLabelList[31] #"C-N Mass Ratio in Live Wood"
            item = {"pname": pname, "pvalue": self.liveWoodCarbonNitrogenMassRatio}
            valueList.append(item)

            #deadWoodCarbonNitrogenMassRatio
            pname = EpcParameter.paramLabelList[32] #"C-N Mass Ratio in Dead Wood"
            item = {"pname": pname, "pvalue": self.deadWoodCarbonNitrogenMassRatio}
            valueList.append(item)

            #stemCoarseRootLitterFraction
            pname = EpcParameter.paramLabelList[33] #"Litter Fraction of Stem/Coarse Root"
            item = {"pname": pname, "pvalue": self.stemCoarseRootLitterFraction}
            valueList.append(item)

            #leafLitterLabileProportion
            pname = EpcParameter.paramLabelList[34] #"Leaf Litter Labile Proportion"
            item = {"pname": pname, "pvalue": self.leafLitterLabileProportion}
            valueList.append(item)

            #leafLitterCelluloseProportion
            pname = EpcParameter.paramLabelList[35] #"Leaf Litter Cellulose Proportion"
            item = {"pname": pname, "pvalue": self.leafLitterCelluloseProportion}
            valueList.append(item)

            #leafLitterLigninProportion
            pname = EpcParameter.paramLabelList[36] #"Leaf Litter Lignin Proportion"
            item = {"pname": pname, "pvalue": self.leafLitterLigninProportion}
            valueList.append(item)

            #fineRootLabileProportion
            pname = EpcParameter.paramLabelList[37] #"Fine Root Labile Proportion"
            item = {"pname": pname, "pvalue": self.fineRootLabileProportion}
            valueList.append(item)

            #fineRootCelluloseProportion
            pname = EpcParameter.paramLabelList[38] #"Fine Root Cellulose Proportion"
            item = {"pname": pname, "pvalue": self.fineRootCelluloseProportion}
            valueList.append(item)

            #fineRootLigninProportion
            pname = EpcParameter.paramLabelList[39] #"Fine Root Lignin Proportion"
            item = {"pname": pname, "pvalue": self.fineRootLigninProportion}
            valueList.append(item)

            #deadWoodCelluloseProportion
            pname = EpcParameter.paramLabelList[40] #"Dead Wood Cellulose Proportion"
            item = {"pname": pname, "pvalue": self.deadWoodCelluloseProportion}
            valueList.append(item)

            #deadWoodLigninProportion
            pname = EpcParameter.paramLabelList[41] #"Dead Wood Lignin Proportion"
            item = {"pname": pname, "pvalue": self.deadWoodLigninProportion}
            valueList.append(item)

            #canopyWaterInterceptionHeight
            pname = EpcParameter.paramLabelList[42] #"Canopy Water Interception Height"
            item = {"pname": pname, "pvalue": self.canopyWaterInterceptionHeight}
            valueList.append(item)

            #stemWaterInterceptionHeight
            pname = EpcParameter.paramLabelList[43] #"Stem Water Interception Height"
            item = {"pname": pname, "pvalue": self.stemWaterInterceptionHeight}
            valueList.append(item)

            #albedo
            pname = EpcParameter.paramLabelList[44] #"Albedo"
            item = {"pname": pname, "pvalue": self.albedo}
            valueList.append(item)

            #canopyLightExtinctionCoefficient
            pname = EpcParameter.paramLabelList[45] #"Canopy Light Extinction Coefficient"
            item = {"pname": pname, "pvalue": self.canopyLightExtinctionCoefficient}
            valueList.append(item)

            #allsidedToProjectedLeafAreaRatio
            pname = EpcParameter.paramLabelList[46] #"All-sided to Projected Leaf Area Ratio"
            item = {"pname": pname, "pvalue": self.allsidedToProjectedLeafAreaRatio}
            valueList.append(item)

            #canopyAverageSecificLeafArea
            pname = EpcParameter.paramLabelList[47] #"Canopy Average Secific Leaf Area"
            item = {"pname": pname, "pvalue": self.canopyAverageSecificLeafArea}
            valueList.append(item)

            #ratioOfShadedToSunlitSLA
            pname = EpcParameter.paramLabelList[48] #"Ratio of Shaded to Sunlit SLA"
            item = {"pname": pname, "pvalue": self.ratioOfShadedToSunlitSLA}
            valueList.append(item)

            #maximumTreeHeight
            pname = EpcParameter.paramLabelList[49] #"Maximum Tree Height"
            item = {"pname": pname, "pvalue": self.maximumTreeHeight}
            valueList.append(item)

            #stemWoodMassAtMaxHeight
            pname = EpcParameter.paramLabelList[50] #"Stem Wood Mass at Max Height"
            item = {"pname": pname, "pvalue": self.stemWoodMassAtMaxHeight}
            valueList.append(item)

            #fractionOfLeafNitrogenInRubisco
            pname = EpcParameter.paramLabelList[51] #"Fraction of Leaf Nitrogen in Rubisco"
            item = {"pname": pname, "pvalue": self.fractionOfLeafNitrogenInRubisco}
            valueList.append(item)

            #startAgeGrowthReduction
            pname = EpcParameter.paramLabelList[52] #"Start of Age Growth Reduction"
            item = {"pname": pname, "pvalue": self.startAgeGrowthReduction}
            valueList.append(item)

            #endAgeGrowthReduction
            pname = EpcParameter.paramLabelList[53] #"End of Age Growth Reduction"
            item = {"pname": pname, "pvalue": self.endAgeGrowthReduction}
            valueList.append(item)

            #growthReductionFactor
            pname = EpcParameter.paramLabelList[54] #"Growth Reduction Factor"
            item = {"pname": pname, "pvalue": self.growthReductionFactor}
            valueList.append(item)

            #allocationReductionFactor
            pname = EpcParameter.paramLabelList[55] #"Allocation Reduction Factor"
            item = {"pname": pname, "pvalue": self.allocationReductionFactor}
            valueList.append(item)

            #nitrogenFixation
            pname = EpcParameter.paramLabelList[56] #"Nitrogen Fixation"
            item = {"pname": pname, "pvalue": self.nitrogenFixation}
            valueList.append(item)

            #maxStomatalConductance
            pname = EpcParameter.paramLabelList[57] #"Maximum Stomatal Conductance"
            item = {"pname": pname, "pvalue": self.maxStomatalConductance}
            valueList.append(item)

            #cuticularConductance
            pname = EpcParameter.paramLabelList[58] #"Cuticular Conductance"
            item = {"pname": pname, "pvalue": self.cuticularConductance}
            valueList.append(item)

            #boundaryLayerConductance
            pname = EpcParameter.paramLabelList[59] #"Boundary Layer Conductance"
            item = {"pname": pname, "pvalue": self.boundaryLayerConductance}
            valueList.append(item)

            #availableSoilWaterFactor
            pname = EpcParameter.paramLabelList[60] #"Available Soil Water Factor"
            item = {"pname": pname, "pvalue": self.availableSoilWaterFactor}
            valueList.append(item)

            #wiltingPointFactor
            pname = EpcParameter.paramLabelList[61] #"Wilting Point Factor"
            item = {"pname": pname, "pvalue": self.wiltingPointFactor}
            valueList.append(item)

            #startOfConductanceReductionForVpd
            pname = EpcParameter.paramLabelList[62] #"Start of Conductance Reduction for Vpd"
            item = {"pname": pname, "pvalue": self.startOfConductanceReductionForVpd}
            valueList.append(item)

            #completeConductanceReductionForVpd
            pname = EpcParameter.paramLabelList[63] #"Complete Conductance Reduction for Vpd"
            item = {"pname": pname, "pvalue": self.completeConductanceReductionForVpd}
            valueList.append(item)

            #thinningRuleOption
            pname = EpcParameter.paramLabelList[64] #"Thinning Rule Option"
            item = {"pname": pname, "pvalue": self.thinningRuleOption}
            valueList.append(item)

            #thinningRuleFileName
            pname = EpcParameter.paramLabelList[65] #"File Containing Thinning Rule Table"
            item = {"pname": pname, "pvalue": self.thinningRuleFileName}
            valueList.append(item)

            #stemCarbonThresholdFor1stThinning
            pname = EpcParameter.paramLabelList[66] #"First Thinning Stem Carbon Threshold"
            item = {"pname": pname, "pvalue": self.stemCarbonThresholdFor1stThinning}
            valueList.append(item)

            #firstThinningFraction
            pname = EpcParameter.paramLabelList[67] #"First Thinning Fraction"
            item = {"pname": pname, "pvalue": self.firstThinningFraction}
            valueList.append(item)

            #thinningRuleCoefficientB00
            pname = EpcParameter.paramLabelList[68] #"Thinning Rule Coefficient B00"
            item = {"pname": pname, "pvalue": self.thinningRuleCoefficientB00}
            valueList.append(item)

            #thinningRuleCoefficientB01
            pname = EpcParameter.paramLabelList[69] #"Thinning Rule Coefficient B01"
            item = {"pname": pname, "pvalue": self.thinningRuleCoefficientB01}
            valueList.append(item)

            #thinningRuleCoefficientB10
            pname = EpcParameter.paramLabelList[70] #"Thinning Rule Coefficient B10"
            item = {"pname": pname, "pvalue": self.thinningRuleCoefficientB10}
            valueList.append(item)

            #thinningRuleCoefficientB11
            pname = EpcParameter.paramLabelList[71] #"Thinning Rule Coefficient B11"
            item = {"pname": pname, "pvalue": self.thinningRuleCoefficientB11}
            valueList.append(item)

            #thinningRuleCoefficientB12
            pname = EpcParameter.paramLabelList[72] #"Thinning Rule Coefficient B12"
            item = {"pname": pname, "pvalue": self.thinningRuleCoefficientB12}
            valueList.append(item)

            #startHarvestCoefficientIntercept
            pname = EpcParameter.paramLabelList[73] #"Start Harvest Coefficient - Intercept"
            item = {"pname": pname, "pvalue": self.startHarvestCoefficientIntercept}
            valueList.append(item)

            #startHarvestCoefficientSlope
            pname = EpcParameter.paramLabelList[74] #"Start Harvest Coefficient - Slope"
            item = {"pname": pname, "pvalue": self.startHarvestCoefficientSlope}
            valueList.append(item)

            #thinningPeriod
            pname = EpcParameter.paramLabelList[75] #"Thinning Period"
            item = {"pname": pname, "pvalue": self.thinningPeriod}
            valueList.append(item)

            #ageOfClearCut
            pname = EpcParameter.paramLabelList[76] #"Age of Clear Cut"
            item = {"pname": pname, "pvalue": self.ageOfClearCut}
            valueList.append(item)

            #harvestCorrectionFactor
            pname = EpcParameter.paramLabelList[77] #"Harvest Correction Factor"
            item = {"pname": pname, "pvalue": self.harvestCorrectionFactor}
            valueList.append(item)

            #exportFractionCoefficientIntercept
            pname = EpcParameter.paramLabelList[78] #"Export Fraction Coefficient - Intercept"
            item = {"pname": pname, "pvalue": self.exportFractionCoefficientIntercept}
            valueList.append(item)

            #exportfractionCoefficientSlope
            pname = EpcParameter.paramLabelList[79] #"Export Fraction Coefficient Slope"
            item = {"pname": pname, "pvalue": self.exportfractionCoefficientSlope}
            valueList.append(item)

            #optimumTempForRootGrowth
            pname = EpcParameter.paramLabelList[80] #"Optimum Temp for Root Growth"
            item = {"pname": pname, "pvalue": self.optimumTempForRootGrowth}
            valueList.append(item)

            #minimumTempForRootGrowth
            pname = EpcParameter.paramLabelList[81] #"Minimum Temp for Root Growth"
            item = {"pname": pname, "pvalue": self.minimumTempForRootGrowth}
            valueList.append(item)

            #bdCoefForMaxRootGrowth
            pname = EpcParameter.paramLabelList[82] #"Bulk Density Coef. for Max Root Growth"
            item = {"pname": pname, "pvalue": self.bdCoefForMaxRootGrowth}
            valueList.append(item)

            #criticalPorosity
            pname = EpcParameter.paramLabelList[83] #"Critical Porosity"
            item = {"pname": pname, "pvalue": self.criticalPorosity}
            valueList.append(item)

            #minPhAllowingRootGrowth
            pname = EpcParameter.paramLabelList[84] #"Minimum pH allowing Root Growth"
            item = {"pname": pname, "pvalue": self.minPhAllowingRootGrowth}
            valueList.append(item)

            #maxPhAllowingRootGrowth
            pname = EpcParameter.paramLabelList[85] #"Maximum pH allowing Root Growth"
            item = {"pname": pname, "pvalue": self.maxPhAllowingRootGrowth}
            valueList.append(item)

            #minPhForOptimumRootGrowth
            pname = EpcParameter.paramLabelList[86] #"Minimum pH for Optimum Root Growth"
            item = {"pname": pname, "pvalue": self.minPhForOptimumRootGrowth}
            valueList.append(item)

            #maxPhForOptimumRootGrowth
            pname = EpcParameter.paramLabelList[87] #"Maximum pH for Optimum Root Growth"
            item = {"pname": pname, "pvalue": self.maxPhForOptimumRootGrowth}
            valueList.append(item)

            #waterSaturationStress
            pname = EpcParameter.paramLabelList[88] #"Water Saturation Stress"
            item = {"pname": pname, "pvalue": self.waterSaturationStress}
            valueList.append(item)

            #potentialVerticalRootGrowthRate
            pname = EpcParameter.paramLabelList[89] #"Potential Vertical Root Growth Rate"
            item = {"pname": pname, "pvalue": self.potentialVerticalRootGrowthRate}
            valueList.append(item)

            #maxAgeOfRootGrowth
            pname = EpcParameter.paramLabelList[90] #"Maximum Age of Root Growth"
            item = {"pname": pname, "pvalue": self.maxAgeOfRootGrowth}
            valueList.append(item)

            #zetaPlantParameter
            pname = EpcParameter.paramLabelList[91] #"Zeta Coefficient"
            item = {"pname": pname, "pvalue": self.zetaPlantParameter}
            valueList.append(item)

        return valueList

    def getParameterValue(self, paramdesc="", posIndex=-1): #paramdesc = parameter label, posIndex: starting from 1
        if paramdesc == "" and posIndex == -1: return None
        else:
            if paramdesc == "": paramdesc = EpcParameter.paramLabelList[posIndex - 1]
            elif posIndex == -1:
                for key, value in EpcParameter.paramLabelList.items():
                    if value == paramdesc:
                        posIndex = key + 1
                        break

        if posIndex > -1 and len(EpcParameter.paramLabelList) == 92:
            ndx1 = int((posIndex-1)/27)
            ndx2 = posIndex % 27
            if ndx2 == 0: ndx2 = 27
            ndx3 = int((ndx2-1)/9)

            if ndx1 == 0:
                if ndx3 == 0:
                    if ndx2 <= 3:
                        if paramdesc == EpcParameter.paramLabelList[0]: # "Growth Form":
                            return self.growthForm
                        elif paramdesc == EpcParameter.paramLabelList[1]: #"Leave Habit":
                            return self.leafHabit
                        elif paramdesc == EpcParameter.paramLabelList[2]:
                            return self.photosyntheticPathway
                    elif ndx2 <= 6:
                        if paramdesc == EpcParameter.paramLabelList[3]: #"Simulation Control Option for Phenology":
                            return self.phenologicalControlOption
                        elif paramdesc == EpcParameter.paramLabelList[4]: #"Year-Day for Start of New Leaf Growth":
                            return self.dayOfYearForStartOfNewLeafGrowth
                        elif paramdesc == EpcParameter.paramLabelList[5]:
                            return self.dayOfYearForMaxLitterFall
                    else:
                        if paramdesc == EpcParameter.paramLabelList[6]: #"Growth Period Duration Fraction":
                            return self.growthPeriodDurationFraction
                        elif paramdesc == EpcParameter.paramLabelList[7]: #"Litterfall Duration Fraction":
                            return self.litterfallPeriodDurationFraction
                        elif paramdesc == EpcParameter.paramLabelList[8]:
                            return self.offsetValueForParallelShift
                if ndx3 == 1:
                    if ndx2 <= 12:
                        if paramdesc == EpcParameter.paramLabelList[9]: #"Intercept Constant for Leaf Unfolding":
                            return self.interceptConstantForLeafUnfolding
                        elif paramdesc == EpcParameter.paramLabelList[10]: #"Slope Constant for Leaf Unfolding":
                            return self.slopeConstantForLeafUnfolding
                        elif paramdesc == EpcParameter.paramLabelList[11]:
                            return self.tempThresholdForChillDay
                    elif ndx2 <= 15:
                        if paramdesc == EpcParameter.paramLabelList[12]: #"Temp Threshold for Thermal Time":
                            return  self.tempThresholdForThermalTime
                        elif paramdesc == EpcParameter.paramLabelList[13]: #"Critical Day-length for Litterfall":
                            return self.criticalDayLengthForLitterfall
                        elif paramdesc == EpcParameter.paramLabelList[14]:
                            return self.soilTempForLitterfall
                    else:
                        if paramdesc == EpcParameter.paramLabelList[15]: #"Prolong Litterfall Factor":
                            return self.prolongLitterfallFactor
                        elif paramdesc == EpcParameter.paramLabelList[16]: #"Annual Leaf Turnover Fraction":
                            return self.annualLeafTurnoverFraction
                        elif paramdesc == EpcParameter.paramLabelList[17]:
                            return self.annualFineRootTurnoverFraction
                if ndx3 == 2:
                    if ndx2 <= 21:
                        if paramdesc == EpcParameter.paramLabelList[18]: #"Annual Coarse Root Turnover Fraction":
                            return self.annualCoarseRootTurnoverFraction
                        elif paramdesc == EpcParameter.paramLabelList[19]: #"Annual Live Wood Turnover Fraction":
                            return self.annualLiveWoodTurnoverFraction
                        elif paramdesc == EpcParameter.paramLabelList[20]:
                            return self.annualWholePlantMortalityFraction
                    elif ndx2 <= 24:
                        if paramdesc == EpcParameter.paramLabelList[21]: #"Annual Fire Mortality Fraction":
                            return self.annualFireMortalityFraction
                        elif paramdesc == EpcParameter.paramLabelList[22]: #"Fine Root to Leaf Growth Ratio":
                            return self.ratioOfFineRootToLeafGrowth
                        elif paramdesc == EpcParameter.paramLabelList[23]:
                            return self.ratioOfStemToLeafGrowth
                    else:
                        if paramdesc == EpcParameter.paramLabelList[24]: #"Live Wood to Total Wood Ratio":
                            return self.ratioOfLiveWoodToTotalWood
                        elif paramdesc == EpcParameter.paramLabelList[25]: #"Coarse Root to Stem Growth Ratio":
                            return self.ratioOfCoarseRootToStemGrowth
                        elif paramdesc == EpcParameter.paramLabelList[26]:
                            return self.dailyGrowthProportion
            elif ndx1 == 1:
                if ndx3 == 0:
                    if ndx2 <= 3:
                        if paramdesc == EpcParameter.paramLabelList[27]: #"C-N Mass Ratio in Leaf":
                            return self.leafCarbonNitrogenMassRatio
                        elif paramdesc == EpcParameter.paramLabelList[28]: #"C-N Mass Ratio in Leaf Litter":
                            return self.leafLitterCarbonNitrogenMassRatio
                        elif paramdesc == EpcParameter.paramLabelList[29]:
                            return self.fineRootCarbonNitrogenMassRatio
                    elif ndx2 <= 6:
                        if paramdesc == EpcParameter.paramLabelList[30]: #"C-N Mass Ratio in Coarse Root":
                            return self.coarseRootCarbonNitrogenMassRatio
                        elif paramdesc == EpcParameter.paramLabelList[31]: #"C-N Mass Ratio in Live Wood":
                            return self.liveWoodCarbonNitrogenMassRatio
                        elif paramdesc == EpcParameter.paramLabelList[32]:
                            return self.deadWoodCarbonNitrogenMassRatio
                    else:
                        if paramdesc == EpcParameter.paramLabelList[33]: #"Litter Fraction of Stem/Coarse Root":
                            return self.stemCoarseRootLitterFraction
                        elif paramdesc == EpcParameter.paramLabelList[34]: #"Leaf Litter Labile Proportion":
                            return self.leafLitterLabileProportion
                        elif paramdesc == EpcParameter.paramLabelList[35]:
                            return self.leafLitterCelluloseProportion
                elif ndx3 == 1:
                    if ndx2 <= 12:
                        if paramdesc == EpcParameter.paramLabelList[36]: #"Leaf Litter Lignin Proportion":
                            return self.leafLitterLigninProportion
                        elif paramdesc == EpcParameter.paramLabelList[37]: #"Fine Root Labile Proportion":
                            return self.fineRootLabileProportion
                        elif paramdesc == EpcParameter.paramLabelList[38]:
                            return self.fineRootCelluloseProportion
                    elif ndx2 <= 15:
                        if paramdesc == EpcParameter.paramLabelList[39]: #"Fine Root Lignin Proportion":
                            return self.fineRootLigninProportion
                        elif paramdesc == EpcParameter.paramLabelList[40]: #"Dead Wood Cellulose Proportion":
                            return self.deadWoodCelluloseProportion
                        elif paramdesc == EpcParameter.paramLabelList[41]:
                            return self.deadWoodLigninProportion
                    else:
                        if paramdesc == EpcParameter.paramLabelList[42]: #"Canopy Water Interception Height":
                            return self.canopyWaterInterceptionHeight
                        elif paramdesc == EpcParameter.paramLabelList[43]: #"Stem Water Interception Height":
                            return self.stemWaterInterceptionHeight
                        elif paramdesc == EpcParameter.paramLabelList[44]:
                            return self.albedo
                else:
                    if ndx2 <= 21:
                        if paramdesc == EpcParameter.paramLabelList[45]: #"Canopy Light Extinction Coefficient":
                            return self.canopyLightExtinctionCoefficient
                        elif paramdesc == EpcParameter.paramLabelList[46]: #"All-sided to Projected Leaf Area Ratio":
                            return self.allsidedToProjectedLeafAreaRatio
                        elif paramdesc == EpcParameter.paramLabelList[47]:
                            return self.canopyAverageSecificLeafArea
                    elif ndx2 <= 24:
                        if paramdesc == EpcParameter.paramLabelList[48]: #"Ratio of Shaded to Sunlit SLA":
                            return self.ratioOfShadedToSunlitSLA
                        elif paramdesc == EpcParameter.paramLabelList[49]: #"Maximum Tree Height":
                            return self.maximumTreeHeight
                        elif paramdesc == EpcParameter.paramLabelList[50]:
                            return self.stemWoodMassAtMaxHeight
                    else:
                        if paramdesc == EpcParameter.paramLabelList[51]: #"Fraction of Leaf Nitrogen in Rubisco":
                            return self.fractionOfLeafNitrogenInRubisco
                        elif paramdesc == EpcParameter.paramLabelList[52]: #"Start of Age Growth Reduction":
                            return self.startAgeGrowthReduction
                        elif paramdesc == EpcParameter.paramLabelList[53]:
                            return self.endAgeGrowthReduction
            elif ndx1 == 2:
                if ndx3 == 0:
                    if ndx2 <= 3:
                        if paramdesc == EpcParameter.paramLabelList[54]: #"Growth Reduction Factor":
                            return self.growthReductionFactor
                        elif paramdesc == EpcParameter.paramLabelList[55]: #"Allocation Reduction Factor":
                            return self.allocationReductionFactor
                        elif paramdesc == EpcParameter.paramLabelList[56]:
                            return self.nitrogenFixation
                    elif ndx2 <= 6:
                        if paramdesc == EpcParameter.paramLabelList[57]: #"Maximum Stomatal Conductance":
                            return self.maxStomatalConductance
                        elif paramdesc == EpcParameter.paramLabelList[58]: #"Cuticular Conductance":
                            return self.cuticularConductance
                        elif paramdesc == EpcParameter.paramLabelList[59]:
                            return self.boundaryLayerConductance
                    else:
                        if paramdesc == EpcParameter.paramLabelList[60]: #"Available Soil Water Factor":
                            return self.availableSoilWaterFactor
                        elif paramdesc == EpcParameter.paramLabelList[61]: #"Wilting Point Factor":
                            return self.wiltingPointFactor
                        elif paramdesc == EpcParameter.paramLabelList[62]:
                            return self.startOfConductanceReductionForVpd
                if ndx3 == 1:
                    if ndx2 <= 12:
                        if paramdesc == EpcParameter.paramLabelList[63]: #"Complete Conductance Reduction for Vpd":
                            return self.completeConductanceReductionForVpd
                        elif paramdesc == EpcParameter.paramLabelList[64]: #"Thinning Rule Option":
                            return self.thinningRuleOption
                        elif paramdesc == EpcParameter.paramLabelList[65]:
                            return self.thinningRuleFileName
                    elif ndx2 <= 15:
                        if paramdesc == EpcParameter.paramLabelList[66]: #"First Thinning Stem Carbon Threshold":
                            return self.stemCarbonThresholdFor1stThinning
                        elif paramdesc == EpcParameter.paramLabelList[67]: #"First Thinning Fraction":
                            return self.firstThinningFraction
                        elif paramdesc == EpcParameter.paramLabelList[68]:
                            return self.thinningRuleCoefficientB00
                    else:
                        if paramdesc == EpcParameter.paramLabelList[69]: #"Thinning Rule Coefficient B01":
                            return self.thinningRuleCoefficientB01
                        elif paramdesc == EpcParameter.paramLabelList[70]: #"Thinning Rule Coefficient B10":
                            return self.thinningRuleCoefficientB10
                        elif paramdesc == EpcParameter.paramLabelList[71]:
                            return self.thinningRuleCoefficientB11
                else:
                    if ndx2 <= 21:
                        if paramdesc == EpcParameter.paramLabelList[72]: #"Thinning Rule Coefficient B12":
                            return self.thinningRuleCoefficientB12
                        elif paramdesc == EpcParameter.paramLabelList[73]: #"Start Harvest Coefficient - Intercept":
                            return self.startHarvestCoefficientIntercept
                        elif paramdesc == EpcParameter.paramLabelList[74]:
                            return self.startHarvestCoefficientSlope
                    if ndx2 <= 24:
                        if paramdesc == EpcParameter.paramLabelList[75]: #"Thinning Period":
                            return self.thinningPeriod
                        elif paramdesc == EpcParameter.paramLabelList[76]: #"Age of Clear Cut":
                            return self.ageOfClearCut
                        elif paramdesc == EpcParameter.paramLabelList[77]:
                            return self.harvestCorrectionFactor
                    else:
                        if paramdesc == EpcParameter.paramLabelList[78]: #"Export Fraction Coefficient - Intercept":
                            return self.exportFractionCoefficientIntercept
                        elif paramdesc == EpcParameter.paramLabelList[79]: #"Export Fraction Coefficient Slope":
                            return self.exportfractionCoefficientSlope
                        elif paramdesc == EpcParameter.paramLabelList[80]:
                            return self.optimumTempForRootGrowth
            else:
                if ndx3 == 0:
                    if ndx2 <= 3:
                        if paramdesc == EpcParameter.paramLabelList[81]: #"Minimum Temp for Root Growth":
                            return self.minimumTempForRootGrowth
                        elif paramdesc == EpcParameter.paramLabelList[82]: #"Bulk Density Coef. for Max Root Growth":
                            return self.bdCoefForMaxRootGrowth
                        elif paramdesc == EpcParameter.paramLabelList[83]:
                            return self.criticalPorosity
                    elif ndx2 <= 6:
                        if paramdesc == EpcParameter.paramLabelList[84]: #"Minimum pH allowing Root Growth":
                            return self.minPhAllowingRootGrowth
                        elif paramdesc == EpcParameter.paramLabelList[85]: #"Maximum pH allowing Root Growth":
                            return self.maxPhAllowingRootGrowth
                        elif paramdesc == EpcParameter.paramLabelList[86]:
                            return self.minPhForOptimumRootGrowth
                    else:
                        if paramdesc == EpcParameter.paramLabelList[87]: #"Maximum pH for Optimum Root Growth":
                            return self.maxPhForOptimumRootGrowth
                        elif paramdesc == EpcParameter.paramLabelList[88]: #"Water Saturation Stress":
                            return self.waterSaturationStress
                        elif paramdesc == EpcParameter.paramLabelList[89]:
                            return self.potentialVerticalRootGrowthRate
                else:
                    # if ndx2 < 12:
                    if paramdesc == EpcParameter.paramLabelList[90]: #"Maximum Age of Root Growth":
                        return self.maxAgeOfRootGrowth
                    elif paramdesc == EpcParameter.paramLabelList[91]:
                        return self.zetaPlantParameter
        return None

class SoilProfile:
    def __init__(self):
        self.profileName = ""
        self.soilLayerList = []

    def sortSoilProfileByDepth(self):
        nextRun = True
        while nextRun:
            nextRun = False
            for i in range(len(self.soilLayerList) - 1):
                if self.soilLayerList[i].depthOfHorizon > self.soilLayerList[i+1].depthOfHorizon:
                    nextRun = True
                    temp = self.soilLayerList[i]
                    self.soilLayerList[i] = self.soilLayerList[i+1]
                    self.soilLayerList[i+1] = temp


class SoilLayer():
    #class variable
    paramLabelList = ParamDomain.readSoilParameterLabelList()

    def __init__(self):
        self.horizonName = "Empty"		            #type: string
        self.depthOfHorizon = -9999			        #type: number
        self.layerThickness = -9999			        #type: number
        self.correctionFactor = -9999			    #type: number
        self.soilTexture = ""			            #type: string, have a domain
        self.soilPh = -9999				            #type: number, may have a range
        self.organicCarbonContent = -9999		    #type: number, range 0-1
        self.gravelContent = -9999			        #type: number, range 0-1
        self.sandContent = -9999			        #type: number, range 0-1
        self.siltContent = -9999			        #type: number, range 0-1
        self.clayContent = -9999			        #type: number, range 0-1
        self.bulkDensity = -9999			        #type: number
        self.poreVolume = -9999				        #type: number, range 0-1
        self.waterCapacity = -9999			        #type: number
        self.permanentWiltingPoint = -9999		    #type: number
        self.saturatedHydraulicConductivity = -9999	#type: number


    def setParameterValue(self, pname, pvalue):
        if len(SoilLayer.paramLabelList) == 16:
            if pname == SoilLayer.paramLabelList[0]: # "Horizon Name":
                self.horizonName = pvalue
            elif pname == SoilLayer.paramLabelList[1]: #"Lower Horizon Border":
                val = -9999
                try: val = int(pvalue)
                except: return self.depthOfHorizon
                self.depthOfHorizon = val
            elif pname == SoilLayer.paramLabelList[2]: #"Layer Thickness":
                val = -9999
                try: val = int(pvalue)
                except: return self.layerThickness
                if val in [2, 5, 10, 20]:
                    self.layerThickness = val
                else: return self.layerThickness
            elif pname == SoilLayer.paramLabelList[3]: #"Correction Factor":
                val = -9999
                try: val = float(pvalue)
                except: return self.correctionFactor
                self.correctionFactor = val
            elif pname == SoilLayer.paramLabelList[4]: #"Texture":
                if pvalue in ParamDomain.readSoilTextureList():   #case sensitive
                    self.soilTexture = pvalue
                    if self.soilTexture == "O":
                        self.sandContent = 0
                        self.siltContent = 0
                        self.clayContent = 0
                else: return self.soilTexture
            elif pname == SoilLayer.paramLabelList[5]: #"pH":
                val = -9999
                try: val = float(pvalue)
                except: return self.soilPh
                if val >= 0 and val <= 14:
                    self.soilPh = val
                else: return self.soilPh
            elif pname == SoilLayer.paramLabelList[6]: #"C-org (M%)":
                val = -9999
                try: val = float(pvalue)
                except: return self.organicCarbonContent
                if val >= 0 and val <= 100:
                    self.organicCarbonContent = val
                else: return self.organicCarbonContent
            elif pname  == SoilLayer.paramLabelList[7]: #"Gravel (Vol.%)":
                val = -9999
                try: val = float(pvalue)
                except: return self.gravelContent
                if val >= 0 and val <= 100:
                    self.gravelContent = val
                else: return self.gravelContent
            elif pname == SoilLayer.paramLabelList[8]: #"Sand (M.%)":
                val = -9999
                try: val = float(pvalue)
                except: return self.sandContent
                if self.soilTexture == "O":
                    self.sandContent = 0
                    return self.sandContent
                else:
                    if val >= 0 and val <= 100:
                        self.sandContent = val
                    else: return self.sandContent
            elif pname == SoilLayer.paramLabelList[9]: #"Silt (M.%)":
                val = -9999
                try: val = float(pvalue)
                except: return self.siltContent
                if self.soilTexture == "O":
                    self.siltContent = 0
                    return self.siltContent
                else:
                    if val >= 0 and val <= 100:
                        self.siltContent = val
                    else: return self.siltContent
            elif pname == SoilLayer.paramLabelList[10]: #"Clay (M.%)":
                val = -9999
                try: val = float(pvalue)
                except: return self.clayContent
                if self.soilTexture == "O":
                    self.clayContent = 0
                    return self.clayContent
                else:
                    if val >= 0 and val <= 100:
                        self.clayContent = val
                    else: return self.clayContent
            elif pname == SoilLayer.paramLabelList[11]: #"BD (g/cm3)":
                val = -9999
                try: val = float(pvalue)
                except: return self.bulkDensity
                if val > 0 and val <= 2.65:
                    self.bulkDensity = val
                else: return self.bulkDensity
            elif pname == SoilLayer.paramLabelList[12]: #"PV (Vol.%)":
                val = -9999
                try: val = float(pvalue)
                except: return self.poreVolume
                if val >= 0 and val <= 100:
                    self.poreVolume = val
                else: return self.poreVolume
            elif pname == SoilLayer.paramLabelList[13]: #"FC Vol.%":
                val = -9999
                try: val = float(pvalue)
                except: return self.waterCapacity
                if val >= 0 and val <= 100:
                    self.waterCapacity = val
                else: return self.waterCapacity
            elif pname == SoilLayer.paramLabelList[14]: #"PWP Vol.%":
                val = -9999
                try: val = float(pvalue)
                except: return self.permanentWiltingPoint
                if val >= 0 and val <= 100:
                    self.permanentWiltingPoint = val
                else: return self.permanentWiltingPoint
            elif pname == SoilLayer.paramLabelList[15]: #"KS (cm/d)":
                val = -9999
                try: val = float(pvalue)
                except: return self.saturatedHydraulicConductivity
                if val > 0:
                    self.saturatedHydraulicConductivity = val
                else: return self.saturatedHydraulicConductivity
            return None

    def getParameterValue(self, pname):
        if len(SoilLayer.paramLabelList) == 16:
            if pname == SoilLayer.paramLabelList[0]: #"Horizon Name":
                return self.horizonName
            elif pname == SoilLayer.paramLabelList[1]: #"Lower Horizon Border":
                return self.depthOfHorizon
            elif pname == SoilLayer.paramLabelList[2]: #"Layer Thickness":
                return self.layerThickness
            elif pname == SoilLayer.paramLabelList[3]: #"Correction Factor":
                return self.correctionFactor
            elif pname == SoilLayer.paramLabelList[4]: #"Texture":
                return self.soilTexture
            elif pname == SoilLayer.paramLabelList[5]: #"pH":
                return self.soilPh
            elif pname == SoilLayer.paramLabelList[6]: #"C-org (M%)":
                return self.organicCarbonContent
            elif pname  == SoilLayer.paramLabelList[7]: #"Gravel (Vol.%)":
                return self.gravelContent
            elif pname == SoilLayer.paramLabelList[8]: #"Sand (M.%)":
                return self.sandContent
            elif pname == SoilLayer.paramLabelList[9]: #"Silt (M.%)":
                return self.siltContent
            elif pname == SoilLayer.paramLabelList[10]: #"Clay (M.%)":
                return self.clayContent
            elif pname == SoilLayer.paramLabelList[11]: #"BD (g/cm3)":
                return self.bulkDensity
            elif pname == SoilLayer.paramLabelList[12]: #"PV (Vol.%)":
                return self.poreVolume
            elif pname == SoilLayer.paramLabelList[13]: #"FC Vol.%":
                return self.waterCapacity
            elif pname == SoilLayer.paramLabelList[14]: #"PWP Vol.%":
                return self.permanentWiltingPoint
            elif pname == SoilLayer.paramLabelList[15]: #"KS (cm/d)":
                return self.saturatedHydraulicConductivity
            return None

    @staticmethod
    def getParamLabelList():
        paramList = []

        list_temp = SoilLayer.paramLabelList.items()
        for key, value in SoilLayer.paramLabelList.items():
            paramList.append(value)
        return paramList


