from pydantic import BaseModel

class Echo(BaseModel):
    stroka: str
    tag: str
    uid: int

