import asyncio
import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from openai import AsyncOpenAI
from pydantic import BaseModel

load_dotenv()

logger = logging.getLogger(__name__)

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
if not OLLAMA_API_KEY:
    raise RuntimeError("OLLAMA_API_KEY is not set. Please add it to your .env file.")

OLLAMA_BASE_URL = "https://cloud.ollama.com/v1"
MODEL = "gemini-3-flash-preview"

app = FastAPI(title="Magic Translator")

client = AsyncOpenAI(
    api_key=OLLAMA_API_KEY,
    base_url=OLLAMA_BASE_URL,
)

LANGUAGE_NAMES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean",
    "ar": "Arabic",
    "hi": "Hindi",
    "he": "Hebrew",
    "tr": "Turkish",
    "pl": "Polish",
    "nl": "Dutch",
    "sv": "Swedish",
    "vi": "Vietnamese",
    "th": "Thai",
    "uk": "Ukrainian",
}


class TranslateRequest(BaseModel):
    text: str
    languages: list[str]


class TranslateResponse(BaseModel):
    result: dict[str, str]


@app.post("/translate")
async def translate(request: TranslateRequest) -> dict[str, str]:
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    if not request.languages:
        raise HTTPException(status_code=400, detail="At least one language must be specified")

    async def translate_one(lang_code: str) -> tuple[str, str]:
        lang_name = LANGUAGE_NAMES.get(lang_code, lang_code)
        prompt = (
            f"Translate the following text to {lang_name}. "
            f"Return only the translated text, no explanations or extra content.\n\n"
            f"Text: {request.text}"
        )
        try:
            response = await client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
            )
            translated = response.choices[0].message.content.strip()
            return lang_code, translated
        except Exception:
            logger.exception("Translation failed for language %s", lang_code)
            raise HTTPException(status_code=502, detail="Translation service error. Please try again later.")

    pairs = await asyncio.gather(*[translate_one(lang) for lang in request.languages])
    return dict(pairs)


app.mount("/", StaticFiles(directory="static", html=True), name="static")
