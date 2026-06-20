import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campushub.settings')
django.setup()

from students.models import Department

departments = [
    {
        "code": "CIVIL",
        "name": "Civil Engineering",
        "description": "The Department of Civil Engineering at MTIET offers a comprehensive program that covers structural engineering, geotechnical engineering, transportation engineering, and environmental engineering. Students gain hands-on experience through state-of-the-art laboratories and industry internships. The department is equipped with modern computing facilities and testing equipment to train students in design, construction, and maintenance of infrastructure projects. Career opportunities include roles in construction firms, government agencies, consulting firms, and research organizations.",
        "image_url": "https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=400&h=250&fit=crop"
    },
    {
        "code": "EEE",
        "name": "Electrical & Electronics Engineering",
        "description": "The Department of Electrical & Electronics Engineering at MTIET provides a strong foundation in electrical circuits, power systems, control systems, and electronics. The curriculum is designed to meet the evolving needs of the power sector and industrial automation. Students have access to well-equipped laboratories including Power Systems Lab, Control Systems Lab, Electrical Machines Lab, and Microprocessors Lab. Graduates find excellent career prospects in power generation companies, manufacturing industries, automation firms, and research institutions.",
        "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=400&h=250&fit=crop"
    },
    {
        "code": "ECE",
        "name": "Electronics & Communication Engineering",
        "description": "The Department of Electronics & Communication Engineering at MTIET offers cutting-edge education in electronics, communication systems, signal processing, VLSI design, and embedded systems. The department boasts advanced laboratories such as Digital Signal Processing Lab, Communication Systems Lab, VLSI Design Lab, and Embedded Systems Lab. Students are trained to meet the demands of the telecommunications, semiconductor, and consumer electronics industries. The department maintains strong industry collaborations for internships and placement opportunities.",
        "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=250&fit=crop"
    },
    {
        "code": "CSE",
        "name": "Computer Science & Engineering",
        "description": "The Department of Computer Science & Engineering at MTIET is at the forefront of computing education and research. The curriculum covers algorithms, data structures, programming languages, database systems, computer networks, and software engineering. Students have access to high-performance computing labs, AI/ML labs, and specialized research facilities. The department organizes hackathons, coding competitions, and technical workshops to foster innovation. Graduates have an excellent placement record with top technology companies and are well-prepared for entrepreneurial ventures.",
        "image_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400&h=250&fit=crop"
    },
    {
        "code": "SAH",
        "name": "Science & Humanities",
        "description": "The Department of Science & Humanities at MTIET provides fundamental education in Mathematics, Physics, Chemistry, and English to engineering students. The department plays a crucial role in building a strong scientific temperament and communication skills among students. Well-equipped physics and chemistry laboratories enable practical learning. The department also offers value-added courses in soft skills, aptitude training, and personality development to enhance employability. Dedicated faculty members ensure a strong foundation for advanced engineering studies.",
        "image_url": "https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=400&h=250&fit=crop"
    },
    {
        "code": "AI&DS",
        "name": "Artificial Intelligence & Data Science",
        "description": "The Department of Artificial Intelligence & Data Science at MTIET is a specialized program focused on AI, machine learning, deep learning, data analytics, and big data technologies. The curriculum includes Python programming, statistical modeling, neural networks, natural language processing, and computer vision. Students work on real-world projects using industry-standard tools and frameworks. The department has dedicated AI/ML labs with GPU-enabled workstations. This program prepares students for the rapidly growing AI and data science job market.",
        "image_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&h=250&fit=crop"
    },
    {
        "code": "CSE(DS)",
        "name": "Computer Science (Data Science)",
        "description": "The Department of Computer Science (Data Science) at MTIET is designed for students who want to specialize in data-driven computing. The program covers core computer science concepts along with specialized courses in data mining, data visualization, statistical analysis, and database technologies. Students gain proficiency in tools like Python, R, SQL, Tableau, and Hadoop. The curriculum emphasizes practical learning through capstone projects and industry internships. Graduates are well-suited for roles as data scientists, data analysts, and data engineers.",
        "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=250&fit=crop"
    },
    {
        "code": "CSE(AI)",
        "name": "Computer Science (Artificial Intelligence)",
        "description": "The Department of Computer Science (Artificial Intelligence) at MTIET offers an intensive program blending core computer science with AI specialization. Students study intelligent systems, robotics, expert systems, fuzzy logic, and cognitive science alongside traditional CS fundamentals. The department features state-of-the-art AI research labs and robotics facilities. Students participate in AI competitions, research projects, and industry-sponsored challenges. This program creates AI specialists capable of developing intelligent solutions across various domains.",
        "image_url": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=400&h=250&fit=crop"
    },
    {
        "code": "MECH",
        "name": "Mechanical Engineering",
        "description": "The Department of Mechanical Engineering at MTIET provides a robust education in thermal engineering, design, manufacturing, and industrial engineering. The department is equipped with modern laboratories including CAD/CAM Lab, Thermodynamics Lab, Fluid Mechanics Lab, Strength of Materials Lab, and Metrology Lab. Students are trained in both theoretical concepts and practical applications using industry-standard software and equipment. The program prepares graduates for careers in automotive, aerospace, manufacturing, and energy sectors with strong placement support.",
        "image_url": "https://images.unsplash.com/photo-1565106431045-5cb6de9d7a2d?w=400&h=250&fit=crop"
    },
]

dept_map = {d.code: d for d in Department.objects.all()}
new_count = 0
update_count = 0
for d in departments:
    obj, created = Department.objects.update_or_create(
        code=d["code"],
        defaults={
            "name": d["name"],
            "description": d["description"],
            "image_url": d["image_url"],
        }
    )
    if created:
        new_count += 1
    else:
        update_count += 1

print(f"Departments: {new_count} created, {update_count} updated. Total: {Department.objects.count()}")
