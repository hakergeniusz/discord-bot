# Copyright (c) 2025-2026 hakergeniusz
#
# Licensed under the EUPL, Version 1.2 or - as soon they will be approved by the European
# Commission - subsequent versions of the EUPL (the "Licence"); You may not use this work
# except in compliance with the Licence.
#
# You may obtain a copy of the Licence at:
# https://joinup.ec.europa.eu/software/page/eupl
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the Licence for the specific language
# governing permissions and limitations under the Licence.

"""Configuration module for the bot, including secrets and global constants."""

import datetime
import os
import tempfile
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
TMP_BASE = Path(tempfile.gettempdir()) / "discord-bot"
CONFIG_PATH = PROJECT_ROOT / "config.yaml"

TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if CONFIG_PATH.exists():
    CONFIG_DATA = yaml.safe_load(CONFIG_PATH.read_text())
    ADMINS = list(CONFIG_DATA.get("admins")) if CONFIG_DATA.get("admins", []) else []
    PREFIX = CONFIG_DATA.get("prefix", "!")
else:
    ADMINS = []
    PREFIX = "!"

RICKROLL_GIF_URL = (
    "https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713"
)

CURRENT_YEAR = datetime.datetime.now(tz=datetime.UTC).date().year

STATUS_MAP = {
    "Finished": "Finished",
    "+1 Lap": "+1 Lap",
    "+2 Laps": "+2 Laps",
    "+3 Laps": "+3 Laps",
    "+4 Laps": "+4 Laps",
    "+5 Laps": "+5 Laps",
    "+6 Laps": "+6 Laps",
    "+7 Laps": "+7 Laps",
    "+8 Laps": "+8 Laps",
    "+9 Laps": "+9 Laps",
    "+10 Laps": "+10 Laps",
    "+11 Laps": "+11 Laps",
    "+12 Laps": "+12 Laps",
    "+13 Laps": "+13 Laps",
    "+14 Laps": "+14 Laps",
    "+15 Laps": "+15 Laps",
    "+16 Laps": "+16 Laps",
    "+17 Laps": "+17 Laps",
    "+18 Laps": "+18 Laps",
    "+19 Laps": "+19 Laps",
    "+22 Laps": "+22 Laps",
    "+24 Laps": "+24 Laps",
    "+25 Laps": "+25 Laps",
    "Lapped": "Lapped",
    "Accident": "DNF (Accident)",
    "Alternator": "DNF (Alternator)",
    "Axle": "DNF (Axle)",
    "Battery": "DNF (Battery)",
    "Brakes": "DNF (Brakes)",
    "Broken wing": "DNF (Broken wing)",
    "Chassis": "DNF (Chassis)",
    "Clutch": "DNF (Clutch)",
    "Collision": "DNF (Collision)",
    "Collision damage": "DNF (Collision damage)",
    "Differential": "DNF (Differential)",
    "Distributor": "DNF (Distributor)",
    "Driver unwell": "DNF (Driver unwell)",
    "Driveshaft": "DNF (Driveshaft)",
    "ERS": "DNF (ERS)",
    "Electrical": "DNF (Electrical)",
    "Electronics": "DNF (Electronics)",
    "Engine": "DNF (Engine)",
    "Exhaust": "DNF (Exhaust)",
    "Fatal accident": "DNF (Fatal accident)",
    "Fire": "DNF (Fire)",
    "Front wing": "DNF (Front wing)",
    "Fuel": "DNF (Fuel)",
    "Fuel leak": "DNF (Fuel leak)",
    "Fuel pipe": "DNF (Fuel pipe)",
    "Fuel pressure": "DNF (Fuel pressure)",
    "Fuel pump": "DNF (Fuel pump)",
    "Fuel system": "DNF (Fuel system)",
    "Gearbox": "DNF (Gearbox)",
    "Halfshaft": "DNF (Halfshaft)",
    "Handling": "DNF (Handling)",
    "Heat shield fire": "DNF (Heat shield fire)",
    "Hydraulics": "DNF (Hydraulics)",
    "Ignition": "DNF (Ignition)",
    "Injection": "DNF (Injection)",
    "Injured": "DNF (Injured)",
    "Injury": "DNF (Injury)",
    "Magneto": "DNF (Magneto)",
    "Mechanical": "DNF (Mechanical)",
    "Not classified": "DNF (Not classified)",
    "Oil leak": "DNF (Oil leak)",
    "Oil pipe": "DNF (Oil pipe)",
    "Oil pressure": "DNF (Oil pressure)",
    "Oil pump": "DNF (Oil pump)",
    "Out of fuel": "DNF (Out of fuel)",
    "Overheating": "DNF (Overheating)",
    "Physical": "DNF (Physical)",
    "Pneumatics": "DNF (Pneumatics)",
    "Power Unit": "DNF (Power Unit)",
    "Power loss": "DNF (Power loss)",
    "Puncture": "DNF (Puncture)",
    "Radiator": "DNF (Radiator)",
    "Rear wing": "DNF (Rear wing)",
    "Retired": "DNF (Retired)",
    "Spark plugs": "DNF (Spark plugs)",
    "Spun off": "DNF (Spun off)",
    "Steering": "DNF (Steering)",
    "Supercharger": "DNF (Supercharger)",
    "Suspension": "DNF (Suspension)",
    "Technical": "DNF (Technical)",
    "Throttle": "DNF (Throttle)",
    "Transmission": "DNF (Transmission)",
    "Turbo": "DNF (Turbo)",
    "Tyre": "DNF (Tyre)",
    "Undertray": "DNF (Undertray)",
    "Vibrations": "DNF (Vibrations)",
    "Water leak": "DNF (Water leak)",
    "Water pressure": "DNF (Water pressure)",
    "Water pump": "DNF (Water pump)",
    "Wheel": "DNF (Wheel)",
    "Wheel bearing": "DNF (Wheel bearing)",
    "Wheel nut": "DNF (Wheel nut)",
    "Did not start": "DNS (Did not start)",
    "Withdrew": "DNS (Withdrew)",
    "Disqualified": "DSQ (Disqualified)",
    "Excluded": "DSQ (Excluded)",
}


# Magic values

## Response codes
UNAUTHORIZED_RESPONSE_CODE: int = 401
RATE_LIMIT_RESPONSE_CODE: int = 429
SUCCESS_RESPONSE_CODE: int = 204
NORESPONSE_SUCCESS_RESPONSE_CODE: int = 200


COWSAY_INPUT_LIMIT: int = 250
MAX_MUSIC_REPLY_COUNT: int = 3
SECONDS_IN_MINUTE: int = 60
F1_FIRST_YEAR: int = 1950
DISCORD_MESSAGE_LIMIT: int = 2000
AI_RESPONSE_LIMIT: int = DISCORD_MESSAGE_LIMIT - 100
FULL_COWSAY_LIMIT: int = 1500
COWSAY_SLICE_LIMIT: int = FULL_COWSAY_LIMIT - 3
