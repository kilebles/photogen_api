from tortoise import fields
from tortoise.models import Model


class Style(Model):
    id = fields.IntField(primary_key=True)
    title = fields.CharField(max_length=100, unique=True)
    prompt = fields.TextField()
    position = fields.IntField()

    generations: fields.ReverseRelation["Generation"]

    class Meta:
        table = "styles"