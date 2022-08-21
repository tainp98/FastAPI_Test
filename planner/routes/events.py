from fastapi import APIRouter, Body, Depends, HTTPException, status
from typing import List
from sqlmodel import select

from database.connection import get_session
from models.events import Events, EventUpdate

event_router = APIRouter(
tags=["Events"]
)
events = []

@event_router.get("/", response_model=List[Events])
async def retrieve_all_Event(session=Depends(get_session)):
    statement = select(Events)
    events = session.exec(statement).all()
    return events


@event_router.get("/{id}", response_model=Events)
async def retrieve_event(id: int, session=Depends(get_session)):
    event = session.get(Events, id)
    if event:
        return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )


@event_router.post("/new")
async def create_event(new_event: Events, session=Depends(get_session)):
    session.add(new_event)
    session.commit()
    session.refresh(new_event)

    return {
        "message": "Event created successfully"
    }


@event_router.put("/edit/{id}", response_model=Events)
async def update_event(id: int, new_data: EventUpdate, session=Depends(get_session)
):
    event = session.get(Events, id)
    if event:
        event_data = new_data.dict(exclude_unset=True)
        for key, value in event_data.items():
            setattr(event, key, value)

        session.add(event)
        session.commit()
        session.refresh(event)

        return event

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )


@event_router.delete("/delete/{id}")
async def delete_event(id: int, session=Depends(get_session)):
    event = session.get(Events, id)
    if event:
        session.delete(event)
        session.commit()

        return {
            "message": "Event deleted successfully"
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )