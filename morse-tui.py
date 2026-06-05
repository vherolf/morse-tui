import re

from pydantic import BaseModel
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.reactive import reactive
from textual.widgets import Footer, Input, Static

DOT = '\N{Middle Dot}'
DASH = '\N{Hyphen-Minus}'


class Morse(BaseModel):
    letter: str
    sequence: str


morsecode: tuple[Morse, ...] = (
    Morse(letter=" ",   sequence=" "),
    Morse(letter="A",   sequence=f"{DOT}{DASH}"),
    Morse(letter="B",   sequence=f"{DASH}{DOT}{DOT}{DOT}"),
    Morse(letter="C",   sequence=f"{DASH}{DOT}{DASH}{DOT}"),
    Morse(letter="D",   sequence=f"{DASH}{DOT}{DOT}"),
    Morse(letter="E",   sequence=f"{DOT}"),
    Morse(letter="F",   sequence=f"{DOT}{DOT}{DASH}{DOT}"),
    Morse(letter="G",   sequence=f"{DASH}{DASH}{DOT}"),
    Morse(letter="H",   sequence=f"{DOT}{DOT}{DOT}{DOT}"),
    Morse(letter="I",   sequence=f"{DOT}{DOT}"),
    Morse(letter="J",   sequence=f"{DOT}{DASH}{DASH}{DASH}"),
    Morse(letter="K",   sequence=f"{DASH}{DOT}{DASH}"),
    Morse(letter="L",   sequence=f"{DOT}{DASH}{DOT}{DOT}"),
    Morse(letter="M",   sequence=f"{DASH}{DASH}"),
    Morse(letter="N",   sequence=f"{DASH}{DOT}"),
    Morse(letter="O",   sequence=f"{DASH}{DASH}{DASH}"),
    Morse(letter="P",   sequence=f"{DOT}{DASH}{DASH}{DOT}"),
    Morse(letter="Q",   sequence=f"{DASH}{DASH}{DOT}{DASH}"),
    Morse(letter="R",   sequence=f"{DOT}{DASH}{DOT}"),
    Morse(letter="S",   sequence=f"{DOT}{DOT}{DOT}"),
    Morse(letter="T",   sequence=f"{DASH}"),
    Morse(letter="U",   sequence=f"{DOT}{DOT}{DASH}"),
    Morse(letter="V",   sequence=f"{DOT}{DOT}{DOT}{DASH}"),
    Morse(letter="W",   sequence=f"{DOT}{DASH}{DASH}"),
    Morse(letter="X",   sequence=f"{DASH}{DOT}{DOT}{DASH}"),
    Morse(letter="Y",   sequence=f"{DASH}{DOT}{DASH}{DASH}"),
    Morse(letter="Z",   sequence=f"{DASH}{DASH}{DOT}{DOT}"),
    Morse(letter="1",   sequence=f"{DOT}{DASH}{DASH}{DASH}{DASH}"),
    Morse(letter="2",   sequence=f"{DOT}{DOT}{DASH}{DASH}{DASH}"),
    Morse(letter="3",   sequence=f"{DOT}{DOT}{DOT}{DASH}{DASH}"),
    Morse(letter="4",   sequence=f"{DOT}{DOT}{DOT}{DOT}{DASH}"),
    Morse(letter="5",   sequence=f"{DOT}{DOT}{DOT}{DOT}{DOT}"),
    Morse(letter="6",   sequence=f"{DASH}{DOT}{DOT}{DOT}{DOT}"),
    Morse(letter="7",   sequence=f"{DASH}{DASH}{DOT}{DOT}{DOT}"),
    Morse(letter="8",   sequence=f"{DASH}{DASH}{DASH}{DOT}{DOT}"),
    Morse(letter="9",   sequence=f"{DASH}{DASH}{DASH}{DASH}{DOT}"),
    Morse(letter="0",   sequence=f"{DASH}{DASH}{DASH}{DASH}{DASH}"),
    Morse(letter="À",   sequence=f"{DOT}{DASH}{DASH}{DOT}{DASH}"),
    Morse(letter="Ä",   sequence=f"{DOT}{DASH}{DOT}{DASH}"),
    Morse(letter="È",   sequence=f"{DOT}{DASH}{DOT}{DOT}{DASH}"),
    Morse(letter="É",   sequence=f"{DOT}{DOT}{DASH}{DOT}{DOT}"),
    Morse(letter="Ö",   sequence=f"{DASH}{DASH}{DASH}{DOT}"),
    Morse(letter="Ü",   sequence=f"{DOT}{DOT}{DASH}{DASH}"),
    Morse(letter="ß",   sequence=f"{DOT}{DOT}{DOT}{DASH}{DASH}{DOT}{DOT}"),
    Morse(letter="CH",  sequence=f"{DASH}{DASH}{DASH}{DASH}"),
    Morse(letter="Ñ",   sequence=f"{DASH}{DASH}{DOT}{DASH}{DASH}"),
    Morse(letter=".",   sequence=f"{DOT}{DASH}{DOT}{DASH}{DOT}{DASH}"),
    Morse(letter=",",   sequence=f"{DASH}{DASH}{DOT}{DOT}{DASH}{DASH}"),
    Morse(letter=":",   sequence=f"{DASH}{DASH}{DASH}{DOT}{DOT}{DOT}"),
    Morse(letter=";",   sequence=f"{DASH}{DOT}{DASH}{DOT}{DASH}{DOT}"),
    Morse(letter="?",   sequence=f"{DOT}{DOT}{DASH}{DASH}{DOT}{DOT}"),
    Morse(letter="-",   sequence=f"{DASH}{DOT}{DOT}{DOT}{DOT}{DASH}"),
    Morse(letter="_",   sequence=f"{DOT}{DOT}{DASH}{DASH}{DOT}{DASH}"),
    Morse(letter="(",   sequence=f"{DASH}{DOT}{DASH}{DASH}{DOT}"),
    Morse(letter=")",   sequence=f"{DASH}{DOT}{DASH}{DASH}{DOT}{DASH}"),
    Morse(letter="'",   sequence=f"{DOT}{DASH}{DASH}{DASH}{DASH}{DOT}"),
    Morse(letter="=",   sequence=f"{DASH}{DOT}{DOT}{DOT}{DASH}"),
    Morse(letter="+",   sequence=f"{DOT}{DASH}{DOT}{DASH}{DOT}"),
    Morse(letter="/",   sequence=f"{DASH}{DOT}{DOT}{DASH}{DOT}"),
    Morse(letter="@",   sequence=f"{DOT}{DASH}{DASH}{DOT}{DASH}{DOT}"),
    Morse(letter="KA",  sequence=f"{DASH}{DOT}{DASH}{DOT}{DASH}"),
    Morse(letter="BT",  sequence=f"{DASH}{DOT}{DOT}{DOT}{DASH}"),
    Morse(letter="AR",  sequence=f"{DOT}{DASH}{DOT}{DASH}{DOT}"),
    Morse(letter="VE",  sequence=f"{DOT}{DOT}{DOT}{DASH}{DOT}"),
    Morse(letter="SK",  sequence=f"{DOT}{DOT}{DOT}{DASH}{DOT}{DASH}"),
    Morse(letter="SOS", sequence=f"{DOT}{DOT}{DOT}{DASH}{DASH}{DASH}{DOT}{DOT}{DOT}"),
    Morse(letter="HH",  sequence=f"{DOT}{DOT}{DOT}{DOT}{DOT}{DOT}{DOT}{DOT}"),
    Morse(letter="!",   sequence=f"{DASH}{DOT}{DASH}{DOT}{DASH}{DASH}"),
)

