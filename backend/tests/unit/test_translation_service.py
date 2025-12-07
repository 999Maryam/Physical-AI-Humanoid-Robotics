import pytest
from backend.src.services.translation_service import TranslationService

@pytest.fixture
def translation_service():
    return TranslationService()

@pytest.mark.asyncio
async def test_translate_text_urdu(translation_service):
    text = "Hello, World!"
    translated_text = await translation_service.translate_text(text, target_language="ur")
    assert translated_text == "Translated (ur): Hello, World!"

@pytest.mark.asyncio
async def test_translate_text_unsupported_language(translation_service):
    text = "Hello, World!"
    translated_text = await translation_service.translate_text(text, target_language="es")
    assert translated_text == "Hello, World!" # Expect original text for unsupported language

@pytest.mark.asyncio
async def test_translate_chapter_urdu(translation_service):
    chapter_text = "This is a chapter about AI. It has multiple sentences."
    translated_chapter = await translation_service.translate_chapter(chapter_text, target_language="ur")
    assert translated_chapter == "Translated (ur): This is a chapter about AI. It has multiple sentences."

@pytest.mark.asyncio
async def test_translate_empty_text(translation_service):
    text = ""
    translated_text = await translation_service.translate_text(text, target_language="ur")
    assert translated_text == "Translated (ur): "
