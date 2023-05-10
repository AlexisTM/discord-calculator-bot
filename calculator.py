#!/usr/bin/env python3
import os
import discord
import numpy as np
from matplotlib import pyplot as plt
import io
import number_sub
from safer_eval import slightly_safer_eval, run_until
from float_fix import float_to_decimal

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
    factorial,
)
from decimal import Decimal

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
    "factorial",
    "Decimal",
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
    "zip",
]

GLOBAL_BUILTINS_DICT = {}
for k in EXTRA_SAFE_BUILTINS:
    GLOBAL_BUILTINS_DICT[k] = __builtins__.__dict__.get(k)

STEPS = np.arange(-10, 10, 0.01)

X_CONIC = np.linspace(-10, 10, 500)
Y_CONIC = np.linspace(-10, 10, 500)
X_CONIC, Y_CONIC = np.meshgrid(X_CONIC, Y_CONIC)


class MyClient(discord.Client):
    COMMAND_CALC = "calc "
    COMMAND_EXEC = ">> "
    COMMAND_GRAPH = "graph "
    COMMAND_CONIC = "conic "
    COMMAND_HEY = "calc"

    def get_help(self):
        embed = discord.Embed(title="Calcy help", color=0x26C0EB)
        embed.add_field(
            name="What am I?",
            value="I am Calcy, a 'safe' python execution environment.",
            inline=True,
        )

        embed.add_field(
            name="calc ",
            value="""The calc command is used for quick maths with most Python math functions available and floats are handled as Decimals:

**Examples:**
  - calc 0.1 + 0.2 # exact decimals
    \\> 0.3
  - calc 12\\*\\*23 # large integers
    \\> 6624737266949237011120128
  - calc 1 | 2 # bitwize operations
    \\> 6624737266949237011120128
  - calc sqrt(abs(sin(pi*e))) # python's math functions
    \\> 0.8797401237108087""",
            inline=False,
        )

        embed.add_field(
            name="graph ",
            value="""The graph command uses pyplot to graph one or multiple functions.
The functions will be of the type: `y = x` where you only write the right side of it.

**Examples:**
  - graph x
    \\> graphs the function `y = x`
  - graph [x, -x]
    \\> graphs the functions `y = x` and `y = -x`""",
            inline=False,
        )

        embed.add_field(
            name=">> ",
            value="""This is a basic python execution, but you do not have access to loops.
Yet, you can execute all string operators and use map, reduce, filter functions.

**Examples:**
  - \\>\\> "hello".upper()
    \\> HELLO
  - \\>\\> list(map(ord, "hello"))
    \\> [104, 101, 108, 108, 111]""",
            inline=False,
        )

        embed.add_field(
            name="conic ",
            value="""Graphs a 2D conic of type `y\\*\\*2 + x\\*\\*2 = 1`.
Due to limitations, you have to move all arguments on one side to make it `= 0`.

**Examples:**
  - conic x\\*\\*2 + y\\*\\*2 - 3\\*\\*2
    > makes a circle of radius 3 (x² + y² = 3²)
  - conic (x\\*\\*2 + y\\*\\*2 -1)\\*\\*3 - x\\*\\*2 * y\\*\\*3
    > Surprise!""",
            inline=False,
        )
        return embed

    async def on_ready(self):
        print("Logged on as {0}!".format(self.user))

    async def on_message(self, message):
        data = message.content
        try:
            data = number_sub.convert(data)
        except Exception as e:
            print("Failed to convert 1k1 types")
        if data.lower().startswith(self.COMMAND_CALC):
            data = data[len(self.COMMAND_CALC) :]
            data = float_to_decimal(data)
            try:
                result = run_until(5, slightly_safer_eval, 
                    data, {"__builtins__": GLOBAL_BUILTINS_DICT}, SAFE_COMMAND_DICT
                )
                await message.channel.send(result)
            except Exception as e:
                await message.channel.send("Couldn't understand your stuff: " + str(e))

        if data.lower().startswith(self.COMMAND_EXEC):
            data = data[len(self.COMMAND_EXEC) :]
            try:
                result = run_until(5, slightly_safer_eval, 
                    data, {"__builtins__": GLOBAL_BUILTINS_DICT}, SAFE_COMMAND_DICT
                )
                await message.channel.send(result)
            except Exception as e:
                await message.channel.send("Couldn't understand your stuff: " + str(e))

        elif data.lower().startswith(self.COMMAND_GRAPH):
            data = data[len(self.COMMAND_GRAPH) :]
            results_x = []
            results_y = []
            try:
                for x in STEPS:
                    SAFE_COMMAND_DICT["x"] = x
                    results_x.append(x)
                    results_y.append(
                        run_until(5, slightly_safer_eval, 
                            data,
                            {"__builtins__": GLOBAL_BUILTINS_DICT},
                            SAFE_COMMAND_DICT,
                        )
                    )

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

        elif data.lower().startswith(self.COMMAND_CONIC):
            data = data[len(self.COMMAND_CONIC) :]
            results_x = []
            results_y = []
            try:
                SAFE_COMMAND_DICT["x"] = X_CONIC
                SAFE_COMMAND_DICT["y"] = Y_CONIC
                result = run_until(5, slightly_safer_eval,
                    data, {"__builtins__": GLOBAL_BUILTINS_DICT}, SAFE_COMMAND_DICT
                )
                plt.figure()
                plt.contour(X_CONIC, Y_CONIC, result, [0])
                plt.title(data + " = 0")
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

        elif data.lower().startswith(self.COMMAND_HEY):
            await message.channel.send(embed=self.get_help())


if __name__ == "__main__":
    # Rights: 34880
    intents = discord.Intents.default()
    intents.typing = False
    intents.presences = False
    intents.messages = True
    intents.message_content=True
    intents.guilds = True
    intents.reactions = True
    ## Make sure to enable INTENT in discord dev portal
    client = MyClient(intents=intents)
    client.run(DISCORD_BOT_TOKEN)
