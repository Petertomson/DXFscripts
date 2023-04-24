import os
import ezdxf
import streamlit as st

st.set_page_config(page_title="DXF Viewer", page_icon="📐")
st.title('DXF adjuster')

st.write('This app is designed to help adjust drawings so friction joints are not too tight or too loose. To do this the app scales the drawing.')
uploaded_file = st.file_uploader("To start choose a .dxf file", type=['dxf'])

if uploaded_file is not None:
    fullname = uploaded_file.name
    folder_path = '.'
    uploaded_file_path = os.path.join(folder_path, uploaded_file.name)
    with open(os.path.join(folder_path, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
if uploaded_file is not None:
    #After uploading ask the user for the values for their sheet material and drawing. The decimal input option
    ply_thickness = st.number_input('Enter the thickness of the sheet material you are cutting: ', 0.0, 200.0, 18.0, 0.01)
    drawing_thickness = st.number_input('Enter the width of the slots in your drawing as a decimal: ', 0.0, 200.0, 18.0, 0.01)

    #Finish choices
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

    #Sort out adjustment values#
    adjust_val = (ply_thickness - finish_adjust) / drawing_thickness
    adjust_number = drawing_thickness - ply_thickness + finish_adjust

    if adjust_number < 0:
        st.write('Your joints in your drawing will be increased by: ', adjust_number*-1, 'mm')
    elif adjust_number == 0:
        st.write('Your joints in your drawing will not be changed')
    else:
        st.write('Your joints in your drawing will be reduced by: ', adjust_number, 'mm')

    # button to start converting process
    if st.button('Adjust .DXF'):
        if uploaded_file is not None:
            #Read the file using ezdxf
            doc = ezdxf.readfile(uploaded_file_path)

            # Select all elements and scale
            st.write('Your drawing will be scaled by ', adjust_val)
            for entity in doc.modelspace():
                entity.scale(adjust_val, adjust_val, 1)
            #Sort out the file name
            basename = uploaded_file_path.removesuffix('.dxf')
            uploaded_file_mod = basename + " " + str(adjust_number) + "mm.dxf"
            doc.saveas(uploaded_file_mod)
            #Load the binary data from the file as f then add it to a download button
            with open(uploaded_file_mod, 'rb') as f:
                st.download_button('Download adjusted file', f,  uploaded_file_mod)
