#🧠 IPC Debugger Tool

#Inter-Process Communication Debugging Simulator (CSE-316 Project)

📌 Overview

The IPC Debugger Tool is a Python-based GUI simulator that visualizes different Inter-Process Communication (IPC) mechanisms. It enables users to observe how processes communicate and synchronize in real time.

The tool demonstrates:

Pipes
Message Queues
Shared Memory
Deadlock scenarios

It is designed to help students understand complex OS concepts like process states, synchronization, and race conditions through interactive visualization.

🚀 Features
🎯 Interactive GUI-based simulation
🔄 Real-time process communication visualization
📡 IPC mechanisms supported:
Pipe Simulation
Message Queue Simulation
Shared Memory Simulation
⚠️ Deadlock visualization (deadlock_visualizer.py)
🧵 Process state tracking
🔐 Synchronization and race condition demonstration
🛠️ Technologies Used
Python 3
Tkinter (GUI)
Multiprocessing & OS concepts
Custom simulation logic
📂 Project Structure
IPC-Debugger/
│
├── main_app.py              # Main application logic
├── main_gui.py              # GUI controller
├── visual_gui.py            # Visualization UI
├── visual_gui_step4.py      # Enhanced UI version
├── deadlock_visualizer.py   # Deadlock simulation
│
├── pipe_simulation.py
├── message_queue_sim.py
├── shared_memory_sim.py
│
├── step1_demo.py            # Demo/testing script
├── requirement.txt          # Dependencies
└── README.md
⚙️ Installation
Clone the repository:
git clone https://github.com/Ashwin-yadav24/IPC-Debugger-Inter-Process-Communication-Debugging-CSE-316-project.git
cd IPC-Debugger-Inter-Process-Communication-Debugging-CSE-316-project
Install dependencies:
pip install -r requirement.txt
Run the project:
python main_app.py
🧪 How It Works
Launch the GUI
Select an IPC method
Create processes
Perform communication
Observe:
Data transfer
Process states
Synchronization
Deadlocks
