import yaml
from abc import ABC
from types import MappingProxyType

class Attribute:
    pass

class Config (ABC):
    _file = None

    @staticmethod
    def _add_attribute(base, attribute):
        if len(attribute.keys()) == 1:
            for key in attribute:
                setattr(base, key, attribute[key])
        else:
            for key in attribute:
                if isinstance(attribute[key], dict):
                    Config._add_attribute(base, { key: Attribute() } )
                    Config._add_attribute(getattr(base, key), attribute[key])
                else:
                    Config._add_attribute(base, { key: attribute[key] } )
        return

    @staticmethod
    def _get_attribute(key = None, base = None):
        if not base:
            base = Config
        attribute = {}
        members = base.__dict__
        for _key in members:
            if isinstance(members, MappingProxyType):
                if isinstance(members[_key], Attribute):
                    if key == None or _key == key:
                        new_base = getattr(base, _key)
                        attribute[_key] = Config._get_attribute(_key, new_base)
            else:
                attribute[_key] = members[_key]
        return attribute

    @staticmethod
    def load():
        with open(Config._file, 'r') as file:
            return yaml.safe_load(file)

    @staticmethod
    def write():
        attributes = Config._get_attribute()
        with open(Config._file, 'w') as file:
            yaml.dump(attributes, file)
            file.close()

    @staticmethod
    def init(file):
        Config._file = file
        attributes = Config.load()
        Config._add_attribute(Config, attributes)
        return
