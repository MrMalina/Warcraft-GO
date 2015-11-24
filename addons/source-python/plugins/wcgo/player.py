﻿"""Module for Wacraft: GO related player functionality."""

# Source.Python
from entities.helpers import index_from_edict
from filters.iterator import _IterObject
from players import PlayerGenerator
import players.entity


class PlayerIter(_IterObject):
    """Class for iterating over all WCGO players."""

    @staticmethod
    def iterator():
        """Iterate over all WCGO player objects."""
        for edict in PlayerGenerator():
            yield Player(index_from_edict(edict))


class Player(players.entity.Player):
    """Player class with WCGO functionality."""

    _registered = set()

    def __init__(self, index):
        """Initialize a new player."""
        super().__init__(index)
        if self.userid not in Player._registered:
            self.gold = 0
            self._hero = None
            self.heroes = {}
            Player._registered.add(self.userid)

    @property
    def hero(self):
        """Get the player's active hero."""
        return self._hero

    @hero.setter
    def hero(self, value):
        """Set the player's active hero."""
        if value.clsid not in self.heroes:
            raise ValueError(
                "Hero {0} not owned by {1}".format(value.clsid, self.steamid))
        if value != self.hero:
            if self.hero is not None:
                self.hero.items.clear()
            self.restrictions.clear()
            self._hero = value
