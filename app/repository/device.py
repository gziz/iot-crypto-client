import yaml
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, models
from ..database import get_db


def get_value(key: str, db: Session = Depends(get_db)):
    key_value = db.query(models.KeyValue).filter(models.KeyValue.key == key).first()
    if key_value:
        return {"value": key_value.value}
    else:
        raise HTTPException(status_code=404, detail="Key not found")

def get_all(db: Session = Depends(get_db)):
    return db.query(models.KeyValue).all()

def insert_value(req: schemas.KeyValue, db: Session = Depends(get_db)):
    key_value = db.query(models.KeyValue).filter(models.KeyValue.key == req.key).first()
    if key_value:
        key_value.value = req.value
    else:
        key_value = models.KeyValue(key=req.key, value=req.value)
        db.add(key_value)
    db.commit()
    return {"status": "success"}

def update_value(req: schemas.KeyValue, db: Session = Depends(get_db)):
    key_value = db.query(models.KeyValue).filter(models.KeyValue.key == req.key).first()
    if not key_value:
        raise HTTPException(status_code=404, detail="Key not found")

    key_value.value = req.value
    db.add(key_value)
    db.commit()
    db.refresh(key_value)
    return key_value
    

def init_db(db: Session = Depends(get_db)):
    if not db.query(models.KeyValue).first():
        with open('defaults.yaml', 'r') as f:
            defaults = yaml.safe_load(f)
        default_url = models.KeyValue(key="url", value=defaults["url"])

        db.add(default_url)
        db.commit()
        return {'message': 'Database initialized with default values'}
    else:
        return {'message': 'Database already contains data'}
    