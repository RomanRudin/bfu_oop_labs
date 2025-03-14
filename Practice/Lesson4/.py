from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Protocol, Optional

@dataclass
class User:
    id: int
    login: str
    password: str = field(repr=False, compare=False)
    name: str = field(compare=False)
    #? email: Optional[str] = None
    email: Optional[str] = field(default=False, compare=False)
    address: Optional[str] = field(default=False, compare=False)


# p1 = User(id=1, 
        #    login='admin', 
        #    password='1234', 
        #    name='Vasya',
        #    email='vasya@example.com',
        #    #?address=''
        #    )
# 
# p2 = User(id=2, 
        #    login='admin', 
        #    password='1234', 
        #    name='Vasya',
        #    )
# 
# print(p1 == p2)