"""Seed data taken directly from the Career Development Plan (November 2026).

Every row here is transcription of the source plan. Nothing is invented:
where the plan does not state a value, the field is left blank so the owner
can fill it in.
"""

from __future__ import annotations

from . import db

SETTINGS: dict[str, str] = {
    "owner_name": "Valentin Zirimwabagabo",
    "owner_initials": "VZ",
    "headline": (
        "Building a career in software development, applied AI, and technology "
        "for social impact."
    ),
    "plan_title": "Career Development Plan",
    "plan_version": "November 2026",
    "plan_start": "2026-11-01",
    "current_focus": (
        "Transitioning from university to professional practice, strengthening "
        "technical skills, and building a sustainable career."
    ),
    "about": (
        "I am an Applied Computer Technology graduate in transition to professional "
        "practice. My interests span software development, IT systems, data analysis, "
        "and applied artificial intelligence.\n\n"
        "I enjoy learning by building practical solutions and understanding how "
        "technology can address real problems. My experience in community projects and "
        "entrepreneurship has also helped me appreciate that successful technology is "
        "not only about writing code. It must respond to people's needs and work within "
        "their circumstances."
    ),
    "aspiration": (
        "To become a skilled technology professional who builds reliable, useful digital "
        "products, develops expertise in applied AI and data-driven systems, and "
        "eventually leads technology initiatives that create opportunities for "
        "underserved communities."
    ),
    "next_roles": "\n".join(
        [
            "Junior Software Developer",
            "Full-Stack Developer",
            "Junior Automation or Applied AI Developer",
            "IT Systems or Technical Support Specialist",
            "Junior Data Analyst, as my analytical skills develop",
        ]
    ),
    "long_term_direction": (
        "Technical leadership, technology entrepreneurship, and further postgraduate "
        "study where appropriate."
    ),
    "growth_mindset": (
        "My academic foundation and practical experience give me a starting point. My "
        "next task is to turn that foundation into demonstrable technical ability, "
        "professional experience, and stronger judgement."
    ),
    "alternative_paths": (
        "Data analysis, IT infrastructure, technical implementation, and product-focused "
        "software development."
    ),
    "alternative_paths_caveat": (
        "These are target pathways rather than guaranteed promotions. The direction will "
        "be reviewed against actual opportunities, performance, and interests."
    ),
    "review_cadence": "Monthly, with a more detailed review every three months.",
    "my_responsibility": (
        "Seek feedback, act on it, communicate progress, and remain accountable for my "
        "development."
    ),
    "closing_statement": (
        "I have spent years working toward an education and building a foundation in "
        "technology. My next challenge is to turn that foundation into professional "
        "experience, deeper technical ability, and work that creates practical value.\n\n"
        "I do not expect to master everything at once. I want to keep learning, build "
        "things that work, learn from people with more experience, and become someone "
        "others can trust to solve problems.\n\n"
        "My long-term ambition is to use technology not only to build a career for "
        "myself, but also to create opportunities and solutions that benefit other "
        "people."
    ),
    "commitment": (
        "Build consistently, learn honestly, seek feedback, and measure progress through "
        "what I can demonstrate."
    ),
    "academic_note": (
        "Add specific dates, deliverables, and verified outcomes where you have evidence. "
        "Do not claim that a project or initiative is completed if it is still ongoing."
    ),
}

JOURNEY = [
    (
        "2015 onwards",
        "Adapting and continuing my education",
        "Continued pursuing education despite displacement and difficult circumstances. "
        "Developed resilience, independence, and a strong sense of responsibility. "
        "Maintained an interest in technology as a way to solve practical problems.",
        "Resilience",
    ),
    (
        "University years",
        "USIU-Africa",
        "Pursued a Bachelor of Science in Applied Computer Technology. Developed "
        "foundations in programming, computer systems, networking, and software "
        "development. Earned Dean's List recognition in multiple semesters.",
        "Foundation",
    ),
    (
        "Practical experience",
        "Projects and community initiatives",
        "Completed an internship with The Result Consultancy Ltd in Kigali. Explored "
        "networking infrastructure, Linux systems, virtualisation, and web development. "
        "Contributed to community initiatives focused on digital skills and youth "
        "empowerment.",
        "Application",
    ),
    (
        "Entrepreneurship",
        "Turashoboye Feeds Ltd",
        "Co-founded a business addressing access to animal feed for farmers in Mahama "
        "Refugee Camp. Developed an interest in understanding customer needs, business "
        "processes, and sustainable growth. Began exploring how digital tools could "
        "improve business operations.",
        "Venture",
    ),
    (
        "Current stage",
        "November 2026",
        "Completed university coursework and progressed to academic attachment. Preparing "
        "for professional opportunities while developing skills in Python, SQL, data "
        "analysis, and applied AI. Exploring suitable fully funded postgraduate "
        "opportunities.",
        "Transition",
    ),
]

