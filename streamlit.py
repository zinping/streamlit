import streamlit as st
import subprocess

def run_pyqt_app():
    subprocess.Popen(["python", "graph-food-v6.py"])

st.title("Click the button below to view the charts")

if st.button("Show Charts"):
    run_pyqt_app()
    st.write("PyQt application launched!")
