from fastapi import APIRouter, HTTPException
from backend.src.services.translation_service import TranslationService
from backend.src.services.ingestion_service import IngestionService # To fetch chapter content

router = APIRouter()
translation_service = TranslationService()
ingestion_service = IngestionService() # Assuming we can reuse or get content from here

@router.post("/chapters/{chapter_id}/translate", response_model=dict)
async def translate_chapter_endpoint(chapter_id: str, target_language: str = "ur"):
    # In a real application, you would fetch the original chapter content from your DB (Neon)
    # For this mock, we'll just pretend to fetch content.
    # You might have a method in IngestionService or a dedicated ChapterService to get content by ID.

    # Mock fetching chapter content
    # For simplicity, let's assume chapter_id directly maps to some content for now.
    # IngestionService currently does not have a direct 'get_chapter_content' method.
    # This part would need actual database integration to retrieve the chapter text.
    original_content = f"This is the content of chapter {chapter_id}."
    # A more realistic approach would involve querying Neon for the content.
    # For example: original_content = ingestion_service.get_chapter_content(chapter_id)

    if not original_content:
        raise HTTPException(status_code=404, detail=f"Chapter with ID {chapter_id} not found")

    translated_text = await translation_service.translate_chapter(original_content, target_language)

    return {"chapter_id": chapter_id, "translated_text": translated_text, "target_language": target_language}
