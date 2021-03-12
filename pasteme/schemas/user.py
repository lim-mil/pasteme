from pydantic import BaseModel, validator


class UserInCreate(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str

    @validator('confirm_password')
    def make_sure_password(cls, v, values, **kwargs):
        if 'password' in values and values['password'] == v:
            return v
        raise ValueError("confirm_password is different from password")
