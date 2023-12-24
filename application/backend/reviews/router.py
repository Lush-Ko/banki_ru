from typing import List

from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from .. import database
# from application.backend.auth import get_current_event  # <-- import this line
from . import schema
from . import services

router = APIRouter(
    tags=['Rewiews'],
    prefix='/rewiews',
)


# Events
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_review_registration(request: schema.Rewiews,
                                     database: Session = Depends(
                                         database.get_db)):
    new_event = await services.new_event_register(request, database)
    return new_event


@router.get('/', response_model=List[schema.Rewiews])
async def get_all_reviews(database: Session = Depends(database.get_db)):
    return await services.all_events(database)


@router.get('/{event_id}', response_model=schema.Rewiews)
async def get_review_by_id(event_id: str,
                           database: Session = Depends(database.get_db)):
    return await services.get_event_by_id(event_id, database)


@router.delete('/{event_id}', status_code=status.HTTP_204_NO_CONTENT,
               response_class=Response)
async def delete_review_by_id(event_id: str,
                              database: Session = Depends(database.get_db)):
    return await services.delete_event_by_id(event_id, database)
