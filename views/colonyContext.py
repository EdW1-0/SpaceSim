from views.guiContext import GUIContext, GUICode

from views.panels import (
    ColonyTabPanel,
    ColonyVehicleDetailPanel,
    ColonyShipPanel,
    ColonyShipDetailPanel,
    ColonyShipLoadingPanel,
    ColonyShipConstructionPanel,
    ColonyItemPanel,
    ColonyBuildingDetailPanel,
    ColonyConstructionDetailPanel,
    ColonyProductionPanel,
    ColonyProductionDetailPanel,
    ColonyResourceDetailPanel,
    TimingPanel
)

from orbitsim import TrajectoryState

from colonysim import Colony
from gameModel import GameModel

import pygame
from pygame_gui.elements import UILabel, UIButton
from pygame_gui import (
    UI_BUTTON_PRESSED,
    UI_SELECTION_LIST_NEW_SELECTION,
)

from pygame.event import Event
from pygame.locals import (
    QUIT,
)

from views.routingModeInfo import RoutingModeInfo


class ColonyContext(GUIContext):
    def __init__(self, screen, model: GameModel, manager, colony: Colony, info: RoutingModeInfo=None):
        super().__init__(screen, model, manager)
        self.colony = colony

        self.colony_name_label = UILabel(
            pygame.Rect(400, 200, 100, 100),
            text="Colony name placeholder",
            manager=manager,
        )
        summary_rect = pygame.Rect(800, 300, 400, 600)
        tab_rect = pygame.Rect(800, 200, 400, 100)
        timing_rect = pygame.Rect(800, 0, 400, 200)
        detail_rect = pygame.Rect(0, 500, 800, 300)

        self.settings_button = UIButton(
            relative_rect=pygame.Rect((0, 0), (100, 50)),
            text="Environ",
            manager=manager,
        )
        self.tech_button = UIButton(
            relative_rect=pygame.Rect((100, 0), (100, 50)),
            text="Technology",
            manager=manager,
        )

        self.tab_panel = ColonyTabPanel(tab_rect, manager=manager)
        self.timing_panel = TimingPanel(
            timing_rect, manager=manager, timingMaster=model.timingMaster
        )

        self.vehicle_panel = ColonyShipPanel(
            summary_rect,
            manager=manager,
            colony=colony,
            title="Vehicles",
            sourceList=self.colony.vehicles,
        )
        self.vehicle_panel.hide()
        self.ship_panel = ColonyShipPanel(
            summary_rect,
            manager=manager,
            colony=colony,
            title="Ships",
            sourceList=self.colony.ships,
        )
        self.ship_panel.hide()
        self.building_panel = ColonyItemPanel(
            summary_rect,
            manager=manager,
            colony=colony,
            title="Buildings",
            sourceList=self.colony.buildings,
        )
        self.building_panel.hide()
        self.production_panel = ColonyProductionPanel(
            summary_rect,
            manager=manager,
            colony=colony,
            title="Production",
            sourceList=self.colony.productionOrders,
        )
        self.production_panel.hide()
        self.construction_panel = ColonyItemPanel(
            summary_rect,
            manager=manager,
            colony=colony,
            title="Construction",
            sourceList=self.model.colonySim.buildingClassesForColony(colony.id),
        )
        self.construction_panel.hide()
        self.resource_panel = ColonyItemPanel(
            summary_rect,
            manager=manager,
            colony=colony,
            title="Resources",
            sourceList=self.model.colonySim._resources,
        )
        self.resource_panel.hide()

        self.vehicle_detail_panel = ColonyVehicleDetailPanel(
            detail_rect, manager=manager
        )
        self.vehicle_detail_panel.hide()
        self.vehicle_loading_panel = ColonyShipLoadingPanel(
            detail_rect,
            manager=manager,
            colonySim=self.model.colonySim,
            colony=self.colony,
        )
        self.vehicle_loading_panel.hide()
        self.ship_detail_panel = ColonyShipDetailPanel(
            detail_rect, manager=manager, orbitSim=self.model.orbitSim
        )
        self.ship_detail_panel.hide()
        self.ship_loading_panel = ColonyShipLoadingPanel(
            detail_rect,
            manager=manager,
            colonySim=self.model.colonySim,
            colony=self.colony,
        )
        self.ship_construction_panel = ColonyShipConstructionPanel(
            detail_rect,
            manager=manager,
            orbitSim=self.model.orbitSim,
        )
        self.ship_construction_panel.hide()
        self.ship_loading_panel.hide()
        self.building_detail_panel = ColonyBuildingDetailPanel(
            detail_rect, manager=manager, colony=self.colony
        )
        self.building_detail_panel.hide()
        self.construction_detail_panel = ColonyConstructionDetailPanel(
            detail_rect, manager=manager, colony=self.colony
        )
        self.construction_detail_panel.hide()
        self.production_detail_panel = ColonyProductionDetailPanel(
            detail_rect,
            manager=manager,
            colony=self.colony,
            title="Available Production",
            sourceList=self.model.colonySim._reactions,
        )
        self.production_detail_panel.hide()
        self.resource_detail_panel = ColonyResourceDetailPanel(
            detail_rect, model=model, manager=manager, colony=self.colony
        )
        self.resource_detail_panel.hide()

        self.active_panel = None
        self.detail_panel = None

        self.info = info
        if self.info:
            self.ship_detail_panel.setShip(self.info.ship)
            self.ship_detail_panel.update()
            self.detail_panel = self.ship_detail_panel
            self.detail_panel.show()

    def populateDetailPanel(self, key, sourceArray, panel, setter, comparator):
        vehicle = None
        for v in sourceArray:
            if comparator(v, key):
                vehicle = v

        assert vehicle
        if self.detail_panel:
            self.detail_panel.hide()

        setter(vehicle)
        panel.update()
        self.detail_panel = panel
        self.detail_panel.show()

    def handleGuiButton(self, event: Event) -> GUICode:
        if event.ui_element == self.settings_button:
            self.upperContext = {"planet": self.colony.locale.id}
            return GUICode.LOADSURFACEVIEW
        elif event.ui_element == self.tech_button:
            return GUICode.LOADTECHVIEW
        if self.timing_panel.handle_event(event):
            return 0
        elif self.tab_panel.handle_event(event):
            return self.handleTabPanel(event)
        elif self.active_panel and self.active_panel.handle_event(event):
            return self.handleActivePanelButton(event)
        elif self.detail_panel and self.detail_panel.handle_event(event):
            return self.handleDetailPanelButton(event)                
        else:
            # Unhandled button click; needs to be explicitly returned as
            # this is usually a list item click, so returning None will
            # suppress its handling.
            return 0
        
    def handleTabPanel(self, event):
        if self.active_panel:
            self.active_panel.hide()
        if self.detail_panel:
            self.detail_panel.hide()

        if event.ui_element == self.tab_panel.buildings_button:
            self.active_panel = self.building_panel
        elif event.ui_element == self.tab_panel.production_button:
            self.active_panel = self.production_panel
            self.detail_panel = self.production_detail_panel
            self.detail_panel.update()
            self.detail_panel.show()
        elif event.ui_element == self.tab_panel.vehicles_button:
            self.active_panel = self.vehicle_panel
        elif event.ui_element == self.tab_panel.ships_button:
            self.active_panel = self.ship_panel
        elif event.ui_element == self.tab_panel.construction_button:
            self.active_panel = self.construction_panel
        elif event.ui_element == self.tab_panel.resource_button:
            self.active_panel = self.resource_panel

        self.active_panel.update()
        self.active_panel.show()
        return 0

    def handleActivePanelButton(self, event):
        if event.ui_element == self.active_panel.hide_button:
            return 0
        if self.active_panel == self.ship_panel:
            if self.detail_panel:
                self.detail_panel.hide()
            if self.active_panel.upperAction == 1:
                self.detail_panel = self.ship_detail_panel
            elif self.active_panel.upperAction == 2:
                self.detail_panel = self.ship_loading_panel
                self.ship_loading_panel.ship = self.ship_panel.ship
            elif self.active_panel.upperAction == 3:
                self.detail_panel = self.ship_construction_panel
            self.detail_panel.update()
            self.detail_panel.show()
        elif self.active_panel == self.vehicle_panel:
            if self.detail_panel:
                self.detail_panel.hide()
            if self.active_panel.upperAction == 1:
                self.detail_panel = self.vehicle_detail_panel
            elif self.active_panel.upperAction == 2:
                self.detail_panel = self.vehicle_loading_panel
                self.vehicle_loading_panel.ship = self.vehicle_panel.ship
            self.detail_panel.update()
            self.detail_panel.show()
        return 0
    
    def handleDetailPanelButton(self, event):
        if event.ui_element == self.detail_panel.hide_button:
            return 0
        if self.detail_panel == self.vehicle_detail_panel:
            self.colony.deployVehicle(self.vehicle_detail_panel.vehicle.id)
            self.detail_panel = None
            self.active_panel.update()
            return 0
        elif self.detail_panel == self.ship_detail_panel:
            if event.ui_element == self.ship_detail_panel.target_button:
                self.info = RoutingModeInfo()
                self.info.ship = self.ship_detail_panel.ship
                self.info.start = self.colony
                return GUICode.LOADORBITVIEW_LAUNCH_PLAN
            elif event.ui_element == self.ship_detail_panel.launch_button:
                self.ship_detail_panel.trajectory().state = (
                    TrajectoryState.PENDING
                )
                return 0

    def handleListSelection(self, event):
        if event.ui_element == self.vehicle_panel.item_list:
            self.populateDetailPanel(
                event.text,
                self.colony.vehicles.values(),
                self.vehicle_detail_panel,
                self.vehicle_detail_panel.setVehicle,
                lambda item, key: item.name == key,
            )
            vehicle = None
            for v in self.colony.vehicles.values():
                if v.name == event.text:
                    vehicle = v
            self.vehicle_panel.setSelectedShip(vehicle)
        elif event.ui_element == self.ship_panel.item_list:
            self.populateDetailPanel(
                event.text,
                self.colony.ships.values(),
                self.ship_detail_panel,
                self.ship_detail_panel.setShip,
                lambda item, key: item.name == key,
            )
            ship = None
            for s in self.colony.ships.values():
                if s.name == event.text:
                    ship = s
            self.ship_panel.setSelectedShip(ship)
        elif (
            event.ui_element == self.ship_loading_panel.item_list
            or event.ui_element == self.vehicle_loading_panel.item_list
        ):
            resource = None
            for r in self.model.colonySim._resources.values():
                if r.name == event.text:
                    resource = r
            self.detail_panel.setResource(resource)
            self.detail_panel.update()

        elif event.ui_element == self.building_panel.item_list:
            self.populateDetailPanel(
                int(event.text.split()[-1]),
                self.colony.buildings.values(),
                self.building_detail_panel,
                self.building_detail_panel.setBuilding,
                lambda item, key: item.id == key,
            )
        elif event.ui_element == self.construction_panel.item_list:
            self.populateDetailPanel(
                event.text,
                self.model.colonySim.buildingClassesForColony(
                    self.colony.id
                ).values(),
                self.construction_detail_panel,
                self.construction_detail_panel.setBuildingClass,
                lambda item, key: item.name == key,
            )
        elif event.ui_element == self.production_panel.item_list:
            po = None
            (text, id) = self.production_panel.item_list.get_single_selection()
            for order in self.colony.productionOrders.values():
                if order.id == int(id):
                    po = order
            assert po
            self.production_panel.setProductionOrder(po)
            self.production_panel.update()
        elif event.ui_element == self.production_detail_panel.item_list:
            reaction = None
            for r in self.model.colonySim._reactions.values():
                if r.name == event.text:
                    reaction = r
            assert reaction
            self.production_detail_panel.setReaction(reaction)
        elif event.ui_element == self.resource_panel.item_list:
            self.populateDetailPanel(
                event.text,
                self.model.colonySim._resources.values(),
                self.resource_detail_panel,
                self.resource_detail_panel.setResource,
                lambda item, key: item.name == key,
            )        

        return 0

    def updatePanels(self):
        self.timing_panel.update()
        if self.active_panel:
            self.active_panel.update()

        if self.detail_panel is self.ship_detail_panel:
            if (
                self.detail_panel.ship
                and self.detail_panel.ship.id not in self.colony.ships
            ):
                self.ship_detail_panel.setShip(None)

        if self.detail_panel:
            self.detail_panel.update()

    def run(self):
        returnCode = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                returnCode = QUIT
                break
            if event.type == UI_BUTTON_PRESSED:
                returnCode = self.handleGuiButton(event)
                if returnCode != 0:
                    break
            elif event.type == UI_SELECTION_LIST_NEW_SELECTION:
                self.handleListSelection(event)

            self.manager.process_events(event)

        self.colony_name_label.set_text(self.colony.name)

        self.screen.fill((250, 100, 50))
        self.updatePanels()

        return returnCode
