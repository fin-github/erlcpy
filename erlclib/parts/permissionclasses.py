class Permissions:
    class Owner: ...
    class Admin: ...
    class Moderator: ...
    class Normal: ...
    
def permission_from_str(permission_str: str):
    try:
        return {
            "Server Owner": Permissions.Owner,
            "Server Administrator": Permissions.Admin,
            "Server Moderator": Permissions.Moderator,
            "Normal": Permissions.Normal
        }[permission_str]
    except KeyError:
        raise KeyError(f"{permission_str} is not a valid ER:LC permission level.")