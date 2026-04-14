#!/bin/bash

pushd `dirname $0` > /dev/null

pyuic5 -x DialogGraphCompare.ui -o ../interface/DialogGraphCompare.py
pyuic5 -x DialogGraphData.ui -o ../interface/DialogGraphData.py
pyuic5 -x DialogGraphProperties.ui -o ../interface/DialogGraphProperties.py
pyuic5 -x DialogPlotProperties.ui -o ../interface/DialogPlotProperties.py
pyuic5 -x DialogShowLog.ui -o ../interface/DialogShowLog.py
pyuic5 -x DialogSoilFileName.ui -o ../interface/DialogSoilFileName.py
pyuic5 -x DialogVersionSettings.ui -o ../interface/DialogVersionSettings.py
pyuic5 -x FormDesignGraph.ui -o ../interface/FormDesignGraph.py
pyuic5 -x FormEpcFile.ui -o ../interface/FormEpcFile.py
pyuic5 -x FormGisFile.ui -o ../interface/FormGisFile.py
pyuic5 -x FormHopspackConfiguration.ui -o ../interface/FormHopspackConfiguration.py
pyuic5 -x FormHopspackRun.ui -o ../interface/FormHopspackRun.py
pyuic5 -x FormInitialAndOutputSetting.ui -o ../interface/FormInitialAndOutputSetting.py
pyuic5 -x FormInputPackage.ui -o ../interface/FormInputPackage.py
pyuic5 -x FormMain.ui -o ../interface/FormMain.py
pyuic5 -x FormModelRun.ui -o ../interface/FormModelRun.py
pyuic5 -x FormReadOutput.ui -o ../interface/FormReadOutput.py
pyuic5 -x FormShowGraph.ui -o ../interface/FormShowGraph.py
pyuic5 -x FormSoilProfile.ui -o ../interface/FormSoilProfile.py
pyuic5 -x FormSpssScript.ui -o ../interface/FormSpssScript.py
pyuic5 -x FormVegFile.ui -o ../interface/FormVegFile.py
#pyuic5 -x HopspackInterface.ui -o ../interface/HopspackInterface.py
