import pygame


from views.panels.sideStatusPanels import SideStatusPanel

from pygame_gui.elements import (
    UIButton,
    UILabel,
    UITextBox,
    UIHorizontalSlider,
    UISelectionList,
)

from views.widgets.selectionListId import SelectionListId
from colonysim import Building, ProductionOrder, ShipClass

from gameModel import GameModel


class ColonyTabPanel(SideStatusPanel):
    def __init__(self, rect, manager=None):
        super().__init__(rect, manager)
        self.buildings_button = UIButton(
            pygame.Rect(0, 0, 100, 50),
            text="Buildings",
            container=self.container,
            manager=manager,
        )

        self.production_button = UIButton(
            pygame.Rect(100, 0, 100, 50),
            text="Production",
            container=self.container,
            manager=manager,
        )

        self.vehicles_button = UIButton(
            pygame.Rect(200, 0, 100, 50),
            text="Vehicles",
            container=self.container,
            manager=manager,
        )

        self.ships_button = UIButton(
            pygame.Rect(300, 0, 100, 50),
            text="Ships",
            container=self.container,
            manager=manager,
        )

        self.construction_button = UIButton(
            pygame.Rect(0, 50, 100, 50),
            text="Construction",
            container=self.container,
            manager=manager,
        )

        self.resource_button = UIButton(
            pygame.Rect(100, 50, 100, 50),
            text="Resources",
            container=self.container,
            manager=manager,
        )

    def handle_event(self, event):
        self.upperEvent = 0
        if super().handle_event(event):
            return True
        elif event.ui_element == self.buildings_button:
            return True
        elif event.ui_element == self.production_button:
            return True
        elif event.ui_element == self.vehicles_button:
            return True
        elif event.ui_element == self.ships_button:
            return True
        elif event.ui_element == self.construction_button:
            return True
        elif event.ui_element == self.resource_button:
            return True
        else:
            return False


class ColonyItemPanel(SideStatusPanel):
    def __init__(
        self,
        rect,
        manager=None,
        colony=None,
        title="Default title",
        sourceList=None,
        itemRect=None,
    ):
        super().__init__(rect, manager)
        self.colony = colony
        self.sourceList = sourceList
        self.item_hash = ""
        self.manager = manager
        if not itemRect:
            self.itemRect = pygame.Rect(0, 100, 400, 500)
        else:
            self.itemRect = itemRect

        self.title_text = UILabel(
            pygame.Rect(0, 50, 400, 50),
            text=title,
            manager=manager,
            container=self.container,
        )

        self.item_list = SelectionListId(
            self.itemRect, [], manager=manager, container=self.container
        )

    def update(self):
        newHash = "".join(map(str, [item.id for item in self.sourceList.values()]))
        if newHash != self.item_hash:
            if len(self.sourceList) == 0:
                self.item_list.set_item_list([])
            elif isinstance(next(iter(self.sourceList.values())), Building):
                self.item_list.set_item_list(
                    [
                        (item.buildingClass.name + " " + str(item.id))
                        for item in self.sourceList.values()
                    ]
                )
            elif isinstance(next(iter(self.sourceList.values())), ProductionOrder):
                self.item_list.set_item_list(
                    [
                        (item.reaction.name + " " + str(item.amount), str(item.id))
                        for item in self.sourceList.values()
                    ]
                )
            else:
                self.item_list.set_item_list(
                    [item.name for item in self.sourceList.values()]
                )
            self.item_list.show()
            self.item_hash = newHash


