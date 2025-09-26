from enum import Enum


class RecipientType(Enum):
    EVERYONE = "everyone"
    ADMINS_ONLY = "admins_only"
    USERS = "users"
    GROUPS = "groups"
