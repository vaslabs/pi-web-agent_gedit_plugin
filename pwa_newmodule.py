import os
import json
from gettext import gettext as _
from gi.repository import GObject, Gtk, Gedit, Gio


EXTENSION_PATH=os.environ['HOME']+'/.pi-web-agent-devel/pwa-extension/'
# Menu item example, insert a new item in the Tools menu
ui_str = """<ui>
  <menubar name="MenuBar">
    <menu name="FileMenu" action="File">
      <placeholder name="FileOps_2">
        <menuitem name="pwa-module" action="pwa-module"/>
        <menuitem name="pwa-extension" action="pwa-extension"/>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""
class ExamplePyWindowActivatable(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "ExamplePyWindowActivatable"

    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        # Insert menu items
        self._insert_menu()

    def do_deactivate(self):
        # Remove any installed menu items
        self._remove_menu()

        self._action_group = None

    def _insert_menu(self):
        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()

        # Create a new action group
        self._action_group = Gtk.ActionGroup("ExamplePyPluginActions")
        self._action_group.add_actions([("pwa-module", None, _("New pi-web-agent Extension Module"),
                                         None, _("New pi-web-agent Extension Module"),
                                         self.on_new_module)])

        self._action_group.add_actions([("pwa-extension", None, _("New pi-web-agent Extension Project"),
                                         None, _("New pi-web-agent Extension Project"),
                                         self.on_new_project)])

        
        
        # Insert the action group
        manager.insert_action_group(self._action_group, -1)

        # Merge the UI
        self._ui_id = manager.add_ui_from_string(ui_str)

    def _remove_menu(self):
        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()

        # Remove the ui
        manager.remove_ui(self._ui_id)

        # Remove the action group
        manager.remove_action_group(self._action_group)

        # Make sure the manager updates
        manager.ensure_update()

    def do_update_state(self):
        self._action_group.set_sensitive(self.window.get_active_document() != None)

    # Menu activate handlers
    def on_clear_document_activate(self, action):
        doc = self.window.get_active_document()
        if not doc:
            return

        doc.set_text('')
        
    def on_new_module(self, action):
        self.window.create_tab(True)
        doc = self.window.get_active_document();
        if not doc:
            return
        doc.set_text('#!/usr/bin/python')
        
    
        
    def on_new_project(self, action):
        self.promptForExtension()
        os.makedirs(EXTENSION_PATH + self.module)
        os.mkdir(EXTENSION_PATH + self.module + '/icons')
        os.mkdir(EXTENSION_PATH + self.module + '/configuration')
        os.mkdir(EXTENSION_PATH + self.module + '/main')
        os.mkdir(EXTENSION_PATH + self.module + '/scripts')
        os.mkdir(EXTENSION_PATH + self.module + '/javascript')
        config = self.getExtensionConfig()
        config_file = open(EXTENSION_PATH + self.module + '/configuration/config.json', 'w')
        json.dump(config, config_file, sort_keys=True, indent=4, separators=(',', ': '))
        python_file = EXTENSION_PATH + self.module + '/main/' + self.module + ".py"       
        self.window.create_tab_from_location(Gio.file_parse_name(python_file), None, 0, 0, True, True)
        
    def register_module(self, a, b):
        self.module = self.entry.get_text()
        Gtk.main_quit(a, b)
        
    def promptForExtension(self):
        prompt_window=Gtk.Window(title="Extension name?")
        self.entry=Gtk.Entry()
        prompt_window.add(self.entry)
        prompt_window.connect("delete-event", self.register_module)
        prompt_window.show_all()
        Gtk.main()
        
    def getExtensionConfig(self):
        return {'title':'Sample Extension', 'version':'Alpha', 'dependencies':[]}
