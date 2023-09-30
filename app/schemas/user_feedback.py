from typing import Optional

from pydantic import BaseModel


class UserFeedback(BaseModel):
    user_class_fruit_type: str
    user_class_maturation_stage: Optional[str]
    user_approval: bool
