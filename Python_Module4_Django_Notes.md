# MODULE 4 — DJANGO WEB FRAMEWORK (BACKEND)
### Complete Study Notes for B.Tech / Engineering Students
*A Textbook-Style + Classroom Lecture + Lab Manual + Django Bootcamp Handbook + Exam & Placement Guide*

---

## 📑 TABLE OF CONTENTS

| # | Topic | Section |
|---|-------|---------|
| 4.1 | Django Introduction & Project Setup | §1 |
| 4.2 | URL Routing & Views | §2 |
| 4.3 | Django Templates | §3 |
| 4.4 | Django Models & ORM | §4 |
| 4.5 | Django Forms & Validation | §5 |
| 4.6 | Django Admin Panel | §6 |
| 4.7 | User Authentication System | §7 |
| 4.8 | Class-Based Views (CBV) | §8 |
| 4.9 | File Upload & Media Handling | §9 |
| — | Capstone Projects (5 complete applications) | §10 |
| — | Final Module Section (Cheat Sheets, Top-100s) | §11 |

> 🧵 **The running thread:** from Topic 4.1 onward we progressively build **one real application — `campushub`** (a college portal with a `students` app) — so every new concept lands inside a growing, working project. By Topic 4.9 you'll have touched every layer of a production-shaped Django app.

---
---

# §1. TOPIC 4.1 — DJANGO INTRODUCTION & PROJECT SETUP

## 4.1.1 Introduction to Web Frameworks

### What Is a Web Framework?

> **Definition:** A **web framework** is a pre-built collection of code, tools, and conventions that handles the **repetitive plumbing** of web applications — URL handling, database access, security, templating, sessions — so developers write only the logic unique to *their* application.

**Why frameworks exist — the pain they remove:** In Modules 2–3 you saw the raw pieces: Python scripts talking to MySQL, HTML pages served somehow. Build a real website by hand and you must write: an HTTP request parser, URL-to-code dispatcher, SQL for every query, session/cookie handling, password hashing, CSRF protection, HTML escaping… **thousands of lines before your first feature.** Frameworks ship all of this, tested by millions.

**Real-world analogy:** Building a web app without a framework is **building a house starting from making your own bricks** 🧱. A framework is a **prefab construction kit** — foundation, walls, plumbing, and wiring standardized and delivered; you design the rooms and decorate.

### Backend vs Frontend (the Module 3 ↔ Module 4 bridge)

| | Frontend (Module 3) | Backend (Module 4) |
|---|---------------------|--------------------|
| Runs on | the **browser** | the **server** |
| Built with | HTML, CSS, Bootstrap | **Python + Django** |
| Responsibilities | display, interaction | logic, data, security, sessions |
| Example | the login form's look | verifying the password, creating the session |

Django **generates** and serves the frontend (your Module-3 HTML/Bootstrap pages become Django *templates*) while running all logic and database work (your Module-1 Python + Module-2 SQL skills) behind the scenes. **Module 4 is where all three previous modules fuse.**

### MVC vs MVT Architecture (preview — detailed in 4.1.3)
Most frameworks organize code as **MVC** (Model–View–Controller). Django uses its own dialect, **MVT** (Model–View–Template). Same separation-of-concerns idea, different naming — fully compared in §4.1.3.

## 4.1.2 Introduction to Django

> **Definition:** **Django** is a free, open-source, **high-level Python web framework** that encourages rapid development and clean, pragmatic design. Tagline: *"The web framework for perfectionists with deadlines."*

### History of Django

| Year | Event |
|------|-------|
| 2003 | Created by **Adrian Holovaty & Simon Willison** at the *Lawrence Journal-World* newspaper (Kansas, USA) — newsrooms need sites built FAST |
| **2005** | Open-sourced; named after jazz guitarist **Django Reinhardt** 🎸 |
| 2008 | Django Software Foundation (DSF) formed; v1.0 |
| 2015–now | Long-Term Support (LTS) releases; Django 4.x/5.x — async support, modern Python |

**Who uses it:** Instagram (one of the largest Django deployments on Earth), Pinterest (origins), Spotify, Dropbox, NASA, Mozilla, YouTube (parts), Disqus — proof it scales from college project to a billion users.

### Why Django Is Popular ⭐
1. **Batteries included** — ORM, admin panel, auth, forms, security, sessions, i18n: in the box.
2. **Python** — you already speak the language (Module 1).
3. **Fast development** — a CRUD app in an afternoon.
4. **Security by default** — CSRF, XSS, SQL-injection protections built in (recall Module 2's injection battles — Django's ORM parameterizes for you).
5. **Scalable & mature** — 20 years of battle-testing, superb documentation.
6. **The free admin panel** — an instant back-office UI for your data (Topic 4.6) that other frameworks simply don't have.

### Django Philosophy
- **DRY — Don't Repeat Yourself:** every piece of knowledge lives in exactly one place (define a model once → forms, admin, and DB schema derive from it).
- **Convention over configuration:** sensible defaults; standard project layout.
- **Explicit is better than implicit** (Pythonic — from the Zen of Python).
- **Loose coupling:** models, views, templates replaceable independently.
- **Batteries-included:** the standard library approach (Module 1.4!) applied to web development — but **swappable** batteries.

## 4.1.3 MVT Architecture ⭐⭐ (the heart of every Django exam)

> **Definition:** **MVT (Model–View–Template)** is Django's architectural pattern dividing an application into three cooperating layers: **Model** (data), **View** (logic), **Template** (presentation).

### The Three Layers in Extreme Detail

**MODEL — the data layer 🗄**
- A Python **class** describing one database table (fields = columns).
- Lives in `models.py`; Django's **ORM** translates it to SQL (CREATE TABLE, SELECT…) — you write Python, Django writes the Module-2 SQL.
- Also home to data-level rules and behavior (validation, computed properties).

**VIEW — the logic layer 🧠**
- A Python **function (or class)** that receives an `HttpRequest`, does the work (query models, validate forms, decide outcomes), and returns an `HttpResponse`.
- Lives in `views.py`. **Crucial naming trap:** Django's "view" = the **controller/business logic**, *not* the visual page!

**TEMPLATE — the presentation layer 🎨**
- An **HTML file with placeholders** (`{{ variable }}`) and light logic (`{% for %}`) that the view fills with data.
- Your entire Module 3 skill set lives here — templates ARE your HTML/Bootstrap pages, now dynamic.

### MVT vs MVC ⭐ (guaranteed viva question)

| Concern | Classic MVC name | Django MVT name |
|---------|------------------|------------------|
| Data / database | Model | **Model** (same) |
| Business logic deciding what happens | **Controller** | **View** 😮 |
| Presentation / what user sees | **View** | **Template** |
| Who routes requests to logic? | programmer-written Controller wiring | **Django itself** (urls.py + framework) |

> 💡 **Memory Trick:** *"Django shifted the names one step: MVC's Controller → MVT's View, MVC's View → MVT's Template."* When an interviewer asks "where is Django's controller?" answer: **the framework itself plus urls.py** play the controller role; your views hold the logic.

### Django Request–Response Cycle ⭐⭐ (memorize this diagram)
```
 BROWSER                                DJANGO SERVER
 ───────                                ─────────────
 ① GET /students/5/  ───────────────▶  ② URL DISPATCHER (urls.py)
                                           "which view handles this path?"
                                                  │ matched!
                                                  ▼
                                        ③ VIEW (views.py)
                                           business logic runs…
                                                  │ needs data
                                                  ▼
                                        ④ MODEL (models.py + ORM)
                                           SELECT … FROM students WHERE id=5
                                           ◀── database row returned
                                                  │ data in hand
                                                  ▼
                                        ⑤ TEMPLATE (student.html)
                                           {{ placeholders }} filled with data
                                                  │ final HTML
 ⑦ Browser renders  ◀───────────────── ⑥ HttpResponse(html) sent back
    the page (Module 3 takes over!)
```
**One-line story for exams:** *URL → View → Model → Template → Response.* Every single page load in every Django site follows exactly these steps.

## 4.1.4 Project Environment Setup

### Python Environment
```bash
python --version        # need 3.10+ (Windows: python, Mac/Linux often python3)
pip --version           # pip = Python's package installer (Module 1 & 2 friend)
```

### Virtual Environments ⭐ — non-negotiable professional habit

> **Definition:** A **virtual environment** is an isolated, per-project Python installation with its **own** packages, so Project A's Django 5.0 never collides with Project B's Django 4.2.

**Analogy:** separate **toolboxes per job site** 🧰 — instead of one global toolbox where swapping a screwdriver for one job breaks another job.

```bash
# CREATE (inside your projects folder)
python -m venv env            # 'env' = folder holding the isolated Python

# ACTIVATE  — your prompt grows an (env) prefix = you're inside
env\Scripts\activate          # Windows
source env/bin/activate       # macOS / Linux

# ... work, install packages — they land only in env/ ...

deactivate                    # leave the environment
```
> ⚠️ **Warning:** The #1 beginner bug — installing Django globally but running the project elsewhere ("`ModuleNotFoundError: No module named 'django'`"). **Always check for `(env)` in your prompt before pip or runserver.** Also: never commit `env/` to Git; commit a `requirements.txt` instead (`pip freeze > requirements.txt`).

### Installing Django
```bash
pip install django                 # latest stable
pip install django==5.0.6          # exact version (team consistency!)
django-admin --version             # verify, e.g. 5.0.6
python -m django --version         # alternative check
```

## 4.1.5 Creating the Django Project

```bash
django-admin startproject campushub
cd campushub
```
### Generated Project Structure ⭐
```
campushub/                  ← outer folder (just a container; rename freely)
├── manage.py               ← your command-line remote control
└── campushub/              ← inner folder = the actual Python package (settings home)
    ├── __init__.py          (marks it a package — Module 1.4!)
    ├── settings.py          ← the project's brain/configuration
    ├── urls.py              ← master URL table (the "reception desk")
    ├── asgi.py              ← async server entry point (modern deployments)
    └── wsgi.py              ← classic server entry point (deployments)
```
| File | Role (one-liner you must know) |
|------|--------------------------------|
| **manage.py** | runs admin tasks: `runserver`, `startapp`, `makemigrations`, `migrate`, `createsuperuser` — never edit it |
| **settings.py** | every project setting: `INSTALLED_APPS`, `DATABASES`, `TEMPLATES`, `STATIC_URL`, `DEBUG`, `SECRET_KEY` |
| **urls.py** | maps URL patterns → views (project-level router) |
| **wsgi.py** | Web Server Gateway Interface — how production servers (Gunicorn/Apache) talk to Django |
| **asgi.py** | Asynchronous SGI — same job for async servers (websockets, async views) |

## 4.1.6 Apps in Django ⭐

> **Definition:** An **app** is a self-contained Django module implementing **one feature area** (students, blog, payments). A **project** is the overall website — a configuration shell that combines one or more apps.

### Project vs App — the comparison every viva asks

| | **Project** | **App** |
|---|------------|---------|
| What | the whole website / configuration | one functional component |
| How many | one per site | many per project |
| Created by | `startproject` | `startapp` |
| Contains | settings.py, root urls.py | models.py, views.py, templates |
| Reusable elsewhere? | no | **yes** — plug into other projects |

**Analogy:** the project is a **shopping mall** 🏬 (one building, one address, one electricity board = settings); apps are the **individual shops** (each self-contained, each could open a branch in another mall). Real example: Instagram-like project = `accounts` app + `posts` app + `chat` app + `notifications` app.

**Best practices:** one app = one purpose, named as a plural noun (`students`, `orders`); split when an app grows multiple unrelated responsibilities.

### Creating an App & App Structure
```bash
python manage.py startapp students
```
```
students/
├── migrations/        ← auto-generated DB change scripts (Topic 4.4)
├── __init__.py
├── admin.py           ← register models for the admin panel (Topic 4.6)
├── apps.py            ← app configuration class (rarely touched)
├── models.py          ← database tables as Python classes (Topic 4.4)
├── tests.py           ← automated tests live here
└── views.py           ← request-handling logic (Topic 4.2)
```
**⭐ CRITICAL STEP — register the app** in `campushub/settings.py`, or Django ignores it:
```python
INSTALLED_APPS = [
    'django.contrib.admin',        # the built-in batteries…
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'students',                    # ← OUR APP (forgetting this = hours of confusion)
]
```

## 4.1.7 The Development Server

```bash
python manage.py runserver           # default http://127.0.0.1:8000/
python manage.py runserver 9000      # custom port
```
**Output:**
```
Watching for file changes with StatReloader
System check identified no issues (0 silenced).
Django version 5.0.6, using settings 'campushub.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```
Open the URL → the green-rocket 🚀 "The install worked successfully!" page. The server **auto-reloads** on every code save (StatReloader).

**DEBUG mode (`settings.py`):** `DEBUG = True` shows detailed yellow error pages with full tracebacks — a development superpower and a production catastrophe (it leaks settings, paths, code). Rule: **DEBUG=True locally, DEBUG=False + ALLOWED_HOSTS set in production.** *(127.0.0.1 = localhost = "this machine" — same client–server picture as Modules 2 & 3, now you own the server!)*

## 4.1.8 END-OF-TOPIC PACK (4.1)

### Quick Revision Notes
- Framework = prebuilt web plumbing; Django = Python, batteries-included, DRY (2005, Lawrence Journal-World, named for Django Reinhardt).
- **MVT:** Model=data(ORM), View=logic(!), Template=HTML; Django+urls.py play MVC's controller.
- Cycle: **URL → View → Model → Template → Response.**
- Setup ritual: `python -m venv env` → activate → `pip install django` → `django-admin startproject campushub` → `python manage.py startapp students` → add to `INSTALLED_APPS` → `runserver`.
- manage.py=commands, settings.py=config, urls.py=router, wsgi/asgi=deployment doors.
- Project = mall (one), Apps = shops (many, reusable).

### Important Definitions
Web framework • Django • MVT • Model • View • Template • Virtual environment • Project • App • Development server • DEBUG mode • WSGI/ASGI.

### FAQs
1. *Is Django frontend or backend?* → Backend — but it renders/serves your frontend templates.
2. *django-admin vs manage.py?* → same toolset; manage.py additionally points at YOUR settings — after creating a project, prefer manage.py.
3. *"No module named django"?* → venv not activated (look for `(env)`).
4. *Can one project use many apps? One app in many projects?* → yes and yes (that's the point).
5. *Why does my new app's stuff not appear?* → not added to INSTALLED_APPS.

### Viva Questions
1. Expand MVT; map each letter to a file. 2. Django's controller is…? 3. Year open-sourced & origin? 4. Command to create a project? An app? 5. Purpose of manage.py (3 examples). 6. What is DRY? 7. Why virtual environments? 8. Default dev-server address/port? 9. wsgi vs asgi in one line. 10. What is "batteries included"?

### Interview Questions
1. Walk through the request–response cycle for `/students/5/`.
2. MVT vs MVC — names table + who routes.
3. Project vs app with the mall analogy + a real decomposition (e-commerce).
4. What does settings.py control? Name six keys.
5. Why is Django called secure by default? *(CSRF, XSS-escaping, ORM parameterization, hashed passwords)*
6. DEBUG=True dangers in production.
7. What problem do virtual environments solve; what is requirements.txt?
8. Name five companies on Django and what that implies about scalability.

### MCQs
1. Django is written in: a) PHP b) **Python** ✓ c) Java d) JS
2. MVT's T = a) Transaction b) **Template** ✓ c) Table d) Test
3. Business logic lives in Django's: a) Model b) **View** ✓ c) Template d) URL
4. Create an app: a) startproject b) **python manage.py startapp** ✓ c) newapp d) django-admin app
5. Default port: a) 80 b) 3306 c) **8000** ✓ d) 5000
6. File listing INSTALLED_APPS: a) urls.py b) **settings.py** ✓ c) admin.py d) apps.py

### Short / Long Answer Questions
**Short:** 1. Three Django philosophy points. 2. venv create/activate commands (both OSes). 3. Five generated project files + one-line roles. 4. Project vs app (3 differences). 5. What happens on `runserver`?
**Long:** 1. MVT in extreme detail with diagram + MVC comparison. 2. Complete environment-to-first-page walkthrough (every command, every file explained). 3. Django history, philosophy, and why-popular essay with real-world users. 4. Anatomy of project and app structures with the purpose of every file.

### Practical Lab Questions
1. Create venv `env`, install Django, freeze requirements.txt, show `(env)` in a screenshot.
2. Create project `campushub` + app `students`; register it; runserver; capture the rocket page.
3. Break it on purpose: comment the app out of INSTALLED_APPS, observe; restore.
4. Run the server on port 9090 and from another device on your LAN (`runserver 0.0.0.0:9090`).

### Debugging Exercises
```
1) ModuleNotFoundError: No module named 'django'        → activate the venv
2) "That port is already in use"                        → another runserver alive; use another port / kill it
3) App created but models/admin ignored                 → missing from INSTALLED_APPS
4) python manage.py runserver → "No such file"          → you're in the OUTER folder's parent; cd to where manage.py lives
5) Edited settings.py of a DIFFERENT old project        → two projects open; check the path in runserver's output line
```

### Assignment Questions
1. One-page essay: "How Django implements DRY" with three concrete mechanisms.
2. Comparison chart: Django vs Flask vs FastAPI (10 parameters).
3. Diagram poster of the request-response cycle, hand-annotated with file names.

### Coding Exercises
1. Script the full setup as a shell/batch file (venv → install → startproject → runserver).
2. Create a project with TWO apps (`students`, `library`) and register both.
3. Explore `python manage.py help` — document five commands you haven't met yet.

### Scenario-Based Questions
1. *Teammate's machine runs Django 4.2, yours 5.0; code breaks on theirs.* → pin versions via requirements.txt inside venvs.
2. *Client wants a news site AND a job board on one domain.* → one project, two apps; justify.
3. *Your deployed site shows full tracebacks to visitors.* → DEBUG left True; explain the fix and the risk.

### Mini Project Ideas
"Hello Department" multi-app skeleton (3 registered apps) • setup-automation script with README • a slide-deck teaching MVT to juniors using your own diagrams.

### Summary
Django is Python's batteries-included web framework: MVT separates data (Model), logic (View), and presentation (Template), with Django itself routing requests via urls.py — URL → View → Model → Template → Response. Professional work starts in a virtual environment, a project is the configuration shell created by `startproject`, features live in reusable apps created by `startapp` and registered in INSTALLED_APPS, and `runserver` gives you an auto-reloading development site at 127.0.0.1:8000. The stage is set — next, we wire URLs to our own views.

---
---
# §2. TOPIC 4.2 — URL ROUTING & VIEWS

## 4.2.1 Introduction to Routing

> **Definition:** **URL routing** is the mechanism that maps an incoming **URL pattern** to the **view function** that should handle it. The router is Django's reception desk: every request first asks *"who handles this address?"*

**Why routing is needed:** one server, thousands of pages — `/`, `/students/`, `/students/5/`, `/about/` — something must dispatch each path to the right Python code. Without routing you'd have one giant if-elif on the raw URL string (and people did, in the dark ages of CGI scripts).

```
        REQUEST: GET /students/5/
                     │
                     ▼
   ┌  campushub/urls.py (PROJECT router) ┐
   │  ''        → home view              │
   │  'admin/'  → admin site             │
   │  'students/' → include(students.urls) ──┐
   └─────────────────────────────────────┘   │ hand-off
                                              ▼
   ┌  students/urls.py (APP router) ──────────┐
   │  ''            → views.index             │
   │  '<int:roll>/' → views.detail   ← MATCH! │
   └───────────────────────────────────────────┘
                     │
                     ▼
            views.detail(request, roll=5)
```

## 4.2.2 urls.py — Structure & Flow

**Project urls.py (`campushub/urls.py`):**
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [                       # Django scans this list TOP-DOWN
    path('admin/', admin.site.urls),
    path('students/', include('students.urls')),   # delegate to the app
    path('', include('students.urls')),            # or make it the homepage
]
```
**App urls.py (`students/urls.py` — you create this file):**
```python
from django.urls import path
from . import views                   # the app's own views.py

app_name = 'students'                 # NAMESPACE (see 4.2.7)

