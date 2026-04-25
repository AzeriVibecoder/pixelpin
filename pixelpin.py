import tkinter as tk
from pynput import mouse, keyboard

BANNER = r"""
  ██████╗ ██╗██╗  ██╗███████╗██╗     ██████╗ ██╗███╗   ██╗
  ██╔══██╗██║╚██╗██╔╝██╔════╝██║     ██╔══██╗██║████╗  ██║
  ██████╔╝██║ ╚███╔╝ █████╗  ██║     ██████╔╝██║██╔██╗ ██║
  ██╔═══╝ ██║ ██╔██╗ ██╔══╝  ██║     ██╔═══╝ ██║██║╚██╗██║
  ██║     ██║██╔╝ ██╗███████╗███████╗██║     ██║██║ ╚████║
  ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═══╝
"""

MENU = """  ┌─────────────────────────────────────────────┐
  │   move mouse    →   live coordinates        │
  │   right-click   →   copy to clipboard       │
  │   esc / middle  →   quit                    │
  └─────────────────────────────────────────────┘
"""


class CoordPicker:
    def __init__(self):
        self.mx = 0
        self.my = 0
        self._running = True

        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.90)
        self.root.config(bg="#0a0a0a", highlightbackground="#00ff88", highlightthickness=1)

        self.label = tk.Label(
            self.root,
            text="0, 0",
            bg="#0a0a0a",
            fg="#00ff88",
            font=("Consolas", 12, "bold"),
            padx=8,
            pady=4,
            bd=0,
        )
        self.label.pack()

        self.mouse_listener = mouse.Listener(
            on_move=self._on_move,
            on_click=self._on_click,
        )
        self.mouse_listener.start()

        self.keyboard_listener = keyboard.Listener(on_press=self._on_key)
        self.keyboard_listener.start()

        self.root.after(10, self._tick)
        self.root.mainloop()

    def _on_move(self, x, y):
        self.mx = x
        self.my = y

    def _on_click(self, x, y, button, pressed):
        if not pressed:
            return
        if button == mouse.Button.right:
            coords = f"{x}, {y}"
            self.root.after(0, lambda: self._copy_and_flash(coords))
        elif button == mouse.Button.middle:
            self.root.after(0, self._quit)

    def _on_key(self, key):
        if key == keyboard.Key.esc:
            self.root.after(0, self._quit)

    def _tick(self):
        if not self._running:
            return
        x, y = self.mx, self.my

        if self.label.cget("fg") == "#00ff88":
            self.label.config(text=f"{x},  {y}")

        win_x = x + 14
        win_y = y - 36
        screen_w = self.root.winfo_screenwidth()
        win_w = self.label.winfo_reqwidth() + 16
        if win_x + win_w > screen_w:
            win_x = x - win_w - 6
        if win_y < 0:
            win_y = y + 20

        self.root.geometry(f"+{win_x}+{win_y}")
        self.root.after(10, self._tick)

    def _copy_and_flash(self, coords: str):
        self.root.clipboard_clear()
        self.root.clipboard_append(coords)
        self.root.update()

        self.label.config(text=f"✓  {coords}", fg="#ffff00", bg="#1a3a1a")
        self.root.config(highlightbackground="#ffff00")
        self.root.after(700, self._reset_label)

    def _reset_label(self):
        self.label.config(fg="#00ff88", bg="#0a0a0a")
        self.root.config(highlightbackground="#00ff88")

    def _quit(self):
        self._running = False
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
        self.root.destroy()


if __name__ == "__main__":
    print(BANNER)
    print(MENU)
    CoordPicker()
