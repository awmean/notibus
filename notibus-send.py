import argparse
import sys

from notibus import NotibusSender


def main():
    parser = argparse.ArgumentParser(
        description="Notibus - Notification Sender",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Hello" "World"
  %(prog)s "Warning" "Low disk space" --urgency critical --icon dialog-warning
  %(prog)s "Admin Alert" "System maintenance" --admins-only
  %(prog)s "Team Msg" "Meeting at 3pm" --users alice,bob,charlie
  %(prog)s "Dev Alert" "Build failed" --groups developers,devops
        """
    )

    parser.add_argument('title', help='Notification title')
    parser.add_argument('body', help='Notification message body')
    parser.add_argument('--urgency', choices=['low', 'normal', 'critical'],
                        default='normal', help='Notification urgency level')
    parser.add_argument('--icon', default='dialog-information',
                        help='Icon name (freedesktop spec)')
    parser.add_argument('--timeout', type=int, default=5000,
                        help='Timeout in milliseconds (0 = no timeout)')

    # Recipient options (mutually exclusive)
    recipient_group = parser.add_mutually_exclusive_group()
    recipient_group.add_argument('--everyone', action='store_true',
                                 help='Send to everyone (default)')
    recipient_group.add_argument('--admins-only', action='store_true',
                                 help='Send to admin users only')
    recipient_group.add_argument('--users', type=str,
                                 help='Comma-separated list of users')
    recipient_group.add_argument('--groups', type=str,
                                 help='Comma-separated list of groups')

    args = parser.parse_args()

    # Create sender
    sender = NotibusSender()

    # Create notification based on arguments
    if args.admins_only:
        success = sender.send_to_admins(args.title, args.body, args.urgency,
                                        args.icon, args.timeout)
    elif args.users:
        user_list = [u.strip() for u in args.users.split(',')]
        success = sender.send_to_users(user_list, args.title, args.body,
                                       args.urgency, args.icon, args.timeout)
    elif args.groups:
        group_list = [g.strip() for g in args.groups.split(',')]
        success = sender.send_to_groups(group_list, args.title, args.body,
                                        args.urgency, args.icon, args.timeout)
    else:
        # Default: everyone
        success = sender.send_to_everyone(args.title, args.body, args.urgency,
                                          args.icon, args.timeout)

    sys.exit(0 if success else 1)


# Example usage as a library
if __name__ == "__main__":
    main()
