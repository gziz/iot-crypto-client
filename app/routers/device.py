import yaml
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, database, models

router = APIRouter(prefix = "/device", tags = ["Sensor Data"])


@router.get("/value")
async def get_value(key: str = Query(...), db: Session = Depends(get_db)):
    key_value = db.query(models.KeyValue).filter(models.KeyValue.key == key).first()
    if key_value:
        return {"value": key_value.value}
    else:
        raise HTTPException(status_code=404, detail=f"Key not found")


@router.get("/value/all")
async def get_all(db: Session = Depends(get_db)):
    return db.query(models.KeyValue).all()


@router.post("/value")
async def insert_value(req: schemas.KeyValue, db: Session = Depends(get_db)):
    key_value = db.query(models.KeyValue).filter(models.KeyValue.key == req.key).first()
    if key_value:
        key_value.value = req.value
    else:
        key_value = models.KeyValue(key=req.key, value=req.value)
        db.add(key_value)
    db.commit()
    return {"status": "success"}


@router.put("/value")
async def update_value(req: schemas.KeyValue, db: Session = Depends(get_db)):
    key_value = db.query(models.KeyValue).filter(models.KeyValue.key == req.key).first()
    if not key_value:
        raise HTTPException(status_code=404, detail="Key not found")

    key_value.value = req.value
    db.add(key_value)
    db.commit()
    db.refresh(key_value)
    return key_value


@router.get('/init-db')
def init_db(db: Session = Depends(get_db)):
    if not db.query(models.KeyValue).first():
        with open('defaults.yaml', 'r') as f:
            defaults = yaml.safe_load(f)

        defaults = [models.KeyValue(key=key, value=value) for key, value in defaults.items()]
        db.add_all(defaults)
        db.commit()
        return {'message': 'Database initialized with default values'}
    else:
        return {'message': 'Database already contains data'}
