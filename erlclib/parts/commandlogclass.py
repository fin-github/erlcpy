from dataclasses import dataclass
from erlclib.parts.playerclass import Player
from datetime import datetime



@dataclass
class CommandLog:
    player: Player
    date: datetime
    command: str