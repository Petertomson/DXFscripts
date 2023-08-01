import os
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Sheet material and finish helper", page_icon="🔨")
st.title('Sheet material and finish helper')

st.write(
    'This app is designed to help you choose the sheet material and finish you should use for your CNC furniture, based on how you answer a series of questions')

reference = ['structure', 'disassembly', 'visuals', 'cost', 'enviro', 'application']

struct_ply = [3.17, 2, 2.83, 3.5, 3.5, 0]
osb = [1.33, 2, 2.33, 5, 5, 0]
marine = [3, 2.8, 3.83, 1.83, 2.5, 0]
spruce = [3.5, 2.67, 3, 3.5, 3.5, 0]
duraply = [5, 2.33, 4.5, 1, 2, 0]
birch = [2, 5, 2.83, 1, 3, 0]

struct_ply_edit = [0, 0, 0, 0, 0, 0]
osb_edit = [0, 0, 0, 0, 0, 0]
marine_edit = [0, 0, 0, 0, 0, 0]
spruce_edit = [0, 0, 0, 0, 0, 0]
duraply_edit = [0, 0, 0, 0, 0, 0]
birch_edit = [0, 0, 0, 0, 0, 0]

struct_ply_total = 0
osb_total = 0
marine_total = 0
spruce_total = 0
duraply_total = 0
birch_total = 0

material_ref_list = [struct_ply,osb,marine,spruce,duraply,birch]
material_edit_list = [struct_ply_edit,osb_edit,marine_edit,spruce_edit,duraply_edit,birch_edit]
material_total_list = [struct_ply_total,osb_total,marine_total,spruce_total,duraply_total,birch_total]
reference = ['structure', 'disassembly', 'visuals', 'cost', 'enviro', 'application']

unfinished = [1.83, 3.17, 1.83, 3.5 , 3.5, 5]
rubio =      [3.17, 3.83, 2.33, 1   , 4,  4.5]
osmo =       [3.67, 3.17, 3.17, 3   , 3,  4]
paint =      [3.83, 1,    4.83, 4   , 2,  4]
stain =      [4,    2,    4.5 , 3   , 3,  3]
varnish =    [3.83, 3.67, 3.17, 4   , 1,  4]

unfinished_edit = [0, 0, 0, 0, 0, 0]
rubio_edit = [0, 0, 0, 0, 0, 0]
osmo_edit = [0, 0, 0, 0, 0, 0]
paint_edit = [0, 0, 0, 0, 0, 0]
stain_edit = [0, 0, 0, 0, 0, 0]
varnish_edit = [0, 0, 0, 0, 0, 0]

unfinished_total = 0
rubio_total = 0
osmo_total = 0
paint_total = 0
stain_total = 0
varnish_total = 0

finish_ref_list = [unfinished,rubio,osmo,paint,stain,varnish]
finish_edit_list = [unfinished_edit,rubio_edit,osmo_edit,paint_edit,stain_edit,varnish_edit]
finish_total_list = [unfinished_total,rubio_total,osmo_total,paint_total,stain_total,varnish_total]

def stringify(i: int = 0) -> str:
    return slider_strings[i - 1]
slider_values = [1, 2, 3, 4, 5]

slider_strings = ["Bring it inside regularly", "Bring it inside during bad weather", "Take it inside for the winter", "Cover it but leave it outside", "Leave it outside uncovered year round"]
structure_slider = st.select_slider("Where will you store your furniture?",
                                    options=slider_values,
                                    value=3,
                                    format_func=stringify,
                                    help = 'This is rough idea of how much of its life your furniture will spend outside.')
st.divider()
slider_strings = ["Never", "Only to move it", "Once a year", "A few times a year", "Very regularly"]
disassembly_slider = st.select_slider("How often will you take apart your furniture?",
                                    options=slider_values,
                                    value=3,
                                    format_func=stringify,
                                    help = 'Some finishes are smoother than others and make it more convenient to dissassemble the furniture.')
st.divider()
slider_strings = ["Not important at all", "Not very important", "I don't mind either way", "Quite important", "Very important"]
visual_slider = st.select_slider("How important is it you that your furniture stays looking brand new?",
                                    options=slider_values,
                                    value=3,
                                    format_func=stringify,
                                    help = 'Clear finishes like oil or varnish will protect the furniture but might discolour or stain slightly over time.')
st.divider()
slider_strings = ["Expensive but long-lasting", "Quite expensive but robust", "Try to balance cost and longevity", "Quite cheap and quite robust", "Very cheap but short-lived"]
cost_slider = st.select_slider("More expensive sheet material can last longer. With that in mind would you like cheaper and short-lived or more expensive and long-lasting furniture",
                                    options=slider_values,
                                    value=3,
                                    format_func=stringify,
                                    help = 'There is always a balance between cost and longevity but in our experience there are some cheap products that last surprisingly well and some expensive ones that are short-lived.')
