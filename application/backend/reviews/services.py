from typing import List, Optional, Union

from fastapi import HTTPException, status

from . import models


async def new_event_register(request, database) -> models.Review:
    new_event = models.Review(id=request.id,
                              text=request.text,
                              problem=request.problem,
                              )
    database.add(new_event)
    database.commit()
    database.refresh(new_event)
    return new_event


def all_events(database) -> List[models.Review]:
    events = database.query(models.Review).all()
    return events


async def get_event_by_id(id, database) -> Optional[models.Review]:
    event_info = database.query(models.Review).get(id)
    if not event_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Data Not Found !")
    return event_info


async def delete_event_by_id(id, database):
    database.query(models.Review).filter(
        models.Review.id == id).delete()
    database.commit()
