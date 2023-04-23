from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from models import Role, AccountEntrance


class RoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Role


class AccountEntranceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AccountEntrance
