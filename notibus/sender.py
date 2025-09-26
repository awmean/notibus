#!/usr/bin/env python3

from typing import List

import dbus

from notibus import NotificationData
from notibus import Recipients


class NotibusSender:
    """Notibus notification sender with recipient filtering using dataclasses"""

    COMMON_ICONS = [
        "dialog-information", "dialog-warning", "dialog-error",
        "dialog-question", "notification-message-email",
        "notification-network-wireless", "battery-low", "security-high"
    ]

    def __init__(self):
        self.bus = dbus.SystemBus()

    def send_notification(self, notification: NotificationData) -> bool:
        """
        Send a notification signal using NotificationData dataclass

        Args:
            notification (NotificationData): Complete notification data
        """

        try:
            # Create signal message
            signal_message = dbus.lowlevel.SignalMessage(
                path="/com/notibus/Notification",
                interface="com.notibus.Notification",
                name="Notification"
            )

            # Add arguments matching the receiver's expected signature
            signal_message.append(str(notification.title))
            signal_message.append(str(notification.body))
            signal_message.append(str(notification.urgency))
            signal_message.append(str(notification.icon))
            signal_message.append(dbus.Int32(notification.timeout))
            signal_message.append(str(notification.recipients.to_json()))

            # Send the signal
            self.bus.send_message(signal_message)

            print(f"✓ Notification sent: '{notification.title}'")
            print(f"  Recipients: {notification.recipients}")
            return True

        except Exception as e:
            print(f"✗ Error sending notification: {e}")
            return False

    def send_to_everyone(self, title: str, body: str, urgency: str = "normal",
                         icon: str = "dialog-information", timeout: int = 5000) -> bool:
        """Send notification to everyone"""
        notification = NotificationData(
            title=title,
            body=body,
            urgency=urgency,
            icon=icon,
            timeout=timeout,
            recipients=Recipients.everyone()
        )
        return self.send_notification(notification)

    def send_to_admins(self, title: str, body: str, urgency: str = "normal",
                       icon: str = "security-high", timeout: int = 5000) -> bool:
        """Send notification to admin users only"""
        notification = NotificationData(
            title=title,
            body=body,
            urgency=urgency,
            icon=icon,
            timeout=timeout,
            recipients=Recipients.admins_only()
        )
        return self.send_notification(notification)

    def send_to_users(self, user_list: List[str], title: str, body: str,
                      urgency: str = "normal", icon: str = "dialog-information",
                      timeout: int = 5000) -> bool:
        """Send notification to specific users"""
        notification = NotificationData(
            title=title,
            body=body,
            urgency=urgency,
            icon=icon,
            timeout=timeout,
            recipients=Recipients.users(user_list)
        )
        return self.send_notification(notification)

    def send_to_groups(self, group_list: List[str], title: str, body: str,
                       urgency: str = "normal", icon: str = "dialog-information",
                       timeout: int = 5000) -> bool:
        """Send notification to specific groups"""
        notification = NotificationData(
            title=title,
            body=body,
            urgency=urgency,
            icon=icon,
            timeout=timeout,
            recipients=Recipients.groups(group_list)
        )
        return self.send_notification(notification)

    def send_custom(self, notification_data: NotificationData) -> bool:
        """Send a custom notification using NotificationData object"""
        return self.send_notification(notification_data)
