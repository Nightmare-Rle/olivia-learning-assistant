// O.L.I.V.I.A Figma — components, instances, auto-layout, variables
const DATA = {
  "k12": {
    "Kindergarten": {
      "Aesthetic Creative Development": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Cognitive Development": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Language Literacy Communication": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Mathematics": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Physical Health Motor Development": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Socio-emotional Development": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Values Development": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ]
    },
    "Grade 1": {
      "GMRC": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Language": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Makabansa": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Mathematics": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Reading and Literacy": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ]
    },
    "Grade 2": {
      "English": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Filipino": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "GMRC": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Makabansa": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Mathematics": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ]
    },
    "Grade 3": {
      "English": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Filipino": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "GMRC": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Makabansa": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Mathematics": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Science": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ]
    },
    "Grade 4": {
      "Araling Panlipunan": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "English": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "EPP TLE": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Filipino": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "GMRC": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Mathematics": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Music and Arts": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "PE and Health": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Science": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ]
    },
    "Grade 5": {
      "Araling Panlipunan": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "English": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "EPP TLE": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Filipino": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "GMRC": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Mathematics": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Music and Arts": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "PE and Health": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Science": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ]
    },
    "Grade 6": {
      "Araling Panlipunan": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "English": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "EPP TLE": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Filipino": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "GMRC": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Mathematics": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Music and Arts": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "PE and Health": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Science": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ]
    },
    "Grade 7": {
      "Araling Panlipunan": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "English": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Filipino": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "MAPEH": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Mathematics": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Science": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "TLE": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Values Education": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ]
    },
    "Grade 8": {
      "Araling Panlipunan": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "English": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Filipino": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "MAPEH": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Mathematics": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Science": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "TLE": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Values Education": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ]
    },
    "Grade 9": {
      "Araling Panlipunan": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "English": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Filipino": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "MAPEH": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Mathematics": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Science": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "TLE": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Values Education": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ]
    },
    "Grade 10": {
      "Araling Panlipunan": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "English": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Filipino": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "MAPEH": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Mathematics": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Science": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "TLE": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Values Education": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ]
    },
    "Grade 11 SHS": {
      "ABM Strand - Applied Economics": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "ABM Strand - Business Ethics Social Responsibility": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "ABM Strand - Business Mathematics": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "ABM Strand - Fundamentals of Accountancy Business Management 1": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "ABM Strand - Organization and Management": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Applied Track - Empowerment Technologies": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Applied Track - English for Academic Professional Purposes": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Applied Track - Entrepreneurship": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Applied Track - Filipino sa Piling Larangan": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Applied Track - Inquiries Investigations Immersion": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Applied Track - Practical Research 1": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Applied Track - Practical Research 2": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Arts and Design Track - Media Arts": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Arts and Design Track - Performing Arts": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Arts and Design Track - Visual Arts": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - 21st Century Literature": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Contemporary Philippine Arts": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Disaster Readiness Risk Reduction": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Earth and Life Science": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Earth Science": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - General Mathematics": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Introduction to Philosophy": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Komunikasyon at Pananaliksik": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Media and Information Literacy": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Oral Communication": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Personal Development": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Physical Education and Health": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Physical Science": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Reading and Writing": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Statistics and Probability": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "GAS Strand - Applied Economics GAS": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "GAS Strand - Disaster Readiness GAS": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "GAS Strand - Humanities 1": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "GAS Strand - Humanities 2": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "GAS Strand - Organization and Management GAS": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "GAS Strand - Social Science 1": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "HUMSS Strand - Disciplines and Ideas in Social Sciences": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "HUMSS Strand - Philippine Politics and Governance": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "HUMSS Strand - World Religions Belief Systems": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "STEM Strand - Basic Calculus": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "STEM Strand - General Biology 1": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "STEM Strand - General Chemistry 1": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "STEM Strand - Pre Calculus": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Sports Track - Fitness and Exercise Programming": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Sports Track - Sports Officiating and Coaching": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Sports Track - Sports Psychology and Nutrition": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "TVL Track - Agri Fishery Arts": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "TVL Track - Home Economics": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "TVL Track - ICT Track": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "TVL Track - Industrial Arts": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ]
    },
    "Grade 12 SHS": {
      "ABM Strand - Business Enterprise Simulation": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "ABM Strand - Business Finance": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "ABM Strand - Fundamentals of Accountancy Business Management 2": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "ABM Strand - Principles of Marketing": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "ABM Strand - Work Immersion ABM": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Applied Track - Empowerment Technologies": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Applied Track - English for Academic Professional Purposes": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Applied Track - Entrepreneurship": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Applied Track - Filipino sa Piling Larangan": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Applied Track - Inquiries Investigations Immersion": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Applied Track - Practical Research 1": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Applied Track - Practical Research 2": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Arts Design Track - Media Arts": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Arts Design Track - Performing Arts": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Arts Design Track - Visual Arts": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Arts and Design Track - Media Arts": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Arts and Design Track - Performing Arts": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Arts and Design Track - Visual Arts": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - 21st Century Literature": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Contemporary Philippine Arts": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Disaster Readiness Risk Reduction": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Earth and Life Science": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Earth Science": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - General Mathematics": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Introduction to Philosophy": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Komunikasyon at Pananaliksik": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Media and Information Literacy": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Oral Communication": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Personal Development": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Physical Education and Health": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Physical Science": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Reading and Writing": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Core Subjects - Statistics and Probability": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "GAS Strand - Applied Economics GAS": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "GAS Strand - Disaster Readiness GAS": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "GAS Strand - Humanities 1": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "GAS Strand - Humanities 2": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "GAS Strand - Organization and Management GAS": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "GAS Strand - Social Science 1": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "HUMSS Strand - Community Engagement Solidarity Citizenship": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "HUMSS Strand - Creative Nonfiction": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "HUMSS Strand - Creative Writing": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "HUMSS Strand - Disciplines and Ideas in Applied Social Sciences": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "HUMSS Strand - Trends Networks Critical Thinking": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "STEM Strand - General Biology 2": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "STEM Strand - General Chemistry 2": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "STEM Strand - General Physics 1": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "STEM Strand - General Physics 2": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "STEM Strand - Research Project STEM": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "STEM Strand - Work Immersion STEM": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Sports Track - Fitness and Exercise Programming": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Sports Track - Sports Officiating and Coaching": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "Sports Track - Sports Psychology and Nutrition": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "TVL Track - Agri Fishery Arts": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "TVL Track - Home Economics": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "TVL Track - ICT Track": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ],
      "TVL Track - Industrial Arts": [
        "Full Lesson",
        "Easy",
        "Full Assessment",
        "Hard",
        "Medium",
        "Practice"
      ]
    },
    "Reference Materials": {
      "Assessment and Grading System": [
        "Full Lesson"
      ],
      "Curriculum Overview": [
        "Full Lesson"
      ],
      "DepEd Order References": [
        "Full Lesson"
      ],
      "Learning Theories and Pedagogy": [
        "Full Lesson"
      ],
      "MATATAG Curriculum Comparison": [
        "Full Lesson"
      ],
      "Most Essential Learning Competencies": [
        "Full Lesson"
      ],
      "Philippine Education Sector Plan": [
        "Full Lesson"
      ],
      "Teaching Strategies and Resources": [
        "Full Lesson"
      ]
    }
  },
  "college": {
    "Business and Finance": {
      "Accountancy": [
        "Accounting Information Systems",
        "Advanced Financial Accounting",
        "Auditing",
        "Auditing and Assurance",
        "Business Finance",
        "Business Laws and Regulations",
        "Business Law and Taxation",
        "Corporate Governance",
        "Cost Accounting and Control",
        "Financial Accounting and Reporting",
        "Financial Management",
        "Fundamentals of Accounting",
        "Governmental Accounting",
        "Management Accounting",
        "Taxation"
      ],
      "Business Administration": [
        "Business Analytics",
        "Business Ethics and Governance",
        "Business Law and Ethics",
        "Entrepreneurship and Innovation",
        "Financial Management",
        "Human Resource Management",
        "Marketing Management",
        "Operations Management",
        "Organizational Behavior",
        "Principles of Management",
        "Strategic Management"
      ],
      "Customs Administration": [
        "Customs Brokerage",
        "Customs Law and Tariff",
        "International Trade and Logistics"
      ],
      "Economics": [
        "Development Economics",
        "Econometrics",
        "International Economics",
        "Macroeconomic Theory",
        "Microeconomic Theory",
        "Philippine Economic History"
      ],
      "Entrepreneurship": [
        "Business Plan Development",
        "Entrepreneurial Mindset",
        "New Venture Creation",
        "Small Business Management",
        "Technopreneurship"
      ],
      "Public Administration": [
        "Local Government Administration",
        "Philippine Public Administration",
        "Public Financial Management",
        "Public Policy Analysis"
      ]
    },
    "Engineering": {
      "Agricultural Engineering": [
        "Agricultural Machinery",
        "Agricultural Structures",
        "Bio-Engineering",
        "Irrigation and Drainage"
      ],
      "Chemical Engineering": [
        "Chemical Engineering Thermodynamics",
        "Chemical Reaction Engineering",
        "Fluid Mechanics and Particle Technology",
        "Heat and Mass Transfer",
        "Process Control and Safety",
        "Separation Processes"
      ],
      "Civil Engineering": [
        "Construction Management",
        "Engineering Management",
        "Engineering Mathematics",
        "Environmental Engineering",
        "Fluid Mechanics",
        "Geotechnical Engineering",
        "Hydraulics and Water Resources",
        "Mechanics of Deformable Bodies",
        "Statics of Rigid Bodies",
        "Steel and Concrete Design",
        "Structural Analysis",
        "Structural Engineering",
        "Transportation Engineering"
      ],
      "Computer Engineering": [
        "Computer Architecture",
        "Digital Logic and Design",
        "Embedded Systems",
        "Microprocessors and Microcontrollers",
        "Operating Systems"
      ],
      "Electrical Engineering": [
        "Circuit Analysis",
        "Electrical Code and Safety",
        "Electrical Machines",
        "Power Electronics and Drives",
        "Power Systems"
      ],
      "Electronics Engineering": [
        "Communications Engineering",
        "Control Systems",
        "Digital Systems",
        "Electronic Circuits",
        "Signal Processing"
      ],
      "Geodetic Engineering": [
        "Cartography and GIS",
        "Geodesy",
        "Surveying"
      ],
      "Industrial Engineering": [
        "Ergonomics and Human Factors",
        "Operations Research",
        "Production Systems",
        "Quality Management",
        "Supply Chain Management"
      ],
      "Mechanical Engineering": [
        "Fluid Mechanics and Machinery",
        "Heat Transfer",
        "HVAC and Refrigeration",
        "Machine Design",
        "Power Plant Engineering",
        "Thermodynamics"
      ],
      "Mining Engineering": [
        "Mineral Processing",
        "Mine Safety and Environment",
        "Mining Methods and Operations"
      ],
      "Sanitary Engineering": [
        "Air Pollution Control",
        "Solid Waste Management",
        "Wastewater Engineering",
        "Water Supply and Treatment"
      ]
    },
    "IT and Computing": {
      "Computer Science": [
        "Algorithms and Complexity",
        "Artificial Intelligence",
        "Automata and Computation",
        "Computer Architecture",
        "Computer Networks",
        "Database Systems",
        "Data Structures and Algorithms",
        "Discrete Structures",
        "Human Computer Interaction",
        "Machine Learning Fundamentals",
        "Operating Systems",
        "Programming Languages",
        "Software Development",
        "Software Engineering",
        "Theory of Computation"
      ],
      "Cyber Security": [
        "Cryptography",
        "Digital Forensics",
        "Ethical Hacking",
        "Information Assurance",
        "Network Security"
      ],
      "Data Science": [
        "Big Data Analytics",
        "Data Mining",
        "Data Visualization",
        "Machine Learning",
        "Statistical Methods"
      ],
      "Information Technology": [
        "Cybersecurity Fundamentals",
        "Database Management",
        "Database Management Systems",
        "Data Structures and Algorithms",
        "Information Management",
        "IT Project Management",
        "Networking and Communications",
        "Networking and Security",
        "Object Oriented Programming",
        "Programming 1 Fundamentals",
        "Software Engineering",
        "Systems Analysis and Design",
        "Web Development",
        "Web Systems and Technologies"
      ]
    },
    "Health Sciences": {
      "Medical Laboratory Science": [
        "Clinical Chemistry",
        "Hematology",
        "Histopathology",
        "Immunohematology",
        "Microbiology and Parasitology"
      ],
      "Midwifery": [
        "Community Midwifery",
        "Emergency Obstetric Care",
        "Fundamentals of Midwifery",
        "Maternal and Child Health",
        "Reproductive Health"
      ],
      "Nursing": [
        "Anatomy and Physiology",
        "Community Health Nursing",
        "Disaster Nursing",
        "Fundamentals of Nursing",
        "Maternal and Child Nursing",
        "Medical Surgical Nursing",
        "Microbiology and Parasitology",
        "Nursing Leadership and Management",
        "Nursing Research",
        "Pharmacology",
        "Psychiatric Nursing"
      ],
      "Nutrition and Dietetics": [
        "Clinical Nutrition",
        "Community Nutrition",
        "Food Service Management",
        "Life Stage Nutrition",
        "Nutrition Science"
      ],
      "Occupational Therapy": [
        "Foundations of OT",
        "Orthotics and Prosthetics",
        "Pediatric OT",
        "Psychosocial OT"
      ],
      "Pharmacy": [
        "Pharmaceutical Chemistry",
        "Pharmaceutics",
        "Pharmacognosy",
        "Pharmacology",
        "Pharmacy Law and Ethics"
      ],
      "Physical Therapy": [
        "Cardiopulmonary PT",
        "Electrotherapy",
        "Human Anatomy and Physiology",
        "Neurological PT",
        "Orthopedic PT",
        "Therapeutic Exercises"
      ],
      "Public Health": [
        "Biostatistics",
        "Environmental Health",
        "Epidemiology",
        "Health Policy and Management",
        "Health Promotion"
      ],
      "Radiologic Technology": [
        "Imaging Modalities",
        "Radiation Protection",
        "Radiographic Anatomy and Positioning",
        "Radiographic Physics"
      ],
      "Respiratory Therapy": [
        "Cardiopulmonary Anatomy and Physiology",
        "Mechanical Ventilation",
        "Neonatal and Pediatric Respiratory Care",
        "Pulmonary Diagnostics",
        "Respiratory Therapeutics"
      ]
    },
    "Education": {
      "Early Childhood Education": [
        "Child Development 0-8",
        "Creative Arts in ECE",
        "Early Childhood Assessment",
        "ECE Curriculum and Pedagogy",
        "Language and Literacy Early Childhood"
      ],
      "Elementary Education": [
        "Child and Adolescent Development",
        "Foundations of Education",
        "Teaching English in Elem",
        "Teaching Filipino in Elem",
        "Teaching Mathematics in Elem",
        "Teaching Multigrade Classes",
        "Teaching Science in Elem",
        "Teaching Social Studies in Elem"
      ],
      "Library and Information Science": [
        "Cataloging and Classification",
        "Foundations of Library Science",
        "Information Sources and Services",
        "Information Technology in Libraries",
        "Library Management"
      ],
      "Physical Education": [
        "Exercise Physiology",
        "Motor Learning and Development",
        "Philippine Games and Sports",
        "Physical Fitness and Wellness",
        "Sports Psychology"
      ],
      "Secondary Education": [
        "Assessment of Learning",
        "Child and Adolescent Development",
        "Curriculum and Instruction",
        "Curriculum Development",
        "Educational Technology",
        "Facilitating Learning",
        "Field Study and Practice Teaching",
        "Field Study and Practicum",
        "Foundations of Education",
        "Language Education",
        "Principles of Teaching",
        "Research in Education",
        "Social Studies Education"
      ],
      "Special Needs Education": [
        "Behavior Management",
        "Foundations of Special Education",
        "Intellectual and Developmental Disabilities",
        "Learning Disabilities"
      ]
    },
    "Social Sciences": {
      "History": [
        "Asian History",
        "Historiography and Historical Methods",
        "Philippine History",
        "World History"
      ],
      "International Studies": [
        "Diplomacy and Negotiation",
        "Foreign Policy Analysis",
        "Global Political Economy",
        "International Law and Organizations",
        "International Relations Theory"
      ],
      "Philosophy": [
        "Epistemology and Metaphysics",
        "Ethics",
        "History of Philosophy",
        "Logic and Critical Thinking"
      ],
      "Political Science": [
        "Comparative Government",
        "International Relations",
        "Philippine Government and Politics",
        "Political Theory",
        "Public Policy and Governance"
      ],
      "Psychology": [
        "Abnormal Psychology",
        "Cognitive Psychology",
        "Developmental Psychology",
        "Experimental Psychology",
        "General Psychology",
        "Industrial Organizational Psychology",
        "Psychological Assessment",
        "Research Methods in Psychology",
        "Social Psychology",
        "Theories of Personality"
      ],
      "Social Work": [
        "Case Management",
        "Child and Family Welfare",
        "Community Organization",
        "Community Organizing",
        "Disaster Risk Management",
        "Field Instruction",
        "Foundations of Social Work",
        "Gender and Development",
        "Introduction to Social Work",
        "Medical and Psychiatric Social Work",
        "Social Welfare Policies",
        "Social Welfare Policy PH",
        "Social Work Practice with Groups",
        "Social Work Research"
      ],
      "Sociology": [
        "General Sociology",
        "Methods of Social Research",
        "Philippine Society and Culture",
        "Social Stratification",
        "Urban and Rural Sociology"
      ]
    },
    "Communication and Arts": {
      "Architecture": [
        "Architectural Design",
        "Architectural Design Fundamentals",
        "Architectural History",
        "Architectural Research Methods",
        "Architectural Theories",
        "Building Laws and Code",
        "Building Technology",
        "Building Utilities",
        "Environmental Architecture",
        "History of Architecture",
        "Professional",
        "Professional Practice and Ethics",
        "Professional Practice",
        "Site Planning and Landscape",
        "Structural Concepts",
        "Urban Design and Planning"
      ],
      "Broadcasting": [
        "Broadcast Writing",
        "Media Management",
        "Radio Production",
        "Television Production"
      ],
      "Communication Research": [
        "Communication Audience Research",
        "Communication Theories",
        "Data Analysis for Communication",
        "Research Methods in Communication"
      ],
      "Fine Arts": [
        "Art Criticism and Aesthetics",
        "Art History",
        "Drawing and Visual Elements",
        "Painting",
        "Sculpture"
      ],
      "Interior Design": [
        "Furniture and Lighting",
        "Interior Construction",
        "Interior Design Foundations",
        "Interior Materials",
        "Professional Practice ID"
      ],
      "Journalism": [
        "Broadcast Journalism",
        "Digital Journalism",
        "Feature and Editorial Writing",
        "Media Law and Ethics",
        "News Writing and Reporting"
      ]
    },
    "Hospitality and Tourism": {
      "Hospitality Management": [
        "Cross Cultural Communication",
        "Events Management",
        "Event Management",
        "Food and Beverage Management",
        "Food and Beverage Service",
        "Food Safety and Sanitation",
        "Front Office and Housekeeping",
        "Front Office Operations",
        "Hospitality Marketing",
        "Hospitality Operations",
        "Hotel and Restaurant Accounting",
        "Housekeeping Management",
        "Introduction to Hospitality Industry",
        "Tourism Planning and Development"
      ],
      "Tourism Management": [
        "Philippine Tourism Geography",
        "Sustainable and Responsible Tourism",
        "Tourism Policy and Planning",
        "Tourism Principles",
        "Tour Operations and Travel Agency"
      ]
    },
    "Criminal Justice and Law": {
      "Criminology": [
        "Comparative Police Systems",
        "Correctional Administration",
        "Criminal Investigation",
        "Criminal Law",
        "Criminal Law and Procedure",
        "Criminal Procedure",
        "Cybercrime and Legal Issues",
        "Forensic Science",
        "Introduction to Criminology",
        "Juvenile Delinquency",
        "Juvenile Delinquency and Justice",
        "Law Enforcement Administration",
        "Police Organization and Administration",
        "Victimology"
      ],
      "Law": [
        "Civil Law",
        "Constitutional Law",
        "Corporation and Business Law",
        "Criminal Law",
        "Labor and Social Legislation",
        "Legal Ethics",
        "Remedial Law",
        "Taxation"
      ]
    },
    "Agriculture and Environment": {
      "Agriculture": [
        "Agricultural Economics",
        "Animal Science",
        "Crop Protection",
        "Crop Science",
        "Soil Science"
      ],
      "Environmental Science": [
        "Climate Change and Disaster Risk",
        "Ecosystem Management",
        "Environmental Chemistry and Toxicology",
        "Environmental Impact Assessment",
        "Environmental Science"
      ],
      "Fisheries": [
        "Aquaculture",
        "Fishery Biology",
        "Fish Processing and Preservation",
        "Marine Ecology"
      ],
      "Food Technology": [
        "Food Chemistry",
        "Food Legislation",
        "Food Microbiology",
        "Food Processing and Engineering",
        "Food Quality and Safety"
      ],
      "Forestry": [
        "Dendrology and Forest Ecology",
        "Forest Management",
        "Forest Products and Utilization",
        "Social Forestry"
      ]
    },
    "Maritime": {
      "Marine Engineering": [
        "Marine Electrical Systems",
        "Marine Engineering Systems",
        "Marine Thermodynamics and Power",
        "Naval Architecture",
        "Shipboard Safety"
      ],
      "Marine Transportation": [
        "Cargo Operations",
        "Celestial Navigation",
        "Marine Meteorology",
        "Maritime Law",
        "Ship Handling and Maneuvering",
        "Terrestrial and Coastal Navigation"
      ]
    },
    "Sciences": {
      "Applied Statistics": [
        "Multivariate Analysis",
        "Probability Theory",
        "Regression and Correlation",
        "Sampling and Survey Methods",
        "Statistical Inference"
      ],
      "Biology": [
        "Cell and Molecular Biology",
        "Comparative Anatomy and Physiology",
        "Ecology and Evolution",
        "Genetics",
        "Microbiology"
      ],
      "Chemistry": [
        "Analytical Chemistry",
        "General Chemistry",
        "Inorganic Chemistry",
        "Organic Chemistry",
        "Physical Chemistry"
      ],
      "Mathematics": [
        "Abstract Algebra",
        "Calculus",
        "Complex Analysis",
        "Differential Equations",
        "Linear Algebra",
        "Real Analysis"
      ],
      "Physics": [
        "Classical Mechanics",
        "Electromagnetism",
        "Optics",
        "Quantum Mechanics",
        "Thermodynamics and Statistical Mechanics"
      ]
    }
  },
  "answerCount": 612
};
const HOME_DATA = [["K-12 Learning", 14, "A5D6A7", "14 grades with DepEd-aligned subjects."], ["College Programs", 12, "90CAF9", "12 categories, multiple programs."], ["Web Search", 0, "FFCC80", "Search Google, browse education portals."], ["Markdown Reader", 0, "CE93D8", "View .md files, lessons, answer keys."], ["Answer Sheets", 612, "F48FB1", "All 612 assessments with answer keys."], ["Create Documents", 0, "80DEEA", "Built-in doc and slide editor."], ["My Content", 0, "FFAB91", "Saved lessons and custom curricula."], ["Admin Panel", 0, "B0BEC5", "Users, backup, password, generator."]];
const GC = 14, CC = 12, SC = 612;

