
from dataclasses import dataclass


@dataclass
class BotCommandDefinition:
    """Describes a bot command"""
    command: str
    description: str
    group_name: str
    index: int
