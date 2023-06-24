from tortoise.queryset import QuerySet

from .base import FilterSet


class OrderingFilterSet(FilterSet):
    def __init__(self, ordering: str | None = None) -> None:
        super().__init__()
        self.ordering = ordering

    def filter_queryset(self, qs: QuerySet, *args, **kwargs) -> QuerySet:
        qs = super().filter_queryset(qs)

        if not isinstance(self.ordering, str):
            return qs

        _, _, field = self.ordering.partition("-")

        if field not in qs.model._meta.db_fields:
            return qs
        return qs.order_by(self.ordering)