class ColonyVehicleDetailPanel(SideStatusPanel):
    def __init__(self, rect, manager=None, vehicle=None):
        super().__init__(rect, manager)
        self.vehicle = vehicle

        self.vehicle_name = UILabel(
            pygame.Rect(200, 50, 200, 50),
            text="Default name",
            manager=manager,
            container=self.container,
        )

        self.vehicle_characteristics = UITextBox(
            "Characteristics",
            pygame.Rect(0, 100, 200, 100),
            manager=manager,
            container=self.container,
        )
        self.vehicle_status = UITextBox(
            "Status",
            pygame.Rect(200, 100, 200, 100),
            manager=manager,
            container=self.container,
        )
        self.vehicle_mission = UITextBox(
            "Mission",
            pygame.Rect(400, 100, 200, 100),
            manager=manager,
            container=self.container,
        )
        self.target_button = UIButton(
            pygame.Rect(600, 100, 100, 50),
            "Set Target",
            manager=manager,
            container=self.container,
        )
        self.embark_button = UIButton(
            pygame.Rect(600, 150, 100, 50),
            "Embark",
            manager=manager,
            container=self.container,
        )

    def setVehicle(self, vehicle):
        self.vehicle = vehicle

    def update(self):
        if not self.vehicle:
            return

        self.vehicle_name.set_text(self.vehicle.name)

        self.vehicle_characteristics.set_text(
            "Class: {0}<br>Velocity: {1}<br>Fuel per m: {2}".format(
                self.vehicle.vehicleClass.name,
                self.vehicle.maxV(),
                self.vehicle.fuelPerM(),
            )
        )
        self.vehicle_status.set_text(
            "Fuel: {0}/{1}<br>".format(
                self.vehicle.fuel, self.vehicle.vehicleClass.maxFuel
            )
        )
        self.vehicle_mission.set_text("Orders: Not implemented<br>")

    def handle_event(self, event):
        if super().handle_event(event):
            return True
        elif event.ui_element == self.embark_button:
            self.hide()
            return True
        else:
            return False


class ColonyShipPanel(ColonyItemPanel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, itemRect=pygame.Rect(0, 100, 400, 200))
        self.target_button = UIButton(
            pygame.Rect(0, 300, 100, 50),
            "Trajectory",
            manager=self.manager,
            container=self.container,
        )
        self.loading_button = UIButton(
            pygame.Rect(100, 300, 100, 50),
            "Payload",
            manager=self.manager,
            container=self.container,
        )
        self.construction_button = UIButton(
            pygame.Rect(200, 300, 100, 50),
            "Construction",
            manager=self.manager,
            container=self.container,
        )
        self.ship = None

    def setSelectedShip(self, ship):
        self.ship = ship

    def handle_event(self, event):
        self.upperAction = 0
        if super().handle_event(event):
            return True
        elif event.ui_element == self.target_button:
            self.upperAction = 1
            return True
        elif event.ui_element == self.loading_button:
            self.upperAction = 2
            return True
        elif event.ui_element == self.construction_button:
            self.upperAction = 3
            return True
        else:
            return False

    def update(self):
        super().update()
        if not self.ship:
            self.target_button.hide()
            self.loading_button.hide()
        else:
            self.target_button.show()
            self.loading_button.show()


# TODO: ColonyVehicleDetailPanel and ColonyShipDetailPanel are almost identical.
# Probably should merge into common superclass
class ColonyShipDetailPanel(SideStatusPanel):
    def __init__(self, rect, manager=None, orbitSim=None, ship=None):
        super().__init__(rect, manager)
        self.ship = ship
        self.orbitSim = orbitSim

        self.ship_name = UILabel(
            pygame.Rect(200, 50, 200, 50),
            text="Default name",
            manager=manager,
            container=self.container,
        )

        self.ship_characteristics = UITextBox(
            "Characteristics",
            pygame.Rect(0, 100, 200, 100),
            manager=manager,
            container=self.container,
        )
        self.ship_status = UITextBox(
            "Status",
            pygame.Rect(200, 100, 200, 100),
            manager=manager,
            container=self.container,
        )
        self.ship_mission = UITextBox(
            "Mission",
            pygame.Rect(400, 100, 200, 100),
            manager=manager,
            container=self.container,
        )
        self.target_button = UIButton(
            pygame.Rect(600, 100, 100, 50),
            "Set Target",
            manager=manager,
            container=self.container,
        )
        self.launch_button = UIButton(
            pygame.Rect(600, 150, 100, 50),
            "Launch",
            manager=manager,
            container=self.container,
        )
        self.launch_button.hide()

    def setShip(self, ship):
        self.ship = ship

    def update(self):
        if not self.ship:
            self.hide()
            return

        self.ship_name.set_text(self.ship.name)

        self.ship_characteristics.set_text(
            "Class: {0}<br>".format(self.ship.shipClass.name)
        )
        self.ship_status.set_text(
            "DeltaV: {0}/{1}<br>".format(
                self.ship.deltaV(), self.ship.shipClass.maxDeltaV
            )
        )

        trajectory = self.trajectory()
        if trajectory:
            self.ship_mission.set_text(trajectory.strRep(self.orbitSim))
            self.launch_button.show()
        else:
            self.ship_mission.set_text("Orders: Not implemented<br>")
            self.launch_button.hide()

    def trajectory(self):
        if not self.ship:
            return None

        particle = None
        for p in self.orbitSim._particles.values():
            if p.payload == self.ship:
                particle = p

        trajectory = None
        if particle:
            try:
                trajectory = self.orbitSim.trajectoryForParticle(particle.id)
            except KeyError:
                pass

        return trajectory

    def handle_event(self, event):
        self.upperAction = 0
        if super(ColonyShipDetailPanel, self).handle_event(event):
            return True
        elif event.ui_element == self.target_button:
            self.upperAction = 1
            return True
        elif event.ui_element == self.launch_button:
            self.upperAction = 2
            return True
        else:
            return False
        
