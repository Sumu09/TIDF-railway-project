from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import os

# Flask app setup
app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static'
)
CORS(app)

trains_data = [
    {"sl_no": 1, "name": "rajdhani express", "status": "Unfinished", "time": "17:57:00"},
    {"sl_no": 2, "name": "goods2 Train", "status": "Unfinished", "time": "17:57:00"},
    {"sl_no": 3, "name": "goods3 Train", "status": "Unfinished", "time": "17:57:00"},
    {"sl_no": 4, "name": "goods4 Train", "status": "Finished", "time": "17:57:00"},
    {"sl_no": 5, "name": "manuh goods Train", "status": "Unfinished", "time": "17:57:00"},
    {"sl_no": 6, "name": "sixth goods Train", "status": "Finished", "time": "17:57:00"},
    {"sl_no": 7, "name": "seventh goods Train", "status": "Unfinished", "time": "17:57:00"},
    {"sl_no": 8, "name": "eighth goods Train", "status": "Unfinished", "time": "17:57:00"},
    {"sl_no": 9, "name": "ninth goods Train", "status": "Unfinished", "time": "17:57:00"},
    {"sl_no": 10, "name": "tenth goods Train", "status": "Unfinished", "time": "17:57:00"},
    {"sl_no": 11, "name": "eleventh goods Train", "status": "Finished", "time": "17:57:00"},
    {"sl_no": 12, "name": "twelfth goods Train", "status": "Unfinished", "time": "17:57:00"},
    {"sl_no": 13, "name": "thirteenth goods Train", "status": "Unfinished", "time": "17:57:00"},
    {"sl_no": 14, "name": "fourteenth goods Train", "status": "Finished", "time": "17:57:00"},
    {"sl_no": 15, "name": "fifteenth goods Train", "status": "Unfinished", "time": "17:57:00"},
]


@app.route('/trains', methods=['GET'])
def get_trains():
    """API endpoint to get all trains data"""
    return jsonify(trains_data)

@app.route('/train/<int:train_id>', methods=['GET'])
def get_train_details(train_id):
    """API endpoint to get specific train details"""
    train = next((t for t in trains_data if t['sl_no'] == train_id), None)
    if train:
        return jsonify(train)
    return jsonify({"error": "Train not found"}), 404

@app.route('/train-report-data', methods=['GET'])
def get_train_report_data():
    """API endpoint to get train report data"""
    train_name = request.args.get('name', 'Unknown Train')
    train_status = request.args.get('status', 'Unknown')
    train_id = request.args.get('id', '1')

    # Generate detailed door data based on train
    door_details = []
    for i in range(1, 21):  # 20 doors for example
        marking_options = ['LI-SI', 'LI-SM', 'Broken-SI', 'Broken-SM', 'OTLI-SI', 'OTLI-SM']
        import random
        marking = random.choice(marking_options)

        door_details.append({
            'position': i,
            'door_number': i,
            'wagon_number': f'WG{str(i//4 + 1).zfill(3)}',
            'marking': marking,
            'image': ''
        })

    # Count markings for summary
    marking_counts = {}
    for detail in door_details:
        marking = detail['marking']
        marking_counts[marking] = marking_counts.get(marking, 0) + 1

    report_data = {
        'train_name': train_name,
        'train_status': train_status,
        'train_number': f'TN{train_id.zfill(3)}',
        'train_side': 'Right Side',
        'station_name': 'Katihar Junction',
        'current_time': datetime.now().strftime("%I:%M %p"),
        'current_date': datetime.now().strftime("%d/%m/%Y"),
        'total_doors': len(door_details),
        'otli_si': marking_counts.get('OTLI-SI', 0),
        'otli_sm': marking_counts.get('OTLI-SM', 0),
        'li_si': marking_counts.get('LI-SI', 0),
        'li_sm': marking_counts.get('LI-SM', 0),
        'broken_si': marking_counts.get('Broken-SI', 0),
        'broken_sm': marking_counts.get('Broken-SM', 0),
        'door_details': door_details
    }

    return jsonify(report_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
