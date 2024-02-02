import pickle
import json
import base64
import gzip, zlib

def im2json(mes):
    return json.dumps({"uuid": mes["uuid"], "image": mes["image"].decode("latin-1")}).encode("latin-1")


def json2im(mes):
    load = json.loads(mes.decode("latin-1"))
    return {"uuid": load["uuid"], "image": load["image"]}
    
