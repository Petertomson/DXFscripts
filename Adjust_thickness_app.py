import os
import ezdxf
import streamlit as st
import io
import pandas as pd
from io import StringIO
import numpy as np
from pathlib import Path


st.set_page_config(page_title="DXF Viewer", page_icon="📐")
st.title('DXF adjuster')

#print("This script adjusts the scale of all drawings in a folder to match the thickness of the ply you have")

uploaded_file = st.file_uploader("Choose a .dxf file",type=['dxf'])

if uploaded_file is not None:
    fullname = uploaded_file.name
    folder_path = '.'
    uploaded_file_path = os.path.join(folder_path, uploaded_file.name)
    st.write(uploaded_file_path)
    with open(os.path.join(folder_path, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
if uploaded_file is not None:
    ply_thickness_str = st.text_input('Ply thickness', '18')

    drawing_thickness = st.number_input('Enter the width of the slots in your drawing as a decimal: ', 18)

    ply_thickness = float(ply_thickness_str)

    finish_option = st.selectbox(
        'What finish are you going to use?',
        ('Varnish', 'Stain', 'Oil', 'Osmo', 'None'))
    if finish_option == 'None':
        finish_adjust = 0.0
    elif finish_option == 'Stain':
        finish_adjust = 0.25
    elif finish_option == 'Oil':
        finish_adjust = 0.04
    elif finish_option == 'Osmo':
        finish_adjust = 0.08
    elif finish_option == 'Varnish':
        finish_adjust = 0.1

    st.write('Your finish will add: ', finish_adjust, 'mm')

    adjust_val = (ply_thickness - finish_adjust) / drawing_thickness
    adjust_number = drawing_thickness - ply_thickness + finish_adjust
    st.write('Your joints in your drawing will be adjusted by: ', adjust_number, 'mm')
    # Prompt the user for a folder path
    #uploaded_file = input("Please select a .dxf file: ")
    # Check dxf then adjust
    # Construct the full file path
    #file_path = os.path.join(uploaded_file)
    #file_base = file_path.removesuffix('.dxf')

    # Open the file with ezdxf
    if st.button('Adjust .DXF'):
        if uploaded_file is not None:
            #st.write(uploaded_file)
            doc = ezdxf.readfile(uploaded_file_path)

            # Select all elements and scale
            st.write('Your drawing will be scaled by ', adjust_val)
            for entity in doc.modelspace():
                entity.scale(adjust_val, adjust_val, 1)

            # Set the units to mm
            # doc.header['$INSUNITS'] = ezdxf.lldxf.UNITS['mm']
            basename = uploaded_file_path.removesuffix('.dxf')
            uploaded_file_mod = basename + " " + str(adjust_number) + "mm.dxf"
            doc.saveas(uploaded_file_mod)
            with open(uploaded_file_mod, 'rb') as f:
                st.download_button('Download adjusted file',f ,  uploaded_file_mod)

#print("Batch processing complete.")