# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Script to make adjustments to a single Iris configuration file
# and then create an additional two configuration files which 
# are subsets of the origianl file.  This script is intented 
# to be run in a GitHub workflow so the output files are never
# committed.
# Arguments:
# 1. Filename for the original Iris config file (which will get overwritten)
# 2. Filename of the first sub config file 
# 3. Filename of the second sub config file 
# 4. Value to adjust all of the Capture X positions 
# 5 Value to adjust all of the Capture Y positions 
# 6. Value to adjust all of the ScreenPosition X values
# 7. Value to adjust all of the ScreenPosition Y values 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import sys
IrisConfigFileName = sys.argv[1]
IrisConfigSubFileName1 = sys.argv[2]
IrisConfigSubFileName2 = sys.argv[3]
CaptureAdjustmentValueX = sys.argv[4]
CaptureAdjustmentValueY = sys.argv[5]
PositionAdjustmentValueX = sys.argv[6]
PositionAdjustmentValueY = sys.argv[7]

from defusedxml.ElementTree import parse
# parse the original input file
et = parse(IrisConfigFileName)

root = et.getroot()
root.find('.').set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
root.find('.').set('xmlns:xsd', 'http://www.w3.org/2001/XMLSchema')

for el in root.iter('Host'):
    el.text = 'localhost'
	
if CaptureAdjustmentValueX != 0:
    for el in root.iter('ScreenCaptureX'):
        s = el.text
        if int(el.text) >= 1920:
          el.text = str(int(el.text) + CaptureAdjustmentValueX)
          print("Capture Position ", s, el.text)

if CaptureAdjustmentValueY != 0:
    for el in root.iter('ScreenCaptureY'):
        el.text = str(int(el.text) + CaptureAdjustmentValueY)

if PositionAdjustmentValueX != 0:
    for el in root.iter('ScreenPositionX'):
        el.text = str(int(el.text) + PositionAdjustmentValueX)

if PositionAdjustmentValueY != 0:
    for el in root.iter('ScreenPositionY'):
        el.text = str(int(el.text) + PositionAdjustmentValueY)

et.write(IrisConfigFileName,encoding="UTF-8",xml_declaration=True)

deletions = []
for el in root:
    if el.tag =="ViewPorts":
        for el1 in el:
            if "Pilot" in el1.find('Name').text:
                print("Flagging for Removal ", el1.tag, el1.find('Name').text)
                deletions.append(el1)
        for x in deletions:
            print("Removing ", x.find('Name').text)
            el.remove(x)
			
for el in root:
    if el.tag =="ViewPorts":
            for el1 in el:
                    print(el1.tag)

et.write(IrisConfigSubFileName2,encoding="UTF-8",xml_declaration=True)
# we must now reparse the original but changed file to make the other subset
et = parse(IrisConfigFileName)
root = et.getroot()
root.find('.').set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
root.find('.').set('xmlns:xsd', 'http://www.w3.org/2001/XMLSchema')
deletions = []
for el in root:
    if el.tag =="ViewPorts":
        for el1 in el:
            if "CP/G" in el1.find('Name').text or "TEDAC" in el1.find('Name').text:
                print("Flagging for Removal ", el1.tag, el1.find('Name').text)
                deletions.append(el1)
        for x in deletions:
            print("Removing ", x.find('Name').text)
            el.remove(x)

for el in root:
    if el.tag =="ViewPorts":
        for el1 in el:
            print(el1.tag)

et.write(IrisConfigSubFileName1,encoding="UTF-8",xml_declaration=True)