urlpatterns = [
    path('', views.index, name='index'),               # /students/
    path('<int:roll>/', views.detail, name='detail'),  # /students/5/
    path('about/', views.about, name='about'),         # /students/about/
]
```
**Routing flow:** request → project urlpatterns top-down → first match wins → if `include()`, the **matched prefix is stripped** and the remainder is tested against the app's patterns → matched view is called. No match anywhere → **404**.
> 📝 **Best practice ⭐:** every app owns its own `urls.py`; the project file only `include()`s them — apps stay portable (plug the shop into any mall).

## 4.2.3 path() and URL Converters

```python
path(route, view, name=None)
#    'students/<int:roll>/'  views.detail  name='detail'
```
**Dynamic parameters:** `<converter:variable>` captures part of the URL and passes it to the view **as a keyword argument** — `/students/5/` → `detail(request, roll=5)` with roll already an `int`.

| Converter | Matches | Example URL part | Passed as |
|-----------|---------|------------------|-----------|
| `int` | digits | `5` | int 5 |
| `str` (default) | any text except `/` | `asha` | 'asha' |
| `slug` | letters, numbers, hyphens, underscores | `python-basics-101` | 'python-basics-101' (SEO-friendly URLs!) |
| `uuid` | universally unique ids | `075194d3-…` | UUID object |
| `path` | any text **including** `/` | `docs/v2/intro` | 'docs/v2/intro' |

```python
path('post/<slug:title>/', views.post, name='post'),
path('files/<path:filepath>/', views.serve_doc),
```
> ⚠️ **Warning:** order matters — put more specific patterns first. `path('<str:name>/')` placed above `path('about/')` would swallow `/about/` as name='about'!

## 4.2.4 Views — the Logic Layer

> **Definition:** A **view** is a Python callable that takes an **HttpRequest** object and returns an **HttpResponse** object. Function-based views (FBV) are plain functions; class-based views (CBV, Topic 4.8) are classes.

### Request–Response Lifecycle of one view call
```
HttpRequest in ─▶ [ VIEW: read request data → talk to models → choose template/data ] ─▶ HttpResponse out
```

### HttpResponse — the raw response
```python
# students/views.py
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Student Portal</h1><p>Welcome!</p>")

def detail(request, roll):                    # roll captured by <int:roll>
    return HttpResponse(f"<h2>Details of student #{roll}</h2>")
```
Visit `/students/` → the h1 renders; `/students/42/` → "Details of student #42". **Use cases:** quick tests, plain-text/JSON-ish outputs, redirects' cousins. For real pages we render templates:

### render() ⭐ — the standard response
```python
from django.shortcuts import render

def index(request):
    students = ["Asha", "Vikram", "Riya"]            # later: from the database!
    context = {                                       # CONTEXT DICTIONARY
        "names": students,                            # key = template variable name
        "count": len(students),
        "title": "Student Portal",
    }
    return render(request, 'students/index.html', context)
#          render(request, template_path, context_dict) → HttpResponse with rendered HTML
```
**What render() does internally:** load template → replace `{{ names }}`, `{{ count }}` with context values → wrap final HTML in an HttpResponse. *(Other shortcuts you'll meet: `redirect('students:index')` → send the browser elsewhere; `get_object_or_404(Model, pk=5)` → fetch-or-404 in one line.)*

## 4.2.5 The Request Object ⭐

Every view's first parameter, carrying everything about the incoming request:

| Attribute | Contains | Example |
|-----------|----------|---------|
| `request.method` | 'GET' / 'POST' / … | branching form logic |
| `request.GET` | query-string params (dict-like) | `/search/?q=python` → `request.GET.get('q')` |
| `request.POST` | submitted form data | `request.POST.get('email')` |
| `request.FILES` | uploaded files (Topic 4.9) | `request.FILES['photo']` |
| `request.user` | logged-in user or Anonymous (Topic 4.7) | `request.user.username` |
| `request.path` | the URL path | '/students/5/' |
| `request.session` | per-visitor storage | `request.session['cart']` |

```python
def search(request):
    query = request.GET.get('q', '')          # ?q=asha  (default '' if absent)
    return render(request, 'students/search.html', {"query": query})

def feedback(request):
    if request.method == 'POST':              # form was SUBMITTED
        msg = request.POST.get('message')
        return HttpResponse("Thanks! We received: " + msg)
    return render(request, 'students/feedback.html')   # first visit: show form
```
*(GET vs POST semantics are exactly Module 3.1.10 — Django simply hands you each bundle as a dictionary.)*

## 4.2.6 Advanced Routing — Namespaces, Names & reverse

**URL naming + namespaces** free you from hard-coding URLs:
```python
# defined:  app_name='students'; path('<int:roll>/', views.detail, name='detail')

# in templates (Topic 4.3):
<a href="{% url 'students:detail' roll=5 %}">Asha</a>     <!-- → /students/5/ -->

# in Python:
from django.urls import reverse
url = reverse('students:detail', args=[5])                 # '/students/5/'
return redirect('students:index')                          # redirect by name
```
**Why ⭐:** change the path pattern once in urls.py → every link in the entire site updates automatically (DRY!). Namespaces (`students:`) prevent name clashes when two apps both define a `detail` route.

## 4.2.7 END-OF-TOPIC PACK (4.2)

### Quick Revision Notes
- Routing: project urls.py top-down, first match; `include()` strips prefix and delegates to app urls.py; no match = 404.
- `path('pattern/', views.fn, name='x')`; converters `<int:>` `<str:>` `<slug:>` `<uuid:>` `<path:>` pass typed kwargs to the view.
- View = HttpRequest in → HttpResponse out; `HttpResponse("html")` raw, `render(request, 'tpl.html', context)` standard; context dict keys = template variables.
- request.method/.GET/.POST/.FILES/.user/.session.
- Name every URL; use `{% url %}` / `reverse()` / `redirect()` — never hard-code paths; `app_name` gives the `app:name` namespace.

### Important Definitions
URL routing • URL dispatcher • urlpatterns • Converter • View (FBV) • HttpRequest/HttpResponse • Context dictionary • render() • Named URL • Namespace • reverse().

### FAQs
1. *404 though the view exists?* → pattern mismatch (trailing slash! order!), or app urls not include()d.
2. *Why does my view get a TypeError about an unexpected argument?* → converter variable name ≠ view parameter name — they must match.
3. *render vs HttpResponse?* → render builds the HttpResponse from a template + context; HttpResponse is the raw object.
4. *Can two patterns point at one view?* → yes (e.g., '' and 'home/').
5. *Where do I see all routes?* → there's no auto list; read urls.py files (or `python manage.py show_urls` with django-extensions).

### Viva Questions
1. Which file routes URLs at project level? 2. Function that delegates to app urls? *(include)* 3. What does `<int:roll>` do — two things? 4. Default converter when none written? *(str)* 5. Which converter allows slashes? 6. First parameter of every view? 7. Two differences GET vs POST dictionaries. 8. Template tag that builds a URL from its name? 9. What does first-match-wins imply about ordering? 10. Purpose of app_name?

### Interview Questions
1. Trace `/students/5/` end-to-end through both urls.py files into the view.
2. Why per-app urls.py + include() is best practice (reusability argument).
3. slug converter — what is a slug and why SEO likes it?
4. Hard-coded URLs vs named URLs — the maintenance story.
5. How does a single view serve both "show form" and "process form"? *(method branching)*
6. request.GET vs request.POST vs request.FILES.
7. What generates a 404 in routing, and how is it different from a view raising Http404?
8. redirect() vs render() — when each (Post/Redirect/Get pattern preview).

### MCQs
1. First-match search order is: a) bottom-up b) **top-down** ✓ c) longest-first d) random
2. `<slug:t>` matches: a) "a b c" b) **"python-basics-101"** ✓ c) "a/b" d) "5.5"
3. include() does: a) imports views b) **delegates remaining path to another urls.py** ✓ c) renders d) redirects
4. render()'s third argument: a) list b) **context dict** ✓ c) tuple d) string
5. Query string `?q=x` lives in: a) request.POST b) **request.GET** ✓ c) request.path d) request.q
6. reverse('students:detail', args=[5]) returns: a) the view b) **'/students/5/'** ✓ c) HttpResponse d) 5

### Short / Long Answer Questions
**Short:** 1. Syntax of path() with all three arguments. 2. Table of the five converters. 3. What does include() strip? 4. Write a view echoing ?name= from the query string. 5. Two benefits of URL naming.
**Long:** 1. URL routing architecture: two-level diagram, flow rules, best practices. 2. Views deep-dive: lifecycle, HttpResponse vs render with code, the request object's attributes. 3. Build routes+views for a mini blog (list, detail by slug, search by query string) — full code both urls.py files + views.py. 4. Named URLs, namespaces and reverse(): the DRY argument with before/after refactor example.

### Practical Lab Questions
1. Wire `students` app: index, detail(int), about — test all three plus a deliberate 404.
2. Add a search view reading `?q=`; display the query back.
3. Feedback view: GET shows a (hand-written) HTML form, POST thanks the user with their message.
4. Rename a URL pattern and prove `{% url %}`-based links survive while a hard-coded one breaks.

### Debugging Exercises
```
1) path('students/<int:roll>', …) but visiting /students/5/ → 404   → missing trailing slash in pattern
2) detail(request, id) with <int:roll>                              → names must match: roll
3) Page not found at /students/ but app urls exist                  → forgot include() in project urls.py
4) NoReverseMatch: 'detail'                                          → namespace needed: 'students:detail' / name typo
5) Both '' and '<str:page>/' defined, about/ shows wrong view        → reorder: specific before generic
```

### Assignment Questions
1. Diagram poster: full routing flow for three different URLs of your project.
2. Compare Django routing with Flask's @app.route decorator (1 page).
3. Design the complete URL scheme (10+ routes, named, namespaced) for a college website.

### Coding Exercises
1. Calculator routes: /add/3/4/ etc. using two int converters per operation.
2. /profile/<slug:username>/ rendering a card template.
3. A view that redirects /old-home/ permanently to the named index route.
4. Mini router quiz app: /quiz/<int:qno>/ cycling through a list of questions held in the view.

### Scenario-Based Questions
1. *Marketing wants /summer-fest/ moved to /events/summer-fest/ without breaking links site-wide.* → named URLs + redirect for the old path.
2. *Two apps both have a route named 'list'; templates link wrongly.* → namespaces fix.
3. *A user bookmarks page 3 of search results.* → why GET (query string) is the right method here.

### Mini Project Ideas
URL-shortener skeleton (slug → redirect) • multi-page department site fully routed • "API-ish" endpoints returning HttpResponse JSON strings for student data.

### Summary
Routing is Django's dispatch layer: the project's urls.py scans patterns top-down and `include()`s each app's own urls.py, where `path()` patterns — with typed converters like `<int:roll>` and `<slug:title>` — hand captured values to views. A view turns an HttpRequest (method, GET/POST dicts, user, files) into an HttpResponse, almost always via `render(request, template, context)`. Name every route, wrap apps in namespaces, and build links with `{% url %}`/`reverse()` so the whole site survives any path refactor. Next: the templates those views render.

---
---
# §3. TOPIC 4.3 — DJANGO TEMPLATES

## 4.3.1 Introduction to Templates

> **Definition:** A **template** is an HTML file containing **placeholders and lightweight logic** that Django's **template engine** fills with data (the context) at request time, producing the final HTML sent to the browser.

**Why templates exist:** views could build HTML strings by hand (`HttpResponse("<h1>"+name+"</h1>")`) — unreadable, unsafe, undesignable. Templates restore the **separation of concerns**: Python logic stays in views, HTML stays in `.html` files your Module-3 skills already master.

**Analogy:** a template is a **certificate blank** 📜 — "This certifies that ______ scored ______" printed once; the engine is the clerk filling each student's name and marks per copy.

### How Django Renders Pages (template processing flow)
```
view: render(request, 'students/index.html', {"names": [...], "count": 3})
            │
            ▼
 ① LOAD   engine finds the file (searches each app's templates/ folder + DIRS)
 ② PARSE  splits text / {{ variables }} / {% tags %}
 ③ FILL   replaces variables from CONTEXT, executes tags (loops, ifs)
 ④ ESCAPE auto-escapes HTML in variables (XSS protection! <b> → &lt;b&gt;)
 ⑤ RETURN final HTML string → wrapped in HttpResponse
```
### Where templates live ⭐ (the double-folder convention)
```
students/
└── templates/
    └── students/            ← yes, app name AGAIN (prevents cross-app name clashes)
        ├── index.html
        └── detail.html
# referenced as: render(request, 'students/index.html', ...)
```

## 4.3.2 Template Syntax — Variables

```html
<!-- context = {"name": "Asha", "marks": 88, "student": obj, "subjects": [...]} -->
<h1>Hello {{ name }}!</h1>                 <!-- variable: double braces -->
<p>Marks: {{ marks }}</p>
<p>Branch: {{ student.branch }}</p>        <!-- dot = attribute / dict key / method -->
<p>First subject: {{ subjects.0 }}</p>     <!-- dot even for list index! -->
```
**Output:** `Hello Asha! Marks: 88 …` — a missing variable renders as **empty string** (no crash). The dot tries, in order: dictionary key → attribute → list index → method call (no parentheses!).

## 4.3.3 Template Tags ⭐ — `{% logic %}`

### if / elif / else
```html
{% if marks >= 75 %}
    <span class="badge bg-success">Distinction</span>
{% elif marks >= 40 %}
    <span class="badge bg-primary">Pass</span>
{% else %}
    <span class="badge bg-danger">Fail</span>
{% endif %}              <!-- closing tag is MANDATORY -->
```
Operators: `== != < > <= >= and or not in` — same spirit as Python (Module 1.3), but only *light* logic belongs here; heavy decisions stay in views.

### for
```html
<ul>
{% for s in students %}
    <li>{{ forloop.counter }}. {{ s.name }} — {{ s.marks }}</li>
{% empty %}
    <li>No students found.</li>            <!-- runs if list is empty ⭐ -->
{% endfor %}
</ul>
```
`forloop.counter` (1-based), `.counter0`, `.first`, `.last` — free loop metadata.

### include — reusable fragments
```html
{% include 'students/_navbar.html' %}      <!-- paste a partial; _ prefix = convention -->
```

### block — placeholders for inheritance (next section)

## 4.3.4 Filters — `{{ value|filter }}`

> **Definition:** **Filters** transform a variable's display, applied with the pipe `|`, chainable, some taking arguments after `:`.

| Filter | Effect | Example → Output |
|--------|--------|------------------|
| `upper` / `lower` | case change | `{{ name|upper }}` → ASHA |
| `title` | Title Case | `{{ "web dev"|title }}` → Web Dev |
| `length` | item/char count | `{{ students|length }}` → 3 |
| `date:"d M Y"` | format dates | `{{ joined|date:"d M Y" }}` → 12 Jun 2026 |
| `default:"—"` | fallback when empty | `{{ phone|default:"N/A" }}` |
| `truncatewords:20` | shorten text | blog previews |
| `floatformat:2` | decimals | `{{ 3.14159|floatformat:2 }}` → 3.14 |
| `join:", "` | list → string | `{{ tags|join:", " }}` |

```html
<p>{{ post.body|truncatewords:25 }}</p>
<small>Published {{ post.created|date:"D, d M Y" }} • {{ post.title|title }}</small>
```

### Custom Filters (when built-ins aren't enough)
```
students/
└── templatetags/            ← exact name, plus empty __init__.py
    ├── __init__.py
    └── student_extras.py
```
```python
# student_extras.py
from django import template
register = template.Library()

@register.filter                      # Module 1 decorators in action!
def grade(marks):
    if marks >= 75: return "A"
    if marks >= 60: return "B"
    return "C" if marks >= 40 else "F"
```
```html
{% load student_extras %}             <!-- top of the template -->
<td>{{ s.marks|grade }}</td>          <!-- 88 → A -->
```

## 4.3.5 Template Inheritance ⭐⭐ (the DRY superpower)

> **Definition:** **Template inheritance** lets a **base template** define the page skeleton with named `{% block %}` holes, while **child templates** `{% extends %}` it and fill only those holes — one navbar/footer maintained in one file.

**base.html (`templates/base.html` — project-level shared layout):**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}CampusHub{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
          rel="stylesheet">
</head>
<body>
    {% include '_navbar.html' %}                 <!-- shared Bootstrap navbar -->

    <main class="container py-4">
        {% block content %}{% endblock %}        <!-- ⭐ the main hole -->
    </main>

    <footer class="bg-dark text-white text-center py-3">© 2026 CampusHub</footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```
**Child (`students/index.html`):**
```html
{% extends 'base.html' %}                 <!-- MUST be the first line -->

{% block title %}Students | CampusHub{% endblock %}

{% block content %}
<h1 class="mb-4">All Students ({{ count }})</h1>
<div class="row g-3">
    {% for s in names %}
    <div class="col-md-4"><div class="card p-3">{{ s }}</div></div>
    {% endfor %}
</div>
{% endblock %}
```
```
        base.html  (skeleton: head, navbar, footer)
        ┌─────────[block title]──────────┐
        ├─────────[block content]────────┤   child fills ONLY the holes;
        └────────────────────────────────┘   everything else inherited
   index.html  detail.html  about.html  … all extend the same base
```
Change the navbar once → **every page updates.** This is Module 3's "shared shell" problem solved properly. *(Project-level base: create `templates/` at project root and add it to `TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']` in settings.)*

## 4.3.6 Static Files (CSS / JS / Images) ⭐

> **Definition:** **Static files** are assets that don't change per request — your stylesheets, scripts, logos — served as-is alongside dynamic templates.

**Configuration (settings.py):**
```python
STATIC_URL = 'static/'                       # URL prefix:  /static/css/style.css
STATICFILES_DIRS = [BASE_DIR / 'static']     # extra project-level static folder
# (each app's own  app/static/app/  folder is found automatically)
```
**Folder layout:**
```
static/
├── css/style.css      ├── js/main.js      └── images/logo.png
```
**Using them in templates:**
```html
{% load static %}                                          <!-- first line(s) -->
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script src="{% static 'js/main.js' %}"></script>
<img src="{% static 'images/logo.png' %}" alt="CampusHub logo">
```
> ⚠️ **Warning:** the top-3 static bugs — forgot `{% load static %}` • hard-coded `/static/...` instead of the tag • `STATICFILES_DIRS` missing. If CSS won't load, check the Network tab (Module 3 DevTools!) for 404s. In production, `collectstatic` gathers everything into one folder for the web server — dev server handles it automatically while DEBUG=True.

### Frontend Integration — Module 3 meets Module 4
Bootstrap via CDN in base.html (above) **or** locally: download to `static/css|js/` and link with `{% static %}`. Your custom `style.css` loads **after** Bootstrap — the exact override pattern from Module 3.3.7. Every Module-3 project can now be ported: its repeated navbar/footer become base.html + includes, its pages become children, its assets move into static/.

## 4.3.7 END-OF-TOPIC PACK (4.3)

### Quick Revision Notes
- Template = HTML + `{{ variables }}` + `{% tags %}` + `|filters`; engine loads→parses→fills→auto-escapes→returns.
- Files at `app/templates/app/x.html` (double-folder!); project-level via DIRS.
- Tags: if/elif/else, for + forloop.counter + {% empty %}, include partials, block holes.
- Filters: upper lower title length date default truncatewords floatformat join; custom via templatetags/ + @register.filter + {% load %}.
- Inheritance: base.html defines blocks; children `{% extends %}` first line and override blocks — one layout, all pages.
- Static: STATIC_URL + STATICFILES_DIRS, `{% load static %}`, `{% static 'css/style.css' %}`.

### Important Definitions
Template • Template engine • Context • Variable interpolation • Template tag • Filter • Partial/include • Template inheritance • Block • Static files • Auto-escaping.

### FAQs
1. *TemplateDoesNotExist?* → wrong path (remember app/templates/app/), app unregistered, or DIRS missing for project-level files.
2. *Variable prints nothing?* → key missing from context (typo) — Django stays silent by design.
3. *Why can't I call methods with arguments in templates?* → templates are intentionally logic-light; compute in the view or a custom filter.
4. *CSS not applying?* → see the static-files warning trio above.
5. *Can a child extend a child?* → yes, multi-level inheritance works.

### Viva Questions
1. Variable vs tag syntax? 2. What does auto-escaping prevent? *(XSS)* 3. Tag that must be a child's first line? 4. What does {% empty %} do? 5. forloop.counter starts at? 6. Filter to format dates? 7. Folder name for custom filters? 8. Two settings for static files? 9. Why the double app-name folder? 10. include vs extends in one line.

### Interview Questions
1. Walk through the render pipeline from view to final HTML.
2. Template inheritance vs include — when each? (skeleton vs fragment)
3. How does Django's auto-escaping protect against XSS; when would you use the `safe` filter (and its risk)?
4. Design the base/child structure for a 10-page site.
5. Custom filter end-to-end: files, decorator, load, use.
6. Static files in development vs production (collectstatic concept).
7. Why keep logic out of templates — the MVT discipline.

### MCQs
1. Print a variable: a) {% name %} b) **{{ name }}** ✓ c) ${name} d) [[name]]
2. Loop tag: a) {{ for }} b) **{% for %}…{% endfor %}** ✓ c) <for> d) @for
3. {{ "abc"|length }} → a) abc b) **3** ✓ c) error d) "3 chars"
4. Child template's first line: a) {% block %} b) **{% extends 'base.html' %}** ✓ c) {% include %} d) {% load %}
5. Static tag needs: a) nothing b) **{% load static %}** ✓ c) import static d) settings only
6. Missing context variable renders: a) error page b) **empty string** ✓ c) None d) 0

### Short / Long Answer Questions
**Short:** 1. if/elif/else block for grades. 2. Loop with counter + empty clause. 3. Three filters with outputs. 4. The two static settings. 5. What does {% include %} take?
**Long:** 1. Template engine architecture & processing flow with diagram. 2. Inheritance masterclass: base.html + two children, full code, the DRY argument. 3. Filters: ten built-ins + complete custom filter implementation. 4. Integrate a Module-3 Bootstrap project into Django templates+static (migration steps).

### Practical Lab Questions
1. Build base.html (Bootstrap navbar/footer) + convert index/detail/about to children.
2. Students table: loop, zebra via forloop, grade via custom filter, {% empty %} state.
3. Wire style.css through static files; prove the 404→fix cycle in DevTools.
4. Create _card.html partial; include it thrice with different contexts (`{% include '_card.html' with title=x %}`).

### Debugging Exercises
```
1) TemplateDoesNotExist students/index.html      → file at students/templates/index.html; add inner students/ folder
2) {{ name }} blank though passed                → context key is 'Name' — case/typo
3) Invalid block tag 'endif'                     → opened {% if %} never closed / nested wrongly
4) 'static' is not a registered tag              → missing {% load static %}
5) {% extends 'base.html' %} mid-file            → must be FIRST template line
6) Navbar shows on index but not detail          → detail.html doesn't extend base
```

### Assignment Questions
1. Refactor Module-3 Project 6 (Nimbus, 4 pages) into one base + four children; report lines saved.
2. One page: "How auto-escaping stops XSS" with an attack example neutralized.
3. Catalogue 15 built-in filters with examples (docs exploration).

### Coding Exercises
1. Custom filter `initials` ("Asha Verma" → "A.V.").
2. Marks dashboard: loop computing badge colors with if-chains.
3. Two-level inheritance: base → dashboard_base (adds sidebar block) → reports page.
4. Breadcrumb partial driven by a context list.

### Scenario-Based Questions
1. *Designer must change the footer on 40 pages by Friday.* → inheritance fixes it in one file — explain the refactor.
2. *A user's comment containing `<script>` shows as text, client asks why.* → auto-escaping; discuss safe-filter trade-offs.
3. *Site sections need different layouts (public vs admin).* → two bases or nested bases — justify a design.

### Mini Project Ideas
Template-ize all six Module-3 projects under one Django site • "components library" page of reusable partials • themed report generator (one data set, three switchable bases).

### Summary
Templates return presentation to clean HTML files: the engine fills `{{ variables }}` from the view's context, executes light `{% if %}`/`{% for %}` logic, transforms output through filters (built-in or custom), and auto-escapes everything against XSS. Inheritance turns repeated layouts into one base.html with block holes that children override, while the static-files system (`{% load static %}` + STATIC settings) serves your CSS/JS/images — letting every Bootstrap page from Module 3 plug straight into Django. Now the data those templates display gets real: models and the ORM.

---
---
# §4. TOPIC 4.4 — DJANGO MODELS & ORM

## 4.4.1 Database Fundamentals & the ORM Concept

**Why databases matter** — Module 2's lesson stands: real apps need permanent, queryable, multi-user, constraint-protected storage. Django ships configured for **SQLite** (`db.sqlite3` — Topic 2.4's single-file engine, perfect for development) and switches to MySQL/PostgreSQL by editing one settings block.

### The ORM ⭐⭐

> **Definition:** An **ORM (Object-Relational Mapper)** is a layer that **maps Python classes ↔ database tables**, class attributes ↔ columns, and objects ↔ rows — so you query and modify the database in pure Python while the ORM generates the SQL.

```
   PYTHON WORLD                          DATABASE WORLD (Module 2!)
   class Student(models.Model)   ⇄      CREATE TABLE students_student (…)
   name = CharField(...)         ⇄      name VARCHAR(50)
   Student.objects.filter(...)   ⇄      SELECT … WHERE …
   s.save()                      ⇄      INSERT / UPDATE …
   s.delete()                    ⇄      DELETE FROM …
