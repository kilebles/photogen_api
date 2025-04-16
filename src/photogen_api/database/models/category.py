from tortoise import fields
from tortoise.models import Model


class Category(Model):
    id = fields.IntField(primary_key=True)
    title = fields.CharField(max_length=100, unique=True)
    preview = fields.CharField(max_length=255, null=True)

    styles: fields.ReverseRelation["Style"]
    generations: fields.ReverseRelation["Generation"]

    class Meta:
        table = "categories"