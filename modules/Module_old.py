class Modules:
    modules = []  # list of module strings
    mods = []  # list of module objects
    active_list = []  # list of modules currently matching the user's choice
    params = []
    discarded = []

    def __init__(self, filename):
        self.modules = load_modules(filename)  # Load the specified config file
        if type(self.modules) is str:  # If the returned modules is a string (and not a list)
            print(self.modules)  # Print the error message
            raise SystemExit  # Quit the program
        else:  # Else, the modules loaded successfully
            for module in self.modules:  # For every module in the list,
                m = Module(module)  # Create a new class for that module
                self.mods.append(m)  # Append the module to a list

    def build_active_list(self, level, answer=None):
        """
        Builds subsequent list of options for user to choose from
        :param answer: last answer given
        :param level: current iteration
        :return: list of options for user to choose from
        """
        if answer is None:  # If no answer is provided, this is the first run
            ops = []
            for mod in self.mods:
                self.active_list.append(mod)
                op1 = mod.get_op_num(level)
                if op1.replace(f"Option{level}", "").strip() not in ops:
                    ops.append(op1.replace(f"Option{level}", "").strip())
            return ops
        else:
            ops = []
            if len(self.active_list) > 1:  # If we are still narrowing down modules\
                # temp_active = copy.deepcopy(self.active_list)
                temp_active = []
                temp_discarded = []
                # Elimination round
                for mod in self.active_list:
                    # Go through elimination round first, then parse through the remainder!!!
                    # Else, return the list of options at the current level
                    prev_option = clean_line(mod.get_op_num(level-1), "Option", level-1)
                    if prev_option != answer:
                        # self.eliminate_mod(self.active_list[i])
                        temp_discarded.append(mod)
                    else:
                        temp_active.append(mod)
                self.active_list = temp_active
                if len(temp_discarded) > 0:
                    self.discarded.append(temp_discarded)
                if len(self.active_list) > 1:
                    for mod in self.active_list:
                        op = clean_line(mod.get_op_num(level), "Option", level)
                        if op not in ops:
                            ops.append(op)
                    return ops
            # Else, we have narrowed down to one module to use
            mod = self.active_list[0]  # Get the remaining module
            if level > len(mod.options):  # If the level is greater than the number of options
                if level > len(mod.options) + len(mod.parameters):  # If level > number of options + params
                    # Run the execute command(s)
                    execs = mod.get_exec()
                    return execs
                else:  # Return a single parameter
                    param_num = level - len(mod.options)
                    param = clean_line(mod.get_param_num(param_num), "Parameter", param_num)
                    return param
            else:
                ops.append(clean_line(mod.get_op_num(level), "Option", level))
                return ops

    def eliminate_mod(self, mod):
        self.active_list.remove(mod)

    def go_back(self):
        if len(self.discarded) > 0:
            # Add the last item in the delete list to the active list
            for item in self.discarded[-1]:
                self.active_list.append(item)
            # Remove the last item in the delete list
            del self.discarded[-1]
        else:
            pass

    def add_mod_param(self, param):
        self.active_list[0].set_param(param)


class Module:
    options = []
    parameters = []
    execute = []
    set_parameters = []

    def __init__(self, module):
        self.options = parse_module(module, "Option")
        self.parameters = parse_module(module, "Parameter")
        self.execute = parse_module(module, "Execute")

    def get_op_num(self, number):
        for option in self.options:
            if int(list(option)[6]) == number:
                return option

    def get_param_num(self, number):
        for param in self.parameters:
            if int(list(param)[9]) == number:
                return param

    def get_params(self):
        return self.parameters

    def get_exec(self):
        return self.execute

    def set_param(self, param):
        self.set_parameters.append(param)


def parse_module(module, keyword):
    """
    Returns a list of keywords for a single module
    :param module: list of strings
    :param keyword: Module keyword you are looking for
    :return: list of lines with the specified keyword
    """
    keys = []
    for line in module:
        keyw = line.split(" ")[0]
        if keyword in keyw:
            keys.append(line)
    if len(keys) > 0:
        return keys
    else:
        print(f"Error parsing module: No keyword {keyword} found.")


def load_modules(filename):
    """
    Returns a list of modules found in a configuration file
    :param filename: name of file to be loaded (without extension)
    :return: list of lists of modules found in the file
    """
    try:
        lines = open(f"modules/{filename}.cfg").readlines()
    except FileNotFoundError:
        return f"Error occurred while parsing {filename}: File Not Found"
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
        return f"Error occurred while parsing {filename}: No configurations found in file."


def clean_line(line, category, num):
    return line.replace(f"{category}{num}", "").strip()
