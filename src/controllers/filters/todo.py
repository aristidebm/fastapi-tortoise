from .base import Filter
from .ordering import OrderingFilterSet


class TodoFilterSet(OrderingFilterSet):
    title = Filter(lookup="iexact")
    description = Filter(lookup="iexact")

    def __init__(
        self,
        ordering: str | None = None,
        title: str | None = None,
        description: str | None = None,
    ):
        super().__init__(ordering)
        self.title = title
        self.description = description
