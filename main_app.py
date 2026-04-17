# import tkinter as tk
# from tkinter import ttk, scrolledtext
# import subprocess
# import threading
# import sys
# import time



# def animate_arrows(canvas, arrow1, arrow2, color):
#     canvas.itemconfig(arrow1, fill=color, width=3)
#     canvas.update()
#     time.sleep(0.20)

#     canvas.itemconfig(arrow2, fill=color, width=3)
#     canvas.update()
#     time.sleep(0.20)

#     canvas.itemconfig(arrow1, fill="black", width=2)
#     canvas.itemconfig(arrow2, fill="black", width=2)
#     canvas.update()



# def run_ipc_process(command, output_box, status_label, canvas, arrow1, arrow2, ipc_label_widget):

#     ipc_mode = command[-1]   # last argument → --pipe / --queue / --shm / --shm-nolock

#     def task():
#         status_label.config(text="Running...", fg="blue")
#         output_box.delete("1.0", tk.END)

#         process = subprocess.Popen(
#             command,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )

#         for line in process.stdout:
#             output_box.insert(tk.END, line)
#             output_box.see(tk.END)

           
#             if ipc_mode == "--pipe":
#                 animate_arrows(canvas, arrow1, arrow2, "yellow")   # bottleneck demo

#             elif ipc_mode == "--queue":
#                 animate_arrows(canvas, arrow1, arrow2, "green")

#             elif ipc_mode == "--shm":
#                 animate_arrows(canvas, arrow1, arrow2, "green")    # safe with lock

#             elif ipc_mode == "--shm-nolock":
#                 animate_arrows(canvas, arrow1, arrow2, "red")      # race condition

#         process.wait()
#         status_label.config(text="Finished", fg="green")

#     threading.Thread(target=task).start()


# class DeadlockTab:
#     THINKING = "thinking"
#     HUNGRY = "hungry"
#     EATING = "eating"
#     DEADLOCK = "deadlock"

#     def __init__(self, parent):
#         self.frame = ttk.Frame(parent)
#         self.frame.pack(fill="both", expand=True)

#         tk.Label(
#             self.frame,
#             text="Deadlock Visualizer - Dining Philosophers",
#             font=("Arial", 16, "bold")
#         ).pack(pady=10)

#         self.canvas = tk.Canvas(self.frame, width=900, height=450, bg="white")
#         self.canvas.pack(pady=10)

#         # Philosopher positions
#         self.positions = [
#             (450, 100),
#             (220, 200),
#             (320, 380),
#             (580, 380),
#             (680, 200),
#         ]

#         # Circles (philosophers)
#         self.philosophers = []
#         for x, y in self.positions:
#             p = self.canvas.create_oval(x - 40, y - 40, x + 40, y + 40,
#                                         fill="lightgray", outline="black", width=2)
#             self.philosophers.append(p)

#         # State labels under philosophers
#         self.state_labels = []
#         for i, (x, y) in enumerate(self.positions):
#             t = self.canvas.create_text(
#                 x, y + 65, text=f"P{i} - thinking", font=("Arial", 11)
#             )
#             self.state_labels.append(t)

#         # Buttons
#         btn_frame = tk.Frame(self.frame)
#         btn_frame.pack(pady=15)

#         tk.Button(
#             btn_frame, text="Simulate Deadlock", width=20, height=2,
#             bg="#FF5722", fg="white", command=self.simulate_deadlock
#         ).grid(row=0, column=0, padx=20)

#         tk.Button(
#             btn_frame, text="Resolve Deadlock", width=20, height=2,
#             bg="#4CAF50", fg="white", command=self.resolve_deadlock
#         ).grid(row=0, column=1, padx=20)

#         self.running = False
#         self.deadlock_detected = False

#         # NEW: store cycle arrows so we can delete after resolve
#         self.cycle_arrows = []

#     # -------------------------------------------------
#     # UPDATE PHILOSOPHER STATE
#     # -------------------------------------------------
#     def _set_state(self, idx, state):
#         colors = {
#             self.THINKING: "lightgray",
#             self.HUNGRY: "yellow",
#             self.EATING: "lightgreen",
#             self.DEADLOCK: "red"
#         }
#         texts = {
#             self.THINKING: "thinking",
#             self.HUNGRY: "waiting",
#             self.EATING: "eating",
#             self.DEADLOCK: "deadlocked"
#         }

