from django.core.cache import caches

memcache = caches['memcache']
filecache = caches['filecache']
dbcache = caches['dbcache']
default = caches['default']


class CachedObject:
    settings = dict(
        cache=default,
        version=None,
        timeout=60,
    )

    def __init__(self, key, **settings):
        self._key = key
        self.settings = self.settings | settings

    def set(
        self,
        value,
        version=settings['version'],
        timeout=settings['timeout']
    ):
        self.settings['cache'].set(
            self._key, value, timeout=timeout, version=version
        )

    def get(
        self,
        default=None,
        version=settings['version'],
        timeout=settings['timeout']
    ):
        _get = self.settings['cache'].get(self._key, version=version)
        if not _get and default:
            self.set(default, version=version, timeout=timeout)
            return self.settings['cache'].get(self._key, default, version)
        return _get
