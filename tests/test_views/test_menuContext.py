from views.menuContext import MenuContext
from views.guiContext import GUIContext

import unittest
from unittest.mock import MagicMock
from tests.test_views.test_guiContext import ScreenMock, ModelMock, isLocal

import pygame

@unittest.skipUnless(isLocal(), "requires Windows")
class TestMenuContext(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.sm = ScreenMock()
        self.sm.fill = MagicMock()
        self.sm.blit = MagicMock()

    def testMenuContext(self):
        self.assertTrue(MenuContext)

    def testMenuContextConstructor(self):
        mc = MenuContext(ScreenMock(), ModelMock(), None)
        self.assertTrue(mc)
        self.assertTrue(issubclass(MenuContext, GUIContext))
        self.assertTrue(isinstance(mc, GUIContext))

    def testMenuContextRun(self):
        mc = MenuContext(self.sm, ModelMock(), None)
        mc.run()
        mc.screen.fill.assert_called()
        mc.screen.blit.assert_called()
