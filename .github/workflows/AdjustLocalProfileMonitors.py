# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Script to make adjustments to the Helios profile by adding in
# additional monitors by XML manipulation.  This should be more
# reliable than using diff-match-patch.
# There are still changes to be made after this script, but it is more
# efficient for these to be text substitutions.  These changes are not 
# committed.
# Arguments:
# 1. Filename for the original Helios Profile file
# 2. Filename for the monitor XML to be inserted into the profile 
# 3. Filename for the Bindings XML to be inserted into the profile 
# 4. Filename of the resultant Helios profile
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import sys
InputHeliosProfile = sys.argv[1]
hpfMonitorFileName1 = sys.argv[2]
hpfBindingFileName1 = sys.argv[3]
OutputHeliosProfile = sys.argv[4]

print("Donor Helios Profile", InputHeliosProfile)
print("Monitor XML ", hpfMonitorFileName1)
print("Binding XML ", hpfBindingFileName1)
print("New Helios Profile ", OutputHeliosProfile)

from defusedxml.ElementTree import parse
# parse the original input file
print("Reading existing profile: ",InputHeliosProfile)
et = parse(InputHeliosProfile)
root = et.getroot()
print("Reading additional monitor XML: ",hpfMonitorFileName1)
monitorsRoot = parse(hpfMonitorFileName1).getroot()
print("Reading additional binding XML: ",hpfBindingFileName1)
bindingsRoot = parse(hpfBindingFileName1).getroot()

# Remove embedded viewports from the profile
for el in root.iter("EmbeddedViewportName"):
    print("Removing ",el.tag ,el.text)
    el.text = ""
	
# Alter the location of the monitor so that it is positioned at the far right
for el in root.iter("Monitor"):
    el.find("Location").text = "3840,0"

# Insert the two additional monitors at the start of the monitor list 
for el in root:
    if el.tag == "Monitors":
        i = 0
        for mel in monitorsRoot:
            el.insert(i,mel)
            i += 1
            print("Adding Monitor",i," at ", mel.find("Location").text)
        continue

# Insert the two additional bindings at the start of the binding list 
for el in root:
    if el.tag == "Bindings":
        i = 0
        for mel in bindingsRoot:
            el.insert(i,mel)
            i += 1
            print("Adding Binding for ", mel.find("StaticValue").text)
        continue

print("Writing new profile: ",OutputHeliosProfile)
et.write(OutputHeliosProfile,encoding="UTF-8",xml_declaration=True)

