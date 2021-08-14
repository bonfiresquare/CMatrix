import yaml
from abc import ABC
from types import MappingProxyType


class Attribute:
    pass


class Config (ABC):
    _file = None

    @staticmethod
    def init(file):
        Config._file = file
        attributes = Config.load()
        Config._add_attribute(attributes)
        return

    @staticmethod
    def _add_attribute(attribute, base = None):
        if not base:
            base = Config
        if len(attribute.keys()) == 1:
            for _key, _value in attribute.items():
                setattr(base, _key, _value)
        else:
            for _key, _value in attribute.items():
                if isinstance(_value, dict):
                    Config._add_attribute({_key: Attribute()}, base)
                    Config._add_attribute(_value, getattr(base, _key))
                else:
                    Config._add_attribute({_key: _value}, base)
        return

    @staticmethod
    def _get_attribute(key = None, base = None):
        if not base:
            base = Config
        attribute = {}
        members = base.__dict__
        for _key, _value in members.items():
            if isinstance(members, MappingProxyType):
                if isinstance(_value, Attribute):
                    if not key or _key == key:
                        new_base = getattr(base, _key)
                        attribute[_key] = Config._get_attribute(_key, new_base)
            else:
                attribute[_key] = _value
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

if __name__ == '__main__':
    Config.init('config.yml')
    c = Config._get_attribute()
    print(c)
