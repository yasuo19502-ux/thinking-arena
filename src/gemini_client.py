"""Gemini API client — structured output with JSON fallback."""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any, TypeVar

from google import genai
from google.genai import types
from pydantic import BaseModel, ValidationError

from src.prompts import (
    build_counter_feedback_prompt,
    build_feedback_prompt,
    build_scenario_prompt,
)
from src.schemas import (
    CounterFeedback,
    Feedback,
    Scenario,
    ScenarioList,
)

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

DEFAULT_MODEL = "gemini-2.5-flash"
MAX_ATTEMPTS = 3  # 1 lần gọi + 2 retry

_MISSING_KEY_MESSAGE = (
    "Chưa cấu hình GEMINI_API_KEY. "
    "Trên máy: tạo `.streamlit/secrets.toml` từ `secrets.toml.example`. "
    "Trên Streamlit Cloud: App Settings → Secrets. "
    "Sau đó khởi động lại app. Không có key vẫn dùng được chế độ demo ở Practice."
)


class GeminiConfigError(Exception):
    """Thiếu cấu hình API (key, v.v.)."""


class GeminiResponseError(Exception):
    """Không parse/validate được phản hồi từ model."""


def _read_secret_or_env(secret_key: str, env_key: str) -> str | None:
    """Đọc từ st.secrets trước, sau đó biến môi trường."""
    try:
        import streamlit as st

        value = st.secrets.get(secret_key)
        if value:
            return str(value).strip()
    except (FileNotFoundError, KeyError, AttributeError, TypeError):
        pass
    env_value = os.getenv(env_key)
    return env_value.strip() if env_value else None


def get_gemini_api_key() -> str | None:
    return _read_secret_or_env("GEMINI_API_KEY", "GEMINI_API_KEY")


def get_gemini_model() -> str:
    return _read_secret_or_env("GEMINI_MODEL", "GEMINI_MODEL") or DEFAULT_MODEL


def has_api_key() -> bool:
    """True nếu có GEMINI_API_KEY từ secrets hoặc biến môi trường."""
    return bool(get_gemini_api_key())


def is_api_configured() -> bool:
    """Alias của has_api_key() — tương thích code cũ."""
    return has_api_key()


def extract_json_from_text(text: str) -> str:
    """
    Trích JSON thuần từ text — xử lý markdown code block hoặc text thừa quanh JSON.
    """
    cleaned = text.strip()
    if not cleaned:
        raise GeminiResponseError("Model trả về nội dung rỗng.")

    fence = re.search(
        r"```(?:json)?\s*([\s\S]*?)\s*```",
        cleaned,
        flags=re.IGNORECASE,
    )
    if fence:
        cleaned = fence.group(1).strip()

    if cleaned.startswith("{") or cleaned.startswith("["):
        return cleaned

    obj_start = cleaned.find("{")
    arr_start = cleaned.find("[")

    if obj_start == -1 and arr_start == -1:
        raise GeminiResponseError("Không tìm thấy JSON trong phản hồi của model.")

    if obj_start == -1:
        start, end_char = arr_start, "]"
    elif arr_start == -1:
        start, end_char = obj_start, "}"
    else:
        start = min(obj_start, arr_start)
        end_char = "}" if start == obj_start else "]"

    end = cleaned.rfind(end_char)
    if end == -1 or end <= start:
        raise GeminiResponseError("JSON trong phản hồi không đầy đủ.")

    return cleaned[start : end + 1]


def _log_warning(message: str) -> None:
    """Ghi log không lộ API key; dùng st.warning nếu đang trong Streamlit."""
    safe = message.replace(get_gemini_api_key() or "", "***")
    logger.warning(safe)
    try:
        import streamlit as st

        st.warning(safe)
    except Exception:
        print(f"[Thinking Arena] {safe}")


def _parse_response_text(text: str, model: type[T]) -> T:
    try:
        payload = json.loads(extract_json_from_text(text))
    except json.JSONDecodeError as exc:
        raise GeminiResponseError(
            f"JSON không hợp lệ: {exc.msg}"
        ) from exc
    except GeminiResponseError:
        raise
    except Exception as exc:
        raise GeminiResponseError(f"Không đọc được JSON: {exc}") from exc

    try:
        return model.model_validate(payload)
    except ValidationError as exc:
        raise GeminiResponseError(
            f"Dữ liệu không khớp schema ({model.__name__}): "
            f"{len(exc.errors())} lỗi validation."
        ) from exc


