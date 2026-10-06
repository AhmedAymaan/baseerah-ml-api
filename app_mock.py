from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def generate_recommendations(glucose):
    """Simple rule-based recommendations based on glucose value."""
    if glucose < 70:
        return {
            "status_summary": "Low blood glucose detected. Take action immediately.",
            "diet": [
                "Consume fast-acting carbohydrates (juice, glucose tablets).",
                "Recheck your blood glucose after 15 minutes.",
                "Follow with a balanced snack containing protein if needed."
            ],
            "exercise": [
                "Stop exercise until your glucose recovers.",
                "Recheck before returning to physical activity.",
                "Seek urgent medical help if symptoms persist."
            ]
        }
    elif glucose > 180:
        return {
            "status_summary": "Elevated blood glucose detected. Monitor closely.",
            "diet": [
                "Choose vegetables, fiber, and lean protein.",
                "Limit sugary drinks and refined carbohydrates.",
                "Drink water regularly."
            ],
            "exercise": [
                "Light to moderate activity like walking may help.",
                "Avoid strenuous exercise if glucose is very high.",
                "Monitor glucose according to your care plan."
            ]
        }
    else:
        return {
            "status_summary": "Blood glucose is in a reasonable range.",
            "diet": [
                "Maintain a balanced diet with vegetables and lean protein.",
                "Limit processed foods and added sugars.",
                "Keep regular meal portions."
            ],
            "exercise": [
                "Maintain regular physical activity.",
                "Walking, cycling, or swimming are good options.",
                "Avoid prolonged inactivity."
            ]
        }


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        glucose = float(data["glucose"])
        age = float(data["age"])
        bmi = float(data["bmi"])
        insulin = float(data["insulin"])
        blood_pressure = float(data["blood_pressure"])

        if glucose <= 0 or age <= 0 or bmi <= 0 or blood_pressure <= 0:
            return jsonify({"error": "All values must be positive numbers."}), 400

        # === مؤقتًا: منطق بسيط بدل الموديل ===
        if glucose > 180 or bmi > 30:
            risk_code = 1
            risk_probability = 72.5
            risk_title = "Higher Diabetes Risk"
        else:
            risk_code = 0
            risk_probability = 28.3
            risk_title = "Lower Diabetes Risk"

        recommendations = generate_recommendations(glucose)

        return jsonify({
            "risk_code": risk_code,
            "risk_probability": risk_probability,
            "risk_title": risk_title,
            "message": "Analysis completed successfully.",
            "recommendations": recommendations,
            "note": "Mock model in use. Real ML model will be integrated later."
        }), 200

    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except ValueError:
        return jsonify({"error": "Please enter valid numeric values."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "baseerah-api"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="127.0.0.1")