# Fun Time Childcare Operations Management System (COMS)

A comprehensive Django-based operations management system designed specifically for childcare centers. The system streamlines daily operations including attendance tracking, enrolment management, and staff administration, all with a modern pink-themed interface and real-time functionality.

## Features

### Attendance Management
- Real-time attendance tracking
- Automated attendance reports
- Mobile-friendly interface

### Enrolment Management
- Multi-step enrolment process
- Child information management
- Parent/guardian information
- Emergency contact details
- Medical information
- Document management

### Staff Management
- Teacher login system
- Profile management
- Role-based access control
- Dashboard with attendance overview

### System Features
- Pink-themed UI with modern design
- Responsive Bootstrap 5 interface
- Font Awesome icons
- Secure authentication system
- Custom form validation
- Data validation and error handling
- Message notifications
- Static file management

## Getting Started

### Prerequisites
- Python 3.13 or higher
- Django 5.2.1
- PostgreSQL (recommended) or SQLite
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/christopherece/childcarecrm_prj.git
cd childcarecrm_prj
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Access the application at `http://localhost:8000`

## Project Structure

```
childcarecrm_prj/
├── attendance/           # Attendance tracking app
├── enrolment/           # Enrolment management app
├── reports/             # Report generation app
├── static/              # Static files (CSS, JS, images)
├── templates/           # Template files
├── manage.py            # Django management script
└── requirements.txt     # Project dependencies
```

## Usage

### Teacher Login
1. Access the login page at `/login/`
2. Enter your credentials
3. After logging in, you'll be redirected to the dashboard

### Attendance Monitoring
1. Navigate to the Monitor page
2. Use QR code scanner for check-in/check-out
3. View real-time attendance status

### Enrolment Process
1. Start enrolment at `/enrolment/start/`
2. Fill out child information
3. Complete parent/guardian details
4. Add medical information
5. Enter emergency contact details

## Form Validation

All forms include:
- Required field validation
- Phone number format validation
- Email format validation
- Empty value handling
- Placeholder text for empty fields
- Success/error messages

## Security Features

- Secure password hashing
- CSRF protection
- Session management
- Role-based access control
- Input validation
- XSS protection

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Christopher Ancheta - christopher.ancheta@otago.ac.nz

