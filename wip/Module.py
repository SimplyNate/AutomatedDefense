class Modules:
    modules = []  # list of module strings
    mods = []  # list of module objects
    active_list = []  # list of modules currently matching the user's choice

    def __init__(self, filename):
        self.modules = load_modules(filename)  # Load the specified config file
        if type(self.modules) is str:  # If the returned modules is a string (and not a list)
            print(self.modules)  # Print the error message
            raise SystemExit  # Quit the program
        else:  # Else, the modules loaded successfully
            for module in self.modules:  # For every module in the list,
                m = Module(module)  # Create a new class for that module
                self.mods.append(m)  # Append the module to a list

    def build_initial_list(self):
        ops = []
        for mod in self.mods:
            self.active_list.append(mod)
            op1 = mod.get_op_num(1)
            if op1 not in ops:
                ops.append(op1.replace("Option1", "").strip())
        return ops

    def build_subsequent_list(self, answer, level):
        """
        Builds subsequent list of options for user to choose from
        :param answer: last answer given
        :param level: current iteration
        :return: list of options for user to choose from
        """
        for mod in self.active_list:

    def eliminate_mod(self, mod):
        self.active_list.remove(mod)



class Module:
    options = []
    parameters = []
    execute = []

    def __init__(self, module):
        self.options = parse_module(module, "Option")
        self.parameters = parse_module(module, "Parameter")
        self.execute = parse_module(module, "Execute")

    def get_op_num(self, number):
        for option in self.options:
            if int(option.split()[6]) == number:
                return option

    def get_param_num(self, number):
        for param in self.parameters:
            if int(param.split()[9]) == number:
                return param

    def get_exec(self):
        return self.execute



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

