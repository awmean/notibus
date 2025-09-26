#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Literal

from notibus import Recipients

# todo: this should include ALL of the freedesktop.Notify stuff
@dataclass
class NotificationData:
    """Complete notification data structure"""
    title: str
    body: str
    urgency: Literal["low", "normal", "critical"] = "normal"
    icon: str = "dialog-information"
    timeout: int = 5000
    recipients: Recipients = None

    def __post_init__(self):
        if self.recipients is None:
            self.recipients = Recipients.everyone()

        # Validate urgency
        if self.urgency not in ["low", "normal", "critical"]:
            self.urgency = "normal"
