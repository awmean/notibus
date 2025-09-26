import json
from dataclasses import dataclass
from typing import List

from notibus import RecipientType


@dataclass
class Recipients:
    """Recipient filter configuration"""
    type: RecipientType
    list: List[str] = None

    def __post_init__(self):
        if self.list is None:
            self.list = []

    @classmethod
    def everyone(cls):
        return cls(type=RecipientType.EVERYONE)

    @classmethod
    def admins_only(cls):
        return cls(type=RecipientType.ADMINS_ONLY)

    @classmethod
    def users(cls, user_list: List[str]):
        return cls(type=RecipientType.USERS, list=user_list)

    @classmethod
    def groups(cls, group_list: List[str]):
        return cls(type=RecipientType.GROUPS, list=group_list)

    @classmethod
    def from_json(cls, json_data: str):
        """Create Recipients from JSON string"""
        try:
            data = json.loads(json_data)
            recipient_type = RecipientType(data.get("type", "everyone"))
            recipient_list = data.get("list", [])
            return cls(type=recipient_type, list=recipient_list)
        except (json.JSONDecodeError, ValueError, KeyError):
            # Fallback to everyone if parsing fails
            return cls.everyone()

    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps({
            "type": self.type.value,
            "list": self.list
        })

    def __str__(self):
        if self.type == RecipientType.EVERYONE:
            return "everyone"
        elif self.type == RecipientType.ADMINS_ONLY:
            return "admins only"
        elif self.type == RecipientType.USERS:
            return f"users: {', '.join(self.list)}"
        elif self.type == RecipientType.GROUPS:
            return f"groups: {', '.join(self.list)}"
        return None
