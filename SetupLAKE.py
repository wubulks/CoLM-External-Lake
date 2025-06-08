import os
import shutil
import argparse


argparser = argparse.ArgumentParser(description='Setup LAKE in CoLM')
argparser.add_argument('-CoLM', type=str, help='Path to the CoLM directory', required=True)
args = argparser.parse_args()

CoLMPath = args.CoLMPath




##########################################################
# Check if the CoLM path exists
if not os.path.exists(CoLMPath):
    print(f"CoLM path {CoLMPath} does not exist. Please ensure you have the correct path.")
    exit(1)
# Check if the LAKE directory exists
if not os.path.exists('./LAKE'):
    print("LAKE directory does not exist. Please ensure you have cloned the LAKE repository.")
    exit(1)
shutil.rmtree(f'{CoLMPath}/main/LAKE', ignore_errors=True)

# Copy the LAKE directory to CoLM's main directory
print("Copying LAKE directory to CoLM's main directory...")
shutil.copytree('./LAKE', f'{CoLMPath}/main/LAKE', dirs_exist_ok=True)

# Check if the Makefile exists in CoLM's main directory
if not os.path.exists(f'{CoLMPath}/Makefile'):
    print("Makefile does not exist in CoLM's main directory. Please ensure you are in the correct directory.")
    exit(1)
shutil.copyfile(f'{CoLMPath}/Makefile', f'{CoLMPath}/Makefile.bak')

# Modify the Makefile to include LAKE
print("Modifying Makefile to include LAKE...")
with open(f'{CoLMPath}/Makefile', 'r') as file:
    lines = file.readlines()
    newlines = []
    for i, line in enumerate(lines):
        if 'main/LAKE' in line:
            # Skip the line that contains 'main/LAKE'
            print("Found 'main/LAKE' in Makefile, pleasing check if it is correct.")
            break
        if 'main/LULCC : main/DA' in line:
            newline = line.replace('main/LULCC : main/DA', 'main/LULCC : main/DA : main/LAKE')
            newlines.append(newline)
        else:
            newlines.append(line)
            
        if 'MOD_SPMD_Task.o' in line:
            newline = line.replace('MOD_SPMD_Task.o', 'MOD_Lake_Const.o')
            newlines.append(newline)
        if 'MOD_Namelist.o' in line:
            newline = line.replace('MOD_Namelist.o', 'MOD_Lake_Namelist.o')
            newlines.append(newline)
        if 'MOD_Vars_TimeInvariants.o' in line:
            newline = line.replace('MOD_Vars_TimeInvariants.o', 'MOD_Lake_Utils.o')
            newlines.append(newline)
            newline = line.replace('MOD_Vars_TimeInvariants.o', 'MOD_Lake_TimeVars.o')
            newlines.append(newline)
        if 'MOD_Lake.o' in line:
            newline = line.replace('MOD_Lake.o', 'MOD_Lake_Subs.o')
            newlines.append(newline)
            newline = line.replace('MOD_Lake.o', 'MOD_Lake_CoLML.o')
            newlines.append(newline)
            newline = line.replace('MOD_Lake.o', 'MOD_Lake_FLake.o')
            newlines.append(newline)
            newline = line.replace('MOD_Lake.o', 'MOD_Lake_Simstrat.o')
            newlines.append(newline)
            newline = line.replace('MOD_Lake.o', 'MOD_Lake_Driver.o')
            newlines.append(newline)
        if 'MOD_Thermal.o' in line:
            newline = line.replace('MOD_Thermal.o', 'MOD_Lake_1DAccVars.o')
            newlines.append(newline)
        if 'MOD_HistSingle.o' in line:
            newline = line.replace('MOD_HistSingle.o', 'MOD_Lake_Hist.o')
            newlines.append(newline)
            
            
with open(f'{CoLMPath}/Makefile', 'w') as file:
    file.writelines(newlines)

print(" *** Successfully Setup LAKE in CoLM ***")

        