STRENGTHS = [
    ("Strength", "Initiative and independent learning", 3, 5),
    ("Strength", "Foundation in computer technology", 3, 5),
    ("Strength", "Exposure to networking and Linux systems", 3, 5),
    ("Strength", "Community leadership and project coordination", 3, 5),
    ("Strength", "Entrepreneurial thinking and customer awareness", 3, 5),
    ("Strength", "Persistence and adaptability", 3, 5),
    ("Development area", "Deeper software engineering practice", 2, 4),
    ("Development area", "Advanced Python and data analysis", 2, 4),
    ("Development area", "Software testing and deployment", 2, 4),
    ("Development area", "Technical communication and interviews", 2, 4),
    ("Development area", "Production-level security and system design", 2, 4),
    ("Development area", "Focused career planning and consistent execution", 2, 5),
]

EXPERIENCES = [
    {
        "category": "Academic",
        "title": "Bachelor of Science in Applied Computer Technology — USIU-Africa",
        "description": "CGPA of 3.368 according to the latest reported academic update. "
        "Dean's List recognition in Spring 2023, Summer 2024, and Fall 2024.",
        "status": "Completed",
        "verified": 1,
    },
    {
        "category": "Academic",
        "title": "Academic attachment / professional practice",
        "description": "Completed university coursework and progressed to academic "
        "attachment as of November 2026.",
        "status": "Ongoing",
        "verified": 0,
    },
    {
        "category": "Professional",
        "title": "Research internship — The Result Consultancy Ltd, Kigali",
        "description": "Explored networking infrastructure, Linux systems, "
        "virtualisation, and web development.",
        "status": "Completed",
        "verified": 0,
    },
    {
        "category": "Project",
        "title": "Inter-university AI hackathon",
        "description": "Participated with an agritech crop-diagnosis concept.",
        "status": "Completed",
        "verified": 0,
    },
    {
        "category": "Entrepreneurship",
        "title": "Turashoboye Feeds Ltd",
        "description": "Co-founded a business serving livestock and poultry farmers in "
        "Mahama Refugee Camp. Contribute to thinking about customer needs, products, "
        "business strategy, and sustainable growth. Interested in using digital systems "
        "to improve inventory, sales, and business information management.",
        "status": "Ongoing",
        "verified": 0,
    },
    {
        "category": "Community",
        "title": "Mahama Tailoring Empowerment Project (M-TEP)",
        "description": "Lead a community initiative focused on tailoring skills and "
        "empowerment for refugee youth and young mothers. Support a model in which "
        "trained participants can pass their skills on to others. Develop practical "
        "experience in coordination, planning, and community engagement.",
        "status": "Ongoing",
        "verified": 0,
    },
    {
        "category": "Community",
        "title": "University and community activities",
        "description": "Involvement in university and community activities as part of "
        "the broader learning journey.",
        "status": "Ongoing",
        "verified": 0,
    },
]

