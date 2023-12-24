from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship, backref
from application.backend.database import Base


class Review(Base):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String(4000), nullable=False)
    problem = Column(String(256))
    problem_short = Column(String(128))
    solution = Column(String(256))
    tags = Column(String(256))
    date = Column(DateTime())

    def __init__(self, id, text, problem, problem_short, solution, tags, *args, **kwargs):
        self.id = id
        self.text = text
        self.problem = problem
        self.problem_short = problem_short
        self.solution = solution
        self.tags = tags
