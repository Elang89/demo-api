import asyncio
from functools import partial
from typing import Callable


async def run_in_thread(sync_function, *args, **kwargs) -> Callable:  # type: ignore
    loop = asyncio.get_running_loop()
    sync_fn = partial(sync_function, *args, **kwargs)
    return await loop.run_in_executor(None, sync_fn)
