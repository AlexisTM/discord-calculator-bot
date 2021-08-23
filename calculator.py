#!/usr/bin/env python3
import os
import discord
import numpy as np
from matplotlib import pyplot as plt
import io
import number_sub

# https://discord.com/api/oauth2/authorize?client_id=863044673849655306&permissions=257698359360&scope=bot

from math import (
    acos,
    asin,
    atan,
    atan2,
    ceil,
    cos,
    cosh,
    degrees,
    e,
    exp,
    fabs,
    floor,
    fmod,
    frexp,
    hypot,
    ldexp,
    log,
    log10,
    modf,
    pi,
    pow,
    radians,
    sin,
    sinh,
    sqrt,
    tan,
    tanh,
)

DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")

SAFE_MATH_COMMANDS = [
    "acos",
    "asin",
    "atan",
    "atan2",
    "ceil",
    "cos",
    "cosh",
    "degrees",
    "e",
    "exp",
    "fabs",
    "floor",
    "fmod",
    "frexp",
    "hypot",
    "ldexp",
    "log",
    "log10",
    "modf",
    "pi",
    "pow",
    "radians",
    "sin",
    "sinh",
    "sqrt",
    "tan",
    "tanh",
]

SAFE_COMMAND_DICT = {}
for k in SAFE_MATH_COMMANDS:
    SAFE_COMMAND_DICT[k] = locals().get(k)

EXTRA_SAFE_BUILTINS = [
    "int",
    "float",
    "bool",
    "str",
    "ord",
    "abs",
    "all",
    "any",
    "ascii",
    "bin",
    "bytearray",
    "bytes",
    "chr",
    "complex",
    "dict",
    "set",
    "divmod",
    "enumerate",
    "filter",
    "format",
    "hash",
    "hex",
    "id",
    "iter",
    "len",
    "list",
    "map",
    "max",
    "min",
    "next",
    "print",
    "oct",
    "pow",
    "repr",
    "reversed",
    "round",
    "slice",
    "sorted",
    "sum",
    "tuple",
    "type",
    "zip"
]

GLOBAL_BUILTINS_DICT = {}
for k in EXTRA_SAFE_BUILTINS:
    GLOBAL_BUILTINS_DICT[k] = __builtins__.__dict__.get(k)

STEPS = np.arange(-10, 10, 0.01)

class MyClient(discord.Client):
    COMMAND_CALC = "calc "
    COMMAND_EXEC = ">> "
    COMMAND_HEY = "calc"
    COMMAND_GRAPH = "graph "

    async def on_ready(self):
        print("Logged on as {0}!".format(self.user))

    async def on_message(self, message):
        data = message.content
        try:
            data = number_sub.convert(data)
        except Exception as e:
            print("Failed to convert 1k1 types")
        if data.lower().startswith(self.COMMAND_CALC):
            data = data.lower()
            data = data[len(self.COMMAND_CALC) :]
            try:
                result = eval(data, {"__builtins__": GLOBAL_BUILTINS_DICT}, SAFE_COMMAND_DICT)
                await message.channel.send(result)
            except Exception as e:
                await message.channel.send("Couldn't understand your stuff: " + str(e))

        if data.lower().startswith(self.COMMAND_EXEC):
            data = data[len(self.COMMAND_EXEC) :]
            try:
                result = eval(data, {"__builtins__": GLOBAL_BUILTINS_DICT}, SAFE_COMMAND_DICT)
                await message.channel.send(result)
            except Exception as e:
                await message.channel.send("Couldn't understand your stuff: " + str(e))

        elif data.lower().startswith(self.COMMAND_HEY):
            await message.channel.send(
                "Hello! <3 I am Calcy and I'm soooo goood at math.\nCall me with calc to solve basic equations: calc 1+1\nCall me with graph to solve equations such as: graph x + 1."
            )

        elif data.lower().startswith(self.COMMAND_GRAPH):
            data = data[len(self.COMMAND_GRAPH) :]
            data = data.lower()
            results_x = []
            results_y = []
            try:
                for x in STEPS:
                    SAFE_COMMAND_DICT["x"] = x
                    results_x.append(x)
                    results_y.append(
                        eval(data, {"__builtins__": GLOBAL_BUILTINS_DICT}, SAFE_COMMAND_DICT)
                    )
                # image = plt.figimage()
                plt.figure()
                plt.plot(results_x, results_y)
                plt.title("y = " + data)
                plt.xlabel("x")
                plt.ylabel("y")
                plt.grid(True)
                buf = io.BytesIO()
                plt.savefig(buf, format="png")
                buf.seek(0)
                file = discord.File(buf, filename="graph.png")
                await message.channel.send("Here it is <3", file=file)

            except Exception as e:
                await message.channel.send("Couldn't understand your stuff: " + str(e))


if __name__ == "__main__":
    # Rights: 34880
    intents = discord.Intents.default()
    intents.typing = False
    intents.presences = False
    intents.messages = True
    intents.guilds = True
    intents.reactions = True
    client = MyClient(intents=intents)
    client.run(DISCORD_BOT_TOKEN)
