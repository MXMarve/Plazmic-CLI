class Cache:
    def __init__(self, file_name):
        self.file_name = file_name
        self.cache = {}
        self.read_cache_file()

    def read_cache_file(self):
        with open(self.file_name, "r") as f:
            for line in f:
                var, value = line.strip().split(" ", 1)
                self.cache[var] = value

    def write_cache_file(self):
        with open(self.file_name, "w") as f:
            for var, value in self.cache.items():
                f.write(f"{var} {value}\n")

    def get(self, var):
        return self.cache.get(var)

    def set(self, var, value):
        self.cache[var] = value
        self.write_cache_file()

    def delete(self, var):
        self.cache.pop(var, None)
        self.write_cache_file()