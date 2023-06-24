"""
[python-descriptors](https://docs.python.org/3/howto/descriptor.html#customized-names)
[fastapi-class-dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/)
"""

from tortoise.queryset import QuerySet


class Filter:
    def __init__(
        self,
        *,
        lookup: str = "exact",
        exclude: bool = False,
        source: str = None,
    ):
        self.lookup = lookup
        self.exclude = exclude
        self.source = source
        self.parent = None
        self._value = None
        self._fieldname = None

    def __set_name__(self, owner, name):
        self._fieldname = name
        self.source = self.source or self._fieldname

    def __get__(self, obj, objtype=None):
        return self._value

    def __set__(self, obj, value):
        self._value = value
        self.parent = obj

    def __repr__(self) -> str:
        return f"{type(self).__name__}(lookup={self.lookup}, source={self.source}, exclude={self.exclude})"

    def filter(self, qs: QuerySet) -> QuerySet:
        if not self._value:
            return qs
        predicate = {f"{self.source}__{self.lookup}": self._value}
        return self.get_method(qs)(**predicate)

    def get_method(self, qs: QuerySet):
        return qs.exclude if self.exclude else qs.filter


class FilterSet:
    def filter_queryset(
        self,
        qs: QuerySet,
        *args,
        **kwargs,
    ) -> QuerySet:
        """
        Filter querysets are not aimed to touch the database so
        `filter_queryset` need to be a sync function.

        Args:
            qs (QuerySet): tortoise.queryset.QuerySet

        Returns:
            tortoise.queryset.QuerySet:
        """
        for source, filter in self.filters.items():
            if source not in qs.model._meta.db_fields:
                continue
            qs = filter.filter(qs)
        return qs

    def __init_subclass__(cls) -> None:
        cls.filters = {}
        for filter in cls.__dict__.values():
            if isinstance(filter, Filter):
                cls.filters[filter.source] = filter

    def __repr__(self) -> str:
        cls = type(self)
        rep = [f"{cls.__name__}", "("]
        for name, field in cls.__dict__.items():
            if isinstance(field, Filter):
                rep.extend([f"\n{name} = {field!r}", ","])
        rep.extend(["\n", ")"])
        return "".join(rep)
