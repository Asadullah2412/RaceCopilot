import os
import json
import streamlit as st
from google import genai as google_genai
from openai import OpenAI
from dotenv import load_dotenv

from prompts import (
    DEBRIEF_SYSTEM_PROMPT,
    FOLLOWUP_SYSTEM_PROMPT,
    build_session_context,
    build_debrief_prompt,
    build_followup_prompt,
)
from logger import log_api_call, log_error

load_dotenv()


# ─────────────────────────────────────────────
# API KEY LOADER
# Works locally (.env) and on Streamlit Cloud (st.secrets)
# ─────────────────────────────────────────────

def _get_secret(key: str) -> str:
    try:
        return st.secrets[key]
    except (FileNotFoundError, KeyError):
        return os.getenv(key, "")


# ─────────────────────────────────────────────
# MODEL CONFIG
# ─────────────────────────────────────────────

# Gemini tries these in order — stops at the first that works
GEMINI_MODELS = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-2.5-flash-lite",
]

# OpenRouter fallback — tries these in order
OPENROUTER_MODELS = [
    "meta-llama/llama-3.3-70b-instruct:free",
    "mistralai/mistral-small-3.1-24b-instruct:free",
    "deepseek/deepseek-r1:free",
]

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


# ─────────────────────────────────────────────
# INTERNAL — GEMINI CALL
# ─────────────────────────────────────────────

def _call_gemini(system_prompt: str, user_message: str, temperature: float, max_tokens: int) -> tuple[str, str]:
    """
    Tries each Gemini model in order.
    Returns (response_text, model_used) on success.
    Raises RuntimeError if all models fail.
    """
    api_key = _get_secret("GEMINI_API_KEY") or _get_secret("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("No Gemini API key found. Set GEMINI_API_KEY in .env or Streamlit secrets.")

    client = google_genai.Client(api_key=api_key)
    full_prompt = f"{system_prompt}\n\n{user_message}"

    for model in GEMINI_MODELS:
        try:
            response = client.models.generate_content(
                model=model,
                contents=full_prompt,
                config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                },
            )
            return response.text, model

        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "quota" in error_str.lower():
                log_error(f"Gemini quota hit — {model}", error_str)
                continue  # Try next Gemini model
            else:
                log_error(f"Gemini error — {model}", error_str)
                raise RuntimeError(f"Gemini failed on {model}: {e}")

    raise RuntimeError("All Gemini models quota exhausted — falling back to OpenRouter.")


# ─────────────────────────────────────────────
# INTERNAL — OPENROUTER FALLBACK CALL
# ─────────────────────────────────────────────

def _call_openrouter(system_prompt: str, user_message: str, temperature: float, max_tokens: int) -> tuple[str, str]:
    """
    Tries each OpenRouter model in order.
    Returns (response_text, model_used) on success.
    Raises RuntimeError if all models fail.
    """
    api_key = _get_secret("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("No OpenRouter API key found. Set OPENROUTER_API_KEY in .env or Streamlit secrets.")

    client = OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)

    for model in OPENROUTER_MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system",  "content": system_prompt},
                    {"role": "user",    "content": user_message},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content, model

        except Exception as e:
            log_error(f"OpenRouter error — {model}", str(e))
            continue

    raise RuntimeError("All OpenRouter models failed.")


# ─────────────────────────────────────────────
# INTERNAL — UNIFIED CALL WITH FALLBACK
# ─────────────────────────────────────────────

