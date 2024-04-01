from dataclasses import dataclass
from erlclib.parts.playerclass import Player

@dataclass
class ServerStatus:
    """
    The status of a server.
    """
    name: str
    owner: Player
    co_owners: list[Player]
    co_owner_ids: list[int]
    amount_of_players: int
    max_players: int
    join_code: str
    acc_verified_req: str
    team_balance_enabled: bool