```
**Why ORM > raw SQL strings (interview gold):** ① pure Python — one language end-to-end ② **automatic parameterization** = SQL-injection safe by default (Module 2.3.6's war, won for free) ③ database-portable (SQLite→MySQL with no query rewrites) ④ models are the single source of truth (DRY) — forms, admin, migrations all derive from them. *Trade-off:* very exotic queries may still need `raw()` SQL — knowing Module 2 lets you read what the ORM writes (`print(qs.query)` shows the SQL!).

## 4.4.2 Models & models.py

> **Definition:** A **model** is a Python class inheriting `django.db.models.Model`; each model = one table, each class attribute (a Field instance) = one column, each object = one row.

```python
# students/models.py
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):                       # human-readable label everywhere
        return self.name

class Student(models.Model):
    roll       = models.IntegerField(unique=True)
    name       = models.CharField(max_length=50)
    email      = models.EmailField(unique=True)
    marks      = models.IntegerField(default=0)
    is_active  = models.BooleanField(default=True)
    admitted   = models.DateField(auto_now_add=True)     # set once at creation
    bio        = models.TextField(blank=True)            # optional long text
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                                   related_name='students')

    class Meta:
        ordering = ['-marks']                # default sort: toppers first

    def __str__(self):
        return f"{self.roll} – {self.name}"
```
**Model lifecycle:** define class → makemigrations (write the change-script) → migrate (apply to DB) → use via ORM → evolve fields → repeat. **Best practices:** always define `__str__` • singular class names (Student, not Students — Django pluralizes the table: `students_student`) • defaults/constraints in the model, not scattered in views • `Meta.ordering` for natural default order.

## 4.4.3 Field Types ⭐ (the vocabulary table)

| Field | Stores / SQL twin (Module 2) | Key arguments & notes |
|-------|------------------------------|------------------------|
| `CharField` | short text / VARCHAR(n) | **max_length required** |
| `TextField` | long text / TEXT | no max_length needed |
| `IntegerField` | whole numbers / INT | default=, validators |
| `FloatField` | approximate decimals / FLOAT | money? use DecimalField! |
| `DecimalField` | exact decimals / DECIMAL(p,s) | max_digits, decimal_places |
| `BooleanField` | True/False / BOOLEAN | default=True/False |
| `DateField` | date / DATE | `auto_now_add=True` (set on create), `auto_now=True` (update every save) |
| `DateTimeField` | date+time / DATETIME | same auto options |
| `EmailField` | CharField + email validation | unique=True common |
| `FileField` | uploaded file **path** (file on disk!) | upload_to='docs/' (Topic 4.9) |
| `ImageField` | FileField + image validation | needs **Pillow** installed |
| `ForeignKey` | many-to-one / FK column | on_delete **required**, related_name |
| `OneToOneField` | one-to-one / FK+UNIQUE | profiles ⭐ |
| `ManyToManyField` | M:N / junction table auto-created! | Module 2's enrollments table, free |

**Common options for any field:** `null=True` (DB may store NULL) vs `blank=True` (form may be empty — validation level!) • `default=` • `unique=True` • `choices=[('A','Active'),('I','Inactive')]` • `db_index=True`.
> 📝 **Exam Tip:** **null vs blank** — null is a *database* rule, blank is a *form/validation* rule. Text fields: prefer `blank=True` alone (store '' not NULL); dates/numbers: usually both.

## 4.4.4 Model Relationships ⭐⭐

```
 ONE-TO-ONE              ONE-TO-MANY (FK)            MANY-TO-MANY
 User ─── Profile        Department ──< Student      Student >──< Course
 passport pattern        Module 2's dept_id!         via auto junction table
 OneToOneField           ForeignKey                  ManyToManyField
```
```python
class Profile(models.Model):                                  # 1:1
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

class Student(models.Model):                                  # N:1 side holds the FK
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                                   related_name='students')

class Course(models.Model):                                   # M:N
    title    = models.CharField(max_length=80)
    students = models.ManyToManyField(Student, related_name='courses')
```
**on_delete options (viva favorite):** `CASCADE` (delete children too) • `PROTECT` (refuse deletion) • `SET_NULL` (needs null=True) • `SET_DEFAULT`. Exactly Module 2.2.1's referential-integrity policies, now in Python.
**Traversing relationships:**
```python
s.department.name                 # forward: child → parent
d.students.all()                  # reverse via related_name: parent → children
c.students.add(s); s.courses.all()  # M2M both directions
```

## 4.4.5 Migrations ⭐

> **Definition:** **Migrations** are version-controlled Python scripts describing database schema changes — Django's way of evolving tables safely and reproducibly (DDL, automated).

```bash
python manage.py makemigrations    # ① detect model changes → write 000X_*.py script
python manage.py migrate           # ② execute pending scripts → actual CREATE/ALTER
python manage.py sqlmigrate students 0001   # peek at the generated SQL (Module 2!)
python manage.py showmigrations    # checklist: [X] applied  [ ] pending
```
```
 models.py edit ──▶ makemigrations ──▶ migrations/0002_….py ──▶ migrate ──▶ DB altered
   (intent)            (recipe written)        (recipe file)      (recipe cooked)
```
> 💡 **Memory Trick:** **makemigrations = writing the recipe, migrate = cooking it.** Commit migration files to Git — teammates `migrate` to replay your schema. First-ever `migrate` also creates Django's built-in tables (auth, sessions, admin).

## 4.4.6 QuerySets, Managers & CRUD

> **Definitions:** A **manager** (`Model.objects` by default) is the gateway to database operations. A **QuerySet** is a **lazy**, chainable collection of database rows — no SQL runs until you actually consume it (loop, list(), len(), slice).

### CREATE
```python
# Way 1: instantiate + save()
d = Department(name="CSE"); d.save()
# Way 2: create() — build + save in one call
s = Student.objects.create(roll=1, name="Asha", email="a@x.com",
                           marks=88, department=d)
```
### READ
```python
Student.objects.all()                       # every row (QuerySet)
Student.objects.filter(marks__gte=75)       # WHERE marks >= 75 (QuerySet, may be empty)
Student.objects.get(roll=1)                 # exactly ONE object — raises
                                            # DoesNotExist / MultipleObjectsReturned!
Student.objects.exclude(is_active=False)    # NOT condition
Student.objects.order_by('-marks', 'name')  # ORDER BY marks DESC, name ASC
Student.objects.filter(marks__gte=40).order_by('-marks')[:3]   # chain + slice = LIMIT 3
Student.objects.count(); Student.objects.exists(); Student.objects.first()
```
### UPDATE
```python
s = Student.objects.get(roll=1); s.marks = 95; s.save()        # single object
Student.objects.filter(department=d).update(is_active=True)    # bulk, one SQL UPDATE
```
### DELETE
```python
Student.objects.get(roll=7).delete()                  # one row
Student.objects.filter(marks__lt=10).delete()         # bulk (respects on_delete!)
```
> ⚠️ **Warning:** `get()` for must-exist single objects only — wrap in try/except or use `get_object_or_404`. `filter()` never raises; it returns an empty QuerySet. And bulk `update()` skips `save()` methods/auto_now — know the trade-off.

## 4.4.7 Field Lookups ⭐ — `field__lookup=value` (double underscore!)

| Lookup | SQL meaning | Example |
|--------|-------------|---------|
| `exact` (default) | = | `filter(name='Asha')` |
| `iexact` | = case-insensitive | `name__iexact='asha'` |
| `contains` / `icontains` | LIKE '%x%' | `name__icontains='sh'` |
| `startswith` / `endswith` | LIKE 'x%' / '%x' | `email__endswith='.edu'` |
| `gt gte lt lte` | > >= < <= | `marks__gte=75` |
| `in` | IN (...) | `roll__in=[1,3,5]` |
| `range` | BETWEEN | `marks__range=(60, 90)` |
| `isnull` | IS NULL | `bio__isnull=True` |
| `year/month/day` | date parts | `admitted__year=2026` |
| **relationship spanning** | JOIN! | `filter(department__name='CSE')` ⭐ |

That last row is the ORM's magic: `Student.objects.filter(department__name='CSE')` silently writes Module 2.2's INNER JOIN for you.

## 4.4.8 Aggregation — aggregate() & annotate()

```python
from django.db.models import Avg, Max, Min, Count, Sum

# aggregate() → ONE summary dict for the whole table (Module 2's plain aggregates)
Student.objects.aggregate(avg=Avg('marks'), top=Max('marks'), n=Count('id'))
# {'avg': 73.0, 'top': 92, 'n': 5}

# annotate() → adds a computed column PER ROW/GROUP (Module 2's GROUP BY!)
Department.objects.annotate(strength=Count('students'),
                            avg_marks=Avg('students__marks'))
for d in _:
    print(d.name, d.strength, d.avg_marks)     # CSE 3 85.0 …

# HAVING equivalent: filter AFTER annotate
Department.objects.annotate(n=Count('students')).filter(n__gte=2)
```
> 💡 **Memory Trick:** **aggregate = one answer** (returns a dict, ends the chain) • **annotate = answer per object** (returns a QuerySet, keeps chaining). aggregate≈plain `SELECT AVG(...)`; annotate≈`GROUP BY`; annotate+filter≈`HAVING`.

## 4.4.9 Q Objects & F Expressions

```python
from django.db.models import Q, F

# Q = build OR / NOT logic (filter args alone can only AND)
Student.objects.filter(Q(marks__gte=90) | Q(department__name='CSE'))
Student.objects.filter(~Q(is_active=True))                 # NOT
Student.objects.filter(Q(name__startswith='A') & Q(marks__gte=75))

# F = reference a FIELD inside the query → math runs IN THE DATABASE
Student.objects.update(marks=F('marks') + 5)               # everyone +5, one SQL, race-safe
Student.objects.filter(marks__gt=F('attendance'))          # compare two columns
```
**Why F matters:** `s.marks += 5; s.save()` reads-then-writes (two trips, race conditions); `F('marks')+5` is a single atomic UPDATE — the bank-balance lesson of Module 2.3.7 applied.

## 4.4.10 Query Optimization — the N+1 killer ⭐

```python
# ❌ N+1 problem: 1 query for students + 1 PER student for department
for s in Student.objects.all():
    print(s.department.name)            # 101 queries for 100 students!

# ✅ select_related — SQL JOIN, ONE query (for FK / OneToOne)
for s in Student.objects.select_related('department'):
    print(s.department.name)            # 1 query

# ✅ prefetch_related — 2 queries + Python stitch (for M2M / reverse FK)
for c in Course.objects.prefetch_related('students'):
    print(c.title, c.students.count())
```
> 📝 **Interview line:** *select_related = JOIN for single-valued relations; prefetch_related = separate query for multi-valued relations.* Diagnose with `django-debug-toolbar` or `connection.queries`.

## 4.4.11 Wiring Models into Views & Templates (the thread continues)
```python
# students/views.py — index/detail now DATABASE-driven
from django.shortcuts import render, get_object_or_404
from .models import Student

def index(request):
    students = Student.objects.select_related('department').all()
    return render(request, 'students/index.html', {'students': students})

def detail(request, roll):
    s = get_object_or_404(Student, roll=roll)        # 404 if absent — clean!
    return render(request, 'students/detail.html', {'s': s})
```
```html
{% for s in students %}
  <tr><td>{{ s.roll }}</td><td>{{ s.name }}</td>
      <td>{{ s.department.name }}</td><td>{{ s.marks }}</td></tr>
{% empty %}<tr><td colspan="4">No students yet.</td></tr>{% endfor %}
```
**The MVT loop is now complete and real:** URL → view → **ORM/model → SQLite** → template → browser.

## 4.4.12 END-OF-TOPIC PACK (4.4)

### Quick Revision Notes
- ORM: class⇄table, attribute⇄column, object⇄row; injection-safe, portable, DRY; see SQL with `qs.query`.
- Fields: CharField(max_length!), TextField, Integer/Float/Decimal, Boolean, Date/DateTime(auto_now_add vs auto_now), Email, File/Image(Pillow), FK/O2O/M2M; null(DB) vs blank(form); on_delete CASCADE/PROTECT/SET_NULL.
- Migrations: makemigrations (write recipe) → migrate (cook); sqlmigrate to peek.
- CRUD: create()/save() • all/filter/get(raises!)/exclude/order_by/[:n] • update() bulk vs save() • delete().
- Lookups `field__gte`, `__icontains`, `__in`, spanning `department__name` (auto-JOIN).
- aggregate()=one dict; annotate()=per-row (GROUP BY); +filter = HAVING. Q = OR/NOT; F = column math in DB. select_related(FK JOIN) / prefetch_related(M2M) kill N+1.

### Important Definitions
ORM • Model • Field • Migration • QuerySet (lazy!) • Manager • Field lookup • Aggregation vs annotation • Q object • F expression • N+1 problem.

### FAQs
1. *"no such table"?* → migrations not run (or app unregistered → makemigrations saw nothing).
2. *Changed a field, DB unchanged?* → ran neither/only one of the two migration commands.
3. *get() crashed?* → zero or multiple matches; use filter().first() or get_object_or_404.
4. *Where IS the database?* → db.sqlite3 in the project root (open it with Module 2.4 skills!).
5. *ManyToMany: where's the table?* → auto-created junction table (appname_course_students).

### Viva Questions
1. Expand ORM; one advantage. 2. Which field needs max_length? 3. null vs blank. 4. auto_now vs auto_now_add. 5. Required argument of ForeignKey besides the model? *(on_delete)* 6. Two migration commands in order. 7. What does objects refer to? 8. filter vs get return types. 9. Lookup for case-insensitive contains? 10. aggregate vs annotate one-liner. 11. Why F('marks')+1 beats marks+=1? 12. Which optimizer uses a JOIN?

### Interview Questions
1. How does the ORM prevent SQL injection? (connect to Module 2.3.6)
2. Model the college domain (Department/Student/Course) with all three relationship types — code it.
3. Explain QuerySet laziness and why chaining is free.
4. Migration workflow in a team (files in Git, conflicts, fake migrations concept).
5. N+1 problem: demonstrate, then fix with both optimizers and explain when each applies.
6. Translate five Module-2 SQL queries into ORM (JOIN, GROUP BY+HAVING, LIKE, BETWEEN, top-3).
7. on_delete options and a business case for each.
8. update() vs save() — signals/auto_now trade-offs.

### MCQs
1. One model maps to one: a) row b) **table** ✓ c) column d) database
2. Mandatory on CharField: a) default b) **max_length** ✓ c) unique d) null
3. Recipe-writing command: a) migrate b) **makemigrations** ✓ c) syncdb d) sqlmigrate
4. get() with no match raises: a) None b) **DoesNotExist** ✓ c) Http404 d) Empty
5. `marks__gte=75` means: a) >75 b) **>=75** ✓ c) =75 d) <=75
6. GROUP-BY-like tool: a) aggregate b) **annotate** ✓ c) F d) Meta
7. OR conditions need: a) F b) **Q** ✓ c) | alone d) Meta
8. FK N+1 fix: a) prefetch_related b) **select_related** ✓ c) only() d) raw()

### Short / Long Answer Questions
**Short:** 1. Write a Book model (5 fields, one FK). 2. The two migration commands + purpose. 3. Three field lookups with SQL twins. 4. Q-query: marks>90 OR dept CSE. 5. What is a lazy QuerySet?
**Long:** 1. ORM concept end-to-end with the mapping diagram and pros/cons vs raw SQL. 2. Field-types catalogue (10+) with arguments, null/blank, choices. 3. All three relationships: models, on_delete, traversal both directions, junction-table explanation. 4. QuerySet API tour: CRUD, lookups, aggregation, Q/F, optimization — with the SQL each generates.

### Practical Lab Questions
1. Build Department+Student models, migrate, inspect with `sqlmigrate` and the SQLite CLI (Module 2.4!).
2. Shell session (`python manage.py shell`): create 2 departments + 6 students; run 10 assorted queries (save the transcript).
3. Convert index/detail views to ORM-driven; add a topper page (`order_by('-marks')[:3]`).
4. Demonstrate N+1 with `connection.queries`, then fix and re-measure.

### Debugging Exercises
```
1) OperationalError: no such table students_student   → run migrate (and makemigrations first)
2) TypeError: __init__() missing 'on_delete'          → FK requires on_delete=models.CASCADE/…
3) MultipleObjectsReturned at get(name='Asha')        → name not unique; filter().first() or get by pk
4) Student.objects.filter(marks > 75)                 → Python comparison! use marks__gt=75
5) s.department prints "Department object (1)"        → define __str__ on Department
6) Changed max_length, site fine, teammate crashes    → you never committed/ran the migration
```

### Assignment Questions
1. Translate the Module-2 "Top 50 SQL queries" items 21–35 into ORM calls.
2. Schema-design doc for a hospital app (4 models, all relationship types, on_delete policies justified).
3. One page: "How migrations make schema changes safe in teams."

### Coding Exercises
1. Library models (Book, Member, Issue FK pair) + 8 shell queries incl. annotate per member.
2. Management report function: per-department dict of count/avg/top using annotate.
3. Bulk +5% marks via F; then per-student grade recompute comparing F vs Python loop timings.
4. Search view: `Q(name__icontains=q) | Q(email__icontains=q)`.

### Scenario-Based Questions
1. *Product manager asks "departments with average marks above 70, largest first."* → annotate+filter+order_by; also write the SQL it replaces.
2. *Two requests increment the same counter simultaneously and one update is lost.* → F expression atomicity.
3. *Page renders slowly; logs show 400 queries.* → diagnose N+1; choose the right optimizer per relation.

### Mini Project Ideas
ORM-powered gradebook with annotate dashboards • quiz bank (Question M2M Tags) with random sampler • migration-history showcase: evolve a model 5 times and document each migration file.

### Summary
Models turn Module-2 tables into Python classes: fields map to columns (with null/blank, choices, on_delete policies), relationships cover 1:1, 1:N and M:N (junction table free of charge), and migrations version every schema change (makemigrations → migrate). The ORM's lazy QuerySets deliver CRUD (create/filter/get/update/delete), double-underscore lookups that span relationships into automatic JOINs, aggregate/annotate for summaries and GROUP BY, Q for OR-logic, F for in-database math, and select_related/prefetch_related to slay the N+1 problem — all injection-safe. Your views now serve real data; next we let users send data back: forms.

---
---
# §5. TOPIC 4.5 — DJANGO FORMS & FORM VALIDATION

## 4.5.1 Introduction — Why Django Forms Exist

Module 3 built HTML forms; Module 4.2 read `request.POST` by hand. Doing that for real apps means hand-writing, for **every** form: the HTML, required/type/length checks, re-display with errors *and* the user's previous input, type conversion, security. **Django Forms automate the entire pipeline.**

> **Definition:** A **Django Form** is a Python class declaring fields + validation rules, from which Django can **render HTML**, **validate submissions**, **report errors**, and hand you **clean, typed Python data**.

### The Form Processing Workflow ⭐ (the sacred if/else)
```
 GET  request ──▶ view creates EMPTY form ──▶ template renders it
 POST request ──▶ form = Form(request.POST)
                   │ form.is_valid()?
        ┌──────────┴──────────┐
        ▼ True                ▼ False
  cleaned_data ready    form re-rendered WITH errors
  → save / act          AND previous values kept (free!)
  → redirect (PRG)
