import asyncio
from enum import Enum

import rich


class LogType(Enum):
    LOG = 0
    WARN = 1
    ERROR = 2


def log(content: str, log_type: LogType = None):
    asyncio.run(_log(content, log_type))


async def _log(content: str, log_type: LogType = None):
    match log_type:
        case LogType.LOG:
            rich.print("[bold blue][LOG] [/bold blue]" + content)
        case LogType.WARN:
            rich.print("[bold yellow][WARN] [/bold yellow]" + content)
        case LogType.ERROR:
            rich.print("[bold red][ERROR] [/bold red]" + content)
        case _:
            rich.print("[bold blue][LOG] [/bold blue]" + content)
