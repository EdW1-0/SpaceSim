from pygame_gui.elements import UIDropDownMenu

class DropDownMenuId(UIDropDownMenu):
    def __init__(self, options: dict, starting_option, rect, manager, container=None):
        super().__init__(list(options.keys()), starting_option, rect, manager, container)
        self.optionsDict = options

    def get_selected_option(self):
        selected_option = self.selected_option
        if selected_option is not None:
            return selected_option, self.optionsDict[selected_option]
        else:
            return None, None
        
    def process_event(self, event):
        processed = super().process_event(event)