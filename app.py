from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

def send_to_zammad(zammad_url, zammad_payload):
    try:
        response = requests.post(zammad_url, json=zammad_payload, headers={'Content-Type': 'application/json'})
        app.logger.info("Response from Zammad: %s", response.text)

        if response.status_code == 200:
            return "ACK", 200
        elif response.status_code == 422 and 'already exists' in response.text:
            # Handle case where the object already exists
            app.logger.info("Event already exists in Zammad.")
            return "ACK", 200
        else:
            app.logger.error("Failed to send data to Zammad. Status code: %d", response.status_code)
            app.logger.error("Response: %s", response.text)
            return "ERR", 500
    except Exception as e:
        app.logger.error("Error while sending request to Zammad: %s", str(e))
        return "ERR", 500

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    # Log the incoming request
    app.logger.info("Incoming request: %s", request.json)

    # Receive the JSON payload from Voys
    data = request.json
    call_id = data.get('call_id')
    event_status = data.get('status')
    direction = data.get('direction')
    caller_number = data['caller'].get('number')
    caller_name = data['caller'].get('name', 'Unknown')
    destination_number = data['destination'].get('number')
    reason = data.get('reason', 'normalClearing')

    # Log the extracted reason
    app.logger.info("Extracted reason: %s", reason)

    # Map Voys direction to Zammad direction
    zammad_direction = 'in' if direction == 'inbound' else 'out'

    # Determine the event type for Zammad
    if event_status == 'created':
        zammad_event = 'newCall'
    elif event_status == 'in-progress':
        zammad_event = 'answer'
    elif event_status == 'ended':
        zammad_event = 'hangup'
    else:
  # Ignore ringing event to avoid duplicate newCall
        return Response("Event ignored", status=200)

    # Prepare the payload for Zammad
    zammad_url = os.getenv("ZAMMAD_URL")
    zammad_payload = {
        "event": zammad_event,
        "from": caller_number,
        "to": destination_number,
        "direction": zammad_direction,
        "callId": call_id
    }

    if zammad_event == 'newCall':
        zammad_payload["user"] = caller_name
    elif zammad_event == 'hangup':
        zammad_payload["cause"] = reason

    # Log the payload being sent to Zammad
    app.logger.info("Sending payload to Zammad: %s", zammad_payload)

    # Send the data to Zammad and process the response
    status, code = send_to_zammad(zammad_url, zammad_payload)

    return Response(status, status=code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
