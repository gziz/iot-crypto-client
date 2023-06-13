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
    
    return schemas.Variables(**key_values)


def send_data_manual(req: schemas.SensorData):
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



def read_send_data():
    db = database.SessionLocal()
    record = db.query(models.SensorData).filter(models.SensorData.sent != 1).first()

    message = json.dumps(record.to_dict())

    ec = ECDSA()
    key_values = get_variables()

    # Turn schema SensorData into a json str object
    r, s = ec.sign(message, key_values.d)

    data = {"message": message, "r": r, "s": s}

    api_res = requests.post(url=key_values.url,
                            data=json.dumps(data),
                            cert=(key_values.client_cert_path,
                                   key_values.client_key_path),
                            verify=key_values.ca_cert_path)
    
    record.sent = 1
    db.commit()
    db.close()

    return api_res.json()