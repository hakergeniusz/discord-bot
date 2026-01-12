import aiohttp
from core.config import status_map


async def race_result(season: int, roundnumber: int, emojis: bool = True) -> list:
    """Gives the result of an F1 race session using Jolpica API.

    Args:
        season (int)
        roundnumber (int): Race number in F1 calendar to check.
        emojis (bool): Default is True, if False, emojis for first three positions will not be given.

    Returns:
        str: Circuit's name.
        list: A list with session results.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.jolpi.ca/ergast/f1/{season}/{roundnumber}/results/') as response:
            if response.status in range(400, 499):
                return None, []

            response = await response.json()
            response = response['MRData']['RaceTable']['Races']
            if response == []:
                return None, []
            circuit_name = response[0]['raceName']
            results = []
            for result in response[0]['Results']:
                POS = result['position']
                if emojis:
                    if POS == '1':
                        POS = '🥇'
                    elif POS == '2':
                        POS = '🥈'
                    elif POS == '3':
                        POS = '🥉'
                    else:
                        POS = f'{POS}.'
                else:
                    POS = f'{POS}.'
                DriverName = result['Driver']['givenName'] + ' ' + result['Driver']['familyName']
                TEAM = result['Constructor']['name']
                status = result['status']
                status = status_map.get(status, status)
                if status == 'Finished':
                    results.append(f'{POS} {DriverName} ({TEAM})')
                else:
                    results.append(f'{POS} {DriverName} ({TEAM}) - {status}')

            return circuit_name, results
