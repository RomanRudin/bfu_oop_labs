from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Protocol, Optional, TypeVar, List, Dict, Sequence, Any
import os, json
from functools import total_ordering

T = TypeVar('T')
ID = "id"


class DataRepositoryProtocol(Protocol[T]):
    def get_all(self) -> Sequence[T]:
        ...
    def get_by_id(self, id: int) -> Optional[T]:
        ...
    def add(self, item: T) -> None:
        ...
    def update(self, item:T ) -> None:
        ...
    def delete(self, item: T) -> None:
        ...



class DataRepository(DataRepositoryProtocol[T]):
    def __init__(self, file_path: str, T: type) -> None:
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            self.file_path = file_path
            self._data = self._load_data()
            self.T = T
        except Exception as e:
            print(e)
            raise FileNotFoundError

    def _load_data(self) -> None:
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(e, self.file_path, sep="\n")
            raise FileNotFoundError

    def _save_data(self) -> None:
        try:
            with open(self.file_path, 'w') as file:
                json.dump(self._data, file, indent=2)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(e, self.file_path, sep="\n")
            raise FileNotFoundError

    def get_all(self) -> Sequence[T]:
        return [self.T(**item) for item in self._load_data()]

    def get_by_id(self, id: int) -> Optional[T]:
        for item in self._load_data():
            if item[ID] == id:
                return self.T(**item)
        return None

    def add(self, item: T) -> None:
        self._data.append(item.__dict__)
        self._save_data()

    def update(self, item: T) -> None:
        for i, entry in enumerate(self._data):
            if entry[ID] == item.id:
                self._data[i] = item.__dict__
                break
        self._save_data()

    def delete(self, item: T) -> None:
        self._data = [elem for elem in self._data if elem[ID] != item.id]
        self._save_data(self._data)