#!/usr/bin/env python3

import grp
import os
import pwd

import dbus
import dbus.mainloop.glib
from gi.repository import GLib

from notibus import NotificationData, RecipientType, Recipients


class NotibusReceiver:
    def __init__(self, admin_groups: list[str] = ['sudo']):
        self.admin_groups = admin_groups

        self.current_user = pwd.getpwuid(os.getuid()).pw_name
        self.user_groups = [grp.getgrgid(g).gr_name for g in os.getgroups()]

        self.is_admin = bool(set(self.admin_groups).intersection(set(self.user_groups)))

        print(f"Notibus started for user: {self.current_user}")
        print(f"User groups: {', '.join(self.user_groups)}")
        print(f"Admin privileges: {'Yes' if self.is_admin else 'No'}")
        print("-" * 50)

    def check_recipient_filter(self, recipients: Recipients) -> bool:
        """Check if current user should receive this notification"""
        if recipients.type == RecipientType.EVERYONE:
            return True

        elif recipients.type == RecipientType.ADMINS_ONLY:
            return self.is_admin

        elif recipients.type == RecipientType.USERS:
            return self.current_user in recipients.list

        elif recipients.type == RecipientType.GROUPS:
            return bool(set(recipients.list).intersection(set(self.user_groups)))

        return False

    def send_notification(self, notification: NotificationData) -> bool:
        """Send desktop notification using D-Bus FreeDesktop notifications"""
        try:
            # Connect to session bus for desktop notifications
            session_bus = dbus.SessionBus()

            # Get the notification service
            notify_service = session_bus.get_object(
                'org.freedesktop.Notifications',
                '/org/freedesktop/Notifications'
            )
            notify_interface = dbus.Interface(
                notify_service,
                'org.freedesktop.Notifications'
            )

            # Map urgency levels to D-Bus notification urgency
            urgency_map = {
                'low': 0,
                'normal': 1,
                'critical': 2
            }

            # Prepare hints dictionary
            hints = {'urgency': dbus.Byte(urgency_map.get(notification.urgency, 1)), 'desktop-entry': 'notibus'}

            # Add desktop-entry hint for better integration

            # Send notification via D-Bus
            # Notify method signature: (app_name, replaces_id, app_icon, summary, body, actions, hints, expire_timeout)
            notification_id = notify_interface.Notify(
                'notibus',  # app_name
                dbus.UInt32(0),  # replaces_id (0 = new notification)
                notification.icon,  # app_icon
                notification.title,  # summary
                notification.body,  # body
                dbus.Array([], signature='s'),  # actions (empty array)
                hints,  # hints
                dbus.Int32(notification.timeout)  # expire_timeout
            )

            print(f"✓ Notification sent via D-Bus (ID: {notification_id}): {notification.title}")
            return True

        except dbus.exceptions.DBusException as e:
            print(f"✗ D-Bus error: {e}")
            return False
        except Exception as e:
            print(f"✗ Failed to send notification: {e}")
            return False

    def handle_notification_signal(self, title, body, urgency="normal", icon="dialog-information",
                                   timeout=5000, recipients_json='{"type":"everyone","list":[]}'):
        """Handle incoming notification signals"""

        # Parse recipients
        recipients = Recipients.from_json(recipients_json)

        # Create notification data
        notification = NotificationData(
            title=str(title),
            body=str(body),
            urgency=str(urgency) if urgency in ["low", "normal", "critical"] else "normal",
            icon=str(icon),
            timeout=int(timeout),
            recipients=recipients
        )

        print(f"Signal received:")
        print(f"  Title: {notification.title}")
        print(f"  Body: {notification.body}")
        print(f"  Urgency: {notification.urgency}")
        print(f"  Icon: {notification.icon}")
        print(f"  Timeout: {notification.timeout}")
        print(f"  Recipients: {notification.recipients}")

        # Check if this user should receive the notification
        if self.check_recipient_filter(notification.recipients):
            print(f"  → Authorized for user '{self.current_user}' ✓")
            self.send_notification(notification)
        else:
            print(f"  → Not authorized for user '{self.current_user}' ✗")

        print("-" * 50)

    def run(self):
        """Start the notification receiver"""
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        try:
            bus = dbus.SystemBus()

            # Listen for notification signals
            bus.add_signal_receiver(
                self.handle_notification_signal,
                signal_name="Notification",
                dbus_interface="com.notibus.Notification"
            )

            print("Listening for notifications on com.notibus.Notification interface...")

            loop = GLib.MainLoop()
            loop.run()

        except KeyboardInterrupt:
            print("\nShutting down...")
        except Exception as e:
            print(f"Error: {e}")