// ─── Color & Style helpers ─────────────────────────────────────────

const hex = c => ({r:parseInt(c.slice(0,2),16)/255,g:parseInt(c.slice(2,4),16)/255,b:parseInt(c.slice(4,6),16)/255});
const solid = c => ({type:"SOLID",color:hex(c),opacity:1});

let DF = null; // default font

function child(node, name) {
  return node.children.find(c => c.name === name);
}

// ─── Frame helpers ─────────────────────────────────────────────────

function F(name, x, y, w, h, color, rx) {
  const o = figma.createFrame(); o.name=name; o.x=x; o.y=y; o.resize(w,h);
  if (color) o.fills=[solid(color)];
  if (rx) o.cornerRadius=rx;
  return o;
}

function R(name, x, y, w, h, color, rx) {
  const o = figma.createRectangle(); o.name=name; o.x=x; o.y=y; o.resize(w,h);
  if (color) o.fills=[solid(color)];
  if (rx) o.cornerRadius=rx;
  return o;
}

function T(name, x, y, w, txt, sz, wgt, c, align) {
  const o = figma.createText(); o.name=name; o.x=x; o.y=y; o.resize(w,20);
  if (DF) o.fontName=DF; o.fontSize=sz; o.characters=txt;
  if (c) o.fills=[solid(c)]; if (align) o.textAlignHorizontal=align;
  return o;
}

