import multiprocessing
from typing import Callable

TIMEOUT=5

def run_until(seconds: int, func: Callable, *args) -> None:
    with multiprocessing.Pool(processes=5) as pool:
        result = pool.apply_async(func, args)
        try:
            return result.get(timeout=seconds)
        except multiprocessing.TimeoutError:
            raise Exception(f"Ouch, more than {seconds} seconds...")

def slightly_safer_eval(command, globals, locals):
    code = compile(command, "<string>", "eval")
    for name in code.co_names:
        if "_" in name:
            raise NameError(f"Haha, nice try. è_é")
    return run_until(TIMEOUT, eval, [code, globals, locals])