@Rem Creates the Helios Installable profile.
@Rem Remember to: 
@Rem   change the daterelease information in the Profile16.json file first (date prereq etc)
@rem
@rem This takes two arguments which are the file/profile suffix in form x.y.z and the minimum helios 
@rem in the form w.x.y.z
@rem
@if [%1]==[] goto usage
@if [%2]==[] goto usage
echo %2
rmdir .\temp /s
del "AH-64D_BLK_II*.helios16"
mkdir .\temp
xcopy AH-64D_BLK_II ".\temp\AH-64D_BLK_II V%1\" /e /v /y
type ".\temp\AH-64D_BLK_II V%1\helios\profiles\Apache Pilot.hpf" | powershell -Command "$input | ForEach-Object { $_ -replace \"profileversionnumber\", \"%1\" }" > ".\temp\AH-64D_BLK_II V%1\helios\profiles\Apache Pilot V%1.hpf"
del ".\temp\AH-64D_BLK_II V%1\helios\profiles\Apache Pilot.hpf"
copy "AH-64D - About this profile.md" ".\temp\AH-64D V%1 - About this profile.md"
copy "LICENSE" ".\temp\LICENSE."
copy "README.md" ".\temp\README.md"
type "Profile16.json" | powershell -Command "$input | ForEach-Object { $_.replace(\"profileversionnumber\", \"%1\").replace(\"_ReleaseDate\", (Get-Date -format \"dd MMMM yyyy\")).replace(\"_MinimumReleaseLevel\",\"%2\")}" > ".\temp\Profile16.json"
cd ".\temp"
"%programfiles%\winrar\winrar.exe" a -afzip -r "..\AH-64D_BLK_II V%1.zip" *.*
cd ..
ren ".\AH-64D_BLK_II V%1.zip" "AH-64D_BLK_II V%1.helios16"
@goto :eof
:usage
@echo Usage: %0 ^[profile suffix e.g. 5.0.0^] ^[minimum release number e.g. 1.6.5300.0^]
@exit /b 1
