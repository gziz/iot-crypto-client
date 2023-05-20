import json
import requests

from .. import schemas, models, database
from ..crypto import ECDSA, get_keys_from_cert


def get_variables():
    
    db = database.SessionLocal()
    response = db.query(models.KeyValue).all()
    db.close()

    key_values = {kv.key: kv.value for kv in response}
    # Get private key
    d, _ = get_keys_from_cert(key_values["client_key_path"])
    key_values["d"] = d

    key_values["client_path"] = (key_values["client_cert_path"],
                                key_values["client_key_path"])
    
    return schemas.Variables(**key_values)


def add_data_manual(req: schemas.SensorData):
    ec = ECDSA()
    key_values = get_variables()

    # Turn schema SensorData into a json str object
    message = req.json()
    r, s = ec.sign(message, key_values.d)

    data = {"message": message, "r": r, "s": s}

    api_res = requests.post(url=key_values.url,
                            data=json.dumps(data),
                            cert=key_values.client_path,
                            verify=key_values.ca_cert_path)

    response = {"message": message,
                 "apiResponse": api_res.json()}
    
    return response



# def read_data():
#     pass

# def add_data():
#     ec = ECDSA()
#     key_values = get_variables()

#     # Turn schema SensorData into a json str object
#     #message = 
#     r, s = ec.sign(message, key_values.d)

#     data = {"message": message, "r": r, "s": s}

#     api_res = requests.post(url=key_values.url,
#                             data=json.dumps(data),
#                             cert=key_values.client_path,
#                             verify=key_values.ca_cert_path)

#     response = {"message": message,
#                  "apiResponse": api_res.json()}
    
#     return response
