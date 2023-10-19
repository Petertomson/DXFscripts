import os
import streamlit as st

st.set_page_config(page_title="Sheet Material Calculator", page_icon="🖌️")
st.title('Sheet Material Calculator')

st.write(
    'This app is designed to help you calculate the amount of sheet material you will need to make your community owned CNC furniture and give you a rough idea of cost.')
st.write("Here is another app to help you choose the best material and finish for your project [Click here](https://petertomson-dxfscripts-material-chooser-cs317k.streamlit.app/)")

unfinished = 1
rubio =      1
osmo =       1
paint =      1
stain =      1
varnish =    1

bench_sheets = 1
table_sheets = .5
chair_sheets = 1
rocking_sheets = 1
hedgehog_sheets = .5
library_sheets = .5
planter_sheets = 0.5

bench_paintable = 3.523
table_paintable = 1.805
chair_paintable = 2.498
rocking_paintable = 3.656
hedgehog_paintable = 1.915
library_paintable = 2.514
planter_paintable = 2.631

bench_quant = st.number_input('Number of benches', min_value=0, max_value=10, value=0, step=1)
table_quant = st.number_input("Number of tables", min_value=0, max_value=10, value=0, step=1)
chair_quant = st.number_input("Number of chairs", min_value=0, max_value=10, value=0, step=1)
rocking_quant = st.number_input("Number of rocking chairs", min_value=0, max_value=10, value=0, step=1)
hedgehog_quant = st.number_input("Number of hedgehog houses", min_value=0, max_value=10, value=0, step=1)
library_quant = st.number_input("Number of sharing libraries", min_value=0, max_value=10, value=0, step=1)
planter_quant = st.number_input("Number of planters", min_value=0, max_value=10, value=0, step=1)


material_select_str = st.radio(
    "What sheet material are you going to use",
    ["Structural plywood", "OSB","Duraply", "Marine plywood","Spruce plywood","Birch plywood"],
    captions=["Softwood builders ply", "Oriented Strand Board", "Tanalised plywood","   ","  ","   "]
)

if material_select_str == "Structural plywood" :
    material_cost = 37.5
elif material_select_str == "OSB" :
    material_cost = 24
elif material_select_str == "Marine plywood" :
    material_cost = 75
elif material_select_str == "Spruce plywood" :
    material_cost = 45
elif material_select_str == "Duraply" :
    material_cost = 95
elif material_select_str == "Birch plywood" :
    material_cost = 95

finish_select_str = st.radio(
    "What type of finish are you going to use",
    ["Unfinished", "Rubio monocoat", "Osmo UV protect","Exterior paint","Exterior stain","Exterior varnish"],
    captions = ["  ", "Linseed oil based", "Oil and wax based finish"," Such as Cuprinol","Such as Ronseal","Such as yacht varnish"]
)

if finish_select_str == "Unfinished" :
    finish_cost = 37.5
    coat_multiplier = 0
    coat_coverage = 0
elif finish_select_str == "Rubio monocoat" :
    finish_cost = 6.21
    coat_multiplier = 1
    coat_coverage = 20
elif finish_select_str == "Osmo UV protect" :
    finish_cost = 4.04
    coat_multiplier = 2
    coat_coverage = 9
elif finish_select_str == "Exterior paint" :
    finish_cost = 1.33
    coat_multiplier = 2
    coat_coverage = 12
elif finish_select_str == "Exterior stain" :
    finish_cost = 4
    coat_multiplier = 3
    coat_coverage = 6
elif finish_select_str == "Exterior varnish" :
    finish_cost = 1.06
    coat_multiplier = 2
    coat_coverage = 17

total_sheets = (bench_sheets*bench_quant)+(table_sheets*table_quant)+(chair_sheets*chair_quant)+(rocking_sheets*rocking_quant) + (hedgehog_sheets * hedgehog_quant) + (library_sheets * library_quant + (planter_sheets * planter_quant))
total_paintable = (bench_paintable*bench_quant)+(table_paintable*table_quant)+(chair_paintable*chair_quant)+(rocking_paintable*rocking_quant)+(hedgehog_paintable*hedgehog_quant) + (library_paintable * library_quant) + (planter_paintable * planter_quant)

total_paint_cost = total_paintable * finish_cost
upper_paint_cost = 1.2 * total_paint_cost
lower_paint_cost = 0.8 * total_paint_cost

total_material_cost = material_cost * total_sheets
upper_material_cost = 1.2 * total_material_cost
lower_material_cost = 0.8 * total_material_cost


if total_sheets != 0.0:
    st.write("The total number of 1220x2440mm sheets required is:",str(total_sheets))
    if finish_select_str != "Unfinished":
        st.write("The total area that needs finish is:",str(round(total_paintable,3)),"m2. Your chosen finish needs",str(coat_multiplier),"layers of finish")
    st.divider()
    st.write("**What follows is not a costing - it's just a ballpark figure of the price you can expect to pay.** It does not include the labour to apply finishes (it's more fun to have a painting party anyway!)")
    st.divider()
    st.write("The raw materials should cost roughly between: £",str('%.2f' % lower_material_cost), "and £",str('%.2f' % upper_material_cost))
    st.write("Each piece of furniture takes roughly an hour to cut (highly dependant on the individual machine) with duplicates being slightly quicker. Expect to pay between £50 and £100 per hour to rent a CNC machine and operator.")
    if finish_select_str != "Unfinished" :
        st.write("Based on the advertised coverage of your finish choice you should need",str(round(total_paintable/(coat_coverage * 1.1)*coat_multiplier,3)),"litre(s) of finish. Which should cost somewhere between £",str('%.0f' % lower_paint_cost), "and £",str('%.f' % upper_paint_cost), "This is the advertised coverage of the finish - most painters will use more than this amount.")
#this not a costing
#boundaries of cost
#ex finishings
#£50-100 per hour (minimum charges)



