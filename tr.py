from abc import ABC,ABCMeta, abstractmethod
from datetime import datetime
import pytz
from django.conf import settings
import collections


class lazyproperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value

class IPropery(metaclass=ABCMeta):
    @abstractmethod
    def getNames(self):
        raise NotImplementedError


class IReader(metaclass=ABCMeta):
    @abstractmethod
    def read(self):
        raise NotImplementedError


class IWriter(metaclass=ABCMeta):
    @abstractmethod
    def write(self):
        raise NotImplementedError
    

class IDjangoDate(metaclass=ABCMeta):

    @classmethod
    def setDate(cls):
        pass
        #raise NotImplementedError    
    
    @classmethod
    def getDate(cls,key,tz=pytz.timezone(settings.TIME_ZONE)):
        date = getattr(cls(), key)
        if not date:
            raise ValueError('Date is None')
        if isinstance(date,str):
            try:
                naive_datetime = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                raise ValueError('Date is not in correcti format balabalabala in setting')
            return naive_datetime.localize(tz)


class Object(ABC):
    @classmethod
    def from_model(cls, model_instance):
        instance = cls()
        for field in model_instance._meta.fields:
            value = getattr(model_instance, field.name)
            if isinstance(value, datetime):
                value = int(value.timestamp())
            setattr(instance, field.name, value)
        return instance
    
class TraditionalObject(Object):
    age = ""
    name = ""
    timestamp = None

    def __init__(self,**kwargs):
        self.age = kwargs.get('age', None)
        self.name = kwargs.get('name', None)
        self.timestamp = kwargs.get('updt_time', None)

    @property
    def timestamp(self):
        return self._updt_time
    
    @timestamp.setter
    def timestamp(self, value):
        self._updt_time = int(value.timestamp())

    

#Example:use mixin inheritance
class PostObject(Object, IPropery,IDjangoDate):
    #IPropery
    def getNames(self):
        return list(self.__dict__.keys())
