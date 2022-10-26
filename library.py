def magenta(str):
    return "\033[35m" + str + "\033[0m"

def red(str):
    return "\033[31m" + str + "\033[0m"

def green(str):
    return "\033[32m" + str + "\033[0m"

def orange(str):
    return "\033[38;5;208m" + str + "\033[0m"

path_regex = r"(\/.*\.[\w:]+)"
