from notibus.notification_data import NotificationData
from notibus.recipients import Recipients
from notibus.sender import NotibusSender

if __name__ == '__main__':
    print("Example library usage:")
    print()

    # Example of using as library with dataclasses
    sender = NotibusSender()

    # Method 1: Using convenience methods
    sender.send_to_everyone("Hello", "World!")
    sender.send_to_admins("System Alert", "Maintenance required", urgency="critical")
    sender.send_to_users(["alice", "bob"], "Meeting", "Conference room A at 2pm")
    sender.send_to_groups(["developers"], "Build Status", "CI pipeline completed")

    # Method 2: Using dataclasses directly
    notification = NotificationData(
        title="Custom Notification",
        body="Using dataclass directly",
        urgency="normal",
        icon="dialog-information",
        timeout=8000,
        recipients=Recipients.users(["charlie", "dave"])
    )
    sender.send_custom(notification)

    print("Check the receiver to see if notifications were received!")
