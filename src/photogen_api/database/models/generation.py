from tortoise import fields
from tortoise.models import Model


class Generation(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="generations")
    job = fields.ForeignKeyField("models.UserJob", related_name="generations", null=True)
    category = fields.ForeignKeyField("models.Category", related_name="generations")
    style = fields.ForeignKeyField("models.Style", related_name="generations", null=True)

    image_url = fields.CharField(max_length=255)
    prompt = fields.TextField()
    status = fields.CharField(max_length=50)

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "generations"
