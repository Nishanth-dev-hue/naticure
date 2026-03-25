from deep_translator import GoogleTranslator

def translate_text(text, dest_lang='en'):
    try:
        if not text:
            return text

        # Normalize language codes
        lang_map = {
            'english': 'en',
            'telugu': 'te',
            'hindi': 'hi',
            'en': 'en',
            'te': 'te',
            'hi': 'hi'
        }

        target = lang_map.get(dest_lang, dest_lang)

        return GoogleTranslator(source='auto', target=target).translate(text)

    except Exception as e:
        return text