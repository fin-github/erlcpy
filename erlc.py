from parts import (
    base,
    playerclass,
    serverclass,
    permissionclasses,
    teamclass,
    otherclasses,
    joinlogclass
)
from datetime import datetime

class ERLC:
    def __init__(self,
                 key: str):
        self.key = key
    
    def get_status(self):
        response = base.send_request(
            "GET",
            part="",
            key=self.key
        )
        # Set the json variable to the json of the request
        json = response.json()
        
        # Create the name variable
        name = json["Name"]
        
        # Create the name vars
        co_owner_ids = json["CoOwnerIds"]
        co_owners: list[playerclass.Player] = []
        for co_owner_id in co_owner_ids: # for co_owner_id in co_owner_ids: append that player object to co_owners
            co_owners.append(
                playerclass.Player( # Create the player class accordingly
                    name=None,
                    id=co_owner_id
                )
            )
        # amount of players
        amount_of_players: int = json["CurrentPlayers"]
        
        # max players
        max_players: int = json["MaxPlayers"]
        
        # join code
        join_code: str = json["JoinKey"]
        
        # acc verified req
        acc_verified_req: str = json["AccVerifiedReq"]
        
        # team balanced enabled
        team_balance_enabled: bool = json["TeamBalance"]
        
        return serverclass.ServerStatus(
            name=json["Name"],
            co_owners=co_owners,
            co_owner_ids=co_owner_id,
            amount_of_players=amount_of_players,
            max_players=max_players,
            join_code=join_code,
            acc_verified_req=acc_verified_req,
            team_balance_enabled=team_balance_enabled
        )
        
    def get_amount_of_players(self):
        return len(base.send_request(
            "GET",
            part="players",
            key=self.key
        ))
        
    def get_players(self):
        raw_players = base.send_request(
            "GET",
            part="players",
            key=self.key
        ).json()
        
        
        players: list[playerclass.Player] = []
        
        for player_dict in raw_players:
            try:
                callsign = player_dict["Callsign"]
            except KeyError: # meaning theyre a civ
                callsign = otherclasses.Unknown
            
            playername, playerid = player_dict["Player"].split[":"]
                
            players.append(
                playerclass.Player(
                    name=playername,
                    permission_level=permissionclasses.permission_from_str(player_dict["Permission"]),
                    callsign=callsign,
                    id=playerid
                )
            )
            
    def get_join_logs(self):
        raw_join_logs = base.send_request(
            "GET",
            part="joinlogs",
            key=self.key
        ).json()
        
        join_logs: list[joinlogclass.JoinLog] = []
        
        for join_log_dict in raw_join_logs:
            status: joinlogclass.Join | joinlogclass.Leave = joinlogclass.Join if join_log_dict["Join"] else joinlogclass.Leave
            date: datetime = datetime.fromtimestamp(join_log_dict["Timestamp"])
            playername, playerid = join_log_dict["Player"].split(";")
            player: playerclass.Player = playerclass.Player(
                name=playername,
                id=playerid
            )
            join_logs.append(
                joinlogclass.JoinLog(
                    status=status,
                    time=date,
                    player=player
                )
            )
        return join_logs
    
    def run_command(self,
                    command: str):
        curlystart = "{"
        curlyend   = "}"
        response = base.send_request(
            "POST",
            part="command",
            key=self.key,
            payload=f'{curlystart}"command": "{command}"{curlyend}'
        )
        
        match response.status_code:
            case 200:
                return True
            case 400:
                raise otherclasses.ApiError("There was an error with this package. Make sure your on the latest version!")
            case 422:
                raise otherclasses.ApiError("The current server is offline (No players)! Command was not executed.")
            case 500:
                raise otherclasses.ApiError("Error while attempting to access roblox.")