import streamlit as st
from twilio.rest import Client
import pandas as pd
from twilio.rest import Client
import joblib
from streamlit_option_menu import option_menu
import requests

try:
    model = joblib.load('./SavedModels/new-4-soils.joblib')
    
except Exception as e:
    st.error(f"Error loading the model: {e}")

# Configure Twilio
twilio_account_sid = "ACd81bfc749c28496c26b3b03dbb62985f"
twilio_auth_token = "14623ec185ca7a9187c3561702702dea"
twilio_phone_number = "+16207098293"
recipient_phone_number = "+918567098852"

# Create a Twilio client
client = Client(twilio_account_sid, twilio_auth_token)

# Define image URLs for each soil type
alluvial_soil_image_url = 'images/alluvial-soil.jpg'
desert_soil_image_url = 'images/desert-soil.jpg'
red_soil_image_url = 'images/red-soil.jpg'
loamy_soil_image_url = 'images/loamy-soil.jpg'

# Create the Streamlit app

with st.sidebar:
    st.title("Soil Predictor App")
    st.write("Welcome to the Soil Predictor")
    st.write(" Choose an option from the menu below to get started:")

    selected = option_menu('Soil Predictor App',
                        ['About us',
                        'Soil Prediction',
                        ],
                        icons=['chat-square-text','question-circle'],
                        default_index=0)
# About Page
if (selected == 'About us'):
    
    st.title("Welcome to Soil Predictor App")
    st.write("An innovative application that predicts soil types based on input features such as Nitrogen, Phosphorus, Potassium, Humidity, Temperature, Conductivity, and pH. This application is designed to assist users in identifying the most suitable soil for their agricultural needs.")

    st.header("App:")
    
    st.write("a) Soil Prediction: Input relevant soil features and get real-time predictions on the type of soil.\n\n b) Crop Recommendations: Receive recommendations for crops suitable for the predicted soil type.\n\n c) Alerts: Get alerts for specific soil conditions, such as low water levels.")
    
    st.write("Thank you soo much for using Soil Predictor. Feel free to explore our features and take advantage of the insights we provide.")

# Soil Prediction Page
if (selected == 'Soil Prediction'):

    st.markdown(
            "<h1 style='text-align: center; color: black;'>Soil Predictor App</h1>",
            unsafe_allow_html=True
        )
    st.markdown(
            "<h6 style='text-align: center; color: grey;'>Note: N, P & K are in KG per Hectare (kg/hg), Temperature is in Degree Celsius (°C), Moisture in Percentage (%) & Conductivity in milliSiemens per centimeter (mS/cm)</h6>",
            unsafe_allow_html=True
        )

    # Create input fields for user to enter features
    col1, col2, col3 = st.columns(3)

    with col1:
        Nitrogen = st.text_input('Nitrogen')
    with col2:
        Phosphorus = st.text_input('Phosphorus')
    with col3:
        Potassium = st.text_input('Potassium')
    with col1:
        Temperature = st.text_input('Temperature')
    with col2:
        Conductivity = st.text_input('Conductivity')
    with col3:
        pH = st.text_input('pH')
    with col1:
        Moisture = st.text_input('Soil Moisture')

    soil = ''

    def predict_soil(input_features):
        return model.predict(input_features)

    st.markdown(
        """
    <style>
    button {
        height: 50px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    if st.button('Submit'):
        try:
            input_features = {
                "Nitrogen" : float(Nitrogen),
                "Phosphorus" : float(Phosphorus),
                "Potassium" : float(Potassium),
                "Temperature" : float(Temperature),
                "Conductivity" :float(Conductivity),
                "pH" : float(pH),
                "Moisture" : float(Moisture)
            }
            
            print("Input features:", input_features)
            
            # Send SMS alert if water level is low
            if float(Moisture) <= 20:
                message = client.messages.create(
                    body="⚠️⚠️ LOW WATER LEVEL IN YOUR SOIL ⚠️⚠️",
                    from_=twilio_phone_number,
                    to=recipient_phone_number
                )

                st.write(
                    '<div style="background-color: Grey; padding: 15px; margin-bottom: 20px; border-radius: 5px; font-size: 20px; color: white; text-align: center">'
                    '<strong>⚠️⚠️LOW WATER LEVEL IN YOUR SOIL⚠️⚠️</strong>'
                    '</div>',
                    unsafe_allow_html=True
                )
            
            try:
                response = requests.post('https://flaskapp02.azurewebsites.net/', json=input_features)
                if response.status_code == 200:
                    result = response.json()
                    soil = result.get("prediction")
                    crop_recommendations = result.get("crop_recommendations")
                    
                    st.write(
                    f'<div style="background-color: black; padding: 15px; margin-bottom: 20px; border-radius: 5px; font-size: 22px; color: white; text-align: center">'
                    f'<strong>According to values you have entered, the soil is seems to be {soil}.</strong>'
                    f'</div>',
                    unsafe_allow_html=True
                    )
                    
                    # Send SMS alert after prediction
                    Soil_recommendation_message = (
                        f"According to values you have entered, the soil is seems to be {soil}.\n\nRecommended crops for {soil} are {crop_recommendations[soil]}.\n\nThank you soo much for using our app. For any further assistance please contact us."
                    )
                    try:
                        message = client.messages.create(
                            body=Soil_recommendation_message,
                            from_=twilio_phone_number,
                            to=recipient_phone_number
                        )
                        # st.success(f"SMS sent successfully")
                    except Exception as e:
                        st.error(f"Error sending SMS: {e}")
                    
                    if soil in crop_recommendations:
                        st.write(
                            f'<div style="background-color: black; padding: 15px; margin-bottom: 20px; border-radius: 5px; font-size: 20px; color: white; text-align: center">'
                            f'Recommended crops for {soil}: {crop_recommendations[soil]}'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                        # Display image based on soil type
                        col1, col2, col3 = st.columns(3)
                    
                        if soil == 'Alluvial Soil':
                            with col2:
                                st.image(alluvial_soil_image_url, width=250, caption="Alluvial Soil")

                        elif soil == 'Desert Soil':
                            with col2:
                                st.image(desert_soil_image_url, width=250, caption="Desert Soil")

                        elif soil == 'Red Soil':
                            with col2:
                                st.image(red_soil_image_url, width=250, caption="Red Soil")

                        elif soil == 'Loamy Soil':
                            with col2:
                                st.image(loamy_soil_image_url, width=250, caption="Loamy Soil")
                else:
                    st.error("Failed to get prediction from the server.")
            except requests.exceptions.ConnectionError:
                st.error("Error: Unable to connect to the server. Please make sure the server is running.")
        except ValueError:
            st.error("Invalid input. Please provide valid numeric values for all features.")
        
        with col1:
            if st.button("Clear"):
                st.rerun();