// ─── Auto-layout helper ────────────────────────────────────────────

function AL(name, x, y, w, h, color, rx, dir, pad, gap) {
  const o = F(name, x, y, w, h, color, rx);
  o.layoutMode = dir === "H" ? "HORIZONTAL" : "VERTICAL";
  o.primaryAxisSizingMode = "AUTO";
  o.counterAxisSizingMode = "AUTO";
  o.paddingLeft = o.paddingRight = o.paddingTop = o.paddingBottom = pad || 0;
  o.itemSpacing = gap || 0;
  return o;
}

// ─── Master Component Builder ──────────────────────────────────────

const MASTERS = {};

function makeComp2(page, name, x, y, builder) {
  const comp = figma.createComponent(); comp.name = name; comp.x = x; comp.y = y;
  builder(comp);
  MASTERS[name] = comp;
  page.appendChild(comp);
  return comp;
}

function inst(name) {
  const m = MASTERS[name];
  return m ? m.createInstance() : null;
}

function setText(node, childName, text) {
  const c = child(node, childName);
  if (c && c.type === "TEXT") c.characters = text;
}

// ═══════════════════════════════════════════════════════════════════
// BUILD MASTER COMPONENTS
// ═══════════════════════════════════════════════════════════════════

function buildMasters(page) {

  // ── Buttons ──
  const BTN_W = 180, BTN_H = 50;
  const btnColors = [
    ["Green","81C784"],["Blue","90CAF9"],["Orange","FFB74D"],
    ["Red","E57373"],["Salmon","FFAB91"],["DeepOrange","FF8A65"],
  ];
  btnColors.forEach(([n,c],i) => {
    makeComp2(page,"Button/"+n, 40, 80+i*70, comp => {
      comp.resize(BTN_W, BTN_H);
      const bg = R("BG",0,0,BTN_W,BTN_H,c,8); comp.appendChild(bg);
      const lb = T("Label",0,BTN_H/2-9,BTN_W,"Button",13,700,"ffffff","CENTER"); comp.appendChild(lb);
    });
  });

  // ── Role Buttons ──
  [["Student","81C784"],["Teacher","90CAF9"],["Admin","FFB74D"]].forEach(([n,c],i) => {
    makeComp2(page,"RoleBtn/"+n, 40+220*i, 460, comp => {
      comp.resize(200, 50);
      const bg = R("BG",0,0,200,50,c,8); comp.appendChild(bg);
      const lb = T("Label",0,16,200,n,14,700,"ffffff","CENTER"); comp.appendChild(lb);
    });
  });

  // ── Difficulty Tags ──
  const tagColors = [
    ["FullLesson","81C784"],["Easy","A5D6A7"],["Medium","FFE082"],
    ["Hard","EF9A9A"],["Practice","CE93D8"],["Assessment","F48FB1"],
  ];
  tagColors.forEach(([n,c],i) => {
    makeComp2(page,"Tag/"+n, 40+160*i, 540, comp => {
      comp.resize(130, 26);
      const bg = R("BG",0,0,130,26,c,4); comp.appendChild(bg);
      const lb = T("Label",0,4,130,n,10,400,"ffffff","CENTER"); comp.appendChild(lb);
    });
  });

  // ── Home Card ──
  makeComp2(page,"HomeCard", 40, 580, comp => {
    comp.resize(300, 200);
    comp.cornerRadius = 14;
    const bg = R("BG",0,0,300,200,"ffffff",14); comp.appendChild(bg);
    const ct = T("Title",20,25,260,"Title",20,700,"000000"); comp.appendChild(ct);
    const cd = T("Desc",20,65,260,"Description",12,400,"444444"); comp.appendChild(cd);
    const ch = T("Hint",20,160,260,"Click to open",10,400,"666666"); comp.appendChild(ch);
  });

  // ── StatusBar ──
  makeComp2(page,"StatusBar", 40, 800, comp => {
    comp.resize(1200, 36);
    const bg = R("BG",0,0,1200,36,"FFF5EB"); comp.appendChild(bg);
    const tx = T("Text",20,10,500,"Status text",10,400,"666666"); comp.appendChild(tx);
  });

  // ── SearchField ──
  makeComp2(page,"SearchField", 40, 850, comp => {
    comp.resize(400, 34);
    const bg = R("BG",0,0,400,34,"f0f0f0",8); comp.appendChild(bg);
    const tx = T("Placeholder",15,9,300,"Search...",12,400,"aaaaaa"); comp.appendChild(tx);
  });

  // ── FormField ──
  makeComp2(page,"FormField", 40, 900, comp => {
    comp.resize(320, 60);
    const lb = T("Label",0,0,200,"Label",13,400,"333333"); comp.appendChild(lb);
    const bg = R("Input",0,20,320,30,"f0f0f0",6); comp.appendChild(bg);
  });

  // ── OfficialPortalBox ──
  makeComp2(page,"OfficialPortal", 40, 980, comp => {
    comp.resize(200, 80);
    const bg = R("BG",0,0,200,80,"FFF8F0",10); comp.appendChild(bg);
    const tl = T("Title",15,8,170,"Portal Title",12,700); comp.appendChild(tl);
    const sd = T("Sub",15,26,170,"Subtitle",10,400,"666666"); comp.appendChild(sd);
    const btn = R("VisitBtn",25,48,100,24,"81C784",6); comp.appendChild(btn);
    const bt = T("BtnLabel",25,53,100,"Visit",9,600,"ffffff","CENTER"); comp.appendChild(bt);
  });

  // ── ScreenFrame wrapper ──
  makeComp2(page,"ScreenFrame", 40, 1080, comp => {
    comp.resize(1200, 800);
    comp.fills = [solid("f5f5f5")];
    comp.cornerRadius = 8;
  });

  // ── AdminTab ──
  makeComp2(page,"AdminTab", 40, 1180, comp => {
    comp.resize(180, 30);
    const bg = R("BG",0,0,180,30,"f0f0f0",6); comp.appendChild(bg);
    const tx = T("Label",0,6,180,"Tab",11,500,"000000","CENTER"); comp.appendChild(tx);
  });
}

