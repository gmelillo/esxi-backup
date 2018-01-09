__author__ = 'Gabriel Melillo <gabriel@melillo.me>'
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser
from os import path


def get_file_path(_file):
    return path.dirname(path.realpath(_file))


def get_config_path(_file_, filename):
    return path.abspath(get_file_path(_file_) + filename)


class ConfigurationINI(object):
    def __init__(self, config_file):
        self.config = ConfigParser()
        self.config.read(config_file)
        self.config_file = config_file

    def __getitem__(self, item):
        return self.config_section_map(item)

    def __iter__(self):
        for val in self.config.sections():
            yield val

    def __len__(self):
        return len(self.config.sections())

    def __setitem__(self, key, value):
        if not isinstance(value, dict):
            raise AttributeError('value must be dict()')

        if 'key' not in value.keys():
            raise KeyError('key missing.')
        if 'value' not in value.keys():
            raise KeyError('value missing.')

        if not key in self.config.sections():
            self.config.add_section(key)

        self.config.set(key, value['key'], value['value'])
        self.config.write(
            open(self.config_file, 'w')
        )

    def config_section_map(self, section):
        dict1 = {}
        options = self.config.options(section)
        for option in options:
            try:
                dict1[option] = self.config.get(section, option)
            except:
                dict1[option] = None
        return dict1
