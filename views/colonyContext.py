from views.guiContext import GUIContext, GUICode
from views.sidePanels.sideStatusPanel import SideStatusPanel
from views.timingView import TimingPanel

from views.sidePanels.colonyStatusPanels import (ColonyTabPanel, 
                                                 ColonyVehicleDetailPanel, 
                                                 ColonyShipDetailPanel, 
                                                 ColonyItemPanel, 
                                                 ColonyBuildingDetailPanel,
                                                 ColonyConstructionDetailPanel,
                                                 ColonyProductionPanel,
                                                 ColonyProductionDetailPanel)

from colonysim.colony import Colony

from orbitsim.orbitTrajectory import TrajectoryState

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
    def __init__(self, screen, model, manager, colony, launchContext = None):
        super().__init__(screen, model, manager)
        self.colony = colony

        self.colony_name_label = UILabel(pygame.Rect(400,200,100, 100), 
                                         text="Colony name placeholder", 
                                         manager=manager)
        summary_rect = pygame.Rect(800, 300, 400, 600)
        tab_rect = pygame.Rect(800, 200, 400, 100)
        timing_rect = pygame.Rect(800, 0, 400, 200)
        detail_rect = pygame.Rect(0, 500, 800, 300)

        self.settings_button =UIButton(relative_rect=pygame.Rect((0, 0), (100, 50)),
                                             text='Environ',
                                             manager=manager)
        
        self.tab_panel = ColonyTabPanel(tab_rect, manager=manager)
        self.timing_panel = TimingPanel(timing_rect, manager = manager, timingMaster=model.timingMaster)

        self.vehicle_panel = ColonyItemPanel(summary_rect, manager=manager, colony=colony, title="Vehicles", sourceList=self.colony.vehicles)
        self.vehicle_panel.hide()
        self.ship_panel = ColonyItemPanel(summary_rect, manager=manager, colony=colony, title="Ships", sourceList=self.colony.ships)
        self.ship_panel.hide()
        self.building_panel = ColonyItemPanel(summary_rect, manager=manager, colony=colony, title="Buildings", sourceList=self.colony.buildings)
        self.building_panel.hide()
        self.production_panel = ColonyProductionPanel(summary_rect, manager=manager, colony=colony, title="Production", sourceList=self.colony.productionOrders)
        self.production_panel.hide()
        self.construction_panel = ColonyItemPanel(summary_rect, manager=manager, colony=colony, title="Construction", sourceList=self.model.colonySim.buildingClassesForColony(colony.id))
        self.construction_panel.hide()

        self.vehicle_detail_panel = ColonyVehicleDetailPanel(detail_rect, manager=manager)
        self.vehicle_detail_panel.hide()
        self.ship_detail_panel = ColonyShipDetailPanel(detail_rect, manager=manager, orbitSim = self.model.orbitSim)
        self.ship_detail_panel.hide()
        self.building_detail_panel = ColonyBuildingDetailPanel(detail_rect, manager=manager, colony=self.colony)
        self.building_detail_panel.hide()
        self.construction_detail_panel = ColonyConstructionDetailPanel(detail_rect, manager=manager, colony=self.colony)
        self.construction_detail_panel.hide()
        self.production_detail_panel = ColonyProductionDetailPanel(detail_rect, 
                                                          manager=manager, 
                                                          colony=self.colony, 
                                                          title="Available Production", 
                                                          sourceList = self.model.colonySim._reactions)
        self.production_detail_panel.hide()

        self.active_panel = None
        self.detail_panel = None

        if launchContext:
            self.ship_detail_panel.setShip(launchContext["ship"])
            self.ship_detail_panel.update()
            self.detail_panel = self.ship_detail_panel
            self.detail_panel.show()

    def populateDetailPanel(self, key, sourceArray, panel, setter, comparator):
        vehicle = None
        for v in sourceArray:
            if comparator(v, key):
                vehicle=v

        assert(vehicle)
        if self.detail_panel:
            self.detail_panel.hide()

        setter(vehicle)
        panel.update()
        self.detail_panel = panel
        self.detail_panel.show()

    def run(self):
        returnCode = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                returnCode = QUIT
                break
            if event.type == UI_BUTTON_PRESSED:
                if event.ui_element == self.settings_button:
                    self.upperContext = {"planet": self.colony.locale.id}
                    returnCode = GUICode.LOADSURFACEVIEW
                    break
                if self.timing_panel.handle_event(event):
                    pass
                elif self.tab_panel.handle_event(event):
                    if self.active_panel:
                        self.active_panel.hide()
                    if self.detail_panel:
                        self.detail_panel.hide()

                    if self.tab_panel.upperEvent == 1:
                        self.active_panel = self.building_panel
                    elif self.tab_panel.upperEvent == 2:
                        self.active_panel = self.production_panel
                        self.detail_panel = self.production_detail_panel
                        self.detail_panel.update()
                        self.detail_panel.show()
                    elif self.tab_panel.upperEvent == 3:
                        self.active_panel = self.vehicle_panel
                    elif self.tab_panel.upperEvent == 4:
                        self.active_panel = self.ship_panel
                    elif self.tab_panel.upperEvent == 5:
                        self.active_panel = self.construction_panel

                    self.active_panel.update()
                    self.active_panel.show()
                    pass
                elif self.active_panel and self.active_panel.handle_event(event):
                    pass
                elif self.detail_panel and self.detail_panel.handle_event(event):
                    if self.detail_panel == self.vehicle_detail_panel:
                        self.colony.deployVehicle(self.vehicle_detail_panel.vehicle.id)
                        self.detail_panel = None
                        self.active_panel.update()
                    elif self.detail_panel == self.ship_detail_panel:
                        if event.ui_element == self.ship_detail_panel.target_button:
                            self.upperContext = {"ship": self.ship_detail_panel.ship, "colony": self.colony.id}
                            returnCode = GUICode.LOADORBITVIEW_LAUNCH_PLAN
                            break
                        elif event.ui_element == self.ship_detail_panel.launch_button:
                            self.ship_detail_panel.trajectory().state = TrajectoryState.PENDING



            elif event.type == UI_SELECTION_LIST_NEW_SELECTION:
                if event.ui_element == self.vehicle_panel.item_list:
                    self.populateDetailPanel(event.text, 
                                             self.colony.vehicles.values(), 
                                             self.vehicle_detail_panel, 
                                             self.vehicle_detail_panel.setVehicle,
                                             lambda item, key: item.name == key)
                elif event.ui_element == self.ship_panel.item_list:
                    self.populateDetailPanel(event.text, 
                                             self.colony.ships.values(),
                                             self.ship_detail_panel,
                                             self.ship_detail_panel.setShip,
                                             lambda item, key: item.name == key)
                elif event.ui_element == self.building_panel.item_list:
                    self.populateDetailPanel(int(event.text.split()[-1]),
                                             self.colony.buildings.values(), 
                                             self.building_detail_panel,
                                             self.building_detail_panel.setBuilding,
                                             lambda item, key: item.id == key)
                elif event.ui_element == self.construction_panel.item_list:
                    self.populateDetailPanel(event.text, 
                                             self.model.colonySim.buildingClassesForColony(self.colony.id).values(),
                                             self.construction_detail_panel,
                                             self.construction_detail_panel.setBuildingClass,
                                             lambda item, key: item.name == key)
                elif event.ui_element == self.production_panel.item_list:
                    po = None
                    (text, id) = self.production_panel.item_list.get_single_selection()
                    for order in self.colony.productionOrders.values():
                        if order.id == int(id):
                            po = order
                    assert(po)
                    self.production_panel.setProductionOrder(po)
                    self.production_panel.update()
                elif event.ui_element == self.production_detail_panel.item_list:
                    reaction = None
                    for r in self.model.colonySim._reactions.values():
                        if r.name == event.text:
                            reaction = r
                    assert(reaction)
                    self.production_detail_panel.setReaction(reaction)

            self.manager.process_events(event)

        self.colony_name_label.set_text(self.colony.name)

        self.screen.fill((250, 100, 50))

        self.timing_panel.update()
        if self.active_panel:
            self.active_panel.update()

        if self.detail_panel is self.ship_detail_panel:
            if self.detail_panel.ship and self.detail_panel.ship.id not in self.colony.ships:
                self.ship_detail_panel.setShip(None)

        if self.detail_panel:
            self.detail_panel.update()

        return returnCode
