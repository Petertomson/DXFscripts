import os
import ezdxf
import streamlit as st
import zipfile

st.set_page_config(page_title="Batch DXF Viewer", page_icon="📐")
st.title('Batch DXF adjuster')

st.write('This app is designed to help adjust drawings so friction joints are not too tight or too loose. To do this the app scales the drawing. Using the information you have given the app will create a set of 10 variants which you can then download')
uploaded_file = st.file_uploader("To start choose a .dxf file", type=['dxf'])
st.divider()
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
        ('None', 'Stain', 'Oil', 'Osmo', 'Varnish'))
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
    st.divider()
    custom_adjust_str = st.select_slider(
        'Customise the fit',
        options=['Very tight', 'Tight', 'Slightly tight', 'No change', 'Slightly loose', 'Loose', 'Very loose'], value='No change')
    if custom_adjust_str == 'Very tight':
        custom_adjust = -0.3
    elif custom_adjust_str == 'Tight':
        custom_adjust = -0.2
    elif custom_adjust_str == 'Slightly tight':
        custom_adjust = -0.1
    elif custom_adjust_str == 'No change':
        custom_adjust = 0.0
    elif custom_adjust_str == 'Slightly loose':
        custom_adjust = 0.1
    elif custom_adjust_str == 'Loose':
        custom_adjust = 0.2
    elif custom_adjust_str == 'Very loose':
        custom_adjust = 0.3

    st.write('This will change the joints by ', custom_adjust, 'mm')
    st.divider()
    #Sort out adjustment values#
    #adjust_val = (ply_thickness - finish_adjust + custom_adjust) / drawing_thickness


    #if adjust_number < 0:
    #    st.write('Altogether the joints in your drawing will be increased by: ', round(adjust_number*-1,2), 'mm')
    #elif adjust_number == 0:
    #    st.write('Your drawing will not be changed')
    #else:
    #    st.write('Altogether the joints in your drawing will be reduced by: ', round(adjust_number,2), 'mm')

    # button to start converting process
    if st.button('Adjust .DXF'):
        if uploaded_file is not None:
            #Read the file using ezdxf
            #doc = ezdxf.readfile(uploaded_file_path)

            # Select all elements and scale
            #st.write('Your drawing will be scaled by ', round(adjust_val,3))
            #for entity in doc.modelspace():
                #entity.scale(adjust_val, adjust_val, 1)
            #Sort out the file name
            basename = uploaded_file_path.removesuffix('.dxf')

            file_list = []
            j = -5

            while j <=5:

                doc = ezdxf.readfile(uploaded_file_path)
                # Select all elements and scale
                adjust_val = (ply_thickness - finish_adjust + custom_adjust + (j /20)) / drawing_thickness
                adjust_number = drawing_thickness - ply_thickness + finish_adjust - custom_adjust + (j/20)
                for entity in doc.modelspace():
                    entity.scale(adjust_val, adjust_val, 1)

                # Set the units to mm
                # doc.header['$INSUNITS'] = ezdxf.lldxf.UNITS['mm']

                if j < 0:
                    uploaded_file_mod = basename + " " + str(ply_thickness) + "mm " + str(round(adjust_number, 2)) + "mm (" + str(j/20) + " variant).dxf"
                elif j == 0:
                    uploaded_file_mod = basename + " " + str(ply_thickness) + "mm " + str(round(adjust_number, 2)) + " (base).dxf"
                else:
                    uploaded_file_mod = basename + " " + str(ply_thickness) + "mm " + str(round(adjust_number, 2)) + "mm (+" + str(j/20) + " variant).dxf"
                doc.saveas(uploaded_file_mod)
                file_list.append(uploaded_file_mod)
                j = j + 1

            with zipfile.ZipFile('Adjusted_files.zip', 'w') as f:
                for x in file_list:
                    f.write(x)
            f.close()

            adjust_number = drawing_thickness - ply_thickness + finish_adjust - custom_adjust
            if adjust_number < 0:
                st.write('Altogether the joints in your drawing will be increased by: ', round(adjust_number * -1, 2),'mm and 10 variants both smaller and larger will be created')
            elif adjust_number == 0:
                st.write('Your drawing will not be changed but 10 variants both smaller and larger will be created')
            else:
                st.write('Altogether the joints in your drawing will be reduced by: ', round(adjust_number, 2), 'mm and 10 variants both smaller and larger will be created')

            #Load the binary data from the file as f then add it to a download button
            with open('Adjusted_files.zip', 'rb') as f:
                st.download_button('Download adjusted file', f,  'Adjusted_files.zip')
                st.balloons()
