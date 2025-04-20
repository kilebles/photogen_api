from tortoise import fields
from tortoise.models import Model


class UserProfile(Model):
    id = fields.IntField(primary_key=True)
    user = fields.OneToOneField("models.User", related_name="profile")
    lora_id = fields.CharField(max_length=100, null=True)
    status = fields.CharField(max_length=50, null=True)
    job_id = fields.IntField(null=True)
    photos = fields.JSONField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "user_profiles"