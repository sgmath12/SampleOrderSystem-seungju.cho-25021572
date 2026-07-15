RESET = "\033[0m"

STATUS_COLORS = {
    "RESERVED": "\033[94m",   # blue
    "CONFIRMED": "\033[92m",  # green
    "PRODUCING": "\033[93m",  # yellow
    "REJECTED": "\033[91m",   # red
    "RELEASE": "\033[95m",    # magenta
    "여유": "\033[92m",
    "부족": "\033[93m",
    "고갈": "\033[91m",
}


RAINBOW = [
    "\033[91m",  # red
    "\033[93m",  # yellow
    "\033[92m",  # green
    "\033[96m",  # cyan
    "\033[94m",  # blue
    "\033[95m",  # magenta
]


def colorize(text, color_code):
    return f"{color_code}{text}{RESET}"


def rainbow_lines(text):
    lines = text.split("\n")
    return "\n".join(colorize(line, RAINBOW[i % len(RAINBOW)]) for i, line in enumerate(lines))


def badge(status):
    color_code = STATUS_COLORS.get(status)
    return colorize(status, color_code) if color_code else status


def pad_badge(status, width):
    colored = badge(status)
    padding = " " * max(0, width - len(str(status)))
    return colored + padding