```

## 4.5.2 forms.py — Creating a Form
```python
# students/forms.py  (you create this file)
from django import forms

class ContactForm(forms.Form):
    name    = forms.CharField(max_length=50, label="Your Name")
    email   = forms.EmailField()
    age     = forms.IntegerField(min_value=16, max_value=60, required=False)
    message = forms.CharField(widget=forms.Textarea)
```
```python
# views.py — the canonical pattern (memorize!)
from django.shortcuts import render, redirect
from .forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)          # BOUND form (has data)
        if form.is_valid():                       # runs ALL validation
            data = form.cleaned_data              # typed dict: age is an int!
            print(data['name'], data['email'])
            return redirect('students:thanks')    # Post→Redirect→Get pattern ⭐
    else:
        form = ContactForm()                      # UNBOUND empty form
    return render(request, 'students/contact.html', {'form': form})
```
```html
<form method="post">
    {% csrf_token %}                 <!-- MANDATORY (see 4.5.6) -->
    {{ form.as_p }}                  <!-- each field wrapped in <p>; also as_table/as_ul -->
    <button class="btn btn-primary">Send</button>
</form>
```
**What you get free:** HTML generation, type conversion (`cleaned_data['age']` is `int`), all error messages, repopulated fields on failure. *(PRG = redirect after successful POST so refresh doesn't resubmit.)*

## 4.5.3 ModelForm ⭐⭐ — forms generated from models

> **Definition:** A **ModelForm** builds a form **automatically from a model** — fields, types, max_lengths, required-ness all derived (DRY!) — and adds a `.save()` that writes the object to the database.

```python
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model  = Student
        fields = ['roll', 'name', 'email', 'marks', 'department']   # explicit list ⭐
        # exclude = ['admitted']  (alternative; explicit fields preferred)

# view: CREATE
def add_student(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()                              # INSERT — model+form in harmony
        return redirect('students:index')
    return render(request, 'students/form.html', {'form': form})

# view: UPDATE — same form, instance pre-fills it!
def edit_student(request, roll):
    s = get_object_or_404(Student, roll=roll)
    form = StudentForm(request.POST or None, instance=s)
    if form.is_valid():
        form.save()                              # UPDATE
        return redirect('students:detail', roll=s.roll)
    return render(request, 'students/form.html', {'form': form})
```
| | Form | ModelForm |
|---|------|-----------|
| Fields declared | manually | **derived from model** |
| save() to DB | you write it | **built-in** |
| Use for | search boxes, contact, login | CRUD on models (most forms!) |

## 4.5.4 Widgets — controlling the HTML ⭐

> **Definition:** A **widget** is the HTML-rendering component of a field — which `<input type>`/element appears and with which attributes. Field = validation logic; widget = appearance.

| Widget | Renders | Typical pairing |
|--------|---------|-----------------|
| `TextInput` | `<input type="text">` | CharField default |
| `EmailInput` | `type="email"` | EmailField default |
| `PasswordInput` | `type="password"` | login forms |
| `Textarea` | `<textarea>` | long text |
| `Select` | `<select>` dropdown | ChoiceField / FK default |
| `CheckboxInput`, `RadioSelect`, `DateInput`, `FileInput` | as named | — |

### Styling forms — Bootstrap integration (the practical question)
```python
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll', 'name', 'email', 'marks', 'department']
        widgets = {                                   # add Module-3 classes!
            'name':  forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control',
                                              'min': 0, 'max': 100}),
            'department': forms.Select(attrs={'class': 'form-select'}),
        }
```
Or render fields manually for full Bootstrap control:
```html
<div class="mb-3">
    <label class="form-label">{{ form.name.label }}</label>
    {{ form.name }}
    {% for err in form.name.errors %}
        <div class="text-danger small">{{ err }}</div>
    {% endfor %}
</div>
```
*(Third-party shortcut worth naming in interviews: `django-crispy-forms` renders whole forms Bootstrap-ready.)*

## 4.5.5 Validation — Built-in & Custom ⭐⭐

**Built-in (declared on fields):** `required=True` (default!), `max_length/min_length`, `min_value/max_value`, type checks (EmailField), `validators=[...]`.

**Custom — two levels:**
```python
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student; fields = ['roll', 'name', 'email', 'marks', 'department']

    # LEVEL 1: clean_<fieldname> — single-field rule
    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@college.edu'):
            raise forms.ValidationError("Use your official @college.edu email.")
        return email                              # ⭐ MUST return the value!

    # LEVEL 2: clean() — cross-field rules
    def clean(self):
        cleaned = super().clean()
        marks, dept = cleaned.get('marks'), cleaned.get('department')
        if marks is not None and dept and dept.name == 'CSE' and marks < 40:
            raise forms.ValidationError("CSE requires minimum 40 marks.")
        return cleaned
```
**Validation order when is_valid() runs:** field built-ins → each `clean_field()` → `clean()` → errors collected into `form.errors` (field errors + non-field errors).

### Displaying errors
```html
{% if form.non_field_errors %}
  <div class="alert alert-danger">{{ form.non_field_errors }}</div>
{% endif %}
<!-- per-field: form.field.errors as in 4.5.4; {{ form.as_p }} shows all automatically -->
```

## 4.5.6 CSRF Protection ⭐⭐ (security must-know)

> **Definition:** **CSRF (Cross-Site Request Forgery)** is an attack where a malicious site silently submits a request **using the victim's logged-in session** in another tab — e.g., an invisible auto-submitting form posting to `yourbank.com/transfer`.

**Django's defense:** every rendered form embeds a secret per-session token via `{% csrf_token %}`; middleware **rejects any POST whose token is missing/wrong (403 Forbidden)**. The attacker's site cannot read your token (browser same-origin policy), so forged POSTs fail.
```html
<form method="post">
    {% csrf_token %}        <!-- renders <input type="hidden" name="csrfmiddlewaretoken" value="…"> -->
```
> ⚠️ **Warning:** *"403 CSRF verification failed"* = you forgot the tag. It belongs in **every** POST form. Never "fix" it by disabling CsrfViewMiddleware. (Module-2 flashback: parameterization beat injection; tokens beat forgery — frameworks make the secure way the easy way.)

## 4.5.7 END-OF-TOPIC PACK (4.5)

### Quick Revision Notes
- Form class = fields + validation + HTML rendering + cleaned_data; the GET/POST if-else + PRG redirect is THE pattern.
- Bound (has data) vs unbound; is_valid() → cleaned_data (typed!).
- ModelForm: Meta.model + fields; save() does INSERT, instance=obj makes it UPDATE.
- Widgets style fields: attrs={'class':'form-control'} = Bootstrap bridge; render manually for full control.
- Validation ladder: built-ins → clean_field() (return value!) → clean() (cross-field) → form.errors.
- {% csrf_token %} in every POST form; missing = 403.

### Important Definitions
Form • Bound/unbound form • cleaned_data • ModelForm • Widget • Validator • clean_field vs clean • Non-field errors • CSRF • PRG pattern.

### FAQs
1. *Form invalid but no errors shown?* → template must print form/field errors (or use as_p).
2. *Why redirect after success?* → PRG stops refresh-resubmission duplicates.
3. *`request.POST or None` trick?* → lets one line build bound (POST) or unbound (GET) form.
4. *ModelForm vs Form?* → tied to a model? ModelForm. Otherwise Form.
5. *Where did my dropdown for FK come from?* → ModelForm renders ForeignKey as a Select of related objects automatically.

### Viva Questions
1. Method that triggers validation? 2. Where does clean data land? 3. Bound vs unbound? 4. ModelForm's Meta needs which two? 5. Field vs widget one-liner. 6. Naming rule for single-field cleaners? 7. What must clean_x return? 8. Expand CSRF; the tag? 9. Status code when token missing? 10. as_p does what?

### Interview Questions
1. Full form lifecycle GET→POST→errors→success with the canonical view.
2. ModelForm internals: how fields derive from the model; create vs update via instance.
3. clean_field vs clean vs field validators — order and use cases.
4. CSRF attack walkthrough + how the token defeats it.
5. Three ways to Bootstrap-style Django forms (widgets attrs, manual render, crispy).
6. Why server-side validation is mandatory even with HTML5 validation (Module 3.1.10 callback).
7. How are previous values preserved on error? *(bound form re-rendered)*

### MCQs
1. Validation runs on: a) save() b) **is_valid()** ✓ c) clean() call d) render
2. Validated data lives in: a) form.data b) **form.cleaned_data** ✓ c) request.POST d) form.values
3. ModelForm save() on a create does: a) UPDATE b) **INSERT** ✓ c) SELECT d) nothing
4. Textarea is a: a) field b) **widget** ✓ c) tag d) filter
5. clean_email must: a) print b) **return the value** ✓ c) save d) redirect
6. Missing csrf_token on POST → a) 404 b) **403** ✓ c) 500 d) silent pass

### Short / Long Answer Questions
**Short:** 1. ContactForm with three fields. 2. The canonical view skeleton. 3. ModelForm for Student (code). 4. Add Bootstrap classes to two widgets. 5. Two differences Form vs ModelForm.
**Long:** 1. Forms architecture: workflow diagram, bound/unbound, rendering modes, error display. 2. ModelForm CRUD pair (add+edit views, one template) fully coded. 3. Validation masterclass: all three levels + error templating. 4. CSRF essay: attack, token mechanism, Django middleware, developer duties.

### Practical Lab Questions
1. Build StudentForm (ModelForm) + add/edit views + Bootstrap template; demo error states.
2. Enforce @college.edu emails and a cross-field rule; screenshot both error types.
3. Deliberately omit csrf_token, capture the 403, fix it.
4. Search form (plain Form, GET method) feeding the ORM icontains query from 4.4.

### Debugging Exercises
```
1) 403 Forbidden on submit                         → {% csrf_token %} missing
2) form.cleaned_data AttributeError                → accessed before/without is_valid()
3) Edit view creates duplicates                    → forgot instance=s in StudentForm(...)
4) clean_email "ValidationError not defined"       → from django import forms; forms.ValidationError
5) Custom rule ignored                             → method named clean_Email (case!) / no return
6) Dropdown empty for department                   → no Department rows exist yet
```

### Assignment Questions
1. Compare raw request.POST handling vs Django Forms on the same feature (lines, safety, UX).
2. Document five built-in validators from the docs with examples.
3. One page: PRG pattern — problem, solution, Django implementation.

### Coding Exercises
1. Registration form: password + confirm with clean() match check (PasswordInput widgets).
2. Feedback form with rating ChoiceField (RadioSelect) saving via ModelForm.
3. Reusable Bootstrap form-field include: `_field.html` partial used for any field.
4. Bulk-marks form: a plain Form with IntegerField bonus applied via F-expression update.

### Scenario-Based Questions
1. *Users double-submit orders by refreshing.* → PRG fix.
2. *Spam bots post to your contact form from scripts.* → CSRF already blocks cross-site posts; discuss what it does and doesn't stop (rate-limiting/captcha for direct bots).
3. *Client wants the same form to create AND edit profiles.* → instance pattern.

### Mini Project Ideas
Complete CRUD (forms-only) student manager • event-registration app with custom validation rules • multi-step survey using one form class per step.

### Summary
Django Forms collapse the form pipeline into a class: fields declare validation, widgets control HTML (and carry your Bootstrap classes), `is_valid()` runs built-ins → `clean_field()` → `clean()` and fills `cleaned_data` with typed values, while errors and previous input re-render automatically. ModelForms derive all of it from your models and add `save()` — with `instance=` turning the same form into an editor. Every POST form carries `{% csrf_token %}`, defeating cross-site forgery, and successful posts end in a redirect (PRG). User input is now safe and structured — time to manage the data like a boss: the admin panel.

---
---
# §6. TOPIC 4.6 — DJANGO ADMIN PANEL

## 4.6.1 Introduction — Django's Killer Feature

> **Definition:** The **Django admin** is an automatically generated, production-ready **web interface for managing your models' data** — list, search, filter, create, edit, delete — built from your model definitions with almost zero code.

**Why it exists / productivity:** every project needs a back office ("staff adds products, edits students, moderates comments"). Hand-building that = weeks (it's literally Topics 4.2–4.5 again, for staff). Django generates it in **two lines per model** — the single biggest reason teams pick Django.
**Analogy:** the admin is the **manager's control room** 🎛 pre-installed in the mall — CCTV over every shop (model), with hire-your-own-staff permissions.

### Activation ritual
```bash
python manage.py createsuperuser     # username, email, password → top-level account
python manage.py runserver           # then open http://127.0.0.1:8000/admin/
```
*(`path('admin/', admin.site.urls)` is pre-wired in project urls.py; auth tables came from your first `migrate`.)*

## 4.6.2 Registering Models
```python
# students/admin.py
from django.contrib import admin
from .models import Department, Student

admin.site.register(Department)       # the two-line miracle
admin.site.register(Student)
```
Refresh /admin/ → both tables appear with full CRUD UI. Rows display via your `__str__` (another reason it matters!).

## 4.6.3 Admin Customization ⭐ — ModelAdmin

```python
@admin.register(Student)                       # decorator style (= register(Student, StudentAdmin))
class StudentAdmin(admin.ModelAdmin):
    list_display  = ('roll', 'name', 'department', 'marks', 'is_active')  # table columns
    search_fields = ('name', 'email')          # search box: icontains across these
    list_filter   = ('department', 'is_active')  # right-hand filter sidebar
    ordering      = ('-marks',)                # default sort
    list_per_page = 25                         # pagination
    list_editable = ('marks',)                 # edit in the list itself!

    fieldsets = (                              # GROUP fields on the edit page
        ('Identity', {'fields': ('roll', 'name', 'email')}),
        ('Academics', {'fields': ('department', 'marks')}),
        ('Status', {'fields': ('is_active',), 'classes': ('collapse',)}),
    )

    @admin.display(description='Grade')        # computed column!
    def grade(self, obj):
        return 'A' if obj.marks >= 75 else 'B' if obj.marks >= 60 else 'C'
    # add 'grade' into list_display to show it
```
| Option | Gives you |
|--------|-----------|
| `list_display` | chosen columns (fields, methods, computed) |
| `search_fields` | top search box (`'department__name'` spans FKs!) |
| `list_filter` | sidebar filters (booleans, FKs, dates shine) |
| `ordering` | default sort (tuple; '-' = DESC) |
| `fieldsets` | grouped, collapsible edit-form sections |
| `readonly_fields`, `date_hierarchy`, `list_editable`, `prepopulated_fields` | the usual next steps |

## 4.6.4 Inlines — edit children inside the parent ⭐
```python
class StudentInline(admin.TabularInline):      # or StackedInline (vertical)
    model = Student
    extra = 1                                  # blank rows offered

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    inlines = [StudentInline]                  # edit a dept AND its students together
```
Open a Department → its students appear as an editable table inside the same page — the 1:N relationship made tangible.

## 4.6.5 Custom Admin Actions — bulk operations
```python
@admin.action(description="Mark selected students inactive")
def deactivate(modeladmin, request, queryset):
    queryset.update(is_active=False)           # ORM bulk update (4.4!)

class StudentAdmin(admin.ModelAdmin):
    actions = [deactivate]                     # appears in the dropdown over the list
