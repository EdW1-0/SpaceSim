from views.guiContext import GUIContext
from views.sidePanels.sideStatusPanel import SideStatusPanel
from views.timingView import TimingPanel

from views.sidePanels.colonyStatusPanels import ColonyTabPanel, ColonyVehiclePanel

from colonysim.colony import Colony

import pygame
from pygame_gui.elements import UILabel, UIButton
from pygame_gui  import (
    UI_BUTTON_PRESSED,
    UI_SELECTION_LIST_NEW_SELECTION,
    UI_BUTTON_ON_HOVERED
)

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    MOUSEBUTTONUP,
    QUIT,
)


class ColonyContext(GUIContext):
    def __init__(self, screen, model, manager, colony):
        super().__init__(screen, model, manager)
        self.colony = colony

        self.colony_name_label = UILabel(pygame.Rect(400,200,100, 100), 
                                         text="Colony name placeholder", 
                                         manager=manager)
        summary_rect = pygame.Rect(800, 300, 400, 600)
        tab_rect = pygame.Rect(800, 200, 400, 100)
        timing_rect = pygame.Rect(800, 0, 400, 200)
        
        self.tab_panel = ColonyTabPanel(tab_rect, manager=manager)
        self.timing_panel = TimingPanel(timing_rect, manager = manager, timingMaster=model.timingMaster)

        self.vehicle_panel = ColonyVehiclePanel(summary_rect, manager=manager, colony=colony)

        self.active_panel = None

    def run(self):
        returnCode = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                returnCode = QUIT
                break
            if event.type == UI_BUTTON_PRESSED:
                if self.timing_panel.handle_event(event):
                    pass
                elif self.tab_panel.handle_event(event):
                    if self.tab_panel.upperEvent == 3:
                        if self.active_panel:
                            self.active_panel.hide()
                        self.active_panel = self.vehicle_panel
                        self.vehicle_panel.update()
                        self.active_panel.show()
                    pass
                elif self.active_panel and self.active_panel.handle_event(event):
                    pass

            self.manager.process_events(event)

        self.colony_name_label.set_text(self.colony.name)

        self.screen.fill((250, 100, 50))

        self.timing_panel.update()

        return returnCode