#         self.canvas.itemconfig(self.philosophers[idx], fill=colors[state])
#         self.canvas.itemconfig(self.state_labels[idx], text=f"P{idx} - {texts[state]}")
#         self.canvas.update()

#     def simulate_deadlock(self):
#         if self.running:
#             return
#         self.running = True
#         threading.Thread(target=self._simulate_sequence).start()

#     def _simulate_sequence(self):
#         # All become hungry → circular wait
#         for i in range(5):
#             self._set_state(i, self.HUNGRY)
#             time.sleep(0.6)

#         # Show circular arrows
#         self._show_cycle()

#         # All deadlocked
#         for i in range(5):
#             self._set_state(i, self.DEADLOCK)

#         self.deadlock_detected = True
#         self.running = False

  
#     def resolve_deadlock(self):
#         if not self.deadlock_detected:
#             return

#         import random
#         chosen = random.randint(0, 4)

#         # One philosopher eats (break cycle)
#         self._set_state(chosen, self.EATING)
#         time.sleep(0.5)

#         # Others go back to thinking
#         for i in range(5):
#             if i != chosen:
#                 self._set_state(i, self.THINKING)

#         # NEW: remove all cycle arrows
#         for a in self.cycle_arrows:
#             self.canvas.delete(a)

#         self.cycle_arrows = []
#         self.canvas.update()

#         self.deadlock_detected = False

#     def _show_cycle(self):
#         self.cycle_arrows = []

#         # create cycle arrows one by one
#         for i in range(5):
#             x1, y1 = self.positions[i]
#             x2, y2 = self.positions[(i + 1) % 5]

#             arrow = self.canvas.create_line(
#                 x1, y1, x2, y2, arrow=tk.LAST, width=3, fill="orange"
#             )
#             self.cycle_arrows.append(arrow)

#             self.canvas.update()
#             time.sleep(0.25)

#         # Flash cycle red/orange
#         for _ in range(2):
#             for a in self.cycle_arrows:
#                 self.canvas.itemconfig(a, fill="red")
#             self.canvas.update()
#             time.sleep(0.3)

#             for a in self.cycle_arrows:
#                 self.canvas.itemconfig(a, fill="orange")
#             self.canvas.update()
#             time.sleep(0.3)


# def main():
#     root = tk.Tk()
#     root.title("IPC Debugger + Deadlock Visualizer")
#     root.geometry("1200x900")

#     notebook = ttk.Notebook(root)
#     notebook.pack(fill="both", expand=True)

   
#     ipc_tab = ttk.Frame(notebook)
#     notebook.add(ipc_tab, text="IPC Debugger")

#     canvas = tk.Canvas(ipc_tab, width=1100, height=250, bg="white")
#     canvas.pack(pady=10)

#     # Process A
#     canvas.create_rectangle(70, 80, 240, 160, fill="#BDE0FE", outline="black", width=2)
#     canvas.create_text(155, 120, text="Process A", font=("Arial", 12, "bold"))

#     # IPC Box
#     ipc_box = canvas.create_rectangle(380, 80, 560, 160, fill="#FFF3B0", outline="black", width=2)
#     ipc_label = canvas.create_text(470, 120, text="IPC", font=("Arial", 12, "bold"))

#     # Process B
#     canvas.create_rectangle(700, 80, 870, 160, fill="#C4F7C3", outline="black", width=2)
#     canvas.create_text(785, 120, text="Process B", font=("Arial", 12, "bold"))

#     # Arrows A→IPC and IPC→B
#     arrow1 = canvas.create_line(240, 120, 380, 120, arrow=tk.LAST, width=2)
#     arrow2 = canvas.create_line(560, 120, 700, 120, arrow=tk.LAST, width=2)

#     # Output area
#     output_box = scrolledtext.ScrolledText(ipc_tab, height=20, width=125)
#     output_box.pack(pady=10)

#     status_label = tk.Label(ipc_tab, text="Idle", font=("Arial", 12))
#     status_label.pack()

