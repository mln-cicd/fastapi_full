from pydantic import BaseModel, conint


class VoteCreate(BaseModel):
    post_id: int
    direction: conint(le=1)
