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

import time
import subprocess

startup = """
Automated Defense by Nathan Horiuchi

                     ,,ggddY""|'""Ybbgg,,
                 ,agd""'      |       `""bg,
              ,gdP"           |           "Ybg,
            ,dP"              |              "Yb,
          ,dP"    RC   _,,ddP"|"Ybb,,_   ID    "Yb,
         ,8"         ,dP"'         `"Yb,         "8,
        ,8'        ,d"                 "b,        `8,
       ,8'.       d"                     "b       .`8,
       d'  '~.   d'                       `b   .~'  `b
       8      '~.8      CyberSecurity      8.~'      8
       8         8        Framework        8         8
       8         8       Version 1.1       8         8
       8         Y,                       ,P         8
       Y,   RS    Ya                     aP    PR   ,P
       `8,         "Ya                 aP"         ,8'
        `8,         /"Yb,_         _,dP"\         ,8'
         `8a       /   `""YbbgggddP""'   \       a8'
          `Yba    /                       \    adP'
            "Yba /                         \ adY" 
              `"Yba,         DE          ,adP"' 
                 `"Y8ba,             ,ad8P"' 
                      ``""YYbaaadPP""'' 


NIST CyberSecurity Framework Version 1.1

1. Identify
2. Protect
3. Detect
4. Respond
5. Recover
"""


def debug(message):
    outfile = open("debug.txt")
    outfile.write(message + "\n")
    outfile.close()


def coolprint(message):
    lines = message.split("\n")
    for line in lines:
        print(line)
        time.sleep(0.01)


def loadmodule(module):
    try:
        lines = open("modules/" + module + ".cfg").readlines()
        modules = []
        mod = []
        for line in lines:
            if line is not "\n":
                mod.append(line)
            elif line is "\n" and len(mod) != 0:
                modules.append(mod)
                mod = []
        if len(modules) != 0:
            return modules
        else:
            return "Error occurred while parsing " + module + " configuration file: No modules loaded."
    except FileNotFoundError:
        print("No module " + module + ".cfg found.")
        quit()


def getmodules(modules, criteria):
    """
    :param modules: List of all loaded modules (from loadmodule)
    :param criteria: List of answers given by users
    :return: List of modules that match the given criteria (answers)
    """
    # If all the criteria is met, add the module to the list
    mods = []
    cnt = 0
    for module in modules:
        matches = []
        for i in range(len(criteria)):
            if criteria[i] in module[i]:
                matches.append(True)
        if len(matches) == len(criteria):
            mods.append(module)
    """
    for module in modules:
        matches = []
        for crit in criteria:
            # if find(crit, module):
            if crit in module[cnt]:
                matches.append(True)
        if len(matches) == len(criteria):
            mods.append(module)
    """
    return mods


def showoptions(array):
    print()
    for item in array:
        print(item)
    print()
    return input("Select a number from above or b to go back: ").strip()


def getparaminput(param):
    inp = input(param + ": ").strip()
    if "ip" in param.lower() or "subnet" in param.lower():
        if is_ip(inp):
            return inp
        else:
            print("IP validation failed. Try again.")
            getparaminput(param)
    else:
        return inp


def getparams(module):
    params = []
    params_given = []
    for line in module:
        # Get all the params and store them in an array
        # Grab The Category
        row = line.split(" ")[0]
        if "Parameter" in row:
            params.append(line.replace("Parameter" + str(len(params)+1), "").strip())
    for param in params:
        print()
        inp = getparaminput(param)
        params_given.append(inp)
    return params_given


def getexecutecommand(module):
    for line in module:
        if "Execute" in line:
            return line.replace("Execute", "").strip()


def execute(command, parameters):
    for i in range(len(parameters)):
        command = command.replace("[Parameter" + str(i+1) + "]", parameters[i])
        if "[Parameter" + str(i+1) + "_file]" in command:
            command = command.replace("[Parameter" + str(i+1) + "_file]", parameters[i].replace("/", "_"))
    print()
    print("Executing: " + command)
    try:
        subprocess.run(command)
    except FileNotFoundError:
        print("Error: Command not found. Exiting.")


# This function finds a piece of a string in a list
def find(needle, haystack):
    for hay in haystack:
        if needle in hay:
            return True
    else:
        return False


# This function removes everything in [original] except [keep]
def reverse_replace(original, keep):
    return original.replace(original.replace(keep, ""), "")


def find_exact(needle, haystack):
    for hay in haystack:
        hay = reverse_replace(hay, needle)
        if needle == hay:
            return True
    else:
        return False


def is_ipv4(hosts):
    """
    Function to validate IPv4 Addresses
    :param hosts: Takes a single host or subnet (ex. 127.0.0.1/24)
    :return: Boolean True or False
    """
    hosts = hosts.strip()
    if "/" not in hosts:
        # Assume that if no mask is specified, use a single host mask
        hosts = hosts + "/32"
    # Check if there are 4 octets and a cidr mask
    if hosts.count(".") == 3:
        # Check if the octets are no more than 255
        mask = int(hosts.split("/")[-1])
        octets = hosts.split("/")[0].split(".")
        for octet in octets:
            octet = int(octet)
            if octet <= 255:
                if mask <= 32:
                    # OK!
                    pass
                else:
                    return False
            else:
                return False
        return True
    else:
        return False


