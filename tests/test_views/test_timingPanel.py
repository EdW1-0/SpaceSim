import unittest
from unittest.mock import MagicMock

from views.timingPanel import TimingPanel

from tests.test_views.test_guiContext import isLocal

from timingMaster import TimingMaster

import pygame
import pygame_gui

class EventMock:
    pass


@unittest.skipUnless(isLocal(), "requires Windows")
class TestTimingPanel(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.manager = pygame_gui.UIManager((1200, 800))
        pygame.display.set_mode((1200, 800))
        self.tmMock = TimingMaster()
        self.tmMock.start = MagicMock()
        self.tmMock.step = MagicMock()
        self.tmMock.stop = MagicMock()

        self.tp = TimingPanel(pygame.Rect(800, 200, 400, 600), self.manager, self.tmMock)

    def testTimingPanelUnhandledEvent(self):
        event = EventMock()
        event.ui_element = "Not a button"
        self.assertFalse(self.tp.handle_event(event))


    def testTimingPanelStart(self):
        event = EventMock()
        event.ui_element = self.tp.start_button
        self.assertTrue(self.tp.handle_event(event))
        
        self.tmMock.start.assert_called_once()

    def testTimingPanelStep(self):
        event = EventMock()
        event.ui_element = self.tp.step_button
        self.assertTrue(self.tp.handle_event(event))
        
        self.tmMock.step.assert_called_once()

    def testTimingPanelStop(self):
        event = EventMock()
        event.ui_element = self.tp.stop_button
        self.assertTrue(self.tp.handle_event(event))
        
        self.tmMock.stop.assert_called_once()

    def testTimingPanelUpdate(self):
        self.tmMock.timestamp = 7
        self.tp.update()
        self.assertEqual(self.tp.time_label.text, str(7))

