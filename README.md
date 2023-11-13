UNRCE Website Project
Introduction
Welcome to the GitHub repository of the UNRCE Website, a Django-based web application designed for the United Nations Regional Centre of Expertise (UNRCE). This project aims to facilitate easy access to project reporting, organization details, and member profiles within the UNRCE community.

Project Setup
To get started with the UNRCE Website project, follow these steps:

Clone the repository:

bash
Copy code
git clone "https://github.com/HaitianWang/UNRCE-Database-project"
Navigate to the project directory:

bash
Copy code
cd UNRCE-django
Install virtualenv:

css
Copy code
python -m pip install --user virtualenv
Create a virtual environment:

bash
Copy code
python -m venv env
Activate the virtual environment:

Mac: source env/bin/activate
Windows: .\env\Scripts\activate
Install required packages:

Copy code
pip install -r requirements.txt
Run the Django server:

Copy code
python3 manage.py runserver
Features
The UNRCE Website provides a range of features, including:

Account Management: Users can manage their profiles, update personal details, and set preferences.
Project Management: Facilitates creating, viewing, and managing projects with an approval workflow.
Organizations: View and manage organization profiles and details.
User and Project Search: Advanced search capabilities for users and projects.
FAQ and Contact Us Pages: Provides helpful information and contact details.
For a detailed guide on how to use these features, refer to the project documentation.

Contribution
Interested in contributing? Please read our contribution guidelines for details on our code of conduct, and the process for submitting pull requests.

License
This project is licensed under the [LICENSE NAME] - see the LICENSE.md file for details.
