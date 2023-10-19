import os
import ezdxf
import streamlit as st

st.set_page_config(page_title="DXF Adjuster", page_icon="📐")
st.title('DXF adjuster')

st.write('This app is designed to help adjust drawings so friction joints are not too tight or too loose. To do this the app scales the drawing. Some of the values in the this script are visually rounded for brevity - this does not affect the accuracy.')
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
    measurement_bool = st.selectbox('Is the file you are using in **Metric** or **Imperial** measurements', ('Metric','Imperial'),0, help = 'Metric measurements are usually millimeters (mm) Imperial measurements are usually Inches (\"\")')
    if measurement_bool == 'Imperial':
        conversion_bool = st.selectbox('Would you like to convert it to metric?', ('Yes', 'No'), 1)
    else:
        conversion_bool = st.selectbox('Would you like to convert it to imperial?', ('Yes', 'No'), 1)

    if measurement_bool == 'Imperial' and conversion_bool == 'Yes':
        measurement_tag = 'mm'
        ply_default = 18.0
        drawing_default = .75
        metric_to_imperial_toggle = 1
        convert_factor= 25.4
        file_conversion_tag = ' converted to metric'
        material_units = '**Metric**'
        drawing_units = 'its original **Imperial**'
        st.write('**Converting to metric will scale your drawing by 25.4**')
    elif measurement_bool == 'Imperial' and conversion_bool == 'No':
        measurement_tag = 'inches'
        ply_default = .75
        drawing_default = .75
        metric_to_imperial_toggle = 0.0394
        convert_factor = 1
        file_conversion_tag = ''
        material_units = 'Imperial'
        drawing_units = 'Imperial'
    elif measurement_bool == 'Metric' and conversion_bool == 'Yes':
        measurement_tag = 'inches'
        ply_default = .75
        drawing_default = 18.0
        metric_to_imperial_toggle = 0.0394
        convert_factor = 0.0394
        st.write('**Converting to imperial will scale your drawing by 0.0394**')
        file_conversion_tag = ' converted to imperial'
        material_units = '**Imperial**'
        drawing_units = 'its original **Metric**'
    elif measurement_bool == 'Metric' and conversion_bool == 'No':
        measurement_tag = 'mm'
        ply_default = 18.0
        drawing_default = 18.0
        convert_factor = 1
        metric_to_imperial_toggle = 1
        file_conversion_tag = ''
        material_units = 'Metric'
        drawing_units = 'Metric'
    drawing_thickness = st.number_input(
        'Enter the width of the friction joints in your drawing as a decimal in ' + drawing_units + ' measurements:', 0.0, 200.0,
        drawing_default, 0.01, help = 'Friction joints are slots in the drawing designed to be knocked together with a mallet')
    st.divider()
    st.write('**Sheet material thickness can vary a lot even over one sheet! The ideal method is to measure your sheet material with calipers in several places and average the result**')
    ply_thickness = st.number_input(('Enter the thickness of the sheet material you are cutting as a decimal in ' + material_units + ' measurements:'), 0.0, 200.0, ply_default, 0.01, help = 'Sheet material thickness can vary a lot even over one sheet! The ideal method is to measure your sheet material with calipers in several places and average the result')

    st.write('**Avoid splitting parts across different sheets as the thickness scaling might cause the friction joins not to fit! Also take care when cutting multiple versions of the same item not to mix of parts that have been scaled differently.**')

    #Finish choices
    #finish_option = st.selectbox(
    #    'What finish are you going to use?',
    #    ('None', 'Stain', 'Oil', 'Osmo', 'Varnish'))
    #if finish_option == 'None':
    #    finish_adjust = round(0.0 * metric_to_imperial_toggle,4)
    #elif finish_option == 'Stain':
    #    finish_adjust = round(0.25 * metric_to_imperial_toggle,4)
    #elif finish_option == 'Oil':
    #    finish_adjust = round(0.04 * metric_to_imperial_toggle,4)
    #elif finish_option == 'Osmo':
    #    finish_adjust = round(0.08 * metric_to_imperial_toggle,4)
    #elif finish_option == 'Varnish':
    #    finish_adjust = round(0.1 * metric_to_imperial_toggle,4)
    finish_adjust = 0
    #st.write('Your finish will add: ', finish_adjust, measurement_tag)
    st.divider()
    custom_adjust_str = st.select_slider(
        'Customise the fit',
        options=['Very tight', 'Tight', 'Slightly tight', 'No change', 'Slightly loose', 'Loose', 'Very loose'], value ='No change', help = 'This slider will slightly increase or reduce the slot width to made the joints stiffer or looser')
    if custom_adjust_str == 'Very tight':
        custom_adjust = round(-0.3 * metric_to_imperial_toggle,4)
    elif custom_adjust_str == 'Tight':
        custom_adjust = round(-0.2 * metric_to_imperial_toggle,4)
    elif custom_adjust_str == 'Slightly tight':
        custom_adjust = round(-0.1 * metric_to_imperial_toggle,4)
    elif custom_adjust_str == 'No change':
        custom_adjust = round(0.0 * metric_to_imperial_toggle,4)
    elif custom_adjust_str == 'Slightly loose':
        custom_adjust = round(0.1 * metric_to_imperial_toggle,4)
    elif custom_adjust_str == 'Loose':
        custom_adjust = round(0.2 * metric_to_imperial_toggle,4)
    elif custom_adjust_str == 'Very loose':
        custom_adjust = round(0.3 * metric_to_imperial_toggle,4)

    st.write('This will change the joints by ', custom_adjust, measurement_tag)
    st.divider()
    #Sort out adjustment values#
    adjust_val = (ply_thickness * convert_factor - finish_adjust + custom_adjust) / (drawing_thickness * convert_factor)
    adjust_number = (drawing_thickness * convert_factor - ply_thickness) + finish_adjust - custom_adjust

    if measurement_bool == 'Imperial' and conversion_bool == 'Yes':
        if adjust_number < 0:
            st.write('Your drawing will be converted to metric and the joints will be increased by: ', round(adjust_number * -1, 4), measurement_tag)
        elif adjust_number == 0:
            st.write('Your drawing will be converted to metric and the joints will not be changed')
        else:
            st.write('Your drawing will be converted to metric and the joints will be reduced by: ', round(adjust_number, 4), measurement_tag)
    elif measurement_bool == 'Imperial' and conversion_bool == 'No':
        if adjust_number < 0:
            st.write('The joints in your drawing will be increased by: ', round(adjust_number  * -1, 4), measurement_tag)
        elif adjust_number == 0:
            st.write('The joints in your drawing will not be changed')
        else:
            st.write('The joints in your drawing will be reduced by: ', round(adjust_number, 4), measurement_tag)
    elif measurement_bool == 'Metric' and conversion_bool == 'Yes':
        if adjust_number < 0:
            st.write('Your drawing will be converted to imperial and the joints will be increased by: ', round(adjust_number * -1, 4), measurement_tag)
        elif adjust_number == 0:
            st.write('Your drawing will be converted to imperial and the joints will not be changed')
        else:
            st.write('Your drawing will be converted to imperial and the joints will be reduced by: ', round(adjust_number, 4), measurement_tag)
    elif measurement_bool == 'Metric' and conversion_bool == 'No':
        if adjust_number < 0:
            st.write('The joints in your drawing will be increased by: ', round(adjust_number * -1, 4), measurement_tag)
        elif adjust_number == 0:
            st.write('The joints in your drawing will not be changed')
        else:
            st.write('The joints in your drawing will be reduced by: ', round(adjust_number, 4), measurement_tag)

    # button to start converting process
    if adjust_val != 1:
        st.write('Altogether your drawing will be scaled by ', round(adjust_val, 3))
        if st.button('Adjust .DXF'):
            if uploaded_file is not None:
                #Read the file using ezdxf
                doc = ezdxf.readfile(uploaded_file_path)

                # Select all elements and scale
                for entity in doc.modelspace():
                    entity.scale(adjust_val, adjust_val, 1)
                #Sort out the file name
                basename = uploaded_file_path.removesuffix('.dxf')
                uploaded_file_mod = basename + file_conversion_tag + " " + str(round(drawing_thickness - adjust_number,3)) + measurement_tag +".dxf"
                doc.saveas(uploaded_file_mod)
                #Load the binary data from the file as f then add it to a download button
                with open(uploaded_file_mod, 'rb') as f:
                    st.download_button('Download adjusted file', f,  uploaded_file_mod)
                    st.balloons()