// ═══════════════════════════════════════════════════════════════════
// SCREEN BUILDERS (use component instances)
// ═══════════════════════════════════════════════════════════════════

function buildLogin(frame) {
  frame.appendChild(T("Title",250,80,700,"O.L.I.V.I.A.",56,700,"1a73e8","CENTER"));
  frame.appendChild(T("Sub",250,145,700,"Online Learning Intelligent Interactive Assistant",20,400,"444444","CENTER"));
  frame.appendChild(T("Credit",250,175,700,"Created by NightmareRLE",13,400,"888888","CENTER"));
  frame.appendChild(T("Logo",250,215,700,"A smart, adaptive learning companion for K-12 and College students.",13,400,"666666","CENTER"));

  [["Student","81C784",300],["Teacher","90CAF9",500],["Admin","FFB74D",700]].forEach(([n,c,x]) => {
    const card = F(n, x, 260, 200, 160, c, 12);
    card.appendChild(T(n+"L",15,25,170,n,22,700,"000000","CENTER"));
    card.appendChild(T(n+"D",15,65,170,"Click to sign in as "+n,11,400,"333333","CENTER"));
    card.appendChild(T(n+"H",15,120,170,"Sign in",10,400,"ffffff","CENTER"));
    frame.appendChild(card);
  });

  const form = F("LoginForm",300,460,600,200,"ffffff",12);
  form.strokes=[{type:"SOLID",color:hex("dddddd"),opacity:1}];
  form.appendChild(T("T",20,18,200,"Sign In to O.L.I.V.I.A",18,700,"000000"));
  form.appendChild(T("UL",20,50,100,"Username",12,400,"333333"));
  form.appendChild(R("UF",20,66,560,30,"f0f0f0",6));
  form.appendChild(T("PL",20,110,100,"Password",12,400,"333333"));
  form.appendChild(R("PF",20,126,560,30,"f0f0f0",6));
  frame.appendChild(form);
}

