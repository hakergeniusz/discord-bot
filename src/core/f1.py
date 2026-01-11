import asyncio
import fastf1


async def find_circuit(season: int, roundnumber: int) -> str:
    """
    Finds an F1 circuit name.

    Args:
        season (int): Season where the race was.
        roundnumber (int): Round number of the race to return the name.

    Returns:
        str: Circuit's name if it existed.
        bool: None, if circuit not found.
    """
    schedule = await asyncio.to_thread(fastf1.get_event_schedule, season)
    row = schedule.loc[schedule['RoundNumber'] == roundnumber]

    if not row.empty:
        event_name = row.iloc[0]['EventName']
        return f"{event_name}"
    else:
        return None


async def does_exist(season: int, roundnumber: int) -> bool:
    """Checks did an F1 race historically exist or not.

    Args:
        season (int)
        roundnumber (int): Race number in F1 calendar to check.

    Returns:
        bool: True if existed, None if it did not exist.
    """
    schedule = await asyncio.to_thread(fastf1.get_event_schedule, season)
    event_row = schedule.loc[schedule['RoundNumber'] == roundnumber]
    if event_row.empty:
        return None
    else:
        return True
