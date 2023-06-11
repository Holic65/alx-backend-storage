#!/usr/bin/env python3
"""0. Writing strings to Redis"""
import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    ''' a function that counts how many times a cache is called'''

    @wraps(method)
    def wrapper(self, *args, **kwds):
        '''wrapper function'''
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args,**kwds)

    return wrapper


def call_history(method: Caallable) -> Callable:
    ''' function that stores history of inputs and outputs '''

    @wraps(method)
    def wrapper(self, *args,**kwds)
        '''wrapper function '''
        self._redis.rpush(method.__qualname__ + ":inputs", str(args))
        output = method(self, *args, **kwds)
        self.__redis.rpush(method.__qualname__ + ":outputs", str(output))
        return output

    return wrapper


class Cache:
    """Cache class"""
    def __init__(self):
        """Constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb()
    
    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in redis"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) ->\
            Union[str, bytes, int, float, None]:
        """Get data from redis"""
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        ''' a function that get data from redis as str'''
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        ''' gets data from redis as int '''
        return self.get(key, int)


    def replay(val: Cache):
        '''replays history of all calls made on class'''
        clsName = val.__qualname__
        print(f"""{clsName} was called {
                val.__self__.get(clsName).decode("utf-8")} times:""")
        inputs = val.__self__.redis.lrange(f"{clsName}:inputs", 0, -1)
        outputs = val.__self.redis.lrange(f"{clsName}:outputs", 0, -1)
        zipped = zip(inputs, outputs)
        for i, o in zipped:
            print(f"""{clsName}(*{i.decode("utf-8")}) -> {o.decode("utf-8")}""")
