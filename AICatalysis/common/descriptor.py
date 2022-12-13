import re

from AICatalysis.common.constant import PeriodicTable


class Descriptor(object):
    """
    Base Descriptor, <get, set, del> method of each param is unlimited
    """

    def __new__(cls, *args, **kwargs):
        if cls is Descriptor:
            raise TypeError(f"<{cls.__name__} class> may not be instantiated")
        return super().__new__(cls)

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        elif self.name in instance.__dict__.keys():
            return instance.__dict__[self.name]
        else:
            return cls.__getattr__(instance, self.name)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class ValueDescriptor(Descriptor):
    """
    Value Descriptor, limit param's value
    """

    def __init__(self, name, value):
        super(ValueDescriptor, self).__init__(name=name)
        self.value = value


class FormulaDescriptor(Descriptor):
    """
    FormulaDescriptor, check name is valid as chemical formula
    """

    def __set__(self, instance, value: str):

        # check digital
        if value.isdigit():
            raise ValueError(f"`{value}` is invalid name")

        # check special symbols
        symbols = [",", "WSC"]
        for symbol in symbols:
            if symbol in value:
                raise ValueError(f"`{value}` is invalid name")

        # check lower
        if value.islower():
            raise ValueError(f"`{value}` is invalid name")

        # check element
        check_value = value
        for element in PeriodicTable[::-1]:
            check_value = re.sub(element, '', check_value)
        check_value = re.sub(r'[\d()\[\]*.·=/Xxnη+ -]+', '', check_value)
        if len(check_value):
            raise ValueError(f"`{value}` is invalid name")

        super().__set__(instance, value)


def not_have_exclude(value, excludes):
    for item in excludes:
        if item in value:
            return False
    else:
        return True


class MetalDescriptor(ValueDescriptor):
    """
    MetalDescriptor, check name has metal
    """
    excludes = ["Reaction", "Ligand"]

    def __set__(self, instance, value):
        for item in self.value:
            if item in value and not_have_exclude(value, self.excludes):
                break
        else:
            raise ValueError(f"`{value}` is invalid name")
        super().__set__(instance, value)


class SolDescriptor(MetalDescriptor):
    """
    SolDescriptor, check name is valid as solvent
    """
    excludes = ["1a", "1 "]

    def __set__(self, instance, value):
        super(SolDescriptor, self).__set__(instance, value)


class GasDescriptor(MetalDescriptor):
    """
    SolDescriptor, check name is valid as solvent
    """
    excludes = []

    def __set__(self, instance, value):
        super(GasDescriptor, self).__set__(instance, value)


class AdditiveDescriptor(MetalDescriptor):
    """
    SolDescriptor, check name is valid as solvent
    """
    excludes = ["1a", "Reaction"]

    def __set__(self, instance, value):
        super(AdditiveDescriptor, self).__set__(instance, value)

class OxidantDescriptor(MetalDescriptor):
    """
    SolDescriptor, check name is valid as solvent
    """
    excludes = ["1a", "Reaction"]

    def __set__(self, instance, value):
        super(OxidantDescriptor, self).__set__(instance, value)


class LigandDescriptor(ValueDescriptor):
    """
    LigandDescriptor, check name is valid as solvent
    """

    def __set__(self, instance, value):
        for item in self.value:
            if item in value:
                break
        else:
            raise ValueError(f"`{value}` is invalid name")
        super().__set__(instance, value)


class TimeDescriptor(Descriptor):
    """
    TimeDescriptor, check name is valid as time
    """

    def __set__(self, instance, value):
        if re.search('[0-9]+\s*h', value) is None:
            raise ValueError(f"`{value}` is invalid name")
        super().__set__(instance, value)
