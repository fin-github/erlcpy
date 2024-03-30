from dataclasses import dataclass
from parts.otherclasses import Unknown
from parts.permissionclasses import Permissions

@dataclass
class Player:
    """
    A class for a player.
    
    Name not required, id is required.
    """
    name: str = Unknown,
    permission_level: Permissions.Owner | Permissions.Admin | Permissions.Moderator | Permissions.Normal = Unknown
    callsign: str = Unknown,
    id: int