import psutil
import os

class HardCache:
    def __init__(self, max_size=45 * 1024 * 1024):
        self.max_size = max_size
        self.cache = {}

    def get(self, key):
        if key in self.cache:
            return self.cache[key]
        else:
            return None

    def set(self, key, value):
        if len(self.cache) >= self.max_size:
            self.prune()
        self.cache[key] = value

    def prune(self):
        # iOS uchun 45MB limitga qarshi ishlaydi
        if psutil.virtual_memory().percent > 90:
            # Agar RAM 90% dan ko'proq ishlatilgan bo'lsa, cache 10% qismini olib tashlaymiz
            prune_size = int(self.max_size * 0.1)
            keys_to_remove = sorted(self.cache.keys(), key=lambda x: len(self.cache[x]), reverse=True)[:prune_size]
            for key in keys_to_remove:
                del self.cache[key]
            os.system('sync')
            os.system('killall -9 springboard')

# Misol foydalanish:
cache = HardCache()
cache.set('key1', 'value1')
cache.set('key2', 'value2')
cache.set('key3', 'value3')
print(cache.get('key1'))  # 'value1'
print(cache.get('key2'))  # 'value2'
print(cache.get('key3'))  # 'value3'
```

Kodda, `psutil` kutubxonasidan foydalanib, RAM holatini tekshirib, agar RAM 90% dan ko'proq ishlatilgan bo'lsa, cache 10% qismini olib tashlaymiz. `os.system` funksiyalaridan foydalanib, RAM ni tozalash uchun `sync` va `killall` buyruqlarini bajaradi.
