from time import time_ns
from datetime import datetime, timezone
from hashlib import blake2s
from random import randrange, getrandbits
from uuid import getnode as get_mac

# base32 = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
base32 = "0123456789abcdefghjkmnpqrstvwxyz"

__author__ = 'Ryan Kwon <kznm.develop@gmail.com>'


def toBase32(n: int) -> str:
    if n < 32:
        return base32[n]
    return toBase32(n // 32) + base32[n % 32]


def LSID1(epoch: datetime = datetime(year=1970, month=1, day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc),
          worker_id: int = int(blake2s(key=get_mac().to_bytes(length=6, byteorder='big'), digest_size=2).hexdigest(), 16)) -> str:
    sequence_id: int = getrandbits(10)

    LSID: str = ""
    now: datetime = datetime.now(timezone.utc)
    now_ns = time_ns()

    # Date(5) # 5 * 5 = 25bit
    diff = now - epoch
    b32_date: str = toBase32(diff.days)
    LSID += ('0' * (5 - len(b32_date)) + b32_date + '-')

    # NS(8) # 8 * 5 = 40bit
    ns = int((now_ns % (24 * 60 * 60 * 1000 * 1000 * 1000)) / 100)
    b32_ns: str = toBase32(ns)
    LSID += ('0' * (8 - len(b32_ns)) + b32_ns + '-')

    # Worker ID(4) # 4 * 5 = 20bit
    b32_wid: str = toBase32(worker_id)
    if len(b32_wid) > 4:
        raise ValueError("Worker ID is too large (0<=int<=2^20-1)")
    LSID += ('0' * (4 - len(b32_wid)) + b32_wid + "-")

    # Random ID(2) # 2 * 5 = 10bit
    b32_sid: str = toBase32(sequence_id)
    if len(b32_sid) > 2:
        raise ValueError("Sequence ID is too large (0<=int<=2^10-1)")
    LSID += ('0' * (2 - len(b32_sid)) + b32_sid)

    return LSID
