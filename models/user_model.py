from pydantic import BaseModel

class User(BaseModel):
    profile_name: str
    target: str
    score_list: str