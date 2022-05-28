@Rem Performs the sanitisation of the profile before commit.
@Rem Remember to: 
@Rem   use Helios Profile Utility to make sure there are no duplicate bindings
@Rem   use Helios Profile Utility to remove all unnecessary interfaces.
@rem
@rem This takes no arguments
@rem
@IF NOT EXIST "Apache Pilot.hpf" @ECHO * * * New profile Apache Pilot.hpf not found in current directory &&EXIT /b 1
@echo * * * This program works on file Apache Pilot.hpf in the current directory
rmdir .\temp /s
@mkdir .\temp
@mkdir .\temp\PreCommit
@move ".\Apache Pilot.hpf" ".\temp\Precommit\Apache Pilot.hpf.candidate"
@powershell -command "Copy-Item -Path \".\AH-64D_BLK_II\Helios\Profiles\Apache Pilot.hpf\" -Destination (\".\temp\precommit\Apache Pilot \" + (get-Date -format \"yyyyMMddHHmm\") + \".hpf.bak\")"
@echo A backup of original profile saved as ".\temp\Precommit\Apache Pilot yyyyMMddHHmm.hpf.bak"
@type ".\temp\Precommit\Apache Pilot.hpf.candidate" | powershell -command "$input | ForEach-Object{$_ -replace '(<StaticValue>)[\d*]\.[\d*]\.[\d*](<\/StaticValue>)','$1profileversionnumber$2'}" > AH-64D_BLK_II\Helios\Profiles\Apache Pilot.hpf
@Echo * * * .\AH-64D_BLK_II\Helios\Profiles\Apache Pilot.hpf has been created - Check and confirm that all is OK
@goto :eof
:usage
@echo Usage: %0 
@exit /b 1
