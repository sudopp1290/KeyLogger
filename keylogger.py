from pynput import mouse, keyboard
import threading
import time

# Latest mouse position
last_move_x = 0
last_move_y = 0

# Latest scroll position
last_scroll_x = 0
last_scroll_y = 0

# Flags and timers
moving = False
move_start_time = 0

scrolling = False
scroll_start_time = 0


# ---------------- Mouse Movement ----------------
def mon_move(x, y):
    global last_move_x, last_move_y
    global moving, move_start_time

    last_move_x = x
    last_move_y = y

    # Restart the timer every time the mouse moves
    moving = True
    move_start_time = time.time()


def print_last_move():
    global moving

    while True:
        if moving and (time.time() - move_start_time >= 1):
            print(f"Last Mouse Position: ({last_move_x}, {last_move_y})")
            moving = False

        time.sleep(0.05)


# ---------------- Mouse Clicks ----------------
def mon_click(x, y, button, pressed):
    if pressed:
        print(f"{button} pressed at ({x}, {y})")
    else:
        print(f"{button} released at ({x}, {y})")


# ---------------- Mouse Scroll ----------------
def mon_scroll(x, y, dx, dy):
    global last_scroll_x, last_scroll_y
    global scrolling, scroll_start_time

    last_scroll_x = x
    last_scroll_y = y

    # Restart the timer every time the wheel scrolls
    scrolling = True
    scroll_start_time = time.time()


def print_last_scroll():
    global scrolling

    while True:
        if scrolling and (time.time() - scroll_start_time >= 1):
            print(f"Last Scroll Position: ({last_scroll_x}, {last_scroll_y})")
            scrolling = False

        time.sleep(0.05)


# ---------------- Keyboard ----------------
def kon_press(key):
    print(f"{key} pressed")


def kon_release(key):
    print(f"{key} released")


# Create listeners
keyboard_listener = keyboard.Listener(
    on_press=kon_press,
    on_release=kon_release
)

mouse_listener = mouse.Listener(
    on_move=mon_move,
    on_click=mon_click,
    on_scroll=mon_scroll
)

# Start background threads
threading.Thread(target=print_last_move, daemon=True).start()
threading.Thread(target=print_last_scroll, daemon=True).start()

# Start listeners
keyboard_listener.start()
mouse_listener.start()

# Keep program running
keyboard_listener.join()
