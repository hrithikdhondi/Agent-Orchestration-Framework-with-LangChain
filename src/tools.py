
import requests
from langchain_core.tools import tool
import ast
import math
import secrets
import string
from datetime import datetime, timezone, timedelta
import functools
import json
import os
import time
import re
from pathlib import Path
from typing import List


# Milestone 2
def log_tool(tool_name: str):
    """
    Decorator that prints Thought/Action/Action Input/Observation blocks
    when the tool is executed. Keeps the original function behavior.
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            # Thought: ideally produced by the agent; we produce a helpful hint
            print("\n# Thought: I should use the", tool_name, "tool.")
            print("# Action:", tool_name)

            # Format the action input (args/kwargs) nicely
            try:
                if kwargs and args:
                    action_input = {"args": args, "kwargs": kwargs}
                elif kwargs:
                    action_input = kwargs
                else:
                    # if single arg, print it plainly
                    action_input = args[0] if len(args) == 1 else args
                action_input_str = json.dumps(action_input, default=str)
            except Exception:
                action_input_str = str(action_input)

            print("# Action Input:", action_input_str)

            # Execute tool and capture the result
            start = time.time()
            result = fn(*args, **kwargs)
            duration = time.time() - start

            # Observation: show tool output
            # Keep it one-line if it's long
            obs = result
            if isinstance(obs, str) and "\n" in obs:
                obs = obs.splitlines()[0] + " ..."

            print("# Observation:", obs)
            print(f"# (tool runtime: {duration:.3f}s)\n")

            return result
        return wrapper
    return decorator


# WEEK - 2 upgrades
@tool
@log_tool("greet")
def greet(name: str) -> str:
    """Greet a person by name. Input should be the person's name."""
    name = name.strip()
    if not name:
        return "Hello! I couldn't find a name to greet."
    return f"Hello {name}, I am your LangChain Agent powered by Gemini!"


@tool
@log_tool("get_weather")
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
@log_tool("calculate")
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
@log_tool("gen_password")
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
@log_tool("get_time")
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

# added other tools in Milestone 2
@tool
@log_tool("read_file")
def read_file(path: str) -> str:
    """
    Safely read and return the content of a file.
    Supports text-based formats: .txt, .md, .json, .py, etc.
    Usage: read_file "notes.txt"
    """
    if not path:
        return "No file path provided."

    # Clean the path to avoid security issues
    path = path.strip()

    if not os.path.exists(path):
        return f"File not found: {path}"

    # Prevent reading binary files as text
    allowed_extensions = (".txt", ".md", ".json", ".py", ".log")

    if not path.endswith(allowed_extensions):
        return f"Unsupported file type. Allowed: {allowed_extensions}"

    try:
        # Handle JSON separately for nice formatting
        if path.endswith(".json"):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return json.dumps(data, indent=2)

        # All other text files
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

            # Avoid flooding output
            if len(content) > 1500:
                return content[:1500] + "\n\n... (truncated)"
            
            return content

    except Exception as e:
        return f"Error reading file: {e}"


@tool
@log_tool("write_file")
def write_file(path: str, content: str, overwrite: bool = False) -> str:
    """
    Write content to a text file.
    - If overwrite=False and file exists -> returns a safe message (no write).
    - If overwrite=True -> replaces file contents.
    Allowed extensions: .txt, .md, .json, .log, .py
    """
    try:
        if not path or content is None:
            return "Usage: write_file(path, content, overwrite=False)"

        # Normalize and restrict to prevent directory traversal outside project
        base = Path(".").resolve()
        target = (base / Path(path)).resolve()
        if not str(target).startswith(str(base)):
            return "Security error: path outside allowed directory."

        allowed = {".txt", ".md", ".json", ".log", ".py"}
        if target.suffix not in allowed:
            return f"Unsupported file extension {target.suffix}. Allowed: {allowed}"

        if target.exists() and not overwrite:
            return f"File already exists: {path}. Use overwrite=True to replace."

        # Ensure parent dirs exist
        target.parent.mkdir(parents=True, exist_ok=True)

        # Write file
        mode = "w"  # overwrite
        with open(target, mode, encoding="utf-8") as f:
            f.write(content)

        return f"Wrote file: {path}"
    except Exception as e:
        return f"Write error: {e}"


