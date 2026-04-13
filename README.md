# 🧠 IPC Debugger Tool  
### Inter-Process Communication Debugging Simulator (CSE-316 Project)

---

## 📌 Overview
The **IPC Debugger Tool** is a Python-based GUI simulator that helps visualize **Inter-Process Communication (IPC)** mechanisms.

It allows users to understand how processes communicate and synchronize using:
- Pipes  
- Message Queues  
- Shared Memory  
- Deadlock visualization  

This project is designed for **Operating System learning** with real-time interactive debugging.

---

## 🚀 Features

- 🎯 Interactive GUI simulation  
- 🔄 Real-time communication visualization  
- 📡 Supports:
  - Pipes
  - Message Queues
  - Shared Memory  
- ⚠️ Deadlock visualization  
- 🧵 Process state tracking  
- 🔐 Race condition & synchronization demo  

---

## 🛠️ Tech Stack

- **Python 3**
- **Tkinter (GUI)**
- **Multiprocessing concepts**

---

## 📂 Project Structure
IPC-Debugger/
│
├── main_app.py
├── main_gui.py
├── visual_gui.py
├── visual_gui_step4.py
├── deadlock_visualizer.py
│
├── pipe_simulation.py
├── message_queue_sim.py
├── shared_memory_sim.py
│
├── step1_demo.py
├── requirement.txt
└── README.md


---

## ⚙️ Installation
git clone https://github.com/Ashwin-yadav24/IPC-Debugger-Inter-Process-Communication-Debugging-CSE-316-project.git
cd IPC-Debugger-Inter-Process-Communication-Debugging-CSE-316-project
pip install -r requirement.txt
python main_app.py


## 🧪 How to Use
Run the application
Select IPC method
Create processes
Send/receive data
Observe:
Process states
Data flow
Deadlocks
Synchronization
## 👥 Team Members
Kumar Yashansh
Himanshu Kumar
Ashwin Kumar Yadav
## 📊 Use Cases
OS Lab Project
IPC Learning
Debugging simulations
Academic demonstrations
## ⚠️ Limitations
Not a real OS-level debugger
Limited scalability
GUI depends on system performance
🔮 Future Improvements
Socket-based IPC
Distributed simulation
Better UI animations
Execution timeline


