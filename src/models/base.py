from typing import Self

from tortoise import fields
from tortoise.manager import Manager
from tortoise.models import Model
from tortoise.queryset import QuerySet


class BaseQuerySet(QuerySet):
    def by_id(self, id) -> Self:
        return self.filter(id=id)

    def latest(self) -> Self:
        return self.order_by("-created")


class BaseManager(Manager):
    def get_queryset(self) -> BaseQuerySet:
        return BaseQuerySet(self._model)


class BaseModel(Model):
    id = fields.UUIDField(pk=True)
    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)
    # Harmonize everything here, we don't want to use
    # queries like ModelClass.all() (it possible as stated in the documentation here https://tortoise.github.io/manager.html)
    # so we define a manager that all subclasses must use like ModelClass.objects.all()
    objects = BaseManager()

    class Meta:
        abstract = True
