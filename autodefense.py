"""
MIT License

Copyright (c) 2019 Nathan Horiuchi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from Module import *
from Functions import *
import re


def homepage():
    """
    Loads the homepage of the application based on the Startup.cfg contents
    :return: list of config files to parse
    """
    homepg = open("modules/Startup.cfg").readlines()  # Read the lines of the Startup config
    splash_screen = ""  # Initialize string to hold splash screen
    options = []  # Initialize variable to store options
    sc_section = False  # Keep track of section
    op_section = False  # Keep track of section
    for line in homepg:  # For each line in the Startup.cfg file:
        if "[Splash Screen]" in line:  # If the splash screen header is read
            sc_section = True  # Start section for splash screen
            op_section = False
            continue  # Skip remainder of for loop iteration
        elif "[Options]" in line:  # If the options header is read
            op_section = True  # Start section for options
            sc_section = False
            continue  # Skip remainder of for loop iteration
        if sc_section:  # If the splash screen is being read:
            if "[Options]" in line:  # If the Options header is reached:
                sc_section = False  # Discontinue section for splash screen
            else:  # Else:
                splash_screen += line  # Add the line to the splash screen string
        elif op_section:  # If the options section is being read:
            if "[Splash Screen]" in line or line == "\n":  # If splash screen is read or a newline is read:
                op_section = False  # Discontinue section for option
            else:  # Else:
                options.append(line.strip())  # Add the line to the options list
    coolprint(splash_screen)  # Print splash screen
    return options


def show_selection(ops):
    """
    Function to print all options to screen
    :param ops: List of options to print
    :return: null
    """
    for i in range(len(ops)):
        print(f"{i+1}. {ops[i]}")
    print()


def make_selection(ops):
    """
    Function to prompt for user selection during Option selection
    :param ops: List of options to select from
    :return: String of user's selection
    """
    while True:  # Input validation
        selection = input("Select a number from above, b to go back, or q to quit: ").strip()  # Get User Input
        if selection is "q" or selection is "quit" or selection is "exit":  # If the user wants to exit:
            raise SystemExit  # Exit application
        elif selection is "b" or selection is "back":  # If the user wants to go back:
            return selection  # Return the selection as-is
        else:  # Else, the user wants to continue
            match = re.compile("[0-9]+")  # Compile RE for any valid integer
            if re.match(match, selection):  # If the user input matches the RE
                selection = int(selection)  # Cast the input as an int
                if selection > len(ops) or selection < 1:  # If the int is not within the valid range:
                    print(f"Please select an option within the range: [1-{len(ops)}]")  # Print Error
                    print()  # Spacer
                else:  # Else, exit the loop and return the user's input
                    return selection


# Determines what to do
def mainloop(config, crit, mods):
    """
    Function to perform the main loop of the prograsm
    :param config: String Name of file to load
    :param crit: List of criteria to search modules for
    :param mods: Modules object (so it doesn't get reinitialized every round)
    :return: config, crit, mods that are set during runtime
    """
    if config is "":  # If the config is blank
        ops = homepage()  # Get the ops from the Startup.cfg
        show_selection(ops)  # Display the list of options to the user
        selected = make_selection(ops)  # Ask for user input and perform input validation
        if selected is "b" or selected is "back":  # If the user wants to go back:
            pass  # Restart the process without doing anything
        else:  # Else, the user wants to proceed
            config = ops[selected - 1]  # Grab the selected option
    elif mods is None:  # Else, if no mods object has been created:
        mods = Modules(config)  # Create the object and restart the process
    else:  # Else, a config file has been selected and modules have been created:
        active_list = mods.build_active_list(crit)  # Build an active list of mod objects that fit the criteria
        if len(active_list) > 1 or len(active_list[0].options) > len(crit):  # If there's more than one mod or there's more options to go through for a mod:
            ops = []  # Initialize list to store options
            for mod in active_list:  # For each mod object in the active_list:
                op = clean_line(mod.options[len(crit)], "Option", len(crit)+1)  # Get the option number corresponding to the amount of criteria given
                if op not in ops:  # If the option is not in the list of options
                    ops.append(op)  # Append the option
            show_selection(ops)  # Display the list of options to the user
            selected = make_selection(ops)  # Ask for user input and perform input validation
            if selected is "b" or selected is "back":  # If the user wants to go back
                if len(crit) > 0:  # If criteria had been given previously:
                    del crit[-1]  # Delete the last choice made
                else:  # Else, there's no choices to delete
                    config = ""  # Reset the config file to read from
            else:  # Else, the user wants to proceed:
                crit.append(ops[selected - 1])  # Append the user's selected option to the list of criteria
        else:  # Else, we are looking to provide the user with parameters or Execute
            mod = active_list[0]  # There should be only one module in the active list, so bind it to a variable
            params = mod.parameters  # Get the parameters from the module
            set_params = []  # Initialize list for storing user's parameters
            i = 0
            while i < len(params):  # For each parameter:
                param = clean_line(params[i], "Parameter", i+1)  # Clean the Param line
                param_answer = input(f"{param}: ")  # Ask the user for input
                if param_answer is "b" or param_answer is "back":  # If the user wants to go back:
                    if i > 0 and len(set_params) > 0:  # If 1 or more parameters have been set already:
                        i -= 1  # Go back one
                        del set_params[-1]  # Remove the last set parameter
                    else:  # Else, no params were set and user wants to see options again:
                        del crit[-1]  # Remove the last set criteria
                        break
                else:  # Else, the user wants to proceed:
                    if "subnet" in param.lower() or "ip" in param.lower():  # If the answer is supposed to contain an IP:
                        if is_ip(param_answer):  # If the input is a valid IP
                            set_params.append(param_answer)  # Append the input to the list of set_params
                            i += 1
                        else:  # Else, input validation failed:
                            print(f"Error: {param_answer} is not a valid IP Address or Subnet")  # Print Error
                    else:  # Else, perform no additional input validation:
                        set_params.append(param_answer)  # Append the input to the list of set_params
                        i += 1
            if len(set_params) == len(params):  # If all params are set:
                exe = mod.execute  # Get the Execute commands from the mod
                for ex in exe:  # For each execution command in the list:
                    execute(ex, set_params)  # Execute the command with the set parameters
                    raise SystemExit  # Exit the program
    return config, crit, mods


# Entry Point into Program
if __name__ == '__main__':
    # Initialize variables
    file = ""
    criteria = []
    modules = None
    # Mainloop
    while True:
        # Refresh variables and rerun mainloop
        file, criteria, modules = mainloop(file, criteria, modules)
