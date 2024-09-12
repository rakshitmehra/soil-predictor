# Soil Prediction Plateform

## Introduction

Welcome to Soil Predictor, an innovative application that predicts soil types based on input features such as Nitrogen, Phosphorus, Potassium, Humidity, Temperature, Conductivity, and pH. This application is designed to assist users in identifying the most suitable soil for their agricultural needs.

## Key Features

- **Soil Prediction:** Input relevant soil features and get real-time predictions on the type of soil.

- **Crop Recommendations for particular soil:** Receive recommendations for crops suitable for the predicted soil type.

- **Alerts:** Get alerts for specific soil conditions, such as low water levels.

## Technologies Used

- Python
- Streamlit
- Twilio API (for SMS alerts)
- Machine Learning (Random Forest, XGBoost)

## How to Run the Streamlit Code

Follow these steps to run the Streamlit code locally:

### Clone the Repository

```bash
git clone https://github.com/rakshitmehra/soil-predicton.git
cd soil-predictor
```
### Install Dependencies
 ```bash
 pip install -r requirements.txt
 ```
 ### Run the Streamlit App
 ```bash
streamlit run main.py
```
This will launch the Streamlit app locally. Open your web browser and navigate to the provided local address to explore soil predictor.