function buildHome(frame) {
  frame.appendChild(T("Title",40,30,400,"O.L.I.V.I.A.",32,700));
  frame.appendChild(T("Sub",40,65,500,"Choose a section to get started",14,400,"555555"));
  frame.appendChild(T("Tag",40,86,400,"Student  |  EN  |  Connected",11,400,"888888"));

  HOME_DATA.forEach(([n,count,color,desc],i) => {
    const col = i%4, row = Math.floor(i/4);
    const card = F(n,40+col*290,120+row*215,270,195,color,14);
    card.appendChild(T("CT",15,22,240,n,20,700));
    card.appendChild(T("Cnt",15,58,240,count>0?count+" available":"",12,400,"333333"));
    card.appendChild(T("Desc",15,88,240,desc,11,400,"444444"));
    card.appendChild(T("H",15,160,240,"Click to open",10,400,"666666"));
    frame.appendChild(card);
  });

  const sb = inst("StatusBar");
  if (sb) { sb.x=0; sb.y=740; setText(sb,"Text","Internet: Connected  |  Student  |  EN"); frame.appendChild(sb); }
}

function buildK12(frame) {
  frame.appendChild(T("Title",40,30,500,"K-12 Learning Materials",28,700));
  frame.appendChild(T("Sub",40,68,400,GC+" grade levels | DepEd-aligned",13,400,"555555"));
  frame.appendChild(T("Info",40,90,400,"Click a grade to view subjects and difficulty levels.",12,400,"888888"));

  const op = inst("OfficialPortal");
  if (op) { op.x=760; op.y=25; setText(op,"Title","Official DepEd Portal"); setText(op,"Sub","Department of Education"); setText(op,"BtnLabel","Visit LRMDS"); frame.appendChild(op); }

  const grades = Object.keys(DATA.k12);
  const left = F("GradeList",40,115,540,620,"f8f8f8",8);
  left.appendChild(T("GL",15,12,200,"Grade Levels",14,700));
  grades.forEach((g,i) => {
    const sg = Object.keys(DATA.k12[g]).length;
    const card = F(g,15,36+i*38,510,32,"f0f0f0",6);
    card.appendChild(T("GN",10,7,490,g+" ("+sg+" subjects)",12,400));
    left.appendChild(card);
  });
  frame.appendChild(left);

  const right = F("Subjects",620,115,540,620,"f8f8f8",8);
  right.appendChild(T("SL",15,12,250,"Subjects & Difficulties",14,700));
  const fg = Object.entries(DATA.k12)[0];
  if (fg) {
    const [gn,subs] = fg;
    right.appendChild(T("GN",15,34,500,gn,13,600,"1a73e8"));
    const c = {"Full Lesson":"81C784","Easy":"A5D6A7","Medium":"FFE082","Hard":"EF9A9A","Practice":"CE93D8","Full Assessment":"F48FB1"};
    Object.entries(subs).slice(0,9).forEach(([sn,diffs],j) => {
      const block = F(sn,15,55+j*40,510,34,"ffffff",6);
      block.appendChild(T("SN",10,8,200,sn,11,400));
      diffs.forEach((d,k) => {
        const dot = F("d",220+k*48,5,44,24,c[d]||"cccccc",4);
        dot.appendChild(T("DL",0,6,44,d.replace("Full Lesson","Lesson").replace("Full Assessment","Assess"),8,400,"ffffff","CENTER"));
        block.appendChild(dot);
      });
      right.appendChild(block);
    });
  }
  frame.appendChild(right);
}

