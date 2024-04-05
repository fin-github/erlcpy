from erlclib.parts.base import *
from erlclib.parts.playerclass import *
from erlclib.parts.serverclass import *
from erlclib.parts.permissionclasses import *
from erlclib.parts.teamclass import *
from erlclib.parts.otherclasses import *
from erlclib.parts.joinlogclass import *
from erlclib.parts.commandlogclass import *
from erlclib.parts.stringify import stringify
from datetime import datetime
from icecream import ic
from json import dumps
from time import sleep as wait

class ERLC:
    def __init__(self,
                 key: str,
                 ratelimit_key: str = None):
        self.key = key
        self.ratelimit_key = ratelimit_key
    
    def get_status(self):
        response = send_request(
            "GET",
            part="",
            key=self.key,
            ratelimit_key=self.ratelimit_key
        )
        # Set the json variable to the json of the request
        json = response.json()
        
        # Create the name variable
        name = json["Name"]
        
        # owner
        owner = Player(
            id=json["OwnerId"]
        )
        
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
        
        return ServerStatus(
            name=json["Name"],
            owner=owner,
            co_owners=co_owners,
            co_owner_ids=co_owner_id,
            amount_of_players=amount_of_players,
            max_players=max_players,
            join_code=join_code,
            acc_verified_req=acc_verified_req,
            team_balance_enabled=team_balance_enabled
        )
        
    def get_players(self):
        raw_players = send_request(
            "GET",
            part="players",
            key=self.key,
            ratelimit_key=self.ratelimit_key
        ).json()
        if not type(raw_players) is dict: print(f"Incorrect type! {type(raw_players)}")
        
        
        players: list[playerclass.Player] = []
        
        for player_dict in raw_players:
            try:
                callsign = player_dict["Callsign"]
            except KeyError: # meaning theyre a civ
                callsign = Unknown
            
            ic(raw_players)
            try:
                playername, playerid = player_dict["Player"].split(":")[0], player_dict["Player"].split(":")[1]
            except:
                playername, playerid = Unknown, Unknown
                
            players.append(
                playerclass.Player(
                    name=playername,
                    permission_level=permission_from_str(player_dict["Permission"]),
                    callsign=callsign,
                    id=playerid
                )
            )
        return players
    
    def get_amount_of_players(self):
        return len(self.get_players())
            
    def get_join_logs(self):
        raw_join_logs = send_request(
            "GET",
            part="joinlogs",
            key=self.key,
            ratelimit_key=self.ratelimit_key
        ).json()
        
        join_logs: list[JoinLog] = []
        
        for join_log_dict in raw_join_logs:
            status: Join | Leave = Join if join_log_dict["Join"] else Leave
            date: datetime = datetime.fromtimestamp(join_log_dict["Timestamp"])
            playername, playerid = join_log_dict["Player"].split(":")
            player: playerclass.Player = playerclass.Player(
                name=playername,
                id=playerid
            )
            join_logs.append(
                JoinLog(
                    status=status,
                    time=date,
                    player=player
                )
            )
        return join_logs
    
    def get_command_logs(self):
        raw_cmd_logs = send_request(
            "GET",
            part="commandlogs",
            key=self.key,
            ratelimit_key=self.ratelimit_key
        )
        ic(raw_cmd_logs)
        raw_cmd_logs = raw_cmd_logs.json()
        
        cmd_logs: list[CommandLog] = []
        
        for cmd_log_dict in raw_cmd_logs:
            try:
                date: datetime = datetime.fromtimestamp(cmd_log_dict["Timestamp"])
            except TypeError:
                date: datetime = datetime.fromtimestamp(int(cmd_log_dict["Timestamp"]))
            try:
                playername, playerid = cmd_log_dict["Player"].split(":")
            except ValueError:
                if cmd_log_dict["Player"] == "Remote Server":
                    rs = RemoteServer()
                    playername, playerid = rs, Unknown
                else:
                    print(f"Could not unpack {cmd_log_dict['Player']}, set to Unknown.")
                    playername, playerid = Unknown, Unknown
            
            if not playername is RemoteServer():
                player: playerclass.Player = playerclass.Player(
                    name=playername,
                    id=playerid
                )
            else:
                player = playername # player = RemoteServer
            command = cmd_log_dict["Command"]
            
            
            cmd_logs.append(
                CommandLog(
                    player=player,
                    date=date,
                    command=command
                )
            )
        return cmd_logs
        
        
    
    def run_command(self,
                    command: str): 
        response = send_command_request(
            command=command,
            key=self.key,
            ratelimit_key=self.ratelimit_key
        )
        
        match response.status_code:
            case 200:
                return True
            case 400:
                raise ApiError("There was an error with this package. Make sure your on the latest version!")
            case 422:
                raise ApiError("The current server is offline (No players)! Command was not executed.")
            case 500:
                raise ApiError("Error while attempting to access roblox.")