class GeminiClient:
    """Client gọi Gemini với prompt + Pydantic schema của Thinking Arena."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str | None = None,
    ) -> None:
        key = api_key or get_gemini_api_key()
        if not key:
            raise GeminiConfigError(_MISSING_KEY_MESSAGE)

        self._model = model or get_gemini_model()
        self._client = genai.Client(api_key=key)

    def generate_scenarios(
        self,
        category: str,
        keyword: str,
        difficulty: str,
        mode: str,
    ) -> ScenarioList:
        prompt = build_scenario_prompt(category, keyword, difficulty, mode)
        result = self._generate_and_parse(prompt, ScenarioList)
        if len(result.scenarios) < 1:
            raise GeminiResponseError("Model không trả về tình huống nào.")
        return result

    def evaluate_answer(
        self,
        scenario: Scenario | dict[str, Any],
        user_answer: str,
        mode: str,
        target_duration: str,
    ) -> Feedback:
        prompt = build_feedback_prompt(scenario, user_answer, mode, target_duration)
        return self._generate_and_parse(prompt, Feedback)

    def evaluate_counter_response(
        self,
        scenario: Scenario | dict[str, Any],
        counter_question: str,
        user_response: str,
    ) -> CounterFeedback:
        prompt = build_counter_feedback_prompt(
            scenario, counter_question, user_response
        )
        return self._generate_and_parse(prompt, CounterFeedback)

    def _generate_and_parse(self, prompt: str, schema_model: type[T]) -> T:
        last_error: Exception | None = None
        use_structured = True

        for attempt in range(1, MAX_ATTEMPTS + 1):
            try:
                raw = self._call_model(
                    prompt,
                    schema_model=schema_model,
                    use_structured=use_structured,
                )
                return _parse_response_text(raw, schema_model)
            except GeminiConfigError:
                raise
            except (GeminiResponseError, ValidationError) as exc:
                last_error = exc
                _log_warning(
                    f"Lần {attempt}/{MAX_ATTEMPTS}: không xử lý được phản hồi — {exc}"
                )
                use_structured = False
            except Exception as exc:
                last_error = exc
                err_text = str(exc).lower()
                if "api key" in err_text or "permission" in err_text:
                    raise GeminiConfigError(
                        "API key không hợp lệ hoặc không có quyền truy cập. "
                        "Kiểm tra lại GEMINI_API_KEY."
                    ) from exc
                _log_warning(
                    f"Lần {attempt}/{MAX_ATTEMPTS}: lỗi gọi Gemini — "
                    f"{type(exc).__name__}: {exc}"
                )
                if "schema" in err_text or "response_schema" in err_text:
                    use_structured = False

        raise GeminiResponseError(
            "Không nhận được phản hồi hợp lệ từ AI sau "
            f"{MAX_ATTEMPTS} lần thử. "
            f"Chi tiết: {last_error}"
        ) from last_error

    def _call_model(
        self,
        prompt: str,
        *,
        schema_model: type[BaseModel],
        use_structured: bool,
    ) -> str:
        config: types.GenerateContentConfig | None = None

        if use_structured:
            config = types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema_model,
            )
            try:
                return self._invoke(prompt, config)
            except Exception as exc:
                if self._is_schema_config_error(exc):
                    _log_warning(
                        "Structured output (response_schema) lỗi — "
                        "chuyển sang JSON schema hoặc JSON thuần."
                    )
                    return self._call_with_json_schema(prompt, schema_model)
                raise

        config = types.GenerateContentConfig(
            response_mime_type="application/json",
        )
        return self._invoke(prompt, config)

    def _call_with_json_schema(
        self,
        prompt: str,
        schema_model: type[BaseModel],
    ) -> str:
        try:
            config = types.GenerateContentConfig(
                response_mime_type="application/json",
                response_json_schema=schema_model.model_json_schema(),
            )
            return self._invoke(prompt, config)
        except Exception as exc:
            if self._is_schema_config_error(exc):
                _log_warning("response_json_schema lỗi — fallback JSON thuần.")
                config = types.GenerateContentConfig(
                    response_mime_type="application/json",
                )
                return self._invoke(prompt, config)
            raise

    def _invoke(
        self,
        prompt: str,
        config: types.GenerateContentConfig | None,
    ) -> str:
        kwargs: dict[str, Any] = {
            "model": self._model,
            "contents": prompt,
        }
        if config is not None:
            kwargs["config"] = config

        response = self._client.models.generate_content(**kwargs)
        text = self._extract_text(response)
        if not text:
            raise GeminiResponseError("Model không trả về nội dung text.")
        return text

    @staticmethod
    def _extract_text(response: Any) -> str:
        if getattr(response, "text", None):
            return response.text.strip()

        candidates = getattr(response, "candidates", None) or []
        for candidate in candidates:
            content = getattr(candidate, "content", None)
            if not content:
                continue
            parts = getattr(content, "parts", None) or []
            chunks: list[str] = []
            for part in parts:
                part_text = getattr(part, "text", None)
                if part_text:
                    chunks.append(part_text)
            if chunks:
                return "\n".join(chunks).strip()
        return ""

    @staticmethod
    def _is_schema_config_error(exc: Exception) -> bool:
        text = str(exc).lower()
        markers = (
            "response_schema",
            "response_json_schema",
            "schema",
            "additionalproperties",
            "validation error for schema",
        )
        return any(m in text for m in markers)


def get_client() -> GeminiClient:
    """Factory tiện cho UI — tạo client mới mỗi lần (tránh stale key)."""
    return GeminiClient()
