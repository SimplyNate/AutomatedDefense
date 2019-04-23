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

from . import Module
from . import Functions
import re


def homepage():
    """
    Loads the homepage of the application based on the Startup.cfg contents
    :return: list of config files to parse
    """
    homepg = open("modules/Startup.cfg").readlines()
    splash_screen = """"""
    options = []
    sc_section = False
    op_section = False
    for line in homepg:
        if sc_section:
            if "[Options]" in line:
                sc_section = False
            else:
                splash_screen += line
        if op_section:
            if "[Splash Screen]" in line or line == "\n":
                op_section = False
            else:
                options.append(line.strip())
        if "[Splash Screen]" in line:
            sc_section = True
        if "[Options]" in line:
            op_section = True

    Functions.coolprint(splash_screen)
    show_selection(options)
    return options


def show_selection(ops):
    for i in range(len(ops)):
        print(f"{i+1}. {ops[i]}")


def make_selection(ops):
    while True:  # Input validation
        selection = input("Select a number from above or q to quit: ").strip()
        if selection is "q" or selection is "quit" or selection is "exit":
            raise SystemExit
        else:
            match = re.compile("[0-9]+")
            if re.match(match, selection):
                selection = int(selection)
                if selection > len(ops) or selection < len(ops):
                    print(f"Please select an option within the range: [1-{len(ops)}]")
                else:  # Else, exit the loop
                    return selection


def replay(history):
    pass


# Determines what to do
def mainloop(part, iteration, selection=None, modules=None):
    pass


# Entry Point into Program
if __name__ == '__main__':
    history = []  # Keeps track of all user input for replay
    done = False
    iteration = 0
    section = "homepage"
    ops, modules, selection = None, None, None
    while not done:
        if section is "homepage":
            ops = homepage()  # Get list of homepage options
            section = "module"  # Change the section for next run
            selected = make_selection(ops)  # Get user input
            selection = ops[selected - 1]  # Get corresponding option from selection
            history.append([iteration, selection])  # Append the user interactions with the iteration
            iteration += 1  # Add 1 to the iteration number
        elif section is "module":
            if modules is None:  # If no modules are defined (selection)
                modules = Module.Modules(selection)  # Create a new modules object
                selection = None  # Reset the selection variable
            active_list = modules.build_active_list(iteration, selection)  # Build the active list
            show_selection(active_list)
            selected = make_selection(active_list)
            selection = active_list[selected - 1]
            history.append([iteration, selection])
            iteration += 1
            # Check if the active_list only has 1 object left
            if len(modules.active_list) == 1:
                if iteration > len((modules.active_list[0]).options):
                    section = "parameter"
        elif section is "parameter":
            param = modules.build_active_list(iteration)
            answer = input(f"{param}: ")
            # Bind the selection to the module
            modules.add_mod_param(answer)
            history.append([iteration, answer])
            iteration += 1
            if iteration > (len((modules.active_list[0]).parameters) + len((modules.active_list[0]).options)):
                section = "execute"
        elif section is "execute":
            exe = modules.build_active_list(iteration)
            params = modules.active_list[0].set_parameters
            Functions.execute(exe, params)
        else:
            print("Error: part is invalid")
            raise SystemExit
