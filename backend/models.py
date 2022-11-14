from pydantic import BaseModel
from enum import Enum 

class Styles(str, Enum):
    baroque: str = 'Baroque'
    impression: str = 'Impressionism'
    harlem: str = 'Harlem Renaissance'

class Commission(BaseModel):
    style : Styles
    passage : str

class Passage(BaseModel):
    chapter: int
    text: str

class Meta(BaseModel):
    lang: str
    source: str
    cover: str

class Book(BaseModel):
    title: str
    author: str
    genre: str
    metadata: Meta
    passages: Passage