def trim(string):
    return "".join([string[:75], "..."]) if len(string) > 75 else string
