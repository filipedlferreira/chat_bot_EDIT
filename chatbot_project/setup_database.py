import psycopg2

# Database connection parameters
conn_params = {
    'dbname': 'EditAssist',
    'user': 'postgres',
    'password': 'mafmafm',
    'host': 'localhost',
    'port': 1234
}

# SQL statements to create tables
create_tables_sql = """
    CREATE TABLE IF NOT EXISTS CourseDetails (
        course_id SERIAL PRIMARY KEY,
        course_name VARCHAR(255),
        description VARCHAR(1000),
        start_date DATE,
        end_date DATE,
        investment VARCHAR(255),
        schedule VARCHAR(255),
        location VARCHAR(255),
        total_hours INT,
        area VARCHAR(255),
        course_type VARCHAR(255)
    );

    CREATE TABLE IF NOT EXISTS Modules (
        module_id SERIAL PRIMARY KEY,
        course_id INT REFERENCES CourseDetails(course_id),
        module_name VARCHAR(255),
        module_description TEXT
    );

    CREATE TABLE IF NOT EXISTS ModuleTopics (
        topic_id SERIAL PRIMARY KEY,
        module_id INT REFERENCES Modules(module_id),
        topic_name VARCHAR(255),
        topic_description TEXT
    );

    CREATE TABLE IF NOT EXISTS Instructors (
        instructor_id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        role VARCHAR(255),
        organization VARCHAR(255)
    );

    CREATE TABLE IF NOT EXISTS AdmissionRequirements (
        requirement_id SERIAL PRIMARY KEY,
        course_id INT REFERENCES CourseDetails(course_id),
        requirement_description TEXT
    );

    CREATE TABLE IF NOT EXISTS PaymentOptions (
        payment_id SERIAL PRIMARY KEY,
        course_id INT REFERENCES CourseDetails(course_id),
        payment_option VARCHAR(255),
        details TEXT
    );

    CREATE TABLE IF NOT EXISTS Certification (
        certification_id SERIAL PRIMARY KEY,
        course_id INT REFERENCES CourseDetails(course_id),
        certification_details TEXT
    );

    CREATE TABLE IF NOT EXISTS Recruitment (
        recruitment_id SERIAL PRIMARY KEY,
        course_id INT REFERENCES CourseDetails(course_id),
        recruitment_details TEXT
    );
"""

