def slightly_safer_eval(command, locals):
    code = compile(command, "<string>", "eval")
    print(code.co_names)
    # Step 3
    for name in code.co_names:
        if "_" in name:
            raise NameError(f"Haha, nice try. è_é")
    return eval(code, {"__builtins__": None}, locals)