```
Select rows → choose action → Go. (The built-in "delete selected" works the same way.)

## 4.6.6 Admin Security — Permissions, Users & Roles

| Flag on a user | Meaning |
|----------------|---------|
| `is_superuser` | all permissions everywhere, implicitly |
| `is_staff` | **may log into /admin/** (but sees only granted models) |
| `is_active` | account enabled at all |

- Django auto-creates **four permissions per model**: add / change / delete / view.
- **Groups = roles ⭐:** create group "Clerks" with *view+add Student* → assign users → role-based access without per-user micromanagement (Module 2's GRANT, with a UI).
- Hygiene: strong superuser password • few superusers • staff users get groups, not superuser • consider changing the `/admin/` URL in production • admin actions respect permissions.

## 4.6.7 END-OF-TOPIC PACK (4.6)

### Quick Revision Notes
- createsuperuser → /admin/; register models in admin.py (2 lines) → instant CRUD UI; __str__ = row labels.
- ModelAdmin: list_display, search_fields (FK spanning), list_filter, ordering, fieldsets(+collapse), list_editable, computed columns via methods.
- Inlines (Tabular/Stacked) edit children inside parents; @admin.action + actions=[] = bulk operations on querysets.
- Security: is_staff (door) vs is_superuser (master key); 4 auto permissions/model; Groups = roles.

### Important Definitions
Admin site • Superuser • ModelAdmin • list_display • Inline • Admin action • Permission • Group/Role • is_staff.

### FAQs
1. *Model missing in admin?* → not registered (or app missing from INSTALLED_APPS).
2. *"Department object (1)" rows?* → define __str__.
3. *Staff user sees an empty admin?* → no permissions/groups granted yet.
4. *Search FK fields?* → 'department__name' in search_fields.
5. *Is admin for end-users?* → No — staff back office only; users get your real views.

### Viva Questions
1. Command creating the admin account? 2. File + function to register? 3. Option controlling columns? 4. Sidebar filters option? 5. Inline purpose in one line. 6. is_staff vs is_superuser. 7. The four per-model permissions. 8. What are groups for? 9. Decorator alternative to register()? 10. Where do bulk actions get their rows? *(queryset)*

### Interview Questions
1. Why is the admin a competitive advantage of Django? 2. Tour a fully customized ModelAdmin (write one cold). 3. Inlines and which relationship they expose. 4. Build role-based staff access (clerk vs manager) with groups. 5. Custom action with permission check. 6. Admin hardening checklist for production.

### MCQs
1. Admin URL default: a) /panel/ b) **/admin/** ✓ c) /manage/ d) /root/
2. Register models in: a) models.py b) **admin.py** ✓ c) settings.py d) urls.py
3. Columns come from: a) list_filter b) **list_display** ✓ c) fields d) ordering
4. Login-to-admin flag: a) is_superuser b) **is_staff** ✓ c) is_admin d) is_active
5. Edit children in parent page: a) actions b) **inlines** ✓ c) fieldsets d) filters
6. Auto permissions per model: a) 2 b) 3 c) **4** ✓ d) 5

### Short / Long Answers
**Short:** 1. Two-line registration. 2. StudentAdmin with 4 options. 3. Tabular vs Stacked inline. 4. An @admin.action skeleton. 5. Three security flags.
**Long:** 1. Admin end-to-end: activation, registration, every customization option with a worked ModelAdmin. 2. Permissions architecture: flags, model permissions, groups, a clerk/manager case study. 3. Inlines + actions: code, mechanics, real workflows they replace.

### Practical Lab Questions
1. Superuser + register both models; add 5 rows through the UI.
2. Full StudentAdmin (columns incl. computed grade, search, filters, fieldsets, list_editable) — screenshot each feature.
3. DepartmentAdmin with StudentInline; create a dept + 3 students in one save.
4. Clerk group (view/add only) + staff user; log in as them and document the differences.

### Debugging Exercises
```
1) /admin/ 404                          → admin path removed from project urls.py
2) Model invisible                      → admin.site.register missing
3) search box absent                    → search_fields not set
4) "students" app label crash on start  → typo in fieldsets field name
5) Action edits nothing                 → used Model.objects.all() instead of the passed queryset
6) New staff user can't log in to admin → is_staff unchecked
```

### Assignment / Coding / Scenario
**Assignment:** compare Django admin vs building a custom back office (cost table); document 5 ModelAdmin options not covered here (docs dive); admin-hardening memo.
**Coding:** export-selected-to-CSV admin action (HttpResponse with text/csv — Modules 1 file skills!); colored marks column via format_html; date_hierarchy on admitted.
**Scenario:** *Non-technical librarian must manage books today* → admin + group, justify; *intern deleted rows accidentally* → remove delete permission, add view-only group; *boss wants weekly bulk deactivation* → custom action.

### Mini Project Ideas
Admin-only inventory tool (zero custom views!) • news-desk: Article+Category with inlines, publish/unpublish actions • staff-roles sandbox demonstrating 3 permission tiers.

### Summary
Two lines in admin.py turn any model into a full management UI behind /admin/, unlocked by createsuperuser. ModelAdmin tunes it — list_display columns (even computed), search across FKs, sidebar filters, fieldsets, in-list editing — while inlines surface 1:N children inside parents and custom actions run ORM bulk operations on selected rows. Security rides on is_staff/is_superuser, four auto permissions per model, and groups-as-roles. The staff side is done; next, accounts for everyone else: authentication.

---
---
# §7. TOPIC 4.7 — USER AUTHENTICATION SYSTEM

## 4.7.1 Authentication vs Authorization ⭐ (the opening question of every interview)

| | **Authentication** | **Authorization** |
|---|--------------------|--------------------|
| Question | **WHO are you?** | **WHAT may you do?** |
| Mechanism | login (credentials → identity) | permissions, groups, roles |
| Example | password check succeeds → you are Asha | Asha may view marks but not edit them |
| Order | always FIRST | always second |

**Analogy:** airport ✈ — authentication = passport control (prove identity); authorization = boarding pass (which gate/seat you're allowed).

## 4.7.2 The Django User Model

Django ships a complete `User` model (`django.contrib.auth.models.User`) — the auth battery:

| Field/flag | Purpose |
|------------|---------|
| `username`, `email`, `first_name`, `last_name` | identity |
| `password` | **hashed** (never plain! see 4.7.8) |
| `is_active`, `is_staff`, `is_superuser` | the Topic-4.6 trio |
| `date_joined`, `last_login` | bookkeeping |
| `user.groups`, `user.user_permissions` | authorization hooks |

**Custom user models:** for extra fields you either (a) **extend with a Profile** — `OneToOneField(User)` holding phone/photo/roll (easy, anytime), or (b) **substitute** via `AbstractUser` + `AUTH_USER_MODEL = 'accounts.User'` (powerful, but must be done **before the first migrate** — a famous gotcha). Rule of thumb for projects: start with Profile; mention AbstractUser in interviews.

## 4.7.3 Registration System
```python
# accounts/forms.py — extend the built-in two-password form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# accounts/views.py
from django.shortcuts import render, redirect
from .forms import RegisterForm

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()                       # hashes the password automatically! ⭐
        return redirect('accounts:login')
    return render(request, 'accounts/register.html', {'form': form})
```
`UserCreationForm` gives username rules, password strength validators, and the match-check between password1/password2 for free (Topic 4.5 skills, pre-built).

## 4.7.4 Login & Logout
```python
# accounts/views.py
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == 'POST':
        user = authenticate(request,                       # ① CHECK credentials
                            username=request.POST['username'],
                            password=request.POST['password'])
        if user is not None:
            login(request, user)                           # ② CREATE the session
            return redirect('students:index')
        return render(request, 'accounts/login.html',
                      {'error': 'Invalid username or password'})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)                                        # ③ DESTROY the session
    return redirect('accounts:login')
```
**The trio:** `authenticate()` verifies and returns a User or None (via the **authentication backend** — default checks the DB; swappable for LDAP/OAuth); `login()` writes the user id into the **session**; `logout()` flushes it. *(Even faster path: Django's built-in `LoginView`/`LogoutView` + one template — name-drop in vivas.)*

**In templates:**
```html
{% if user.is_authenticated %}
    Hello, {{ user.username }}! <a href="{% url 'accounts:logout' %}">Logout</a>
{% else %}
    <a href="{% url 'accounts:login' %}">Login</a>
{% endif %}
```

## 4.7.5 Sessions & Cookies ⭐ (how login "sticks")

> **Definition:** HTTP is **stateless** — each request is a stranger. A **session** is server-side per-visitor storage; a **cookie** holding the random `sessionid` ties the visitor's browser to it.

```
 LOGIN:  server stores {user_id: 7} under key 'a8f3…' (django_session table)
         → Set-Cookie: sessionid=a8f3…
 EVERY NEXT REQUEST: browser sends Cookie: sessionid=a8f3…
         → middleware loads the session → request.user = Asha
 LOGOUT: session deleted → cookie now points at nothing
```
Use it yourself: `request.session['cart'] = [1,5]` — dict-like, persisted per visitor (the e-commerce cart in §10 runs on this). Settings: `SESSION_COOKIE_AGE`, browser-close expiry, etc.

## 4.7.6 Protecting Views & Authorization
```python
from django.contrib.auth.decorators import login_required, permission_required

@login_required                               # Module-1 decorators, earning rent!
def dashboard(request):
    return render(request, 'students/dashboard.html')

@permission_required('students.change_student')      # authorization layer
def edit_marks(request, roll): ...
```
- Anonymous visitor → redirected to `settings.LOGIN_URL` (e.g. `LOGIN_URL = 'accounts:login'`) with `?next=/dashboard/` so login returns them.
- **Permissions & groups** (Topic 4.6's model: add/change/delete/view × Groups-as-roles) check in code via `user.has_perm('students.view_student')` and in templates via `{% if perms.students.change_student %}`.

## 4.7.7 Password Management
```python
# urls.py — built-in views do ALL the work
from django.contrib.auth import views as auth_views
urlpatterns += [
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-reset/',  auth_views.PasswordResetView.as_view(),  name='password_reset'),
    # + done/confirm/complete companions — Django provides the full 4-step reset flow
]
```
**Change** = logged-in user supplies old + new. **Reset** = forgot it: email link with a one-time token → set new password (dev tip: `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'` prints the email to your terminal).

## 4.7.8 Security Best Practices ⭐

**Password hashing:** Django **never stores passwords** — it stores `<algorithm>$<iterations>$<salt>$<hash>` (PBKDF2-SHA256 by default; Argon2 optional). Hashing is one-way; login re-hashes the attempt and compares. Salt = random per-user spice so identical passwords hash differently and rainbow tables fail.
```
plain "lion123" ─PBKDF2(+salt, 600k rounds)─▶ pbkdf2_sha256$600000$rTx…$Jq9…  (stored)
   login attempt ────── same recipe ─────────▶ compare hashes, never plaintexts
```
**Brute force & friends:** strength validators on by default (AUTH_PASSWORD_VALIDATORS) • rate-limit login (django-axes / django-ratelimit) • HTTPS in production (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE = True`) • generic error messages ("invalid username **or** password" — don't reveal which) • CSRF on all auth forms • never log passwords.

## 4.7.9 END-OF-TOPIC PACK (4.7)

### Quick Revision Notes
- AuthN = who (login) vs AuthZ = what (permissions); always in that order.
- Built-in User: username/email/hashed password/is_active/staff/superuser; extend via OneToOne Profile or AbstractUser (before first migrate!).
- Registration: UserCreationForm subclass → form.save() hashes automatically.
- Login trio: authenticate() → login() (session write) → logout() (flush); template flag user.is_authenticated.
- Sessions: server-side dict + sessionid cookie defeat HTTP statelessness; request.session is yours too.
- @login_required (+ LOGIN_URL, ?next=), @permission_required, groups=roles, perms in templates.
- Built-in PasswordChange/Reset views; hashing = PBKDF2 + salt, one-way; generic errors, rate-limiting, HTTPS cookies.

### Important Definitions
Authentication • Authorization • User model • Session • Cookie • sessionid • Hash • Salt • Authentication backend • LOGIN_URL/next • Permission • Group.

### FAQs
1. *Can I read a user's password?* → No — only the hash exists; that's the point.
2. *login() vs authenticate()?* → authenticate verifies; login persists (session). Both needed.
3. *Why am I logged out in another browser?* → sessions are per-browser cookies.
4. *@login_required loops forever?* → LOGIN_URL misnamed / login view itself protected.
5. *Where are sessions stored?* → django_session table by default (cache/file/cookie backends exist).

### Viva Questions
1. AuthN vs AuthZ one-liner. 2. Import path of User. 3. Which form gives password1/password2? 4. The three functions of the login trio. 5. What does the sessionid cookie contain? *(random key only — no data)* 6. Decorator protecting views? 7. Where does ?next= come from? 8. Default hash algorithm? 9. What is salt for? 10. Flag checked by template {% if user.is_authenticated %}?

### Interview Questions
1. Trace a full login: form POST → authenticate → backend → session → next request's request.user.
2. Why hash+salt instead of encryption for passwords?
3. Sessions vs cookies vs localStorage (tie back to Module 3.1.13).
4. Profile vs AbstractUser — trade-offs and the migration timing trap.
5. Implement role-based access for clerk/teacher/admin using groups + decorators + template perms.
6. The password-reset token flow — why is it safe?
7. Five hardening steps for a production login system.

### MCQs
1. "What can you do" is: a) authentication b) **authorization** ✓ c) hashing d) session
2. authenticate() returns on failure: a) False b) **None** ✓ c) error page d) exception
3. Session data lives: a) in the cookie b) **on the server** ✓ c) in JS d) in templates
4. @login_required redirects to: a) /admin/ b) **settings.LOGIN_URL** ✓ c) home d) 403
5. Passwords are stored as: a) plaintext b) encrypted c) **salted hashes** ✓ d) base64
6. UserCreationForm validates: a) email MX b) **password match + strength** ✓ c) phone d) captcha

### Short / Long Answers
**Short:** 1. RegisterForm code. 2. login_view skeleton. 3. Session mechanism in 3 lines. 4. Two auth decorators. 5. Hash vs encrypt.
**Long:** 1. Complete auth system: register/login/logout code + templates + URLs. 2. Sessions & cookies architecture with the statelessness story. 3. Password security essay: hashing, salting, validators, reset flow, brute-force defenses. 4. Authorization design: permissions, groups, decorators, template checks — clerk/manager case study.

### Practical Lab Questions
1. Build the accounts app: register → login → protected dashboard → logout (navbar reflects state).
2. Add ?next= proof: hit /dashboard/ logged out, land back after login.
3. Console-email password reset end-to-end; paste the emailed link from the terminal.
4. Two groups (viewers/editors); protect edit view by permission; test both users.

### Debugging Exercises
```
1) authenticate() always None                 → password set without hashing (used User(password=…) not create_user/form)
2) Redirect loop at /accounts/login/          → login view behind @login_required
3) user.is_authenticated False after login()  → login(request, user) never called / session middleware removed
4) Reset email never "arrives" in dev         → console EMAIL_BACKEND not set; check terminal
5) PermissionDenied for a superuser? Impossible → it isn't; check you're logged in as the test user, not admin
6) Logout link triggers 405                   → built-in LogoutView now requires POST — use a form button
```

### Assignment / Coding / Scenario
**Assignment:** diagram poster of the login lifecycle; compare session auth vs token auth (API world) in one page; audit a real site's login UX for the practices in 4.7.8.
**Coding:** Profile model (photo, roll) auto-created on registration; "remember me" checkbox toggling session expiry; login attempt counter in session locking after 5 tries.
**Scenario:** *DB leaks — are passwords safe?* (hash+salt discussion) • *College wants teachers-only marks editing* (groups + permission_required) • *User reports being logged out on phone but not laptop* (per-browser sessions).

### Mini Project Ideas
Members-only notes portal • role-based marks system (student view / teacher edit) • full auth starter-kit app you can reuse in every capstone (§10 will!).

### Summary
Django's auth battery delivers the whole identity stack: a ready User model with salted-hash passwords, UserCreationForm-powered registration, the authenticate→login→logout trio writing to cookie-linked server-side sessions that defeat HTTP's statelessness, @login_required/@permission_required guarding views with groups as roles, and built-in change/reset flows. Security defaults are strong — your job is to keep them on (HTTPS cookies, generic errors, rate limits). Users exist; now let's write less view code for their pages: class-based views.

---
---
# §8. TOPIC 4.8 — CLASS-BASED VIEWS (CBV)

## 4.8.1 FBV vs CBV

> **Definition:** A **class-based view** is a view written as a **class** (inheriting Django's View/generic classes); HTTP methods map to class methods (`get()`, `post()`), and behavior is reused through **inheritance and mixins** instead of copy-paste.

By Topic 4.5 you noticed every CRUD view looks identical: fetch → form → is_valid → save → redirect. Django noticed decades ago and shipped **generic CBVs** that implement those patterns; you supply 3–4 attributes.

| | FBV | CBV |
|---|-----|-----|
| Style | explicit function, all logic visible | declarative class, logic inherited |
| Repetition | high across CRUD | near zero (generics) |
| HTTP methods | `if request.method == 'POST':` | separate `get()/post()` methods |
| Learning curve | gentle | steeper (hidden machinery) |
| Best for | one-off/custom logic | standard CRUD pages ⭐ |

**Honest interview answer:** *use generics for standard list/detail/CRUD; FBVs when logic is unusual; never fight a generic into knots.*

## 4.8.2 The Five Generic Views ⭐⭐ (a full CRUD in ~25 lines)

```python
# students/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Student
from .forms import StudentForm

class StudentListView(ListView):                  # READ many
    model = Student
    template_name = 'students/index.html'         # default: students/student_list.html
    context_object_name = 'students'               # default: object_list
    paginate_by = 10                               # free pagination!
    def get_queryset(self):                        # customize the data
        return Student.objects.select_related('department').order_by('-marks')

class StudentDetailView(DetailView):              # READ one (pk or slug from URL)
    model = Student
    template_name = 'students/detail.html'
    context_object_name = 's'

class StudentCreateView(CreateView):              # CREATE
    model = Student
    form_class = StudentForm                       # or fields = ['roll','name',…]
    template_name = 'students/form.html'
    success_url = reverse_lazy('students:index')   # lazy: resolved at runtime ⭐

class StudentUpdateView(UpdateView):              # UPDATE — same template!
    model = Student
    form_class = StudentForm
    template_name = 'students/form.html'
    success_url = reverse_lazy('students:index')

class StudentDeleteView(DeleteView):              # DELETE (GET=confirm page, POST=do it)
    model = Student
    template_name = 'students/confirm_delete.html'
    success_url = reverse_lazy('students:index')
```
```python
# students/urls.py — note .as_view() ⭐
path('',                views.StudentListView.as_view(),   name='index'),
path('<int:pk>/',       views.StudentDetailView.as_view(), name='detail'),
path('add/',            views.StudentCreateView.as_view(), name='add'),
path('<int:pk>/edit/',  views.StudentUpdateView.as_view(), name='edit'),
path('<int:pk>/delete/',views.StudentDeleteView.as_view(), name='delete'),
```
| Generic | Replaces the FBV that… | Key attributes |
|---------|------------------------|----------------|
| ListView | queries all + renders list | model, paginate_by, get_queryset |
| DetailView | get_object_or_404 + render | model (expects pk/slug in URL) |
| CreateView | blank form / validate / save / redirect | form_class, success_url |
| UpdateView | instance form / validate / save / redirect | same + pk in URL |
| DeleteView | confirm page + delete + redirect | success_url |

*(Why `reverse_lazy`? class attributes evaluate at import time, before URLConf loads — lazy defers resolution. Classic interview nugget.)*

## 4.8.3 Mixins ⭐ — composable behavior

> **Definition:** A **mixin** is a small class adding one capability, combined with views through multiple inheritance. Order matters: **mixins first, view last.**

```python
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class StudentCreateView(LoginRequiredMixin, CreateView):        # = @login_required
    login_url = 'accounts:login'
    ...

class StudentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'students.delete_student'             # = @permission_required
    ...
```
Other staples: `UserPassesTestMixin` (custom rule, e.g. author-only edit), `SuccessMessageMixin`. Decorators are to FBVs what mixins are to CBVs.

## 4.8.4 CBV Workflow & MRO (how the magic dispatches)
```
 request ─▶ as_view() returns a handler ─▶ instance created
        ─▶ dispatch(): method check (GET? POST?) + mixin gatekeepers run here
        ─▶ get() / post() of the generic
             ListView.get  → get_queryset → get_context_data → render
             CreateView.post → form_valid()/form_invalid() hooks
