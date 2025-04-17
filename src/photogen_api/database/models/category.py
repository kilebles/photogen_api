from tortoise import fields
from tortoise.models import Model


class Category(Model):
    id = fields.IntField(primary_key=True)
    gender = fields.CharField(max_length=10, null=True)
    title = fields.CharField(max_length=100, unique=True)
    prompt = fields.TextField(null=True)
    preview = fields.CharField(max_length=255, null=True)
    position = fields.IntField(default=0)

    styles: fields.ReverseRelation["Style"]
    generations: fields.ReverseRelation["Generation"]

    class Meta:
        table = "categories"