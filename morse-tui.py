import re
import pydantic
from typing import Optional

from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Input
from textual.widgets import Footer
from textual.binding import Binding

dot = '\N{Middle Dot}'
dash = '\N{Hyphen-Minus}'

class Morse(pydantic.BaseModel):
    letter: str
    sequence: str

    def __init__(self, letter: str, sequence:str):
        super(Morse, self).__init__(letter=letter, sequence=sequence)

morsecode = (
        Morse(" ",f" "),
        Morse("A",f"{dot}{dash}"),
        Morse("B",f"{dash}{dot}{dot}{dot}"),
        Morse("C",f"{dash}{dot}{dash}{dot}"),
        Morse("D",f"{dash}{dot}{dot}"),
        Morse("E",f"{dot}"),
        Morse("F",f"{dot}{dot}{dash}{dot}"),
        Morse("G",f"{dash}{dash}{dot}"),
        Morse("H",f"{dot}{dot}{dot}{dot}"),
        Morse("I",f"{dot}{dot}"),
        Morse("J",f"{dot}{dash}{dash}{dash}"),
        Morse("K",f"{dash}{dot}{dash}"),
        Morse("L",f"{dot}{dash}{dot}{dot}"),
        Morse("M",f"{dash}{dash}"),
        Morse("N",f"{dash}{dot}"),
        Morse("O",f"{dash}{dash}{dash}"),
        Morse("P",f"{dot}{dash}{dash}{dot}"),
        Morse("Q",f"{dash}{dash}{dot}{dash}"),
        Morse("R",f"{dot}{dash}{dot}"),
        Morse("S",f"{dot}{dot}{dot}"),
        Morse("T",f"{dash}"),
        Morse("U",f"{dot}{dot}{dash}"),
        Morse("V",f"{dot}{dot}{dot}{dash}"),
        Morse("W",f"{dot}{dash}{dash}"),
        Morse("X",f"{dash}{dot}{dot}{dash}"),
        Morse("Y",f"{dash}{dot}{dash}{dash}"),
        Morse("Z",f"{dash}{dash}{dot}{dot}"),
        Morse("1",f"{dot}{dash}{dash}{dash}{dash}"),
        Morse("2",f"{dot}{dot}{dash}{dash}{dash}"),
        Morse("3",f"{dot}{dot}{dot}{dash}{dash}"),
        Morse("4",f"{dot}{dot}{dot}{dot}{dash}"),
        Morse("5",f"{dot}{dot}{dot}{dot}{dot}"),
        Morse("6",f"{dash}{dot}{dot}{dot}{dot}"),
        Morse("7",f"{dash}{dash}{dot}{dot}{dot}"),
        Morse("8",f"{dash}{dash}{dash}{dot}{dot}"),
        Morse("9",f"{dash}{dash}{dash}{dash}{dot}"),
        Morse("0",f"{dash}{dash}{dash}{dash}{dash}"),
        Morse("À",f"{dot}{dash}{dash}{dot}{dash}"),
        Morse("Ä",f"{dot}{dash}{dot}{dash}"),
        Morse("È",f"{dot}{dash}{dot}{dot}{dash}"),
        Morse("É",f"{dot}{dot}{dash}{dot}{dot}"),
        Morse("Ö",f"{dash}{dash}{dash}{dot}"),
        Morse("Ü",f"{dot}{dot}{dash}{dash}"),
        Morse("ß",f"{dot}{dot}{dot}{dash}{dash}{dot}{dot}"),
        Morse("CH",f"{dash}{dash}{dash}{dash}"),
        Morse("Ñ",f"{dash}{dash}{dot}{dash}{dash}"),
        Morse(".",f"{dot}{dash}{dot}{dash}{dot}{dash}"),
        Morse(",",f"{dash}{dash}{dot}{dot}{dash}{dash}"),
        Morse(":",f"{dash}{dash}{dash}{dot}{dot}{dot}"),
        Morse(";",f"{dash}{dot}{dash}{dot}{dash}{dot}"),
        Morse("?",f"{dot}{dot}{dash}{dash}{dot}{dot}"),
        Morse("-",f"{dash}{dot}{dot}{dot}{dot}{dash}"),
        Morse("_",f"{dot}{dot}{dash}{dash}{dot}{dash}"),
        Morse("(",f"{dash}{dot}{dash}{dash}{dot}"),
        Morse(")",f"{dash}{dot}{dash}{dash}{dot}{dash}"),
        Morse("'",f"{dot}{dash}{dash}{dash}{dash}{dot}"),
        Morse("=",f"{dash}{dot}{dot}{dot}{dash}"),
        Morse("+",f"{dot}{dash}{dot}{dash}{dot}"),
        Morse("/",f"{dash}{dot}{dot}{dash}{dot}"),
        Morse("@",f"{dot}{dash}{dash}{dot}{dash}{dot}"),
        Morse("KA",f"{dash}{dot}{dash}{dot}{dash}"),
        Morse("BT",f"{dash}{dot}{dot}{dot}{dash}"),
        Morse("AR",f"{dot}{dash}{dot}{dash}{dot}"),
        Morse("VE",f"{dot}{dot}{dot}{dash}{dot}"),
        Morse("SK",f"{dot}{dot}{dot}{dash}{dot}{dash}"),
        Morse("SOS",f"{dot}{dot}{dot}{dash}{dash}{dash}{dot}{dot}{dot}"),
        Morse("HH",f"{dot}{dot}{dot}{dot}{dot}{dot}{dot}{dot}"),
        Morse("!",f"{dash}{dot}{dash}{dot}{dash}{dash}"),
        )

