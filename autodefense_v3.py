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

    coolprint(splash_screen)
    return options


def show_selection(ops):
    for i in range(len(ops)):
        print(f"{i+1}. {ops[i]}")
    print()


def make_selection(ops):
    while True:  # Input validation
        selection = input("Select a number from above, b to go back, or q to quit: ").strip()
        if selection is "q" or selection is "quit" or selection is "exit":
            raise SystemExit
        elif selection is "b" or selection is "back":
            return selection
        else:
            match = re.compile("[0-9]+")
            if re.match(match, selection):
                selection = int(selection)
                if selection > len(ops) or selection < 1:
                    print(f"Please select an option within the range: [1-{len(ops)}]")
                    print()
                else:  # Else, exit the loop
                    return selection


# Determines what to do
def mainloop(config, crit, mods):
    if config is "":
        ops = homepage()
        show_selection(ops)
        selected = make_selection(ops)
        if selected is "b" or selected is "back":
            pass  # Restart the process without doing anything
        else:
            config = ops[selected - 1]
    # Else if no mods object has been created
    elif mods is None:
        mods = Modules(config)  # Create the object and restart the process
    else:
        # Build an active list of mod objects that fit the criteria
        active_list = mods.build_active_list(crit)
        # If there's more than one mod or there's more options to go through for a mod:
        if len(active_list) > 1 or len(active_list[0].options) > len(crit):
            ops = []  # Initialize list to store options
            for mod in active_list:
                op = clean_line(mod.get_op_num(len(crit)+1), "Option", len(crit)+1)
                if op not in ops:
                    ops.append(op)
            show_selection(ops)
            selected = make_selection(ops)
            # If the user wants to go back
            if selected is "b" or selected is "back":
                # Delete the last choice made
                if len(crit) > 0:
                    del crit[-1]
                else:
                    config = ""
            else:
                crit.append(ops[selected - 1])
        else:  # Else, we are looking to provide the user with parameters or Execute
            mod = active_list[0]  # There should be only one module in the active list, so bind it to a variable
            params = mod.get_params()
            set_params = []
            for i in range(len(params)):
                param = clean_line(params[i], "Parameter", i+1)
                param_answer = input(f"{param}: ")
                if param_answer is "b" or param_answer is "back":
                    if i > 0:
                        i -= 1
                        del set_params[-1]
                    else:
                        del crit[-1]
                else:
                    set_params.append(param_answer)
            # Check if all parameters are set
            if len(set_params) == len(params):
                # All parameters are set: Execute
                exe = mod.get_exec()
                for ex in exe:
                    execute(ex, set_params)
                    raise SystemExit

    return config, crit, mods


# Entry Point into Program
if __name__ == '__main__':
    file = ""
    criteria = []
    done = False
    modules = None
    while not done:
        file, criteria, modules = mainloop(file, criteria, modules)
