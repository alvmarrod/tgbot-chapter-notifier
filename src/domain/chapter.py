# Alvaro - Btc Sources

from dataclasses import dataclass
from src.domain.domain_exception import DomainException

if __name__ == "__main__":
    raise DomainException("Este fichero es una clase no ejecutable")

@dataclass
class MangaChapter():
    """Models a manga chapter.
    
    - Chapter name (if any)(NOT manga name)
    - Number, str because of non integers
    - A link (html)
    """
    name:   str
    number: str
    link:   str
