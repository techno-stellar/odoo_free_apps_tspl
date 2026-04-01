Dynamic User Notification
=========================

Overview
--------

``dynamic_user_notification_tspl`` adds a configurable notification engine for
Odoo backend users. Administrators can define notification rules per model and
send real-time user notifications when records are created, updated to selected
states, or deleted.

The module is designed for businesses that want configurable alerts without
writing custom code for every model-specific event.

Features
--------

- Create notification rules from the backend interface.
- Select the target model for each rule.
- Notify selected users on record creation.
- Notify selected users when a chosen state field changes to selected values.
- Notify selected users before record deletion.
- Choose notification type: ``success``, ``danger``, ``warning``, or ``info``.
- Mark notifications as sticky when they should remain visible until dismissed.
- Activate rules only after confirmation.

Access and Configuration
------------------------

Notification rules are stored in the model
``dynamic.user.notification.config`` and are available to internal users with
standard access rights.

Each configuration includes:

- configuration name
- related model
- users to notify
- notification type
- sticky behavior
- trigger options for create, update, and delete

Update notifications are controlled through a selected ``selection`` field and
one or more target states. A notification is sent only when that configured
field is included in the write values and the new value matches one of the
selected states.

How It Works
------------

When a configured model is affected:

- on ``create``, confirmed active rules with ``Notify on Creation`` enabled are
  evaluated
- on ``write``, confirmed active rules with ``Notify on State change`` enabled
  are evaluated
- on ``unlink``, confirmed active rules with ``Notify on Deletion`` enabled are
  evaluated before the record is removed
- matching rules send a real-time ``simple_notification`` event to each
  configured user

The notification message includes the model description, record display name,
the action or target state, and the user who triggered the event.

Technical Behavior
------------------

- The module extends the abstract ``base`` model to monitor ``create``,
  ``write``, and ``unlink`` across Odoo models.
- Models starting with ``ir.`` are excluded from notification processing.
- Configuration changes refresh an in-registry cache of active confirmed rules.
- The module uses context key ``skip_notification`` internally to avoid
  recursive notifications while configuration records are being managed.
- Notifications are delivered through ``bus.bus`` using the
  ``simple_notification`` channel.

Installation
------------

1. Place the module in your custom addons path.
2. Restart the Odoo server.
3. Update the Apps list.
4. Install the module ``Dynamic User Notification``.
5. Open ``Technical > Email > Notification Config``.
6. Create and confirm one or more notification rules.

Usage
-----

1. Open ``Technical > Email > Notification Config``.
2. Create a new notification configuration.
3. Select the model and users to notify.
4. Choose the notification type and sticky behavior.
5. Enable one or more triggers:
   ``On Create``, ``On Update``, or ``On Delete``.
6. For update notifications, choose the state field and target states.
7. Confirm the configuration.
8. Perform the configured action on records of the selected model.
9. The selected users receive real-time backend notifications.

Files
-----

- ``models/base.py``: hooks create, write, and unlink on the abstract base model
- ``models/notification_config.py``: configuration model, cache handling, and
  notification dispatch logic
- ``views/notification_config_views.xml``: list and form views for notification
  rules
- ``views/menus.xml``: technical menu entry for configuration access
- ``security/ir.model.access.csv``: access rights for notification
  configuration records

Version History
---------------

**18.0.1.0.0**

- Initial Odoo 18 release
- Added configurable user notifications by model
- Added create, state-based update, and delete triggers
- Added real-time backend notification dispatch through Odoo bus
