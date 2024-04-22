from flask import Flask, jsonify, request

app = Flask(__name__)

MAX_PATIENTS_PER_DAY = 5

WEEKLY_SCHEDULE = [
    {'day': 'Monday', 'available': True},
    {'day': 'Tuesday', 'available': True},
    {'day': 'Wednesday', 'available': True},
    {'day': 'Thursday', 'available': True},
    {'day': 'Friday', 'available': True},
    {'day': 'Saturday', 'available': True},
    {'day': 'Sunday', 'available': False}
]

doctors = [
    {'id': 1, 'name': 'Dr. A', 'specialty': 'Cardiology'},
    {'id': 2, 'name': 'Dr. B', 'specialty': 'Dermatology'},
    {'id': 3, 'name': 'Dr. C', 'specialty': 'Pediatrics'}
]

def get_available_slots(doctor_id, day):
    schedule = next((entry for entry in WEEKLY_SCHEDULE if entry['day'] == day), None)
    if not schedule or not schedule['available']:
        return []

    doctor = next((doc for doc in doctors if doc['id'] == doctor_id), None)
    if not doctor:
        return []

    slots = []
    for i in range(MAX_PATIENTS_PER_DAY):
        slots.append({'doctorId': doctor_id, 'day': day, 'slot': i + 1})
    return slots

def book_appointment(doctor_id, day, slot):
    return {'doctorId': doctor_id, 'day': day, 'slot': slot}



# doctors listing
@app.route('/doctors', methods=['GET'])
def get_doctors():
    return jsonify(doctors)

# doctor detail page
@app.route('/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    doctor = next((doc for doc in doctors if doc['id'] == doctor_id), None)
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404
    return jsonify(doctor)

# availability 
@app.route('/doctors/<int:doctor_id>/availability', methods=['GET'])
def get_availability(doctor_id):
    day = request.args.get('day')
    if not day:
        return '''
            <h1>Day parameter is required</h1>
            <p>Example usage:</p>
            <code>/doctors/1/availability?day=Monday</code>
        ''', 400
    slots = get_available_slots(doctor_id, day)
    return jsonify(slots)

# appointment booking
@app.route('/appointments', methods=['POST'])
def book_appointment_route():
    data = request.get_json()
    doctor_id = data.get('doctorId')
    day = data.get('day')
    slot = data.get('slot')
    if not doctor_id or not day or not slot:
        return jsonify({'error': 'Missing required parameters'}), 400
    appointment = book_appointment(doctor_id, day, slot)
    return jsonify(appointment)

if __name__ == '__main__':
    app.run(debug=True)