from tortoise import fields
from tortoise.models import Model


class UserJob(Model):
    id = fields.IntField(primary_key=True)
    user = fields.ForeignKeyField("models.User", related_name="jobs")
    job_id = fields.CharField(max_length=100)
    job_type = fields.CharField(max_length=50)
    status = fields.CharField(max_length=50)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    generations: fields.ReverseRelation["Generation"]

    class Meta:
        table = "user_jobs"