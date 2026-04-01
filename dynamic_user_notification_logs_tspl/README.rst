Dynamic User Notification Logs
==============================

Overview
--------

``dynamic_user_notification_logs_tspl`` extends the Dynamic User Notification
module by storing notification activity in a dedicated log model. It allows
administrators to keep a history of which notification configuration was
triggered, which record caused it, who performed the action, which user was
notified, and what message was sent.

This module is designed for teams that need traceability and auditing for
real-time backend notifications.

Dependencies
------------

This module depends on:

- ``dynamic_user_notification_tspl``

The base notification module provides the configuration model, trigger engine,
and real-time notification delivery. This add-on builds on top of that logic to
store log records for matching notifications.

Features
--------

- Adds a dedicated notification log model.
- Creates logs for create notifications when enabled in the configuration.
- Creates logs for update notifications when enabled in the configuration.
- Creates logs for delete notifications when enabled in the configuration.
- Stores the triggering user, notified user, record reference, action type, and
  generated message.
- Adds a smart button on the notification configuration form to open related
  logs.
- Provides list, form, and search views for notification log analysis.

Configuration Enhancements
--------------------------

The module extends ``dynamic.user.notification.config`` with three additional
options:

- ``Create Logs on Create``
- ``Create Logs on Update``
- ``Create Logs on Delete``

These options are independent for each trigger type. A notification log is
created only when:

- the base notification rule matches the event
- the related log option is enabled for that trigger

How It Works
------------

When the base notification module processes a matching event:

- the inherited notification method calls the original notification logic first
- it receives the list of generated notifications
- it checks whether log creation is enabled for the current action type
- it creates one log record per notified user

Each log stores:

- notification configuration
- model technical name
- record id and reference
- action type: ``create``, ``write``, or ``unlink``
- triggering user
- notified user
- notification message

User Interface
--------------

- A smart button on the notification configuration form opens related logs.
- The log list view shows the action type, configuration, record, model,
  triggering user, notified user, and message.
- The search view supports filtering by action type and grouping by
  configuration, user, notified user, and model.

Technical Behavior
------------------

- The module inherits ``dynamic.user.notification.config`` and overrides
  ``_check_and_notify`` to append log creation after notifications are built.
- Logs are stored in ``dynamic.user.notification.logs``.
- The log model dynamically resolves record references from models that are
  present in the active notification configuration registry.
- Log creation uses ``sudo()`` when writing log records.

Installation
------------

1. Ensure ``dynamic_user_notification_tspl`` is available in your addons path.
2. Place this module in your custom addons path.
3. Restart the Odoo server.
4. Update the Apps list.
5. Install the module ``Dynamic User Notification Logs``.
6. Open an existing notification configuration and enable log creation options
   where needed.

Usage
-----

1. Open a notification configuration created through the base module.
2. Enable one or more log options for create, update, or delete events.
3. Confirm that the base notification rule is active and confirmed.
4. Perform the configured action on a matching record.
5. Open the ``Logs`` smart button on the configuration form.
6. Review the generated log entries in the list or form view.

Files
-----

- ``models/dynamic_user_notification_logs.py``: notification log model and
  stored log fields
- ``models/notification_config.py``: inherited configuration model, log options,
  smart button action, and log creation logic
- ``views/dynamic_user_notification_logs_views.xml``: list, form, search, and
  action definition for logs
- ``views/notification_config_views.xml``: inherited form view adding log
  options and smart button
- ``security/ir.model.access.csv``: access rights for notification logs

Version History
---------------

**18.0.1.0.0**

- Initial Odoo 18 release
- Added persistent logs for dynamic user notifications
- Added per-trigger log creation options on notification configurations
- Added log browsing from the configuration form
