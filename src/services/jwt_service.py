from typing import Any, Dict, List

from jose import jwt


async def decode_jwt(
        token: str,
        *,
        key: Any,
        algorithms: List[str] = ["HS256"],
        **kwargs: Any
) -> Dict[str, Any]:
    return jwt.decode(token, key=key, algorithms=algorithms, **kwargs)


async def encode_jwt(
        payload: dict,
        *,
        key: Any,
        algorithm: str = "HS256",
        **kwargs: Any,
):
    return jwt.encode(payload, key=key, algorithm=algorithm, **kwargs)
