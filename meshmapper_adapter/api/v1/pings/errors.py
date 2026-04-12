from fastapi import HTTPException

class UnknownKey(Exception):
    def __init__(self, key: str):
        self.key = key