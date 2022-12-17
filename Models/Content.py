from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import Optional

class Content(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, index=True)
    text: Optional[str] = Field(default=None)
    content: Optional[bytes] = Field(default=None)


