import enum

from tortoise import fields
from tortoise.models import Q

from .base import BaseManager, BaseModel, BaseQuerySet


class TodoStatus(enum.Enum):
    CREATED = "created"
    INPROGRESS = "inProgress"
    DONE = "done"


class TodoQuerySet(BaseQuerySet):
    def get_uncompleted(self):
        return self.filter(~Q(state=TodoStatus.DONE))


class TodoManager(BaseManager):
    def get_queryset(self) -> TodoQuerySet:
        return TodoQuerySet(self._model)


class Todo(BaseModel):
    title = fields.CharField(max_length=255)
    description = fields.TextField(null=True)
    status = fields.CharEnumField(
        TodoStatus,
        max_length=255,
        default=TodoStatus.CREATED,
    )
    objects = TodoManager()

    class Meta:
        # It is highly recommended to define table attribute
        # on each config, by doing so you can refactor (rename, move to other apps)
        # without need for db migrations headache.
        table = "todos"