class ColonyShipConstructionPanel(SideStatusPanel):
    def __init__(self, rect, manager=None, model: GameModel=None, colony=None):
        super().__init__(rect, manager)
        self.model = model
        self.colony = colony  
        self.shipClass: ShipClass = None
        self.item_hash = ""


        self.title = UILabel(
        pygame.Rect(200, 0, 200, 50),
        text="Ship construction",
        manager=manager,
        container=self.container,
        )

        self.shipClass_name = UILabel(
            pygame.Rect(200, 50, 200, 50),
            text="Default ship",
            manager=manager,
            container=self.container,
        )

        self.construction_list = UISelectionList(
            pygame.Rect(0, 100, 400, 100),
            [("foo", "bar")],
            manager=manager,
            container=self.container,
        )

        self.construction_text = UITextBox(
            "Placeholder",
            pygame.Rect(400, 100, 100, 100),
            manager=manager,
            container=self.container,
        )

        self.function_text = UITextBox(
            "Condition",
            pygame.Rect(500, 100, 100, 100),
            manager=manager,
            container=self.container,
        )

        self.construct_button = UIButton(
            pygame.Rect(600, 100, 100, 50),
            "Construct",
            manager=manager,
            container=self.container,
        )
    
    def setShipClassId(self, id):
        self.shipClass = self.model.orbitSim.shipClassById(id)
    
    def update(self):
        if self.colony:
            sourceList = self.model.colonySim.shipClassesForColony(self.colony)
            newHash = "".join(map(str, [item for item in sourceList]))
            if newHash != self.item_hash:
                if len(sourceList) == 0:
                    self.construction_list.set_item_list([])
                else:
                    self.construction_list.set_item_list(sourceList)

                self.construction_list.show()
                self.item_hash = newHash

        if self.shipClass:
            self.shipClass_name.set_text(self.shipClass.name)

    def handle_event(self, event):
        self.upperAction = 0
        if super(ColonyShipConstructionPanel, self).handle_event(event):
            return True
        else:
            return False


# TODO: Overengineering for now. Eventually this will prune the full list of
# resources existing in the game down to just those
# actually stored either in the colony or ship.
class ResourceUnion:
    def __init__(self, ship, colony):
        self.ship = ship
        self.colony = colony

    def values(self):
        unionMap = {}
        for k in self.ship.cargo.keys():
            unionMap[k] = 0
        # for k in self.


