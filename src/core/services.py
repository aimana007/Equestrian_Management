from sqlalchemy.orm import Session, joinedload
from src.core.models import Rider, Horse, Entry


def register_entry(session: Session, rider_name: str, rider_age: int, horse_name: str, horse_age: int, event_name: str):
    rider = session.query(Rider).filter_by(name=rider_name).first()
    if not rider:
        rider = Rider(name=rider_name, age=rider_age)
        session.add(rider)
        session.commit()

    horse = session.query(Horse).filter_by(name=horse_name).first()
    if not horse:
        horse = Horse(name=horse_name, age=horse_age)
        session.add(horse)
        session.commit()

    entry = Entry(rider_id=rider.id, horse_id=horse.id, event_name=event_name)
    session.add(entry)
    session.commit()
    return entry


def add_score(session: Session, entry_id: int, score: int):
    entry = session.query(Entry).filter_by(id=entry_id).first()
    if entry:
        entry.score = score
        session.commit()
        return entry
    return None


def list_entries(session: Session):
    return session.query(Entry).options(
        joinedload(Entry.rider),
        joinedload(Entry.horse)
    ).all()
