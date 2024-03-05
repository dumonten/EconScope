import json

class ImageConverter:
    @staticmethod
    def encode(message):
        return json.dumps({"uuid": message["uuid"], "image": message["image"].decode("latin-1")}).encode("latin-1")

    @staticmethod
    def decode(message):
        load = json.loads(message.decode("latin-1"))
        return {"uuid": load["uuid"], "image": load["image"].encode("latin-1")}
