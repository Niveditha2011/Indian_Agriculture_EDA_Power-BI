import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector

connection = mysql.connector.connect(
  host = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
  port = 4000,
  user = "2XWsHPpwQA4Z6ce.root",
  password = "lFu7DqRUZThvq3kn",
  database = "Retail_Project",
 
)
mycursor=connection.cursor()

df = pd.read_csv(r"C:\Users\Python Class\Agridata_Project2\cleaned_agriculture_data.csv")

user_color='white'
original_title = """
<div style="background-color:{};padding:12px">
<h2 style="font-family:Courier;color:black;font-weight: bold;test-align:center;">🌿INDIAN AGRICULTURE ANALYSIS</h2>
</div>""".format(user_color)
st.markdown(original_title, unsafe_allow_html=True)

eda_Options = ["select a Question",
               "1. Top 7 RICE PRODUCTION State Data",
               "2. Top 5 Wheat Producing States Data and its percentage(%)",
               "3. Oil seed production by top 5 states",
               "4. Top 7 SUNFLOWER PRODUCTION  State",
               "5. India's SUGARCANE PRODUCTION From Last 50 Years",
               "6. Rice Production Vs Wheat Production (Last 50y)",
               "7. Rice Production By West Bengal Districts",
               "8. Top 10 Wheat Production Years From UP",
               "9. Millet Production (Last 50y)",
               "10. Sorghum Production (Kharif and Rabi) by Region",
               "11. Top 7 States for Groundnut Production",
               "12. Soybean Production by Top 5 States and Yield Efficiency",
               "13. Oilseed Production in Major States",
               "14. Impact of Area Cultivated on Production (Rice, Wheat, Maize)",
               "15. Rice vs. Wheat Yield Across States"
               ]

sql_Options = ["select a Question",
               "1. Year-wise Trend of Rice Production Across States (Top 3)"
               ]
st.sidebar.image(r"C:\Users\Python Class\Agridata_Project2\crop1.jpeg")
sel_option = st.sidebar.selectbox("EDA QUESTIONS",eda_Options,index=0) 
sel1_option = st.sidebar.selectbox("SQL QUESTIONS",sql_Options,index=0) 

#1
if sel_option == "1. Top 7 RICE PRODUCTION State Data":

    state_rice_production = df.groupby("state_name")["rice_production"].sum().reset_index() 
    #We group the data by state,add rice grown per state.If state has data for multiple years, we combine them into one total number.
    # reset_index() - without this after grouping state becomes index not columns , to make it has a we use this 
    top_rice_states = state_rice_production.nlargest(7, "rice_production")  

    #  interactive bar plot
    fig = px.bar(
        top_rice_states, 
        x="rice_production", 
        y="state_name", 
        text="rice_production",  # Show values on bars
        orientation="h",  #bars go sideways (horizontal)
        title="Top 7 Rice Producing States",
        labels={"rice_production": "Total Rice Production (kg)", "state_name": "State"},
        color="state_name",  # Color by value
        color_discrete_sequence=px.colors.sequential.Blues_r  # Color gradient
    )

    # Show values when hovering
    fig.update_traces(texttemplate="%{text:.2s}", textposition="outside", hoverinfo="x+y")
    #texttemplate="%{text:.2s}" → Formatting the Numbers,%{text} → rice production numbers, .2s → formats number in a short form (scientific notation).
    #textposition="outside" → Showing Numbers Outside the Bars , hoverinfo="x+y" → What Info to Show When Hovering

    # Show the interactive plot
    st.plotly_chart(fig, use_container_width=True)

#2
if sel_option == "2. Top 5 Wheat Producing States Data and its percentage(%)":
    state_wheat_production = df.groupby("state_name")["wheat_production"].sum().reset_index()
    top_wheat_states = state_wheat_production.nlargest(5,"wheat_production") 

    fig = px.bar(
        top_wheat_states, 
        x="wheat_production", 
        y="state_name", 
        text="wheat_production",  # Show values on bars
        labels={"wheat_production": "Total Wheat Production", "state_name": "State"},
        title="Top 5 Wheat Producing States",
        color="state_name",  # Different colors for each state
        orientation="h",  # Horizontal bar chart
        color_discrete_sequence=px.colors.sequential.Viridis   # Use Blues_r color palette
    )


    fig.update_traces(texttemplate="%{text:.2s}", textposition="outside", hoverinfo="x+y")
    st.plotly_chart(fig, use_container_width=True)

    # Calculate Percentage
    top_wheat_states["percentage"] = (top_wheat_states["wheat_production"] / top_wheat_states["wheat_production"].sum()) * 100

    fig = px.pie(
        top_wheat_states, 
        values="wheat_production", 
        names="state_name", 
        title="PERCENTAGE OF Top 5 WHEAT PRODUCING STATES",
        hover_data=["percentage"],  # Show percentage on hover
        labels={"percentage": "Percentage (%)"},
        color="state_name",
        color_discrete_sequence=px.colors.qualitative.Pastel1 ,
        custom_data=["percentage"]
    )
    # Format hover template
    fig.update_traces(hovertemplate='%{label}')
    st.plotly_chart(fig, use_container_width=True)