ACTIONS_70_20_10 = [
    (
        "70 — Practice",
        "Complete and document a full-stack software project",
        "Learning through practical work",
    ),
    (
        "70 — Practice",
        "Build a Python project involving data analysis or automation",
        "Learning through practical work",
    ),
    (
        "70 — Practice",
        "Practise SQL through real datasets and progressively harder exercises",
        "Learning through practical work",
    ),
    (
        "70 — Practice",
        "Apply software testing, version control, deployment, and security practices",
        "Learning through practical work",
    ),
    (
        "70 — Practice",
        "Use portfolio projects to demonstrate skills to employers",
        "Learning through practical work",
    ),
    ("20 — People", "Seek guidance from an experienced developer or IT professional", "Learning from others"),
    ("20 — People", "Request feedback and code reviews on projects", "Learning from others"),
    ("20 — People", "Learn from lecturers, former supervisors, and professional peers", "Learning from others"),
    (
        "20 — People",
        "Practise explaining technical decisions and presenting project outcomes",
        "Learning from others",
    ),
    (
        "10 — Study",
        "Strengthen Python, SQL, data analysis, and software engineering fundamentals",
        "Structured learning",
    ),
    (
        "10 — Study",
        "Progress into supervised and unsupervised machine learning after building the foundations",
        "Structured learning",
    ),
    ("10 — Study", "Study APIs, authentication, database security, and deployment", "Structured learning"),
    (
        "10 — Study",
        "Select courses that address specific skill gaps rather than collecting "
        "certificates without practical application",
        "Structured learning",
    ),
]

CAREER_STAGES = [
    (
        "0–12 Months",
        "Stage 1: Entry into professional practice",
        "Target junior software development, IT systems, automation, or relevant "
        "internship opportunities. Focus on portfolio development, technical interviews, "
        "job applications, and practical experience.",
        "In progress",
    ),
    (
        "1–3 Years",
        "Stage 2: Develop professional depth",
        "Become a dependable developer or technical specialist who can build, maintain, "
        "test, and explain complete systems. Develop stronger teamwork, system design, "
        "security, and problem-solving skills.",
        "Not started",
    ),
    (
        "3–5+ Years",
        "Stage 3: Specialisation and leadership",
        "Develop deeper expertise in applied AI, data-enabled products, or software "
        "systems. Explore technical leadership, technology entrepreneurship, and a funded "
        "master's degree aligned with my goals.",
        "Not started",
    ),
]

SKILLS = [
    (
        "Software development",
        "Build a complete application",
        "Working demo, readable code, tests, documentation",
    ),
    (
        "Python and data",
        "Analyse a dataset and build a practical tool",
        "Reproducible analysis and clear findings",
    ),
    (
        "SQL and databases",
        "Practise querying and database design",
        "Correct queries, sound schema, reliable data handling",
    ),
    (
        "Security",
        "Apply authentication and access controls",
        "Appropriate permissions, secure secrets, validated inputs",
    ),
    (
        "Communication",
        "Present projects and explain technical decisions",
        "Clear demonstrations and stronger interview responses",
    ),
    (
        "Employability",
        "Tailor CV and portfolio to target roles",
        "Relevant applications, interviews, and actionable feedback",
    ),
]

GOALS = [
    (
        "Improve technical competence",
        "I can independently build, debug, test, and explain a small application.",
        "Technical",
    ),
    (
        "Develop an employable portfolio",
        "I have at least two well-documented projects demonstrating relevant skills.",
        "Portfolio",
    ),
    (
        "Gain professional experience",
        "I secure a suitable job, internship, contract, or meaningful practical assignment.",
        "Experience",
    ),
    (
        "Improve professional communication",
        "I can present my work clearly to technical and non-technical audiences.",
        "Communication",
    ),
    (
        "Strengthen professional relationships",
        "I have people who can provide honest feedback and speak to work they have "
        "observed.",
        "Network",
    ),
    (
        "Pursue further education strategically",
        "I identify suitable funded programmes and submit well-prepared applications when "
        "eligible.",
        "Education",
    ),
    (
        "Connect technology to impact",
        "I can show how a project responds to a real user or organisational need.",
        "Impact",
    ),
]

SUPPORT = [
    ("Technical mentor", "Guidance on software engineering practices, architecture, and career decisions."),
    (
        "Professional network",
        "Opportunities to learn from developers, data professionals, IT specialists, and "
        "technology entrepreneurs.",
    ),
    ("Career feedback", "Honest reviews of my CV, portfolio, applications, and interview performance."),
    (
        "Academic and professional referees",
        "People who know my work and can provide accurate recommendations.",
    ),
    (
        "Learning resources",
        "Access to documentation, development tools, structured training, and practical "
        "projects.",
    ),
    (
        "Personal sustainability",
        "A realistic schedule that accounts for financial responsibilities, job searching, "
        "and ongoing community commitments.",
    ),
]

