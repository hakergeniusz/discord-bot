# Copyright (C) 2026 hakergeniusz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Configuration module for the bot, including secrets and global constants."""

import datetime
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
TMP_BASE = PROJECT_ROOT / "tmp"

OWNER_ID = int(os.environ.get("DISCORD_OWNER_ID", "0"))
TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")

RICKROLL_GIF_URL = "https://tenor.com/view/rickroll-roll-rick-never-gonna-give-you-up-never-gonna-gif-22954713"  # noqa: E501

CURRENT_YEAR = datetime.date.today().year

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
