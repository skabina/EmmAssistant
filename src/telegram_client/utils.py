from datetime import time
import datetime
import json
from pathlib import Path
import re


def correct_email(email: str) -> bool:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return bool(re.fullmatch(regex, email))


def greetings_by_time(times_message: datetime) -> str:
    twelve_step = time(12, 0)
    six_step = time(6,0)
    fifteen_step = time(15, 0)
    twenty_one_step = time(21, 0)

    with open(Path("src/resources/phrases.json"), "r", encoding="utf-8") as f:
        BOT_PHRASES = json.load(f)

    if six_step <= times_message < twelve_step:
        return BOT_PHRASES["time_based"]["morning"]
    elif twelve_step <= times_message < fifteen_step:
        return BOT_PHRASES["time_based"]["afternoon"]
    elif fifteen_step <= times_message < twenty_one_step:
        return BOT_PHRASES["time_based"]["evening"]
    elif twenty_one_step <= times_message or times_message < six_step:
        return BOT_PHRASES["time_based"]["night"]
    


   
