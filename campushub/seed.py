import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campushub.settings')
django.setup()

from students.models import Student

students_data = [
    {"name": "Asha Verma", "roll": 101, "email": "asha@campus.com", "branch": "CSE", "marks": 88, "phone": "9876543210"},
    {"name": "Vikram Singh", "roll": 102, "email": "vikram@campus.com", "branch": "ECE", "marks": 72, "phone": "9876543211"},
    {"name": "Riya Patel", "roll": 103, "email": "riya@campus.com", "branch": "CSE", "marks": 91, "phone": "9876543212"},
    {"name": "Amit Kumar", "roll": 104, "email": "amit@campus.com", "branch": "ME", "marks": 45, "phone": "9876543213"},
    {"name": "Priya Sharma", "roll": 105, "email": "priya@campus.com", "branch": "EEE", "marks": 35, "phone": "9876543214"},
    {"name": "Rohit Das", "roll": 106, "email": "rohit@campus.com", "branch": "CE", "marks": 62, "phone": "9876543215"},
]

for data in students_data:
    Student.objects.get_or_create(roll=data["roll"], defaults=data)

print(f"Seeded {Student.objects.count()} students.")
