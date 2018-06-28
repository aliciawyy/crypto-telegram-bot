from enum import Enum, auto, unique


class WorkflowEnum(Enum):
    pass


@unique
class CommandEnum(Enum):
    START = auto()
    REGISTER = auto()
    CANCEL = auto()

    def text(self):
        return self.name.replace("_", " ").lower()

    def command(self):
        return "/" + self.name.lower()


def build_menu(buttons, n_cols=1, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu
