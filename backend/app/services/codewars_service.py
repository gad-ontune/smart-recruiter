import httpx
from typing import Optional

from app.core.config import settings


class CodewarsError(Exception):
    pass


def fetch_kata(kata_id: str, max_retries: int = 3, base_delay: float = 1.0) -> dict:
    """Fetch a single kata from the Codewars public API with retry logic."""
    url = f"{settings.codewars_base_url}/code-challenges/{kata_id}"
    
    for attempt in range(max_retries + 1):
        try:
            response = httpx.get(url, timeout=10.0)
            if response.status_code == 404:
                raise CodewarsError(f"Kata '{kata_id}' not found")
            if response.status_code != 200:
                raise CodewarsError(f"Codewars API error: {response.status_code}")
            return response.json()
        except httpx.RequestError as exc:
            if attempt < max_retries:
                # Exponential backoff: 1s, 2s, 4s, ...
                delay = base_delay * (2 ** attempt)
                print(f"Attempt {attempt + 1} failed for kata {kata_id}: {exc}. Retrying in {delay}s...")
                import time
                time.sleep(delay)
            else:
                raise CodewarsError(f"Failed to fetch kata '{kata_id}' after {max_retries + 1} attempts: {exc}") from exc


def map_kata_to_question(kata: dict) -> dict:
    """Shape a raw Codewars kata response into our Question schema fields."""
    return {
        "type": "coding",
        "title": kata.get("name", "Untitled kata"),
        "prompt": kata.get("description", ""),
        "difficulty": (kata.get("rank") or {}).get("name", "unknown"),
        "languages": kata.get("languages", []),
        "source": "codewars",
        "source_id": kata.get("id"),
        "source_url": kata.get("url"),
        "tags": kata.get("tags", []),
    }


def map_kata_to_question(kata: dict) -> dict:
    """Shape a raw Codewars kata response into our Question schema fields."""
    return {
        "type": "coding",
        "title": kata.get("name", "Untitled kata"),
        "prompt": kata.get("description", ""),
        "difficulty": (kata.get("rank") or {}).get("name", "unknown"),
        "languages": kata.get("languages", []),
        "source": "codewars",
        "source_id": kata.get("id"),
        "source_url": kata.get("url"),
        "tags": kata.get("tags", []),
    }


def import_kata_as_question(kata_id: str) -> dict:
    kata = fetch_kata(kata_id)
    return map_kata_to_question(kata)

