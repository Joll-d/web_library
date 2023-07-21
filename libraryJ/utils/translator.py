from deep_translator import GoogleTranslator
import asyncio

class Translator:

    def __init__(self, destination_language: str) -> None:
        self.destination_language = destination_language

    def translate(self, source_text: str|list) -> str:
        if isinstance(source_text, str):
            translated_text = self.translate_element(source_text)
        elif isinstance(source_text, list):
            loop = asyncio.new_event_loop() 
            asyncio.set_event_loop(loop) 

            translated_text = source_text.copy()
            tasks = [self.translate_element_async(element) for element in source_text]
            translated_text = loop.run_until_complete(asyncio.gather(*tasks))

            loop.close() 

        return translated_text

    async def translate_element_async(self, source_text: str) -> str:
        translated_text = GoogleTranslator(source='auto', target=self.destination_language).translate(source_text)
        return translated_text
    
    def translate_element(self, source_text: str) -> str:
        translated_text = GoogleTranslator(source='auto', target=self.destination_language).translate(source_text)
        return translated_text
