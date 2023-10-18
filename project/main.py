from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from schemas import ContactCreate, ContactUpdate, Contact  # Импортируем Pydantic модели
from datetime import date, timedelta

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/contacts/", response_model=Contact)  # Используем Pydantic модель в response_model
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.get("/contacts/{contact_id}", response_model=Contact)  # Используем Pydantic модель в response_model
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@app.put("/contacts/{contact_id}", response_model=Contact)
def update_contact(contact_id: int, contact_update: ContactUpdate, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    for field, value in contact_update.dict().items():
        setattr(db_contact, field, value)
    
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.delete("/contacts/{contact_id}", response_model=Contact)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return contact

@app.get("/contacts/", response_model=list[Contact])
def search_contacts(q: str, db: Session = Depends(get_db)):
    contacts = db.query(Contact).filter(
        (Contact.first_name.ilike(f"%{q}%")) |
        (Contact.last_name.ilike(f"%{q}%")) |
        (Contact.email.ilike(f"%{q}%"))
    ).all()
    return contacts

@app.get("/contacts/birthdays/", response_model=list[Contact])
def upcoming_birthdays(db: Session = Depends(get_db)):
    current_date = date.today()
    seven_days_later = current_date + timedelta(days=7)
    upcoming_birthday_contacts = (
        db.query(Contact)
        .filter(Contact.birthdate >= current_date, Contact.birthdate <= seven_days_later)
        .all()
    )
    return upcoming_birthday_contacts