```
**MRO (Method Resolution Order)** — Python's left-to-right inheritance search (Module 1.7's OOP!) — is why `LoginRequiredMixin` must precede the generic: its dispatch() runs first and can redirect before any work happens. Inspect with `StudentCreateView.__mro__`. Common hooks to override: `get_queryset`, `get_context_data` (add extra context), `form_valid` (e.g., `form.instance.author = self.request.user` before save).

## 4.8.5 END-OF-TOPIC PACK (4.8)

### Quick Revision Notes
- CBV = view as class; URLs need `.as_view()`; methods get()/post() replace if-method branching.
- Five generics: ListView (paginate_by, context_object_name, get_queryset) • DetailView (pk/slug) • Create/UpdateView (form_class, success_url=reverse_lazy) • DeleteView (GET confirm, POST delete).
- Mixins add powers: LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin — **listed before** the generic (MRO!).
- dispatch() routes by HTTP method; override hooks: get_queryset, get_context_data, form_valid.

### Important Definitions
CBV • Generic view • as_view() • Mixin • MRO • dispatch() • reverse_lazy • context_object_name • form_valid hook.

### FAQs
1. *TemplateDoesNotExist student_list.html?* → generics have default template names; set template_name or follow the convention.
2. *Why reverse_lazy not reverse?* → import-time vs runtime resolution.
3. *Where's my object in DetailView's template?* → `object` (or model name lowercase / your context_object_name).
4. *Mixin ignored?* → placed after the generic — order is everything.
5. *Replace ALL FBVs?* → no; standard pages yes, exotic logic no.

### Viva Questions
1. URL hookup difference FBV vs CBV? *(.as_view())* 2. Five generics + one attribute each. 3. Which generic shows a confirmation page? 4. Mixin = ? in one line. 5. Decorator twin of LoginRequiredMixin? 6. What does dispatch() decide? 7. Expand MRO; why mixins-first? 8. Default context name in ListView? *(object_list)* 9. Attribute enabling pagination? 10. Hook to tweak the saved object?

### Interview Questions
1. Convert a given FBV CRUD set to generics — narrate every replaced line.
2. CBV request lifecycle: as_view → dispatch → handler → hooks.
3. Explain MRO with LoginRequiredMixin and what breaks when reversed.
4. form_valid use case: stamping request.user on the object.
5. When do CBVs hurt? (debugging hidden flow, one-off logic) — balanced answer.
6. Pagination with ListView: attribute + template variables (page_obj, is_paginated).

### MCQs
1. URLs use: a) View() b) **View.as_view()** ✓ c) View.run d) view()
2. Pagination attribute: a) page_size b) **paginate_by** ✓ c) limit d) per_page
3. CreateView redirect target: a) redirect_to b) **success_url** ✓ c) next d) goto
4. Lazy URL resolver: a) reverse b) **reverse_lazy** ✓ c) url() d) resolve
5. Correct order: a) CreateView, LoginRequiredMixin b) **LoginRequiredMixin, CreateView** ✓ c) any d) neither
6. DeleteView on GET shows: a) deletes instantly b) **confirmation page** ✓ c) 405 d) list

### Short / Long Answers
**Short:** 1. ListView with three attributes. 2. as_view() purpose. 3. Two mixins + function. 4. get_queryset override example. 5. FBV vs CBV (3 points).
**Long:** 1. Full CRUD via generics: all five classes + URLs + the three templates. 2. CBV internals: dispatch, MRO, hooks — with diagram. 3. Mixins masterclass: auth mixins + UserPassesTestMixin author-only edit. 4. Balanced essay: FBV vs CBV decision framework with examples of each winning.

### Practical Lab Questions
1. Re-implement Topic 4.5's add/edit as Create/UpdateView; diff the line counts.
2. Paginated ListView (3/page) with Bootstrap pagination links (page_obj loop).
3. Protect add/edit/delete with auth mixins; verify redirects.
4. UserPassesTestMixin: only the creating user may delete (add created_by FK first).

### Debugging Exercises
```
1) path('add/', StudentCreateView)            → missing .as_view()
2) ImproperlyConfigured: no URL to redirect   → success_url absent (or define get_absolute_url)
3) reverse() at class level crashes at import → use reverse_lazy
4) Mixin never redirects anonymous users      → declared after the generic view
5) ListView template gets empty 'students'    → context_object_name mismatch with template loop
6) DeleteView deletes via GET in tests        → it shouldn't; you posted to it — confirm template's form method
```

### Assignment / Coding / Scenario
**Assignment:** mapping table FBV-pattern → generic; MRO printout annotated for one view; one page "ccbv.co.uk-style" anatomy of CreateView.
**Coding:** SearchListView (get_queryset reads ?q= via icontains+Q); SuccessMessageMixin on create/update; a base OwnerRequiredMixin reused by two views.
**Scenario:** *50 nearly identical list pages requested* → generics + one base class; *junior can't trace where saving happens* → explain form_valid/MRO debugging; *legacy FBV app, partial migration?* → coexist, convert standard pages first.

### Mini Project Ideas
Generic-views-only notes app (zero function views) • reusable "CRUD factory" base classes • blog list/detail with pagination + author-only mixins (feeds §10 Project 3!).

### Summary
CBVs trade explicit repetition for declarative inheritance: `.as_view()` adapts a class for URLs, dispatch() routes by HTTP verb, and the five generics — List/Detail/Create/Update/Delete — implement the eternal CRUD patterns from a few attributes (form_class, success_url via reverse_lazy, paginate_by). Mixins bolt on authentication and permissions when listed before the generic (MRO!), and hooks like get_queryset/form_valid customize the flow. Less code, same power — now the final core skill: letting users upload files.

---
---
# §9. TOPIC 4.9 — FILE UPLOAD & MEDIA HANDLING

## 4.9.1 Introduction — static vs media (don't confuse them!)

> **Definitions:** **Static files** = *your* assets shipped with the code (CSS/JS/logo — Topic 4.3). **Media files** = files **users upload at runtime** (profile photos, resumes, product images). Different folders, different settings, different security posture (media = untrusted input!).

| | Static | Media |
|---|--------|-------|
| Author | developer | **end users** |
| Examples | style.css, logo.png | resume.pdf, selfie.jpg |
| Settings | STATIC_URL / STATICFILES_DIRS | **MEDIA_URL / MEDIA_ROOT** |
| Trust level | trusted | ⚠ validate everything |

## 4.9.2 Configuration ⭐
```python
# settings.py
MEDIA_ROOT = BASE_DIR / 'media'      # WHERE on disk uploads are stored
MEDIA_URL  = '/media/'               # URL prefix to serve them

# project urls.py — dev-server serving of media (DEBUG only!)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ ... ] + static(settings.MEDIA_URL,
                               document_root=settings.MEDIA_ROOT)
```
```
upload "photo.jpg" → saved at  media/students/photo.jpg   (MEDIA_ROOT + upload_to)
                   → served at /media/students/photo.jpg  (MEDIA_URL + path)
                   → DB stores ONLY the relative path string ⭐ (file lives on disk!)
```

## 4.9.3 FileField & ImageField
```python
# models.py
class Student(models.Model):
    ...
    photo  = models.ImageField(upload_to='students/photos/', blank=True)
    resume = models.FileField(upload_to='students/resumes/', blank=True)
    # upload_to supports date patterns: 'docs/%Y/%m/' → media/docs/2026/06/
```
```bash
pip install Pillow        # ⭐ ImageField requires the Pillow imaging library
```
- `ImageField` = FileField + verification that the upload IS an image (via Pillow).
- Useful attributes: `s.photo.url` (for templates), `s.photo.name` (relative path), `s.photo.size` (bytes).
- **Storage process:** request.FILES receives the bytes → Django writes the file under MEDIA_ROOT/upload_to (renaming on collisions) → the model row stores the path.

## 4.9.4 Upload Forms ⭐ (two famous requirements)
```python
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll', 'name', 'email', 'photo', 'resume']

def add_student(request):
    form = StudentForm(request.POST or None,
                       request.FILES or None)       # ① FILES passed to the form!
    if form.is_valid():
        form.save()
        return redirect('students:index')
    return render(request, 'students/form.html', {'form': form})
```
```html
<form method="post" enctype="multipart/form-data">   <!-- ② the magic attribute! -->
    {% csrf_token %}
    {{ form.as_p }}
    <button class="btn btn-primary">Save</button>
</form>
```
> ⚠️ **Warning — the two classic bugs:** forms "ignore" the file when (1) `enctype="multipart/form-data"` is missing on the `<form>` (file never leaves the browser properly) or (2) `request.FILES` isn't passed to the form constructor. Memorize both.

**Displaying uploads:**
```html
{% if s.photo %}
    <img src="{{ s.photo.url }}" class="img-fluid rounded" alt="{{ s.name }} photo">
{% else %}
    <img src="{% static 'images/default-avatar.png' %}" alt="Default avatar">
{% endif %}
<a href="{{ s.resume.url }}" download class="btn btn-sm btn-outline-primary">Resume</a>
```

## 4.9.5 File Security ⭐ (media = untrusted input)
```python
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

def validate_size(f):
    if f.size > 2 * 1024 * 1024:                       # 2 MB cap
        raise ValidationError("File too large (max 2 MB).")

class Student(models.Model):
    resume = models.FileField(
        upload_to='students/resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx']),
                    validate_size])
```
**Checklist:** ✅ whitelist extensions (never blacklist) ✅ cap size (also server-level: DATA_UPLOAD_MAX_MEMORY_SIZE) ✅ ImageField for images (content check, not just name) ✅ never trust/execute uploads; serve from /media/, never import or run ✅ in production, MEDIA_ROOT outside code dirs, web server (Nginx) or cloud storage (S3 via django-storages) serves it — Django's `static()` helper is **dev-only**.

## 4.9.6 Image Processing — resizing & optimization
```python
# models.py — shrink huge photos on save (Pillow)
from PIL import Image

class Student(models.Model):
    photo = models.ImageField(upload_to='students/photos/', blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)              # write file first
        if self.photo:
            img = Image.open(self.photo.path)
            if img.height > 600 or img.width > 600:
                img.thumbnail((600, 600))          # keeps aspect ratio
                img.save(self.photo.path, optimize=True, quality=80)
```
Saves disk + bandwidth (a 4 MB phone selfie → ~80 KB avatar). Heavier needs → libraries like `django-imagekit`/`sorl-thumbnail` (name-drop for interviews).

## 4.9.7 END-OF-TOPIC PACK (4.9)

### Quick Revision Notes
- Static (yours) vs media (users'); MEDIA_ROOT=disk home, MEDIA_URL=serving prefix; dev urls.py `+ static(...)`; DB stores the path, disk stores the file.
- ImageField needs Pillow; upload_to subfolders (+%Y/%m); .url/.name/.size.
- Upload duo: `enctype="multipart/form-data"` + `Form(request.POST, request.FILES)`.
- Security: extension whitelist (FileExtensionValidator), size validator, ImageField content check, never execute uploads, production serving via web server/cloud.
- Pillow resize in save() = optimization pattern.

### Important Definitions
Media files • MEDIA_ROOT vs MEDIA_URL • upload_to • multipart/form-data • request.FILES • Pillow • FileExtensionValidator • Thumbnailing.

### FAQs
1. *Photo "saved" but file field empty?* → the famous duo (enctype / request.FILES).
2. *Image shows 404?* → media URL patterns not added in dev, or MEDIA_URL mismatch.
3. *"Cannot use ImageField because Pillow is not installed"* → exactly that; pip install Pillow.
4. *Does deleting the row delete the file?* → No! orphaned files remain (cleanup = signal/cron — know the caveat).
5. *Static vs media again?* → who authored it: you → static; user → media.

### Viva Questions
1. MEDIA_ROOT vs MEDIA_URL. 2. Library behind ImageField? 3. Form-tag attribute for uploads? 4. Second argument to the form constructor? 5. What does the DB column store? 6. upload_to purpose? 7. One validator class for extensions? 8. Why whitelist not blacklist? 9. Who serves media in production? 10. .url vs .path on a file field.

### Interview Questions
1. Complete upload pipeline: form → request.FILES → storage → DB path → template URL.
2. Static vs media architecture and why production splits them to Nginx/S3.
3. Threat-model user uploads: five attacks, five mitigations.
4. ImageField vs FileField internals (content verification).
5. Auto-thumbnail strategy: save() override vs signals vs imagekit — trade-offs.
6. Orphaned-file problem and cleanup approaches.

### MCQs
1. Uploads live under: a) STATIC_ROOT b) **MEDIA_ROOT** ✓ c) BASE_DIR d) templates
2. ImageField requires: a) NumPy b) **Pillow** ✓ c) OpenCV d) nothing
3. Upload form enctype: a) text/plain b) **multipart/form-data** ✓ c) json d) urlencoded
4. Files arrive in: a) request.POST b) **request.FILES** ✓ c) request.GET d) request.body
5. DB stores: a) the bytes b) **the file path** ✓ c) base64 d) URL only
6. Safer validation style: a) blacklist b) **whitelist** ✓ c) none d) size only

### Short / Long Answers
**Short:** 1. The two media settings + dev URL line. 2. Model with photo+resume. 3. The upload view. 4. Size validator code. 5. Show-photo-or-default template snippet.
**Long:** 1. Media architecture end-to-end with the path/URL diagram and prod notes. 2. Secure upload feature: validators, limits, serving — full code. 3. Image optimization: Pillow save() override, before/after numbers, alternatives.

### Practical Lab Questions
1. Add photo+resume to Student; full add/edit flow with previews on detail page.
2. Break it both classic ways (enctype, FILES) and document the symptoms.
3. Enforce pdf/docx ≤ 2 MB on resume; screenshot both rejections.
4. Thumbnail pipeline: upload a 3000px image, verify the stored 600px version.

### Debugging Exercises
```
1) form.is_valid() but s.photo empty            → request.FILES not passed
2) Upload silently absent server-side           → enctype missing
3) /media/students/p.jpg 404 in dev             → + static(...) line absent in urls.py
4) ImportError: Pillow                          → pip install Pillow (in the venv!)
5) ValidationError never triggers for .exe      → validators on the WRONG field / not migrated
6) Disk filling though rows deleted             → orphaned files; rows don't delete files
```

### Assignment / Coding / Scenario
**Assignment:** comparison note: local MEDIA_ROOT vs S3 (5 factors); one page on multipart encoding; survey 3 real sites' upload restrictions.
**Coding:** profile-photo crop-to-square on save; multi-file gallery model (FK Image rows + inline admin); CSV import view (FileField + Module-1 csv parsing into ORM creates!).
**Scenario:** *Users upload 20 MB DSLR photos, site slows* → size cap + thumbnailing; *security audit flags executable uploads* → whitelist + content checks + no-execute serving; *moving to two web servers* → local disk fails, S3/shared storage discussion.

### Mini Project Ideas
Resume-bank app (upload, list, download, validators) • photo gallery with auto-thumbnails • assignment-submission portal (per-student folders via upload_to callable).

### Summary
Media handling gives users a voice in your filesystem — safely: MEDIA_ROOT/MEDIA_URL define storage and serving (dev helper in urls.py; Nginx/S3 in production), FileField/ImageField (Pillow) put paths in the DB and bytes on disk under upload_to, and uploads only work with the sacred duo — multipart enctype + request.FILES. Treat every upload as hostile: whitelist extensions, cap sizes, verify content, never execute; optimize images on save. All nine core skills are now yours — time to build the five capstones.

---
---
# §10. CAPSTONE PROJECTS — Five Complete Django Applications

> **How to use this section:** Project 1 is presented **in full** — it's the graduation of the `campushub` thread, every file shown. Projects 2–5 are complete **blueprints**: full data design + models, the views/forms/templates that differ from Project 1's patterns, and step plans. Build them in order; each adds one new architectural muscle. A shared **Deployment Preparation** guide closes the section (it applies to all five).

---

## 🎓 PROJECT 1 — Student Management System (full build)

### 1. Requirements Analysis
Staff manage departments & students (CRUD); only logged-in users may modify; public may view lists; admin panel for back office; search; Bootstrap UI. *Actors:* visitor (read), staff user (CRUD), superuser (admin).

### 2. Database Design
```
 Department (1) ───< (N) Student
 ┌────────────┐        ┌──────────────────────────────┐
 │ id PK      │        │ id PK • roll UNIQUE • name   │
 │ name UNIQ  │        │ email UNIQ • marks • photo   │
 └────────────┘        │ is_active • admitted          │
                       │ department FK → Department    │
                       └──────────────────────────────┘
```
### 3. Complete Folder Structure
```
campushub/
├── manage.py
├── campushub/ (settings.py, urls.py, wsgi.py, asgi.py)
├── students/  (models.py, views.py, forms.py, urls.py, admin.py,
│               templates/students/, migrations/)
├── accounts/  (views.py, forms.py, urls.py, templates/accounts/)
├── templates/ (base.html, _navbar.html)
├── static/    (css/style.css)
└── media/     (students/photos/)
```
### 4. Models (students/models.py) — as built through Topics 4.4 + 4.9
```python
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self): return self.name

class Student(models.Model):
    roll       = models.IntegerField(unique=True)
    name       = models.CharField(max_length=50)
    email      = models.EmailField(unique=True)
    marks      = models.IntegerField(default=0)
    is_active  = models.BooleanField(default=True)
    admitted   = models.DateField(auto_now_add=True)
    photo      = models.ImageField(upload_to='students/photos/', blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,
                                   related_name='students')
    class Meta: ordering = ['-marks']
    def __str__(self): return f"{self.roll} – {self.name}"
```
### 5. Forms (students/forms.py)
```python
from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model  = Student
        fields = ['roll', 'name', 'email', 'marks', 'department', 'photo']
        widgets = {f: forms.TextInput(attrs={'class': 'form-control'})
                   for f in ['roll', 'name', 'email', 'marks']}
        widgets['department'] = forms.Select(attrs={'class': 'form-select'})
    def clean_email(self):
        e = self.cleaned_data['email']
        if not e.endswith('@college.edu'):
            raise forms.ValidationError("Official @college.edu email required.")
        return e
```
### 6. Views (students/views.py) — CBV style (Topic 4.8)
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from .models import Student
from .forms import StudentForm

class StudentListView(ListView):
    model = Student; template_name = 'students/index.html'
    context_object_name = 'students'; paginate_by = 10
    def get_queryset(self):
        qs = Student.objects.select_related('department')
        q = self.request.GET.get('q', '')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(email__icontains=q))
        return qs

class StudentDetailView(DetailView):
    model = Student; template_name = 'students/detail.html'; context_object_name = 's'

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student; form_class = StudentForm
    template_name = 'students/form.html'
    success_url = reverse_lazy('students:index')

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student; form_class = StudentForm
    template_name = 'students/form.html'
    success_url = reverse_lazy('students:index')

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student; template_name = 'students/confirm_delete.html'
    success_url = reverse_lazy('students:index')
```
### 7. URLs
```python
# students/urls.py  (app_name='students')
path('', StudentListView.as_view(), name='index'),
path('<int:pk>/', StudentDetailView.as_view(), name='detail'),
path('add/', StudentCreateView.as_view(), name='add'),
path('<int:pk>/edit/', StudentUpdateView.as_view(), name='edit'),
path('<int:pk>/delete/', StudentDeleteView.as_view(), name='delete'),
# accounts/urls.py: register/, login/, logout/  (Topic 4.7 views)
# project urls.py: admin/, include both apps, + static(MEDIA_URL, ...)
```
### 8. Templates (key files; all extend base.html from Topic 4.3)
```html
<!-- students/index.html -->
{% extends 'base.html' %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
  <h1>Students</h1>
  <form class="d-flex" method="get">
    <input class="form-control me-2" name="q" value="{{ request.GET.q }}"
           placeholder="Search…">
    <button class="btn btn-outline-primary">Go</button>
  </form>
  {% if user.is_authenticated %}
    <a class="btn btn-primary" href="{% url 'students:add' %}">+ Add</a>
  {% endif %}
</div>
<table class="table table-striped table-hover align-middle">
  <thead class="table-dark"><tr>
    <th>Roll</th><th>Name</th><th>Dept</th><th>Marks</th><th></th></tr></thead>
  <tbody>
  {% for s in students %}
    <tr><td>{{ s.roll }}</td>
        <td><a href="{% url 'students:detail' s.pk %}">{{ s.name }}</a></td>
        <td>{{ s.department.name }}</td><td>{{ s.marks }}</td>
        <td>{% if user.is_authenticated %}
          <a class="btn btn-sm btn-outline-secondary"
             href="{% url 'students:edit' s.pk %}">Edit</a>
          <a class="btn btn-sm btn-outline-danger"
             href="{% url 'students:delete' s.pk %}">Delete</a>
        {% endif %}</td></tr>
  {% empty %}<tr><td colspan="5">No students found.</td></tr>{% endfor %}
  </tbody>
</table>
{% if is_paginated %}  <!-- Bootstrap pagination from page_obj -->
<nav><ul class="pagination">
  {% if page_obj.has_previous %}<li class="page-item">
    <a class="page-link" href="?page={{ page_obj.previous_page_number }}&q={{ request.GET.q }}">«</a></li>{% endif %}
  <li class="page-item disabled"><span class="page-link">
    {{ page_obj.number }} / {{ page_obj.paginator.num_pages }}</span></li>
  {% if page_obj.has_next %}<li class="page-item">
    <a class="page-link" href="?page={{ page_obj.next_page_number }}&q={{ request.GET.q }}">»</a></li>{% endif %}
</ul></nav>{% endif %}
{% endblock %}
```
```html
<!-- students/form.html — serves BOTH create & update -->
{% extends 'base.html' %}
{% block content %}
<h1>{% if form.instance.pk %}Edit{% else %}Add{% endif %} Student</h1>
<form method="post" enctype="multipart/form-data" class="col-md-6">
  {% csrf_token %}
  {{ form.as_p }}
  <button class="btn btn-primary">Save</button>
  <a class="btn btn-secondary" href="{% url 'students:index' %}">Cancel</a>
</form>
{% endblock %}

<!-- students/confirm_delete.html -->
{% extends 'base.html' %}{% block content %}
<div class="alert alert-danger">Delete <b>{{ object }}</b> permanently?</div>
<form method="post">{% csrf_token %}
  <button class="btn btn-danger">Yes, delete</button>
  <a class="btn btn-secondary" href="{% url 'students:index' %}">Cancel</a>
</form>{% endblock %}
```
### 9. Authentication & Admin
Accounts app exactly as Topic 4.7 (register/login/logout, navbar shows state); admin exactly as Topic 4.6 (StudentAdmin with list_display/search/filters + DepartmentAdmin with StudentInline).

### 10. Step-by-Step Development (the order that works)
① venv+project+apps ② settings (apps, templates DIRS, static, media) ③ models→migrate→superuser ④ admin customization, seed data through it ⑤ base.html+navbar ⑥ ListView+index ⑦ Detail ⑧ Form+Create/Update ⑨ Delete ⑩ auth app + mixins ⑪ search & pagination ⑫ photo upload ⑬ polish (messages framework, empty states) ⑭ test matrix: visitor vs user vs admin.

---

## 📚 PROJECT 2 — Library Management System (blueprint)