#3
if sel_option == "3. Oil seed production by top 5 states":
    state_oilSeed_production = df.groupby("state_name")["oilseeds_production"].sum().reset_index()
    top_oilseed_states = state_oilSeed_production.nlargest(5,"oilseeds_production") 

    fig = px.bar(
        top_oilseed_states, 
        x="oilseeds_production", 
        y="state_name", 
        text="oilseeds_production",  # Show values on bars
        labels={"oilseeds_production": "Total Oil Seed Production", "state_name": "State"},
        title="Top 5 Oil Seed Producing States",
        color="state_name",  # Different colors for each state
        orientation="h",  # Horizontal bar chart
        color_discrete_sequence=px.colors.sequential.Blues_r   # Use Blues_r color palette
    )
    fig.update_traces(texttemplate="%{text:.2s}", textposition="outside", hoverinfo="x+y")
    st.plotly_chart(fig, use_container_width=True)

#4
if sel_option == "4. Top 7 SUNFLOWER PRODUCTION  State":
    state_sunflower_production = df.groupby("state_name")["sunflower_production"].sum().reset_index()
    top_sunflower_states = state_sunflower_production.nlargest(7,"sunflower_production") 

    fig = px.bar(
        top_sunflower_states, 
        x="sunflower_production", 
        y="state_name", 
        text="sunflower_production",  # Show values on bars
        labels={"sunflower_production": "Total Sunflower Production", "state_name": "State"},
        title="Top 7 Sunflower Producing States",
        color="state_name",  # Different colors for each state
        orientation="h",  # Horizontal bar chart
        color_discrete_sequence=px.colors.sequential.Viridis   # Use Blues_r color palette
    )
    fig.update_traces(texttemplate="%{text:.2s}", textposition="outside", hoverinfo="x+y")
    st.plotly_chart(fig, use_container_width=True)

#5
if sel_option == "5. India's SUGARCANE PRODUCTION From Last 50 Years":
    yearwise_sugarcane_production = df.groupby("year")["sugarcane_production"].sum().reset_index()
    sugarcane_prod = yearwise_sugarcane_production.tail(50)
    # Create Interactive Line Plot
    fig = px.line(
        sugarcane_prod, 
        x="year", 
        y="sugarcane_production", 
        markers=True,  # Show markers at data points
        labels={"sugarcane_production": "Total Sugarcane Production", "year": "Year"},
        title="India's Sugarcane Production Over the Last 50 Years",
        color_discrete_sequence=px.colors.sequential.Viridis   # Use Viridis color palette
    )
    fig.update_traces(mode="lines+markers", hoverinfo="x+y")
    #"lines" → Draws a continuous line connecting data points."markers" → Adds distinct points (dots) at each data value for better visibility.
    #"lines+markers" → Combines both, ensuring the trend is visible while making individual data points easy to spot.
    st.plotly_chart(fig, use_container_width=True)

#6
if sel_option == "6. Rice Production Vs Wheat Production (Last 50y)":

    # Assuming df has 'year', 'rice_production', 'wheat_production'
    last_50_years = df.tail(50)  

    # Melt the data for Plotly
    #melt is a function used to unpivot a DataFrame from wide format to long format.
    #It helps transform columns into rows, making the data more suitable for analysis and visualization.
    melted_df = last_50_years.melt(id_vars=["year"], # Keeps the year column unchanged.
                                value_vars=["rice_production", "wheat_production"], #Specifies which columns to melt.
                                var_name="Crop", #The new column that stores the original column names (rice_production and wheat_production).
                                value_name="Production") #The new column that

    fig = px.bar(melted_df, x="year", 
                y="Production", 
                color="Crop",
                barmode="stack",  # Stacked bars
                labels={"Production": "Total Production (in tons)", "year": "Year"},
                title="Rice vs Wheat Production - Last 50 Years in Stacked Bar",
                color_discrete_map={"rice_production": "gold", "wheat_production": "black"})

    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

