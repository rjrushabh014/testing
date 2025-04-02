# Chikitsak Healthcare Chatbot

Chikitsak is an interactive healthcare assessment web application built with Flask. It guides users through a symptom assessment process by collecting personal details, engaging in an interactive chat, and generating a detailed report with possible diagnoses.

## Features

- **Multi-Page Experience:**
  - **Homepage:** Collects user details (age, sex).
  - **Chat Interface:** Interactive chat with a healthcare chatbot powered by a generative AI model.
  - **Assessment Complete:** Notifies the user when the assessment is finished.
  - **Possible Conditions:** Displays a list of potential diseases with expandable details.
  - **Assessment Report:** Provides a detailed patient report with an option to download as a PDF.

- **Interactive Chat:** Real-time conversation with an AI healthcare assistant.
- **Dynamic Report Generation:** Generates a report that includes patient history and reported symptoms.
- **PDF Download:** Uses html2pdf.js to allow users to download the report.
- **Loading Bar Animation:** Visual feedback indicating progress during user interactions.

## Technologies Used

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS (Tailwind CSS), JavaScript
- **APIs:** Google Generative AI for chatbot responses
- **PDF Generation:** html2pdf.js
- **Deployment Options:** Render, Fly.io, Railway, PythonAnywhere, Firebase Hosting (with proper configuration)

## Setup Instructions

### Prerequisites

- Python 3.8+ (or later)
- pip (Python package manager)
- (Optional) Node.js if you use Firebase CLI for deployment
- (Optional) NVM (Node Version Manager) for managing Node.js versions on Ubuntu

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/chikitsak.git
   cd chikitsak



## Create and Activate a Virtual Environment:

python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate


## Install Dependencies:

pip install -r requirements.txt


## Start the Flask Server:
flask run


chikitsak/
├── app.py                     # Main Flask application
├── requirements.txt           # Python dependencies
├── templates/
│   ├── homepage.html          # Homepage for user input
│   ├── index.html             # Chat interface
│   ├── Assesment_complete.html  # Assessment complete notification page
│   ├── possible_disease.html    # Possible conditions page with toggling details
│   └── Assesment_report.html    # Detailed assessment report page with PDF download
├── static/
│   ├── style.css              # Custom CSS styles
│   └── script.js              # Custom JavaScript
└── firebase-config.js         # (Optional) Firebase configuration file