Project Link: https://github.com/christopherece/childcarecrm_prj Attendance System

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![Django 5.2.1](https://img.shields.io/badge/django-5.2.1-blue.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern Django-based web application for managing childcare attendance with real-time tracking, notifications, and comprehensive reporting capabilities.

## 🚀 Features

### 📱 Attendance Management
- ✅ Real-time attendance tracking with sign-in/sign-out functionality
- ✅ Late sign-in notifications with customizable reasons
- ✅ Comprehensive attendance records with historical data
- ✅ Status-based filtering (Present/Absent)
- ✅ Room-based attendance tracking
- ✅ Last 7 days attendance summary
- ✅ Attendance rate calculation
- ✅ Average sign-in/sign-out times
- ✅ Responsive design for mobile and tablet devices

### 📝 Enrolment Management
- ✅ Multi-step enrolment process:
  - Child information (name, DOB, gender, emergency contact)
  - Parent/Guardian details
  - Medical information:
    - Allergies
    - Medical conditions
    - Medications
    - Medical notes
    - Immunization records
  - Emergency contact details
  - Document management
- ✅ Profile picture upload
- ✅ Data validation and error handling
- ✅ Form field validation
- ✅ Required field checks
- ✅ File upload validation

### 👥 Child Management
- ✅ Child details view with:
  - Basic information
  - Emergency contact details
  - Medical information
  - Attendance records
  - Profile picture
- ✅ Editable child information
- ✅ Emergency contact management
- ✅ Medical record management
- ✅ Document viewing (immunization records)

### 📊 Reports and Analytics
- ✅ Child attendance reports
- ✅ Custom date range selection
- ✅ Attendance statistics
- ✅ PDF report generation
- ✅ Room-based attendance summaries
- ✅ Historical attendance tracking

### 🏫 Center Management
- ✅ Center information management
- ✅ Room management with capacity tracking
- ✅ Opening time configuration
- ✅ Center-wide attendance overview
- ✅ Staff assignments
- ✅ Room-based child management

### 👩‍🏫 Staff Management
- ✅ Teacher login system
- ✅ Profile management
- ✅ Role-based access control
- ✅ Dashboard with attendance overview
- ✅ Room assignments
- ✅ Child monitoring capabilities

### 🔐 Security Features
- ✅ Secure password hashing
- ✅ CSRF protection
- ✅ Session management
- ✅ Role-based access control
- ✅ Input validation
- ✅ XSS protection
- ✅ Secure file uploads

### 🎨 UI/UX Features
- ✅ Pink-themed modern interface
- ✅ Responsive Bootstrap 5 design
- ✅ Font Awesome icons
- ✅ Real-time updates
- ✅ Intuitive navigation
- ✅ Consistent styling across all pages
- ✅ Mobile-friendly interface
- ✅ Interactive forms with validation feedback

### 📱 Mobile Features
- ✅ QR code scanner for check-in/check-out
- ✅ Mobile-optimized interface
- ✅ Touch-friendly controls
- ✅ Offline support
- ✅ Push notifications for important updates

### 🔄 System Features
- ✅ Data validation and error handling
- ✅ Custom form validation
- ✅ Message notifications
- ✅ Static file management
- ✅ Database optimization
- ✅ Performance optimization
- ✅ Error logging and monitoring
- ✅ Backup and recovery capabilities

### 👥 User Roles
- 📝 Teachers: 
  - Manage attendance
  - View records
  - Update profiles
  - Monitor students by room
  - Filter attendance by status
- ⚙️ Admin: 
  - Full access to all features
  - System management
  - Center configuration
  - User management

## 📁 Project Structure

```
childcare_attendace/
├── attendance/           # Main application
│   ├── models.py        # Database models (Child, Parent, Attendance, etc.)
│   ├── views.py         # Application views
│   ├── forms.py         # Forms for data entry
│   └── templates/       # HTML templates
│       └── attendance/
├── notifications/       # Notification system
├── reports/            # Report generation
└── static/             # Static files (CSS, JS, images)
```

## 🛠️ Setup Instructions

1. **Prerequisites**:
   - Python 3.13 or higher
   - Django 5.2.1
   - PostgreSQL (recommended) or SQLite
   - pip (Python package manager)

2. **Installation Steps**:
   ```bash
   # Clone the repository
   git clone https://github.com/christopherece/childcarecrm_prj.git
   cd childcarecrm_prj
   
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Set up the database
   python manage.py makemigrations
   python manage.py migrate
   
   # Create a superuser (optional)
   python manage.py createsuperuser
   
   # Run the development server
   python manage.py runserver
   ```

3. **Access the Application**:
   - Open your web browser and navigate to `http://localhost:8000`
   - Login with your credentials
   - Start using the system!

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
# Create .env file in project root
# Add the following variables:
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=your-database-url
EMAIL_HOST=your-email-host
EMAIL_PORT=your-email-port
EMAIL_HOST_USER=your-email-user
EMAIL_HOST_PASSWORD=your-email-password
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Configure database settings in `settings.py`:
- PostgreSQL is recommended
- Ensure timezone is set to 'Pacific/Auckland'

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser (for admin access):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Access the application:
- Main application: http://localhost:8000
- Admin panel: http://localhost:8000/admin

### 📊 Usage

### 📱 Teacher Login
- Teachers can log in using their credentials
- Dashboard shows all children in their center
- Live search functionality for quick lookup
- Monitor view for room-based attendance tracking
- Filter students by room and attendance status

### 📅 Attendance Management
- Sign-in/Sign-out functionality with timestamps
- Automatic notifications to parents
- Late sign-in tracking with reasons
- Attendance records view with detailed information
- Notes tracking for special attendance circumstances

### 📧 Notifications
- Email notifications for sign-ins and late arrivals
- Customizable notification templates
- Notification history tracking

## 📊 Database Schema

### 📝 Key Models
- Child: Stores child information, parent relationship, and attendance records
- Parent: Contact information and relationship to children
- Attendance: Tracks sign-in/sign-out times, status, and notes
- Center: Childcare center information including capacity and contact details
- Teacher: Staff profiles with center assignments

## 🔐 Security
- All pages require authentication
- Role-based access control
- CSRF protection for forms
- Secure password hashing
- Email verification for notifications

## 🕒 Timezone Handling
- All timestamps are stored in UTC
- Displayed in Pacific/Auckland timezone
- Automatic timezone conversion for user interface

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, please open an issue in the GitHub repository.

## 📚 Documentation

- [User Guide](docs/user_guide.md)
- [API Documentation](docs/api.md)
- [Deployment Guide](docs/deployment.md)

## 🎯 Roadmap

- [ ] Multi-language support
- [ ] Mobile app integration
- [ ] Advanced reporting features
- [ ] Parent portal
- [ ] Analytics dashboard
