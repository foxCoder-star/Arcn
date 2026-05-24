import os
import urllib.parse
import threading
import datetime


# -------------------------
# TIMER STATE
# -------------------------
_timer_thread = None
_timer_cancel = threading.Event()


# -------------------------
# WEBSITE TOOLS
# -------------------------

def open_youtube(entities: dict = {}):
    os.system("open -a 'Google Chrome' 'https://youtube.com'")

def open_google(entities: dict = {}):
    os.system("open -a 'Google Chrome'")

def open_chatgpt(entities: dict = {}):
    os.system("open -a 'Google Chrome' 'https://chatgpt.com'")


# -------------------------
# APP TOOLS
# -------------------------

def open_terminal(entities: dict = {}):
    os.system("open -a Terminal")

def open_notes(entities: dict = {}):
    os.system("open -a Notes")

def open_finder(entities: dict = {}):
    os.system("open -a Finder")

def open_settings(entities: dict = {}):
    os.system("open -a 'System Settings'")

def open_vscode(entities: dict = {}):
    os.system("open -a 'Visual Studio Code'")


# -------------------------
# CONTROL TOOLS
# -------------------------

def close_app(entities: dict = {}):
    os.system(
        "osascript -e 'tell application \"System Events\" to keystroke \"q\" using command down'"
    )

def increase_volume(entities: dict = {}):
    os.system(
        "osascript -e \"set volume output volume ((output volume of (get volume settings)) + 10)\""
    )

def decrease_volume(entities: dict = {}):
    os.system(
        "osascript -e \"set volume output volume ((output volume of (get volume settings)) - 10)\""
    )

def mute_volume(entities: dict = {}):
    os.system(
        "osascript -e \"set volume with output muted\""
    )

def lock_mac(entities: dict = {}):
    os.system(
        "/System/Library/CoreServices/Menu\\ Extras/User.menu/Contents/Resources/CGSession -suspend"
    )

def increase_brightness(entities: dict = {}):
    os.system(
        "osascript -e 'tell application \"System Events\" to key code 144'"
    )

def decrease_brightness(entities: dict = {}):
    os.system(
        "osascript -e 'tell application \"System Events\" to key code 145'"
    )


# -------------------------
# SEARCH TOOLS
# -------------------------

def search_youtube(entities: dict = {}):
    query = entities.get("query", "")
    encoded = urllib.parse.quote(query)
    os.system(
        f"open -a 'Google Chrome' 'https://www.youtube.com/results?search_query={encoded}'"
    )

def search_google(entities: dict = {}):
    query = entities.get("query", "")
    encoded = urllib.parse.quote(query)
    os.system(
        f"open -a 'Google Chrome' 'https://www.google.com/search?q={encoded}'"
    )


# -------------------------
# TIMER TOOLS
# -------------------------

def _parse_duration(entities: dict) -> int:
    """Convert duration entity to seconds."""
    duration = entities.get("duration", "")
    if not duration:
        return 0

    duration = duration.lower()
    parts = duration.split()

    if len(parts) < 2:
        return 0

    try:
        amount = int(parts[0])
    except ValueError:
        return 0

    unit = parts[1]

    if any(u in unit for u in ["s", "sec"]):
        return amount
    elif any(u in unit for u in ["m", "min"]):
        return amount * 60
    elif any(u in unit for u in ["h", "hr", "hour"]):
        return amount * 3600

    return 0


def set_timer(entities: dict = {}):

    global _timer_thread, _timer_cancel

    seconds = _parse_duration(entities)

    if seconds == 0:
        print("TIMER: Couldn't parse duration")
        return

    # Cancel any existing timer
    _timer_cancel.set()
    _timer_cancel = threading.Event()

    def countdown():
        print(f"TIMER: Started for {seconds} seconds")
        cancelled = _timer_cancel.wait(timeout=seconds)
        if not cancelled:
            print("TIMER: Time is up!")
            os.system("osascript -e 'display notification \"Timer is up!\" with title \"Arcn\"'")

    _timer_thread = threading.Thread(target=countdown, daemon=True)
    _timer_thread.start()


def cancel_timer(entities: dict = {}):
    global _timer_cancel
    _timer_cancel.set()
    print("TIMER: Cancelled")


# -------------------------
# TIME + DATE
# -------------------------

def tell_time(entities: dict = {}):
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M %p")
    print(f"TIME: {time_str}")
    return time_str

def tell_date(entities: dict = {}):
    now = datetime.datetime.now()
    date_str = now.strftime("%A, %B %d %Y")
    print(f"DATE: {date_str}")
    return date_str


# -------------------------
# NOTES
# -------------------------

def take_note(entities: dict = {}):
    topic = entities.get("topic", "")
    if not topic:
        print("NOTE: Nothing to save")
        return

    notes_file = os.path.expanduser("~/Arcn/notes.txt")
    timestamp  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    with open(notes_file, "a") as f:
        f.write(f"[{timestamp}] {topic}\n")

    print(f"NOTE: Saved — {topic}")


# -------------------------
# GREET + PERSONALITY
# -------------------------

def greet(entities: dict = {}):
    hour = datetime.datetime.now().hour
    if hour < 12:
        print("ARCN: Good morning.")
    elif hour < 17:
        print("ARCN: Good afternoon.")
    else:
        print("ARCN: Good evening.")

