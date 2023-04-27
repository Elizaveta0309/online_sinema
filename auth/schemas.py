from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from db.models import Role, AccountEntrance


class RoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Role


class AccountEntranceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AccountEntrance
