import json
import os
import tkinter as tk
from tkinter import font

# --- CYBERPUNK PALETTE DESIGN CODES ---
COLOR_BG = "#D6EDFF"  # Frost Blue
COLOR_CYAN = "#0082FD"  # Glowing Neon Primary
COLOR_MUTED = "#253042"  # Inactive Structural Grey
COLOR_HIGHLIGHT = "#6FB8FF"  # Active Selection Row Glow
COLOR_WHITE = "#253042"  # High-Contrast Standard Text
COLOR_ALERT = "#ff0000"  # Emergency Compile / Alarm Red

# Automatically figures out your desktop path whether you are on Mac or Windows
SD_ROOT = os.path.expanduser("~/Desktop/test_book/")
CACHE_FILE = os.path.join(SD_ROOT, ".brain_freeze_cache.json")


class BrainFreezeSandbox:
    def __init__(self, root):
        self.root = root
        print("Brain Freeze Sandbox Starting...")

        # Force full-screen application view and strip vanilla OS windows
        # Testing Mode
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        self.root.configure(bg=COLOR_BG)

        # Appliance Mode (enable later)
        # self.root.attributes('-fullscreen', True)
        # self.root.overrideredirect(True)

        # Build local testing directory if it doesn't exist yet
        if not os.path.exists(SD_ROOT):
            os.makedirs(os.path.join(SD_ROOT, "01_characters"))
            os.makedirs(os.path.join(SD_ROOT, "02_chapter"))
            os.makedirs(os.path.join(SD_ROOT, "03_research"))
            self.create_sample_files()

        # Typography configuration profiles
        self.font_h1 = font.Font(family="Helvetica", size=12, weight="normal")
        self.font_body = font.Font(family="Helvetica", size=11, weight="normal")
        self.font_bold = font.Font(family="Helvetica", size=11, weight="normal")

        # Global Logic Registers
        self.current_dir = SD_ROOT
        self.selected_lines = set()
        self.visible_items = []
        self.folder_history = {}
        self.cursor_index = 0
        self.mode = "menu"  # "menu", "line_browser", or "compiled"

        # Number of rows visible at once
        self.viewport_size = 20

        # Line Extraction Module Registers
        self.current_file_path = ""
        self.file_lines = []
        self.line_cursor = 0

        # Countdown Clock Software Registers
        self.remaining_seconds = 0
        self.timer_active = False

        # --- DEVELOPMENT KEYBOARD BRIDGE ---
        self.root.bind("<Up>", lambda e: self.simulate_hardware_trigger("UP"))
        self.root.bind("<Down>", lambda e: self.simulate_hardware_trigger("DOWN"))
        self.root.bind("<Return>", lambda e: self.simulate_hardware_trigger("SELECT"))
        self.root.bind("<Escape>", lambda e: self.simulate_hardware_trigger("BACK"))
        self.root.bind("<space>", lambda e: self.simulate_hardware_trigger("COMPILE"))
        self.root.bind("s", lambda e: self.simulate_hardware_trigger("TIMER_SET"))
        self.root.bind("x", lambda e: self.simulate_hardware_trigger("TIMER_EXEC"))
        self.root.bind("q", lambda e: self.root.destroy())
        self.root.bind("<F12>", lambda e: self.root.destroy())
        self.root.bind("c", lambda e: self.simulate_hardware_trigger("CLEAR"))

        self.load_session_cache()
        self.refresh_directory()
        self.render_chassis()
        self.start_software_clock_loop()

        print("Brain Freeze Sandbox Ready")

    def create_sample_files(self):
        """Generates mock files inside your Desktop folder to let you test right away."""
        with open(os.path.join(SD_ROOT, "01_characters", "Protagonist.txt"), "w") as f:
            f.write("Eyes: Piercing Slate Blue\nHair: Blonde & Scruffy\nScar: Jagged line across left cheek\n")
        with open(os.path.join(SD_ROOT, "02_chapter", "Hooks.txt"), "w") as f:
            f.write("In Media Res: Open mid-argument\nSensory Drop: Start with loud explosion\n")
        with open(os.path.join(SD_ROOT, "03_research", "Train_Specs.txt"), "w") as f:
            f.write("Brakes: 1890s air systems take 400 yards to stop\nFuel: Consumes 2 tons of coal per hour\n")

    def load_session_cache(self):
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r") as f:
                    self.selected_lines = set(json.load(f))
            except Exception as e:
                print(f"Cache load error: {e}")
                self.selected_lines = set()

    def save_session_cache(self):
        try:
            with open(CACHE_FILE, "w") as f:
                json.dump(list(self.selected_lines), f)
        except Exception as e:
            print(f"Error: {e}")

    def clear_session_state(self):
        """Wipes all extracted freeze-frame selections."""

        self.selected_lines.clear()

        try:
            if os.path.exists(CACHE_FILE):
                os.remove(CACHE_FILE)
        except Exception as e:
            print(f"Cache delete error: {e}")

        self.render_chassis()

        print("Freeze Frame Cleared")

    def refresh_directory(self):
        if hasattr(self, 'current_dir') and hasattr(self, 'cursor_index'):
            self.folder_history[self.current_dir] = self.cursor_index

        self.visible_items = []
        try:
            items = sorted(os.listdir(self.current_dir))
            dirs = [i for i in items if os.path.isdir(os.path.join(self.current_dir, i))]
            files = [i for i in items if
                     os.path.isfile(os.path.join(self.current_dir, i)) and i.endswith(('.txt', '.md'))]

            for d in dirs: self.visible_items.append({"name": d, "is_dir": True})
            for f in files: self.visible_items.append({"name": f, "is_dir": False})
        except Exception as e:
            print(f"Error: {e}")

        self.cursor_index = self.folder_history.get(self.current_dir, 0)

    def render_chassis(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Build that glowing 3px border container
        outer_frame = tk.Frame(self.root, bg=COLOR_CYAN, bd=1)
        outer_frame.pack(fill="both", expand=True, padx=8, pady=8)

        self.canvas = tk.Frame(outer_frame, bg=COLOR_BG)
        self.canvas.pack(fill="both", expand=True, padx=2, pady=2)

        if self.mode == "menu":
            self.list_pane = tk.Frame(self.canvas, bg=COLOR_BG)
            self.list_pane.pack(fill="both", expand=True, padx=15)
            self.repaint_menu_rows()


        elif self.mode == "line_browser":
            self.list_pane = tk.Frame(self.canvas, bg=COLOR_BG)
            self.list_pane.pack(fill="both", expand=True, padx=15)
            self.repaint_line_rows()


        elif self.mode == "compiled":
            grid_system = tk.Frame(self.canvas, bg=COLOR_BG)
            grid_system.pack(fill="both", expand=True, padx=15, pady=15)
            grid_system.grid_columnconfigure((0, 1, 2), weight=1)
            grid_system.grid_rowconfigure(0, weight=1)

            columns_map = [("01_characters", "👤 CHARACTERS"),
                           ("02_chapter", "🎬 SCENE"),
                           ("03_research", "📚 RESEARCH")]

            for idx, (keyword, col_title) in enumerate(columns_map):
                box_glow = tk.Frame(grid_system, bg=COLOR_CYAN, bd=0.5)
                box_glow.grid(row=0, column=idx, sticky="nsew", padx=8, pady=8)

                box_content = tk.Frame(box_glow, bg=COLOR_BG)
                box_content.pack(fill="both", expand=True, padx=2, pady=2)

                tk.Label(box_content, text=col_title, font=self.font_bold, fg=COLOR_CYAN, bg=COLOR_BG).pack(anchor="w",
                                                                                                            padx=15,
                                                                                                            pady=12)

                column_text = ""
                for combined_string in self.selected_lines:
                    if "||" in combined_string:
                        origin_path, line_content = combined_string.split("||", 1)
                        if keyword in origin_path:
                            column_text += f"• {line_content}\n\n"

                txt = tk.Text(box_content, font=self.font_body, fg=COLOR_WHITE, bg=COLOR_BG, wrap="word", bd=0,
                              highlightthickness=0, spacing1=0, spacing3=0)
                txt.insert("1.0", column_text if column_text else "[ NO COGNITIVE ANCHORS LINKED ]\n")
                txt.config(state="disabled")
                txt.pack(fill="both", expand=True, padx=15, pady=5)

    def repaint_menu_rows(self):
        for w in self.list_pane.winfo_children():
            w.destroy()

        # Display folder path marker
        rel_path = self.current_dir.replace(SD_ROOT, "SYS://")
        tk.Label(self.list_pane, text=f"PATH: {rel_path}\n", font=self.font_bold, fg=COLOR_MUTED, bg=COLOR_BG).pack(
            anchor="w")
        tk.Label(
            self.list_pane,
            text=f"ITEM {self.cursor_index + 1}/{len(self.visible_items)}",
            font=self.font_body,
            fg=COLOR_MUTED,
            bg=COLOR_BG
        ).pack(anchor="w")

        start_idx = max(
            0,
            min(
                self.cursor_index - self.viewport_size // 2,
                max(0, len(self.visible_items) - self.viewport_size)
            )
        )

        end_idx = start_idx + self.viewport_size

        for idx in range(start_idx, min(end_idx, len(self.visible_items))):
            item = self.visible_items[idx]

            full_path = os.path.join(self.current_dir, item["name"])
            icon = "📁" if item["is_dir"] else "📄"
            matches = sum(1 for p_line in self.selected_lines if p_line.startswith(full_path))
            tether_label = f" [{matches} EXTRACTED]" if matches > 0 else ""

            is_active = (idx == self.cursor_index)

            lbl = tk.Label(
                self.list_pane,
                text=f"{'> ' if is_active else '  '}{icon} {item['name']}{'/' if item['is_dir'] else ''}{tether_label}",
                font=self.font_body,
                fg=COLOR_CYAN if is_active else (COLOR_WHITE if matches > 0 else COLOR_MUTED),
                bg=COLOR_BG,
                anchor="w",
                padx=15,
                pady=6
            )
            lbl.pack(fill="x")

    def repaint_line_rows(self):
        for w in self.list_pane.winfo_children():
            w.destroy()
        filename = os.path.basename(self.current_file_path)
        tk.Label(self.list_pane, text=f"FILE MODULE: {filename}\n", font=self.font_bold, fg=COLOR_MUTED,
                 bg=COLOR_BG).pack(anchor="w")

        start_idx = max(
            0,
            min(
                self.line_cursor - self.viewport_size // 2,
                max(0, len(self.file_lines) - self.viewport_size)
            )
        )

        end_idx = start_idx + self.viewport_size

        for idx in range(start_idx, min(end_idx, len(self.file_lines))):
            line = self.file_lines[idx]
            unique_line_key = f"{self.current_file_path}||{line}"
            is_armed = unique_line_key in self.selected_lines
            is_active = (idx == self.line_cursor)

            lbl = tk.Label(
                self.list_pane,
                text=f"  {'[ LOCKED ]' if is_armed else '[ READY  ]'}  {line}",
                font=self.font_body,
                fg=COLOR_CYAN if is_active else (COLOR_WHITE if is_armed else COLOR_MUTED),
                bg=COLOR_HIGHLIGHT if is_active else COLOR_BG,
                anchor="w",
                padx=15,
                pady=6
            )
            lbl.pack(fill="x")

    def simulate_hardware_trigger(self, action):
        """Processes keyboard maps and cleanly mocks physical input behavior."""
        if action == "UP":
            if self.mode == "menu" and self.visible_items:
                self.cursor_index = (self.cursor_index - 1) % len(self.visible_items)
                self.repaint_menu_rows()
            elif self.mode == "line_browser" and self.file_lines:
                self.line_cursor = (self.line_cursor - 1) % len(self.file_lines)
                self.repaint_line_rows()

        elif action == "DOWN":
            if self.mode == "menu" and self.visible_items:
                self.cursor_index = (self.cursor_index + 1) % len(self.visible_items)
                self.repaint_menu_rows()
            elif self.mode == "line_browser" and self.file_lines:
                self.line_cursor = (self.line_cursor + 1) % len(self.file_lines)
                self.repaint_line_rows()

        elif action == "SELECT":
            if self.mode == "menu" and self.visible_items:
                target = self.visible_items[self.cursor_index]
                target_path = os.path.join(self.current_dir, target["name"])
                if target["is_dir"]:
                    self.current_dir = target_path
                    self.refresh_directory()
                    self.render_chassis()
                else:
                    self.open_line_browser(target_path)
            elif self.mode == "line_browser" and self.file_lines:
                active_line = self.file_lines[self.line_cursor]
                unique_line_key = f"{self.current_file_path}||{active_line}"
                if unique_line_key in self.selected_lines:
                    self.selected_lines.remove(unique_line_key)
                else:
                    self.selected_lines.add(unique_line_key)
                self.save_session_cache()
                self.repaint_line_rows()

        elif action == "BACK":
            if self.mode == "menu":
                if self.current_dir.rstrip('/') != SD_ROOT.rstrip('/'):
                    self.current_dir = os.path.dirname(self.current_dir.rstrip('/'))
                    self.refresh_directory()
                    self.render_chassis()
            elif self.mode in ["line_browser", "compiled"]:
                self.mode = "menu"
                self.render_chassis()

        elif action == "COMPILE":
            self.mode = "compiled" if self.mode == "menu" else "menu"
            self.render_chassis()

        elif action == "TIMER_SET":
            self.remaining_seconds += 600
            if self.remaining_seconds > 5940:
                self.remaining_seconds = 0
            self.refresh_timer_label()

        elif action == "TIMER_EXEC":
            if self.remaining_seconds > 0:
                self.timer_active = not self.timer_active
            self.refresh_timer_label()

        elif action == "CLEAR":
            self.clear_session_state()

    def open_line_browser(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                self.file_lines = [l.strip() for l in f.readlines() if l.strip()]
            self.current_file_path = filepath
            self.line_cursor = 0
            self.mode = "line_browser"
            self.render_chassis()
        except Exception as e:
            print(f"Error: {e}")

    def start_software_clock_loop(self):
        """Software level timer tracker to simulate hardware clock countdown changes."""
        if self.timer_active and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.refresh_timer_label()
            if self.remaining_seconds == 0:
                self.timer_active = False
                self.refresh_timer_label()
                print("🔊 SANDBOX BEEP: Countdown Complete!")
                self.root.bell()
        self.root.after(1000, self.start_software_clock_loop)

    def refresh_timer_label(self):
        if not hasattr(self, 'clock_lbl'):
            return
        t_display = f"⏱️ TIMER: {self.remaining_seconds // 60:02d}:{self.remaining_seconds % 60:02d}"
        if self.timer_active:
            t_display += " [ARMED]"
        self.clock_lbl.config(text=t_display)


if __name__ == "__main__":
    root = tk.Tk()
    app = BrainFreezeSandbox(root)
    root.mainloop()
