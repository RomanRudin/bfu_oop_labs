from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Protocol, Optional, TypeVar, List, Dict, Sequence, Any
import os, json
from functools import total_ordering

T = TypeVar('T')


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
    def __init__(self, file_path: str, entity_type: type) -> None:
        self.file_path = file_path
        self.entity_type = entity_type
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    def _load_data(self) -> List[Dict]:
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_data(self, data: List[Dict]) -> None:
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def get_all(self) -> Sequence[T]:
        return [self.entity_type(**item) for item in self._load_data()]

    def get_by_id(self, id: int) -> Optional[T]:
        for item in self._load_data():
            if item['id'] == id:
                return self.entity_type(**item)
        return None

    def add(self, item: T) -> None:
        data = self._load_data()
        data.append(item.__dict__)
        self._save_data(data)

    def update(self, item: T) -> None:
        data = self._load_data()
        for i, entry in enumerate(data):
            if entry['id'] == item.id:
                data[i] = item.__dict__
                break
        self._save_data(data)

    def delete(self, item: T) -> None:
        data = self._load_data()
        data = [entry for entry in data if entry['id'] != item.id]
        self._save_data(data)