import tkinter as tk
from tkinter import ttk, PhotoImage
from collections import deque
import time
import os

# --- 1. KNOWLEDGE BASE (Facts and Rules) ---
# (Knowledge base remains the same)
ALL_FACTS = [
    "Color: Blue", "Color: Yellow", "Color: Red/White", 
    "Body Shape: Flattened", "Body Shape: Oval", "Body Shape: Tube-like",
    "Fins: Spiky", "Fins: Large Fan", "Fins: Caudal Forked",
    "Habitat: Coral Reef", "Habitat: Sandy Bottom", "Habitat: Open Ocean",
    "Color: White/Pale", "Temp: High" 
]

RULES = [
    ('Species: Blue Tang', ["Color: Blue", "Body Shape: Oval", "Habitat: Coral Reef"]),
    ('Species: Flounder', ["Body Shape: Flattened", "Habitat: Sandy Bottom"]), 
    ('Species: Lionfish', ["Color: Red/White", "Fins: Spiky", "Habitat: Coral Reef"]),
    ('Species: Seahorse', ["Body Shape: Tube-like", "Fins: Large Fan", "Habitat: Coral Reef"]),
    ('Condition: Bleaching', ["Color: White/Pale", "Habitat: Coral Reef", "Temp: High"]),
]
GOALS = sorted(list(set(rule[0] for rule in RULES)))

# --- 2. INFERENCE ALGORITHMS ---
# (Inference algorithms remain the same, kept outside the class for brevity)

def forward_chaining_bfs(initial_facts, update_log_callback=None):
    current_facts = set(initial_facts)
    log = []
    
    while True:
        rule_fired_in_this_pass = False
        for i, (conclusion, required_facts) in enumerate(RULES):
            rule_index = i + 1
            if conclusion in current_facts: continue
            if all(fact in current_facts for fact in required_facts):
                log_msg = f"[FC/BFS] Rule {rule_index} Matched: IF ({' AND '.join(required_facts)}) THEN **{conclusion}**"
                log.append(log_msg)
                if update_log_callback: update_log_callback(log_msg)
                current_facts.add(conclusion)
                rule_fired_in_this_pass = True
                if conclusion.startswith("Species:") or conclusion.startswith("Condition:"):
                    return conclusion, log
        if not rule_fired_in_this_pass: break
    return "Species: Unknown / Condition: Undetermined", log

def backward_chaining_dfs(goal, facts, update_log_callback=None, indent=""):
    log_msg = f"{indent}🔎 Checking if **{goal}** is provable..."
    if update_log_callback: update_log_callback(log_msg)
    if goal in facts:
        log_msg = f"{indent}✅ Goal **{goal}** is already a known fact."
        if update_log_callback: update_log_callback(log_msg)
        return True
    
    for i, (conclusion, required_facts) in enumerate(RULES):
        if conclusion == goal:
            rule_index = i + 1
            log_msg = f"{indent}├── Trying Rule {rule_index}: IF ({' AND '.join(required_facts)}) THEN {goal}"
            if update_log_callback: update_log_callback(log_msg)
            all_prereqs_proven = True
            for fact in required_facts:
                if not backward_chaining_dfs(fact, facts, update_log_callback, indent + "│  "):
                    all_prereqs_proven = False
                    break 
            if all_prereqs_proven:
                log_msg = f"{indent}└── **Goal {goal} PROVEN** by Rule {rule_index}."
                if update_log_callback: update_log_callback(log_msg)
                return True 
    log_msg = f"{indent}❌ Goal **{goal}** cannot be proven by the current facts/rules."
    if update_log_callback: update_log_callback(log_msg)
    return False


# --- 3. TKINTER GUI SETUP ---

class MarineExpertSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🐟 Marine Life Identifier - AI Expert System (FC/BC Demo)")
        self.geometry("1000x700")
        self.resizable(True, True)

        self.colors = {
            "bg_dark": "#0A243F", "bg_light": "#1A4E7E", "frame_bg": "#12375F",
            "text_color": "#E0F2F7", "accent_green": "#4CAF50", "accent_blue": "#00BCD4",
            "welcome_banner": "#0097A7", 
            "log_bg": "#0D335D"
        }

        self.style = ttk.Style(self)
        try:
            from ttkbootstrap import Style
            self.style = Style(theme='superhero')
        except ImportError:
            self.style.theme_use('clam') 
            self.configure_custom_style()

        self.configure(bg=self.colors["bg_dark"])
        self.fact_vars = {}
        self.goal_var = tk.StringVar(self)
        self.bg_image = None
        self.current_log_window = None

        # --- ICON LOADING (Updated to use 'sharp_img.png') ---
        icon_path_png = "sharp_img.png" # Using the filename you provided

        self.app_icon = None 
        if os.path.exists(icon_path_png):
            try:
                # Load the PhotoImage for the icon
                self.app_icon = PhotoImage(file=icon_path_png)
                # Set it as the icon for the main window and all Toplevels
                self.iconphoto(True, self.app_icon) 
            except Exception as e:
                print(f"Error loading PNG icon '{icon_path_png}': {e}")
                self.app_icon = None
        else:
            print(f"Icon file '{icon_path_png}' not found. Using default Tkinter icon.")
        # --- END ICON LOADING ---

        # Background Image Logic (Placeholder remains)
        image_path = "underwater_bg.png" 
        if os.path.exists(image_path):
            try:
                self.bg_image_raw = PhotoImage(file=image_path)
                self.bg_image = self.bg_image_raw.subsample(
                    int(self.bg_image_raw.width / 1000) or 1,
                    int(self.bg_image_raw.height / 700) or 1
                )
            except Exception as e:
                self.bg_image = None
        
        self.create_widgets()


    def configure_custom_style(self):
        self.style.configure('.', font=('Segoe UI', 10), foreground=self.colors["text_color"], background=self.colors["bg_dark"])
        self.style.configure('TFrame', background=self.colors["frame_bg"])
        self.style.configure('TLabelframe', background=self.colors["frame_bg"], foreground=self.colors["text_color"])
        self.style.configure('TLabelframe.Label', font=('Segoe UI', 12, 'bold'), foreground=self.colors["text_color"], background=self.colors["frame_bg"])
        self.style.configure('TCheckbutton', background=self.colors["frame_bg"], foreground=self.colors["text_color"], font=('Segoe UI', 11))
        self.style.map('TCheckbutton', background=[('active', self.colors["bg_light"])])
        self.style.configure('TButton', font=('Segoe UI', 11, 'bold'), background=self.colors["accent_blue"], foreground='white')
        self.style.map('TButton', background=[('active', self.colors["bg_light"])])
        self.style.configure('Accent.TButton', background=self.colors["accent_green"], foreground='white')

    def create_widgets(self):
        # Background Image Layer
        if self.bg_image:
            self.bg_label = tk.Label(self, image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Main Container Frame
        main_container = ttk.Frame(self, padding=15, style='TFrame')
        main_container.pack(fill="both", expand=True)
        
        main_container.grid_rowconfigure(0, weight=0)
        main_container.grid_rowconfigure(1, weight=1) 
        main_container.grid_columnconfigure(0, weight=1)

        # --- Welcome Banner (ROW 0 - Enhanced Visuals) ---
        welcome_frame = ttk.Frame(main_container, padding=20)
        welcome_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        
        banner_bg = self.colors["welcome_banner"]
        welcome_frame.configure(style='Welcome.TFrame')
        self.style.configure('Welcome.TFrame', background=banner_bg)
        
        ttk.Label(welcome_frame, text="WELCOME TO THE MARINE AI EXPERT SYSTEM", 
                  font=('Poppins', 22, 'bold'), foreground='white', 
                  background=banner_bg).pack(fill='x', pady=(0, 5))
        
        ttk.Label(welcome_frame, text="Identify marine life or diagnose ecosystem health using Forward Chaining (Prediction) and Backward Chaining (Confirmation).", 
                  font=('Segoe UI', 12, 'italic'), foreground=self.colors["text_color"], 
                  background=banner_bg).pack(fill='x')


        # --- Main Input/Control Frame (ROW 1 - Now taking up vertical space) ---
        control_frame = ttk.Frame(main_container, style='TFrame')
        control_frame.grid(row=1, column=0, padx=15, pady=15, sticky="nsew") 
        control_frame.grid_columnconfigure(0, weight=1, uniform="ctrl_group")
        control_frame.grid_columnconfigure(1, weight=1, uniform="ctrl_group")
        control_frame.grid_rowconfigure(0, weight=1)

        # --- Left Half: User Input (Facts) ---
        input_frame = ttk.LabelFrame(control_frame, text="1. Marine Observation Deck 🌊", padding="15", style='TLabelframe')
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.checkbox_frame = ttk.Frame(input_frame, style='TFrame')
        self.checkbox_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        ttk.Label(self.checkbox_frame, text="Select all observed characteristics:", 
                  font=('Segoe UI', 11, 'italic'), foreground=self.colors["accent_blue"], 
                  background=self.colors["frame_bg"]).grid(row=0, column=0, columnspan=3, sticky='w', pady=10)
        
        cols = 3
        for i, fact in enumerate(ALL_FACTS):
            var = tk.IntVar(value=0)
            chk = ttk.Checkbutton(self.checkbox_frame, text=fact, variable=var, style='TCheckbutton')
            row_num = i // cols + 1 
            col_num = i % cols
            chk.grid(row=row_num, column=col_num, sticky='w', padx=10, pady=4)
            self.fact_vars[fact] = var
        

        # --- Right Half: Control Panel (Buttons) ---
        control_panel = ttk.LabelFrame(control_frame, text="2. Inference Control Panel", padding="15", style='TLabelframe')
        control_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # FC Button
        self.fc_button = ttk.Button(control_panel, text="RUN FORWARD CHAINING (PREDICT SPECIES)", command=self.run_forward_chaining, style='Accent.TButton')
        self.fc_button.pack(fill="x", pady=(5, 20))

        # BC Goal Selection
        ttk.Label(control_panel, text="3. Confirmation Goal (Backward Chaining):", 
                  font=('Segoe UI', 11, 'bold'), foreground=self.colors["accent_blue"], background=self.colors["frame_bg"]).pack(fill='x', pady=(20, 5))
        
        self.goal_var.set(GOALS[0])
        self.goal_dropdown = ttk.OptionMenu(control_panel, self.goal_var, GOALS[0], *GOALS)
        self.goal_dropdown.pack(fill='x', pady=5)
        
        self.bc_button = ttk.Button(control_panel, text="RUN BACKWARD CHAINING (CONFIRM GOAL)", command=self.run_backward_chaining, style='TButton')
        self.bc_button.pack(fill="x", pady=(5, 20))
        
        
    def get_current_facts(self):
        initial_facts = []
        for fact, var in self.fact_vars.items():
            if var.get() == 1:
                initial_facts.append(fact)
        return initial_facts

    def update_log_and_scroll(self, log_text_widget, message):
        log_text_widget.config(state='normal')
        log_text_widget.insert(tk.END, message + "\n")
        log_text_widget.see(tk.END)
        log_text_widget.config(state='disabled')
        self.update_idletasks()

    def open_log_window(self, title, algorithm_func, is_fc):
        if self.current_log_window and self.current_log_window.winfo_exists():
            self.current_log_window.destroy()

        new_window = tk.Toplevel(self)
        new_window.title(f"AI Inference Log: {title}")
        new_window.geometry("600x600")
        new_window.configure(bg=self.colors["bg_dark"])

        # Set the icon for the new Toplevel window
        if self.app_icon:
            new_window.iconphoto(True, self.app_icon) 
        
        log_frame = ttk.Frame(new_window, padding=15, style='TFrame')
        log_frame.pack(fill="both", expand=True)

        result_label = ttk.Label(log_frame, text="Result: Calculating...", 
                                 font=('Poppins', 16, 'bold'), foreground=self.colors["accent_blue"], background=self.colors["frame_bg"])
        result_label.pack(fill='x', pady=10)
        
        progress_bar = ttk.Progressbar(log_frame, mode='indeterminate', length=200)
        progress_bar.pack(fill='x', pady=5)
        progress_bar.start()

        log_text = tk.Text(log_frame, wrap='word', height=20, width=50, state='disabled', 
                           font=('Consolas', 10), bg=self.colors["log_bg"], fg=self.colors["text_color"], 
                           insertbackground=self.colors["text_color"], relief="sunken", padx=10, pady=10)
        log_text.pack(fill='both', expand=True, pady=5)
        
        self.current_log_window = new_window
        
        self.after(100, lambda: self.start_inference_process(title, algorithm_func, is_fc, result_label, progress_bar, log_text))


    def start_inference_process(self, title, algorithm_func, is_fc, result_label, progress_bar, log_text):
        
        self.fc_button.config(state='disabled')
        self.bc_button.config(state='disabled')

        initial_facts = self.get_current_facts()

        log_text.config(state='normal')
        log_text.delete('1.0', tk.END)
        log_text.insert(tk.END, f"--- Starting {title} ---\n")
        log_text.insert(tk.END, f"Initial Observations: {', '.join(initial_facts) if initial_facts else 'None'}\n\n")
        log_text.config(state='disabled')
        
        def window_update_callback(message):
            self.update_log_and_scroll(log_text, message)

        if is_fc:
            final_result, _ = algorithm_func(initial_facts, window_update_callback)
            display_result = final_result
            color = self.colors["accent_green"] if 'Unknown' not in final_result and 'Undetermined' not in final_result else 'red'
        else:
            goal = self.goal_var.get()
            is_proven = algorithm_func(goal, initial_facts, window_update_callback)
            display_result = f"Goal '{goal}' is {'PROVEN' if is_proven else 'NOT PROVEN'}."
            color = self.colors["accent_green"] if is_proven else 'red'
            
        progress_bar.stop()
        result_label.config(text=f"Result: {display_result}", foreground=color)
        window_update_callback(f"\n--- {title} FINISHED ---")

        self.fc_button.config(state='normal')
        self.bc_button.config(state='normal')


    def run_forward_chaining(self):
        self.open_log_window("FORWARD CHAINING (BFS Rule Traversal)", forward_chaining_bfs, is_fc=True)

    def run_backward_chaining(self):
        self.open_log_window("BACKWARD CHAINING (DFS Rule Traversal)", backward_chaining_dfs, is_fc=False)

# --- 4. MAIN EXECUTION ---
if __name__ == "__main__":
    app = MarineExpertSystem()
    app.mainloop()