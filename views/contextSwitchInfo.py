from dataclasses import dataclass
from guiContext import GUIContext

from colonysim.colony import Colony
from colonysim.ship import Ship


@dataclass
class ContextSwitchInfo:
    next: GUIContext
    mode: str
    ship: Ship
    colony: Colony