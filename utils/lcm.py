from typing import Optional

from django.core.cache import cache

CACHE_PREFIX_LOGIN_CODE = "landzero:login-code:"

CACHE_PREFIX_LOGIN_CODE_EXISTED = "landzero:login-code:existed:"


def touch(code: str):
    cache.set(CACHE_PREFIX_LOGIN_CODE_EXISTED + code, 'true', 300)


def exist(code: str) -> bool:
    return True if cache.get(CACHE_PREFIX_LOGIN_CODE_EXISTED + code, None) else False


def remove(code: str):
    cache.delete(CACHE_PREFIX_LOGIN_CODE_EXISTED + code)
    cache.delete(CACHE_PREFIX_LOGIN_CODE + code)


def set_user_id(code: str, user_id: str):
    cache.set(CACHE_PREFIX_LOGIN_CODE + code, user_id, 300)


def get_user_id(code: str) -> Optional[str]:
    return cache.get(CACHE_PREFIX_LOGIN_CODE + code)
