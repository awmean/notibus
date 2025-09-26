import argparse

from notibus import NotibusReceiver


def main():
    parser = argparse.ArgumentParser(description="Notibus - DBus Notification Receiver")
    parser.add_argument('--debug', action='store_true', help='Enable debug output')

    print("Notibus - Notification Receiver")
    print("=" * 50)

    receiver = NotibusReceiver()
    receiver.run()


if __name__ == "__main__":
    main()