function buildCollege(frame) {
  frame.appendChild(T("Title",40,30,500,"College Programs",28,700));
  frame.appendChild(T("Sub",40,68,400,CC+" categories | CHED-aligned",13,400,"555555"));
  frame.appendChild(T("Info",40,90,400,"Click a category to view programs and topics.",12,400,"888888"));

  const cats = Object.keys(DATA.college);
  const left = F("CategoryList",40,115,540,620,"f8f8f8",8);
  left.appendChild(T("CL",15,12,200,"Categories",14,700));
  cats.forEach((c,i) => {
    const pc = Object.keys(DATA.college[c]).length;
    const card = F(c,15,36+i*38,510,32,"f0f0f0",6);
    card.appendChild(T("CN",10,7,490,c+" ("+pc+" programs)",12,400));
    left.appendChild(card);
  });
  frame.appendChild(left);

  const right = F("Programs",620,115,540,620,"f8f8f8",8);
  right.appendChild(T("SL",15,12,250,"Programs & Difficulties",14,700));
  const fc = Object.entries(DATA.college)[0];
  if (fc) {
    const [cn,progs] = fc;
    right.appendChild(T("GN",15,34,500,cn,13,600,"1a73e8"));
    const c = {"Full Lesson":"81C784","Easy":"A5D6A7","Medium":"FFE082","Hard":"EF9A9A","Practice":"CE93D8","Full Assessment":"F48FB1"};
    Object.entries(progs).slice(0,9).forEach(([pn,topics],j) => {
      const block = F(pn,15,55+j*40,510,34,"ffffff",6);
      block.appendChild(T("PN",10,8,200,pn,11,400));
      topics.slice(0,5).forEach((d,k) => {
        const dot = F("d",220+k*48,5,44,24,c[d]||"cccccc",4);
        dot.appendChild(T("DL",0,6,44,d.replace("Full Lesson","Lesson").replace("Full Assessment","Assess"),8,400,"ffffff","CENTER"));
        block.appendChild(dot);
      });
      right.appendChild(block);
    });
  }
  frame.appendChild(right);
}

function buildSearch(frame) {
  frame.appendChild(T("Title",40,30,500,"Web Search",28,700));
  const url = F("URLBar",40,70,900,36,"ffffff",8);
  url.strokes=[{type:"SOLID",color:hex("dddddd"),opacity:1}];
  url.appendChild(T("PH",15,10,500,"Search Google or enter URL...",13,400,"bbbbbb"));
  frame.appendChild(url);
  frame.appendChild(T("OB",960,70,180,"Open Browser",14,700,"1a73e8"));

  frame.appendChild(T("QL",40,120,300,"Quick Links",16,700));
  [["YouTube","FF0000"],["Google","4285F4"],["DepEd LRMDS","81C784"],
   ["CHED","90CAF9"],["Wikipedia","888888"],["Khan Academy","1a73e8"],
   ["Coursera","0056D2"],["Google Scholar","4285F4"]].forEach(([n,c],i) => {
    const col=i%4, row=Math.floor(i/4);
    const btn = F(n,40+col*285,155+row*70,260,55,c,8);
    btn.appendChild(T(n+"L",0,18,260,n,14,700,"ffffff","CENTER"));
    frame.appendChild(btn);
  });
}