class ColonyShipLoadingPanel(ColonyItemPanel):
    def __init__(self, rect, manager=None, colonySim=None, colony=None):
        super().__init__(
            rect,
            manager,
            colony,
            title="Cargo Loading",
            sourceList=colonySim._resources,
        )

        self.ship = None
        self.resource = None

        self.resource_label = UILabel(
            pygame.Rect(500, 50, 200, 50),
            text="Default resource",
            manager=manager,
            container=self.container,
        )
        self.colony_cap = UILabel(
            pygame.Rect(450, 100, 50, 50),
            text="Colcap",
            manager=manager,
            container=self.container,
        )
        self.colony_amount = UILabel(
            pygame.Rect(400, 100, 50, 50),
            text="Colamt",
            manager=manager,
            container=self.container,
        )

        self.amount_slider = UIHorizontalSlider(
            pygame.Rect(460, 150, 300, 50),
            0,
            (-100, 100),
            manager=self.manager,
            container=self.container,
        )
        self.amount_tally = UILabel(
            pygame.Rect(600, 100, 50, 50),
            text="0",
            manager=manager,
            container=self.container,
        )

        self.ship_amount = UILabel(
            pygame.Rect(700, 100, 50, 50),
            text="Shipamt",
            manager=manager,
            container=self.container,
        )
        self.ship_cap = UILabel(
            pygame.Rect(750, 100, 50, 50),
            text="Shipcap",
            manager=manager,
            container=self.container,
        )
        self.confirm_button = UIButton(
            pygame.Rect(700, 200, 100, 50),
            "Confirm",
            manager=manager,
            container=self.container,
        )

    def setShip(self, ship):
        self.ship = ship

    def setResource(self, resource):
        self.resource = resource

    def getBid(self):
        col_amt = self.colony.reportResources(self.resource.id)
        if self.resource.id in self.ship.cargo:
            ship_amt = self.ship.cargo[self.resource.id]
        else:
            ship_amt = 0

        sliderpos = self.amount_slider.get_current_value()
        if sliderpos < 0:
            amount = ship_amt * sliderpos / 100
        elif sliderpos > 0:
            amount = col_amt * sliderpos / 100
        else:
            amount = 0

        return amount

    def update(self):
        super().update()
        if self.resource:
            col_amt = self.colony.reportResources(self.resource.id)
            if self.resource.id in self.ship.cargo:
                ship_amt = self.ship.cargo[self.resource.id]
            else:
                ship_amt = 0
            col_cap = self.colony.reportCapacity(self.resource.id)
            ship_cap = "Inf"

            self.resource_label.set_text(self.resource.name)
            self.colony_amount.set_text(str(col_amt))
            self.colony_cap.set_text(str(col_cap))
            self.ship_amount.set_text(str(ship_amt))
            self.ship_cap.set_text(str(ship_cap))

            self.amount_tally.set_text(str(self.getBid()))

        else:
            self.resource_label.set_text("No resource")
            self.colony_amount.set_text("0")
            self.colony_cap.set_text("0")
            self.ship_amount.set_text("0")
            self.ship_cap.set_text("0")

    def handle_event(self, event):
        if super(ColonyShipLoadingPanel, self).handle_event(event):
            return True
        elif event.ui_element == self.confirm_button:
            bid = self.getBid()
            if bid > 0:
                # TODO: Should probably make this a utility method - "transferResource".
                # Should also probably add some consistency
                # between how colonies and ships describe resources - dict or not?
                excess = self.ship.addCargo(
                    {self.resource.id: self.colony.getResources(self.resource.id, bid)}
                )
                self.colony.storeResources(self.resource.id, excess[self.resource.id])
            elif bid < 0:
                excess = self.colony.storeResources(
                    self.resource.id,
                    self.ship.removeCargo({self.resource.id: -bid})[self.resource.id],
                )
                self.ship.addCargo({self.resource.id: excess})

            return True
        else:
            return False


class ColonyBuildingDetailPanel(SideStatusPanel):
    def __init__(self, rect, manager=None, colony=None, building=None):
        super().__init__(rect, manager)
        self.colony = colony
        self.building = building

        self.building_name = UILabel(
            pygame.Rect(200, 50, 200, 50),
            text="Default building",
            manager=manager,
            container=self.container,
        )
        self.status_text = UITextBox(
            "Placeholder",
            pygame.Rect(0, 100, 100, 100),
            manager=manager,
            container=self.container,
        )

        self.condition_text = UITextBox(
            "Condition",
            pygame.Rect(100, 100, 100, 100),
            manager=manager,
            container=self.container,
        )

        self.class_specific_text = UITextBox(
            "Specific",
            pygame.Rect(500, 100, 100, 100),
            manager=manager,
            container=self.container,
        )
        self.toggle_button = UIButton(
            pygame.Rect(600, 100, 100, 50),
            "Toggle",
            manager=manager,
            container=self.container,
        )
        self.demolish_button = UIButton(
            pygame.Rect(600, 150, 100, 50),
            "Demolish",
            manager=manager,
            container=self.container,
        )

    def setBuilding(self, building):
        self.building = building

    def handle_event(self, event):
        if super(ColonyBuildingDetailPanel, self).handle_event(event):
            return True
        elif event.ui_element == self.toggle_button:
            if self.building.running():
                self.building.stop()
            elif self.building.idle():
                self.building.start()
            return True
        elif event.ui_element == self.demolish_button:
            self.building.demolish()
            return True
        else:
            return False

    def update(self):
        if not self.building:
            self.hide()
            return

        self.building_name.set_text(
            self.building.buildingClass.name + str(self.building.id)
        )
        if self.building.demolishing():
            status = "{0}<br>{1}".format(
                str(self.building.status), self.building.demolitionProgress
            )
        else:
            status = "{0}".format(str(self.building.status))
        self.status_text.set_text(status)

        self.condition_text.set_text("Condition: " + str(self.building.condition) + "%")
        self.class_specific_text.set_text(self.building.summaryString())


