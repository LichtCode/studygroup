from datetime import datetime
topics = [
    {
        "name": "Data Science",
        "description": (
            "Data Science is the field of study that uses algorithms, processes, and systems "
            "to extract insights and knowledge from structured and unstructured data."
        ),
        "tags": ["Python", "Big Data", "Machine Learning", "Statistics", "Algorithms"],
        "created_at": datetime(2025, 1, 24, 14, 30).isoformat(),
        "updated_at": datetime(2025, 1, 24, 18, 15).isoformat(),
    },
    {
        "name": "Artificial Intelligence",
        "description": (
            "Artificial Intelligence focuses on building intelligent agents capable of "
            "making decisions and performing tasks autonomously."
        ),
        "tags": ["Machine Learning", "Algorithms", "Python", "Robotics", "Big Data"],
        "created_at": datetime(2025, 1, 20, 9, 15).isoformat(),
        "updated_at": datetime(2025, 1, 21, 16, 45).isoformat(),
    },
    {
        "name": "Blockchain",
        "description": (
            "Blockchain is a decentralized digital ledger that records transactions "
            "across many computers securely and transparently."
        ),
        "tags": ["Cryptocurrency", "Security", "Data Science", "Python", "Big Data"],
        "created_at": datetime(2025, 1, 22, 10, 30).isoformat(),
        "updated_at": datetime(2025, 1, 23, 13, 10).isoformat(),
    },
    {
        "name": "Cybersecurity",
        "description": (
            "Cybersecurity involves protecting systems, networks, and programs "
            "from digital attacks, breaches, and unauthorized access."
        ),
        "tags": ["Security", "Networking", "Python", "Cloud Computing", "Big Data"],
        "created_at": datetime(2025, 1, 18, 15, 45).isoformat(),
        "updated_at": datetime(2025, 1, 19, 17, 30).isoformat(),
    },
    {
        "name": "DevOps",
        "description": (
            "DevOps is a set of practices that combines software development "
            "and IT operations to shorten the development lifecycle."
        ),
        "tags": ["Cloud Computing", "Networking", "Python", "Automation", "Security"],
        "created_at": datetime(2025, 1, 21, 11, 00).isoformat(),
        "updated_at": datetime(2025, 1, 21, 14, 20).isoformat(),
    },
    {
        "name": "Game Development",
        "description": (
            "Game Development is the process of designing, creating, and releasing "
            "video games using programming and creative skills."
        ),
        "tags": ["Python", "Algorithms", "UI/UX Design", "Mobile App Development", "3D Design"],
        "created_at": datetime(2025, 1, 23, 9, 45).isoformat(),
        "updated_at": datetime(2025, 1, 24, 12, 50).isoformat(),
    },
    {
        "name": "Cloud Computing",
        "description": (
            "Cloud Computing provides on-demand delivery of IT resources over the internet "
            "with pay-as-you-go pricing."
        ),
        "tags": ["Networking", "Security", "Big Data", "DevOps", "Python"],
        "created_at": datetime(2025, 1, 19, 8, 30).isoformat(),
        "updated_at": datetime(2025, 1, 20, 10, 45).isoformat(),
    },
    {
        "name": "Quantum Computing",
        "description": (
            "Quantum Computing leverages the principles of quantum mechanics to perform "
            "computations far beyond the capabilities of classical computers."
        ),
        "tags": ["Algorithms", "Security", "Python", "Big Data", "Research"],
        "created_at": datetime(2025, 1, 17, 12, 15).isoformat(),
        "updated_at": datetime(2025, 1, 18, 16, 40).isoformat(),
    },
    {
        "name": "Internet of Things (IoT)",
        "description": (
            "IoT connects physical devices to the internet, enabling data exchange and "
            "intelligent operations."
        ),
        "tags": ["Networking", "Embedded Systems", "Security", "Python", "Cloud Computing"],
        "created_at": datetime(2025, 1, 24, 7, 45).isoformat(),
        "updated_at": datetime(2025, 1, 24, 15, 10).isoformat(),
    },
    {
        "name": "UI/UX Design",
        "description": (
            "UI/UX Design focuses on improving user satisfaction by enhancing the usability, "
            "accessibility, and interaction between the user and the product."
        ),
        "tags": ["Web Design", "Graphic Design", "Mobile App Development", "Prototyping", "Testing"],
        "created_at": datetime(2025, 1, 23, 13, 15).isoformat(),
        "updated_at": datetime(2025, 1, 23, 18, 25).isoformat(),
    },
    {
        "name": "Mobile App Development",
        "description": (
            "Mobile App Development involves creating software applications "
            "for mobile devices like smartphones and tablets."
        ),
        "tags": ["Python", "UI/UX Design", "Backend Development", "Testing", "Algorithms"],
        "created_at": datetime(2025, 1, 25, 11, 00).isoformat(),
        "updated_at": datetime(2025, 1, 25, 12, 30).isoformat(),
    },
    {
        "name": "Web Design",
        "description": (
            "Web Design focuses on designing the layout, content production, and graphic "
            "design of websites."
        ),
        "tags": ["UI/UX Design", "Frontend Development", "Python", "Prototyping", "Graphics"],
        "created_at": datetime(2025, 1, 18, 10, 20).isoformat(),
        "updated_at": datetime(2025, 1, 18, 14, 40).isoformat(),
    },
    {
        "name": "Functional Programming",
        "description": (
            "Functional Programming is a programming paradigm where programs are constructed "
            "using pure functions."
        ),
        "tags": ["Python", "Algorithms", "Data Science", "Software Testing", "Mathematics"],
        "created_at": datetime(2025, 1, 20, 16, 00).isoformat(),
        "updated_at": datetime(2025, 1, 20, 17, 50).isoformat(),
    },
    {
        "name": "Robotics",
        "description": (
            "Robotics deals with the design, construction, operation, and use of robots "
            "for various applications."
        ),
        "tags": ["Embedded Systems", "Algorithms", "Machine Learning", "Python", "Automation"],
        "created_at": datetime(2025, 1, 22, 14, 00).isoformat(),
        "updated_at": datetime(2025, 1, 22, 18, 20).isoformat(),
    },
]

