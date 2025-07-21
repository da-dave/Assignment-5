from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas

def create(db: Session, sandwich):
    # Create a new instance of the Sandwich model with the provided data
    db_sandwich = models.Sandwich(
        sandwich_name=sandwich.sandwich_name,
        price=sandwich.price
    )
    # Add the newly created Order object to the database session
    db.add(db_sandwich)
    # Commit the changes to the database
    db.commit()
    # Refresh the Order object to ensure it reflects the current state in the database
    db.refresh(db_sandwich)
    # Return the newly created Order object
    return db_sandwich

def update(db: Session, sandwich_id, sandwich):
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()
    update_data = sandwich.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_sandwich, key, value)

    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich



def delete(db: Session, sandwich_id):
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()

    db.delete(db_sandwich)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


def read_all(db: Session):
    return db.query(models.Sandwich).all()

def read_one(db: Session, sandwich_id):
    return db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()