#     # Buttons
#     btn_frame = tk.Frame(ipc_tab)
#     btn_frame.pack(pady=15)

#     buttons = [
#         ("Pipe", "--pipe", "#4CAF50", "Pipe"),
#         ("Queue", "--queue", "#2196F3", "Queue"),
#         ("SHM (Lock)", "--shm", "#FF9800", "SHM (Lock)"),
#         ("SHM (No Lock)", "--shm-nolock", "#F44336", "SHM (No Lock)"),
#     ]

#     for idx, (btn_text, cmd, color, ipc_text) in enumerate(buttons):
#         tk.Button(
#             btn_frame, text=btn_text, width=22, height=2,
#             bg=color, fg="white",
#             command=lambda c=cmd, it=ipc_text: [
#                 canvas.itemconfig(ipc_label, text=it),
#                 run_ipc_process(
#                     [sys.executable, "step1_demo.py", c],
#                     output_box, status_label, canvas, arrow1, arrow2, ipc_label
#                 )
#             ]
#         ).grid(row=0, column=idx, padx=15)

   
#     deadlock_tab = DeadlockTab(notebook)
#     notebook.add(deadlock_tab.frame, text="Deadlock Visualizer")

#     root.mainloop()


# # if __name__ == "__main__":
# #     main()

# if __name__ == "__main__":
#     main()


# import tkinter as tk
# from tkinter import ttk, scrolledtext
# import subprocess
# import threading
# import sys
# import time


# def animate_arrows(canvas, arrow1, arrow2, color):
#     canvas.itemconfig(arrow1, fill=color, width=3)
#     canvas.update()
#     time.sleep(0.20)
#     canvas.itemconfig(arrow2, fill=color, width=3)
#     canvas.update()
#     time.sleep(0.20)
#     canvas.itemconfig(arrow1, fill="black", width=2)
#     canvas.itemconfig(arrow2, fill="black", width=2)
#     canvas.update()


# def run_ipc_process(command, output_box, status_label, canvas, arrow1, arrow2, ipc_label_widget):
#     ipc_mode = command[-1]

#     def task():
#         status_label.config(text="Running...", fg="blue")
#         output_box.delete("1.0", tk.END)

#         process = subprocess.Popen(
#             command,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )

#         for line in process.stdout:
#             output_box.insert(tk.END, line)
#             output_box.see(tk.END)

#             if ipc_mode == "--pipe":
#                 animate_arrows(canvas, arrow1, arrow2, "yellow")
#             elif ipc_mode == "--queue":
#                 animate_arrows(canvas, arrow1, arrow2, "green")
#             elif ipc_mode == "--shm":
#                 animate_arrows(canvas, arrow1, arrow2, "green")
#             elif ipc_mode == "--shm-nolock":
#                 animate_arrows(canvas, arrow1, arrow2, "red")

#         process.wait()
#         status_label.config(text="Finished", fg="green")

#     threading.Thread(target=task).start()


# class DeadlockTab:
#     THINKING = "thinking"
#     HUNGRY = "hungry"
#     EATING = "eating"
#     DEADLOCK = "deadlock"

#     def __init__(self, parent):
#         self.frame = ttk.Frame(parent)
#         self.frame.pack(fill="both", expand=True)

#         tk.Label(
#             self.frame,
#             text="Deadlock Visualizer - Dining Philosophers",
#             font=("Arial", 16, "bold")
#         ).pack(pady=10)

#         self.canvas = tk.Canvas(self.frame, width=900, height=450, bg="white")
#         self.canvas.pack(pady=10)

#         self.positions = [
#             (450, 100),
#             (220, 200),
#             (320, 380),
#             (580, 380),
#             (680, 200),
#         ]

#         self.philosophers = []
#         for x, y in self.positions:
#             p = self.canvas.create_oval(
#                 x - 40, y - 40, x + 40, y + 40,
#                 fill="lightgray", outline="black", width=2
#             )
#             self.philosophers.append(p)

#         self.state_labels = []
#         for i, (x, y) in enumerate(self.positions):
#             t = self.canvas.create_text(
#                 x, y + 65,
#                 text=f"P{i} - thinking",
#                 font=("Arial", 11)
#             )
#             self.state_labels.append(t)

