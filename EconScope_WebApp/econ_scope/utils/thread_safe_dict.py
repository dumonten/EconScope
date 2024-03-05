import threading

class ThreadSafeDict:
    def __init__(self):
        self.proc_dict = {}
        self.lock = threading.Lock()
        
    def update_dict(self, key, value):
        with self.lock:
            self.proc_dict[key] = value

    def get_dict_value(self, key):
        with self.lock:
            return self.proc_dict[key]
    
    def delete_from_dict(self, key):
        with self.lock:
            del self.proc_dict[key]