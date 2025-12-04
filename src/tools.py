
import requests
from langchain_core.tools import tool
import ast
import math
import secrets
import string
from datetime import datetime, timezone, timedelta


# WEEK - 2 upgrades
@tool
def greet(name: str) -> str:
    """Greet a person by name. Input should be the person's name."""
    name = name.strip()
    if not name:
        return "Hello! I couldn't find a name to greet."
    return f"Hello {name}, I am your LangChain Agent powered by Gemini!"


@tool
def get_weather(city: str) -> str:
    """Get current temperature of a city. Input should be the city name."""
    city = city.strip() or ""
    if not city:
        return "Please provide a city name."

    try:
        url = f"https://wttr.in/{city}?format=j1"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        current = data.get("current_condition", [])
        if not current:
            return f"Could not read weather for {city}."
        temp_c = current[0].get("temp_C")
        area = data.get("nearest_area", [{}])[0].get("areaName", [{}])[0].get("value", city)
        return f"Current temperature in {area} is {temp_c}°C"
    except requests.RequestException as e:
        return f"Weather API error: {e}"
    except Exception as e:
        return f"Unexpected error while fetching weather: {e}"

@tool
def calculate(expression: str) -> str:
    """
    Safely evaluate a math expression and return the result.
    Supports +, -, *, /, **, %, parentheses, and math module funcs (sin, cos, sqrt...).
    Example: "calculate 12*(3+4) - sqrt(16)"
    """
    if not expression:
        return "No expression provided."

    # allow math functions and constants
    allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
    # allow built-in names we consider safe
    allowed_names.update({"abs": abs, "round": round})

    try:
        # parse the expression into an AST and evaluate only safe nodes
        node = ast.parse(expression, mode="eval")

        class SafeEval(ast.NodeVisitor):
            SAFE_NODES = (
                ast.Expression, ast.BinOp, ast.UnaryOp, ast.Call,
                ast.Name, ast.Load, ast.Constant, ast.Pow, ast.Sub, ast.Add,
                ast.Mult, ast.Div, ast.Mod, ast.UAdd, ast.USub, ast.Tuple,
                ast.List, ast.Tuple, ast.Expr, ast.Attribute, ast.Subscript,
                ast.Index, ast.Slice, ast.ListComp
            )

            def visit(self, node):
                if not isinstance(node, self.SAFE_NODES):
                    raise ValueError(f"Unsafe expression: {type(node).__name__}")
                return super().visit(node)

        SafeEval().visit(node)
        result = eval(compile(node, filename="<ast>", mode="eval"), {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"Calculator error: {e}"


# --- Password generator tool ---
@tool
def gen_password(length: int = 16, require_symbols: bool = True) -> str:
    """
    Generate a secure password. Returns the password (not stored).
    Example: 'gen_password 20' or 'gen_password length=12 require_symbols=False'
    """
    try:
        length = int(length)
        if length < 6 or length > 128:
            return "Password length must be between 6 and 128."

        alphabet = string.ascii_letters + string.digits
        if require_symbols:
            alphabet += string.punctuation

        # use secrets.choice for cryptographic randomness
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password
    except Exception as e:
        return f"Password generator error: {e}"

# --- Time / date tool ---
@tool
def get_time(tz: str = "UTC") -> str:
    """
    Return current date/time in 12-hour format with AM/PM.
    Supported tz values: "UTC" (default), "IST"/"INDIA", "LOCAL" (system local time).
    Example returns: "04:43:09 PM" or "04:43:09 PM (IST)"
    """
    try:
        if tz and tz.upper() in ("LOCAL", "LOCALTIME"):
            now = datetime.now().astimezone()  # system local timezone
        else:
            now = datetime.now(timezone.utc)
            if tz and tz.upper() in ("IST", "INDIA"):
                now = now.astimezone(timezone(timedelta(hours=5, minutes=30)))
            # else keep UTC

        # 12-hour format: %I = hour (01..12), %p = AM/PM
        time_str = now.strftime("%I:%M:%S %p")
        # optionally append zone short label
        zone_label = "UTC"
        if tz and tz.upper() in ("IST", "INDIA"):
            zone_label = "IST"
        elif tz and tz.upper().startswith("LOCAL"):
            zone_label = "LOCAL"
        return f"{time_str} ({zone_label})"
    except Exception as e:
        return f"Time tool error: {e}"


def get_tools():
    """Return a list of tool functions decorated with @tool."""
    return [greet, get_weather, calculate, gen_password, get_time]