#         btn_frame = tk.Frame(self.frame)
#         btn_frame.pack(pady=15)

#         deadlock_btn = tk.Label(
#             btn_frame,
#             text="Simulate Deadlock",
#             bg="#FF5722",
#             fg="white",
#             width=20,
#             height=2,
#             font=("Arial", 11, "bold"),
#             relief="raised",
#             bd=3,
#             cursor="hand2"
#         )
#         deadlock_btn.grid(row=0, column=0, padx=20)
#         deadlock_btn.bind("<Button-1>", lambda e: self.simulate_deadlock())

#         resolve_btn = tk.Label(
#             btn_frame,
#             text="Resolve Deadlock",
#             bg="#4CAF50",
#             fg="white",
#             width=20,
#             height=2,
#             font=("Arial", 11, "bold"),
#             relief="raised",
#             bd=3,
#             cursor="hand2"
#         )
#         resolve_btn.grid(row=0, column=1, padx=20)
#         resolve_btn.bind("<Button-1>", lambda e: self.resolve_deadlock())

#         self.running = False
#         self.deadlock_detected = False
#         self.cycle_arrows = []

#     def _set_state(self, idx, state):
#         colors = {
#             self.THINKING: "lightgray",
#             self.HUNGRY: "yellow",
#             self.EATING: "lightgreen",
#             self.DEADLOCK: "red"
#         }

#         texts = {
#             self.THINKING: "thinking",
#             self.HUNGRY: "waiting",
#             self.EATING: "eating",
#             self.DEADLOCK: "deadlocked"
#         }

#         self.canvas.itemconfig(self.philosophers[idx], fill=colors[state])
#         self.canvas.itemconfig(self.state_labels[idx], text=f"P{idx} - {texts[state]}")
#         self.canvas.update()

#     def simulate_deadlock(self):
#         if self.running:
#             return
#         self.running = True
#         threading.Thread(target=self._simulate_sequence).start()

#     def _simulate_sequence(self):
#         for i in range(5):
#             self._set_state(i, self.HUNGRY)
#             time.sleep(0.6)

#         self._show_cycle()

#         for i in range(5):
#             self._set_state(i, self.DEADLOCK)

#         self.deadlock_detected = True
#         self.running = False

#     def resolve_deadlock(self):
#         if not self.deadlock_detected:
#             return

#         import random
#         chosen = random.randint(0, 4)

#         self._set_state(chosen, self.EATING)
#         time.sleep(0.5)

#         for i in range(5):
#             if i != chosen:
#                 self._set_state(i, self.THINKING)

#         for a in self.cycle_arrows:
#             self.canvas.delete(a)

#         self.cycle_arrows = []
#         self.canvas.update()
#         self.deadlock_detected = False

#     def _show_cycle(self):
#         self.cycle_arrows = []

#         for i in range(5):
#             x1, y1 = self.positions[i]
#             x2, y2 = self.positions[(i + 1) % 5]

#             arrow = self.canvas.create_line(
#                 x1, y1, x2, y2,
#                 arrow=tk.LAST,
#                 width=3,
#                 fill="orange"
#             )

#             self.cycle_arrows.append(arrow)
#             self.canvas.update()
#             time.sleep(0.25)

#         for _ in range(2):
#             for a in self.cycle_arrows:
#                 self.canvas.itemconfig(a, fill="red")
#             self.canvas.update()
#             time.sleep(0.3)

#             for a in self.cycle_arrows:
#                 self.canvas.itemconfig(a, fill="orange")
#             self.canvas.update()
#             time.sleep(0.3)


# def main():
#     root = tk.Tk()
#     root.title("IPC Debugger + Deadlock Visualizer")
#     root.geometry("1200x900")

#     notebook = ttk.Notebook(root)
#     notebook.pack(fill="both", expand=True)

#     ipc_tab = ttk.Frame(notebook)
#     notebook.add(ipc_tab, text="IPC Debugger")

#     canvas = tk.Canvas(ipc_tab, width=1100, height=250, bg="white")
#     canvas.pack(pady=10)