#7
if sel_option == "7. Rice Production By West Bengal Districts":
    dis_riceProd_WB = df[df["state_name"] == "West Bengal"].groupby("dist_name")["rice_production"].sum().reset_index()

    fig = px.bar(
        dis_riceProd_WB, 
        x="rice_production", 
        y="dist_name", 
        text="rice_production",  # Show values on bars
        labels={"rice_production": "Total Rice Production", "dist_name": "District"},
        title="RICE PRODUCTION BY WEST BENGAL DISTRICT WISE",
        color="dist_name",  # Different colors for each dis
        orientation="h",  # Horizontal bar chart
        color_discrete_sequence=px.colors.sequential.Blues_r  
    )
    fig.update_traces(texttemplate="%{text:.2s}", textposition="outside", hoverinfo="x+y")
    st.plotly_chart(fig, use_container_width=True)

#8
if sel_option == "8. Top 10 Wheat Production Years From UP":
    yearwise_wheatProd_UP = df[df["state_name"] == "Uttar Pradesh"].groupby("year")["wheat_production"].sum().reset_index()
    top_wheat_yearwise = yearwise_wheatProd_UP.nlargest(10,"wheat_production") 

    fig = px.bar(
        top_wheat_yearwise, 
        x="wheat_production", 
        y="year", 
        text="wheat_production",  # Show values on bars
        labels={"wheat_production": "Total Wheat Production", "year": "Year"},
        title="TOP 10 WHEAT PRODUCTION IN UP (YEARWISE)",
        color="year",  # Different colors for each state
        orientation="h",  # Horizontal bar chart
        color_discrete_sequence=px.colors.sequential.Viridis   # Use Blues_r color palette
    )
    fig.update_traces(texttemplate="%{text:.2s}", textposition="outside", hoverinfo="x+y")
    st.plotly_chart(fig, use_container_width=True)

#9
if sel_option == "9. Millet Production (Last 50y)":
    yearwise_MILLET_production = df.groupby("year")[["pearl_millet_production", "finger_millet_production"]].sum().reset_index()
    millet_prod = yearwise_MILLET_production.tail(50)
    # Create Interactive Line Plot
    fig = px.line(
        millet_prod, 
        x="year", 
        y=["pearl_millet_production","finger_millet_production"] ,
        markers=True,  
        labels={"value": "Millet Production", "year": "Year", "variable": "Millet Type"},
        title="India's Millet Production Over the Last 50 Years",
        color_discrete_sequence=px.colors.sequential.Viridis   # Use Viridis color palette
    )
    fig.update_traces(mode="lines+markers", hoverinfo="x+y")
    #"lines" → Draws a continuous line connecting data points."markers" → Adds distinct points (dots) at each data value for better visibility.
    #"lines+markers" → Combines both, ensuring the trend is visible while making individual data points easy to spot.
    st.plotly_chart(fig, use_container_width=True)

#10
if sel_option == "10. Sorghum Production (Kharif and Rabi) by Region":
    region_Sorghum_production = df.groupby("state_name")[["kharif_sorghum_production", "rabi_sorghum_production"]].sum().reset_index()
    # Reshape DataFrame for easier plotting
    df_melted = region_Sorghum_production.melt(id_vars="state_name", 
                                            var_name="Season", 
                                            value_name="Production")
    # Create Grouped Bar Chart
    fig = px.bar(
        df_melted, 
        x="state_name", 
        y="Production", 
        color="Season", 
        barmode="group",
        labels={"Production": "Sorghum Production (Tonnes)", "state_name": "State"},
        title="Sorghum Production (Kharif & Rabi) by State",
        color_discrete_map={"kharif_sorghum_production": "green", "rabi_sorghum_production": "blue"}
    )
    st.plotly_chart(fig, use_container_width=True)

#11
if sel_option == "11. Top 7 States for Groundnut Production":
    state_groundNut_production = df.groupby("state_name")["groundnut_production"].sum().reset_index()
    top_groundnut_states = state_groundNut_production.nlargest(7,"groundnut_production") 

    fig = px.bar(
        top_groundnut_states, 
        x="groundnut_production", 
        y="state_name", 
        text="groundnut_production",  # Show values on bars
        labels={"groundnut_production": "Total GroundNut Production", "state_name": "State"},
        title="Top 7 States for Groundnut Production",
        color="state_name",  # Different colors for each state
        orientation="h",  # Horizontal bar chart
        color_discrete_sequence=px.colors.qualitative.Pastel1  
    )
    fig.update_traces(texttemplate="%{text:.2s}", textposition="outside", hoverinfo="x+y")
    st.plotly_chart(fig, use_container_width=True)

