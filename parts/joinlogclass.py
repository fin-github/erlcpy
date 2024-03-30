from dataclasses import dataclass
from datetime import datetime
from parts import (
    playerclass
)

class Join: ...
class Leave: ...

@dataclass
class JoinLog:
    status: Join | Leave
    time: datetime
    player: playerclass.Player