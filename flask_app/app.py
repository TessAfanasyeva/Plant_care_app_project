import requests
from datetime import timedelta
from flask import Flask, render_template, request
from fuzzywuzzy import fuzz

API_KEY = "sk-zgc3645919b3f266b563"
API_URL = f"https://perenual.com/api/species-list?key={API_KEY}&limit=3000&page="

app = Flask(__name__)

def get_plant_data(plant_name):
    response = requests.get(API_URL + "&q=" + plant_name)
    data = response.json()["data"]

    direct_match = None
    close_matches = []

    for plant in data:
        common_name = plant["common_name"]
        scientific_names = plant["scientific_name"]
        other_names = plant["other_name"] if plant["other_name"] else []

        if not isinstance(scientific_names, list):
            continue

        all_names = [common_name] + scientific_names + other_names

        combined_names = " ".join(all_names)

        match_score = fuzz.partial_ratio(plant_name.lower(), combined_names.lower())

        if match_score > 60:
            if plant_name.lower() == common_name.lower():
                direct_match = plant
                break
            else:
                close_matches.append({
                    "common_name": common_name,
                    "original_name": plant_name,
                    "watering": plant["watering"]
                })

    if direct_match:
        return direct_match
    elif close_matches:
        return close_matches
    else:
        return None

def get_watering_frequency(frequency):
    if frequency == "Frequent":
        duration = timedelta(days=2)
    elif frequency == "Average":
        duration = timedelta(days=7)
    elif frequency == "Minimum":
        duration = timedelta(days=28)
    elif frequency == "None":
        return "never"
    else:
        return "unknown"
    days = duration.days
    return days

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home.html')
def home():
    return render_template('home.html')

@app.route('/page_stop.html', methods=['GET'])
def page_stop():
    return render_template('page_stop.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        plant_name = request.form['plant_name']
    elif request.method == 'GET':
        plant_name = request.args.get('plant_name')

    plant_data = get_plant_data(plant_name)

    if plant_data is not None:
        if isinstance(plant_data, list):  # close matches
            close_matches = plant_data
            return render_template('close_matches.html', close_matches=close_matches)
        else:  # direct match
            plant_name = plant_data["common_name"]
            watering_frequency = plant_data["watering"]
            frequency_description = get_watering_frequency(watering_frequency)

            with open("plant_details.txt", "w") as file:
                file.write(f"Plant Name: {plant_name}\n")
                file.write(f"Watering Frequency: {frequency_description}")

            return render_template('result.html', plant_name=plant_name, frequency_description=frequency_description)
    else:
        return render_template('result.html', error_message="No plant details found for the provided name.")


if __name__ == '__main__':
    app.run()
