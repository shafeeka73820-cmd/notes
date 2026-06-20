import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campushub.settings')
django.setup()

from django.utils.text import slugify
from .models import Quote, Category

categories = ['motivation', 'wisdom', 'technology', 'education', 'life']
for c in categories:
    Category.objects.get_or_create(name=c, defaults={'slug': slugify(c)})

cat_map = {c.name: c for c in Category.objects.all()}

quotes = [
    {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs", "category": "motivation", "is_famous": True, "source": "Stanford Commencement 2005"},
    {"text": "Code is like humor. When you have to explain it, it's bad.", "author": "Cory House", "category": "technology", "is_famous": False, "source": "Twitter"},
    {"text": "The best time to plant a tree was 20 years ago. The second best time is now.", "author": "Chinese Proverb", "category": "life", "is_famous": True, "source": ""},
    {"text": "Education is the most powerful weapon which you can use to change the world.", "author": "Nelson Mandela", "category": "education", "is_famous": True, "source": ""},
    {"text": "First, solve the problem. Then, write the code.", "author": "John Johnson", "category": "technology", "is_famous": True, "source": ""},
    {"text": "In the middle of every difficulty lies opportunity.", "author": "Albert Einstein", "category": "wisdom", "is_famous": True, "source": ""},
    {"text": "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "author": "Martin Fowler", "category": "technology", "is_famous": True, "source": "Refactoring"},
    {"text": "Learning never exhausts the mind.", "author": "Leonardo da Vinci", "category": "education", "is_famous": True, "source": ""},
    {"text": "The function of good software is to make the complex appear to be simple.", "author": "Grady Booch", "category": "technology", "is_famous": False, "source": ""},
    {"text": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt", "category": "motivation", "is_famous": True, "source": ""},
    {"text": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius", "category": "wisdom", "is_famous": True, "source": ""},
    {"text": "The beautiful thing about learning is that nobody can take it away from you.", "author": "B.B. King", "category": "education", "is_famous": True, "source": ""},
]

for q in quotes:
    cat = cat_map.get(q.pop('category'))
    Quote.objects.get_or_create(text=q['text'], defaults={**q, 'category': cat})

print(f"Seeded {Quote.objects.count()} quotes in {Category.objects.count()} categories.")
