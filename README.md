

# 🔬 UniversalLab: Automated CFD Wind Tunnel

UniversalLab is an end-to-end, web-based Computational Fluid Dynamics (CFD) solution that automates the transition from 3D CAD models to aerodynamic physics simulations. By integrating **Streamlit** for the frontend and **OpenFOAM 11** for the physics engine, it allows users to perform high-fidelity wind tunnel tests without manual terminal configuration.

---

## ⚙️ Setup & Installation

### 1. Ubuntu Environment (For Windows Users)
OpenFOAM requires a Linux environment. On Windows, use WSL (Windows Subsystem for Linux):
* Open PowerShell as Administrator and run: `wsl --install -d Ubuntu-22.04`
* After restarting and setting up your account, update the system: `sudo apt update && sudo apt upgrade -y`

### 2. OpenFOAM 11 Installation
Install OpenFOAM 11 using the official repository:
```bash
sudo add-apt-repository [http://dl.openfoam.org/ubuntu](http://dl.openfoam.org/ubuntu)
sudo apt-get update
sudo apt-get -y install openfoam11
Note: Add source /opt/openfoam11/etc/bashrc to your ~/.bashrc to load the environment automatically.
```
3. Python Environment
Create a virtual environment and install the visualization stack:

```Bash

python3 -m venv venv
source venv/bin/activate
pip install streamlit pyvista numpy stpyvista trame trame-vtk trame-simput
```
🚀 Execution Guide
Step 1: Launch the Dashboard
Run the following command in your terminal:

```Bash

streamlit run app.py\
```
Step 2: Upload & Simulate
Upload a watertight .stl model.

Click "🚀 Run Simulation".

Monitor the terminal; the process is complete when the solver displays End.

Step 3: Analyze Results
The 3D Interactive Flow View will load automatically once results are ready.

Use the Aerodynamics Report to view the Top Air Velocity.

Download the final results as a .glb file for external use.

📂 Project Structure
app.py: Web interface and GLB export logic.

Allrun: Orchestration script for the OpenFOAM solver.

system/: Configuration dictionaries for meshing and physics.

result.foam: The bridge file for reading CFD data.

⚠️ Troubleshooting
Empty Mesh: Ensure the STL model is "watertight" (no holes).

Permission Denied: Run chmod +x Allrun to allow the script to execute.

## 🚀 Execution Guide

### Step 1: Launch the Dashboard

```bash
streamlit run app.py
```

### Step 2: Upload & Simulate

- Upload a **watertight `.stl` model**
- Click **🚀 Run Simulation**
- Wait until the solver prints **End** in the terminal

### Step 3: Analyze Results

- The **3D Interactive Flow View** appears when results are ready
- Review **Top Air Velocity** in the Aerodynamics Report
- Export results as a **`.glb` file**

---

## 📂 Project Structure

```
app.py        → Web interface & GLB export logic
Allrun        → OpenFOAM solver orchestration script
system/       → Meshing & physics configuration dictionaries
result.foam   → CFD data reference file
```

---

## 🧠 The Core Project Structure (Explained Clearly)

| Folder / File       | Importance |
|---------------------|-----------|
| **app.py** | The main Streamlit app — acts as the UI *and* orchestrator that triggers CFD jobs. |
| **0/** | Initial conditions — defines inlet wind velocity (20 m/s) and pressure fields. |
| **constant/** | Physics setup — contains `transportProperties` and the `triSurface/` folder where STL geometry is stored. |
| **system/** | The CFD logic layer — includes dictionaries like `blockMeshDict`, `snappyHexMeshDict`, and `controlDict` that tell OpenFOAM how to mesh and solve the equations. |
| **Allrun** | Automation script — runs the full OpenFOAM pipeline in sequence. |
| **requirements.txt** | Lists Python dependencies such as `streamlit`, `pyvista`, and `pyvistaqt`. |
| **README.md** | Project documentation and setup guide. |

---

## ⚠️ Troubleshooting

**Empty Mesh** → Ensure the STL model is fully *watertight* (no holes)

**Permission Denied** → Allow script execution:

```bash
chmod +x Allrun
```


