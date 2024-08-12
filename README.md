# **Simple Voys (VOIP Provider) Integration with Zammad**

This repository houses a Flask application that provides a real-time integration between Voys, a VOIP provider, and Zammad, an open-source support ticketing system. The application leverages Voys' "gespreknotifications" (call notifications) to receive and process real-time updates about VOIP calls and uses Zammad’s generic CTI interface to update call information within Zammad.

## **Prerequisites**
You'll need Docker on your system to run the application in a containerized setup. Git is recommended for easy cloning of the repository.

## **Installation**
- git clone https://github.com/Qsb11/zammad-voys.git
- cd zammad-voys

## **Build the Docker image:**
- docker build -t voys-zammad-integration .
- Run the container:
- docker run -p 5000:5000 --env ZAMMAD_URL='https://your-zammad-endpoint.com' voys-zammad-integration
- Replace 'https://your-zammad-endpoint.com' with the actual URL of your Zammad installation.

## **Features**
- Real-Time Call Updates: Utilizes Voys' "gespreknotifications" to receive and process updates about VOIP calls as they happen.
- Webhook Receiver: Handles incoming POST requests containing JSON data from Voys.
- Data Processing: Extracts call data from Voys' notifications and maps it into formats compatible with Zammad’s Generic CTI.
- Zammad Integration via Generic CTI: Connects and updates Zammad using its generic CTI interface, ensuring that all call events and details are logged and actionable within Zammad’s ticketing system.

## **API Endpoint**
- POST /webhook: Accepts JSON payloads from Voys, processing them to update call statuses and details directly in Zammad via the Generic CTI.
  
## **Files Included**
- Dockerfile: Defines the Docker commands needed to build the image.
- app.py: The main Flask application script.
- requirements.txt: Lists all dependencies required by the application.


## **Dependencies**

**The project depends on several Python packages, including:**
- Flask==3.0.3
- requests==2.31.0
- Jinja2==3.1.2
- MarkupSafe==2.1.3
- itsdangerous==2.1.2
- These are all specified in the requirements.txt file and are installed during the Docker build.

## **Usage Rights**
This project is open-source and freely available for anyone to use, modify, and distribute without restrictions.
