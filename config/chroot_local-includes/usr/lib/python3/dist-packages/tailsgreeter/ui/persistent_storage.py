import logging
import gi
import glob
import os
import sh
import threading
from typing import TYPE_CHECKING, Callable

from tailsgreeter.ui import _
from tailsgreeter.config import persistent_settings_dir
from tailsgreeter.errors import PersistentStorageError

gi.require_version('GLib', '2.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk

if TYPE_CHECKING:
    from tailsgreeter.settings.persistence import PersistentStorageSettings


class PersistentStorage(object):
    def __init__(self, persistence_setting: "PersistentStorageSettings",
                 load_settings_cb, apply_settings_cb: Callable, builder):
        self.persistence_setting = persistence_setting
        self.load_settings_cb = load_settings_cb
        self.apply_settings_cb = apply_settings_cb

        self.box_storage = builder.get_object('box_storage')
        self.box_storagecreate = builder.get_object('box_storagecreate')
        self.box_storage_unlock = builder.get_object('box_storage_unlock')
        self.box_storage_unlocked = builder.get_object('box_storage_unlocked')
        self.button_storage_unlock = builder.get_object('button_storage_unlock')  # type: Gtk.Button
        self.checkbutton_storage_show_passphrase = builder.get_object('checkbutton_storage_show_passphrase')
        self.entry_storage_passphrase = builder.get_object('entry_storage_passphrase')
        self.image_storage_state = builder.get_object('image_storage_state')
        self.infobar_persistence = builder.get_object('infobar_persistence')
        self.label_infobar_persistence = builder.get_object('label_infobar_persistence')
        self.spinner_storage_unlock = builder.get_object('spinner_storage_unlock')
        self.button_start = builder.get_object("button_start")

        self.checkbutton_storage_show_passphrase.connect(
            'toggled', self.cb_checkbutton_storage_show_passphrase_toggled)

        self.box_storage.set_focus_chain([
            self.box_storage_unlock,
            self.box_storage_unlocked,
            self.checkbutton_storage_show_passphrase])

        is_created = self.persistence_setting.is_created()
        self.box_storagecreate.set_visible(not is_created)
        self.box_storage.set_visible(is_created)

        if is_created:
            self.box_storage_unlock.set_visible(True)
            self.checkbutton_storage_show_passphrase.set_visible(True)
            self.image_storage_state.set_visible(True)
            self.entry_storage_passphrase.set_visible(True)
            self.spinner_storage_unlock.set_visible(False)

    @staticmethod
    def passphrase_changed(editable):
        # Remove warning icon
        editable.set_icon_from_icon_name(Gtk.EntryIconPosition.SECONDARY, None)

    def unlock(self):
        self.entry_storage_passphrase.set_sensitive(False)
        self.button_storage_unlock.set_sensitive(False)
        self.button_storage_unlock.set_label(_("Unlocking…"))
        self.checkbutton_storage_show_passphrase.set_visible(False)
        self.image_storage_state.set_visible(False)
        self.spinner_storage_unlock.set_visible(True)

        passphrase = self.entry_storage_passphrase.get_text()

        # Let's execute the unlocking in a thread
        def do_unlock_storage():
            try:
                if self.persistence_setting.unlock(passphrase):
                    GLib.idle_add(self.cb_unlocked)
                else:
                    GLib.idle_add(self.cb_unlock_failed_with_incorrect_passphrase)
            except PersistentStorageError as e:
                logging.error(e)
                GLib.idle_add(self.unlock_failed)
                return

        unlocking_thread = threading.Thread(target=do_unlock_storage)
        unlocking_thread.start()

    def cb_unlock_failed_with_incorrect_passphrase(self):
        logging.debug("Storage unlock failed")
        self.entry_storage_passphrase.set_sensitive(True)
        self.button_storage_unlock.set_sensitive(True)
        self.button_storage_unlock.set_label(_("Unlock"))
        self.checkbutton_storage_show_passphrase.set_visible(True)
        self.image_storage_state.set_visible(True)
        self.spinner_storage_unlock.set_visible(False)
        self.label_infobar_persistence.set_label(
                _("Cannot unlock encrypted storage with this passphrase."))
        self.infobar_persistence.set_visible(True)
        self.entry_storage_passphrase.select_region(0, -1)
        self.entry_storage_passphrase.set_icon_from_icon_name(
                Gtk.EntryIconPosition.SECONDARY,
                'dialog-warning-symbolic')
        self.entry_storage_passphrase.grab_focus()

    def unlock_failed(self):
        self.button_storage_unlock.set_label(_("Unlock"))
        self.image_storage_state.set_visible(True)
        self.spinner_storage_unlock.set_visible(False)
        self.label_infobar_persistence.set_label(
            _("Failed to unlock the Persistent Storage. "
              "Please start Tails and send an error report."))
        self.infobar_persistence.set_visible(True)
        self.button_start.set_sensitive(True)

    def activation_failed(self):
        self.button_storage_unlock.set_label(_("Unlock"))
        self.image_storage_state.set_visible(True)
        self.spinner_storage_unlock.set_visible(False)
        self.label_infobar_persistence.set_label(
            _("Failed to activate the Persistent Storage. "
              "Please start Tails and send an error report."))
        self.infobar_persistence.set_visible(True)
        self.button_start.set_sensitive(True)

    def cb_unlocked(self):
        logging.debug("Storage unlocked")

        # Activate the Persistent Storage
        try:
            self.persistence_setting.activate_persistent_storage()
        except PersistentStorageError as e:
            logging.error(e)
            self.activation_failed()
            return

        self.spinner_storage_unlock.set_visible(False)
        self.entry_storage_passphrase.set_visible(False)
        self.button_storage_unlock.set_visible(False)
        self.infobar_persistence.set_visible(False)
        self.image_storage_state.set_from_icon_name('tails-unlocked',
                                                    Gtk.IconSize.BUTTON)

        if not os.listdir(persistent_settings_dir):
            self.apply_settings_cb()
        else:
            self.load_settings_cb()

        # We're done unlocking and activating the Persistent Storage
        self.image_storage_state.set_visible(True)
        self.box_storage_unlocked.set_visible(True)
        self.button_start.set_sensitive(True)

    def cb_checkbutton_storage_show_passphrase_toggled(self, widget):
        self.entry_storage_passphrase.set_visibility(widget.get_active())