**Requirements:** catalog books, register members, issue/return with due dates, search, availability tracking, fine display. *New muscles:* two FKs on one model, business-logic view (issue/return), computed properties.
**Database design:**
```
 Author(1)──<(N) Book(1)──<(N) Issue(N)>──(1) Member
 Book: title, author FK, isbn UNIQ, copies_total, copies_available
 Member: name, email UNIQ, joined
 Issue: book FK, member FK, issue_date, due_date, returned (bool), return_date
```
**Models (core):**
```python
class Book(models.Model):
    title  = models.CharField(max_length=120)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    isbn   = models.CharField(max_length=13, unique=True)
    copies_total = models.PositiveIntegerField(default=1)
    copies_available = models.PositiveIntegerField(default=1)
    @property
    def is_available(self): return self.copies_available > 0

class Issue(models.Model):
    book   = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issues')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='issues')
    issue_date  = models.DateField(auto_now_add=True)
    due_date    = models.DateField()
    returned    = models.BooleanField(default=False)
    @property
    def fine(self):
        from datetime import date
        late = (date.today() - self.due_date).days
        return max(late, 0) * 5 if not self.returned else 0
```
**Key view — the transaction-shaped logic (Module 2.3.7 spirit):**
```python
@login_required
def issue_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if not book.is_available:
            form.add_error(None, "No copies available.")
        elif form.is_valid():
            issue = form.save(commit=False)        # ⭐ commit=False pattern
            issue.book = book
            issue.save()
            book.copies_available = F('copies_available') - 1   # atomic!
            book.save(update_fields=['copies_available'])
            return redirect('library:book_detail', pk=book.pk)
    ...
```
**Views/templates/forms:** Book & Member CRUD = Project-1 generic pattern verbatim; plus issue/return FBVs, "overdue report" ListView (`filter(returned=False, due_date__lt=today)`), search across `Q(title|author__name|isbn)`. **Admin:** Book list with availability column; Issue list_filter by returned + date_hierarchy. **Auth:** all mutations behind login; "Librarians" group owns issue/return permissions.
**Steps:** models+admin first (run the library entirely from admin on day 1!) → public catalog → issue/return logic → overdue report → fines on member page.

---

## ✍ PROJECT 3 — Blog Management System (blueprint)

**Requirements:** posts with categories & slugs, author = logged-in user, comments by users, draft/published states, per-category pages. *New muscles:* slugs, form_valid user-stamping, related comments, UserPassesTestMixin (author-only edit).
**Database design:**
```
 User(1)──<(N) Post(N)>──(1) Category      Post(1)──<(N) Comment(N)>──(1) User
 Post: title, slug UNIQ, body, created, status(choices: D/P), author FK, category FK
 Comment: post FK, user FK, body, created
```
**Models (core):**
```python
class Post(models.Model):
    STATUS = [('D', 'Draft'), ('P', 'Published')]
    title    = models.CharField(max_length=150)
    slug     = models.SlugField(unique=True)
    body     = models.TextField()
    status   = models.CharField(max_length=1, choices=STATUS, default='D')
    created  = models.DateTimeField(auto_now_add=True)
    author   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    class Meta: ordering = ['-created']
```
**Signature pieces:**
```python
# URLs by slug (SEO — Topic 4.2 converters)
path('post/<slug:slug>/', PostDetailView.as_view(), name='detail')

# CreateView stamps the author — THE form_valid pattern ⭐
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post; fields = ['title', 'slug', 'body', 'category', 'status']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Author-only editing
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    ...
    def test_func(self):
        return self.get_object().author == self.request.user

# Comment posting lives inside PostDetail (FBV) or a small FBV:
@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug, status='P')
    form = CommentForm(request.POST)
    if form.is_valid():
        c = form.save(commit=False); c.post = post; c.user = request.user; c.save()
    return redirect('blog:detail', slug=slug)
```
**Lists:** published-only (`get_queryset → filter(status='P')`), category page (`filter(category__slug=…)`), author dashboard ("my posts incl. drafts"). **Admin:** prepopulated_fields={'slug': ('title',)}, list_filter status/category, comments inline under posts. **Templates:** index cards with `truncatewords:30`, detail + comment list + form.
**Steps:** models+admin → public list/detail → auth reuse → create/edit with stamping & guards → comments → category pages → drafts dashboard.

---

## 🛒 PROJECT 4 — E-Commerce Mini Store (blueprint)

**Requirements:** product catalog with images & categories, **session-based cart** (no purchase DB rows needed to start), checkout creating Orders, auth, product image uploads. *New muscles:* sessions as data store, order snapshotting, money = DecimalField.
**Database design:**
```
 Category(1)──<(N) Product : name, slug, price DECIMAL(8,2), image, stock, available
 User(1)──<(N) Order(1)──<(N) OrderItem(N)>──(1) Product
 Order: user FK, created, total DECIMAL, status(choices)
 OrderItem: order FK, product FK, qty, price_at_purchase  ⭐ snapshot!
```
**The session cart (Topic 4.7.5 cashing in):**
```python
def cart_add(request, pid):
    cart = request.session.get('cart', {})          # {product_id: qty}
    cart[str(pid)] = cart.get(str(pid), 0) + 1
    request.session['cart'] = cart                  # reassign → session saved
    return redirect('store:cart')

def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    items = [{'p': p, 'qty': cart[str(p.id)],
              'line': p.price * cart[str(p.id)]} for p in products]
    total = sum(i['line'] for i in items)
    return render(request, 'store/cart.html', {'items': items, 'total': total})

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if request.method == 'POST' and cart:
        order = Order.objects.create(user=request.user, total=0)
        total = 0
        for p in Product.objects.filter(id__in=cart.keys()):
            qty = cart[str(p.id)]
            OrderItem.objects.create(order=order, product=p, qty=qty,
                                     price_at_purchase=p.price)   # snapshot
            total += p.price * qty
        order.total = total; order.save()
        request.session['cart'] = {}                # empty the cart
        return redirect('store:order_done', pk=order.pk)
    ...
```
**Why snapshot price?** prices change; an order must remember what was actually paid (real-world data-integrity thinking — examiners love this point). **Rest of the build:** Product List/Detail generics with category filter + image cards (Module 3 grid!), "My orders" ListView filtered to request.user, admin with OrderItem inlines + stock list_editable.
**Steps:** catalog models+admin+seed → public catalog → session cart (add/remove/view) → auth → checkout → my-orders → polish (badges with cart count via context processor — stretch).

---

## 💼 PROJECT 5 — Job Portal (blueprint)

**Requirements:** two user roles (recruiter posts jobs, candidate applies with **resume upload**), application tracking with statuses, search/filter by location & type, dashboards per role. *New muscles:* role pattern via Profile, FileField validators in anger, unique_together (one application per job per user), role-gated mixins.
**Database design:**
```
 User(1)──(1) Profile(role: 'R'/'C', phone)
 User(R)(1)──<(N) Job : title, company, location, jtype(choices), salary, description, posted, active
 Job(1)──<(N) Application(N)>──(1) User(C)
 Application: job FK, candidate FK, resume FileField(pdf≤2MB), cover_note, status(choices A/S/R), applied
 Meta: unique_together = ('job', 'candidate')   ⭐ no duplicate applications
```
**Signature pieces:**
```python
class Application(models.Model):
    STATUS = [('A', 'Applied'), ('S', 'Shortlisted'), ('R', 'Rejected')]
    job       = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    resume    = models.FileField(upload_to='resumes/%Y/%m/',
                 validators=[FileExtensionValidator(['pdf']), validate_size])
    status    = models.CharField(max_length=1, choices=STATUS, default='A')
    class Meta: unique_together = ('job', 'candidate')

class RecruiterRequiredMixin(UserPassesTestMixin):          # role gate, reused
    def test_func(self):
        return self.request.user.profile.role == 'R'
```
- Candidate flow: job ListView (search `Q(title|company|location)` + jtype filter) → DetailView → apply FBV (multipart! duplicate-catch via IntegrityError) → "My applications" with status badges.
- Recruiter flow: JobCreate/Update (RecruiterRequiredMixin, form_valid stamps recruiter) → "Applicants" ListView per job (own jobs only!) → status-update view (POST changing Application.status).
- **Admin:** Job list_filter (jtype, location, active); Application list_display with status, list_editable status, resume link column via format_html.
**Steps:** Profile+role registration (two register buttons setting role) → job CRUD for recruiters → public search/list/detail → application with upload+validators+unique guard → both dashboards → status workflow → permission test matrix (the demo that wins vivas: log in as each role and show the walls).

---

## 🚀 Deployment Preparation (applies to all five — concept level)

**The dev→production checklist:**
```
1 SECRETS    SECRET_KEY & DB passwords → environment variables (never in Git)
2 DEBUG      DEBUG = False  +  ALLOWED_HOSTS = ['yourdomain.com']
3 DATABASE   SQLite → PostgreSQL/MySQL (swap the DATABASES block; Module 2 returns!)
4 STATIC     python manage.py collectstatic → one folder; served by WhiteNoise/Nginx
5 MEDIA      user uploads → Nginx-served folder or S3 (django-storages)
6 SERVER     runserver is DEV-ONLY → Gunicorn/uWSGI (the wsgi.py door!) behind Nginx
7 HTTPS      certificate (Let's Encrypt); SECURE_SSL_REDIRECT, secure cookies
8 FREEZE     pip freeze > requirements.txt; migrations committed; createsuperuser on server
9 CHECK      python manage.py check --deploy  ← Django's own production audit ⭐
```
```
 BROWSER ⇄ NGINX (HTTPS, static/, media/) ⇄ GUNICORN (N workers) ⇄ DJANGO ⇄ PostgreSQL
```
Hosting for students: **PythonAnywhere** (gentlest), **Railway/Render** (git-push deploys) — any of the five projects deploys in an evening; the §11 deployment overview goes deeper.

### 📈 Capstone Ladder Recap
| # | Project | New architectural muscle |
|---|---------|--------------------------|
| 1 | Student MS | the full canonical stack, search+pagination |
| 2 | Library | multi-FK domain, business-logic views, F-atomic stock |
| 3 | Blog | slugs, author stamping, ownership guards, comments |
| 4 | Mini Store | session cart, order snapshots, money fields |
| 5 | Job Portal | roles via Profile, gated dashboards, validated uploads, unique_together |

---
---
# §11. FINAL MODULE SECTION — SUMMARY, CHEAT SHEETS & PREPARATION GUIDES

## 11.1 Complete Module Summary

| Topic | Core Idea | Must-Know Keywords |
|-------|-----------|---------------------|
| 4.1 Setup | MVT framework, batteries included | venv, startproject/startapp, INSTALLED_APPS, runserver, manage.py/settings.py |
| 4.2 Routing & Views | URL → view → response | path(), converters, include, request.GET/POST, render(context), named URLs |
| 4.3 Templates | dynamic HTML, DRY layouts | {{ }}, {% if/for %}, filters, extends/block, include, {% static %} |
| 4.4 Models & ORM | Python classes ⇄ tables | fields, FK/O2O/M2M, makemigrations/migrate, filter/get, lookups, annotate, Q/F, select_related |
| 4.5 Forms | safe user input | Form vs ModelForm, is_valid/cleaned_data, widgets, clean_x/clean, csrf_token, PRG |
| 4.6 Admin | free back office | register, ModelAdmin options, inlines, actions, is_staff, groups |
| 4.7 Auth | who + what | User, authenticate/login/logout, sessions, @login_required, hashing+salt |
| 4.8 CBV | declarative CRUD | as_view, 5 generics, success_url/reverse_lazy, mixins, MRO, form_valid |
| 4.9 Media | user uploads | MEDIA_ROOT/URL, Image/FileField, Pillow, multipart+request.FILES, validators |
| §10 Capstones | 5 complete apps | the ladder: SMS → Library → Blog → Store → Job Portal |

## 11.2 Complete Request–Response Lifecycle Diagram ⭐ (the one-page Django)
```
 BROWSER ── GET /students/5/?ref=mail  (+ Cookie: sessionid=…) ──────────────┐
                                                                             ▼
 ┌─ DJANGO ───────────────────────────────────────────────────────────────────┐
 │ ① WSGI/ASGI entry (wsgi.py)                                                │
 │ ② MIDDLEWARE stack (in order): Security → Session(loads request.session)   │
 │      → CSRF (verifies POSTs) → Authentication(sets request.user) → …       │
 │ ③ URL DISPATCHER: project urls.py ─include→ students/urls.py               │
 │      '<int:pk>/' matches → StudentDetailView.as_view()                      │
 │ ④ VIEW: dispatch() → mixin gates (login? perms?) → get()                    │
 │ ⑤ MODEL/ORM: Student.objects.select_related(...).get(pk=5)                  │
 │      → SQL → DATABASE → row → Python object                                 │
 │ ⑥ TEMPLATE ENGINE: detail.html + context → blocks filled, vars escaped      │
 │ ⑦ HttpResponse(html) → middleware (response phase, reverse order) → out    │
 └──────────────────────────────────────────────────────────────────────────────┘
                                                                             │
 BROWSER ◀── 200 OK + HTML ── renders (Module 3 takes over) ◀────────────────┘
 (errors: no URL match → 404 • gate fails → 302 to login / 403 • view crash → 500)
```

## 11.3 Complete Django Mind Map
```
                              MODULE 4 — DJANGO
                                     │
   ┌──────────┬──────────┬──────────┼──────────┬──────────┬──────────┐
   ▼          ▼          ▼          ▼          ▼          ▼          ▼
 SETUP     ROUTING    TEMPLATES   MODELS     FORMS      ADMIN      AUTH
 venv      path()     {{ var }}   fields     Form/      register   authenticate
 start-    <int:pk>   {%if for%}  FK O2O     ModelForm  ModelAdmin login/logout
 project   include    filters     M2M        is_valid   list_*     sessions
 startapp  names+     extends/    migrate    cleaned_   inlines    @login_
 INSTALLED reverse    block       QuerySet   data       actions    required
 _APPS     request.   {%static%}  lookups    widgets    groups     hashing
 runserver GET/POST   custom      Q F        clean_x    is_staff   perms
                      filters     annotate   csrf                  reset
   ┌─────────┴───────────┐  select_related        │
   ▼                     ▼                        ▼
  CBV                  MEDIA                 CAPSTONES
  as_view()            MEDIA_ROOT/URL        1 Student MS (full)
  List/Detail/         Image/FileField      2 Library   3 Blog
  Create/Update/       Pillow, multipart,    4 Store     5 Job Portal
  Delete + mixins      request.FILES,        + deployment checklist
  reverse_lazy, MRO    validators, resize
```

## 11.4 Django Cheat Sheet 📄 (commands & files)
```
SETUP   python -m venv env • activate • pip install django pillow
        django-admin startproject campushub • python manage.py startapp students
        settings.py: INSTALLED_APPS += ['students'], TEMPLATES DIRS, STATIC/MEDIA
RUN     python manage.py runserver [port] • shell • check --deploy
DB      makemigrations • migrate • sqlmigrate app 0001 • showmigrations
ADMIN   createsuperuser → /admin/
FLOW    URL(urls.py) → VIEW(views.py) → MODEL(models.py) → TEMPLATE(.html) → Response
FILES   manage.py(commands) settings.py(config) urls.py(routes) wsgi/asgi(deploy doors)
        app: models/views/forms/admin/urls/templates/app//migrations
```

## 11.5 URL Routing Cheat Sheet
```python
# project urls.py
path('admin/', admin.site.urls)
path('students/', include('students.urls'))
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# app urls.py            app_name = 'students'
path('', views.index, name='index')
path('<int:pk>/', views.detail, name='detail')        # int str slug uuid path
path('add/', views.StudentCreateView.as_view(), name='add')
# linking
{% url 'students:detail' s.pk %} • reverse('students:index') • reverse_lazy (class attrs)
redirect('students:index')  • get_object_or_404(Student, pk=pk)
# view essentials
request.method GET POST • request.GET.get('q','') • request.POST • request.FILES
request.user • request.session • render(request,'app/t.html',{'k':v}) • HttpResponse
```

## 11.6 ORM Cheat Sheet 📄
```python
# CRUD
Student.objects.create(...)  /  s = Student(...); s.save()
Student.objects.all() • .filter(...) • .exclude(...) • .get(pk=1)  # raises!
.order_by('-marks','name') • [:3] • .count() .exists() .first()
qs.update(field=val) • s.save() • s.delete() • qs.delete()
# LOOKUPS  field__lookup
exact iexact contains icontains startswith endswith gt gte lt lte
in range isnull year month day • SPAN: filter(department__name='CSE')  # auto JOIN
# AGGREGATION
from django.db.models import Avg,Max,Min,Sum,Count,Q,F
.aggregate(avg=Avg('marks'))                    # one dict
.annotate(n=Count('students')).filter(n__gte=2) # GROUP BY + HAVING
# Q / F
.filter(Q(a=1) | Q(b=2)) • ~Q(...) • .update(marks=F('marks')+5)  # atomic
# OPTIMIZE
.select_related('fk') (JOIN) • .prefetch_related('m2m') • print(qs.query)
# FIELDS  CharField(max_length) TextField Integer/Decimal(max_digits,decimal_places)
# Boolean Date(auto_now_add|auto_now) Email Image(upload_to)+Pillow File
# ForeignKey(M, on_delete=CASCADE|PROTECT|SET_NULL, related_name=) OneToOne M2M
# null(DB) vs blank(form) • choices • unique • Meta: ordering
# MIGRATE  makemigrations → migrate    (recipe → cook)
```

## 11.7 Forms Cheat Sheet 📄
```python
class XForm(forms.Form): name = forms.CharField(max_length=50)
class SForm(forms.ModelForm):
    class Meta: model=Student; fields=[...]; widgets={'name':forms.TextInput(
        attrs={'class':'form-control'})}
    def clean_email(self): v=self.cleaned_data['email']; ...; return v
    def clean(self): c=super().clean(); ...; return c
# THE VIEW PATTERN
form = SForm(request.POST or None, request.FILES or None, instance=obj_or_None)
if form.is_valid(): form.save(); return redirect(...)        # PRG!
return render(request,'form.html',{'form':form})
# TEMPLATE
<form method="post" enctype="multipart/form-data"> {% csrf_token %}
{{ form.as_p }} • manual: {{ form.f }} {{ form.f.errors }} {{ form.non_field_errors }}
# commit=False → stamp fields → save():  obj=form.save(commit=False); obj.user=request.user; obj.save()
```

## 11.8 Authentication Cheat Sheet 📄
```python
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
user = authenticate(request, username=u, password=p)   # None on failure
login(request, user) • logout(request) • request.user.is_authenticated
@login_required(login_url=…) / settings.LOGIN_URL • ?next= auto-return
user.has_perm('app.change_model') • {% if perms.app.change_model %}
Groups = roles • is_staff(admin door) is_superuser(all) is_active
Passwords: PBKDF2+salt, one-way; UserCreationForm.save() hashes
Sessions: request.session['k']=v • sessionid cookie • django_session table
Built-ins: LoginView/LogoutView, PasswordChange/Reset views (console email in dev)
```

## 11.9 Admin Panel Cheat Sheet 📄
```python
# admin.py
admin.site.register(Model)                      # minimal
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display=('roll','name','department','marks')   # + methods
    search_fields=('name','department__name')           # FK spanning
    list_filter=('department','is_active') • ordering=('-marks',)
    list_editable=('marks',) • list_per_page=25
    fieldsets=(('Group',{'fields':(…),'classes':('collapse',)}),)
    readonly_fields • prepopulated_fields={'slug':('title',)} • date_hierarchy
class ChildInline(admin.TabularInline): model=Child; extra=1   # → inlines=[...]
@admin.action(description="…")
def act(modeladmin, request, queryset): queryset.update(...)   # → actions=[act]
# users: createsuperuser • is_staff to enter • 4 perms/model • groups=roles
```

## 11.10 CBV vs FBV Comparison Guide
| Situation | Choose | Because |
|-----------|--------|---------|
| Standard list/detail/CRUD | **CBV generics** | 3 attributes replace 30 lines |
| Pagination, common patterns | CBV | paginate_by etc. built in |
| One-off custom flow (issue_book, checkout) | **FBV** | logic visible top-to-bottom |
| Many similar views | CBV + base class | inheritance kills duplication |
| Teaching/debugging beginners | FBV first | nothing hidden |
| Auth gating | parity | @login_required ↔ LoginRequiredMixin |
**Translation table:** fetch list↔ListView • get_object_or_404+render↔DetailView • form GET/POST dance↔Create/UpdateView • confirm+delete↔DeleteView • method if/else↔get()/post() • decorator↔mixin (listed first!) • reverse↔reverse_lazy.