#     canvas.create_rectangle(70, 80, 240, 160, fill="#BDE0FE", outline="black", width=2)
#     canvas.create_text(155, 120, text="Process A", font=("Arial", 12, "bold"))

#     canvas.create_rectangle(380, 80, 560, 160, fill="#FFF3B0", outline="black", width=2)
#     ipc_label = canvas.create_text(470, 120, text="IPC", font=("Arial", 12, "bold"))

#     canvas.create_rectangle(700, 80, 870, 160, fill="#C4F7C3", outline="black", width=2)
#     canvas.create_text(785, 120, text="Process B", font=("Arial", 12, "bold"))

#     arrow1 = canvas.create_line(240, 120, 380, 120, arrow=tk.LAST, width=2)
#     arrow2 = canvas.create_line(560, 120, 700, 120, arrow=tk.LAST, width=2)

#     output_box = scrolledtext.ScrolledText(ipc_tab, height=20, width=125)
#     output_box.pack(pady=10)

#     status_label = tk.Label(ipc_tab, text="Idle", font=("Arial", 12))
#     status_label.pack()

#     btn_frame = tk.Frame(ipc_tab)
#     btn_frame.pack(pady=15)

#     buttons = [
#         ("Pipe", "--pipe", "#4CAF50", "Pipe"),
#         ("Queue", "--queue", "#2196F3", "Queue"),
#         ("SHM (Lock)", "--shm", "#FF9800", "SHM (Lock)"),
#         ("SHM (No Lock)", "--shm-nolock", "#F44336", "SHM (No Lock)")
#     ]

#     for idx, (btn_text, cmd, color, ipc_text) in enumerate(buttons):
#         btn = tk.Label(
#             btn_frame,
#             text=btn_text,
#             bg=color,
#             fg="white",
#             width=18,
#             height=2,
#             font=("Arial", 11, "bold"),
#             relief="raised",
#             bd=3,
#             cursor="hand2"
#         )

#         btn.grid(row=0, column=idx, padx=15)

#         def on_click(event, c=cmd, it=ipc_text):
#             canvas.itemconfig(ipc_label, text=it)
#             run_ipc_process(
#                 [sys.executable, "step1_demo.py", c],
#                 output_box,
#                 status_label,
#                 canvas,
#                 arrow1,
#                 arrow2,
#                 ipc_label
#             )

#         btn.bind("<Button-1>", on_click)
#         btn.bind("<Enter>", lambda e, b=btn: b.config(relief="sunken"))
#         btn.bind("<Leave>", lambda e, b=btn: b.config(relief="raised"))

#     deadlock_tab = DeadlockTab(notebook)
#     notebook.add(deadlock_tab.frame, text="Deadlock Visualizer")

#     root.mainloop()


# if __name__ == "__main__":
#     main()




import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import threading
import sys
import time

BG = "#1e1f26"
CARD = "#2b2d3a"


def animate_arrows(canvas, arrow1, arrow2, color):
    canvas.itemconfig(arrow1, fill=color, width=5)
    canvas.itemconfig(arrow2, fill=color, width=5)
    canvas.update()
    time.sleep(0.25)
    canvas.itemconfig(arrow1, fill="#8a8a8a", width=3)
    canvas.itemconfig(arrow2, fill="#8a8a8a", width=3)
    canvas.update()


def run_ipc_process(command, output_box, status_label, canvas, arrow1, arrow2, ipc_label):
    mode = command[-1]

    def task():
        output_box.delete("1.0", tk.END)
        status_label.config(text="● Running", fg="#00aaff")

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for line in process.stdout:
            output_box.insert(tk.END, line)
            output_box.see(tk.END)

            if mode == "--pipe":
                canvas.itemconfig(ipc_label, text="PIPE")
                animate_arrows(canvas, arrow1, arrow2, "#2ecc71")

            elif mode == "--queue":
                canvas.itemconfig(ipc_label, text="QUEUE")
                animate_arrows(canvas, arrow1, arrow2, "#3498db")

            elif mode == "--shm":
                canvas.itemconfig(ipc_label, text="SHM LOCK")
                animate_arrows(canvas, arrow1, arrow2, "#f39c12")

            elif mode == "--shm-nolock":
                canvas.itemconfig(ipc_label, text="SHM NO LOCK")
                animate_arrows(canvas, arrow1, arrow2, "#e74c3c")

        process.wait()
        status_label.config(text="● Finished", fg="#2ecc71")

    threading.Thread(target=task).start()


