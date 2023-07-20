from deep_translator import GoogleTranslator

class Translator:

    def __init__(self, destination_language: str) -> None:
        self.destination_language = destination_language

    def translate(self, source_text: str|list) -> str:
        if isinstance(source_text, str):
            translated_text = self.translate_element(source_text)
        elif isinstance(source_text, list):
            translated_text = source_text.copy()
            for i, source_text_element in enumerate(translated_text):
                translated_text[i] = self.translate_element(source_text_element)
                print(i)
        return translated_text

    def translate_element(self, source_text: str) -> str:
        translated_text = GoogleTranslator(source='auto', target=self.destination_language).translate(source_text)
        return translated_text
