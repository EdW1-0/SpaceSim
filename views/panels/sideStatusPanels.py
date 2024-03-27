import pygame

from pygame_gui.elements import UIButton, UIImage, UILabel
from pygame_gui.core import UIContainer

from views.widgets.selectionListId import SelectionListId

from colonysim import Building, ProductionOrder


class SideStatusPanel:
    def __init__(self, rect, manager=None):
        self.rect = rect
        self.container = UIContainer(rect, manager=manager)
        background = pygame.Surface((rect.width, rect.height))
        pygame.draw.rect(background, (10, 10, 10), (0, 0, rect.width, rect.height))
        self.background = UIImage(
            (0, 0, rect.width, rect.height),
            background,
            manager=manager,
            container=self.container,
        )

        self.hide_button = UIButton(
            relative_rect=pygame.Rect((0, 0), (20, 20)),
            text="X",
            container=self.container,
            manager=manager,
        )

    def hide(self):
        self.container.hide()

    def show(self):
        self.container.show()

    def handle_event(self, event):
        if event.ui_element == self.hide_button:
            print("Boop!")
            self.hide()
            return True
        else:
            return False


class ItemListPanel(SideStatusPanel):
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
        if isinstance(self.sourceList, dict):
            newHash = "".join(map(str, [item.id for item in self.sourceList.values()]))
        elif isinstance(self.sourceList, set):
            newHash = "".join(map(str, self.sourceList))
        if newHash != self.item_hash:
            if len(self.sourceList) == 0:
                self.item_list.set_item_list([])
            elif isinstance(self.sourceList, set):
                self.item_list.set_item_list(
                    [str(item) for item in self.sourceList]
                )
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