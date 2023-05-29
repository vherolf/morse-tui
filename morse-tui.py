import re
import pydantic
from typing import Optional

from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Input
from textual.widgets import Footer
from textual.binding import Binding

class Morse(pydantic.BaseModel):
    letter: str
    sequence: str

    def __init__(self, letter: str, sequence:str):
        super(Morse, self).__init__(letter=letter, sequence=sequence)

morsecode = (
        Morse(" "," "),
        Morse("A",".-"),
        Morse("B","-..."),
        Morse("C","-.-."),
        Morse("D","-.."),
        Morse("E","."),
        Morse("F","..-."),
        Morse("G","--."),
        Morse("H","...."),
        Morse("I",".."),
        Morse("J",".---"),
        Morse("K","-.-"),
        Morse("L",".-.."),
        Morse("M","--"),
        Morse("N","-."),
        Morse("O","---"),
        Morse("P",".--."),
        Morse("Q","--.-"),
        Morse("R",".-."),
        Morse("S","..."),
        Morse("T","-"),
        Morse("U","..-"),
        Morse("V","...-"),
        Morse("W",".--"),
        Morse("X","-..-"),
        Morse("Y","-.--"),
        Morse("Z","--.."),
        Morse("1",".----"),
        Morse("2","..---"),
        Morse("3","...--"),
        Morse("4","....-"),
        Morse("5","....."),
        Morse("6","-...."),
        Morse("7","--..."),
        Morse("8","---.."),
        Morse("9","----."),
        Morse("0","-----"),
        Morse("À",".--.-"),
        Morse("Ä",".-.-"),
        Morse("È",".-..-"),
        Morse("É","..-.."),
        Morse("Ö","---."),
        Morse("Ü","..--"),
        Morse("ß","...--.."),
        Morse("CH","----"),
        Morse("Ñ","--.--"),
        Morse(".",".-.-.-"),
        Morse(",","--..--"),
        Morse(":","---..."),
        Morse(";","-.-.-."),
        Morse("?","..--.."),
        Morse("-","-....-"),
        Morse("_","..--.-"),
        Morse("(","-.--."),
        Morse(")","-.--.-"),
        Morse("'",".----."),
        Morse("=","-...-"),
        Morse("+",".-.-."),
        Morse("/","-..-."),
        Morse("@",".--.-."),
        Morse("KA","-.-.-"),
        Morse("BT","-...-"),
        Morse("AR",".-.-."),
        Morse("VE","...-."),
        Morse("SK","...-.-"),
        Morse("SOS","...---..."),
        Morse("HH","........"),
        Morse("!","-.-.--"),
        )

## decode helper functions

def sentencesFromMorseText(text='... --- \t .  \n ... --- .  \r  ... --- .'):
    ## splits text into sentences
    sentences = re.split(r'(\\{1,}|\r{1,}|\n{1,})', text)
    #print('sentences', sentences)
    return sentences

def wordsFromMorseSentences(sentence='... --- .  ... --- .   ... --- .'):
    ## splits a sentence into words when two or more spaces 
    words = re.split("\s{2,}", sentence)
    #print('words', words)
    return words

def charsFromMorseWords(word='... --- .  ... --- .   ... --- .'):
    ## splits a sentence into words when two or more spaces 
    chars = re.split("\s{1,}", word)
    #print('chars', chars)
    return chars

def normalize(text='_'):
    # replace unusual minus and and not needed white spaces
    return text.replace('_','-')

def decodeChar(char='.'):
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
        yield Input(placeholder="Enter text or morse code")
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
