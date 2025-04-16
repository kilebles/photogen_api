from tortoise import fields
from tortoise.models import Model


class Style(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, unique=True)
    category = fields.ForeignKeyField("models.Category", related_name="styles")

    generations: fields.ReverseRelation["Generation"]

    class Meta:
        table = "styles"