FIRST_90 = [
    ("Days 1–30 — Direction and preparation", "Choose one primary job family."),
    (
        "Days 1–30 — Direction and preparation",
        "Review five relevant job descriptions and identify common requirements.",
    ),
    ("Days 1–30 — Direction and preparation", "Update my CV and professional portfolio."),
    (
        "Days 1–30 — Direction and preparation",
        "Select one project that demonstrates the skills employers request.",
    ),
    ("Days 31–60 — Building evidence", "Make meaningful progress on the selected project."),
    ("Days 31–60 — Building evidence", "Write documentation and test the main features."),
    ("Days 31–60 — Building evidence", "Ask someone knowledgeable to review the work."),
    ("Days 31–60 — Building evidence", "Practise technical questions and project explanations."),
    ("Days 61–90 — Applying and improving", "Publish the project when it is ready and safe to share."),
    ("Days 61–90 — Applying and improving", "Apply consistently to suitable opportunities."),
    ("Days 61–90 — Applying and improving", "Track applications, responses, and feedback."),
    (
        "Days 61–90 — Applying and improving",
        "Identify the next technical gap and revise the development plan.",
    ),
]


def _insert_rows(table: str, columns: list[str], rows: list[tuple]) -> None:
    if not rows:
        return
    placeholders = ", ".join("?" for _ in columns + ["sort_order", "updated_at"])
    with db.connect() as conn:
        conn.executemany(
            f"INSERT INTO {table} ({', '.join(columns)}, sort_order, updated_at) "
            f"VALUES ({placeholders})",
            [
                (*row, (index + 1) * 10, db._now())
                for index, row in enumerate(rows)
            ],
        )


def seed_all() -> None:
    """Populate every table from the plan content."""
    db.set_settings(SETTINGS)

    _insert_rows(
        "journey",
        ["period", "title", "description", "theme"],
        JOURNEY,
    )

    _insert_rows(
        "strengths",
        ["kind", "name", "current_level", "target_level", "evidence", "next_action"],
        [
            (
                kind,
                name,
                current,
                target,
                None,
                "To be defined: what will prove this has moved up a level?",
            )
            for kind, name, current, target in STRENGTHS
        ],
    )

    _insert_rows(
        "experiences",
        ["category", "title", "description", "status", "verified", "start_date", "end_date", "evidence"],
        [
            (
                item["category"],
                item["title"],
                item["description"],
                item["status"],
                item["verified"],
                None,
                None,
                None,
            )
            for item in EXPERIENCES
        ],
    )

    _insert_rows(
        "actions_702010",
        ["bucket", "action", "detail", "status", "progress", "due_date", "notes"],
        [(bucket, action, detail, "Not started", 0, None, None) for bucket, action, detail in ACTIONS_70_20_10],
    )

    _insert_rows(
        "career_stages",
        ["stage", "timeframe", "title", "description", "status", "progress"],
        [
            (
                timeframe,
                "Stage",
                title,
                description,
                status,
                10 if status == "In progress" else 0,
            )
            for timeframe, title, description, status in CAREER_STAGES
        ],
    )

    _insert_rows(
        "skills",
        ["priority_area", "planned_action", "evidence_of_success", "status", "progress", "evidence_link", "last_practiced"],
        [
            (area, action, evidence, "Not started", 0, None, None)
            for area, action, evidence in SKILLS
        ],
    )

    _insert_rows(
        "goals",
        ["goal", "success_looks_like", "category", "status", "progress", "target_date", "notes"],
        [(goal, success, category, "Not started", 0, None, None) for goal, success, category in GOALS],
    )

    _insert_rows(
        "first90",
        ["phase", "task", "done", "done_date", "notes"],
        [(phase, task, 0, None, None) for phase, task in FIRST_90],
    )

    _insert_rows(
        "support",
        ["category", "need", "status", "who", "notes"],
        [(category, need, "Needed", None, None) for category, need in SUPPORT],
    )

    db.log("system", "Career Development Plan imported (November 2026).")
