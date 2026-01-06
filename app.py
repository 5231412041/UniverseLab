import streamlit as st
import subprocess
import os
import pyvista as pv
import numpy as np
import base64

st.set_page_config(page_title="UniversalLab", layout="wide")
st.title("🔬 UniversalLab")

# --- SIMULATION SECTION (UNTOUCHED - WE KNOW THIS WORKS!) ---
uploaded_file = st.file_uploader("Upload 3D Car Model", type=['stl'])

if uploaded_file is not None:
    os.makedirs("constant/triSurface", exist_ok=True)
    with open("constant/triSurface/car.stl", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    if st.button("🚀 Run Simulation"):
        with st.spinner("Physics Engine Running... Check terminal for progress."):
            process = subprocess.Popen(["/bin/bash", "./Allrun"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            while True:
                line = process.stdout.readline()
                if not line: break
                print(line.strip())
            process.wait()

    # --- THE FIXED "STATIC 3D" VISUALIZATION ---
    if os.path.exists("result.foam"):
        st.divider()
        col1, col2 = st.columns([3, 1])
        
        try:
            # 1. Load results
            reader = pv.POpenFOAMReader("result.foam")
            reader.enable_all_patch_arrays()
            reader.set_active_time_value(reader.time_values[-1])
            mesh = reader.read()
            
            # 2. Render to a GLB file (Standard 3D format)
            # off_screen=True prevents the plotter from trying to start a server loop
            plotter = pv.Plotter(off_screen=True)
            plotter.set_background("#111111")
            
            if "car" in mesh["boundary"].keys():
                plotter.add_mesh(mesh["boundary"]["car"], color="white", smooth_shading=True)
            
            # 3. Add Airflow Tubes (Crucial for GLB visibility)
            streamlines = mesh["internalMesh"].streamlines(
                vectors="U", 
                n_points=100,
                source_center=(0, 0, 1.0),
                source_radius=2.0
            )
            # We turn lines into 'tubes' so they are solid 3D objects in the viewer
            plotter.add_mesh(streamlines.tube(radius=0.015), scalars="U", cmap="turbo")
            plotter.view_isometric()
            
            # Export to binary GLB format
            plotter.export_gltf("view.glb")
            
            # 4. Show in Browser using Google Model-Viewer
            with col1:
                st.subheader("3D Interactive Flow View")
                with open("view.glb", "rb") as f:
                    data = f.read()
                    b64 = base64.b64encode(data).decode()
                
                # This HTML component is 100% stable because it runs in the browser, not Python
                st.components.v1.html(
                    f"""
                    <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
                    <model-viewer src="data:model/gltf-binary;base64,{b64}" 
                                  style="width: 100%; height: 550px; background-color: #111;" 
                                  camera-controls auto-rotate shadow-intensity="1">
                    </model-viewer>
                    """,
                    height=600,
                )

            with col2:
                st.header("📊 Aerodynamics")
                u_data = mesh["internalMesh"]["U"]
                u_max = np.max(np.linalg.norm(u_data, axis=1))
                st.metric("Top Air Velocity", f"{u_max:.2f} m/s")
                st.download_button("💾 Download 3D Model (.glb)", data, file_name="audi_flow_results.glb")

        except Exception as e:
            st.error(f"Visualization Engine Error: {e}")
