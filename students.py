import re
import config


def code_and_name(s_dirty):
    s = s_dirty.strip().split(', ')
    code = s[0]
    if len(s) == 1:
        name = re.search(r"^[a-z\-]+", code).group(0).capitalize()
    else:
        name = s[1]
    return code, name


def duplicate_warning(duplicates):
    print(f"The following names are duplicated!! {duplicates}")


def name_conflict(name_dict):
    names = list(name_dict.values())
    duplicates = set([name for name in names if names.count(name) > 1])
    if duplicates:
        duplicate_warning(duplicates)
    return duplicates


class Students:

    def __init__(self, filename):
        with open(filename, 'r') as f:
            values = {}
            for s_dirty in f.readlines():
                c, n = code_and_name(s_dirty)
                values[c] = n
        self.values = values

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, values):
        self._values = values

    def __getitem__(self, key):
        return self._values[key]


def loadClassLists(config_path):
    c = config.load(config_path)
    classes = {}
    for cls, path in zip(c["courses"], c["class_paths"]):
        classes[cls] = Students(path)
    return classes


def firstNamesInCourse(course):
    return list(course.values.values())
