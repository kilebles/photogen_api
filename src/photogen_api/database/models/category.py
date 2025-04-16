from tortoise import fields
from tortoise.models import Model


class Category(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)

    styles: fields.ReverseRelation["Style"]
    generations: fields.ReverseRelation["Generation"]

    class Meta:
        table = "categories"