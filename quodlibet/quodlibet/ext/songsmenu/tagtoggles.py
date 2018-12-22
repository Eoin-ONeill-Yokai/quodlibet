from gi.repository import Gtk
from quodlibet import _
from quodlibet.plugins.songsmenu import SongsMenuPlugin
from quodlibet.qltk import Icons
from quodlibet.util import connect_obj

class TagToggle():
    def __init__(self, name = None, values = []):
        self.name = name
        self.tags = values # todo: Gather tags from library?

class TagTogglesMenu( SongsMenuPlugin ):
    """ Tag Toggling Plugin """

    PLUGIN_ID = 'TagToggles'
    PLUGIN_NAME = _('Tag Toggles')
    PLUGIN_DESC = _('Basic Tag Toggle Menu')
    PLUGIN_ICON = Icons.DOCUMENT_PROPERTIES

    DEFAULT_TOGGLES = [
        TagToggle("mood", ["Adventure","Airship","Ambient","Battle",
                            "Beautiful","Bright","Chill","Cool",
                            "Creepy","Cute","Dark","Dreamy","Dungeon",
                            "Ending","Energetic","Epic","Evil","Exotic",
                            "Fanfare","Forest","Funky","Funny","Happy",
                            "Intense","Love","Main Theme","March",
                            "Mysterious","Opening","Overworld","Somber",
                            "Spiritual","Stealth","Strange","Strategic",
                            "Town","Waltz"])
    ]

    toggles = None
    active_toggle = None
    active_songs = []

    def get_or_load_toggles(self):
        if not self.toggles:
            self.toggles = self.DEFAULT_TOGGLES
        return self.toggles

    def __set_active_toggle(self, toggle_tuple):
        self.active_toggle = toggle_tuple

    def __set_active_songs(self, songs):
        self.active_songs = []
        self.active_songs.extend(songs)

    def __set_active_song(self, song):
        self.active_songs = []
        self.active_songs.append(song)

    def __toggle_tag(self, tag_key, tag_value):
        if len(self.active_songs) == 0:
            print("ERR")
            return

        for song in self.active_songs:
            values = song(tag_key).split()
            if tag_value in values:
                values.remove(tag_value)
            else:
                values.append(tag_value)

            print(values)
            song[tag_key] = "\n".join(values)

    def __init__(self, *args, **kwargs):
        super(TagTogglesMenu, self).__init__(**kwargs)
        submenu = Gtk.Menu()
        print("init")
        toggles = self.get_or_load_toggles()
        for tog_index, toggle in enumerate(toggles):
            toggle_item = Gtk.MenuItem(toggle.name.capitalize())
            toggle_menu = Gtk.Menu()
            toggle_item.set_submenu(toggle_menu)
            for tag_index, tag in enumerate(toggle.tags):
                tag_item = Gtk.MenuItem("+ " + tag)
                toggle_menu.append(tag_item)
                connect_obj(tag_item, 'activate', self.__toggle_tag, toggle.name, tag)
            connect_obj(toggle_item, 'activate', self.__set_active_toggle, (toggle,toggle_menu))
            submenu.append(toggle_item)

        if submenu.get_children():
            self.set_submenu(submenu)
        else:
            self.set_sensitive(False)

    def plugin_single_song(self, song):
        self.__set_active_song(song)
        for tag in self.active_toggle[0].tags:
            if tag in song(self.active_toggle[0].name).split():
                for child in self.active_toggle[1].get_children():
                    if child.get_label() == "+ " + tag:
                        child.set_label("- " + tag)
