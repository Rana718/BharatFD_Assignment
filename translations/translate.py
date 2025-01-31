from googletrans import Translator

async def translate_text(text, target_lang):
    translator = Translator()
    try:
        translation = await translator.translate(text, dest=target_lang)
        return translation.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

