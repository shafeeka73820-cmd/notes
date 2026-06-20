import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campushub.settings')
django.setup()

from django.utils.text import slugify

# ===== Departments =====
from students.models import Department, Student
depts = {'CSE': 'Computer Science', 'ECE': 'Electronics', 'EEE': 'Electrical', 'ME': 'Mechanical', 'CE': 'Civil'}
for code, name in depts.items():
    Department.objects.get_or_create(code=code, defaults={'name': name})

# ===== Students =====
students_data = [
    {"name": "Asha Verma", "roll": 101, "email": "asha@campus.com", "branch": "CSE", "marks": 88},
    {"name": "Vikram Singh", "roll": 102, "email": "vikram@campus.com", "branch": "ECE", "marks": 72},
    {"name": "Riya Patel", "roll": 103, "email": "riya@campus.com", "branch": "CSE", "marks": 91},
    {"name": "Amit Kumar", "roll": 104, "email": "amit@campus.com", "branch": "ME", "marks": 45},
    {"name": "Priya Sharma", "roll": 105, "email": "priya@campus.com", "branch": "EEE", "marks": 35},
    {"name": "Rohit Das", "roll": 106, "email": "rohit@campus.com", "branch": "CE", "marks": 62},
    {"name": "Sneha Gupta", "roll": 107, "email": "sneha@campus.com", "branch": "CSE", "marks": 95},
    {"name": "Arun Nair", "roll": 108, "email": "arun@campus.com", "branch": "ECE", "marks": 78},
    {"name": "Divya K", "roll": 109, "email": "divya@campus.com", "branch": "CSE", "marks": 85},
]
dept_map = {d.code: d for d in Department.objects.all()}
for s in students_data:
    s['department'] = dept_map.get(s['branch'])
    Student.objects.get_or_create(roll=s['roll'], defaults=s)

# ===== Quotes =====
from quotes.models import Quote, Category
cats = ['motivation', 'wisdom', 'technology', 'education', 'life']
for c in cats:
    Category.objects.get_or_create(name=c, defaults={'slug': slugify(c)})
cat_map = {c.name: c for c in Category.objects.all()}
quotes = [
    {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs", "cat": "motivation", "famous": True, "src": "Stanford 2005"},
    {"text": "Code is like humor. When you have to explain it, it is bad.", "author": "Cory House", "cat": "technology", "famous": False, "src": "Twitter"},
    {"text": "The best time to plant a tree was 20 years ago. The second best time is now.", "author": "Chinese Proverb", "cat": "life", "famous": True, "src": ""},
    {"text": "Education is the most powerful weapon which you can use to change the world.", "author": "Nelson Mandela", "cat": "education", "famous": True, "src": ""},
    {"text": "First, solve the problem. Then, write the code.", "author": "John Johnson", "cat": "technology", "famous": True, "src": ""},
    {"text": "In the middle of every difficulty lies opportunity.", "author": "Albert Einstein", "cat": "wisdom", "famous": True, "src": ""},
    {"text": "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "author": "Martin Fowler", "cat": "technology", "famous": True, "src": "Refactoring"},
    {"text": "Learning never exhausts the mind.", "author": "Leonardo da Vinci", "cat": "education", "famous": True, "src": ""},
    {"text": "The function of good software is to make the complex appear simple.", "author": "Grady Booch", "cat": "technology", "famous": False, "src": ""},
    {"text": "Believe you can and you are halfway there.", "author": "Theodore Roosevelt", "cat": "motivation", "famous": True, "src": ""},
    {"text": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius", "cat": "wisdom", "famous": True, "src": ""},
    {"text": "The beautiful thing about learning is that nobody can take it away from you.", "author": "B.B. King", "cat": "education", "famous": True, "src": ""},
]
for q in quotes:
    cat = cat_map.get(q['cat'])
    Quote.objects.get_or_create(text=q['text'], defaults={'author': q['author'], 'category': cat, 'is_famous': q['famous'], 'source': q['src']})

print(f"Seeded: {Department.objects.count()} depts, {Student.objects.count()} students, {Quote.objects.count()} quotes")
