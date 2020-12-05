#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2020/1/16 11:06

try:
    import pylibmc as memcache
    _pylibmc = True
except ImportError, e:
    import memcache
    _pylibmc = False

from rklib.utils.encoding import force_str, force_unicode


class MemcacheClient(object):

    def __init__(self, servers, default_timeout=0):
        '''
        servers is a string like "192.168.0.1:9988;192.168.0.1:9989"
        '''
        self._servers = servers
        self._current = memcache.Client(servers.split(';'))
        if _pylibmc:
            self._current.behaviors['distribution'] = 'consistent'
            self._current.behaviors['tcp_nodelay'] = 1
        self.default_timeout = default_timeout

    def add(self, key, value, timeout=0, min_compress=50):
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        self._current = memcache.Client(self._servers.split(';'))
        return self._current.add(force_str(key), value, timeout or self.default_timeout, min_compress)

    def get(self, key, default=None):
        try:
            val = self._current.get(force_str(key))
        except:
            val = self._current.get(force_str(key))
        if val is None:
            return default
        return val

    def set(self, key, value, timeout=0, min_compress=50):
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        try:
            return self._current.set(force_str(key), value, timeout or self.default_timeout, min_compress)
        except:
            return self._current.set(force_str(key), value, timeout or self.default_timeout, min_compress)

    def delete(self, key):
        try:
            try:
                val = self._current.delete(force_str(key))
            except:
                val = self._current.delete(force_str(key))
            if type(val) == bool:
                val = 1
        except:
            val = 0
        return val

    def get_multi(self, keys):
        return self._current.get_multi(map(force_str, keys))

    def close(self, **kwargs):
        self._current.disconnect_all()

    def incr(self, key, delta=1):
        return self._current.incr(key, delta)

    def decr(self, key, delta=1):
        return self._current.decr(key, delta)

    def current(self):
        return self._current


if __name__ == '__main__':
    tt = MemcacheClient('192.168.1.12:1978')
    tt.set('SealofMagic/models.user_levels.UserLevels/1', {'activity_levels': '\x80\x02]q\x01.', 'uid': 1, 'elite_process': '\x80\x02]q\x01', 'normal_process': 10102})
    print tt.get('SealofMagic/models.user_levels.UserLevels/1')