import os
import logging
import pandas as pd
import PyPDF2
from ollama import Client

logging.basicConfig(level=logging.DEBUG)


def analyze_files_in_directory(directory_path):
    files = os.listdir(directory_path)
    logging.debug(f"Found {len(files)} files in the directory: {files}")

    if not files:
        logging.warning("No files found in the directory.")
        return

    for file in files:
        file_path = os.path.join(directory_path, file)
        logging.debug(f"Processing file: {file_path}")
        analyze_file(file_path)


def analyze_file(downloaded_file_path):
    client = Client(host='http://localhost:11434')

    if downloaded_file_path.endswith('.xlsx') or downloaded_file_path.endswith('.xls'):
        df = pd.read_excel(downloaded_file_path, engine='openpyxl')
        file_content = df.to_string()
    elif downloaded_file_path.endswith('.pdf'):
        with open(downloaded_file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            file_content = ''
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                file_content += page.extract_text()
    else:
        logging.warning(f"Skipping file {downloaded_file_path} as it is not an Excel or PDF file.")
        return

    if not file_content.strip():
        logging.warning(f"No text found in file {downloaded_file_path}.")
        return

    def preprocess_file_content(content):
        preprocessed_content = content.replace('\n', ' ').replace('\r', '')
        return preprocessed_content

    file_content = preprocess_file_content(file_content)
    print(file_content)

    system_prompt = ("You are an AI specialized in generating SQL statements. Only return the SQL statement without "
                     "any additional text or explanation.")

    examples = [
        {"role": "user", "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, '
                                    'tag2, tag3, tag4, tag5) VALUES ("ERP Systems", "SAP", "Microsoft Dynamics", '
                                    '"Oracle", "Infor")'},
        {"role": "assistant", "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ('
                                         '"ERP Systems", "SAP", "Microsoft Dynamics", "Oracle", "Infor")'},
        {"role": "user", "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, '
                                    'tag2, tag3, tag4, tag5) VALUES ("IT Project Management", "Agile", "Scrum", '
                                    '"Kanban", "Waterfall")'},
        {"role": "assistant", "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ("IT '
                                         'Project Management", "Agile", "Scrum", "Kanban", "Waterfall")'},
        {"role": "user", "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, '
                                    'tag2, tag3, tag4, tag5) VALUES ("IT Security", "Cryptography", '
                                    '"Network Security", "Cloud Security", "Cybersecurity")'},
        {"role": "assistant", "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ("IT '
                                         'Security", "Cryptography", "Network Security", "Cloud Security", '
                                         '"Cybersecurity")'},
        {"role": "user", "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2,'
                                    'tag3, tag4, tag5) VALUES ("Microeconomics", "Supply and Demand", "Elasticity", '
                                    '"Market Structures", "Consumer Theory")'},
        {"role": "assistant", "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ('
                                         '"Microeconomics", "Supply and Demand", "Elasticity", "Market Structures", '
                                         '"Consumer Theory")'},
        {"role": "user", "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2,'
                                    'tag3, tag4, tag5) VALUES ("Macroeconomics", "Fiscal Policy", "Monetary Policy", '
                                    '"Unemployment", "Inflation")'},
        {"role": "assistant", "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ('
                                         '"Macroeconomics", "Fiscal Policy", "Monetary Policy", "Unemployment", '
                                         '"Inflation")'},
        {"role": "user", "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2,'
                                    'tag3, tag4, tag5) VALUES ("Calculus", "Limits", "Derivatives", "Integrals", '
                                    '"Series")'},
        {"role": "assistant", "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ('
                                         '"Calculus", "Limits", "Derivatives", "Integrals", "Series")'},
        {"role": "user", "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2,'
                                    'tag3, tag4, tag5) VALUES ("Linear Algebra", "Vectors", "Matrices", "Eigenvalues '
                                    'and'
                                    'Eigenvectors", "Linear Transformations")'},
        {"role": "assistant", "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ('
                                         '"Linear'
                                         'Algebra", "Vectors", "Matrices", "Eigenvalues and Eigenvectors", '
                                         '"Linear Transformations")'},
        {"role": "user", "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2,'
                                    'tag3, tag4, tag5) VALUES ("Statistics", "Probability", "Hypothesis Testing", '
                                    '"Regression Analysis", "Statistical Inference")'},
        {"role": "assistant", "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ('
                                         '"Statistics", "Probability", "Hypothesis Testing", "Regression Analysis", '
                                         '"Statistical Inference")'},
        {"role": "user", "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2,'
                                    'tag3, tag4, tag5) VALUES ("Architecture", "Design Principles", "Architectural '
                                    'Styles", "Building Materials", "Sustainability in Architecture")'},
        {"role": "assistant", "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ('
                                         '"Architecture", "Design Principles", "Architectural Styles", "Building '
                                         'Materials", "Sustainability in Architecture")'},
        {"role": "user", "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2,'
                                    'tag3, tag4, tag5) VALUES ("Physics", "Mechanics", "Electromagnetism", '
                                    '"Thermodynamics", "Quantum Mechanics")'},
        {"role": "assistant", "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ('
                                         '"Physics", "Mechanics", "Electromagnetism", "Thermodynamics", '
                                         '"Quantum Mechanics")'},
        {"role": "user", "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2,'
                                    'tag3, tag4, tag5) VALUES ("Chemistry", "Organic Chemistry", "Inorganic Chemistry",'
                                    '"Physical Chemistry", "Biochemistry")'},
        {"role": "assistant", "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ('
                                         '"Chemistry", "Organic Chemistry", "Inorganic Chemistry", "Physical '
                                         'Chemistry",'
                                         '"Biochemistry")'},
        {"role": "user", "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2,'
                                    'tag3, tag4, tag5) VALUES ("Biology", "Cell Biology", "Genetics", "Ecology", '
                                    '"Evolution")'},
        {"role": "assistant", "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ('
                                         '"Biology", "Cell Biology", "Genetics", "Ecology", "Evolution")'},
        {"role": "user", "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2,'
                                    'tag3, tag4, tag5) VALUES ("Computer Science", "Algorithms", "Data Structures", '
                                    '"Operating Systems", "Computer Networks")'},
        {"role": "assistant", "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ('
                                         '"Computer Science", "Algorithms", "Data Structures", "Operating Systems", '
                                         '"Computer Networks")'},
        {"role": "user", "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2,'
                                    'tag3, tag4, tag5) VALUES ("Psychology", "Cognitive Psychology", "Developmental '
                                    'Psychology", "Social Psychology", "Clinical Psychology")'},
        {"role": "assistant", "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ('
                                         '"Psychology", "Cognitive Psychology", "Developmental Psychology", '
                                         '"Social Psychology", "Clinical Psychology")'},
        {"role": "user", "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, '
                                    'tag2, tag3, tag4, tag5) VALUES ("Geology", "Mineralogy", "Petrology", '
                                    '"Paleontology", "Seismology")'},
        {"role": "assistant",
         "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ("Geology", "Mineralogy", '
                    '"Petrology", "Paleontology", "Seismology")'},
        {"role": "user", "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, '
                                    'tag2, tag3, tag4, tag5) VALUES ("Astronomy", "Astrophysics", "Cosmology", '
                                    '"Planetary Science", "Stellar Astronomy")'},
        {"role": "assistant", "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ('
                                         '"Astronomy", "Astrophysics", "Cosmology", "Planetary Science", '
                                         '"Stellar Astronomy")'},
        {"role": "user",
         "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, '
                    'tag5) VALUES ("Philosophy", "Metaphysics", "Epistemology", "Ethics", "Logic")'},
        {"role": "assistant",
         "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ("Philosophy", '
                    '"Metaphysics", "Epistemology", "Ethics", "Logic")'},
        {"role": "user",
         "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, '
                    'tag5) VALUES ("Sociology", "Social Theory", "Cultural Sociology", "Political Sociology", '
                    '"Urban Sociology")'},
        {"role": "assistant",
         "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ("Sociology", '
                    '"Social Theory", "Cultural Sociology", "Political Sociology", "Urban Sociology")'},
        {"role": "user",
         "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, '
                    'tag5) VALUES ("Anthropology", "Cultural Anthropology", "Biological Anthropology", "Linguistic '
                    'Anthropology", "Archaeology")'},
        {"role": "assistant",
         "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ("Anthropology", '
                    '"Cultural Anthropology", "Biological Anthropology", "Linguistic Anthropology", "Archaeology")'},
        {"role": "user",
         "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, '
                    'tag5) VALUES ("Political Science", "Political Theory", "Comparative Politics", "International '
                    'Relations", "Public Administration")'},
        {"role": "assistant",
         "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ("Political Science", '
                    '"Political Theory", "Comparative Politics", "International Relations", "Public Administration")'},
        {"role": "user",
         "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, '
                    'tag5) VALUES ("History", "Ancient History", "Medieval History", "Modern History", "Art History")'},
        {"role": "assistant",
         "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ("History", "Ancient '
                    'History", "Medieval History", "Modern History", "Art History")'},
        {"role": "user",
         "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, '
                    'tag5) VALUES ("Literature", "Poetry", "Drama", "Fiction", "Literary Criticism")'},
        {"role": "assistant",
         "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ("Literature", "Poetry", '
                    '"Drama", "Fiction", "Literary Criticism")'},
        {"role": "user",
         "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, '
                    'tag5) VALUES ("Linguistics", "Phonetics", "Syntax", "Semantics", "Sociolinguistics")'},
        {"role": "assistant",
         "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ("Linguistics", '
                    '"Phonetics", "Syntax", "Semantics", "Sociolinguistics")'},
        {"role": "user",
         "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, '
                    'tag5) VALUES ("Music", "Music Theory", "Musicology", "Ethnomusicology", "Music Education")'},
        {"role": "assistant",
         "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ("Music", "Music Theory", '
                    '"Musicology", "Ethnomusicology", "Music Education")'},
        {"role": "user",
         "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, '
                    'tag5) VALUES ("Art", "Painting", "Sculpture", "Photography", "Performance Art")'},
        {"role": "assistant",
         "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ("Art", "Painting", '
                    '"Sculpture", "Photography", "Performance Art")'},
        {"role": "user",
         "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, '
                    'tag5) VALUES ("Theatre", "Acting", "Directing", "Playwriting", "Dramaturgy")'},
        {"role": "assistant",
         "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ("Theatre", "Acting", '
                    '"Directing", "Playwriting", "Dramaturgy")'},
        {"role": "user",
         "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, '
                    'tag5) VALUES ("Dance", "Ballet", "Modern Dance", "Jazz Dance", "Choreography")'},
        {"role": "assistant",
         "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ("Dance", "Ballet", '
                    '"Modern Dance", "Jazz Dance", "Choreography")'},
        {"role": "user",
         "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, '
                    'tag5) VALUES ("Film", "Film Theory", "Film Production", "Screenwriting", "Film Criticism")'},
        {"role": "assistant",
         "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ("Film", "Film Theory", '
                    '"Film Production", "Screenwriting", "Film Criticism")'},
        {"role": "user",
         "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, '
                    'tag5) VALUES ("Education", "Curriculum and Instruction", "Educational Psychology", '
                    '"Special Education", "Educational Leadership")'},
        {"role": "assistant",
         "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ("Education", "Curriculum '
                    'and Instruction", "Educational Psychology", "Special Education", "Educational Leadership")'},
        {"role": "user",
         "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, '
                    'tag5) VALUES ("Law", "Constitutional Law", "Criminal Law", "Corporate Law", "International Law")'},
        {"role": "assistant",
         "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ("Law", "Constitutional '
                    'Law", "Criminal Law", "Corporate Law", "International Law")'},
        {"role": "user", "content": 'Input: tag1, tag2, tag3, tag4, tag5\nINSERT INTO qualitaetsmanagement (tag1, '
                                    'tag2, tag3, tag4, tag5) VALUES ("Medicine", "Anatomy", "Physiology", '
                                    '"Pathology", "Pharmacology")'},
        {"role": "assistant", "content": 'INSERT INTO qualitaetsmanagement (tag1, tag2, tag3, tag4, tag5) VALUES ('
                                         '"Medicine", "Anatomy", "Physiology", "Pathology", "Pharmacology")'}

    ]

    messages = [{"role": "system", "content": system_prompt}] + examples + [
        {
            'role': 'user',
            'content': 'please create a sql statement out of the file for insertion into a database, use this and '
                       'write things for "VALUES": INSERT INTO database ( tag1, tag2, tag3, tag4, tag5 ) VALUES ( ) '
                       + file_content,
        },
    ]

    response = client.chat(model='llama3', messages=messages)
    logging.debug(response)
    return response


analyze_files_in_directory("../downloads")
