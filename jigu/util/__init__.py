from __future__ import annotations

import base64
import hashlib
import uuid
import json

from bech32 import bech32_encode, convertbits

__all__ = ["b64_to_dict", "dict_to_b64", "get_bech", "generate_salt", "hash_amino"]


def b64_to_dict(b64data: str) -> dict:
    return json.loads(base64.b64decode(b64data).decode("utf-8"))


def dict_to_b64(data: dict) -> str:
    return base64.b64encode(json.dumps(data).encode("utf-8")).decode("utf-8")


def get_bech(prefix: str, payload: str) -> str:
    return bech32_encode(
        prefix, convertbits(bytes.fromhex(payload), 8, 5)
    )  # base64 -> base32


def generate_salt() -> str:
    """Generate a 4 bytes salt."""
    return uuid.uuid4().hex[:4]


def hash_amino(txdata: str) -> str:
    """Get the transaction hash from Amino-encoded Transaction in base64."""
    return hashlib.sha256(base64.b64decode(txdata)).digest().hex()
