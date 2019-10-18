import datetime
from dataclasses import dataclass, MISSING

import marshmallow as ma

from app.core.types import bunch
from app.core.types import FilterParams


class Schema(ma.Schema):
    dict_class = bunch


class FilterSchema(Schema):
    dict_class = FilterParams


@dataclass
class User(bunch):
    id: int = 0
    name: str = ''
    is_enabled: bool = True
    created_at: datetime.datetime = datetime.datetime.now
    updated_at: datetime.datetime = datetime.datetime.now


class UserSchema(ma.Schema):
    dict_class = User
    id = ma.fields.Integer(required=True)
    name = ma.fields.String(required=True)


schema = UserSchema()
user = schema.load({'id': 1, 'name': 'test'})
assert 1 == user.id, user.id
assert 'test' == user['name'], user.name
assert True is user.is_enabled, user.is_enabled
assert isinstance(user.created_at, datetime.datetime)
