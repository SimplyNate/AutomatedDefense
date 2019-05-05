# AutomatedDefense  
A Python framework script that gives a methodical approach in guiding the user to choose the action they are looking for.  

## Requirements  
Python 3.6 or greater  

## Usage  
`py autodefense.py`  

The script will look into the `Modules` directory for a `Startup.cfg` file. The script reads for the splash screen and a catalogue of the module configs available to the script, then present these options to the user. When the user chooses a valid option, the script will then look for a .cfg file of the same name in the `Modules` directory.  

## How to Create Modules  
Note: If you only want to add on to a config, skip to step 3.  

1.  Create a new config file in the format [configname].cfg  
2.  Add the config name to the Options list in the `Startup.cfg` file  
3.  Add Option# to the file, then the Option Description that is displayed to the user, separated by spaces  
4.  Add Parameter# to the file, then the Parameter Description that is displayed to the user, separated by spaces. This should indicate what the executing script will need from the user to proceed.
5.  Add Execute to the file, then the line to be executed. If parameters are used, place [Parameter#] in its place.  
6.  Separate modules in a file by newlines  
7.  Comments may be added only in their own separate lines  
