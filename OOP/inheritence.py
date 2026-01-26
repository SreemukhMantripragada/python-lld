"""
Docstring for Python-LLD.OOP.inheritence
Design: Storage with compression, encryption, metrics features.
This is a legacy inheritence design of a key->value storage. 
Optional features supported:
1. Compression(zlib)
2. Encryption(simple XOR cipher)
3. Metrics(Count operations)

Feature combos are created using new subclasses like "EncryptedCompressedStorage" this does not scale as it is meant to explode as combinations increase. 

Task: Refactor to a composition based design. 

Requirements:
1. Public API stays same:
    put(key: str, data: bytes) -> None
    get(key: str) -> bytes
2. Semantics to preserve:
    If both compression+encryption are enabled
    . On put: Compress->Encrypt
    . On get: Decrypt->Decompress
3. Metrics Feature:
    . Count puts and gets
    . expose stats() returning {"puts": int, "gets": int} (Only if metrics enabled)
4. Must be able to stack features in code like 
    storage = MetricsLayer(XorEncryptionLayer(CompressionLayer(InMemoryStorage())))
"""
import zlib
from dataclasses import dataclass

def xor_crypt(data: bytes, key: bytes) -> bytes:
    # repeat-key XOR (toy crypto)
    out = bytearray(len(data))
    for i, b in enumerate(data):
        out[i] = b ^ key[i % len(key)]
    return bytes(out)

class StorageError(KeyError):
    pass

class BaseStorage:
    def put(self, key: str, data: bytes) -> None:
        raise NotImplementedError

    def get(self, key: str) -> bytes:
        raise NotImplementedError

class InMemoryStorage(BaseStorage):
    def __init__(self):
        self._db: dict[str, bytes] = {}

    def put(self, key: str, data: bytes) -> None:
        self._db[key] = data

    def get(self, key: str) -> bytes:
        if key not in self._db:
            raise StorageError(key)
        return self._db[key]

class CompressedStorage(InMemoryStorage):
    def put(self, key: str, data: bytes) -> None:
        super().put(key, zlib.compress(data, level=6))

    def get(self, key: str) -> bytes:
        return zlib.decompress(super().get(key))

class EncryptedStorage(InMemoryStorage):
    def __init__(self, key: bytes):
        super().__init__()
        self._key = key

    def put(self, key: str, data: bytes) -> None:
        super().put(key, xor_crypt(data, self._key))

    def get(self, key: str) -> bytes:
        return xor_crypt(super().get(key), self._key)

class EncryptedCompressedStorage(InMemoryStorage):
    # subclass explosion begins...
    def __init__(self, key: bytes):
        super().__init__()
        self._key = key

    def put(self, key: str, data: bytes) -> None:
        compressed = zlib.compress(data, level=6)
        encrypted = xor_crypt(compressed, self._key)
        super().put(key, encrypted)

    def get(self, key: str) -> bytes:
        encrypted = super().get(key)
        compressed = xor_crypt(encrypted, self._key)
        return zlib.decompress(compressed)

def build_legacy_storage(*, compress: bool, encrypt: bool, key: bytes | None):
    if compress and encrypt:
        if not key:
            raise ValueError("key required when encrypt=True")
        return EncryptedCompressedStorage(key)
    if compress:
        return CompressedStorage()
    if encrypt:
        if not key:
            raise ValueError("key required when encrypt=True")
        return EncryptedStorage(key)
    return InMemoryStorage()