#12
if sel_option == "12. Soybean Production by Top 5 States and Yield Efficiency":
    soyabean_prod = df.groupby(["state_name","soyabean_yield"])["soyabean_production"].sum().reset_index()
    top_soyabean_states = soyabean_prod.nlargest(5,"soyabean_production") 
    # Scatter Plot for Yield Efficiency vs. Production
    fig = px.scatter(
        top_soyabean_states, 
        x="soyabean_yield", 
        y="soyabean_production", 
        size="soyabean_production",  # Bubble size based on total production
        hover_name="state_name",
        labels={"soyabean_yield": "Yield Efficiency (kg/ha)", "soyabean_production": "Soybean Production (Tonnes)"},
        title="Soybean Production vs. Yield Efficiency (Top 5 States)",
        color="state_name"
    )
    st.plotly_chart(fig, use_container_width=True)

#13
if sel_option == "13. Oilseed Production in Major States":
    oilSeed_prod = df.groupby("state_name")["oilseeds_production"].sum().reset_index()

    fig = px.bar(
        oilSeed_prod, 
        x="state_name", 
        y="oilseeds_production", 
        color="state_name",
        text="oilseeds_production",
        labels={"oilseeds_production": "Oilseed Production (Tonnes)", "state_name": "State"},
        title="Oilseed Production in Major States",
    )
    fig.update_traces(texttemplate='%{text}', textposition='outside')  # Display production values
    st.plotly_chart(fig, use_container_width=True)

#14
if sel_option == "14. Impact of Area Cultivated on Production (Rice, Wheat, Maize)":
    crop_data = pd.DataFrame({
        "Crop": ["Rice", "Wheat", "Maize"],
        "Crop Area (ha)": [df["rice_area"].sum(), df["wheat_area"].sum(), df["maize_area"].sum()],
        "Crop Production (tonnes)": [df["rice_production"].sum(), df["wheat_production"].sum(), df["maize_production"].sum()]
    })
    # Scatter Plot: Cultivated Area vs. Production
    fig = px.scatter(
        crop_data, 
        x="Crop Area (ha)", 
        y="Crop Production (tonnes)", 
        color="Crop", 
        size="Crop Production (tonnes)",  # Bubble size based on total production
        hover_name="Crop",
        title="Impact of Area Cultivated on Production (Rice, Wheat, Maize)",
        labels={"Crop Area (ha)": "Cultivated Area (Hectares)", "Crop Production (tonnes)": "Total Production (Tonnes)"},
    )
    st.plotly_chart(fig, use_container_width=True)

#15
if sel_option == "15. Rice vs. Wheat Yield Across States":
    yield_data = df.groupby("state_name")[["rice_yield", "wheat_yield"]].mean().reset_index()
    # Convert data to long format for bar chart
    yield_data_melted = yield_data.melt(id_vars="state_name", var_name="Crop", value_name="Yield (kg/ha)")
    fig = px.bar(
        yield_data_melted, 
        x="state_name", 
        y="Yield (kg/ha)", 
        color="Crop", 
        barmode="group",
        title="Rice vs. Wheat Yield Across States",
        labels={"Yield (kg/ha)": "Yield (kg/ha)", "state_name": "State"}
    )
    st.plotly_chart(fig, use_container_width=True)

#SQL QUES
#1
if sel1_option == "1. Year-wise Trend of Rice Production Across States (Top 3)":
    mycursor.execute("""
    WITH Top_States AS (
    SELECT state_name 
    FROM Crops_Data
    GROUP BY state_name
    ORDER BY SUM(rice_production) DESC
    LIMIT 3
    )
    SELECT A.year, A.state_name, SUM(A.rice_production) AS rice_production
    FROM Crops_Data A
    JOIN Top_States B ON A.state_name = B.state_name
    GROUP BY A.year, A.state_name
    ORDER BY A.year, rice_production DESC""") 
    result = mycursor.fetchall()
    # Convert to DataFrame
    df = pd.DataFrame(result, columns=["year","state_name","rice_production"])