## 11.11 Django Security Guide 🔒
| Threat | Attack in one line | Django's shield | Your duty |
|--------|--------------------|------------------|-----------|
| SQL injection | input becomes SQL | ORM parameterizes | avoid raw(); if used, params=[] |
| XSS | input becomes script in pages | template auto-escaping | use `|safe` only on trusted content |
| CSRF | other site posts as you | token middleware | {% csrf_token %} everywhere |
| Password theft | DB leak exposes logins | PBKDF2+salt hashing | never store/log plaintext |
| Session hijack | stolen cookie = identity | secure session machinery | HTTPS + SECURE cookies in prod |
| Clickjacking | site framed invisibly | X-Frame-Options middleware | keep it enabled |
| Hostile uploads | exe disguised as pdf | nothing automatic! | whitelist+size+content checks (4.9) |
| Info leakage | tracebacks to users | DEBUG=False | + ALLOWED_HOSTS, env-var secrets |
Final word: run `python manage.py check --deploy` before any launch.

## 11.12 Django Project Structure Guide 🏗
```
project/
├── manage.py • requirements.txt • .gitignore(env/, db.sqlite3, media/)
├── project/  settings.py urls.py wsgi.py asgi.py
├── app1/, app2/ …   each: models forms views urls admin templates/app/ migrations
├── templates/ base.html _navbar.html      (project-wide; DIRS in settings)
├── static/ css/ js/ images/               (yours)
└── media/                                  (users'; never in Git)
```
Conventions: one feature = one app • app templates double-folder • per-app urls.py + namespaces • fat models/forms, thin views • settings split (base/dev/prod) at scale • migrations committed, db.sqlite3 not.

## 11.13 Production Deployment Overview 🚀
The §10 checklist is the practice; the architecture is the theory:
```
 Internet ⇄ NGINX (TLS, static/, media/, reverse proxy)
          ⇄ GUNICORN (3–5 workers running Django via wsgi.py)
          ⇄ PostgreSQL/MySQL (managed DB) • media → S3 at scale
```
Pipeline: env vars (SECRET_KEY, DB creds, DEBUG=False) → pip install -r requirements.txt → migrate → collectstatic → createsuperuser → gunicorn project.wsgi → Nginx config → HTTPS (Let's Encrypt) → monitor logs. Student-friendly hosts: PythonAnywhere, Railway, Render. Buzzwords to recognize: WhiteNoise (static without Nginx), django-environ (env files), CI/CD (auto-deploy on git push), Docker (containerized parity).

## 11.14 Beginner Mistakes Checklist ✅
**Setup:** ❑ venv not activated ❑ app missing from INSTALLED_APPS ❑ wrong directory for manage.py.
**Routing/Views:** ❑ trailing-slash mismatches ❑ generic pattern above specific ❑ hard-coded URLs ❑ missing .as_view() ❑ converter/parameter name mismatch.
**Templates:** ❑ single-folder template path ❑ extends not first line ❑ {% load static %} forgotten ❑ logic stuffed into templates.
**ORM:** ❑ makemigrations without migrate (or vice versa) ❑ get() for maybe-absent rows ❑ Python comparison inside filter ❑ N+1 loops ❑ no __str__.
**Forms:** ❑ csrf_token missing (403) ❑ cleaned_data before is_valid ❑ instance= forgotten on edit ❑ no redirect after POST.
**Auth/Media:** ❑ password set without hashing ❑ login view itself @login_required ❑ enctype/request.FILES duo ❑ Pillow not installed ❑ media URLs not wired in dev.
**Deploy:** ❑ DEBUG=True live ❑ SECRET_KEY in Git ❑ runserver as production server ❑ collectstatic skipped.

```

## 11.15 Top 100 Django Interview Questions 🧠
**Architecture & setup (1–12):** 1. What is Django; why "batteries included"? 2. MVT vs MVC — full mapping. 3. Where is Django's controller? 4. Request–response lifecycle (with middleware). 5. Project vs app. 6. Role of settings.py / manage.py / wsgi vs asgi. 7. Why virtual environments + requirements.txt? 8. What happens on runserver? 9. DEBUG=True risks. 10. What is middleware; name four. 11. Django's design philosophies (DRY, explicit). 12. Name big Django deployments.
**Routing & views (13–24):** 13. How URL dispatching works (two levels, first match). 14. path converters — all five. 15. include() mechanics. 16. Named URLs/namespaces/reverse — why. 17. reverse vs reverse_lazy. 18. FBV anatomy: request in, response out. 19. request.GET vs POST vs FILES vs session. 20. render() internals. 21. redirect & the PRG pattern. 22. get_object_or_404. 23. How does Django produce 404/500? 24. Slug URLs and SEO.
**Templates (25–34):** 25. Template engine pipeline. 26. Variables' dot-resolution order. 27. Tags vs filters. 28. Inheritance: extends/block — the DRY case. 29. include vs extends. 30. Custom filter steps. 31. Auto-escaping & XSS; the safe filter risk. 32. Static files: settings, tag, collectstatic. 33. Why templates stay logic-light. 34. Context processors (concept).
**ORM & models (35–56):** 35. What is an ORM; injection safety. 36. Model→table mapping rules. 37. null vs blank. 38. auto_now vs auto_now_add. 39. on_delete options with use cases. 40. The three relationships + junction tables. 41. related_name purpose. 42. Migration workflow; why commit migrations. 43. QuerySet laziness. 44. filter vs get (exceptions!). 45. Field lookups — ten of them. 46. Relationship-spanning lookups = JOINs. 47. aggregate vs annotate. 48. HAVING equivalent. 49. Q objects (OR/NOT). 50. F expressions & race conditions. 51. N+1 + both fixes & when each. 52. update() vs save() trade-offs. 53. choices fields. 54. Meta options (ordering, unique_together). 55. How to see the SQL. 56. raw() — when and how safely.
**Forms (57–66):** 57. Form lifecycle & the canonical view. 58. Bound vs unbound. 59. cleaned_data typing. 60. ModelForm vs Form; Meta. 61. instance= for edits. 62. commit=False stamping. 63. Field vs widget; Bootstrap styling routes. 64. Validation ladder order. 65. CSRF: attack + token mechanics. 66. Why server-side validation regardless of HTML5.
**Admin & auth (67–84):** 67. Why admin is a differentiator. 68. ModelAdmin top options. 69. Inlines. 70. Custom actions. 71. is_staff vs is_superuser vs is_active. 72. Four model permissions; groups as roles. 73. AuthN vs AuthZ. 74. authenticate/login/logout trio. 75. Sessions & cookies vs statelessness. 76. Where session data lives. 77. @login_required + next. 78. permission_required & has_perm. 79. Password hashing: PBKDF2, salt, one-way. 80. UserCreationForm gifts. 81. Profile vs AbstractUser (+timing trap). 82. Password-reset token flow. 83. Login hardening (rate limit, generic errors, HTTPS cookies). 84. Logout-as-POST rationale.
**CBV & media (85–94):** 85. as_view/dispatch flow. 86. Five generics + their attributes. 87. get_queryset/get_context_data/form_valid hooks. 88. Mixins & MRO ordering. 89. FBV vs CBV decision framework. 90. Pagination via ListView. 91. Static vs media. 92. MEDIA settings + dev serving. 93. The multipart/request.FILES duo. 94. Upload security checklist.
**Production & misc (95–100):** 95. The deploy checklist (DEBUG, hosts, secrets, collectstatic). 96. Gunicorn+Nginx architecture. 97. check --deploy. 98. Django's shields per OWASP threat (the 11.11 table). 99. Signals (concept + example). 100. What is DRF and why it's your next step.

## 11.16 Top 100 Django Viva Questions 🎤 (rapid-fire with answers)
**1–20 basics:** 1. Django language? *(Python)* 2. MVT expansion. 3. T maps to MVC's? *(View)* 4. Open-source year? *(2005)* 5. Named after? *(Django Reinhardt)* 6. Create project cmd. 7. Create app cmd. 8. Register apps where? *(INSTALLED_APPS)* 9. Default port? *(8000)* 10. Config file? *(settings.py)* 11. Command runner file? *(manage.py)* 12. DRY = ? 13. Deployment door file? *(wsgi.py)* 14. venv create cmd. 15. Dev server cmd. 16. Project:app analogy answer? *(mall:shops)* 17. First page seen? *(rocket)* 18. Auto-reload feature name? *(StatReloader)* 19. DEBUG production value? *(False)* 20. Framework's controller? *(Django+urls.py)*
**21–40 routing/templates:** 21. Function mapping URLs? *(path)* 22. Delegating function? *(include)* 23. `<int:pk>` passes type? *(int)* 24. Slug allows? *(letters digits - _)* 25. View's first param? *(request)* 26. Query params dict? *(request.GET)* 27. Template renderer shortcut? *(render)* 28. Context type? *(dict)* 29. URL-from-name tag? *({% url %})* 30. Python reverse function? *(reverse)* 31. Variable syntax? *({{ }})* 32. Tag syntax? *({% %})* 33. Child's first line? *(extends)* 34. Hole tag? *(block)* 35. Empty-loop tag? *({% empty %})* 36. 1-based counter? *(forloop.counter)* 37. Date filter example? *(date:"d M Y")* 38. Static loader? *({% load static %})* 39. Template folder rule? *(app/templates/app/)* 40. Escaping prevents? *(XSS)*
**41–60 ORM:** 41. ORM expansion. 42. Model base class? *(models.Model)* 43. CharField needs? *(max_length)* 44. Long text field? *(TextField)* 45. FK mandatory arg? *(on_delete)* 46. M2M table? *(auto junction)* 47. Recipe cmd? *(makemigrations)* 48. Cook cmd? *(migrate)* 49. Default manager? *(objects)* 50. All rows? *(.all())* 51. May-be-empty fetch? *(filter)* 52. Exactly-one fetch? *(get)* 53. get() empty raises? *(DoesNotExist)* 54. >= lookup? *(__gte)* 55. Case-insensitive contains? *(__icontains)* 56. DESC order syntax? *(order_by('-f'))* 57. One-dict summary? *(aggregate)* 58. Per-row summary? *(annotate)* 59. OR helper? *(Q)* 60. Column-math helper? *(F)*
**61–80 forms/admin/auth:** 61. Validation trigger? *(is_valid())* 62. Clean data attr? *(cleaned_data)* 63. Model-tied form? *(ModelForm)* 64. Edit binder kwarg? *(instance)* 65. HTML of a field? *(widget)* 66. Field-cleaner naming? *(clean_<field>)* 67. CSRF tag? *({% csrf_token %})* 68. Missing token code? *(403)* 69. Admin URL? */admin/* 70. Admin account cmd? *(createsuperuser)* 71. Register where? *(admin.py)* 72. Columns option? *(list_display)* 73. Children-in-parent? *(inlines)* 74. Bulk dropdown? *(actions)* 75. Admin-door flag? *(is_staff)* 76. Credential checker? *(authenticate)* 77. Session writer? *(login)* 78. Logged-in test in template? *(user.is_authenticated)* 79. Guard decorator? *(@login_required)* 80. Hash algorithm? *(PBKDF2)*
**81–100 CBV/media/deploy:** 81. Class hookup method? *(.as_view())* 82. List generic pagination attr? *(paginate_by)* 83. Create redirect attr? *(success_url)* 84. Lazy resolver? *(reverse_lazy)* 85. Method router? *(dispatch)* 86. Mixin order rule? *(mixins first)* 87. Login mixin name? *(LoginRequiredMixin)* 88. Object-save hook? *(form_valid)* 89. Uploads disk setting? *(MEDIA_ROOT)* 90. Uploads URL setting? *(MEDIA_URL)* 91. Image library? *(Pillow)* 92. Form enctype? *(multipart/form-data)* 93. Files dict? *(request.FILES)* 94. Extension validator class? *(FileExtensionValidator)* 95. Static gather cmd? *(collectstatic)* 96. Prod app server? *(Gunicorn)* 97. Prod front server? *(Nginx)* 98. Deploy audit cmd? *(check --deploy)* 99. Allowed domains setting? *(ALLOWED_HOSTS)* 100. Next framework to learn? *(Django REST Framework)*

## 11.17 Top 100 Django MCQs 💯 (✓ = answer)
**Setup & architecture (1–20)**
1. Django is a ___ framework: a) frontend b) **backend web** ✓ c) mobile d) game
2. MVT's M: a) Module b) **Model** ✓ c) Method d) Main
3. Logic lives in: a) Template b) **View** ✓ c) Model d) urls
4. Project creator: a) startapp b) **django-admin startproject** ✓ c) new d) init
5. App creator: a) **python manage.py startapp** ✓ b) newapp c) startproject d) mkapp
6. Apps registered in: a) urls.py b) **settings.py** ✓ c) admin.py d) apps.py
7. Dev server command: a) **python manage.py runserver** ✓ b) start c) serve d) launch
8. Default DB: a) MySQL b) **SQLite** ✓ c) Postgres d) Oracle
9. wsgi.py is for: a) tests b) **deployment entry** ✓ c) styling d) routing
10. DRY = a) Don't Run Yet b) **Don't Repeat Yourself** ✓ c) Data Rules d) none
11. Django written at a: a) bank b) **newspaper** ✓ c) university d) game studio
12. manage.py is: a) edited often b) **a command-line utility** ✓ c) a model d) a view
13. (env) in prompt means: a) error b) **venv active** ✓ c) admin d) debug
14. DEBUG in production: a) True b) **False** ✓ c) 1 d) optional
15. Settings constant for domains: a) HOSTS b) **ALLOWED_HOSTS** ✓ c) DOMAINS d) SITES
16. MVC's controller ≈ Django's: a) Template b) **View(+urls)** ✓ c) Model d) Form
17. requirements.txt made by: a) pip list b) **pip freeze** ✓ c) pip save d) venv
18. Reusable unit: a) project b) **app** ✓ c) template d) view
19. First migrate creates: a) nothing b) **auth/session tables** ✓ c) your models only d) admin user
20. Lifecycle order: a) View→URL→Model b) **URL→View→Model→Template** ✓ c) Template first d) random
**Routing, views, templates (21–45)**
21. Capture int: a) (int) b) **<int:pk>** ✓ c) {int} d) [int]
22. Default converter: a) int b) **str** ✓ c) slug d) path
23. include() lives in: a) views b) **urls** ✓ c) models d) admin
24. First match wins scanning: a) bottom-up b) **top-down** ✓ c) longest d) alpha
25. Query string lives in: a) request.POST b) **request.GET** ✓ c) FILES d) body
26. render's 3rd arg: a) list b) **dict** ✓ c) str d) tuple
27. Page-not-found code: a) 403 b) **404** ✓ c) 500 d) 302
28. redirect returns code: a) 200 b) **302** ✓ c) 404 d) 418
29. Template variable: a) {% v %} b) **{{ v }}** ✓ c) ${v} d) ((v))
30. Loop close: a) {% end %} b) **{% endfor %}** ✓ c) {% done %} d) none
31. Inheritance tag: a) include b) **extends** ✓ c) import d) block
32. Override areas: a) zones b) **blocks** ✓ c) slots d) divs
33. Reusable fragment: a) extends b) **include** ✓ c) embed d) part
34. |length on "abcd": a) abcd b) **4** ✓ c) error d) "four"
35. Auto-escape stops: a) CSRF b) **XSS** ✓ c) SQLi d) DoS
36. {% static %} needs: a) settings only b) **{% load static %}** ✓ c) import d) nothing
37. Missing context var renders: a) crash b) **empty** ✓ c) None d) 0
38. Custom filters folder: a) filters/ b) **templatetags/** ✓ c) tags/ d) custom/
39. URL by name in template: a) {% link %} b) **{% url %}** ✓ c) {% path %} d) {% route %}
40. forloop.counter starts: a) 0 b) **1** ✓ c) -1 d) configurable
41. {% empty %} pairs with: a) if b) **for** ✓ c) block d) include
42. as_view() belongs to: a) FBV b) **CBV** ✓ c) forms d) admin
43. App templates path: a) templates/x.html b) **app/templates/app/x.html** ✓ c) static d) views
44. {% if %} closes with: a) {% fi %} b) **{% endif %}** ✓ c) {% end %} d) }} 
45. date:"Y" outputs: a) day b) **year** ✓ c) month d) time
**ORM (46–70)**
46. Model maps to: a) row b) **table** ✓ c) column d) DB
47. Row maps to: a) class b) **object/instance** ✓ c) field d) manager
48. CharField must set: a) null b) **max_length** ✓ c) default d) unique
49. Money field: a) Float b) **DecimalField** ✓ c) Integer d) Char
50. Set-once timestamp: a) auto_now b) **auto_now_add** ✓ c) default d) now()
51. FK requires: a) related_name b) **on_delete** ✓ c) null d) unique
52. Delete children too: a) PROTECT b) **CASCADE** ✓ c) SET_NULL d) IGNORE
53. M2M creates: a) nothing b) **junction table** ✓ c) view d) index
54. Recipe command: a) migrate b) **makemigrations** ✓ c) sqlmigrate d) sync
55. Apply command: a) makemigrations b) **migrate** ✓ c) apply d) push
56. Default manager: a) items b) **objects** ✓ c) rows d) query
57. QuerySets are: a) eager b) **lazy** ✓ c) cached forever d) strings
58. get() with 2 matches: a) first b) **MultipleObjectsReturned** ✓ c) list d) None
59. >= lookup: a) __ge b) **__gte** ✓ c) __min d) >=
60. LIKE '%x%' (any case): a) contains b) **icontains** ✓ c) iexact d) search
61. JOIN via lookup: a) join() b) **relation__field** ✓ c) raw d) merge
62. Whole-table average: a) annotate b) **aggregate** ✓ c) Avg alone d) group
63. GROUP BY analog: a) aggregate b) **annotate** ✓ c) order_by d) values only
64. OR queries need: a) F b) **Q** ✓ c) | on querysets only d) raw
65. Atomic increment: a) v+=1;save b) **F('v')+1** ✓ c) annotate d) signals
66. FK N+1 fix: a) prefetch_related b) **select_related** ✓ c) only d) defer
67. M2M N+1 fix: a) select_related b) **prefetch_related** ✓ c) raw d) cache
68. See SQL: a) qs.sql b) **qs.query** ✓ c) print(qs) d) explain only
69. null=True controls: a) forms b) **database** ✓ c) admin d) templates
70. Default ordering set in: a) admin b) **Meta** ✓ c) views d) urls
**Forms, admin, auth (71–90)**
71. Validation method: a) clean() call b) **is_valid()** ✓ c) save d) check
72. Valid data in: a) data b) **cleaned_data** ✓ c) POST d) fields
73. Model-driven form: a) Form b) **ModelForm** ✓ c) AdminForm d) AutoForm
74. Edit existing via: a) initial b) **instance=** ✓ c) pk= d) object=
75. Stamp before save: a) save(True) b) **save(commit=False)** ✓ c) pre_save d) clean
76. Field's HTML part: a) validator b) **widget** ✓ c) template d) tag
77. Single-field cleaner: a) validate_x b) **clean_x** ✓ c) check_x d) x_clean
78. CSRF protects against: a) injection b) **forged cross-site POSTs** ✓ c) XSS d) sniffing
79. Admin path: a) /panel b) **/admin/** ✓ c) /root d) /manage
80. Admin account: a) adduser b) **createsuperuser** ✓ c) newadmin d) signup
81. Columns option: a) fields b) **list_display** ✓ c) columns d) show
82. Sidebar filters: a) search_fields b) **list_filter** ✓ c) ordering d) facets
83. Children inline: a) actions b) **inlines** ✓ c) fieldsets d) nested
84. Admin login flag: a) is_superuser b) **is_staff** ✓ c) is_admin d) staff_only
85. Identity check fn: a) login b) **authenticate** ✓ c) verify d) check
86. Session creator: a) authenticate b) **login** ✓ c) start d) session()
87. Session data stored: a) cookie b) **server** ✓ c) JS d) URL
88. Guard decorator: a) @auth b) **@login_required** ✓ c) @protect d) @user
89. Passwords stored as: a) text b) **salted hash** ✓ c) base64 d) encrypted reversible
90. Roles via: a) flags b) **groups** ✓ c) cookies d) middleware
**CBV, media, deploy (91–100)**
91. URL hookup: a) View b) **View.as_view()** ✓ c) View() d) view.run
92. List pagination: a) page_size b) **paginate_by** ✓ c) limit d) chunk
93. Create redirect: a) next_url b) **success_url** ✓ c) goto d) after
94. Class-attr resolver: a) reverse b) **reverse_lazy** ✓ c) url c) resolve
95. Mixin position: a) last b) **before the generic** ✓ c) anywhere d) inside Meta
96. Uploads dict: a) request.POST b) **request.FILES** ✓ c) request.GET d) request.media
97. Upload form needs enctype: a) urlencoded b) **multipart/form-data** ✓ c) json d) text
98. ImageField needs: a) NumPy b) **Pillow** ✓ c) OpenCV d) GD
99. Static gather: a) gatherstatic b) **collectstatic** ✓ c) buildstatic d) pack
100. Production server pair: a) runserver+Apache b) **Gunicorn+Nginx** ✓ c) IIS only d) shell

---
