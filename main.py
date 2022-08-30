from dataclasses import dataclass
import PySimpleGUI as sg
import process

unique_id = 0

sg.theme("Default 1")


def add_pokemon(window: sg.Window, name):
    global unique_id, NameMng
    tmp = []
    NameMng.add_Name(name, unique_id)
    for i in name:
        tmp.append(
            sg.Button(i, key=f"pokemon_button_{unique_id}", button_color=("#fff", Colors.Gray), font=("UD デジタル 教科書体 NK-B", 12, "bold")))
        unique_id += 1
    window.extend_layout(window["column"], [tmp])


class Colors:
    Gray = "#757575"
    Yellow = "#c9b458"
    Green = "#4caf50"


@dataclass
class CharState:
    id: int
    char: str
    color: str


class Name:
    def __init__(self, name, start_id) -> None:
        self.name = name
        self.chars: list[CharState] = []
        idx = start_id
        for i in range(len(name)):
            self.chars.append(CharState(idx, name[i], Colors.Gray))
            idx += 1

    def is_in_id(self, id: int):
        return len([i for i in self.chars if i.id == id]) != 0

    def get_chars_by_id(self, id: int):
        return [i for i in self.chars if i.id == id][0]


class NameManager:
    def __init__(self) -> None:
        self.initialize()

    def initialize(self):
        self.Names: list[Name] = []
        self.decided: str = "_____"
        self.non_decided: list[str] = [""]*5
        self.no_use: str = ""

    def get_name_by_id(self, id: int):
        for name in self.Names:
            if name.is_in_id(id):
                return name
        raise Exception()

    def get_chars_by_id(self, id: int):
        return self.get_name_by_id(id).get_chars_by_id(id)

    def add_Name(self, name: str, start_id: int):
        self.Names.append(Name(name, start_id))

    def process(self):
        self.decided: str = "_____"
        self.non_decided: list[str] = [""]*5
        self.no_use: str = ""
        for name in self.Names:
            for idx, char in enumerate(name.chars):
                match char.color:
                    case Colors.Green:
                        tmp = list(self.decided)
                        tmp[idx] = char.char
                        self.decided = str("".join(tmp))
                    case Colors.Yellow:
                        self.non_decided[idx] += char.char
                    case Colors.Gray:
                        if not char.char in self.no_use:
                            self.no_use += char.char
        return process.process(self.decided, self.non_decided, self.no_use)


NameMng = NameManager()

layout = [
    [sg.Column([], size=(400, 200),
               key="column", scrollable=True,  vertical_scroll_only=True)],
    [
        [sg.InputText("", key="pokemon_name")],
        [sg.Button("Enter", key="key_button_ok")]
    ],
    [sg.Button("リセット", key="reset"), sg.Button("入力欄にコピー", key="copy")],
    [sg.Listbox(NameMng.process(), size=(50, 60), key="list")],
]
window = sg.Window("Pokemon Wordle Adviser", layout=layout, size=(
    400, 500))
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "key_button_ok":
        add_pokemon(window, values["pokemon_name"])
        if len(NameMng.process()) > 0:
            window["pokemon_name"].update(NameMng.process()[0])
    if event.startswith("pokemon_button_"):
        id = int(event.replace("pokemon_button_", ""))
        char_button = NameMng.get_chars_by_id(id)
        if char_button.color == Colors.Gray:
            char_button.color = Colors.Yellow
            window[event].update(button_color=Colors.Yellow)
        elif char_button.color == Colors.Yellow:
            char_button.color = Colors.Green
            window[event].update(button_color=Colors.Green)
        elif char_button.color == Colors.Green:
            char_button.color = Colors.Gray
            window[event].update(button_color=Colors.Gray)
        if len(NameMng.process()) > 0:
            window["pokemon_name"].update(NameMng.process()[0])
    if event == "reset":
        for name in NameMng.Names:
            for char in name.chars:
                window[f"pokemon_button_{char.id}"].update(visible=False)
                window[f"pokemon_button_{char.id}"].Widget.master.pack_forget()
        NameMng.initialize()
        if len(NameMng.process()) > 0:
            window["pokemon_name"].update(NameMng.process()[0])
    if event == "copy":
        if len(values["list"]) != 0:
            window["pokemon_name"].update(values["list"][0])
    window["list"].update(NameMng.process())
    window["column"].contents_changed()