# O(1) lookup dicts built once at import time
_ENCODE: dict[str, str] = {m.letter: m.sequence for m in morsecode}
_DECODE: dict[str, str] = {m.sequence: m.letter for m in morsecode}


def _normalize(text: str) -> str:
    """Convert ASCII dot to unicode middle-dot used internally."""
    return text.replace('.', DOT)


def is_morse(text: str) -> bool:
    """Heuristic: if >25% of chars are morse symbols, treat as morse input."""
    if not text:
        return False
    dots = text.count('.') + text.count(DOT)
    dashes = text.count('-')
    if dots + dashes == 0:
        return False
    spaces = text.count(' ')
    return (dots + dashes + spaces) > len(text) / 4


def encode(text: str) -> str:
    """Encode plain text to morse code. Unknown chars are skipped."""
    parts = [_ENCODE[c] for c in text.upper() if c in _ENCODE]
    return ' '.join(parts)


def decode(text: str) -> str:
    """Decode morse code to plain text."""
    text = _normalize(text)
    words: list[str] = []
    for sentence in re.split(r'[\r\n\\]+', text):
        for word in re.split(r'\s{2,}', sentence):
            chars = [_DECODE.get(c, '') for c in re.split(r'\s+', word.strip()) if c]
            word_str = ''.join(chars)
            if word_str:
                words.append(word_str)
    return ' '.join(words)


class MorseOutput(Static):
    output: reactive[str] = reactive("")

    def watch_output(self, value: str) -> None:
        self.update(value)


class MorseApp(App):
    CSS = """
    Screen {
        layout: vertical;
        padding: 1 2;
    }

    Input {
        margin-bottom: 1;
    }

    MorseOutput {
        padding: 1 2;
        border: round $primary;
        min-height: 5;
        color: $text;
    }
    """

    BINDINGS = [
        Binding("d", "toggle_dark", "Toggle dark mode"),
        Binding("ctrl+c", "quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Input(
            placeholder="Type text → morse  |  Type ·-· --- morse → text  (words: 2 spaces, sentences: 3 spaces)"
        )
        yield MorseOutput()
        yield Footer()

    def on_input_changed(self, event: Input.Changed) -> None:
        value = event.value
        if is_morse(value):
            self.query_one(MorseOutput).output = decode(value)
        else:
            self.query_one(MorseOutput).output = encode(value)


def main() -> None:
    MorseApp().run()


if __name__ == "__main__":
    main()