@tool
@log_tool("append_file")
def append_file(path: str, content: str) -> str:
    """
    Append content to a text file. Creates file if it doesn't exist.
    """
    try:
        if not path or content is None:
            return "Usage: append_file(path, content)"

        base = Path(".").resolve()
        target = (base / Path(path)).resolve()
        if not str(target).startswith(str(base)):
            return "Security error: path outside allowed directory."

        allowed = {".txt", ".md", ".json", ".log", ".py"}
        if target.suffix not in allowed:
            return f"Unsupported file extension {target.suffix}. Allowed: {allowed}"

        target.parent.mkdir(parents=True, exist_ok=True)

        with open(target, "a", encoding="utf-8") as f:
            f.write(content)

        return f"Appended to file: {path}"
    except Exception as e:
        return f"Append error: {e}"

#Milestone 3 upgrades

#Text Analyzer Tool
@tool
def analyze_text(text: str) -> str:
    """
    Analyze text and extract key points.
    Useful for research analysis before summarization.
    """
    if not text:
        return "No text provided."

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Pick top sentences as key points (simple heuristic)
    key_points = sentences[:5]

    result = {
        "key_points": key_points,
        "sentence_count": len(sentences)
    }

    return json.dumps(result, indent=2)

#Keyword Extractor Tool
@tool
def extract_keywords(text: str, top_k: int = 5) -> str:
    """
    Extract important keywords from text.
    """
    if not text:
        return "No text provided."

    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    freq = {}

    for w in words:
        freq[w] = freq.get(w, 0) + 1

    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    keywords = [w for w, _ in sorted_words[:top_k]]

    return json.dumps({"keywords": keywords}, indent=2)

#Task Decomposer Tool
@tool
def decompose_task(goal: str) -> str:
    """
    Break a goal into structured subtasks.
    """
    if not goal:
        return "No goal provided."

    subtasks = [
        f"Understand the goal: {goal}",
        "Identify required information",
        "Collect data if needed",
        "Organize findings",
        "Prepare final output"
    ]

    return json.dumps(
        {"goal": goal, "subtasks": subtasks},
        indent=2
    )

#Agent Logger / Trace Tool
@tool
def log_agent_step(agent_name: str, action: str) -> str:
    """
    Log what an agent is doing at a specific step.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = {
        "agent": agent_name,
        "action": action,
        "time": timestamp
    }

    print(f"[AGENT LOG] {log_entry}")

    return "Agent step logged successfully."

#Shared Memory Search Tool
@tool
def search_shared_memory(query: str, memory_context: str) -> str:
    """
    Search shared memory context for relevant information.
    (Context is passed from orchestrator)
    """
    if not query:
        return "No query provided."

    if not memory_context:
        return "Shared memory is empty."

    # Simple relevance check
    matches = []
    for line in memory_context.split("\n"):
        if query.lower() in line.lower():
            matches.append(line)

    if not matches:
        return "No relevant memory found."

    return json.dumps(
        {"relevant_memory": matches[:3]},
        indent=2
    )

#Shared Memory Save
@tool
def prepare_memory_entry(content: str, tag: str = "general") -> str:
    """
    Prepare a structured memory entry to store in shared memory.
    """
    if not content:
        return "No content to save."

    entry = {
        "tag": tag,
        "content": content,
        "saved_at": datetime.now().isoformat()
    }

    return json.dumps(entry, indent=2)

#JSON Structurer Tool
@tool
def structure_as_json(title: str, points: List[str]) -> str:
    """
    Convert text points into structured JSON.
    """
    if not title or not points:
        return "Title or points missing."

    structured = {
        "title": title,
        "items": points
    }

    return json.dumps(structured, indent=2)

#Table Generator Tool
@tool
def generate_markdown_table(headers: List[str], rows: List[List[str]]) -> str:
    """
    Generate a markdown table from headers and rows.
    """
    if not headers or not rows:
        return "Headers or rows missing."

    table = "| " + " | ".join(headers) + " |\n"
    table += "| " + " | ".join(["---"] * len(headers)) + " |\n"

    for row in rows:
        table += "| " + " | ".join(row) + " |\n"

    return table

def get_tools():
    """Return a list of tool functions decorated with @tool."""
    return [
        # Milestone 2 tools
        greet,
        get_weather,
        calculate,
        gen_password,
        get_time,
        read_file,
        write_file,
        append_file,

        # Milestone 3 tools
        analyze_text,
        extract_keywords,
        decompose_task,
        log_agent_step,
        search_shared_memory,
        prepare_memory_entry,
        structure_as_json,
        generate_markdown_table,
    ]