def is_ipv6(hosts):
    """
    Function to validate IPv6 Addresses
    :param hosts: Takes a single host or subnet
    :return: Boolean True or False
    """
    hosts = hosts.strip()
    if "/" not in hosts:
        # Assume that if no mask is specified, use a single host mask
        hosts = hosts + "/128"
    if ":" in hosts:
        mask = int(hosts.split("/")[-1])
        groups = hosts.split("/")[0].split(":")
        for group in groups:
            if len(group) is not 0 and len(group) <= 4:
                try:
                    group = int(group, 16)
                except Exception as e:
                    return False
            else:
                return False
        return True
    else:
        return False


def is_ip(hosts):
    if is_ipv4(hosts) or is_ipv6(hosts):
        return True
    return False


def getoptions(modules, part, answer=None):
    options = []
    for mod in modules:
        op = str(len(options)+1) + ". " + mod[part].replace("Option"+str(part+1), "").strip()
        if not find(mod[part].replace("Option"+str(part+1), "").strip(), options):
            options.append(op)
    return options


def level0(module, part, answer=None, modules=None, answers=None):
    """
    :param module: String of the name of the config file to load
    :param part: Integer keeping track of which line of a module we are looking at
    :param answer: String of the last given answer
    :param modules: List of the loaded modules from the module config
    :param answers: List of all previous answers given in a runtime
    """
    if modules is None:
        modules = loadmodule(module)
    if type(modules) is str:   # If modules is a string, it failed to load and produced an error message
        print(modules)   # Print the error message
        quit()   # Quit the program
    else:   # Modules loaded successfully
        options = []   # Holds a list of options for the user to choose from
        if answer is None:   # No answer is given, thus we need to load the first level options
            for mod in modules:
                op = str(len(options)+1) + ". " + mod[part].replace("Option"+str(part+1), "").strip()
                if not find(mod[part].replace("Option"+str(part+1), "").strip(), options):
                    options.append(op)
            inp = showoptions(options)
            if inp.strip() is "b":
                homepage()
            else:
                matches = False
                for item in options:
                    if inp in item.split(" ")[0]:
                        level0(module, part+1, item.replace(inp + ".", "").strip(), modules, [item.replace(inp + ".", "").strip()])
                        matches = True
                        # break
                if not matches:
                    level0(module, part, answer, modules, answers)
        else:  # An answer is given
            counter = 1
            # Get all the modules that fit the current description
            mods = getmodules(modules, answers)
            for mod in mods:
                op = mod[part]
                # Since there are multiple options for a given level, we have to deal with that outside the loop
                if "Option" in op:
                    op = str(counter) + ". " + mod[part].replace("Option" + str(part + 1), "").strip()
                    if not find(mod[part].replace("Option" + str(part + 1), "").strip(), options):
                        options.append(op)
                        counter += 1
                # There should only be one valid parameter or execute for each module at each level
                elif "Parameter" in op:
                    # Get the parameters from the module
                    # Get the execute statement
                    # Execute the command with the parameters
                    execute(getexecutecommand(mod), getparams(mod))
                    break
            """
            for mod in modules:
                # print("Module part: " + mod[part-1])
                # If the answer to the previous iteration is found in the module at the given part
                # if find(answer, mod):
                reverse_replace = mod[part-1].replace(answer, "").strip()
                # print(answer + " = " + mod[part - 1].replace(reverse_replace, "").strip())
                if answer == mod[part-1].replace(reverse_replace, "").strip():
                    # print(" = " + mod[part-1].replace(reverse_replace, "").strip())
                    # Grab the current part
                    op = mod[part]
                    # Since there are multiple options for a given level, we have to deal with that outside the loop
                    if "Option" in op:
                        op = str(counter) + ". " + mod[part].replace("Option"+str(part+1), "").strip()
                        if not find(mod[part].replace("Option"+str(part+1), "").strip(), options):
                            options.append(op)
                            counter += 1
                    # There should only be one valid parameter or execute for each module at each level
                    elif "Parameter" in op:
                        # Get the parameters from the module
                        # Get the execute statement
                        # Execute the command with the parameters
                        execute(getexecutecommand(mod), getparams(mod))
                        break 
            """
            # Now that we're outside the for loop, we can handle the options
            if len(options) > 0:
                inp = showoptions(options)
                if inp.strip() is "b":
                    # Remove the last answer
                    if len(answers) > 1:
                        answers.remove(answers[-1])
                        level0(module, part-1, answers[-1], modules, answers)
                    else:
                        level0(module, part-1, None, modules, None)
                matches = False
                for item in options:
                    if inp in item.split(" ")[0]:
                        # print("answer=" + item.replace(inp + ".", "").strip())
                        answers.append(item.replace(inp + ".", "").strip())
                        level0(module, part+1, item.replace(inp + ".", "").strip(), modules, answers)
                        matches = True
                        break
                if not matches:
                    level0(module, part, answer, modules, answers)


def homepage():
    coolprint(startup)
    selection = input("Select a number from above or q to quit: ").strip()
    if selection is "1":
        level0("identify", 0)
    elif selection is "2":
        level0("protect", 0)
    elif selection is "3":
        level0("detect", 0)
    elif selection is "4":
        level0("respond", 0)
    elif selection is "5":
        level0("recover", 0)
    elif selection is "q" or selection == "quit" or selection == "exit":
        print("Exiting")
        quit()
    else:
        print("Bad input. Please enter a number 1-5 or q")
        homepage()


if __name__ == '__main__':
    homepage()