tags_content = [
    "Python", "Django", "Machine Learning", "Data Science", "Artificial Intelligence",
    "Cloud Computing", "Frontend Development", "Backend Development", "Full Stack Development",
    "Mobile App Development", "Blockchain", "Cybersecurity", "Game Development", "DevOps",
    "AR/VR Development", "UI/UX Design", "Web Design", "Robotics", "Internet of Things (IoT)",
    "Big Data", "Quantum Computing", "Database Management", "Software Testing", "Networking",
    "Embedded Systems", "Functional Programming", "Open Source Contributions", "Algorithms",
    "Competitive Programming", "Tech Blogging"
]

users_data = [
    {
        "username": "alice_johnson",
        "email": "alice.johnson@example.com",
        "bio": "A data scientist passionate about Python and Machine Learning. Loves solving complex problems using AI.",
        "tags": ["Python", "Data Science", "Machine Learning"],
        "contact_phone": "+1234567890",
        "location": "New York, USA"
    },
    {
        "username": "bob_smith",
        "email": "bob.smith@example.com",
        "bio": "A backend developer specializing in Django and DevOps practices. Always looking for ways to optimize workflows.",
        "tags": ["Django", "Backend Development", "DevOps"],
        "contact_phone": "+1234567891",
        "location": "San Francisco, USA"
    },
    {
        "username": "carol_davis",
        "email": "carol.davis@example.com",
        "bio": "A creative front-end developer with a passion for building responsive and user-friendly interfaces.",
        "tags": ["Mobile App Development", "UI/UX Design", "Web Design"],
        "contact_phone": "+1234567892",
        "location": "London, UK"
    },
    {
        "username": "daniel_lee",
        "email": "daniel.lee@example.com",
        "bio": "A cybersecurity enthusiast who also dabbles in Blockchain and Quantum Computing.",
        "tags": ["Cybersecurity", "Blockchain", "Quantum Computing"],
        "contact_phone": "+1234567893",
        "location": "Berlin, Germany"
    },
    {
        "username": "emily_brown",
        "email": "emily.brown@example.com",
        "bio": "A machine learning researcher exploring the possibilities of AI in healthcare.",
        "tags": ["Artificial Intelligence", "Algorithms", "Tech Blogging"],
        "contact_phone": "+1234567894",
        "location": "Toronto, Canada"
    },
    {
        "username": "frank_moore",
        "email": "frank.moore@example.com",
        "bio": "A robotics engineer working on IoT-enabled devices for smart homes.",
        "tags": ["Robotics", "Internet of Things (IoT)", "Embedded Systems"],
        "contact_phone": "+1234567895",
        "location": "Sydney, Australia"
    },
    {
        "username": "grace_white",
        "email": "grace.white@example.com",
        "bio": "A software tester with an interest in functional programming and networking.",
        "tags": ["Functional Programming", "Software Testing", "Networking"],
        "contact_phone": "+1234567896",
        "location": "Cape Town, South Africa"
    },
    {
        "username": "harry_green",
        "email": "harry.green@example.com",
        "bio": "A full-stack developer focused on building scalable web applications.",
        "tags": ["Full Stack Development", "Cloud Computing", "AR/VR Development"],
        "contact_phone": "+1234567897",
        "location": "Mumbai, India"
    },
    {
        "username": "irene_black",
        "email": "irene.black@example.com",
        "bio": "A competitive programmer who enjoys tackling algorithmic challenges.",
        "tags": ["Big Data", "Competitive Programming", "Algorithms"],
        "contact_phone": "+1234567898",
        "location": "Singapore"
    },
    {
        "username": "jack_wilson",
        "email": "jack.wilson@example.com",
        "bio": "A web designer with a knack for creating sleek and modern interfaces.",
        "tags": ["Open Source Contributions", "Web Design", "Frontend Development"],
        "contact_phone": "+1234567899",
        "location": "Tokyo, Japan"
    },
    {
        "username": "karen_lewis",
        "email": "karen.lewis@example.com",
        "bio": "A Django developer passionate about building robust web solutions.",
        "tags": ["Django", "Backend Development", "Data Science"],
        "contact_phone": "+1234567800",
        "location": "Chicago, USA"
    },
    {
        "username": "liam_hall",
        "email": "liam.hall@example.com",
        "bio": "A game developer with an interest in blockchain technologies.",
        "tags": ["Blockchain", "Game Development", "Quantum Computing"],
        "contact_phone": "+1234567801",
        "location": "Dublin, Ireland"
    },
    {
        "username": "mia_king",
        "email": "mia.king@example.com",
        "bio": "A cloud computing expert who loves teaching others about Python.",
        "tags": ["Python", "Cloud Computing", "Machine Learning"],
        "contact_phone": "+1234567802",
        "location": "Auckland, New Zealand"
    },
    {
        "username": "noah_scott",
        "email": "noah.scott@example.com",
        "bio": "A software tester with a focus on UI/UX improvements.",
        "tags": ["Software Testing", "UI/UX Design", "Web Design"],
        "contact_phone": "+1234567803",
        "location": "Dubai, UAE"
    },
    {
        "username": "olivia_adams",
        "email": "olivia.adams@example.com",
        "bio": "A robotics enthusiast who enjoys sharing knowledge through blogging.",
        "tags": ["Robotics", "Functional Programming", "Tech Blogging"],
        "contact_phone": "+1234567804",
        "location": "Lagos, Nigeria"
    },
    {
        "username": "patrick_clark",
        "email": "patrick.clark@example.com",
        "bio": "A full-stack developer with a passion for AR/VR applications.",
        "tags": ["Full Stack Development", "Artificial Intelligence", "AR/VR Development"],
        "contact_phone": "+1234567805",
        "location": "Los Angeles, USA"
    },
    {
        "username": "quinn_torres",
        "email": "quinn.torres@example.com",
        "bio": "A frontend developer with a love for open source projects.",
        "tags": ["Frontend Development", "Open Source Contributions", "Embedded Systems"],
        "contact_phone": "+1234567806",
        "location": "Madrid, Spain"
    },
    {
        "username": "rachel_martinez",
        "email": "rachel.martinez@example.com",
        "bio": "An IoT developer focused on integrating big data for smart cities.",
        "tags": ["Internet of Things (IoT)", "Big Data", "Software Testing"],
        "contact_phone": "+1234567807",
        "location": "Mexico City, Mexico"
    },
    {
        "username": "steve_evans",
        "email": "steve.evans@example.com",
        "bio": "A backend developer with a strong interest in cloud technologies.",
        "tags": ["Competitive Programming", "Backend Development", "Cloud Computing"],
        "contact_phone": "+1234567808",
        "location": "Vancouver, Canada"
    },
    {
        "username": "tracy_anderson",
        "email": "tracy.anderson@example.com",
        "bio": "A cybersecurity professional passionate about blockchain security.",
        "tags": ["Cybersecurity", "DevOps", "Blockchain"],
        "contact_phone": "+1234567809",
        "location": "Paris, France"
    }
]






