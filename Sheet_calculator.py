import os
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Sheet Material Calculator", page_icon="🔨")
st.title('Sheet Material Calculator')

st.write(
    'This app is designed to help you calculate the amount of sheet material you will need to make your community owned CNC furniture and give you a rough idea of cost.')

reference = ['structure', 'disassembly', 'visuals', 'cost', 'enviro', 'application']

struct_ply =1
osb =       1
marine =    1
spruce =    1
duraply =   1
birch =     1

unfinished = 1
rubio =      1
osmo =       1
paint =      1
stain =      1
varnish =    1

bench_sheets = 1
table_sheets = 1
chair_sheets = 1
rocking_sheets = 1
hedgehog_sheets = 1
library_sheets = 1

bench_quant = st.number_input("Number of benches", value=int, placeholder="0")
table_quant = st.number_input("Number of tables", value=int, placeholder=0)
chair_quant = st.number_input("Number of chairs", value=int, placeholder=0)
rocking_quant = st.number_input("Number of rocking chairs", value=int, placeholder=0)
hedgehog_quant = st.number_input("Number of hedgehog houses", value=int, placeholder=0)
library_quant = st.number_input("Number of sharing libraries", value=int, placeholder=0)

material_select_str = st.radio(
    "What sheet material are you going to use",
    ["Structural plywood", "OSB", "Marine plywood","Spruce plywood","Duraply","Birch plywood"],
    captions = ["Softwood builders ply", "Oriented Strand Board", "","","Tanalised plywood",""])

if material_select_str == "Structural plywood" :
    material_cost = 1
elif material_select_str == "OSB" :
    material_cost = 2
elif material_select_str == "Marine plywood" :
    material_cost = 3
elif material_select_str == "Spruce plywood" :
    material_cost = 4
elif material_select_str == "Duraply" :
    material_cost = 5
elif material_select_str == "Birch plywood" :
    material_cost = 6

total_sheets = (bench_sheets*bench_quant)+(table_sheets*table_quant)+(chair_sheets*chair_quant)+(rocking_sheets*rocking_quant)+(hedgehog_sheets*hedgehog_quant)+(library_sheets*library_quant)
total_cost = material_cost*total_sheets

st.write("The total number of sheets is:",total_sheets, "and it should cost roughly:",total_cost)



