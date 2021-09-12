def slightly_safer_eval(command, globals, locals):
    code = compile(command, "<string>", "eval")
    for name in code.co_names:
        if "_" in name:
            raise NameError(f"Haha, nice try. è_é")
    return eval(code, globals, locals)
