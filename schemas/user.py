from ma import ma
from models.user import User


class UserSchema(ma.ModdelSchema):
    class Meta:
        fields = ('id', 'name', 'email', 'password')