class Modules:
    modules = []  # list of module strings
    mods = []  # list of module objects

    def __init__(self, filename):
        self.modules = load_modules(filename)  # Load the specified config file
        if type(self.modules) is str:  # If the returned modules is a string (and not a list)
            print(self.modules)  # Print the error message
            raise SystemExit  # Quit the program
        else:  # Else, the modules loaded successfully
            for module in self.modules:  # For every module in the list,
                m = Module(module)  # Create a new class for that module
                self.mods.append(m)  # Append the module to a list

    def build_active_list(self, criteria):
        """
        Builds active list of mods based on search criteria
        :param criteria: list of criteria to build the active list from
        :return: list of mods that match the criteria
        """
        active_list = []
        if len(criteria) > 0:
            for mod in self.mods:
                crit_matching = 0
                if len(criteria) <= len(mod.options):
                    for i in range(len(criteria)):
                        if criteria[i] == clean_line(mod.options[i], "Option", i+1):
                            crit_matching += 1
                    if crit_matching == len(criteria):
                        active_list.append(mod)
            if len(active_list) > 0:
                return active_list
            else:
                print(f"No modules found matching criteria: {criteria}")
                raise SystemExit
        else:
            return self.mods


class Module:
    options = []
    parameters = []
    execute = []

    def __init__(self, module):
        self.options = parse_module(module, "Option")
        self.parameters = parse_module(module, "Parameter")
        self.execute = parse_module(module, "Execute")


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
        if keyword in keyw and "#" not in keyw:
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