function buildReader(frame) {
  frame.appendChild(T("Title",40,30,500,"Markdown Reader",28,700));
  frame.appendChild(T("Open",40,75,130,"Open .md File",14,700,"1a73e8"));
  frame.appendChild(T("NF",190,83,300,"No file opened",13,400,"999999"));
  const lang = F("Lang",360,73,100,36,"f0f0f0",6);
  lang.appendChild(T("LT",10,10,80,"EN ▼",12,400,"000000","CENTER"));
  frame.appendChild(lang);

  const cont = F("Content",40,125,1120,560,"FFF0D0",10);
  cont.appendChild(T("H1",50,60,800,"Select a lesson from K-12 or College tabs to view content here.",15,400,"555555"));
  cont.appendChild(T("H2",50,95,800,"Use the language dropdown (EN/TL) to switch languages.",14,400,"666666"));
  cont.appendChild(T("H3",50,130,800,"Topics with both EN and TL versions display in the selected language.",14,400,"666666"));
  frame.appendChild(cont);

  const sb = inst("StatusBar");
  if (sb) { sb.x=40; sb.y=700; sb.resize(1120,30); setText(sb,"Text","words: 0  |  lines: 1  |  EN  |  No file"); frame.appendChild(sb); }
}

function buildAnswers(frame) {
  frame.appendChild(T("Title",40,30,500,"Answer Sheets",28,700));
  frame.appendChild(T("Sub",40,68,400,SC+" assessment materials available",12,400,"555555"));

  frame.appendChild(R("Search",40,90,380,30,"f0f0f0",8));
  frame.appendChild(T("ST",50,98,300,"Search by subject, grade, or program...",12,400,"aaaaaa"));
  frame.appendChild(T("Ref",440,90,80,"Refresh",13,700,"1a73e8"));
  frame.appendChild(T("ShowAll",535,90,130,"Show All Answers",13,700,"FF8A65"));

  const left = F("List",40,135,420,570,"f8f8f8",8);
  left.appendChild(T("AC",15,12,200,"Recent Assessments",14,600));
  ["K-12 Kindergarten - Aesthetic Creative - 30 items","K-12 Grade 1 - Language Makabansa - 25 items",
   "K-12 Grade 2 - English GMRC - 30 items","K-12 Grade 3 - Science Math - 35 items",
   "College IT - Computer Science - 40 items","College Engineering - Civil Eng. - 45 items"].forEach((s,i) => {
    const item = F("I"+i,10,36+i*56,400,48,"FFF8F0",8);
    item.appendChild(T("N"+i,10,6,380,s,10,400));
    left.appendChild(item);
  });
  frame.appendChild(left);

  const view = F("View",480,135,680,570,"FFF0D0",10);
  view.appendChild(T("KT",20,18,600,"Answer Key — Full Assessment",18,700,"1a73e8"));
  view.appendChild(T("KM",20,44,600,"Grade 1 · Language Makabansa · EN",12,400,"666666"));
  view.appendChild(R("D",20,68,640,1,"dddddd"));
  view.appendChild(T("P1",20,82,200,"Part I: Multiple Choice",14,700));
  view.appendChild(T("A1",20,106,400," 1. B  2. A  3. C  4. B  5. D",12,400));
  view.appendChild(T("A2",20,126,400," 6. A  7. C  8. B  9. D  10. A",12,400));
  view.appendChild(T("P2",20,158,200,"Part II: True or False",14,700));
  view.appendChild(T("A3",20,182,400,"11. T  12. F  13. T  14. T  15. F",12,400));
  view.appendChild(T("P3",20,214,200,"Part III: Fill in the Blank",14,700));
  view.appendChild(T("A4",20,238,400,"16. photosynthesis  17. ecosystem  18. molecule",12,400));
  view.appendChild(T("A5",20,258,400,"19. nucleus  20. mitochondria",12,400));
  frame.appendChild(view);
}

function buildCreate(frame) {
  frame.appendChild(T("Title",40,30,200,"Create",28,700));
  ["Upload","Doc 1","Slide 1"].forEach((n,i) => {
    const st = F(n,40+i*120,65,110,28,"FFB74D",6);
    st.appendChild(T(n,10,6,90,n,11,600,"ffffff","CENTER"));
    frame.appendChild(st);
  });

  const tb = F("TB",40,100,1120,34,"FFB74D",8);
  ["Undo","Redo","|","Arial","12","|","B","I","U","|","~","1.",">","[]","**","X"].forEach((n,i) => {
    tb.appendChild(T(n,10+i*68,8,50,n,11,400,"ffffff"));
  });
  frame.appendChild(tb);

  const can = F("Canvas",100,148,1000,560,"ffffff");
  can.strokes=[{type:"SOLID",color:hex("dddddd"),opacity:1}];
  can.appendChild(T("Cursor",30,22,400,"Start typing here...",12,400,"bbbbbb"));
  frame.appendChild(can);

  const sb = inst("StatusBar");
  if (sb) { sb.x=100; sb.y=708; sb.resize(1000,28); setText(sb,"Text","words: 0  |  lines: 1  |  Doc 1"); frame.appendChild(sb); }
}

function buildAdmin(frame) {
  frame.appendChild(T("Title",40,30,400,"Admin Panel",26,700));
  frame.appendChild(T("Sub",40,65,400,"System management and configuration",13,400,"555555"));

  const tabs = F("Tabs",40,90,1120,34,"f0f0f0",8);
  ["Manage Users","Backup and Restore","Change Password","Generate Curriculum"].forEach((n,i) => {
    tabs.appendChild(T(n,20+i*190,8,180,n,12,500,"000000","CENTER"));
  });
  frame.appendChild(tabs);

  const box = F("Content",40,135,1120,620,"f8f8f8");
  box.appendChild(T("AUT",20,15,200,"Manage Users",16,600));
  ["Username","Password","Role (student/teacher/admin)"].forEach((l,i) => {
    box.appendChild(T(l+"L",20+i*220,45,200,l,12,400));
    box.appendChild(R(l+"E",20+i*220,63,200,28,"f0f0f0",6));
  });
  box.appendChild(T("AddUser",680,60,100,"Add User",13,700,"81C784"));

  box.appendChild(T("ST",20,110,200,"Students (24)",14,600));
  box.appendChild(R("SL",20,135,540,180,"ffffff",8));
  ["Juan Dela Cruz","Maria Santos","Jose Rizal","Andres Bonifacio","Gabriela Silang","Lapu-Lapu"].forEach((n,i) => {
    const row = F("R"+i,20,135+i*30,540,28,"f8f8f8");
    row.appendChild(T("N",10,5,300,n,11,400));
    row.appendChild(T("E",400,5,50,"Edit",10,600,"ffffff"));
    row.appendChild(T("D",455,5,50,"Del",10,600,"ffffff"));
    box.appendChild(row);
  });

  box.appendChild(T("TT",20,335,200,"Teachers (8)",14,600));
  box.appendChild(R("TL",20,360,540,150,"ffffff",8));
  ["Gloria Macapagal-Arroyo","Fidel V. Ramos","Corazon Aquino"].forEach((n,i) => {
    const row = F("R2_"+i,20,360+i*30,540,28,"f8f8f8");
    row.appendChild(T("N",10,5,300,n,11,400));
    box.appendChild(row);
  });
  frame.appendChild(box);
}

