
from dataclasses import dataclass
from src.domain.domain_exception import DomainException

if __name__ == "__main__":
    raise DomainException("Este fichero es una clase no ejecutable")

@dataclass
class TelegramChat():
    """Models a telegram chat.

    - ID
    - Name (title)
    """
    id:     str
    name:   str
