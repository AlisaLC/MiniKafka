import hashlib
import struct
from bisect import bisect_left

class ConsistentHashRing:
    def __init__(self, replicas=100):
        self.replicas = replicas
        self._keys = []
        self._nodes = {}
        self._sorted_keys = []

    def add_node(self, node):
        for i in range(self.replicas):
            key = self.gen_key('%s:%s' % (node.uuid, i))
            self._keys.append(key)
            self._nodes[key] = node
        self._sorted_keys = sorted(self._keys)

    def remove_node(self, node):
        for i in range(self.replicas):
            key = self.gen_key('%s:%s' % (node.uuid, i))
            self._keys.remove(key)
            del self._nodes[key]
        self._sorted_keys = sorted(self._keys)

    def get_node(self, key):
        if not self._nodes:
            return None
        pos = bisect_left(self._sorted_keys, self.gen_key(key))
        if pos == len(self._sorted_keys):
            return self._nodes[self._sorted_keys[0]]
        else:
            return self._nodes[self._sorted_keys[pos]]

    def gen_key(self, key):
        return struct.unpack_from('>I', hashlib.md5(key.encode('utf-8')).digest())[0]

    def __repr__(self):
        return 'ConsistentHashRing(%r)' % self._nodes