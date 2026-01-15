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

import os
import datetime
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TMP_BASE = os.path.join(PROJECT_ROOT, "tmp")

OWNER_ID = int(os.environ.get('DISCORD_OWNER_ID', '0'))
TOKEN = os.environ.get('DISCORD_BOT_TOKEN', '')

PC_POWEROFF = os.environ.get('POWEROFF_COMMAND')
if PC_POWEROFF != 'True':
    PC_POWEROFF = None

CURRENT_YEAR = datetime.date.today().year

status_map = {
    "Lapped": "Lapped",
    "Retired": "DNF",
    "Accident": "DNF (Accident)",
    "Collision": "DNF (Collision)",
    "Spun off": "DNF (Spin)",
    "Not classified": "NC",
    "Gearbox": "DNF (Gearbox)",
    "Engine": "DNF (Engine)",
    "Transmission": "DNF (Transmission)",
    "Electrical": "DNF (Electrical)",
    "Out of fuel": "DNF (Fuel)",
    "Oil leak": "DNF (Oil)",
    "Brakes": "DNF (Brakes)",
    "Suspension": "DNF (Suspension)",
    "Tyre": "DNF (Tyre)",
    "Cooling": "DNF (Cooling)",
    "Did not start": "DNS",
    "Withdrew": "DNS",
    "Injury": "DNS",
    "Illness": "DNS",
    "Disqualified": "DSQ",
    "Oil pressure": "DNF (Oil)",
    "Clutch": "DNF (Clutch)",
    "Supercharger": "DNF (Supercharger)",
    "Hydraulics": "DNF (Hydraulics)"
}

def cowsay(text: str) -> str:
    """
    A simple cowsay.

    Args:
        text (str): Text for the cow to say.

    Returns:
        str: Cow in a code block that says the *text* argument.
    """
    if text is None:
        return
    length = len(text)
    top_bottom =  " " + "_" * (length + 2)
    bubble_text = f"< {text} >"
    cow = fr"""
```
{top_bottom}
{bubble_text}
 {('-' * (length + 2))}
        \   ^__^
         \  (oo)\_______
            (__)\       )\\/\\
                ||----w |
                ||     ||
```
    """
    return cow
