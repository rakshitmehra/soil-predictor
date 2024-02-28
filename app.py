from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load the model
try:
    model = joblib.load('./SavedModels/new-4-soils.joblib')
except Exception as e:
    print(f"Error loading the model: {e}")

# Crop recommendations
crop_recommendations = {
    'Alluvial Soil': 'Rice, Wheat, Bajra, Chickpea, Soybean, Cotton, Mustard, Groundnut, Sesame, Barley, Maize.',
    'Desert Soil': 'Corns, Beans, Onions, Garlics, Tomatoes.',
    'Red Soil': 'Cotton, Wheat, Rice, Pulses, Millets, Tobacco, Oil seeds, Potatoes, Fruits.',
    'Loamy Soil': 'Tomatoes, Carrot, Peppers, Green Beans, Cucumbers, Strawberries, Sweet Corn, Spinach, Potatoes.'
}

@app.route("/")
def home():
    return "Server is running."

@app.route("/", methods=["POST"])
def predict():
    try:
        # Get input data from request
        data = request.json
        
        # Perform prediction using the loaded model
        input_features = [
            float(data.get("Nitrogen", 0)), 
            float(data.get("Phosphorus", 0)), 
            float(data.get("Potassium", 0)), 
            float(data.get("Temperature", 0)), 
            float(data.get("Conductivity", 0)), 
            float(data.get("pH", 0)), 
            float(data.get("Moisture", 0))
        ]
        prediction = model.predict([input_features])
        
        soil_names = ['Alluvial Soil', 'Desert Soil', 'Loamy Soil', 'Red Soil']
        
        if 0 <= prediction[0] < len(soil_names):
            soil = soil_names[prediction[0]]
        else:
            soil = 'Soil is not fit for growing crops'
            
        response = {
            "prediction": soil,
            "crop_recommendations": crop_recommendations
        }
        return jsonify(response), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
