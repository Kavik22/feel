from pydantic import BaseModel
from typing import Optional, List


class UserValidator(BaseModel):
    email: str
    last_reset_code: Optional[int] | None = None
    password: Optional[str] | None = None
    re_password: Optional[str] | None = None
    wishes: Optional[str] | None = None
    calendar: Optional[str] | None = None
    test_result: Optional[str] | None = None


class MailBodyValidator(BaseModel):
    to: List[str]
    subject: str
    body: str