class App:
    def __init__(self, root):
        self.root = root
        root.title("IPC Debugger + Deadlock Visualizer")
        root.geometry("1350x920")
        root.configure(bg=BG)

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.ipc_tab = tk.Frame(notebook, bg=BG)
        notebook.add(self.ipc_tab, text="IPC Debugger")

        self.deadlock_tab = tk.Frame(notebook, bg=BG)
        notebook.add(self.deadlock_tab, text="Deadlock Visualizer")

        self.build_ipc()
        self.build_deadlock()

    def make_btn(self, parent, text, color, cmd, row, col):
        b = tk.Label(
            parent,
            text=text,
            bg=color,
            fg="white",
            font=("Arial", 12, "bold"),
            width=20,
            height=2,
            bd=2,
            relief="raised",
            cursor="hand2"
        )
        b.grid(row=row, column=col, padx=8, pady=8)
        b.bind("<Button-1>", lambda e: cmd())
        b.bind("<Enter>", lambda e: b.config(relief="sunken"))
        b.bind("<Leave>", lambda e: b.config(relief="raised"))

    def build_ipc(self):
        top = tk.Frame(self.ipc_tab, bg=BG)
        top.pack(fill="x", pady=8)

        self.canvas = tk.Canvas(
            top,
            width=1150,
            height=260,
            bg="#f8f9fa",
            highlightthickness=0
        )
        self.canvas.pack(pady=15)

        self.canvas.create_rectangle(
            70, 70, 300, 170,
            fill="#4A90E2",
            outline="#1f4e79",
            width=3
        )
        self.canvas.create_text(
            185, 95,
            text="PROCESS A",
            font=("Arial", 15, "bold"),
            fill="white"
        )
        self.canvas.create_text(
            185, 130,
            text="Sender / Producer",
            font=("Arial", 12),
            fill="white"
        )

        self.canvas.create_rectangle(
            455, 70, 695, 170,
            fill="#F5C542",
            outline="#b8860b",
            width=3
        )
        self.canvas.create_text(
            575, 95,
            text="QUEUE",
            font=("Arial", 15, "bold"),
            fill="black"
        )
        self.canvas.create_text(
            575, 130,
            text="Shared Data Channel",
            font=("Arial", 12),
            fill="black"
        )

        self.canvas.create_rectangle(
            850, 70, 1080, 170,
            fill="#58D68D",
            outline="#1e8449",
            width=3
        )
        self.canvas.create_text(
            965, 95,
            text="PROCESS B",
            font=("Arial", 15, "bold"),
            fill="white"
        )
        self.canvas.create_text(
            965, 130,
            text="Receiver / Consumer",
            font=("Arial", 12),
            fill="white"
        )

        self.arrow1 = self.canvas.create_line(
            300, 120, 455, 120,
            arrow=tk.LAST,
            width=4,
            fill="black"
        )

        self.arrow2 = self.canvas.create_line(
            695, 120, 850, 120,
            arrow=tk.LAST,
            width=4,
            fill="black"
        )

        self.ipc_label = self.canvas.create_text(
            575, 150,
            text="Select IPC Method",
            font=("Arial", 11, "bold"),
            fill="#333333"
        )

        middle = tk.Frame(self.ipc_tab, bg=BG)
        middle.pack(fill="both", expand=True, pady=8)

        left = tk.Frame(middle, bg=BG)
        left.pack(fill="both", expand=True)

        title = tk.Label(
            left,
            text="Output & Logs",
            bg=CARD,
            fg="white",
            font=("Arial", 13, "bold"),
            anchor="w",
            padx=10
        )
        title.pack(fill="x")

        self.output_box = scrolledtext.ScrolledText(
            left,
            bg="black",
            fg="white",
            insertbackground="white",
            font=("Courier", 11),
            height=18
        )
        self.output_box.pack(fill="both", expand=True)

        bottom = tk.Frame(self.ipc_tab, bg=BG)
        bottom.pack(fill="x", pady=8)

        status_bar = tk.Frame(bottom, bg=CARD)
        status_bar.pack(fill="x", pady=4)

        tk.Label(
            status_bar,
            text="Status:",
            bg=CARD,
            fg="white",
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=10)

        self.status_label = tk.Label(
            status_bar,
            text="● Idle",
            bg=CARD,
            fg="#f1c40f",
            font=("Arial", 11, "bold")
        )
        self.status_label.pack(side="left")

        btn_frame = tk.Frame(bottom, bg=BG)
        btn_frame.pack()

        self.make_btn(btn_frame, "RUN / Pipe", "#2ecc71", lambda: self.run_mode("--pipe"), 0, 0)
        self.make_btn(btn_frame, "RUN / Queue", "#3498db", lambda: self.run_mode("--queue"), 0, 1)
        self.make_btn(btn_frame, "RUN / SHM (Lock)", "#f39c12", lambda: self.run_mode("--shm"), 0, 2)
        self.make_btn(btn_frame, "RUN / SHM (No Lock)", "#e74c3c", lambda: self.run_mode("--shm-nolock"), 0, 3)

    def run_mode(self, mode):
        run_ipc_process(
            [sys.executable, "step1_demo.py", mode],
            self.output_box,
            self.status_label,
            self.canvas,
            self.arrow1,
            self.arrow2,
            self.ipc_label
        )

    def build_deadlock(self):
        tk.Label(
            self.deadlock_tab,
            text="Deadlock Visualizer",
            bg=BG,
            fg="white",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        self.dead_canvas = tk.Canvas(
            self.deadlock_tab,
            width=900,
            height=500,
            bg="white"
        )
        self.dead_canvas.pack(pady=10)

        self.positions = [
            (450, 90),
            (250, 220),
            (330, 410),
            (570, 410),
            (650, 220)
        ]

        self.nodes = []
        for i, (x, y) in enumerate(self.positions):
            node = self.dead_canvas.create_oval(
                x - 40, y - 40, x + 40, y + 40,
                fill="lightgray",
                width=2
            )
            self.nodes.append(node)
            self.dead_canvas.create_text(
                x, y,
                text=f"P{i+1}",
                font=("Arial", 12, "bold")
            )

        self.dead_info = tk.Label(
            self.deadlock_tab,
            text="Click Simulate Deadlock",
            bg=BG,
            fg="#00aaff",
            font=("Arial", 12, "bold")
        )
        self.dead_info.pack()

        btn = tk.Frame(self.deadlock_tab, bg=BG)
        btn.pack(pady=10)

        self.make_btn(btn, "Simulate Deadlock", "#e74c3c", self.sim_deadlock, 0, 0)
        self.make_btn(btn, "Resolve Deadlock", "#2ecc71", self.resolve_deadlock, 0, 1)

        self.lines = []

    def sim_deadlock(self):
        for i in range(5):
            self.dead_canvas.itemconfig(self.nodes[i], fill="red")
            self.root.update()
            time.sleep(0.4)

        self.lines = []
        for i in range(5):
            x1, y1 = self.positions[i]
            x2, y2 = self.positions[(i + 1) % 5]

            line = self.dead_canvas.create_line(
                x1, y1, x2, y2,
                arrow=tk.LAST,
                width=3,
                fill="orange"
            )
            self.lines.append(line)

        self.dead_info.config(text="Deadlock Created: Circular Wait", fg="red")

    def resolve_deadlock(self):
        for line in self.lines:
            self.dead_canvas.delete(line)

        for i in range(5):
            self.dead_info.config(text=f"P{i+1} is eating for 2 sec", fg="green")
            self.dead_canvas.itemconfig(self.nodes[i], fill="lightgreen")
            self.root.update()
            time.sleep(2)
            self.dead_canvas.itemconfig(self.nodes[i], fill="lightgray")

        self.dead_info.config(text="Deadlock Resolved Successfully", fg="#00aaff")


root = tk.Tk()
app = App(root)
root.mainloop()