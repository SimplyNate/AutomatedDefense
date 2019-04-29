import time
import subprocess


def debug(message):
    outfile = open("debug.txt")
    outfile.write(message + "\n")
    outfile.close()


def coolprint(message):
    lines = message.split("\n")
    for line in lines:
        print(line)
        time.sleep(0.01)


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


def execute(command, parameters):
    command = command.replace("Execute", "").strip()
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
