import random
import sys

class Section:
    def __init__(self, name, text):
        self.name = name
        self.text = text
        self.tags = set()

    def add_tags(self, tags):
        self.tags.update(set(tags))

    def hastag(self, tag):
        return tag in self.tags

    def __repr__(self):
        return "Section(%s, %s, %s)" % (repr(self.name), repr(self.text),
                                        repr(self.tags))

    def format(self, references):
        pass

class ShuffledSections:
    def __init__(self, as_list, from_nr, to_nr, from_name, nr_sections):
        self.as_list = as_list
        self.from_nr = from_nr
        self.to_nr = to_nr
        self.from_name = from_name
        self.name_to_nr = {}
        for n in from_name:
            self.name_to_nr[n] = to_nr[from_name[n]]
        for nr in nr_sections:
            self.name_to_nr[nr_sections[nr]] = nr

class Book:
    def __init__(self):
        self.sections = []
        self.from_name = {}
        self.nr_sections = {}
        self.max = 0
        self.codewords = set()

    def add(self, section):
        if section.name in self.from_name:
            raise Exception('Duplicate section names (%s) not allowed.' %
                            section.name)
        self.sections.append(section)
        self.from_name[section.name] = section
        if len(self.sections) > self.max:
            self.max = len(self.sections)

    def add_codeword(self, word):
        self.codewords.add(word)

    def force_section_nr(self, name, nr):
        self.nr_sections[nr] = name
        if nr > self.max:
            self.max = nr

    def shuffle(self):
        as_list = [None]
        from_nr = {}
        to_nr = {}
        shuffled = self.sections[:]
        for p in self.nr_sections.values():
            if p in self.from_name:
                shuffled.remove(self.from_name[p])
        random.shuffle(shuffled)
        for nr in range(1, self.max + 1):
            if (self.nr_sections.has_key(nr)
                and self.nr_sections[nr] in self.from_name):
                section = self.from_name[self.nr_sections[nr]]
            elif len(shuffled):
                section = shuffled.pop()
            else:
                section = None
            as_list.append(section)
            from_nr[nr] = section
            if section:
                to_nr[section] = nr
        return ShuffledSections(as_list, from_nr, to_nr, self.from_name.copy(),
                                self.nr_sections)

class Item (object):
    def __init__(self, name):
        self.name = name

class Hero (object):
    "The hero (player character) of a Book."
    def __init__(self):
        self.carrying_capacity = 10
        self.skills = set()
