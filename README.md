# UNRCE Official Website
***Empowering Global Collaboration and Community Engagement***

## Introduction

The UNRCE Database Project is a comprehensive Django-based web application developed for the United Nations Regional Centre of Expertise (UNRCE). This application is designed to streamline the management and visibility of projects, organizations, and user profiles within the UNRCE community. Our platform is tailored to facilitate collaboration and enhance user engagement across various UNRCE initiatives. Website has been host and applied.

## Architecture

### Django and MVC Pattern

This project is structured using the Django framework, adhering to the Model-View-Controller (MVC) architecture. This design pattern ensures a clean separation of concerns, with each component handling its specific aspect of the application:

- **Model:** Manages the data and business logic of the application.
- **View:** Renders data to the user and handles user interaction.
- **Controller:** Processes user requests and renders the appropriate view.

## Getting Started

To set up and run the UNRCE Database Project on your local machine, follow these steps:

1. **Clone the Repository:**
`git clone https://github.com/HaitianWang/UNRCE-Database-project`


1. **Navigate to Project Directory:**
`cd UNRCE-django`


3. **Set Up Virtual Environment:**
`python -m venv env`


4. **Activate Virtual Environment:**
- Mac: `source env/bin/activate`
- Windows: `./env/Scripts/activate`

5. **Install Dependencies:**
`pip install -r requirements.txt`


6. **Run the Server:**
`python3 manage.py runserver`

## Configuring API Keys

UNRCE relies on several external API to provide its full range of features. To get the application running properly, you'll need to configure the API key for SendGrid. Open the [views.py](./UNRCE-django/UNRCE_APP/views.py) file and modify the following:

#### SendGrid API Key (for email services)
**Locate the line in your code:** `sg = SendGridAPIClient('Please enter your SendGrid API key')`  
**Provide your OpenAI API Key:** Replace the placeholder text with your actual SendGrid API key.

#### Important Notes
- Securing API Keys: It's crucial to keep your API keys confidential. Avoid pushing these keys to public repositories or sharing them in insecure environments.
- API Key Permissions: Ensure that your API keys have the necessary permissions for the services required by MealMate.
- Changes in Code: After updating the API keys in the code, save the changes and restart the server to apply them.

## Features

The UNRCE Database Project includes a variety of features designed to enhance user experience:

- **User Account Management:** Enables users to manage their profiles and settings.
- **Project Submission and Approval:** Streamlines the process of project creation, submission, and administrative approval.
- **Organization Profiles:** Allows for detailed views and management of various organizations within the UNRCE.
- **Comprehensive Search Functionality:** Provides robust search capabilities for users, projects, and organizations.
- **Interactive FAQ and Contact Pages:** Offers users assistance and direct communication channels.

## Contributing

We welcome contributions to the UNRCE Database Project. Please ensure to read our [contribution guidelines](LINK_TO_CONTRIBUTION_GUIDELINES) before making a pull request.

## License

This project is licensed under MIT. For more details, see the [LICENSE](./LICENSE) file.