function buildMyContent(frame) {
  frame.appendChild(T("Title",40,30,400,"My Content",28,700));
  frame.appendChild(T("Sub",40,68,400,"Your custom-created lessons and saved materials",14,400,"555555"));
  frame.appendChild(T("Refresh",940,35,90,"Refresh",13,700,"81C784"));

  [["Custom Arithmetic Lesson","Mathematics · Grade 1 · 15 items · Created 07/12/2026","A5D6A7"],
   ["English Grammar Fundamentals","English · Grade 2 · 20 items · Created 07/11/2026","90CAF9"],
   ["Biology Cell Structure","Science · Grade 4 · 25 items · Created 07/10/2026","FFCC80"],
   ["Philippine History Overview","AP · Grade 5 · 30 items · Created 07/09/2026","CE93D8"],
   ["Computer Programming Basics","IT · College · 20 items · Created 07/08/2026","80DEEA"],
  ].forEach(([title,meta,color],i) => {
    const card = F("L"+i,40,100+i*65,1120,55,color,10);
    card.appendChild(T("LT",20,8,400,title,14,600));
    card.appendChild(T("LM",20,30,600,meta,10,400,"333333"));
    card.appendChild(T("Open",1000,12,100,"Open",12,700,"ffffff","CENTER"));
    frame.appendChild(card);
  });
}

// ═══════════════════════════════════════════════════════════════════
// MAIN
// ═══════════════════════════════════════════════════════════════════

function main() {
  figma.notify("O.L.I.V.I.A building components...", {timeout:3000});

  const tmp = figma.createText();
  const df = tmp.fontName; tmp.remove();
  const boldFont = {family:df.family, style:"Bold"};

  Promise.all([
    figma.loadFontAsync(df),
    figma.loadFontAsync(boldFont).catch(()=>{}),
  ]).then(() => {
    DF = df;

    // Create paint styles
    [
      ["Primary/Text","000000"],["Primary/Accent","1a73e8"],["Surface/Cream","FFF8F0"],
      ["Surface/Gold","FFF0D0"],["Surface/Warm","FFF5EB"],
      ["Card/K12","A5D6A7"],["Card/College","90CAF9"],["Card/Search","FFCC80"],
      ["Card/MD","CE93D8"],["Card/Answers","F48FB1"],["Card/Generate","FFAB91"],
      ["Card/Admin","B0BEC5"],["Button/Green","81C784"],["Button/Blue","90CAF9"],
      ["Button/Orange","FFB74D"],["Diff/FullLesson","81C784"],["Diff/Easy","A5D6A7"],
      ["Diff/Medium","FFE082"],["Diff/Hard","EF9A9A"],["Diff/Practice","CE93D8"],
      ["Diff/Assessment","F48FB1"],["Toolbar/Doc","FFB74D"],["Toolbar/Slide","FF8A65"],
    ].forEach(([n,c]) => { const s = figma.createPaintStyle(); s.name=n; s.paints=[solid(c)]; });

    const page = figma.currentPage;
    page.name = "O.L.I.V.I.A";

    // ── Components section (top-left) ──
    buildMasters(page);
    page.appendChild(T("Note",40,20,400,"Master components above — drag into screens or edit. 23 paint styles created.",12,400,"666666"));

    // ── Screen frames (grid below components) ──
    const navMap = {};
    const COMP_H = 80 + 22; // components section height offset

    const grid = [
      ["01 Login", buildLogin, 0,0],
      ["02 Home", buildHome, 1,0],
      ["03 K-12 Learning", buildK12, 2,0],
      ["04 College", buildCollege, 0,1],
      ["05 Web Search", buildSearch, 1,1],
      ["06 Markdown Reader", buildReader, 2,1],
      ["07 Answer Sheets", buildAnswers, 0,2],
      ["08 Create Document", buildCreate, 1,2],
      ["09 My Content", buildMyContent, 2,2],
      ["10 Admin Panel", buildAdmin, 0,3],
    ];
    const GX = 40, GY = COMP_H + 40, GW = 1240, GH = 840;

    grid.forEach(([name, builder, col, row]) => {
      try {
        const sf = F(name, GX+col*GW, GY+row*GH, 1200, 800, "f5f5f5", 8);
        builder(sf);
        page.appendChild(sf);
        navMap[name] = sf;
      } catch(err) {
        const ef = F("Error "+name, GX+col*GW, GY+row*GH, 1200, 800, "ffebee", 8);
        ef.appendChild(T("EM",20,20,800,"Error: "+err.message,14,400,"c62828"));
        page.appendChild(ef);
      }
    });

    // ── Prototype connections ──
    function addNav(node, dest) {
      if (!node || !dest) return;
      try { node.reactions = [{ trigger: { type: "ON_CLICK" }, action: { type: "NODE", destinationId: dest.id, navigation: "NAVIGATE", transition: { type: "DISSOLVE", duration: 0.3 } } }]; } catch(e) {}
    }
    function findC(node, name) {
      return node && node.children ? node.children.find(c => c.name === name || c.name.startsWith(name)) : null;
    }
    function findCs(node, names) {
      return node && node.children ? node.children.filter(c => names.some(n => c.name === n || c.name.startsWith(n))) : [];
    }

    const L = navMap["01 Login"], H = navMap["02 Home"];
    const K = navMap["03 K-12 Learning"], C = navMap["04 College"];
    const W = navMap["05 Web Search"], R = navMap["06 Markdown Reader"];
    const A = navMap["07 Answer Sheets"], D = navMap["08 Create Document"];
    const M = navMap["09 My Content"], AD = navMap["10 Admin Panel"];

    if (L) findCs(L, ["Student","Teacher","Admin"]).forEach(n => addNav(n, H));
    if (H) { addNav(findC(H, "K-12"), K); addNav(findC(H, "College"), C); addNav(findC(H, "Web Search"), W); addNav(findC(H, "Markdown Reader"), R); addNav(findC(H, "Answer Sheets"), A); addNav(findC(H, "Create"), D); addNav(findC(H, "My Content"), M); addNav(findC(H, "Admin Panel"), AD); }
    [K,C,W,R,A,D,M,AD].forEach(f => { if (f) { const t = findC(f, "Title"); if (t && t.type==="TEXT") addNav(t, H); } });

    figma.notify("Done! 1 page with components + "+grid.length+" connected screens.", {timeout:5000});
    figma.closePlugin();
  }).catch(err => {
    figma.notify("Error: "+err.message, {error:true});
    figma.closePlugin();
  });
}

main();