## decode helper functions

def sentencesFromMorseText(text=f'{dot}{dot}{dot} {dash}{dash}{dash} \t {dot}  \n {dot}{dot}{dot} {dash}{dash}{dash} {dot}  \r  {dot}{dot}{dot} {dash}{dash}{dash} {dot}'):
    ## splits text into sentences
    sentences = re.split(r'(\\{1,}|\r{1,}|\n{1,})', text)
    #print('sentences', sentences)
    return sentences

def wordsFromMorseSentences(sentence=f'{dot}{dot}{dot} {dash}{dash}{dash} {dot}  {dot}{dot}{dot} {dash}{dash}{dash} {dot}   {dot}{dot}{dot} {dash}{dash}{dash} {dot}'):
    ## splits a sentence into words when two or more spaces 
    words = re.split("\s{2,}", sentence)
    #print('words', words)
    return words

def charsFromMorseWords(word=f'{dot}{dot}{dot} {dash}{dash}{dash} {dot}  {dot}{dot}{dot} {dash}{dash}{dash} {dot}   {dot}{dot}{dot} {dash}{dash}{dash} {dot}'):
    ## splits a sentence into words when two or more spaces 
    chars = re.split("\s{1,}", word)
    #print('chars', chars)
    return chars

def normalize(text='_'):
    # replace unusual minus and and not needed white spaces
    return text.replace('_','{dash}')

def toDotDash(text=""):
    return text.replace('-',f'{dash}').replace('.',f'{dot}')

def decodeChar(char=f'{dot}'):
    for glyph in morsecode:
        if glyph.sequence == char:
            return glyph.letter
    return None

def encodeChar(char='A'):
    for glyph in morsecode:
        if glyph.letter == char:
            return glyph.sequence
    return None


# morse text en-/decoder function

def isMorseCode(text):
    dot = text.count('.')
    dash = text.count('-')
    leer = text.count(' ')
    if (dot+dash+leer) > len(text)/4:
        return True
    return False
    
def decodeText(text):
    result = ""
    text = toDotDash(text)
    sentences = sentencesFromMorseText(text)
    for sentence in sentences:
        words = wordsFromMorseSentences(sentence)
        for word in words:
            chars = charsFromMorseWords(word)
            result = result + ' '
            for char in chars:
                g = decodeChar(normalize(char))
                if g is not None:
                  result = result + str( g )
    result = result
    return str(result)

def encodeText(text):
    result = ""
    for char in text.upper():
        print("EncodedText ",char)
        result = result + encodeChar(char) + ' '
    result = result
    return str(result)

## Textual

class MorseWidget(Widget):

    text = reactive("")

    def render(self) -> str:
        return f"{self.text}"

class MorseApp(App):
    CSS = """
          """
    BINDINGS = [ Binding(key="d", action="toggle_dark", description="Toggle dark mode", show=True)
               ]
    
    mode = True

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter text or morse code (seperate morse words by 1 space, morse sentences by 3 spaces)")
        yield MorseWidget()
        yield Footer()

    def on_input_changed(self, event: Input.Changed) -> None:
        if isMorseCode(event.value):
            self.query_one(MorseWidget).text = decodeText(event.value)
        else:
            self.query_one(MorseWidget).text = encodeText(event.value)

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

def main():
    app = MorseApp()
    app.run()

if __name__ == '__main__':
    main()
