from pygame_gui.elements import UISelectionList


class SelectionListId(UISelectionList):
    def get_single_selection(self):
        """
        Get the selected item in a list, if any.
        Only works if this is a single-selection list.

        :return: A single item name as a string or None.

        """
        if not self.allow_multi_select:
            selected_list = [(item['text'], item['object_id']) for
                             item in self.item_list if item['selected']]
            if len(selected_list) == 1:
                return selected_list[0]
            elif len(selected_list) == 0:
                return None
            else:
                raise RuntimeError('More than one item selected in'
                                   ' single-selection selection list')
        else:
            raise RuntimeError('Requesting single selection,'
                               ' from multi-selection list')