st.divider()
slider_strings = ["Doesn't matter at all", "Not very concerned", "Neutral", "Slightly concerned", "Very concerned"]
enviro_slider = st.select_slider("Some sheet materials and finishes can have a large impact on the environment and can be hazardous to use. How concerned about the products environmental impact are you?",
                                    options=slider_values,
                                    value=3,
                                    format_func=stringify,
                                    help = 'These rating are decided using the Environmental Product Declarations and Health and Safety for each of the products tested')
st.divider()
slider_strings = ["Quick but short-lived", "Relatively quick but slightly short-lived", "Try to balance speed and longevity", "Quite slow and quite robust", "Very slow but durable"]
application_slider = st.select_slider("Applying finishes can be a trade off between time and longevity. With that in mind would you like a quicker but less durable finish or a slower but more long-lasting one?",
                                    options=slider_values,
                                    value=3,
                                    format_func=stringify,
                                    help = 'Finishing furniture can be a very labourious process. If you are running a community build session we would suggest using a quicker finish to avoid having to recoat after the event finishes')

slider_list = [structure_slider, disassembly_slider, visual_slider, cost_slider, enviro_slider, application_slider]

def cross_multiply(slider_val, reference_val):
    return (slider_val * reference_val)

j = 0
while j <= 5:
    i = 0
    while i <= 5:
        material_edit_list[i][j] = cross_multiply(slider_list[j], material_ref_list[i][j])
        finish_edit_list[i][j] = cross_multiply(slider_list[j], finish_ref_list[i][j])
        i = i+1
    j = j+1

j = 0
while j <= 5:
    i = 0
    while i <=5:
        material_total_list[j] = material_total_list[j] + material_edit_list[j][i]
        finish_total_list[j] = finish_total_list[j] + finish_edit_list[j][i]
        i = i+1
    j = j+1
material_list = ["Structural plywood","OSB (oriented strand board)","Marine plywood","Spruce plywood","Duraply plywood","Birch plywood"]
winning_material_index = material_total_list.index(max(material_total_list))
if winning_material_index == 0:
    winning_material = "**Structural plywood**"
elif winning_material_index == 1:
    winning_material = "**OSB (oriented strand board)**"
elif winning_material_index == 2:
    winning_material = "**Marine plywood**"
elif winning_material_index == 3:
    winning_material = "**Spruce plywood**"
elif winning_material_index == 4:
    winning_material = "**Duraply plywood**"
elif winning_material_index == 5:
    winning_material = "**Birch plywood**"

finish_list = ['Untreated', 'Linseed oil', 'Hardwax', 'Paint', 'Wood stain', 'Varnish']
winning_finish_index = finish_total_list.index(max(finish_total_list))
if winning_finish_index == 0:
    winning_finish = "**No finish at all**"
elif winning_finish_index == 1:
    winning_finish = "**Linseed oil based treatment such as Rubio**"
elif winning_finish_index == 2:
    winning_finish = "**Hardwax based treatment such as Osmo UV-protect**"
elif winning_finish_index == 3:
    winning_finish = "**Shed paint such as Cuprinol garden shades**"
elif winning_finish_index == 4:
    winning_finish = "**Exterior wood stain such as Ronseal exterior wood stain**"
elif winning_finish_index == 5:
    winning_finish = "**Exterior grade wood varnish**"

st.divider()

st.write("The best sheet material in your context is:",winning_material, "and it should be finished with:",winning_finish)
st.divider()
st.caption('These outcomes are based on a series of on going tests conducted in Knowle West, Bristol. The following charts are visualisations of the scoring process so you can see the runners up.')


material_data = pd.DataFrame({
    'Materials': material_list,
    'Score': material_total_list,
})
material_chart_min = min(material_total_list) - 2
material_chart_max = max(material_total_list) + 2

st.altair_chart(alt.Chart(material_data).mark_bar(clip=True).encode(
    alt.X('Score', scale=alt.Scale(domain=(material_chart_min, material_chart_max))),
    y='Materials',
    color=alt.condition(
            alt.datum.Score == max(material_total_list),  # If the year is 1810 this test returns True,
            alt.value('salmon'),     # which sets the bar orange.
            alt.value('steelblue')   # And if it's not true it sets the bar steelblue.
    )
),use_container_width=True)

finish_data = pd.DataFrame({
    'Finishes': finish_list,
    'Score': finish_total_list,
})
finish_chart_min = min(finish_total_list) - 2
finish_chart_max = max(finish_total_list) + 2

st.altair_chart(alt.Chart(finish_data).mark_bar(clip=True).encode(
    alt.X('Score', scale=alt.Scale(domain=(finish_chart_min, finish_chart_max))),
    y='Finishes',
    color=alt.condition(
            alt.datum.Score == max(finish_total_list),  # If the year is 1810 this test returns True,
            alt.value('salmon'),     # which sets the bar orange.
            alt.value('steelblue')   # And if it's not true it sets the bar steelblue.
    )
),use_container_width=True)

