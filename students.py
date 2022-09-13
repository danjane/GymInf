import re


def code_and_name(s_dirty):
    s = s_dirty.strip().split(', ')
    code = s[0]
    if len(s) == 1:
        name = re.search(r'^[a-z\-]+', code).group(0).capitalize()
    else:
        name = s[1]
    return name, code


class Students:

    def __init__(self, filename):
        with open(filename, 'r') as f:
            values = {}
            for s_dirty in f.readlines():
                values[s_dirty] = s_dirty

        self.values = values

    def __getitem__(self, key):
        return "Albert"
        # return self._values[key]

