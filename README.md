# discord-calculator-bot
This is a discord bot that allows you to quickly calculate and graph math.

## Start the bot

```bash
export DISCORD_BOT_TOKEN="Your token"

python3 /home/alarm/calculator.py
```

## Usage

**calc**

The calc command is used for quick maths with most Python math functions available and floats are handled as Decimals:

```bash
calc 0.1 + 0.2 # exact decimals
> 0.3
- calc 12**23 # large integers
> 6624737266949237011120128
calc 1 | 2 # bitwize operations
> 6624737266949237011120128
calc sqrt(abs(sin(pi*e))) # python's math functions
> 0.8797401237108087
```

**graph**

The graph command uses pyplot to graph one or multiple functions.
The functions will be of the type: y = x where you only write the right side of it.

```bash
graph x
> graphs the function y = x
graph [x, -x]
> graphs the functions y = x and y = -x
```

**>>**

This is a basic python execution, but you do not have access to loops.
Yet, you can execute all string operators and use map, reduce, filter functions.

```bash
>> "hello".upper()
> HELLO
>> list(map(ord, "hello"))
> [104, 101, 108, 108, 111]
```

**conic**

Graphs a 2D conic of type y\*\*2 + x\*\*2 = 1.
Due to limitations, you have to move all arguments on one side to make it = 0.

```bash
conic x**2 + y**2 - 3**2
> makes a circle of radius 3 (x² + y² = 3²)
conic (x**2 + y**2 -1)**3 - x**2 * y**3
> Surprise!
```
