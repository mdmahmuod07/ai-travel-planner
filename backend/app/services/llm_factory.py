import os
import json
import logging
import traceback
import httpx
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from app.config import settings

# Ensure environment is reloaded
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

logger = logging.getLogger("llm_factory")

class LLMProvider:
    def __init__(self):
        self.gemini_key = (
            settings.GEMINI_API_KEY
            or os.getenv("GEMINI_API_KEY", "")
            or os.getenv("GOOGLE_API_KEY", "")
        ).strip()
        self.openai_key = (
            settings.OPENAI_API_KEY
            or os.getenv("OPENAI_API_KEY", "")
        ).strip()

        if self.gemini_key:
            logger.info("LLM Provider: Gemini API Key detected.")
        if self.openai_key:
            logger.info("LLM Provider: OpenAI API Key detected.")
        if not self.gemini_key and not self.openai_key:
            logger.warning("LLM Provider: No external API key (GEMINI_API_KEY / OPENAI_API_KEY) found. Agents will use the high-fidelity authentic destination knowledge engine.")

    async def generate_json(self, system_prompt: str, user_prompt: str) -> Optional[Dict[str, Any]]:
        """
        Attempts LLM call to Gemini or OpenAI, logging any errors with full tracebacks.
        Falls back to None if keys are absent or API calls fail.
        """
        # Re-check env vars in case they were set at runtime
        gemini_key = (self.gemini_key or os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "")).strip()
        openai_key = (self.openai_key or os.getenv("OPENAI_API_KEY", "")).strip()

        if gemini_key:
            res = await self._call_gemini(gemini_key, system_prompt, user_prompt)
            if res:
                return res

        if openai_key:
            res = await self._call_openai(openai_key, system_prompt, user_prompt)
            if res:
                return res

        return None

    async def _call_gemini(self, api_key: str, system_prompt: str, user_prompt: str) -> Optional[Dict[str, Any]]:
        # Try active Gemini models in order of capability & speed
        models_to_try = ["gemini-2.0-flash", "gemini-1.5-flash"]
        for model in models_to_try:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
                payload = {
                    "contents": [
                        {
                            "role": "user",
                            "parts": [
                                {
                                    "text": (
                                        f"{system_prompt}\n\n"
                                        "CRITICAL INSTRUCTION: Respond strictly in valid JSON format only, "
                                        "with NO surrounding markdown backticks or commentary.\n\n"
                                        f"TASK CONTEXT:\n{user_prompt}"
                                    )
                                }
                            ]
                        }
                    ],
                    "generationConfig": {
                        "responseMimeType": "application/json",
                        "temperature": 0.7
                    }
                }

                async with httpx.AsyncClient(timeout=35.0) as client:
                    response = await client.post(url, json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        text = data['candidates'][0]['content']['parts'][0]['text'].strip()
                        # Clean any accidental markdown fence
                        if text.startswith("```json"):
                            text = text[7:]
                        if text.startswith("```"):
                            text = text[3:]
                        if text.endswith("```"):
                            text = text[:-3]
                        parsed = json.loads(text.strip())
                        logger.info(f"Gemini API call ({model}) succeeded.")
                        return parsed
                    else:
                        logger.error(
                            f"Gemini API ({model}) returned error HTTP {response.status_code}: {response.text}"
                        )
            except Exception as e:
                logger.error(f"Gemini API ({model}) exception: {e}\n{traceback.format_exc()}")

        return None

    async def _call_openai(self, api_key: str, system_prompt: str, user_prompt: str) -> Optional[Dict[str, Any]]:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-4o-mini",
                "response_format": {"type": "json_object"},
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7
            }

            async with httpx.AsyncClient(timeout=35.0) as client:
                response = await client.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    text = data['choices'][0]['message']['content'].strip()
                    parsed = json.loads(text)
                    logger.info("OpenAI API call (gpt-4o-mini) succeeded.")
                    return parsed
                else:
                    logger.error(
                        f"OpenAI API returned error HTTP {response.status_code}: {response.text}"
                    )
        except Exception as e:
            logger.error(f"OpenAI API exception: {e}\n{traceback.format_exc()}")

        return None

llm_provider = LLMProvider()
