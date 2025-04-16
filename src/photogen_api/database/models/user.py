from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(primary_key=True)
    telegram_id = fields.CharField(max_length=100, unique=True)
    first_name = fields.CharField(max_length=100, null=True)
    last_name = fields.CharField(max_length=100, null=True)
    username = fields.CharField(max_length=100, null=True)
    role = fields.CharField(max_length=50, default="new")
    gender = fields.CharField(max_length=10, null=True)
    tokens = fields.IntField(default=0)
    photo = fields.CharField(max_length=255, null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    profile: fields.ReverseRelation["UserProfile"]
    jobs: fields.ReverseRelation["UserJob"]
    generations: fields.ReverseRelation["Generation"]

    class Meta:
        table = "users"