# SDP Grading System

## Overview

The SDP Grading System is a web-based application designed to streamline the grading process for Senior Design Projects at Khalifa University's Electrical & Computer Engineering Department. This system aims to improve efficiency, accuracy, and security in managing student grades and feedback.

## Features

- Secure user authentication and role-based access control
- Grade entry and management for examiners
- Real-time grade viewing for students
- Comprehensive reporting tools for coordinators
- Automated grade calculations and data processing

## Technology Stack

- Backend: Django (Python)
- Database: SQLite
- Frontend: Django Templating Engine, HTML, CSS, JavaScript
- Additional Libraries: openpyxl for Excel report generation

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/AhsanRao/sdp-grading-system.git
   ```

2. Navigate to the project directory:
   ```
   cd sdp-grading-system
   ```

3. Create a virtual environment:
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

5. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

6. Apply database migrations:
   ```
   python manage.py migrate
   ```

7. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

8. Run the development server:
   ```
   python manage.py runserver
   ```

## Usage

1. Access the application through a web browser at `http://localhost:8000`
2. Log in using your credentials based on your role (student, examiner, or coordinator)
3. Navigate through the interface to perform role-specific tasks

## Project Structure

- `accounts/`: User authentication and management
- `grading/`: Core grading functionality
- `reports/`: Report generation and management
- `templates/`: HTML templates for the frontend
- `static/`: Static files (CSS, JavaScript, images)

## Contributing

We welcome contributions to the SDP Grading System. Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For any queries or support, please contact the project team at [email@example.com](mailto:email@example.com).

## Acknowledgments

- Khalifa University, Electrical & Computer Engineering Department
- All contributors and testers who helped shape this project