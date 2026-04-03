import os
from llama_index.llms.google_genai import GoogleGenAI
from google.genai import types

def pro_model(temperature: float = 0.1) -> GoogleGenAI:
    """
    Pro モデルを返す。
    技術的な翻訳目的に利用する場合、temperature(温度感)は 0 ～ 0.2 くらいが良いらしい。
    """
    model: str = os.environ.get("GEMINI_MODEL", "gemini-3.1-pro-preview")
    return GoogleGenAI(
        model=model,
        temperature=temperature
    )

def flash_model(temperature: float = 0.5) -> GoogleGenAI:
    """
    Flash モデルを返す。
    Lite モデルで足りない場合に利用する。
    """
    model: str = os.environ.get("GEMINI_FLASH_MODEL", "gemini-3.1-flash-preview")
    return GoogleGenAI(
        model=model,
        temperature=temperature
    )

def flash_lite_model(temperature: float = 1.0, deep_thinking: bool = False) -> GoogleGenAI:
    """
    Flash Lite モデルを返す
    翻訳以外はこれを利用する想定。
    """
    model: str = os.environ.get("GEMINI_FLASH_LITE_MODEL", "gemini-3.1-flash-lite-preview")

    # deep thinking level は ON/OFF くらいの感覚で。
    generation_config = None
    if deep_thinking:
        generation_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                thinking_level=types.ThinkingLevel.HIGH
            )
        )

    return GoogleGenAI(
        model=model,
        temperature=temperature,
        generation_config=generation_config
    )