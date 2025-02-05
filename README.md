# Rasa Intake Assistant for Spectrum Psychological Services

## Overview
This project implements a Rasa-based conversational assistant to automate the patient intake process at Spectrum Psychological Services. The assistant interacts with users to gather important information like patient details, insurance information, and appointment preferences. It also answers frequently asked questions about the clinic's services, ensuring a smoother onboarding experience while reducing manual workload.

## Key Features
- **Natural Language Understanding:** Recognizes user intents and entities using Rasa's advanced NLP pipeline.
- **Automated Patient Intake:** Collects patient and insurance details, such as names, dates of birth, and contact numbers.
- **Custom Actions:** Integrates with a backend server to handle appointment availability checks and insurance validation.
- **Flexible Deployment:** Deployed using Docker and managed via Supervisor.

## Project Structure
```
.
├── README.md                            # Documentation file
├── actions.py                           # Custom actions for handling backend logic
├── config.yml                           # Rasa pipeline and policies configuration
├── domain.yml                           # Intent, entities, slots, and responses definition
├── endpoints.yml                        # Configuration for Rasa action server endpoints
├── requirements.txt                     # Python dependencies
├── Dockerfile.txt                       # Docker configuration for containerization
├── fly.toml                             # Deployment configuration for Fly.io
├── supervisord.conf                     # Supervisor configuration to manage Rasa services
```

## Setup Instructions
### 1. Clone the repository
```bash
git clone https://github.com/yourusername/rasa-intake-assistant.git
cd rasa-intake-assistant
```

### 2. Install dependencies
Create a virtual environment and install dependencies using:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Train the Rasa model
Train the assistant using the following command:
```bash
rasa train
```

### 4. Run the assistant locally
To run the Rasa server and custom action server locally:
```bash
rasa run --enable-api --cors "*" --port 5005
rasa run actions --port 5060
```
Access the assistant at: `http://localhost:5005`

## Deployment Instructions
The assistant is containerized using Docker and deployable via Fly.io.

### Build and run using Docker
```bash
docker build -t rasa-intake-assistant .
docker run -p 5005:5005 -p 5060:5060 rasa-intake-assistant
```

### Deploy via Fly.io
Fly.io configuration is specified in the `fly.toml` file. To deploy:
```bash
fly launch
```

## Key Components
- **actions.py:** Contains backend logic for tasks like insurance validation and appointment scheduling.
- **config.yml:** Defines the NLP pipeline and fallback policies for handling user queries.
- **domain.yml:** Specifies intents, entities, slots, responses, and forms used in the conversations.
- **Dockerfile:** Sets up the container environment with the Rasa model and dependencies.

## Supported Intents and Entities
The assistant can recognize and handle multiple user intents related to patient intake, clinic services, and insurance inquiries.

### Example Intents
- `ask_services`: Inquire about the clinic’s available services.
- `provide_patient_name`: Provide the name of the patient.
- `ask_appointment_scheduling`: Ask about scheduling a new appointment.
- `ask_insurance_*`: Inquire about accepted insurance providers.

### Entities Captured
- `patient_first_name`, `patient_last_name`
- `caller_first_name`, `caller_last_name`
- `patient_dob`, `caller_dob`
- `insurance_company`, `insurance_id`

## License
This project is licensed under the MIT License.

## Contact
For questions or feedback, feel free to reach out:
- **Email:** Adam.RivardWalter@gmail.com  
- **GitHub:** [adamw80](https://github.com/adamw80)
