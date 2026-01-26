"""
Solution:
Task:
1. Refactor such that "InMemoryStorage" reamins the core storage.
2. Each feature becomes a layer that wraps any Storage
3. build_storage(compress, encrypt, metrics, key) returns a composed object

Target structure
1. class Storage(Protocol) or ABC with put/get
2. CompressionLayer(inner: Storage)
3. XorEncryptionLayer(inner: Storage, key: bytes)
4. MetricsLayer(inner: Storage) with stats()


We can use the decorator design pattern. Extending functionality is by adding wrappers
Instead of subclassing for each functionality, we add wrappers around the object at runtime dynamically.
Each wrapper adds it functionality and the outer most layer would call the function which inturn is 
called until the actual object is reached. 
 

Approach:
Lets have a Storage interface which the InMemoryStorage will inherit and implement get and put
So we can consider a decorator "Layer" which is an add on to the baseline storage. 
Which implments put and get. 
As a decorator class "IS A" Storage and "HAS A" Storage
So the decorator class can have children CompressionLayer, XorEncryptionLayer, MetricsLayer
"""
from abc import ABC, abstractmethod
import zlib

class StorageError(KeyError):
    pass

class Storage(ABC):
    @abstractmethod
    def put(self, key: str, data: bytes) -> None: ...
    @abstractmethod
    def get(self, key: str) -> bytes: ... 

class InMemoryStorage(Storage):
    def __init__(self):
        self._db : dict[str, bytes] = {}
    
    def put(self, key: str, data: bytes) -> None:
        self._db[key] = data
    
    def get(self, key: str) -> bytes:
        if key not in self._db:
            raise StorageError(key)
        return self._db[key]
    
class LayerDecorator(Storage):
    def __init__(self, storage: Storage):
        self._decorated_storage = storage
    
    def put(self, key: str, data: bytes) -> None:
        return self._decorated_storage.put(key, data)

    def get(self, key: str) -> bytes:
        return self._decorated_storage.get(key)

class CompressionLayer(LayerDecorator):
    def put(self, key: str, data: bytes) -> None:
        # Get from the super() object, apply transformation and put back into the super() obj
        compressed = zlib.compress(data, level=6)
        super().put(key, compressed)
    
    def get(self, key: str) -> bytes:
        temp_data = super().get(key)
        return zlib.decompress(temp_data)

class XorEncryptionLayer(LayerDecorator):
    def put(self, key: str, data: bytes) -> None:

        super().put(key, )
    
 