class ColonyConstructionDetailPanel(SideStatusPanel):
    def __init__(self, rect, manager=None, colony=None, buildingClass=None):
        super().__init__(rect, manager)
        self.colony = colony
        self.buildingClass = buildingClass
        self.buildingClass_name = UILabel(
            pygame.Rect(200, 50, 200, 50),
            text="Default building",
            manager=manager,
            container=self.container,
        )

        self.construction_list = UISelectionList(
            pygame.Rect(0, 100, 400, 100),
            [("foo", "bar")],
            manager=manager,
            container=self.container,
        )

        self.construction_text = UITextBox(
            "Placeholder",
            pygame.Rect(400, 100, 100, 100),
            manager=manager,
            container=self.container,
        )

        self.function_text = UITextBox(
            "Condition",
            pygame.Rect(500, 100, 100, 100),
            manager=manager,
            container=self.container,
        )

        self.construct_button = UIButton(
            pygame.Rect(600, 100, 100, 50),
            "Construct",
            manager=manager,
            container=self.container,
        )

    def setBuildingClass(self, buildingClass):
        self.buildingClass = buildingClass

    def handle_event(self, event):
        if super(ColonyConstructionDetailPanel, self).handle_event(event):
            return True
        elif event.ui_element == self.construct_button:
            if self.buildingClass:
                self.colony.addBuilding(self.buildingClass)
            return True
        else:
            return False

    def update(self):
        if not self.buildingClass:
            self.hide()
            return

        self.buildingClass_name.set_text(self.buildingClass.name)
        self.construction_text.set_text(
            "Time: {0}<br>Cost: {1}".format(
                self.buildingClass.constructionTime(), self.buildingClass.constructionCost
            )
        )
        self.function_text.set_text("Stuff here")


