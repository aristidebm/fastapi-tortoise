from fastapi import APIRouter, Depends, HTTPException  # noqa
from src.models.todo import Todo
from src.views.serializers import TodoRead
from typing_extensions import Annotated

from .filters import TodoFilterSet

router = APIRouter(prefix="/todos")


# [class-based-dependency]https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/
@router.get("/", response_model=list[TodoRead])
async def get_todos(filter: Annotated[TodoFilterSet, Depends()]):
    # FIXME: return only books that are available to the public.
    qs = Todo.objects.all()
    todos = await filter.filter_queryset(qs)
    return todos
