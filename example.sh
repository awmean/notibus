#!/bin/bash

# Notibus D-Bus notification examples using bash
# These commands send signals that match your Python receiver's expected format

# Send to everyone
dbus-send --system --type=signal \
    /com/notibus/Notification \
    com.notibus.Notification.Notification \
    string:"Test" \
    string:"Hello World" \
    string:"normal" \
    string:"dialog-information" \
    int32:5000 \
    string:'{"type":"everyone","list":[]}'

# Send to admins only
dbus-send --system --type=signal \
    /com/notibus/Notification \
    com.notibus.Notification.Notification \
    string:"Admin Alert" \
    string:"System maintenance required" \
    string:"critical" \
    string:"security-high" \
    int32:8000 \
    string:'{"type":"admins_only","list":[]}'

# Send to specific users
dbus-send --system --type=signal \
    /com/notibus/Notification \
    com.notibus.Notification.Notification \
    string:"Meeting" \
    string:"Conference room A at 2pm" \
    string:"normal" \
    string:"dialog-information" \
    int32:5000 \
    string:'{"type":"users","list":["alice","bob"]}'

# Send to specific groups
dbus-send --system --type=signal \
    /com/notibus/Notification \
    com.notibus.Notification.Notification \
    string:"Build Status" \
    string:"CI pipeline completed" \
    string:"normal" \
    string:"dialog-information" \
    int32:5000 \
    string:'{"type":"groups","list":["developers"]}'