class ColonyProductionDetailPanel(ColonyItemPanel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reaction = None

        self.queue_button = UIButton(
            pygame.Rect(500, 200, 200, 50),
            "Queue Order",
            manager=self.manager,
            container=self.container,
        )
        self.amount_slider = UIHorizontalSlider(
            pygame.Rect(500, 100, 200, 50),
            0,
            (0, 100),
            manager=self.manager,
            container=self.container,
        )
        self.amount_text = UILabel(
            pygame.Rect(500, 250, 200, 50),
            text="-1",
            manager=self.manager,
            container=self.container,
        )

        self.reaction_text = UILabel(
            pygame.Rect(500, 50, 200, 50),
            text="Should be overwritten",
            manager=self.manager,
            container=self.container,
        )

    def setReaction(self, reaction):
        self.reaction = reaction

    def update(self):
        super().update()
        amount = self.amount_slider.get_current_value()
        self.amount_text.set_text(str(amount))

        if self.reaction:
            self.reaction_text.set_text(self.reaction.name)
        else:
            self.reaction_text.set_text("No selection")

    def handle_event(self, event):
        if super(ColonyProductionDetailPanel, self).handle_event(event):
            return True
        elif event.ui_element == self.queue_button:
            if self.reaction:
                self.colony.addProductionOrder(
                    self.reaction, self.amount_slider.get_current_value()
                )
            return True
        else:
            return False


class ColonyProductionPanel(ColonyItemPanel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, itemRect=pygame.Rect(0, 100, 400, 200))
        self.productionOrder = None
        self.status_text = UILabel(
            pygame.Rect(0, 400, 100, 50),
            text="Status placeholder",
            manager=self.manager,
            container=self.container,
        )

        self.name_text = UILabel(
            pygame.Rect(50, 350, 200, 50),
            text="name placeholder",
            manager=self.manager,
            container=self.container,
        )
        self.progress_text = UILabel(
            pygame.Rect(100, 400, 100, 50),
            text="progress placeholder",
            manager=self.manager,
            container=self.container,
        )

        self.pause_button = UIButton(
            pygame.Rect(50, 450, 100, 50),
            "Pause",
            manager=self.manager,
            container=self.container,
        )
        self.resume_button = UIButton(
            pygame.Rect(150, 450, 100, 50),
            "Resume",
            manager=self.manager,
            container=self.container,
        )
        self.cancel_button = UIButton(
            pygame.Rect(250, 450, 100, 50),
            "Cancel",
            manager=self.manager,
            container=self.container,
        )

    def setProductionOrder(self, po):
        self.productionOrder = po

    def handle_event(self, event):
        if super(ColonyProductionPanel, self).handle_event(event):
            return True
        elif event.ui_element == self.resume_button:
            self.colony.startProductionOrder(self.productionOrder.id)
            return True
        elif event.ui_element == self.pause_button:
            self.colony.pauseProductionOrder(self.productionOrder.id)
            return True
        elif event.ui_element == self.cancel_button:
            self.colony.cancelProductionOrder(self.productionOrder.id)
            self.setProductionOrder(None)
            return True
        else:
            return False

    def update(self):
        super().update()
        if self.productionOrder:
            self.status_text.set_text(self.productionOrder.status.name)
            self.name_text.set_text(self.productionOrder.reaction.name)
            self.progress_text.set_text(
                "{0}/{1}".format(
                    self.productionOrder.remaining, self.productionOrder.amount
                )
            )
            self.pause_button.show()
            self.resume_button.show()
            self.cancel_button.show()

        else:
            self.name_text.set_text("No order selected")
            self.status_text.set_text("")
            self.pause_button.hide()
            self.resume_button.hide()
            self.cancel_button.hide()


class ColonyResourcePanel(ColonyItemPanel):
    pass


class ColonyResourceDetailPanel(SideStatusPanel):
    def __init__(self, rect, model, manager=None, colony=None):
        super().__init__(rect, manager)
        self.colony = colony
        self.model = model

        self.name_text = UILabel(
            pygame.Rect(300, 50, 200, 50),
            text="name placeholder",
            manager=manager,
            container=self.container,
        )
        self.properties_text = UILabel(
            pygame.Rect(50, 100, 200, 50),
            text="prop placeholder",
            manager=manager,
            container=self.container,
        )
        self.reactions_text = UILabel(
            pygame.Rect(50, 150, 200, 50),
            text="react placeholder",
            manager=manager,
            container=self.container,
        )

        self.amount_text = UILabel(
            pygame.Rect(350, 100, 200, 50),
            text="amnt placeholder",
            manager=manager,
            container=self.container,
        )
        self.capacity_text = UILabel(
            pygame.Rect(350, 150, 200, 50),
            text="cap placeholder",
            manager=manager,
            container=self.container,
        )
        self.projection_text = UILabel(
            pygame.Rect(350, 200, 200, 50),
            text="proj placeholder",
            manager=manager,
            container=self.container,
        )

    def setResource(self, resource):
        self.resource = resource

    def update(self):
        if self.resource:
            self.name_text.set_text(self.resource.name)
            self.properties_text.set_text(
                "Base value: {0}, units:{1}".format(
                    self.resource.baseValue, self.resource.units
                )
            )
            self.reactions_text.set_text("Reactions go here")

            self.amount_text.set_text(
                "Amount: {0} {1}".format(
                    self.colony.reportResources(self.resource.id), self.resource.units
                )
            )
            self.capacity_text.set_text(
                "Capacity: {0} {1}".format(
                    self.colony.reportCapacity(self.resource.id), self.resource.units
                )
            )
            self.projection_text.set_text("Projection will go here")
        else:
            self.name_text.set_text("No resource selected")
            self.properties_text.set_text("")
            self.reactions_text.set_text("")
            self.amount_text.set_text("")
            self.capacity_text.set_text("")
            self.projection_text.set_text("")
