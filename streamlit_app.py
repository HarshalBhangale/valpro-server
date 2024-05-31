import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from prop_valuation import compute_valuation  # Import the function from the module

def main():
    # Title of the web app
    st.title('Property Valuator')

    # Collecting inputs
    address = st.text_input('Address')
    property_type = st.selectbox('Property Type', ['office', 'industrial'])
    industrial_size = st.number_input('Industrial Size', min_value=250)
    industrial_subtype = st.selectbox('Industrial Sub Type', ['prime industrial park', 'prime leaseback', 'prime quality non-leaseback', 'secondary quality building'])
    office_grade = st.selectbox('Office Grade', ['A', 'B', 'C'])
    distance = st.number_input('Distance to City Center', min_value=0.0, format="%.2f")
    expense = st.number_input('Monthly Expenses', min_value=0.0, format="%.2f")

    # Button to submit inputs
    submit_button = st.button('Display on Map')

    if submit_button:
        valuations = compute_valuation(address, property_type, industrial_size, industrial_subtype, office_grade)
        print(address, property_type, industrial_size, industrial_subtype, office_grade)

        if valuations and len(valuations) > 0:
            # Create a map centered around the first valuation result (or another logical center)
            initial_location = [valuations[0]['latitude'], valuations[0]['longitude']]
            m = folium.Map(location=initial_location, zoom_start=13)

            # Iterate through each valuation and add a marker
            for valuation in valuations:
                folium.Marker(
                    [valuation['latitude'], valuation['longitude']],
                    popup=f"Area: {valuation['area']}<br>Valuation: ${valuation['valuation']:,.2f}",
                    tooltip=valuation['region']
                ).add_to(m)

            # Display the map in Streamlit
            folium_static(m)
        else:
            st.error('No valuation data received.')

if __name__ == "__main__":
    main()