def how_are_you(entities: dict = {}):
    print("ARCN: All systems running. How can I help?")

def stop_cancel(entities: dict = {}):
    print("ARCN: Understood, cancelling.")
    cancel_timer()


# -------------------------
# MODES
# -------------------------

def developer_mode(entities: dict = {}):
    os.system("open -a 'Visual Studio Code'")
    os.system("open -a Terminal")

def study_mode(entities: dict = {}):
    os.system("open -a Notes")
    os.system("open -a 'Google Chrome'")


# -------------------------
# PLACEHOLDERS
# (real implementations coming)
# -------------------------

def play_music(entities: dict = {}):
    print("ARCN: Music playback coming soon.")

def pause_music(entities: dict = {}):
    print("ARCN: Music playback coming soon.")

def skip_song(entities: dict = {}):
    print("ARCN: Music playback coming soon.")

def get_weather(entities: dict = {}):
    print("ARCN: Weather integration coming soon.")

def send_message(entities: dict = {}):
    print("ARCN: Messaging coming soon.")

def ask_question(entities: dict = {}):
    print("ARCN: Knowledge engine coming soon.")

def create_reminder(entities: dict = {}):
    print("ARCN: Reminders coming soon.")


# -------------------------
# TOOL REGISTRY
# -------------------------

TOOLS = {

    # WEBSITES
    "open_youtube"      : {"function": open_youtube,       "confirmation": "Opening YouTube",            "type": "website"},
    "open_google"       : {"function": open_google,        "confirmation": "Opening Google",             "type": "website"},
    "open_chatgpt"      : {"function": open_chatgpt,       "confirmation": "Opening ChatGPT",            "type": "website"},

    # APPS
    "open_terminal"     : {"function": open_terminal,      "confirmation": "Opening Terminal",           "type": "app"},
    "open_notes"        : {"function": open_notes,         "confirmation": "Opening Notes",              "type": "app"},
    "open_finder"       : {"function": open_finder,        "confirmation": "Opening Finder",             "type": "app"},
    "open_settings"     : {"function": open_settings,      "confirmation": "Opening Settings",           "type": "app"},
    "open_vscode"       : {"function": open_vscode,        "confirmation": "Opening VS Code",            "type": "app"},

    # CONTROLS
    "close_app"         : {"function": close_app,          "confirmation": "Closing current app",        "type": "control"},
    "system_volume_up"  : {"function": increase_volume,    "confirmation": "Increasing volume",          "type": "control"},
    "system_volume_down": {"function": decrease_volume,    "confirmation": "Decreasing volume",          "type": "control"},
    "mute_volume"       : {"function": mute_volume,        "confirmation": "Muting volume",              "type": "control"},
    "lock_mac"          : {"function": lock_mac,           "confirmation": "Locking Mac",                "type": "control"},
    "system_brightness_up"  : {"function": increase_brightness, "confirmation": "Increasing brightness", "type": "control"},
    "system_brightness_down": {"function": decrease_brightness, "confirmation": "Decreasing brightness", "type": "control"},

    # SEARCHES
    "search_google"     : {"function": search_google,      "confirmation": "Searching Google",           "type": "search"},
    "search_youtube"    : {"function": search_youtube,     "confirmation": "Searching YouTube",          "type": "search"},

    # TIMER
    "set_timer"         : {"function": set_timer,          "confirmation": "Timer started",              "type": "timer"},
    "cancel_timer"      : {"function": cancel_timer,       "confirmation": "Timer cancelled",            "type": "timer"},

    # TIME + DATE
    "tell_time"         : {"function": tell_time,          "confirmation": "Checking time",              "type": "info"},
    "tell_date"         : {"function": tell_date,          "confirmation": "Checking date",              "type": "info"},

    # NOTES
    "take_note"         : {"function": take_note,          "confirmation": "Note saved",                 "type": "note"},

    # PERSONALITY
    "greet"             : {"function": greet,              "confirmation": "",                           "type": "personality"},
    "how_are_you"       : {"function": how_are_you,        "confirmation": "",                           "type": "personality"},
    "stop_cancel"       : {"function": stop_cancel,        "confirmation": "Cancelled",                  "type": "control"},

    # MODES
    "developer_mode"    : {"function": developer_mode,     "confirmation": "Entering developer workspace", "type": "mode"},
    "study_mode"        : {"function": study_mode,         "confirmation": "Entering study mode",        "type": "mode"},

    # COMING SOON
    "play_music"        : {"function": play_music,         "confirmation": "",                           "type": "media"},
    "pause_music"       : {"function": pause_music,        "confirmation": "",                           "type": "media"},
    "skip_song"         : {"function": skip_song,          "confirmation": "",                           "type": "media"},
    "get_weather"       : {"function": get_weather,        "confirmation": "",                           "type": "info"},
    "send_message"      : {"function": send_message,       "confirmation": "",                           "type": "message"},
    "ask_question"      : {"function": ask_question,       "confirmation": "",                           "type": "knowledge"},
    "create_reminder"   : {"function": create_reminder,    "confirmation": "",                           "type": "reminder"},
}