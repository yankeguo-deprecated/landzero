from typing import Optional

from django.core.cache import cache

CACHE_PREFIX_LOGIN_CODE = "landzero:login-code:"

CACHE_PREFIX_LOGIN_CODE_EXISTED = "landzero:login-code:existed:"


def mark_code(code: str):
    cache.set(CACHE_PREFIX_LOGIN_CODE_EXISTED + code, 'true', 300)


def unmark_code(code: str):
    cache.delete(CACHE_PREFIX_LOGIN_CODE_EXISTED + code)


def has_code(code: str) -> bool:
    return True if cache.get(CACHE_PREFIX_LOGIN_CODE_EXISTED + code, None) else False


def set_code_user(code: str, user_id: str):
    cache.set(CACHE_PREFIX_LOGIN_CODE + code, user_id, 300)


def get_code_user(code: str) -> Optional[str]:
    return cache.get(CACHE_PREFIX_LOGIN_CODE + code)


def delete_code_user(code: str):
    return cache.delete(CACHE_PREFIX_LOGIN_CODE + code)