# SQL statements to insert initial data
insert_data_sql = """
    INSERT INTO CourseDetails (course_name, description, start_date, end_date, investment, schedule, location, total_hours, area, course_type)
    VALUES 
    ('Data Science & Business Analytics', 'O curso de Data Science & Business Analytics dá-te o conhecimento para a recolha, tratamento e análise de dados, potenciando a sua aplicação e utilização estratégica na gestão de negócio.', '2024-09-24', '2025-02-25', '€348 x 8', 'Tue, Wed, Thu, 19h-23h', 'Lisbon', 216, 'Data & Business', 'Course'),
    ('Data Engineering', 'Este curso aborda os fundamentos essenciais da Engenharia de Dados, fornecendo uma compreensão abrangente das técnicas e ferramentas necessárias para lidar com grandes volumes de dados. Desde a orquestração de pipelines de dados até à construção de Data Warehouses, passando ainda pelo processamento em tempo real, os alunos irão embarcar numa jornada de aprendizagem abrangente, culminando num projeto prático onde poderão aplicar e consolidar todo o conhecimento adquirido!', '2024-10-04', '2025-01-11', '€290 x 5', 'Mon, Wed, Fri, 18h-22h', 'Porto', 136, 'Data Engineering', 'Intensive Course'),
    ('Plataformas para Sites, Blogs e Lojas Online', 'Este workshop tem como objectivo perceber quais as plataformas mais adequadas para se criar uma loja online, um site institucional ou mesmo um blog.', '2024-06-26', '2024-07-03', '€170', 'Mon, Wed, 19h-22h', 'Remote', 12, 'Data & Business', 'Workshop');

    INSERT INTO Modules (course_id, module_name, module_description)
    VALUES 
    (1, 'Data Science Fundamentals', 'Data Science Definition/Applications, Data Mining, Python Fundamentals, Data Understanding'),
    (1, 'Databases Fundamentals', 'Database concept, Datawarehouse concept, Relational and non-relational, SQL Fundamentals'),
    (1, 'Big Data Technologies', 'Big Data Ecosystem, Distributed Data Processing with Spark'),
    (1, 'Business Analytics', 'Introduction to Google Analytics, KPIs, Dashboards with Data Studio'),
    (1, 'Analyzing & Visualizing Data', 'Introduction to Information Visualization, Plotting with python, Building dashboards'),
    (1, 'Exploratory Data Analysis', 'Descriptive Statistics, Cleaning data techniques, Visual exploration'),
    (1, 'Quantitative & Statistical Analysis', 'Types of Quantitative Data, Collection Methods, Analysis Methods'),
    (1, 'Machine Learning Models', 'Introduction to Machine Learning Models, Supervised and Unsupervised Learning'),
    (1, 'Introduction to Neural Networks', 'Different Types of Neural Networks, Selected Examples'),
    (1, 'Applied Practice', 'Identify a problem, Obtain data, Analyze data, Create visualizations, Present insights'),
    (2, 'Data Engineering Fundamentals', 'Introduction to fundamental concepts, architecture notions, basic networking, containerization, infrastructure as code'),
    (2, 'Data Pipeline Orchestration', 'Introduction to data pipeline orchestration, Airflow basics, scheduling pipelines, monitoring and failure management'),
    (2, 'Data Warehousing', 'Principles of Data Warehousing, dimensional modeling, introduction to BigQuery, performance optimization'),
    (2, 'Data Processing', 'Introduction to batch data processing, Apache Spark, batch job optimization, practical exercises'),
    (2, 'Real-Time Data (Streaming)', 'Introduction to real-time data processing, frameworks like Apache Kafka and Flink, SQL-based real-time processing, event-time processing'),
    (2, 'Analytics Engineering', 'Introduction to dbt, building transformation pipelines in dbt, advanced dbt features'),
    (2, 'Applied Project', 'Application of all content to a real data problem, including data collection, processing, and presentation of insights'),
    (3, 'Overview of Platforms', 'Understanding the best platforms for creating online stores, institutional sites, and blogs'),
    (3, 'Initial Steps for Online Presence', 'Domain registration, hosting, and everything necessary for having an online presence'),
    (3, 'Strengthening Online Presence', 'The importance of online presence and how to work on it, introduction to SEO'),
    (3, 'Platform Differences', 'Differences between platforms and their features, suitable platforms for each business need');

    INSERT INTO Instructors (name, role, organization)
    VALUES 
    ('Nuno Reis', 'Co-founder & Data Scientist', 'Thorly Education'),
    ('Bruno Valinhas', 'Head of Analytics', 'Jornal Público'),
    ('Ângelo Pereira', 'Lead Data Scientist', 'Nielsen'),
    ('German Mendez', 'Lead Machine Learning', 'Siemens'),
    ('Roberto Vega', 'Data Scientist', 'DareData Engineering'),
    ('Carla Geraldes', 'Senior Total Rewards Analyst', 'Farfetch'),
    ('Rute Moutinho', 'Country Manager - Portugal', 'Departamento Pedagógico'),
    ('Lisandra Caires', 'Pedagogical Manager', 'Departamento Pedagógico'),
    ('Ana Ferreira', 'Pedagogical Assistant', 'Departamento Pedagógico'),
    ('Diva Azevedo', 'Student Admissions Manager', 'Departamento Pedagógico'),
    ('Filipa Freitas', 'Designer & Founder', 'Lance Collective'),
    ('Laura Silva', 'Student Admissions / Pedagogical Assistant', 'Departamento Remote Learning'),
    ('Ariana Rodrigues', 'Remote Learning Manager', 'Departamento Remote Learning'),
    ('Sofia Sobral', 'Remote Learning Assistant', 'Departamento Remote Learning');

    INSERT INTO AdmissionRequirements (course_id, requirement_description)
    VALUES 
    (1, 'Minimum age 18 years, background in Engineering, Economy, Accounting, etc.'),
    (1, 'Professional experience in an analytical domain'),
    (1, 'Free SOPP (Pedagogical & Professional Orientation Session) with a Student Admissions Manager'),
    (2, 'Minimum age 18 years, background in Software Engineering, System Development, Data Analysis, or related fields'),
    (2, 'Professional experience in programming, preferably in Python'),
    (2, 'Free SOPP (Pedagogical & Professional Orientation Session) with a Student Admissions Manager'),
    (3, 'Minimum age 18 years; Basic knowledge of internet usage and digital communication'),
    (3, 'Free SOPP (Pedagogical & Professional Orientation Session) with a Student Admissions Manager');

    INSERT INTO PaymentOptions (course_id, payment_option, details)
    VALUES 
    (1, 'Monthly Payments', '€348 x 8, no interest'),
    (1, 'Full Payment', '€2644.80 with a 5% discount'),
    (1, 'ISA Financing', 'Pay after getting a job through an Income Share Agreement with Fundação José Neves'),
    (2, 'Monthly Payments', '€290 x 5, no interest'),
    (2, 'Full Payment', '€1377.50 with a 5% discount'),
    (3, 'Full Payment', '€170');

    INSERT INTO Certification (course_id, certification_details)
    VALUES 
    (1, 'Includes hours, modules, topics, final grades, DGERT certification, and signature from pedagogical coordination'),
    (2, 'Includes hours, modules, topics, final grades, DGERT certification, and signature from pedagogical coordination'),
    (3, 'Includes total hours, topics covered, and tutor information');

    INSERT INTO Recruitment (course_id, recruitment_details)
    VALUES 
    (1, 'Access to a network of recruitment partners aimed at accelerating students professional careers'),
    (2, 'Access to a network of recruitment partners aimed at accelerating students professional careers'),
    (3, 'Access to a network of recruitment partners aimed at accelerating students professional careers');
"""

# Function to create tables and insert data
def setup_database():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()

        # Create tables
        cur.execute(create_tables_sql)
        
        # Insert initial data
        cur.execute(insert_data_sql)

        # Commit changes
        conn.commit()

        # Close cursor and connection
        cur.close()
        conn.close()

        print("Database setup completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function to set up the database
setup_database()