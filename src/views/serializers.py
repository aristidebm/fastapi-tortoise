from src.models import Todo
from tortoise.contrib.pydantic import pydantic_model_creator

TodoRead = pydantic_model_creator(
    cls=Todo,
    include=(
        "title",
        "description",
        "created",
    ),
)
