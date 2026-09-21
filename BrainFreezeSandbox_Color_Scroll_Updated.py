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
SD_ROOT = r"C:\Users\laure\OneDrive\Desktop\test_book"
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
        self.viewport_size = 12

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
        self.root.bind("r", lambda e: self.simulate_hardware_trigger("CHARACTER"))
        self.root.bind("y", lambda e: self.simulate_hardware_trigger("SCENE"))
        self.root.bind("g", lambda e: self.simulate_hardware_trigger("RESEARCH"))
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
        self.selected_lines = set()
        self.selected_markdown_chunks = set()

        if os.path.exists(CACHE_FILE):
            try:
                with open (CACHE_FILE, "r") as f:
                    cache_data = json.load(f)

                # Load existing line-based selections
                if isinstance(cache_data, dict):
                    self.selected_lines = set(
                        cache_data.get("selected_lines", [])
                    )

                    # Load Markdown selections
                    self.selected_markdown_chunks = set(
                        cache_data.get("selected_markdown_chunks", [])
                    )

                # Support the old cache format
                elif ininstance(cache_data, list):
                    self.selected_lines = set(cache_data)

            except Exception as e:
                print(f"Cache load error: {e}")

    def save_session_cache(self):
        try:
            cache_data = {
                "selected_lines": list(self.selected_lines),
                "selected_markdown_chunks": list(
                    getattr(self, "selected_markdown_chunks", set())
                )
            }

            with open(CACHE_FILE, "w") as f:
                json.dump(cache_data, f)

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
                     os.path.isfile(os.path.join(self.current_dir, i)) and i.endswith(('.txt', '.md', '.json'))]

            for d in dirs: self.visible_items.append({"name": d, "is_dir": True})
            for f in files: self.visible_items.append({"name": f, "is_dir": False})
        except Exception as e:
            print(f"Error: {e}")

        self.cursor_index = self.folder_history.get(self.current_dir, 0)

    def render_freeze_character(self):
        """Displays the Character Freeze Frame."""

        for widget in self.root.winfo_children():
            widget.destroy()

        screen = tk.Frame(
            self.root,
            bg="#FFA7A7"
        )
        screen.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        tk.Label(
            screen,
            text="CHARACTER: BIOMETRICS DEPLOYED",
            font=self.font_bold,
            fg="#7A0000",
            bg="#FFA7A7"
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

        tk.Label(
            screen,
            text="=" * 70,
            font=self.font_body,
            fg="#5A0000",
            bg="#FFA7A7"
        ).pack(
            anchor="w"
        )

        character_text = ""

        # Existing line-based selections
        for combined_string in self.selected_lines:

            if "||" in combined_string:

                origin_path, line_content = combined_string.split(
                    "||",
                    1
                )

                if "01_characters" in origin_path:

                    character_text += f"• {line_content}\n\n"

        # Markdown frozen chunks
        if hasattr(self, "selected_markdown_chunks"):

            markdown_by_subject = {}

            for combined_string in self.selected_markdown_chunks:

                if "||" in combined_string:

                    origin_path, chunk_title = combined_string.split(
                        "||",
                        1
                    )

                    if "01_characters" in origin_path:

                        for chunk in getattr(
                            self,
                            "markdown_chunks",
                            []
                        ):

                            if chunk["title"] == chunk_title:

                                subject = chunk["subject"]

                                if subject not in markdown_by_subject:
                                    markdown_by_subject[subject] = []

                                markdown_by_subject[subject].append(
                                    chunk
                                )

            for subject, chunks in markdown_by_subject.items():

                character_text += f"\n{subject}\n"
                character_text += "-" * 70
                character_text += "\n\n"

                for chunk in chunks:

                    body = "\n".join(
                        chunk["lines"]
                    ).strip()

                    character_text += f"{chunk['title']}\n"

                    if body:
                        character_text += f"{body}\n\n"

        txt = tk.Text(
            screen,
            font=self.font_body,
            fg="#000000",
            bg="#FFA7A7",
            wrap="word",
            bd=0,
            highlightthickness=0,
            spacing1=0,
            spacing3=0
        )

        txt.insert(
            "1.0",
            character_text if character_text else "[NO CHARACTER INFORMATION SELECTED]\n"
        )

        txt.config(state="disabled")

        txt.pack(
            fill="both",
            expand=True,
            pady=15
        )
        tk.Label(
            screen,
            text="R = Character     Y = Scene     G = Research",
            font=self.font_body,
            fg="#5A0000",
            bg="#FFA7A7"
        ).pack(
            anchor="w"
        )

    def render_freeze_scene(self):
        """Displays the Scene Freeze Frame."""

        for widget in self.root.winfo_children():
            widget.destroy()

        screen = tk.Frame(
            self.root,
            bg="#FEFFAB"
        )
        screen.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        tk.Label(
            screen,
            text="SCENE: ANCHORS SECURED",
            font=self.font_bold,
            fg="#514B00",
            bg="#FEFFAB"
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

        tk.Label(
            screen,
            text="=" * 70,
            font=self.font_body,
            fg="#665F00",
            bg="#FEFFAB"
        ).pack(
            anchor="w"
        )

        tk.Label(
            screen,
            text="SCENE SCREEN",
            font=self.font_body,
            fg="#000000",
            bg="#FEFFAB"
        ).pack(
            anchor="w",
            pady=20
        )

        tk.Label(
            screen,
            text="R = Character     Y = Scene     G = Research",
            font=self.font_body,
            fg="#665F00",
            bg="#FEFFAB"
        ).pack(
            anchor="w"
        )

    def render_freeze_research(self):
        """Displays the Research Freeze Frame."""

        for widget in self.root.winfo_children():
            widget.destroy()

        screen = tk.Frame(
            self.root,
            bg="#C4FFCB"
        )
        screen.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        tk.Label(
            screen,
            text="RESEARCH: COORDINATES ISOLATED",
            font=self.font_bold,
            fg="#365C1F",
            bg="#C4FFCB"
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

        tk.Label(
            screen,
            text="=" * 70,
            font=self.font_body,
            fg="#4F663F",
            bg="#C4FFCB"
        ).pack(
            anchor="w"
        )

        tk.Label(
            screen,
            text="RESEARCH SCREEN",
            font=self.font_body,
            fg="#000000",
            bg="#C4FFCB"
        ).pack(
            anchor="w",
            pady=20
        )

        tk.Label(
            screen,
            text="R = Character     Y = Scene     G = Research",
            font=self.font_body,
            fg="#4F663F",
            bg="#C4FFCB"
        ).pack(
            anchor="w"
        )

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
            
        elif self.mode == "markdown_browser":
            self.list_pane = tk.Frame(self.canvas, bg=COLOR_BG)
            self.list_pane.pack(fill="both", expand=True, padx=15)
            self.repaint_markdown_rows()

        elif self.mode == "json_browser":
            self.list_pane = tk.Frame(self.canvas, bg=COLOR_BG)
            self.list_pane.pack(fill="both", expand=True, padx=15)
            self.repaint_json_rows()

        elif self.mode == "freeze_character":
            self.render_freeze_character()

        elif self.mode == "freeze_scene":
            self.render_freeze_scene()

        elif self.mode == "freeze_research":
            self.render_freeze_research()

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

                # Existing line-based cognitive anchors
                for combined_string in self.selected_lines:
                    if "||" in combined_string:
                        origin_path, line_content = combined_string.split("||", 1)

                        if keyword in origin_path:
                            column_text += f"• {line_content}\n\n"

                # Markdown frozen chunks
                if hasattr(self, "selected_markdown_chunks"):

                    markdown_by_subject = {}

                    for combined_string in self.selected_markdown_chunks:

                        if "||" in combined_string:

                            origin_path, chunk_title = combined_string.split("||", 1)

                            if keyword in origin_path:

                                for chunk in getattr(self, "markdown_chunks", []):

                                    if chunk["title"] == chunk_title:

                                        subject = chunk["subject"]

                                        if subject not in markdown_by_subject:
                                            markdown_by_subject[subject] = []

                                        markdown_by_subject[subject].append(chunk)

                    for subject, chunks in markdown_by_subject.items():

                        column_text += f"\n[{subject}]\n\n"

                        for chunk in chunks:

                            body = "\n".join(chunk["lines"]).strip()

                            column_text += f"• {chunk['title']}\n"

                            if body:
                                column_text += f"{body}\n\n"

                txt = tk.Text(
                    box_content,
                    font=self.font_body,
                    fg=COLOR_WHITE,
                    bg=COLOR_BG,
                    wrap="word",
                    bd=0,
                    highlightthickness=0,
                    spacing1=0,
                    spacing3=0
                )

                txt.insert(
                    "1.0",
                    column_text if column_text else "[NO COGNITIVE ANCHORS LINKED]\n"
                )

                txt.config(state="disabled")
                txt.pack(fill="both", expand=True, padx=15, pady=5)


    def repaint_markdown_rows(self):
        for w in self.list_pane.winfo_children():
            w.destroy()

        # Create a scrollable area for the Markdown document.
        scroll_canvas = tk.Canvas(
            self.list_pane,
            bg=COLOR_BG,
            highlightthickness=0,
            bd=0
        )

        scrollbar = tk.Scrollbar(
            self.list_pane,
            orient="vertical",
            command=scroll_canvas.yview
        )

        scroll_canvas.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        scroll_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll_frame = tk.Frame(
            scroll_canvas,
            bg=COLOR_BG
        )

        scroll_window = scroll_canvas.create_window(
            (0, 0),
            window=scroll_frame,
            anchor="nw"
        )

        def update_scroll_region(event=None):
            scroll_canvas.configure(
                scrollregion=scroll_canvas.bbox("all")
            )

        scroll_frame.bind(
            "<Configure>",
            update_scroll_region
        )

        def resize_scroll_frame(event):
            scroll_canvas.itemconfig(
                scroll_window,
                width=event.width
            )

        scroll_canvas.bind(
            "<Configure>",
            resize_scroll_frame
        )

        # Mouse-wheel scrolling while using the computer.
        scroll_canvas.bind(
            "<MouseWheel>",
            lambda event: scroll_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )
        )

        filename = os.path.basename(self.current_file_path)

        tk.Label(
            scroll_frame,
            text=f"REFERENCE MODULE: {filename}\n",
            font=self.font_bold,
            fg=COLOR_MUTED,
            bg=COLOR_BG
        ).pack(anchor="w")

        # Build freezeable Markdown chunks.
        self.markdown_chunks = []

        current_chunk = None
        current_subject = ""
        current_category = ""

        for line in self.file_lines:

            # # heading = major section.
            # It is context only, never selectable.
            if line.startswith("# ") and not line.startswith("## "):

                if current_chunk is not None:
                    self.markdown_chunks.append(current_chunk)
                    current_chunk = None

                current_subject = ""
                current_category = ""

            # ## heading = current subject.
            # It is context only, never selectable.
            elif line.startswith("## "):

                if current_chunk is not None:
                    self.markdown_chunks.append(current_chunk)
                    current_chunk = None

                current_subject = line[3:].strip()
                current_category = ""

            # ### heading = current category.
            # It is context only, never selectable.
            elif line.startswith("### "):

                if current_chunk is not None:
                    self.markdown_chunks.append(current_chunk)
                    current_chunk = None

                current_category = line[4:].strip()

            # #### heading = new freezeable chunk.
            elif line.startswith("#### "):

                if current_chunk is not None:
                    self.markdown_chunks.append(current_chunk)

                current_chunk = {
                    "title": line[5:].strip(),
                    "subject": current_subject,
                    "category": current_category,
                    "lines": []
                }

            # Everything after #### belongs to that chunk.
            elif current_chunk is not None:
                current_chunk["lines"].append(line)

        # Add the final chunk.
        if current_chunk is not None:
            self.markdown_chunks.append(current_chunk)

        # Show the chunks.
        displayed_subject = None
        displayed_category = None

        for idx, chunk in enumerate(self.markdown_chunks):

            subject = chunk["subject"]
            category = chunk["category"]

            # Show the ## subject as context.
            if subject != displayed_subject:

                tk.Label(
                    scroll_frame,
                    text=subject,
                    font=self.font_bold,
                    fg=COLOR_MUTED,
                    bg=COLOR_BG,
                    anchor="w",
                    justify="left",
                    padx=15,
                    pady=10
                ).pack(fill="x")

                displayed_subject = subject
                displayed_category = None

            # Show the ### category as context.
            if category and category != displayed_category:

                tk.Label(
                    scroll_frame,
                    text=category,
                    font=self.font_bold,
                    fg=COLOR_WHITE,
                    bg=COLOR_BG,
                    anchor="w",
                    justify="left",
                    padx=30,
                    pady=5
                ).pack(fill="x")

                displayed_category = category

            title = chunk["title"]
            body = "\n".join(chunk["lines"]).strip()

            chunk_text = title

            if idx == self.markdown_cursor:
                chunk_text = "▶ " + chunk_text

            unique_chunk_key = (
                f"{self.current_file_path}||{title}"
            )

            if unique_chunk_key in self.selected_markdown_chunks:
                chunk_text = "🔒 " + chunk_text

            if body:
                chunk_text += f"\n\n{body}"

            lbl = tk.Label(
                scroll_frame,
                text=chunk_text,
                font=self.font_body,
                fg=COLOR_WHITE,
                bg=COLOR_BG,
                anchor="w",
                justify="left",
                padx=45,
                pady=10
            )

            lbl.pack(fill="x")

    def repaint_json_rows(self):
        for w in self.list_pane.winfo_children():
            w.destroy()

        filename = os.path.basename(self.current_file_path)

        tk.Label(
            self.list_pane,
            text=f"JSON MODULE: {filename}\n",
            font=self.font_bold,
            fg=COLOR_MUTED,
            bg=COLOR_BG
        ).pack(anchor="w")

        # Get the top-level JSON items.
        json_items = list(self.json_data.items())

        # Number of items visible at one time.
        visible_rows = 12

        # Work out which part of the JSON should be displayed.
        if len(json_items) <= visible_rows:
            start_idx = 0
        else:
            start_idx = self.json_cursor - (visible_rows // 2)

            if start_idx < 0:
                start_idx = 0

            max_start = len(json_items) - visible_rows

            if start_idx > max_start:
                start_idx = max_start

        end_idx = min(
            start_idx + visible_rows,
            len(json_items)
        )

        # Draw the portion of the JSON currently in view.
        for idx in range(start_idx, end_idx):
            key, value = json_items[idx]

            is_active = (idx == self.json_cursor)

            if not hasattr(self, "selected_json_items"):
                self.selected_json_items = set()

            unique_json_key = f"{self.current_file_path}||{key}"
            is_armed = unique_json_key in self.selected_json_items
            
            if isinstance(value, (dict, list)):
                display_value = "[ GROUP ]"
            else:
                display_value = str(value)

            lbl = tk.Label(
                self.list_pane,
                text=f"  {'[ ACTIVE + LOCKED]' if is_active and is_armed else ('[ ACTIVE ]' if is_active else ('[ LOCKED ]' if is_armed else '[ READY ]'))} {key}: {display_value}",
                font=self.font_body,
                fg=COLOR_CYAN if is_active else (
                    COLOR_WHITE if is_armed else COLOR_MUTED
                ),
                bg=COLOR_HIGHLIGHT if is_active else COLOR_BG,
                anchor="w",
                padx=15,
                pady=6
            )

            lbl.pack(fill="x")             

    def repaint_menu_rows(self):
        for w in self.list_pane.winfo_children():
            w.destroy()

        # Display folder path marker
        rel_path = self.current_dir.replace(SD_ROOT, "SYS://")
        tk.Label(
            self.list_pane,
            text=f"PATH: {rel_path}\n",
            font=self.font_bold,
            fg=COLOR_MUTED,
            bg=COLOR_BG
        ).pack(anchor="w")

        for idx, item in enumerate(self.visible_items):
            full_path = os.path.join(self.current_dir, item["name"])
            icon = "📁" if item["is_dir"] else "📄"

            matches = sum(
                1 for p_line in self.selected_lines
                if p_line.startswith(full_path)
            )

            markdown_matches = sum(
                1 for p_chunk in self.selected_markdown_chunks
                if p_chunk.startswith(full_path)
            )

            matches += markdown_matches

            tether_label = f" [{matches} EXTRACTED]" if matches > 0 else ""

            is_active = (idx == self.cursor_index)

            lbl = tk.Label(
                self.list_pane,
                text=f"  {icon} {item['name']}{'/' if item['is_dir'] else ''}{tether_label}",
                font=self.font_body,
                fg=COLOR_CYAN if is_active else (
                    COLOR_WHITE if matches > 0 else COLOR_MUTED
                ),
                bg=COLOR_HIGHLIGHT if is_active else COLOR_BG,
                anchor="w",
                padx=15,
                pady=6
            )
            lbl.pack(fill="x")

    def repaint_line_rows(self):
        for w in self.list_pane.winfo_children():
            w.destroy()

        filename = os.path.basename(self.current_file_path)

        tk.Label(
            self.list_pane,
            text=f"FILE MODULE: {filename}\n",
            font=self.font_bold,
            fg=COLOR_MUTED,
            bg=COLOR_BG
        ).pack(anchor="w")

        # Number of lines visible at one time
        visible_rows = 12

        # Work out which part of the file should be displayed.
        if len(self.file_lines) <= visible_rows:
            start_idx = 0
        else:
            start_idx = self.line_cursor - (visible_rows // 2)

            if start_idx < 0:
                start_idx = 0

            max_start = len(self.file_lines) - visible_rows

            if start_idx > max_start:
                start_idx = max_start

        end_idx = min(
            start_idx + visible_rows,
            len(self.file_lines)
        )

        # Draw only the portion of the file currently in view.
        for idx in range(start_idx, end_idx):
            line = self.file_lines[idx]

            unique_line_key = f"{self.current_file_path}||{line}"

            is_armed = unique_line_key in self.selected_lines
            is_active = (idx == self.line_cursor)

            lbl = tk.Label(
                self.list_pane,
                text=f"  {'[ LOCKED ]' if is_armed else '[ READY  ]'}  {line}",
                font=self.font_body,
                fg=COLOR_CYAN if is_active else (
                    COLOR_WHITE if is_armed else COLOR_MUTED
                ),
                bg=COLOR_HIGHLIGHT if is_active else COLOR_BG,
                anchor="w",
                padx=15,
                pady=6
            )

            lbl.pack(fill="x")
    
    def repaint_markdown_rows(self):
        for w in self.list_pane.winfo_children():
            w.destroy()

        # Create a scrollable area for the Markdown document.
        scroll_canvas = tk.Canvas(
            self.list_pane,
            bg=COLOR_BG,
            highlightthickness=0,
            bd=0
        )

        scrollbar = tk.Scrollbar(
            self.list_pane,
            orient="vertical",
            command=scroll_canvas.yview
        )

        scroll_canvas.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        scroll_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scroll_frame = tk.Frame(
            scroll_canvas,
            bg=COLOR_BG
        )

        scroll_window = scroll_canvas.create_window(
            (0, 0),
            window=scroll_frame,
            anchor="nw"
        )

        def update_scroll_region(event=None):
            scroll_canvas.configure(
                scrollregion=scroll_canvas.bbox("all")
            )

        scroll_frame.bind(
            "<Configure>",
            update_scroll_region
        )

        def resize_scroll_frame(event):
            scroll_canvas.itemconfig(
                scroll_window,
                width=event.width
            )

        scroll_canvas.bind(
            "<Configure>",
            resize_scroll_frame
        )

        # Mouse-wheel scrolling while using the computer.
        scroll_canvas.bind(
            "<MouseWheel>",
            lambda event: scroll_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )
        )

        filename = os.path.basename(self.current_file_path)

        tk.Label(
            scroll_frame,
            text=f"REFERENCE MODULE: {filename}\n",
            font=self.font_bold,
            fg=COLOR_MUTED,
            bg=COLOR_BG
        ).pack(anchor="w")
        tk.Label(
            self.list_pane,
            text=f"REFERENCE MODULE: {filename}\n",
            font=self.font_bold,
            fg=COLOR_MUTED,
            bg=COLOR_BG
        ).pack(anchor="w")

        # Build freezeable Markdown chunks.
        self.markdown_chunks = []

        current_chunk = None
        current_subject = ""
        current_category = ""

        for line in self.file_lines:

            # # heading = major section.
            # It is context only, never selectable.
            if line.startswith("# ") and not line.startswith("## "):

                if current_chunk is not None:
                    self.markdown_chunks.append(current_chunk)
                    current_chunk = None

                current_subject = ""
                current_category = ""

            # ## heading = current subject.
            # It is context only, never selectable.
            elif line.startswith("## "):

                if current_chunk is not None:
                    self.markdown_chunks.append(current_chunk)
                    current_chunk = None

                current_subject = line[3:].strip()
                current_category = ""

            # ### heading = current category.
            # It is context only, never selectable.
            elif line.startswith("### "):

                if current_chunk is not None:
                    self.markdown_chunks.append(current_chunk)
                    current_chunk = None

                current_category = line[4:].strip()

            # #### heading = new freezeable chunk.
            elif line.startswith("#### "):

                if current_chunk is not None:
                    self.markdown_chunks.append(current_chunk)

                current_chunk = {
                    "title": line[5:].strip(),
                    "subject": current_subject,
                    "category": current_category,
                    "lines": []
                }

            # Everything after #### belongs to that chunk.
            elif current_chunk is not None:
                current_chunk["lines"].append(line)

        # Add the final chunk.
        if current_chunk is not None:
            self.markdown_chunks.append(current_chunk)

        # Show the chunks.
        displayed_subject = None
        displayed_category = None

        for idx, chunk in enumerate(self.markdown_chunks):

            subject = chunk["subject"]
            category = chunk["category"]

            # Show the ## subject as context.
            if subject != displayed_subject:

                tk.Label(
                    self.list_pane,
                    text=subject,
                    font=self.font_bold,
                    fg=COLOR_MUTED,
                    bg=COLOR_BG,
                    anchor="w",
                    justify="left",
                    padx=15,
                    pady=10
                ).pack(fill="x")

                displayed_subject = subject
                displayed_category = None

            # Show the ### category as context.
            if category and category != displayed_category:

                tk.Label(
                    self.list_pane,
                    text=category,
                    font=self.font_bold,
                    fg=COLOR_WHITE,
                    bg=COLOR_BG,
                    anchor="w",
                    justify="left",
                    padx=30,
                    pady=5
                ).pack(fill="x")

                displayed_category = category

            title = chunk["title"]
            body = "\n".join(chunk["lines"]).strip()

            chunk_text = title

            if idx == self.markdown_cursor:
                chunk_text = "▶ " + chunk_text

            unique_chunk_key = (
                f"{self.current_file_path}||{title}"
            )

            if unique_chunk_key in self.selected_markdown_chunks:
                chunk_text = "🔒 " + chunk_text

            if body:
                chunk_text += f"\n\n{body}"

            lbl = tk.Label(
                self.list_pane,
                text=chunk_text,
                font=self.font_body,
                fg=COLOR_WHITE,
                bg=COLOR_BG,
                anchor="w",
                justify="left",
                padx=45,
                pady=10
            )

            lbl.pack(fill="x")
    def simulate_hardware_trigger(self, action):
        """Processes keyboard maps and cleanly mocks physical input behavior."""

        if action == "UP":
            if self.mode == "menu" and self.visible_items:
                self.cursor_index = max(self.cursor_index - 1, 0)
                self.repaint_menu_rows()

            elif self.mode == "line_browser" and self.file_lines:
                self.line_cursor = max(self.line_cursor - 1, 0)
                self.repaint_line_rows()

            elif self.mode == "json_browser" and self.json_data:
                self.json_cursor = max(self.json_cursor - 1, 0)
                self.repaint_json_rows()

            elif self.mode == "markdown_browser" and self.markdown_chunks:
                self.markdown_cursor = max(self.markdown_cursor - 1, 0)
                self.repaint_markdown_rows()

        elif action == "DOWN":
            if self.mode == "menu" and self.visible_items:
                self.cursor_index = min(
                    self.cursor_index + 1,
                    len(self.visible_items) - 1
                )
                self.repaint_menu_rows()

            elif self.mode == "line_browser" and self.file_lines:
                self.line_cursor = min(
                    self.line_cursor + 1,
                    len(self.file_lines) - 1
                )
                self.repaint_line_rows()

            elif self.mode == "json_browser" and self.json_data:
                self.json_cursor = min(
                    self.json_cursor + 1,
                    len(self.json_data) - 1
                )
                self.repaint_json_rows()

            elif self.mode == "markdown_browser" and self.markdown_chunks:
                self.markdown_cursor = min(
                    self.markdown_cursor + 1,
                    len(self.markdown_chunks) - 1
                )
                self.repaint_markdown_rows()

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

            elif self.mode == "json_browser" and self.json_data:
                json_items = list(self.json_data.items())
                key, value = json_items[self.json_cursor]

                if not hasattr(self, "selected_json_items"):
                    self.selected_json_items = set()

                unique_json_key = f"{self.current_file_path}||{key}"

                if unique_json_key in self.selected_json_items:
                    self.selected_json_items.remove(unique_json_key)
                else:
                    self.selected_json_items.add(unique_json_key)

                self.repaint_json_rows()

            elif self.mode == "markdown_browser" and self.markdown_chunks:
                chunk = self.markdown_chunks[self.markdown_cursor]
                chunk_title = chunk["title"]

                unique_chunk_key = (
                    f"{self.current_file_path}||{chunk_title}"
                )

                if unique_chunk_key in self.selected_markdown_chunks:
                    self.selected_markdown_chunks.remove(unique_chunk_key)
                else:
                    self.selected_markdown_chunks.add(unique_chunk_key)
                self.save_session_cache()
                self.repaint_markdown_rows()

        elif action == "BACK":
            if self.mode == "menu":
                if self.current_dir.rstrip("/") != SD_ROOT.rstrip("/"):
                    self.current_dir = os.path.dirname(
                        self.current_dir.rstrip("/")
                    )
                    self.refresh_directory()
                    self.render_chassis()

            elif self.mode in [
                "line_browser",
                "json_browser",
                "markdown_browser",
                "compiled",
                "freeze_character",
                "freeze_scene",
                "freeze_research"
            ]:
                self.mode = "menu"
                self.render_chassis()

        elif action == "CHARACTER":
            self.mode = "freeze_character"
            self.render_chassis()

        elif action == "SCENE":
            self.mode = "freeze_scene"
            self.render_chassis()

        elif action == "RESEARCH":
            self.mode = "freeze_research"
            self.render_chassis()

        elif action == "COMPILE":
            self.compiled_markdown_chunks = []

            if hasattr(self, "selected_markdown_chunks"):

                # If Markdown chunks are not currently loaded,
                # rebuild them from the saved Markdown selection.
                if not hasattr(self, "markdown_chunks"):

                    if self.selected_markdown_chunks:

                        saved_selection = next(
                            iter(self.selected_markdown_chunks)
                        )

                        if "||" in saved_selection:
                            saved_path, saved_title = saved_selection.split(
                                "||", 1
                            )

                            if os.path.exists(saved_path):
                                self.open_line_browser(saved_path)

                # Now collect the selected Markdown chunks.
                if hasattr(self, "markdown_chunks"):

                    for chunk in self.markdown_chunks:

                        unique_chunk_key = (
                            f"{self.current_file_path}||{chunk['title']}"
                        )

                        if unique_chunk_key in self.selected_markdown_chunks:
                            self.compiled_markdown_chunks.append(chunk)

            self.mode = "freeze_character"
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
            if filepath.endswith(".md"):
                with open(filepath, "r", encoding="utf-8") as f:
                    self.file_lines = [
                        l.rstrip()
                        for l in f.readlines()
                        if l.strip()
                    ]

                self.current_file_path = filepath
                self.markdown_cursor = 0

                if not hasattr(self, "selected_markdown_chunks"):
                    self.selected_markdown_chunks = set()
                self.mode = "markdown_browser"
                self.render_chassis()

            elif filepath.endswith(".json"):
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)

                self.json_data = data
                self.current_file_path = filepath
                self.mode = "json_browser"
                self.json_cursor = 0
                self.render_chassis()

            else:
                with open(filepath, "r", encoding="utf-8") as f:
                    self.file_lines = [
                        l.strip()
                        for l in f.readlines()
                        if l.strip()
                    ]

                self.current_file_path = filepath
                self.line_cursor = 0
                self.mode = "line_browser"
                self.render_chassis()

        except Exception as e:
            print(f"Error: {e}")

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