def _call_with_fallback(
    system_prompt: str,
    user_message: str,
    temperature: float,
    max_tokens: int,
    mode: str,
    sim: str,
    track: str,
) -> str:
    """
    Tries Gemini first. If Gemini quota is exhausted, falls back to OpenRouter.
    Logs which provider and model was used.
    Returns raw response text.
    Raises RuntimeError if both providers fail.
    """
    # Try Gemini
    try:
        text, model_used = _call_gemini(system_prompt, user_message, temperature, max_tokens)
        log_api_call(mode=mode, sim=sim, track=track, provider="Gemini", model=model_used)
        return text

    except RuntimeError as gemini_error:
        if "quota exhausted" in str(gemini_error):
            st.warning("⚠️ Gemini quota hit — switching to OpenRouter fallback.")
        else:
            st.warning(f"⚠️ Gemini unavailable ({gemini_error}) — trying OpenRouter.")

    # Fallback to OpenRouter
    text, model_used = _call_openrouter(system_prompt, user_message, temperature, max_tokens)
    log_api_call(mode=mode, sim=sim, track=track, provider="OpenRouter", model=model_used)
    return text


# ─────────────────────────────────────────────
# INTERNAL — JSON PARSER
# ─────────────────────────────────────────────

def _parse_json(raw: str) -> dict:
    """Strips markdown fences if present, then parses JSON."""
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        cleaned = "\n".join(lines[1:-1]).strip()
    return json.loads(cleaned)


# ─────────────────────────────────────────────
# PUBLIC FUNCTION 1 — analyse_debrief()
# ─────────────────────────────────────────────

def analyse_debrief(
    sim: str,
    car_class: str,
    track: str,
    laps: int,
    conditions: str,
    driver_debrief: str,
) -> dict:
    """
    Sends the driver's freeform debrief for structured analysis.
    Tries Gemini first, falls back to OpenRouter on quota failure.

    Returns:
        {"status": "ok",    "data": {...}}
        {"status": "error", "message": "..."}
    """
    session_ctx  = build_session_context(sim, car_class, track, laps, conditions)
    user_message = build_debrief_prompt(session_ctx, driver_debrief)

    try:
        raw = _call_with_fallback(
            system_prompt=DEBRIEF_SYSTEM_PROMPT,
            user_message=user_message,
            temperature=0.4,
            max_tokens=1500,
            mode="debrief",
            sim=sim,
            track=track,
        )
        return {"status": "ok", "data": _parse_json(raw)}

    except json.JSONDecodeError as e:
        log_error("JSON parse failure", str(e))
        return {
            "status": "error",
            "message": "Engineer received garbled data. Try submitting the debrief again.",
        }

    except Exception as e:
        log_error("Both providers failed — debrief", str(e))
        return {
            "status": "error",
            "message": f"Engineer is unreachable on all channels. ({e})",
        }


# ─────────────────────────────────────────────
# PUBLIC FUNCTION 2 — followup_chat()
# ─────────────────────────────────────────────

def followup_chat(
    sim: str,
    car_class: str,
    track: str,
    laps: int,
    conditions: str,
    original_analysis: dict,
    chat_history: list[dict],
    new_question: str,
) -> dict:
    """
    Handles follow-up questions after the debrief is shown.
    Caps chat history at 8 turns to control token usage.

    Returns:
        {"status": "ok",    "reply": "..."}
        {"status": "error", "message": "..."}
    """
    session_ctx   = build_session_context(sim, car_class, track, laps, conditions)
    analysis_text = json.dumps(original_analysis, indent=2)
    user_message  = build_followup_prompt(session_ctx, analysis_text, new_question)

    if chat_history:
        history_block = "\n".join(
            f"[{'Driver' if m['role'] == 'user' else 'Engineer'}]: {m['text']}"
            for m in chat_history[-8:]
        )
        user_message = f"[CONVERSATION SO FAR]\n{history_block}\n\n{user_message}"

    try:
        raw = _call_with_fallback(
            system_prompt=FOLLOWUP_SYSTEM_PROMPT,
            user_message=user_message,
            temperature=0.7,
            max_tokens=600,
            mode="followup",
            sim=sim,
            track=track,
        )
        return {"status": "ok", "reply": raw.strip()}

    except Exception as e:
        log_error("Both providers failed — followup", str(e))
        return {
            "status": "error",
            "message": "Engineer lost comms on all channels. Try again in a moment.",
        }