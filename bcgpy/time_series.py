from collections.abc import Iterator, Sequence
from typing import overload, override

from sympy import Expr


class GlobalTimeSeries(Sequence[Expr]):
    _instance: "GlobalTimeSeries | None" = None

    def __new__(cls) -> "GlobalTimeSeries":
        instance = cls._instance
        if instance is None:
            instance = object.__new__(cls)
            cls._instance = instance
        return instance

    def __init__(self) -> None:
        initialized = hasattr(self, "_data")
        if not initialized:
            self._data: list[Expr] = []

    @override
    def __setattr__(self, name: str, value: object) -> None:
        initialized = hasattr(self, "_data")
        if initialized:
            raise AttributeError("GlobalTimeSeries is read-only")
        object.__setattr__(self, name, value)

    @override
    def __delattr__(self, name: str) -> None:
        raise AttributeError("GlobalTimeSeries is read-only")

    @override
    def __len__(self) -> int:
        data = self._data
        length = len(data)
        return length

    @overload
    def __getitem__(self, index: int) -> Expr: ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[Expr]: ...

    @override
    def __getitem__(self, index: int | slice) -> Expr | Sequence[Expr]:
        data = self._data
        item = data[index]
        return item

    @override
    def __iter__(self) -> Iterator[Expr]:
        data = self._data
        iterator = iter(data)
        return iterator

    def mutable_copy(self) -> list[Expr]:
        data = self._data
        snapshot = list(data)
        return snapshot

    def reset(self) -> None:
        data = self._data
        data.clear()
