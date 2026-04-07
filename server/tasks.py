SCHEMAS = {
    "hr": {
        "create_sql": """
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    salary REAL NOT NULL,
    hire_date TEXT NOT NULL,
    manager_id INTEGER,
    is_active INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    budget REAL NOT NULL,
    location TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT,
    status TEXT DEFAULT 'active',
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE IF NOT EXISTS assignments (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    project_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    hours_per_week INTEGER DEFAULT 40,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

CREATE TABLE IF NOT EXISTS salaries (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    effective_date TEXT NOT NULL,
    pay_grade TEXT DEFAULT 'mid',
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

CREATE TABLE IF NOT EXISTS leave_requests (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    approved_by INTEGER,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (approved_by) REFERENCES employees(id)
);

CREATE TABLE IF NOT EXISTS performance_reviews (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    reviewer_id INTEGER,
    score REAL NOT NULL,
    review_date TEXT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (reviewer_id) REFERENCES employees(id)
);

CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS employee_skills (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    certified INTEGER DEFAULT 0,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (skill_id) REFERENCES skills(id)
);

CREATE TABLE IF NOT EXISTS project_milestones (
    id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    due_date TEXT NOT NULL,
    completed_date TEXT,
    budget_used REAL,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    industry TEXT NOT NULL
);
""",

        "seed_sql": """
INSERT INTO departments (id, name, budget, location) VALUES
    (1, 'Engineering', 500000, 'Building A'),
    (2, 'Marketing', 200000, 'Building B'),
    (3, 'Sales', 300000, 'Building C'),
    (4, 'HR', 150000, 'Building A'),
    (5, 'Finance', 250000, 'Building D');

INSERT INTO employees (id, name, department, salary, hire_date, manager_id, is_active) VALUES
    (1,  'Alice Johnson',  'Engineering', 95000,  '2019-03-15', NULL, 1),
    (2,  'Bob Smith',      'Engineering', 88000,  '2020-07-01', 1,    1),
    (3,  'Carol White',    'Marketing',   72000,  '2018-11-20', NULL, 1),
    (4,  'David Brown',    'Sales',       68000,  '2021-01-10', NULL, 1),
    (5,  'Eve Davis',      'Engineering', 102000, '2017-06-05', 1,    1),
    (6,  'Frank Miller',   'HR',          65000,  '2022-03-01', NULL, 1),
    (7,  'Grace Lee',      'Finance',     78000,  '2019-09-12', NULL, 1),
    (8,  'Henry Wilson',   'Sales',       71000,  '2020-04-18', 4,    1),
    (9,  'Ivy Chen',       'Engineering', 97000,  '2021-08-22', 1,    1),
    (10, 'Jack Taylor',    'Marketing',   69000,  '2023-01-05', 3,    0),
    (11, 'Karen Adams',    'Engineering', 97000,  '2018-02-14', 1,    1),
    (12, 'Leo Martinez',   'Finance',     82000,  '2020-11-30', 7,    1),
    (13, 'Nina Patel',     'Marketing',   67000,  '2024-01-15', 3,    1);

INSERT INTO projects (id, name, department_id, start_date, end_date, status) VALUES
    (1, 'Website Redesign', 1, '2024-01-01', '2024-06-30', 'completed'),
    (2, 'Mobile App',       1, '2024-03-01', NULL,          'active'),
    (3, 'Q1 Campaign',      2, '2024-01-15', '2024-03-31', 'completed'),
    (4, 'CRM Integration',  3, '2024-02-01', NULL,          'active'),
    (5, 'Benefits Portal',  4, '2024-04-01', NULL,          'active'),
    (6, 'Budget Dashboard', 5, '2024-01-01', '2024-05-15', 'completed');

INSERT INTO assignments (id, employee_id, project_id, role, hours_per_week) VALUES
    (1,  1,    1, 'Lead',      30),
    (2,  2,    1, 'Developer', 40),
    (3,  5,    2, 'Lead',      35),
    (4,  9,    2, 'Developer', 40),
    (5,  11,   2, 'Developer', 40),
    (6,  3,    3, 'Lead',      25),
    (7,  10,   3, 'Assistant', 40),
    (8,  4,    4, 'Lead',      30),
    (9,  8,    4, 'Sales Rep', 35),
    (10, 6,    5, 'Lead',      40),
    (11, 7,    6, 'Lead',      30),
    (12, 12,   6, 'Analyst',   40),
    (13, NULL, 2, 'Unassigned', 0),
    (14, 5,    4, 'Consultant', 10),
    (15, 9,    5, 'Helper',     5),
    (16, 2,    2, 'Tester',     20),
    (17, 5,    2, 'Reviewer',   10);

INSERT INTO salaries (id, employee_id, amount, effective_date, pay_grade) VALUES
    (1,  1,  85000,  '2019-03-15', 'mid'),
    (2,  1,  90000,  '2020-01-01', 'senior'),
    (3,  1,  95000,  '2021-01-01', 'senior'),
    (4,  2,  80000,  '2020-07-01', 'mid'),
    (5,  2,  88000,  '2021-07-01', 'senior'),
    (6,  3,  68000,  '2018-11-20', 'mid'),
    (7,  3,  72000,  '2020-01-01', 'mid'),
    (8,  4,  65000,  '2021-01-10', 'junior'),
    (9,  4,  68000,  '2022-01-10', 'mid'),
    (10, 5,  95000,  '2017-06-05', 'senior'),
    (11, 5,  100000, '2019-01-01', 'senior'),
    (12, 5,  102000, '2020-01-01', 'senior'),
    (13, 6,  60000,  '2022-03-01', 'junior'),
    (14, 6,  65000,  '2023-01-01', 'mid'),
    (15, 7,  75000,  '2019-09-12', 'mid'),
    (16, 7,  78000,  '2021-01-01', 'mid'),
    (17, 8,  68000,  '2020-04-18', 'mid'),
    (18, 8,  71000,  '2021-04-18', 'mid'),
    (19, 9,  85000,  '2021-08-22', 'mid'),
    (20, 9,  97000,  '2022-08-22', 'senior'),
    (21, 11, 90000,  '2018-02-14', 'senior'),
    (22, 11, 97000,  '2020-01-01', 'senior'),
    (23, 12, 78000,  '2020-11-30', 'mid'),
    (24, 12, 82000,  '2022-01-01', 'senior'),
    (25, 10, 72000,  '2023-01-05', 'mid'),
    (26, 10, 69000,  '2024-01-05', 'mid'),
    (27, 1,  95000,  '2021-01-01', 'senior');

INSERT INTO leave_requests (id, employee_id, start_date, end_date, status, approved_by) VALUES
    (1,  1,  '2024-01-15', '2024-01-19', 'approved', 6),
    (2,  2,  '2024-02-01', '2024-02-05', 'approved', 1),
    (3,  3,  '2024-03-10', '2024-03-22', 'approved', NULL),
    (4,  4,  '2024-01-20', '2024-01-22', 'rejected', 6),
    (5,  5,  '2024-04-01', '2024-04-03', 'pending',  NULL),
    (6,  8,  '2024-03-05', '2024-03-15', 'approved', 4),
    (7,  9,  '2024-02-15', '2024-02-18', 'rejected', 1),
    (8,  11, '2024-05-01', '2024-05-10', 'pending',  NULL),
    (9,  12, '2024-01-02', '2024-01-04', 'approved', 7),
    (10, 2,  '2024-06-01', '2024-06-07', 'pending',  NULL);

INSERT INTO performance_reviews (id, employee_id, reviewer_id, score, review_date) VALUES
    (1,  1,  NULL, 92, '2024-01-15'),
    (2,  2,  1,    85, '2024-01-15'),
    (3,  3,  NULL, 78, '2024-02-01'),
    (4,  4,  NULL, 70, '2024-02-01'),
    (5,  5,  1,    95, '2024-01-15'),
    (6,  8,  4,    72, '2024-02-01'),
    (7,  9,  1,    88, '2024-03-01'),
    (8,  11, 1,    91, '2024-01-15'),
    (9,  12, 7,    80, '2024-03-01'),
    (10, 7,  NULL, 83, '2024-02-01'),
    (11, 2,  1,    90, '2024-06-01'),
    (12, 5,  1,    97, '2024-06-01');

INSERT INTO skills (id, name, category) VALUES
    (1, 'Python',             'Programming'),
    (2, 'JavaScript',         'Programming'),
    (3, 'SQL',                'Database'),
    (4, 'Data Analysis',      'Analytics'),
    (5, 'Project Management', 'Management'),
    (6, 'Communication',      'Soft Skills');

INSERT INTO employee_skills (id, employee_id, skill_id, certified) VALUES
    (1,  1,  1, 1),
    (2,  1,  3, 1),
    (3,  2,  1, 1),
    (4,  2,  2, 1),
    (5,  3,  5, 0),
    (6,  3,  6, 1),
    (7,  4,  6, 1),
    (8,  5,  1, 1),
    (9,  5,  3, 1),
    (10, 5,  4, 1),
    (11, 7,  4, 1),
    (12, 7,  3, 0),
    (13, 9,  1, 1),
    (14, 9,  2, 0),
    (15, 11, 1, 1),
    (16, 11, 2, 1),
    (17, 8,  6, 1),
    (18, 12, 3, 1),
    (19, 12, 4, 1);

INSERT INTO project_milestones (id, project_id, name, due_date, completed_date, budget_used) VALUES
    (1,  1, 'Design Phase',      '2024-02-01', '2024-01-28', 15000),
    (2,  1, 'Development',       '2024-04-01', '2024-04-15', 35000),
    (3,  1, 'Testing',           '2024-05-15', '2024-05-10', 10000),
    (4,  2, 'Requirements',      '2024-04-01', '2024-03-25', 8000),
    (5,  2, 'Alpha Release',     '2024-06-01', NULL,          NULL),
    (6,  2, 'Beta Release',      '2024-08-01', NULL,          20000),
    (7,  3, 'Campaign Launch',   '2024-02-01', '2024-02-05', 12000),
    (8,  4, 'Integration Setup', '2024-03-01', '2024-03-10', 18000),
    (9,  4, 'Data Migration',    '2024-04-15', NULL,          NULL),
    (10, 5, 'Portal Design',     '2024-05-01', '2024-05-03', 5000);

INSERT INTO clients (id, name, industry) VALUES
    (1, 'Acme Corp',  'Technology'),
    (2, 'GlobalBank', 'Finance'),
    (3, 'HealthPlus', 'Healthcare'),
    (4, 'EduLearn',   'Education');
""",

        "schema_info": (
            "Tables: "
            "employees (id, name, department, salary, hire_date, manager_id, is_active), "
            "departments (id, name, budget, location), "
            "projects (id, name, department_id, start_date, end_date, status), "
            "assignments (id, employee_id, project_id, role, hours_per_week), "
            "salaries (id, employee_id, amount, effective_date, pay_grade), "
            "leave_requests (id, employee_id, start_date, end_date, status, approved_by), "
            "performance_reviews (id, employee_id, reviewer_id, score, review_date), "
            "skills (id, name, category), "
            "employee_skills (id, employee_id, skill_id, certified), "
            "project_milestones (id, project_id, name, due_date, completed_date, budget_used), "
            "clients (id, name, industry)"
        ),
    },

    
    "hospital": {
        "create_sql": """
CREATE TABLE patients (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, age INTEGER NOT NULL,
    gender TEXT NOT NULL, blood_type TEXT, admitted_date TEXT, is_discharged INTEGER DEFAULT 0
);
CREATE TABLE doctors (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, specialization TEXT NOT NULL,
    department TEXT NOT NULL, years_experience INTEGER NOT NULL, is_available INTEGER DEFAULT 1
);
CREATE TABLE appointments (
    id INTEGER PRIMARY KEY, patient_id INTEGER NOT NULL, doctor_id INTEGER NOT NULL,
    scheduled_date TEXT NOT NULL, status TEXT DEFAULT 'scheduled', notes TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(id), FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);
CREATE TABLE medications (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL,
    dosage_unit TEXT NOT NULL, is_controlled INTEGER DEFAULT 0
);
CREATE TABLE prescriptions (
    id INTEGER PRIMARY KEY, appointment_id INTEGER NOT NULL, medication_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL, duration_days INTEGER, refills_allowed INTEGER,
    FOREIGN KEY (appointment_id) REFERENCES appointments(id), FOREIGN KEY (medication_id) REFERENCES medications(id)
);
CREATE TABLE wards (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, floor INTEGER NOT NULL,
    capacity INTEGER NOT NULL, head_doctor_id INTEGER,
    FOREIGN KEY (head_doctor_id) REFERENCES doctors(id)
);
""",
        "seed_sql": """
INSERT INTO patients VALUES
(1,'John Doe',45,'M','A+','2024-01-10',0),(2,'Jane Smith',32,'F','B-','2024-01-15',1),
(3,'Bob Wilson',67,'M',NULL,'2024-02-01',0),(4,'Alice Brown',28,'F','O+','2024-02-10',1),
(5,'Charlie Davis',55,'M','AB+','2024-03-01',0),(6,'Diana Lee',41,'F','A-','2024-03-05',0),
(7,'Edward Kim',73,'M',NULL,'2024-03-10',0),(8,'Fiona Clark',36,'F','B+','2024-03-15',1),
(9,'George Hall',50,'M','O-',NULL,0);

INSERT INTO doctors VALUES
(1,'Dr. Sarah Chen','Cardiology','Internal Medicine',15,1),
(2,'Dr. Mike Ross','Orthopedics','Surgery',10,1),
(3,'Dr. Emily Park','Neurology','Internal Medicine',8,0),
(4,'Dr. James Liu','Pediatrics','Pediatrics',12,1),
(5,'Dr. Anna White','Cardiology','Internal Medicine',20,1),
(6,'Dr. Tom Green','General','Emergency',5,1);

INSERT INTO appointments VALUES
(1,1,1,'2024-01-12','completed','Routine checkup'),
(2,2,2,'2024-01-20','completed',NULL),
(3,3,1,'2024-02-05','completed','Follow-up required'),
(4,4,4,'2024-02-15','cancelled',NULL),
(5,5,5,'2024-03-02','completed','Urgent referral'),
(6,6,3,'2024-03-06','scheduled',NULL),
(7,7,1,'2024-03-12','scheduled','First visit'),
(8,1,5,'2024-03-15','completed',NULL),
(9,3,6,'2024-03-18','completed','Emergency visit'),
(10,9,1,'2024-03-20','scheduled',NULL),
(11,5,5,'2024-03-22','completed','Second opinion'),
(12,6,3,'2024-03-25','cancelled',NULL);

INSERT INTO medications VALUES
(1,'Aspirin','Pain Relief','mg',0),(2,'Metformin','Diabetes','mg',0),
(3,'Lisinopril','Blood Pressure','mg',0),(4,'Oxycodone','Pain Relief','mg',1),
(5,'Amoxicillin','Antibiotic','mg',0),(6,'Diazepam','Anxiety','mg',1);

INSERT INTO prescriptions VALUES
(1,1,3,30,90,2),(2,1,1,60,NULL,0),(3,3,2,30,180,3),
(4,5,3,30,90,NULL),(5,5,4,10,30,0),(6,8,1,30,NULL,0),
(7,9,5,20,14,1),(8,11,3,30,90,2),(9,11,1,60,NULL,NULL),
(10,3,2,60,90,1);

INSERT INTO wards VALUES
(1,'Cardiology Ward',3,20,1),(2,'Surgical Ward',2,15,2),
(3,'Neurology Ward',3,12,3),(4,'Emergency',1,30,NULL),
(5,'Pediatrics',2,18,4);
""",
        "schema_info": (
            "Tables: patients (id, name, age, gender, blood_type, admitted_date, is_discharged), "
            "doctors (id, name, specialization, department, years_experience, is_available), "
            "appointments (id, patient_id, doctor_id, scheduled_date, status, notes), "
            "medications (id, name, category, dosage_unit, is_controlled), "
            "prescriptions (id, appointment_id, medication_id, quantity, duration_days, refills_allowed), "
            "wards (id, name, floor, capacity, head_doctor_id)"
        ),
    },

    
    "university": {
        "create_sql": """
CREATE TABLE students (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, major TEXT NOT NULL,
    enrollment_year INTEGER NOT NULL, gpa REAL, is_active INTEGER DEFAULT 1
);
CREATE TABLE professors (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, department TEXT NOT NULL,
    tenure_status TEXT DEFAULT 'non-tenured', salary REAL NOT NULL
);
CREATE TABLE courses (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, department TEXT NOT NULL,
    credits INTEGER NOT NULL, max_enrollment INTEGER NOT NULL, professor_id INTEGER,
    FOREIGN KEY (professor_id) REFERENCES professors(id)
);
CREATE TABLE enrollments (
    id INTEGER PRIMARY KEY, student_id INTEGER NOT NULL, course_id INTEGER NOT NULL,
    semester TEXT NOT NULL, grade TEXT, completed INTEGER DEFAULT 0,
    FOREIGN KEY (student_id) REFERENCES students(id), FOREIGN KEY (course_id) REFERENCES courses(id)
);
CREATE TABLE scholarships (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, amount REAL NOT NULL,
    eligibility_gpa REAL NOT NULL, department TEXT
);
CREATE TABLE student_scholarships (
    id INTEGER PRIMARY KEY, student_id INTEGER NOT NULL, scholarship_id INTEGER NOT NULL,
    awarded_date TEXT NOT NULL, renewed INTEGER DEFAULT 0,
    FOREIGN KEY (student_id) REFERENCES students(id), FOREIGN KEY (scholarship_id) REFERENCES scholarships(id)
);
""",
        "seed_sql": """
INSERT INTO students VALUES
(1,'Amy Zhang','Computer Science',2021,3.8,1),(2,'Ben Torres','Computer Science',2021,3.8,1),
(3,'Cara Patel','Mathematics',2020,3.5,1),(4,'Dan Reyes','Physics',2022,3.2,1),
(5,'Ella Nguyen','Computer Science',2020,3.9,1),(6,'Finn O''Brien','Mathematics',2021,NULL,1),
(7,'Grace Kim','Physics',2022,2.8,1),(8,'Hugo Diaz','Computer Science',2023,NULL,1),
(9,'Iris Johnson','Mathematics',2020,3.6,0),(10,'Jake Martin','Physics',2021,3.1,1);

INSERT INTO professors VALUES
(1,'Prof. Williams','Computer Science','tenured',120000),
(2,'Prof. Garcia','Mathematics','tenured',110000),
(3,'Prof. Anderson','Physics','non-tenured',95000),
(4,'Prof. Thomas','Computer Science','non-tenured',105000),
(5,'Prof. Robinson','History','tenured',100000),
(6,'Prof. Yamamoto','Biology','non-tenured',92000);

INSERT INTO courses VALUES
(1,'Data Structures','Computer Science',4,30,1),(2,'Algorithms','Computer Science',4,25,4),
(3,'Linear Algebra','Mathematics',3,35,2),(4,'Quantum Mechanics','Physics',4,20,3),
(5,'Calculus II','Mathematics',4,40,2),(6,'Machine Learning','Computer Science',3,20,1),
(7,'World History','History',3,50,5),(8,'Databases','Computer Science',3,25,NULL);

INSERT INTO enrollments VALUES
(1,1,1,'Fall 2021','A',1),(2,1,2,'Spring 2022','A',1),(3,1,6,'Fall 2022','B+',1),
(4,2,1,'Fall 2021','A',1),(5,2,2,'Spring 2022','B',1),(6,3,3,'Fall 2020','A',1),
(7,3,5,'Spring 2021','B+',1),(8,4,4,'Fall 2022','B',1),(9,5,1,'Fall 2020','A',1),
(10,5,2,'Spring 2021','A',1),(11,5,6,'Fall 2021','A',1),(12,7,4,'Fall 2022','C',1),
(13,6,3,'Fall 2021',NULL,0),(14,8,1,'Fall 2023',NULL,0),(15,10,4,'Fall 2021','B-',1),
(16,1,1,'Fall 2021','A',1),(17,4,7,'Spring 2023','A',1),(18,2,6,'Fall 2022','A',1);

INSERT INTO scholarships VALUES
(1,'Dean''s Award',5000,3.5,'Computer Science'),
(2,'Merit Scholarship',3000,3.0,NULL),
(3,'STEM Excellence',8000,3.7,'Computer Science'),
(4,'Math Achievement',4000,3.4,'Mathematics');

INSERT INTO student_scholarships VALUES
(1,1,1,'2022-09-01',1),(2,1,3,'2022-09-01',0),(3,5,1,'2021-09-01',1),
(4,5,3,'2021-09-01',1),(5,3,4,'2021-09-01',0),(6,2,2,'2022-09-01',0);
""",
        "schema_info": (
            "Tables: students (id, name, major, enrollment_year, gpa, is_active), "
            "professors (id, name, department, tenure_status, salary), "
            "courses (id, name, department, credits, max_enrollment, professor_id), "
            "enrollments (id, student_id, course_id, semester, grade, completed), "
            "scholarships (id, name, amount, eligibility_gpa, department), "
            "student_scholarships (id, student_id, scholarship_id, awarded_date, renewed)"
        ),
    },

    
    "ecommerce": {
        "create_sql": """
CREATE TABLE suppliers (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, country TEXT NOT NULL,
    rating REAL, contract_end_date TEXT
);
CREATE TABLE customers (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL,
    region TEXT NOT NULL, signup_date TEXT NOT NULL, is_premium INTEGER DEFAULT 0
);
CREATE TABLE products (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL,
    price REAL NOT NULL, stock_qty INTEGER NOT NULL, supplier_id INTEGER,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);
CREATE TABLE orders (
    id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, order_date TEXT NOT NULL,
    status TEXT DEFAULT 'pending', shipping_address TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL, product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL, unit_price REAL NOT NULL, discount REAL,
    FOREIGN KEY (order_id) REFERENCES orders(id), FOREIGN KEY (product_id) REFERENCES products(id)
);
CREATE TABLE returns (
    id INTEGER PRIMARY KEY, order_item_id INTEGER NOT NULL, return_date TEXT NOT NULL,
    reason TEXT NOT NULL, refund_amount REAL,
    FOREIGN KEY (order_item_id) REFERENCES order_items(id)
);
""",
        "seed_sql": """
INSERT INTO suppliers VALUES
(1,'TechParts Inc','USA',4.5,'2025-12-31'),(2,'GlobalSupply','China',3.8,'2025-06-30'),
(3,'EuroGoods','Germany',4.2,NULL),(4,'QuickShip','India',NULL,'2024-12-31');

INSERT INTO customers VALUES
(1,'Sarah Miller','sarah@email.com','North','2023-01-15',1),
(2,'Tom Brown','tom@email.com','South','2023-03-20',0),
(3,'Lisa Wang','lisa@email.com','North','2023-06-10',1),
(4,'Mark Jones','mark@email.com','West','2023-09-05',0),
(5,'Nina Patel','nina@email.com','South','2024-01-12',0),
(6,'Oscar Lee','oscar@email.com','North','2024-02-28',1),
(7,'Paula Davis','paula@email.com','West','2024-03-15',0);

INSERT INTO products VALUES
(1,'Laptop Pro','Electronics',1200.00,50,1),(2,'Wireless Mouse','Electronics',29.99,200,1),
(3,'Desk Lamp','Home',45.00,150,3),(4,'USB Hub','Electronics',19.99,300,2),
(5,'Office Chair','Furniture',350.00,30,3),(6,'Monitor Stand','Furniture',89.99,75,NULL),
(7,'Keyboard','Electronics',79.99,120,2),(8,'Notebook Set','Stationery',12.99,500,4),
(9,'Webcam HD','Electronics',65.00,40,1);

INSERT INTO orders VALUES
(1,1,'2024-01-15','delivered','123 Main St'),(2,1,'2024-02-20','delivered','123 Main St'),
(3,2,'2024-01-25','delivered','456 Oak Ave'),(4,3,'2024-03-01','delivered','789 Pine Rd'),
(5,4,'2024-03-10','cancelled',NULL),(6,2,'2024-03-15','shipped','456 Oak Ave'),
(7,5,'2024-04-01','pending','321 Elm St'),(8,6,'2024-04-05','delivered','654 Maple Dr'),
(9,3,'2024-04-10','delivered','789 Pine Rd'),(10,1,'2024-04-15','pending','123 Main St');

INSERT INTO order_items VALUES
(1,1,1,1,1200.00,NULL),(2,1,2,2,29.99,5.00),(3,2,7,1,79.99,NULL),
(4,3,5,1,350.00,25.00),(5,3,3,2,45.00,NULL),(6,4,1,1,1200.00,100.00),
(7,4,4,3,19.99,NULL),(8,5,6,1,89.99,NULL),(9,6,8,5,12.99,NULL),
(10,7,2,1,29.99,NULL),(11,8,1,1,1200.00,50.00),(12,8,3,1,45.00,NULL),
(13,9,7,2,79.99,10.00),(14,9,4,1,19.99,NULL),(15,10,2,3,29.99,NULL);

INSERT INTO returns VALUES
(1,1,'2024-02-01','Defective',1200.00),(2,4,'2024-02-10','Wrong size',350.00),
(3,6,'2024-03-20','Changed mind',NULL),(4,11,'2024-04-20','Defective',NULL);
""",
        "schema_info": (
            "Tables: suppliers (id, name, country, rating, contract_end_date), "
            "customers (id, name, email, region, signup_date, is_premium), "
            "products (id, name, category, price, stock_qty, supplier_id), "
            "orders (id, customer_id, order_date, status, shipping_address), "
            "order_items (id, order_id, product_id, quantity, unit_price, discount), "
            "returns (id, order_item_id, return_date, reason, refund_amount)"
        ),
    },

    
    "library": {
        "create_sql": """
CREATE TABLE authors (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, nationality TEXT, birth_year INTEGER
);
CREATE TABLE books (
    id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER NOT NULL,
    genre TEXT NOT NULL, published_year INTEGER, isbn TEXT, copies_available INTEGER DEFAULT 1,
    FOREIGN KEY (author_id) REFERENCES authors(id)
);
CREATE TABLE members (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL,
    membership_type TEXT DEFAULT 'basic', join_date TEXT NOT NULL, is_active INTEGER DEFAULT 1
);
CREATE TABLE loans (
    id INTEGER PRIMARY KEY, book_id INTEGER NOT NULL, member_id INTEGER NOT NULL,
    loan_date TEXT NOT NULL, due_date TEXT NOT NULL, return_date TEXT,
    FOREIGN KEY (book_id) REFERENCES books(id), FOREIGN KEY (member_id) REFERENCES members(id)
);
CREATE TABLE fines (
    id INTEGER PRIMARY KEY, loan_id INTEGER NOT NULL, amount REAL NOT NULL,
    paid INTEGER DEFAULT 0, paid_date TEXT,
    FOREIGN KEY (loan_id) REFERENCES loans(id)
);
CREATE TABLE reservations (
    id INTEGER PRIMARY KEY, book_id INTEGER NOT NULL, member_id INTEGER NOT NULL,
    reserved_date TEXT NOT NULL, status TEXT DEFAULT 'active',
    FOREIGN KEY (book_id) REFERENCES books(id), FOREIGN KEY (member_id) REFERENCES members(id)
);
""",
        "seed_sql": """
INSERT INTO authors VALUES
(1,'George Orwell','British',1903),(2,'Jane Austen','British',1775),
(3,'Haruki Murakami','Japanese',1949),(4,'Gabriel Garcia Marquez','Colombian',1927),
(5,'Toni Morrison','American',1931);

INSERT INTO books VALUES
(1,'1984',1,'Fiction',1949,'978-0451524935',3),
(2,'Pride and Prejudice',2,'Fiction',1813,'978-0141439518',2),
(3,'Norwegian Wood',3,'Fiction',1987,NULL,1),
(4,'One Hundred Years of Solitude',4,'Fiction',1967,'978-0060883287',2),
(5,'Beloved',5,'Fiction',1987,'978-1400033416',1),
(6,'Animal Farm',1,'Fiction',1945,'978-0451526342',4),
(7,'Kafka on the Shore',3,'Fiction',2002,NULL,2),
(8,'Love in the Time of Cholera',4,'Fiction',1985,'978-0307389732',1),
(9,'Song of Solomon',5,'Fiction',1977,NULL,0),
(10,'Sense and Sensibility',2,'Fiction',1811,'978-0141439662',3);

INSERT INTO members VALUES
(1,'Alice Reed','alice@lib.com','premium','2022-01-15',1),
(2,'Bob Shaw','bob@lib.com','basic','2022-06-20',1),
(3,'Clara Ruiz','clara@lib.com','premium','2023-01-10',1),
(4,'David Tan','david@lib.com','basic','2023-03-05',1),
(5,'Eva Nowak','eva@lib.com','basic','2023-07-22',0),
(6,'Fred Obi','fred@lib.com','premium','2024-01-08',1),
(7,'Gina Lim','gina@lib.com','basic','2024-02-14',1),
(8,'Hank Yoo','hank@lib.com','basic','2024-03-01',1);

INSERT INTO loans VALUES
(1,1,1,'2024-01-15','2024-02-15','2024-02-10'),
(2,3,2,'2024-01-20','2024-02-20',NULL),
(3,5,1,'2024-02-01','2024-03-01','2024-03-05'),
(4,2,3,'2024-02-10','2024-03-10','2024-03-08'),
(5,7,4,'2024-03-01','2024-04-01',NULL),
(6,1,2,'2024-03-05','2024-04-05','2024-04-01'),
(7,4,6,'2024-03-10','2024-04-10',NULL),
(8,6,1,'2024-03-15','2024-04-15','2024-04-12'),
(9,8,3,'2024-03-20','2024-04-20',NULL),
(10,10,7,'2024-04-01','2024-05-01','2024-04-28'),
(11,1,4,'2024-04-05','2024-05-05',NULL),
(12,9,5,'2023-06-01','2023-07-01',NULL);

INSERT INTO fines VALUES
(1,3,2.50,1,'2024-03-10'),(2,2,15.00,0,NULL),
(3,12,50.00,0,NULL),(4,6,0.00,1,'2024-04-01'),
(5,5,8.00,0,NULL);

INSERT INTO reservations VALUES
(1,3,3,'2024-02-25','fulfilled'),(2,9,1,'2024-03-01','active'),
(3,7,2,'2024-03-15','active'),(4,5,6,'2024-04-01','cancelled'),
(5,1,7,'2024-04-10','active');
""",
        "schema_info": (
            "Tables: authors (id, name, nationality, birth_year), "
            "books (id, title, author_id, genre, published_year, isbn, copies_available), "
            "members (id, name, email, membership_type, join_date, is_active), "
            "loans (id, book_id, member_id, loan_date, due_date, return_date), "
            "fines (id, loan_id, amount, paid, paid_date), "
            "reservations (id, book_id, member_id, reserved_date, status)"
        ),
    },
}


TASKS = [

    
    {
        "task_type": "syntax_fix", "difficulty": "easy", "schema_name": "hr",
        "description": "Get all salary records where the amount is between 70000 and 95000.",
        "broken_query": "SELECT employee_id, amount FROM salaries WHERE amount BETWEEN 70000 TO 95000",
        "correct_query": "SELECT employee_id, amount FROM salaries WHERE amount BETWEEN 70000 AND 95000",
        "hint": "There is a syntax error in the range filter.",
    },
    {
        "task_type": "syntax_fix", "difficulty": "easy", "schema_name": "hr",
        "description": "Find all employees whose name starts with 'Ali'.",
        "broken_query": "SELECT name FROM employees WHERE name LIKE '%Ali_'",
        "correct_query": "SELECT name FROM employees WHERE name LIKE 'Ali%'",
        "hint": "The wildcard pattern doesn't match the description.",
    },
    {
        "task_type": "syntax_fix", "difficulty": "easy", "schema_name": "hr",
        "description": "Get all employees who work in Engineering or HR.",
        "broken_query": "SELECT name, department FROM employees WHERE department IN 'Engineering', 'HR'",
        "correct_query": "SELECT name, department FROM employees WHERE department IN ('Engineering', 'HR')",
        "hint": "The IN clause has a syntax issue.",
    },
    {
        "task_type": "syntax_fix", "difficulty": "easy", "schema_name": "hr",
        "description": "Get a unique list of department names from the employees table.",
        "broken_query": "SELECT name, DISTINCT department FROM employees",
        "correct_query": "SELECT DISTINCT department FROM employees",
        "hint": "The SELECT clause has a keyword placement error.",
    },
    {
        "task_type": "syntax_fix", "difficulty": "easy", "schema_name": "hr",
        "description": "Create a label combining each employee's name and department separated by a dash.",
        "broken_query": "SELECT name + ' - ' + department AS label FROM employees",
        "correct_query": "SELECT name || ' - ' || department AS label FROM employees",
        "hint": "The concatenation operator isn't correct for this database engine.",
    },
    {
        "task_type": "syntax_fix", "difficulty": "easy", "schema_name": "hr",
        "description": "Create a display label combining each employee's name and department with a dash separator.",
        "broken_query": "SELECT name || department AS label FROM employees",
        "correct_query": "SELECT name || ' - ' || department AS label FROM employees",
        "hint": "The output doesn't match what the description asks for.",
    },
    {
        "task_type": "syntax_fix", "difficulty": "easy", "schema_name": "hr",
        "description": "Combine employee names and client names into one unified list with a type label.",
        "broken_query": "SELECT name, 'employee' as type, department FROM employees UNION SELECT name, 'client' FROM clients",
        "correct_query": "SELECT name, 'employee' as type, department FROM employees UNION SELECT name, 'client' as type, industry FROM clients",
        "hint": "The UNION fails to execute.",
    },
    {
        "task_type": "syntax_fix", "difficulty": "easy", "schema_name": "hr",
        "description": "Find all top-level employees who have no manager assigned.",
        "broken_query": "SELECT name FROM employees WHERE manager_id = NULL",
        "correct_query": "SELECT name FROM employees WHERE manager_id IS NULL",
        "hint": "The query returns no rows even though some employees have no manager.",
    },
    {
        "task_type": "syntax_fix", "difficulty": "easy", "schema_name": "hr",
        "description": "Show each leave request's employee ID and who approved it, defaulting to 0 if no approver is recorded.",
        "broken_query": "SELECT employee_id, IFNULL(0, approved_by) FROM leave_requests",
        "correct_query": "SELECT employee_id, IFNULL(approved_by, 0) FROM leave_requests",
        "hint": "The fallback value isn't being applied correctly when the approver is missing.",
    },

    
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "hr",
        "description": "Calculate the ratio of each department's total salary to its budget, avoiding division by zero when budget is 0.",
        "broken_query": "SELECT d.name, SUM(e.salary) / NULLIF(SUM(e.salary), 0) FROM employees e JOIN departments d ON e.department = d.name GROUP BY d.name",
        "correct_query": "SELECT d.name, SUM(e.salary) / NULLIF(d.budget, 0) FROM employees e JOIN departments d ON e.department = d.name GROUP BY d.name",
        "hint": "The division-by-zero protection is being applied to the wrong value.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "hr",
        "description": "Count how many employees hold a certified skill in each skill category.",
        "broken_query": "SELECT s.category, COUNT(*) as certified_count FROM employee_skills es JOIN skills s ON es.skill_id = s.id GROUP BY s.category",
        "correct_query": "SELECT s.category, COUNT(CASE WHEN es.certified = 1 THEN 1 END) as certified_count FROM skills s LEFT JOIN employee_skills es ON s.id = es.skill_id GROUP BY s.category",
        "hint": "The counts are too high and some categories are missing entirely.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "hr",
        "description": "Calculate the percentage of the 100000 budget used for each project milestone.",
        "broken_query": "SELECT name, (budget_used / 100000.0) * 100 AS utilization_pct FROM project_milestones",
        "correct_query": "SELECT name, (COALESCE(budget_used, 0) / 100000.0) * 100 AS utilization_pct FROM project_milestones",
        "hint": "Some milestones show NULL instead of a percentage.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "hr",
        "description": "Show each employee's name, department, and their total salary paid from the salary history table.",
        "broken_query": "SELECT e.name, e.department, SUM(s.amount) as total_paid FROM employees e JOIN salaries s ON e.id = s.employee_id GROUP BY e.department",
        "correct_query": "SELECT e.name, e.department, SUM(s.amount) as total_paid FROM employees e JOIN salaries s ON e.id = s.employee_id GROUP BY e.id, e.name, e.department",
        "hint": "The query returns fewer rows than expected — employee names are getting collapsed.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "hr",
        "description": "Count approved and rejected leave requests separately per department in a single query.",
        "broken_query": "SELECT e.department, COUNT(*) as approved FROM leave_requests lr JOIN employees e ON lr.employee_id = e.id WHERE lr.status = 'approved' GROUP BY e.department",
        "correct_query": "SELECT e.department, SUM(CASE WHEN lr.status = 'approved' THEN 1 ELSE 0 END) as approved, SUM(CASE WHEN lr.status = 'rejected' THEN 1 ELSE 0 END) as rejected FROM leave_requests lr JOIN employees e ON lr.employee_id = e.id GROUP BY e.department",
        "hint": "The query only shows one status category and the counts seem wrong.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "hr",
        "description": "Get the average review score given by each reviewer.",
        "broken_query": "SELECT reviewer_id, AVG(reviewer_id) as avg_score FROM performance_reviews GROUP BY reviewer_id",
        "correct_query": "SELECT reviewer_id, AVG(score) as avg_score FROM performance_reviews GROUP BY reviewer_id",
        "hint": "The averages look suspiciously like ID numbers.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "hr",
        "description": "Count how many unique employees are assigned to each project.",
        "broken_query": "SELECT project_id, COUNT(employee_id) as unique_employees FROM assignments GROUP BY project_id",
        "correct_query": "SELECT project_id, COUNT(DISTINCT employee_id) as unique_employees FROM assignments GROUP BY project_id",
        "hint": "Some project counts are higher than expected.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "hr",
        "description": "Get each employee's name alongside their manager's name. Employees with no manager should still appear.",
        "broken_query": "SELECT e.name as employee, m.name as manager FROM employees e JOIN employees m ON e.id = m.id",
        "correct_query": "SELECT e.name as employee, m.name as manager FROM employees e LEFT JOIN employees m ON e.manager_id = m.id",
        "hint": "Every employee shows themselves as their own manager, and top-level employees are missing.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "hr",
        "description": "Get each employee's name along with the names of the skills they possess.",
        "broken_query": "SELECT e.name, s.name as skill FROM employees e JOIN employee_skills es ON e.id = es.skill_id JOIN skills s ON es.skill_id = s.id",
        "correct_query": "SELECT e.name, s.name as skill FROM employees e JOIN employee_skills es ON e.id = es.employee_id JOIN skills s ON es.skill_id = s.id",
        "hint": "The results show wrong employee-skill pairings.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "hr",
        "description": "Get each project's name and its department's name.",
        "broken_query": "SELECT p.name as project, d.name as department FROM projects p JOIN departments d ON p.department_id = d.name",
        "correct_query": "SELECT p.name as project, d.name as department FROM projects p JOIN departments d ON p.department_id = d.id",
        "hint": "The join returns very few or no results.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "hr",
        "description": "Get all employees who were hired in the year 2020.",
        "broken_query": "SELECT name, hire_date FROM employees WHERE strftime('%y', hire_date) = '2020'",
        "correct_query": "SELECT name, hire_date FROM employees WHERE strftime('%Y', hire_date) = '2020'",
        "hint": "The query returns no results even though employees were hired in 2020.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "hr",
        "description": "Find leave requests that started after March 1st 2024.",
        "broken_query": "SELECT * FROM leave_requests WHERE start_date > '01-03-2024'",
        "correct_query": "SELECT * FROM leave_requests WHERE start_date > '2024-03-01'",
        "hint": "The date comparison isn't producing the expected results.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "hr",
        "description": "Calculate how many days overdue each completed milestone was (completed after its due date).",
        "broken_query": "SELECT name, julianday(due_date) - julianday(completed_date) as days_overdue FROM project_milestones WHERE completed_date IS NOT NULL",
        "correct_query": "SELECT name, julianday(completed_date) - julianday(due_date) as days_overdue FROM project_milestones WHERE completed_date IS NOT NULL",
        "hint": "Late milestones show negative numbers instead of positive.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "hr",
        "description": "Find leave requests that last more than 7 days (end date more than 7 days after start date).",
        "broken_query": "SELECT * FROM leave_requests WHERE end_date > date(start_date, '-7 days')",
        "correct_query": "SELECT * FROM leave_requests WHERE end_date > date(start_date, '+7 days')",
        "hint": "The query returns too many rows.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "hr",
        "description": "Get the first 3 characters of each employee's name as a name code.",
        "broken_query": "SELECT name, SUBSTR(name, 0, 3) as name_code FROM employees",
        "correct_query": "SELECT name, SUBSTR(name, 1, 3) as name_code FROM employees",
        "hint": "The name codes are only 2 characters long.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "hr",
        "description": "Find all employees in the 'engineering' department using a case-insensitive search.",
        "broken_query": "SELECT name FROM employees WHERE department = 'engineering'",
        "correct_query": "SELECT name FROM employees WHERE LOWER(department) = 'engineering'",
        "hint": "The query returns no results.",
    },

    
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "hr",
        "description": "Get employee names and the names of skills they are certified in, going through the bridge table.",
        "broken_query": "SELECT e.name, s.name as skill FROM employees e JOIN skills s ON e.id = s.id WHERE s.id IN (SELECT skill_id FROM employee_skills WHERE certified = 1)",
        "correct_query": "SELECT e.name, s.name as skill FROM employees e JOIN employee_skills es ON e.id = es.employee_id JOIN skills s ON es.skill_id = s.id WHERE es.certified = 1",
        "hint": "The results are incorrect — the query takes a shortcut through the tables.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "hr",
        "description": "List all departments and the count of their active projects, including departments that have zero active projects.",
        "broken_query": "SELECT d.name, COUNT(p.id) as active_projects FROM departments d LEFT JOIN projects p ON d.id = p.department_id WHERE p.status = 'active' GROUP BY d.name",
        "correct_query": "SELECT d.name, COUNT(p.id) as active_projects FROM departments d LEFT JOIN projects p ON d.id = p.department_id AND p.status = 'active' GROUP BY d.name",
        "hint": "Departments with zero active projects don't appear in the output.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "hr",
        "description": "Find active employees who are not assigned to any project.",
        "broken_query": "SELECT name FROM employees WHERE is_active = 1 AND id NOT IN (SELECT employee_id FROM assignments)",
        "correct_query": "SELECT name FROM employees e WHERE is_active = 1 AND NOT EXISTS (SELECT 1 FROM assignments a WHERE a.employee_id = e.id)",
        "hint": "The query unexpectedly returns zero rows.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "hr",
        "description": "Find employees whose current salary matches the highest recorded salary for the 'senior' pay grade.",
        "broken_query": "SELECT e.name FROM employees e WHERE e.salary = (SELECT s.amount FROM salaries s WHERE s.pay_grade = 'senior')",
        "correct_query": "SELECT e.name FROM employees e WHERE e.salary = (SELECT MAX(s.amount) FROM salaries s WHERE s.pay_grade = 'senior')",
        "hint": "The query throws a runtime error about subquery results.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "hr",
        "description": "Get the average salary amount paid per department from the salary history table.",
        "broken_query": "SELECT dept_avg.department, dept_avg.avg_amount FROM (SELECT e.department, AVG(s.amount) as avg_amount FROM employees e JOIN salaries s ON e.id = s.employee_id GROUP BY e.department)",
        "correct_query": "SELECT dept_avg.department, dept_avg.avg_amount FROM (SELECT e.department, AVG(s.amount) as avg_amount FROM employees e JOIN salaries s ON e.id = s.employee_id GROUP BY e.department) AS dept_avg",
        "hint": "The query fails with a syntax error near the end.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "hr",
        "description": "Find employees who have received at least one performance review.",
        "broken_query": "SELECT e.name FROM employees e WHERE EXISTS (SELECT 1 FROM performance_reviews pr WHERE pr.score > 0)",
        "correct_query": "SELECT e.name FROM employees e WHERE EXISTS (SELECT 1 FROM performance_reviews pr WHERE pr.employee_id = e.id)",
        "hint": "The query returns all employees, including ones who were never reviewed.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "hr",
        "description": "Find departments whose average employee salary is higher than the Engineering department's average salary.",
        "broken_query": "SELECT department, AVG(salary) as avg_sal FROM employees GROUP BY department HAVING AVG(salary) > (SELECT AVG(salary) FROM employees WHERE department = 'HR')",
        "correct_query": "SELECT department, AVG(salary) as avg_sal FROM employees GROUP BY department HAVING AVG(salary) > (SELECT AVG(salary) FROM employees WHERE department = 'Engineering')",
        "hint": "The comparison benchmark seems to be set against the wrong reference point.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "hr",
        "description": "Rank employees by salary within each department so that employees with the same salary share the same rank.",
        "broken_query": "SELECT name, department, salary, ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as salary_rank FROM employees",
        "correct_query": "SELECT name, department, salary, RANK() OVER (PARTITION BY department ORDER BY salary DESC) as salary_rank FROM employees",
        "hint": "Employees with identical salaries get different rank numbers.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "hr",
        "description": "For each performance review, show the review score and the average score for that employee's department.",
        "broken_query": "SELECT pr.employee_id, pr.score, AVG(pr.score) OVER () as dept_avg FROM performance_reviews pr",
        "correct_query": "SELECT pr.employee_id, pr.score, AVG(pr.score) OVER (PARTITION BY e.department) as dept_avg FROM performance_reviews pr JOIN employees e ON pr.employee_id = e.id",
        "hint": "The department average is the same number for every single row.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "hr",
        "description": "Show each salary record alongside the previous salary amount for that employee chronologically.",
        "broken_query": "SELECT employee_id, amount, effective_date, LAG(employee_id) OVER (PARTITION BY employee_id ORDER BY effective_date) as prev_salary FROM salaries",
        "correct_query": "SELECT employee_id, amount, effective_date, LAG(amount) OVER (PARTITION BY employee_id ORDER BY effective_date) as prev_salary FROM salaries",
        "hint": "The previous salary column contains the same number on every row for each employee.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "hr",
        "description": "Rank all employees by salary in descending order with no gaps in the ranking numbers when salaries are equal.",
        "broken_query": "SELECT name, salary, RANK() OVER (ORDER BY salary DESC) as rnk FROM employees",
        "correct_query": "SELECT name, salary, DENSE_RANK() OVER (ORDER BY salary DESC) as rnk FROM employees",
        "hint": "The ranking skips numbers after tied employees.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "hr",
        "description": "For each milestone show the total budget used including all previous milestones and the current one (cumulative).",
        "broken_query": "SELECT name, budget_used, SUM(budget_used) OVER (ORDER BY due_date ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING) as running_total FROM project_milestones",
        "correct_query": "SELECT name, budget_used, SUM(budget_used) OVER (ORDER BY due_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_total FROM project_milestones",
        "hint": "The running total decreases as you go down the rows instead of increasing.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "hr",
        "description": "Divide employees into 4 salary quartiles from lowest to highest paid.",
        "broken_query": "SELECT name, salary, NTILE(10) OVER (ORDER BY salary) as quartile FROM employees",
        "correct_query": "SELECT name, salary, NTILE(4) OVER (ORDER BY salary) as quartile FROM employees",
        "hint": "The quartile values go up to 10 instead of 4.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "hr",
        "description": "Find departments whose total salary bill exceeds 200000.",
        "broken_query": "WITH dept_salaries AS (SELECT department, SUM(salary) as total FROM employees GROUP BY department) SELECT department, total FROM employees WHERE total > 200000",
        "correct_query": "WITH dept_salaries AS (SELECT department, SUM(salary) as total FROM employees GROUP BY department) SELECT department, total FROM dept_salaries WHERE total > 200000",
        "hint": "The query errors out — it can't find a column.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "hr",
        "description": "Find employees who earn above the company average salary AND score above the average review score.",
        "broken_query": "WITH avg_salary AS (SELECT AVG(salary) as avg_sal FROM employees), avg_score AS (SELECT AVG(score) as avg_sc FROM performance_reviews) SELECT e.name FROM employees e JOIN performance_reviews pr ON e.id = pr.employee_id WHERE e.salary > (SELECT avg_sal FROM avg_score) AND pr.score > (SELECT avg_sc FROM avg_salary)",
        "correct_query": "WITH avg_salary AS (SELECT AVG(salary) as avg_sal FROM employees), avg_score AS (SELECT AVG(score) as avg_sc FROM performance_reviews) SELECT e.name FROM employees e JOIN performance_reviews pr ON e.id = pr.employee_id WHERE e.salary > (SELECT avg_sal FROM avg_salary) AND pr.score > (SELECT avg_sc FROM avg_score)",
        "hint": "The query returns wrong results — the comparisons seem mixed up.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "hr",
        "description": "Find projects where the total budget used across all milestones exceeds 50000.",
        "broken_query": "WITH milestone_totals AS (SELECT project_id, SUM(budget_used) as total_budget FROM project_milestones GROUP BY project_id) SELECT p.name FROM projects p JOIN milestone_totals mt ON p.id = mt.project_id WHERE mt.total > 50000",
        "correct_query": "WITH milestone_totals AS (SELECT project_id, SUM(budget_used) as total_budget FROM project_milestones GROUP BY project_id) SELECT p.name FROM projects p JOIN milestone_totals mt ON p.id = mt.project_id WHERE mt.total_budget > 50000",
        "hint": "The query errors on a missing column reference.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "hr",
        "description": "Find employee IDs that have assignments but do NOT have any performance reviews on record.",
        "broken_query": "SELECT employee_id FROM performance_reviews EXCEPT SELECT employee_id FROM assignments WHERE employee_id IS NOT NULL",
        "correct_query": "SELECT employee_id FROM assignments WHERE employee_id IS NOT NULL EXCEPT SELECT employee_id FROM performance_reviews",
        "hint": "The results show the opposite of what was asked.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "hr",
        "description": "Find employees who have both a performance review AND at least one leave request on record.",
        "broken_query": "SELECT name FROM employees INTERSECT SELECT employee_id FROM performance_reviews",
        "correct_query": "SELECT DISTINCT e.name FROM employees e JOIN performance_reviews pr ON e.id = pr.employee_id JOIN leave_requests lr ON e.id = lr.employee_id",
        "hint": "The INTERSECT produces incompatible results.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "hr",
        "description": "Find active employees who are not assigned to any project.",
        "broken_query": "SELECT employee_id FROM assignments EXCEPT SELECT id FROM employees WHERE is_active = 1",
        "correct_query": "SELECT id FROM employees WHERE is_active = 1 EXCEPT SELECT employee_id FROM assignments",
        "hint": "The query returns assignment IDs that don't match active employees.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "hr",
        "description": "List all salary figures from both the current employee salary column and the historical salary records table.",
        "broken_query": "SELECT name, salary FROM employees UNION ALL SELECT employee_id, amount FROM salaries",
        "correct_query": "SELECT CAST(id AS TEXT) as identifier, salary FROM employees UNION ALL SELECT CAST(employee_id AS TEXT) as identifier, amount FROM salaries",
        "hint": "The first column mixes text names and numeric IDs, causing sorting issues.",
    },

    
    {
        "task_type": "optimization", "difficulty": "hard", "schema_name": "hr",
        "description": "Find active employees not assigned to any project. Current query fails silently when NULL values exist in assignments.",
        "broken_query": "SELECT name FROM employees WHERE is_active = 1 AND id NOT IN (SELECT employee_id FROM assignments)",
        "correct_query": "SELECT name FROM employees e WHERE is_active = 1 AND NOT EXISTS (SELECT 1 FROM assignments a WHERE a.employee_id = e.id)",
        "hint": "The query returns no results at all.",
    },
    {
        "task_type": "optimization", "difficulty": "hard", "schema_name": "hr",
        "description": "Find departments that have at least one project. Current query uses a slow GROUP BY + HAVING pattern.",
        "broken_query": "SELECT d.name FROM departments d LEFT JOIN projects p ON d.id = p.department_id GROUP BY d.name HAVING COUNT(p.id) > 0",
        "correct_query": "SELECT d.name FROM departments d WHERE EXISTS (SELECT 1 FROM projects p WHERE p.department_id = d.id)",
        "hint": "Rewrite for better performance.",
    },
    {
        "task_type": "optimization", "difficulty": "hard", "schema_name": "hr",
        "description": "Find employees earning above average, show their score compared to average, with the same salary average subquery repeated three times. Rewrite using a CTE.",
        "broken_query": "SELECT e.name, e.salary, (SELECT AVG(salary) FROM employees) as avg_sal, pr.score, (SELECT AVG(score) FROM performance_reviews) as avg_sc FROM employees e LEFT JOIN performance_reviews pr ON e.id = pr.employee_id WHERE e.salary > (SELECT AVG(salary) FROM employees)",
        "correct_query": "WITH averages AS (SELECT (SELECT AVG(salary) FROM employees) as avg_sal, (SELECT AVG(score) FROM performance_reviews) as avg_sc) SELECT e.name, e.salary, a.avg_sal, pr.score, a.avg_sc FROM employees e LEFT JOIN performance_reviews pr ON e.id = pr.employee_id CROSS JOIN averages a WHERE e.salary > a.avg_sal",
        "hint": "Eliminate the repeated computation.",
    },
    {
        "task_type": "optimization", "difficulty": "hard", "schema_name": "hr",
        "description": "Find employees in departments starting with 'Eng'. Current query has a leading wildcard killing index use.",
        "broken_query": "SELECT name, department FROM employees WHERE department LIKE '%Eng%'",
        "correct_query": "SELECT name, department FROM employees WHERE department LIKE 'Eng%'",
        "hint": "Optimize the pattern match for index usage.",
    },
    {
        "task_type": "optimization", "difficulty": "hard", "schema_name": "hr",
        "description": "Get the highest review score per employee. Current query uses a slow correlated subquery with ORDER BY + LIMIT 1.",
        "broken_query": "SELECT e.name, (SELECT pr.score FROM performance_reviews pr WHERE pr.employee_id = e.id ORDER BY pr.score DESC LIMIT 1) as top_score FROM employees e",
        "correct_query": "SELECT e.name, MAX(pr.score) as top_score FROM employees e LEFT JOIN performance_reviews pr ON e.id = pr.employee_id GROUP BY e.id, e.name",
        "hint": "Replace the per-row subquery with a single-pass approach.",
    },
    {
        "task_type": "optimization", "difficulty": "hard", "schema_name": "hr",
        "description": "Find all employees in Engineering or Sales. Current query uses OR which blocks index optimization on the department column.",
        "broken_query": "SELECT name, department FROM employees WHERE department = 'Engineering' OR department = 'Sales'",
        "correct_query": "SELECT name, department FROM employees WHERE department = 'Engineering' UNION ALL SELECT name, department FROM employees WHERE department = 'Sales'",
        "hint": "Split for better index utilization.",
    },

    
    {
        "task_type": "logic_fix", "difficulty": "expert", "schema_name": "hr",
        "description": "Calculate the running total of budget used across milestones ordered by due date.",
        "broken_query": "SELECT name, budget_used, SUM(budget_used) OVER () as running_total FROM project_milestones",
        "correct_query": "SELECT name, budget_used, SUM(COALESCE(budget_used, 0)) OVER (ORDER BY due_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_total FROM project_milestones",
        "hint": "The running total is the same value on every row, and NULLs propagate.",
    },
    {
        "task_type": "logic_fix", "difficulty": "expert", "schema_name": "hr",
        "description": "For each employee show their most recent (latest by date) salary from the salary history.",
        "broken_query": "SELECT DISTINCT employee_id, LAST_VALUE(amount) OVER (PARTITION BY employee_id ORDER BY effective_date) as latest_salary FROM salaries",
        "correct_query": "SELECT DISTINCT employee_id, LAST_VALUE(amount) OVER (PARTITION BY employee_id ORDER BY effective_date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as latest_salary FROM salaries",
        "hint": "The results don't show the actual latest salary for each employee.",
    },
    {
        "task_type": "logic_fix", "difficulty": "expert", "schema_name": "hr",
        "description": "Find all employees who report directly or indirectly to the employee with id = 1 (full org hierarchy traversal).",
        "broken_query": "WITH RECURSIVE org AS (SELECT id, name, manager_id FROM employees WHERE manager_id IS NOT NULL UNION ALL SELECT e.id, e.name, e.manager_id FROM employees e JOIN org ON e.manager_id = org.id) SELECT name FROM org",
        "correct_query": "WITH RECURSIVE org AS (SELECT id, name, manager_id FROM employees WHERE id = 1 UNION ALL SELECT e.id, e.name, e.manager_id FROM employees e JOIN org ON e.manager_id = org.id) SELECT name FROM org WHERE id != 1",
        "hint": "The query returns too many employees.",
    },
    {
        "task_type": "logic_fix", "difficulty": "expert", "schema_name": "hr",
        "description": "Build the full org hierarchy with depth levels starting from the top-level manager.",
        "broken_query": "WITH RECURSIVE hierarchy AS (SELECT id, name, manager_id, 1 as level FROM employees WHERE manager_id IS NULL UNION ALL SELECT e.id, e.name, e.manager_id, h.level FROM employees e JOIN hierarchy h ON e.manager_id = h.id) SELECT name, level FROM hierarchy",
        "correct_query": "WITH RECURSIVE hierarchy AS (SELECT id, name, manager_id, 0 as level FROM employees WHERE manager_id IS NULL UNION ALL SELECT e.id, e.name, e.manager_id, h.level + 1 FROM employees e JOIN hierarchy h ON e.manager_id = h.id) SELECT name, level FROM hierarchy",
        "hint": "All employees have the same depth level.",
    },
    {
        "task_type": "logic_fix", "difficulty": "expert", "schema_name": "hr",
        "description": "Get the second highest salary within each department.",
        "broken_query": "SELECT department, MAX(salary) as second_highest FROM employees WHERE salary < (SELECT MAX(salary) FROM employees) GROUP BY department",
        "correct_query": "SELECT department, salary as second_highest FROM (SELECT department, salary, DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) as rnk FROM employees) WHERE rnk = 2",
        "hint": "The query uses a global maximum instead of per-department logic.",
    },
    {
        "task_type": "logic_fix", "difficulty": "expert", "schema_name": "hr",
        "description": "Find employees whose most recent salary is lower than their very first recorded salary.",
        "broken_query": "SELECT e.name FROM employees e JOIN salaries s ON e.id = s.employee_id WHERE s.amount < (SELECT MIN(amount) FROM salaries WHERE employee_id = e.id)",
        "correct_query": "SELECT e.name FROM employees e WHERE (SELECT amount FROM salaries WHERE employee_id = e.id ORDER BY effective_date DESC LIMIT 1) < (SELECT amount FROM salaries WHERE employee_id = e.id ORDER BY effective_date ASC LIMIT 1)",
        "hint": "The query always returns zero rows.",
    },
    {
        "task_type": "logic_fix", "difficulty": "expert", "schema_name": "hr",
        "description": "Find managers who earn less than at least one of their direct reports.",
        "broken_query": "SELECT DISTINCT m.name as manager FROM employees e JOIN employees m ON e.id = m.manager_id WHERE e.salary > m.salary",
        "correct_query": "SELECT DISTINCT m.name as manager FROM employees e JOIN employees m ON e.manager_id = m.id WHERE e.salary > m.salary",
        "hint": "The join condition has the relationship backwards.",
    },
    {
        "task_type": "logic_fix", "difficulty": "expert", "schema_name": "hr",
        "description": "Find employees who are assigned to every single active project (relational division).",
        "broken_query": "SELECT e.name FROM employees e JOIN assignments a ON e.id = a.employee_id JOIN projects p ON a.project_id = p.id WHERE p.status = 'active' GROUP BY e.id, e.name HAVING COUNT(p.id) > 1",
        "correct_query": "SELECT e.name FROM employees e WHERE NOT EXISTS (SELECT p.id FROM projects p WHERE p.status = 'active' AND NOT EXISTS (SELECT 1 FROM assignments a WHERE a.employee_id = e.id AND a.project_id = p.id))",
        "hint": "The query returns employees with more than one active project, not those assigned to ALL active projects.",
    },
    {
        "task_type": "logic_fix", "difficulty": "expert", "schema_name": "hr",
        "description": "Find departments where every active employee has at least one performance review on record.",
        "broken_query": "SELECT DISTINCT e.department FROM employees e JOIN performance_reviews pr ON e.id = pr.employee_id WHERE e.is_active = 1",
        "correct_query": "SELECT e.department FROM employees e WHERE e.is_active = 1 GROUP BY e.department HAVING COUNT(DISTINCT e.id) = (SELECT COUNT(DISTINCT pr2.employee_id) FROM performance_reviews pr2 JOIN employees e2 ON pr2.employee_id = e2.id WHERE e2.department = e.department AND e2.is_active = 1)",
        "hint": "The query returns departments where at least one employee has a review, not where every employee has one.",
    },
    {
        "task_type": "logic_fix", "difficulty": "expert", "schema_name": "hr",
        "description": "Find all pairs of employees who share at least one skill but work in different departments.",
        "broken_query": "SELECT e1.name, e2.name FROM employees e1 JOIN employees e2 ON e1.id != e2.id JOIN employee_skills es ON e1.id = es.employee_id WHERE e1.department != e2.department",
        "correct_query": "SELECT DISTINCT e1.name, e2.name FROM employees e1 JOIN employee_skills es1 ON e1.id = es1.employee_id JOIN employee_skills es2 ON es1.skill_id = es2.skill_id AND es1.employee_id != es2.employee_id JOIN employees e2 ON es2.employee_id = e2.id WHERE e1.department != e2.department AND e1.id < e2.id",
        "hint": "The query doesn't verify a shared skill exists.",
    },
    {
        "task_type": "optimization", "difficulty": "expert", "schema_name": "hr",
        "description": "Show total, approved, rejected, and pending leave request counts per department in a single query using conditional aggregation.",
        "broken_query": "SELECT e.department, COUNT(*) as total, (SELECT COUNT(*) FROM leave_requests lr2 JOIN employees e2 ON lr2.employee_id = e2.id WHERE e2.department = e.department AND lr2.status = 'approved') as approved FROM leave_requests lr JOIN employees e ON lr.employee_id = e.id GROUP BY e.department",
        "correct_query": "SELECT e.department, COUNT(*) as total, SUM(CASE WHEN lr.status = 'approved' THEN 1 ELSE 0 END) as approved, SUM(CASE WHEN lr.status = 'rejected' THEN 1 ELSE 0 END) as rejected, SUM(CASE WHEN lr.status = 'pending' THEN 1 ELSE 0 END) as pending FROM leave_requests lr JOIN employees e ON lr.employee_id = e.id GROUP BY e.department",
        "hint": "Replace the correlated subqueries with a single-pass approach.",
    },
    {
        "task_type": "optimization", "difficulty": "expert", "schema_name": "hr",
        "description": "Rank employees by salary within their department. Current query uses an inefficient self-join count to compute rank.",
        "broken_query": "SELECT e1.name, e1.department, e1.salary, COUNT(e2.id) + 1 as salary_rank FROM employees e1 LEFT JOIN employees e2 ON e1.department = e2.department AND e2.salary > e1.salary GROUP BY e1.id, e1.name, e1.department, e1.salary",
        "correct_query": "SELECT name, department, salary, RANK() OVER (PARTITION BY department ORDER BY salary DESC) as salary_rank FROM employees",
        "hint": "Replace the O(n²) self-join with a window function.",
    },
    {
        "task_type": "logic_fix", "difficulty": "expert", "schema_name": "hr",
        "description": "Find the employee who has had the most distinct salary change events over time.",
        "broken_query": "SELECT employee_id, COUNT(*) as changes FROM salaries GROUP BY employee_id ORDER BY changes DESC LIMIT 1",
        "correct_query": "SELECT employee_id, COUNT(DISTINCT effective_date) as changes FROM salaries GROUP BY employee_id ORDER BY changes DESC LIMIT 1",
        "hint": "The count is inflated by duplicate records.",
    },

    
    {
        "task_type": "syntax_fix", "difficulty": "easy", "schema_name": "hospital",
        "description": "Get all patients whose age is between 30 and 60.",
        "broken_query": "SELECT name, age FROM patients WHERE age BETWEEN 30 TO 60",
        "correct_query": "SELECT name, age FROM patients WHERE age BETWEEN 30 AND 60",
        "hint": "The range filter has a syntax error.",
    },
    {
        "task_type": "syntax_fix", "difficulty": "easy", "schema_name": "hospital",
        "description": "Find all patients who have not been discharged and have a NULL blood type.",
        "broken_query": "SELECT name FROM patients WHERE is_discharged = 0 AND blood_type = NULL",
        "correct_query": "SELECT name FROM patients WHERE is_discharged = 0 AND blood_type IS NULL",
        "hint": "The query returns no patients even though some match.",
    },
    {
        "task_type": "syntax_fix", "difficulty": "easy", "schema_name": "hospital",
        "description": "List all doctors sorted by years of experience.",
        "broken_query": "SELECT name, specialization, years_experience FROM doctors ORDERY BY years_experience DESC",
        "correct_query": "SELECT name, specialization, years_experience FROM doctors ORDER BY years_experience DESC",
        "hint": "The query has a syntax error.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "hospital",
        "description": "Count how many appointments each doctor has for each status (completed, scheduled, cancelled).",
        "broken_query": "SELECT d.name, COUNT(*) as completed FROM appointments a JOIN doctors d ON a.doctor_id = d.id WHERE a.status = 'completed' GROUP BY d.name",
        "correct_query": "SELECT d.name, SUM(CASE WHEN a.status = 'completed' THEN 1 ELSE 0 END) as completed, SUM(CASE WHEN a.status = 'scheduled' THEN 1 ELSE 0 END) as scheduled, SUM(CASE WHEN a.status = 'cancelled' THEN 1 ELSE 0 END) as cancelled FROM appointments a JOIN doctors d ON a.doctor_id = d.id GROUP BY d.name",
        "hint": "Only completed appointments appear — two other statuses are missing.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "hospital",
        "description": "Calculate the total prescribed quantity per medication, treating NULL quantities as 0.",
        "broken_query": "SELECT m.name, SUM(p.quantity) as total_qty FROM medications m LEFT JOIN prescriptions p ON m.id = p.medication_id GROUP BY m.name",
        "correct_query": "SELECT m.name, COALESCE(SUM(p.quantity), 0) as total_qty FROM medications m LEFT JOIN prescriptions p ON m.id = p.medication_id GROUP BY m.name",
        "hint": "Some medications show NULL instead of 0 for their total.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "hospital",
        "description": "Show each appointment's patient name and doctor name.",
        "broken_query": "SELECT p.name as patient, d.name as doctor FROM patients p JOIN appointments a ON p.id = a.patient_id JOIN doctors d ON a.doctor_id = d.name",
        "correct_query": "SELECT p.name as patient, d.name as doctor FROM patients p JOIN appointments a ON p.id = a.patient_id JOIN doctors d ON a.doctor_id = d.id",
        "hint": "The join produces very few results.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "hospital",
        "description": "Find all patients admitted after February 2024.",
        "broken_query": "SELECT name, admitted_date FROM patients WHERE strftime('%y', admitted_date) = '2024' AND admitted_date > '02-01-2024'",
        "correct_query": "SELECT name, admitted_date FROM patients WHERE admitted_date > '2024-02-01'",
        "hint": "The date filtering returns no results — both conditions have issues.",
    },
    
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "hospital",
        "description": "List all wards and their head doctor's name, including wards with no head doctor assigned.",
        "broken_query": "SELECT w.name as ward, d.name as head_doctor FROM wards w JOIN doctors d ON w.head_doctor_id = d.id",
        "correct_query": "SELECT w.name as ward, d.name as head_doctor FROM wards w LEFT JOIN doctors d ON w.head_doctor_id = d.id",
        "hint": "Some wards are missing from the output.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "hospital",
        "description": "Find patients who have had appointments with every cardiologist in the hospital.",
        "broken_query": "SELECT p.name FROM patients p JOIN appointments a ON p.id = a.patient_id JOIN doctors d ON a.doctor_id = d.id WHERE d.specialization = 'Cardiology' GROUP BY p.id, p.name HAVING COUNT(d.id) > 1",
        "correct_query": "SELECT p.name FROM patients p WHERE NOT EXISTS (SELECT d.id FROM doctors d WHERE d.specialization = 'Cardiology' AND NOT EXISTS (SELECT 1 FROM appointments a WHERE a.patient_id = p.id AND a.doctor_id = d.id))",
        "hint": "The query checks for more than one cardiology visit, not visits to ALL cardiologists.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "hospital",
        "description": "Show the average patient age per doctor, including doctors who have had no appointments.",
        "broken_query": "SELECT d.name, AVG(p.age) as avg_patient_age FROM doctors d JOIN appointments a ON d.id = a.doctor_id JOIN patients p ON a.patient_id = p.id WHERE a.status != 'cancelled' GROUP BY d.id",
        "correct_query": "SELECT d.name, AVG(p.age) as avg_patient_age FROM doctors d LEFT JOIN appointments a ON d.id = a.doctor_id AND a.status != 'cancelled' LEFT JOIN patients p ON a.patient_id = p.id GROUP BY d.id, d.name",
        "hint": "Doctors with no non-cancelled appointments are missing, and the GROUP BY is incomplete.",
    },
    {
        "task_type": "optimization", "difficulty": "hard", "schema_name": "hospital",
        "description": "Find doctors who have at least one completed appointment. Current query uses GROUP BY + HAVING which is slow.",
        "broken_query": "SELECT d.name FROM doctors d LEFT JOIN appointments a ON d.id = a.doctor_id WHERE a.status = 'completed' GROUP BY d.name HAVING COUNT(a.id) > 0",
        "correct_query": "SELECT d.name FROM doctors d WHERE EXISTS (SELECT 1 FROM appointments a WHERE a.doctor_id = d.id AND a.status = 'completed')",
        "hint": "Rewrite for better performance — eliminate the full aggregation.",
    },
    
    {
        "task_type": "logic_fix", "difficulty": "expert", "schema_name": "hospital",
        "description": "For each doctor, show the running count of their completed appointments ordered by date.",
        "broken_query": "SELECT doctor_id, scheduled_date, COUNT(*) OVER () as running_count FROM appointments",
        "correct_query": "SELECT doctor_id, scheduled_date, COUNT(*) OVER (PARTITION BY doctor_id ORDER BY scheduled_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_count FROM appointments WHERE status = 'completed'",
        "hint": "The count is the same for every row, cancelled/scheduled appointments are included, and it's not partitioned by doctor.",
    },
    {
        "task_type": "logic_fix", "difficulty": "expert", "schema_name": "hospital",
        "description": "Find the second most prescribed medication by total quantity.",
        "broken_query": "SELECT m.name, SUM(p.quantity) as total FROM medications m JOIN prescriptions p ON m.id = p.medication_id GROUP BY m.id, m.name ORDER BY total DESC LIMIT 1 OFFSET 1",
        "correct_query": "SELECT name, total FROM (SELECT m.name, SUM(p.quantity) as total, DENSE_RANK() OVER (ORDER BY SUM(p.quantity) DESC) as rnk FROM medications m JOIN prescriptions p ON m.id = p.medication_id GROUP BY m.id, m.name) WHERE rnk = 2",
        "hint": "If two medications tie for first place, the result is wrong.",
    },
    {
        "task_type": "logic_fix", "difficulty": "expert", "schema_name": "hospital",
        "description": "Find patients who were prescribed controlled medications but whose appointment was not with a doctor from Internal Medicine.",
        "broken_query": "SELECT DISTINCT p.name FROM patients p JOIN appointments a ON p.id = a.patient_id JOIN prescriptions pr ON a.id = pr.appointment_id JOIN medications m ON pr.medication_id = m.id JOIN doctors d ON a.doctor_id = d.id WHERE m.is_controlled = 1 AND d.department = 'Internal Medicine'",
        "correct_query": "SELECT DISTINCT p.name FROM patients p JOIN appointments a ON p.id = a.patient_id JOIN prescriptions pr ON a.id = pr.appointment_id JOIN medications m ON pr.medication_id = m.id JOIN doctors d ON a.doctor_id = d.id WHERE m.is_controlled = 1 AND d.department != 'Internal Medicine'",
        "hint": "The filter condition returns the opposite set of results.",
    },

    
    {
        "task_type": "syntax_fix", "difficulty": "easy", "schema_name": "university",
        "description": "Find all students whose name starts with 'A'.",
        "broken_query": "SELECT name, major FROM students WHERE name LIKE '%A'",
        "correct_query": "SELECT name, major FROM students WHERE name LIKE 'A%'",
        "hint": "The pattern doesn't match what's described.",
    },
    {
        "task_type": "syntax_fix", "difficulty": "easy", "schema_name": "university",
        "description": "Get a unique list of departments from the courses table.",
        "broken_query": "SELECT name, DISTINCT department FROM courses",
        "correct_query": "SELECT DISTINCT department FROM courses",
        "hint": "There's a keyword placement error.",
    },
    {
        "task_type": "syntax_fix", "difficulty": "easy", "schema_name": "university",
        "description": "Get all students in Computer Science or Physics.",
        "broken_query": "SELECT name, major FROM students WHERE major IN 'Computer Science', 'Physics'",
        "correct_query": "SELECT name, major FROM students WHERE major IN ('Computer Science', 'Physics')",
        "hint": "The IN clause has a syntax issue.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "university",
        "description": "Find the highest GPA student in each major.",
        "broken_query": "SELECT major, name, MIN(gpa) as top_gpa FROM students WHERE is_active = 1 AND gpa IS NOT NULL GROUP BY major",
        "correct_query": "SELECT major, name, MAX(gpa) as top_gpa FROM students WHERE is_active = 1 AND gpa IS NOT NULL GROUP BY major",
        "hint": "The results show the lowest GPA students, not the highest.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "university",
        "description": "List all professors and the count of courses they teach, including professors who teach zero courses.",
        "broken_query": "SELECT p.name, COUNT(c.id) as course_count FROM professors p INNER JOIN courses c ON p.id = c.professor_id GROUP BY p.name",
        "correct_query": "SELECT p.name, COUNT(c.id) as course_count FROM professors p LEFT JOIN courses c ON p.id = c.professor_id GROUP BY p.name",
        "hint": "A professor is missing from the results.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "university",
        "description": "Count how many unique students are enrolled in each course.",
        "broken_query": "SELECT course_id, COUNT(student_id) as unique_students FROM enrollments GROUP BY course_id",
        "correct_query": "SELECT course_id, COUNT(DISTINCT student_id) as unique_students FROM enrollments GROUP BY course_id",
        "hint": "Some courses show inflated student counts.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "university",
        "description": "Find students who enrolled in the Fall 2021 semester.",
        "broken_query": "SELECT DISTINCT s.name FROM students s JOIN enrollments e ON s.id = e.student_id WHERE e.semester LIKE '%fall%'",
        "correct_query": "SELECT DISTINCT s.name FROM students s JOIN enrollments e ON s.id = e.student_id WHERE LOWER(e.semester) = 'fall 2021'",
        "hint": "The query matches too many semesters — it finds all fall semesters, not just Fall 2021.",
    },
    # --- HARD ---
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "university",
        "description": "Rank students by GPA within each major, with tied GPAs getting the same rank and no gaps.",
        "broken_query": "SELECT name, major, gpa, ROW_NUMBER() OVER (PARTITION BY major ORDER BY gpa DESC) as gpa_rank FROM students WHERE gpa IS NOT NULL",
        "correct_query": "SELECT name, major, gpa, DENSE_RANK() OVER (PARTITION BY major ORDER BY gpa DESC) as gpa_rank FROM students WHERE gpa IS NOT NULL",
        "hint": "Students with equal GPAs get different rank numbers.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "university",
        "description": "Find students whose GPA is above their major's average GPA.",
        "broken_query": "SELECT name, major, gpa FROM students WHERE gpa > (SELECT AVG(gpa) FROM students) AND gpa IS NOT NULL",
        "correct_query": "SELECT s.name, s.major, s.gpa FROM students s WHERE s.gpa > (SELECT AVG(s2.gpa) FROM students s2 WHERE s2.major = s.major AND s2.gpa IS NOT NULL) AND s.gpa IS NOT NULL",
        "hint": "The query compares against a single average, not a per-major average.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "university",
        "description": "Show each professor and their total enrolled students across all courses, including professors with no enrolled students.",
        "broken_query": "SELECT p.name, COUNT(e.student_id) as total_students FROM professors p JOIN courses c ON p.id = c.professor_id JOIN enrollments e ON c.id = e.course_id GROUP BY p.id",
        "correct_query": "SELECT p.name, COUNT(DISTINCT e.student_id) as total_students FROM professors p LEFT JOIN courses c ON p.id = c.professor_id LEFT JOIN enrollments e ON c.id = e.course_id GROUP BY p.id, p.name",
        "hint": "Professors without students are missing, counts may be inflated, and GROUP BY is incomplete.",
    },
    {
        "task_type": "optimization", "difficulty": "hard", "schema_name": "university",
        "description": "Get the highest grade per student. Current query uses a slow correlated subquery.",
        "broken_query": "SELECT s.name, (SELECT e.grade FROM enrollments e WHERE e.student_id = s.id AND e.grade IS NOT NULL ORDER BY e.grade ASC LIMIT 1) as best_grade FROM students s",
        "correct_query": "SELECT s.name, MIN(e.grade) as best_grade FROM students s LEFT JOIN enrollments e ON s.id = e.student_id AND e.grade IS NOT NULL GROUP BY s.id, s.name",
        "hint": "Replace the per-row subquery with a single-pass approach.",
    },
    
    {
        "task_type": "logic_fix", "difficulty": "expert", "schema_name": "university",
        "description": "Find students who are enrolled in every Computer Science course offered.",
        "broken_query": "SELECT s.name FROM students s JOIN enrollments e ON s.id = e.student_id JOIN courses c ON e.course_id = c.id WHERE c.department = 'Computer Science' GROUP BY s.id, s.name HAVING COUNT(DISTINCT c.id) > 2",
        "correct_query": "SELECT s.name FROM students s WHERE NOT EXISTS (SELECT c.id FROM courses c WHERE c.department = 'Computer Science' AND NOT EXISTS (SELECT 1 FROM enrollments e WHERE e.student_id = s.id AND e.course_id = c.id))",
        "hint": "The query checks for more than 2 CS courses, not ALL of them.",
    },
    {
        "task_type": "logic_fix", "difficulty": "expert", "schema_name": "university",
        "description": "Find majors where every active student has a GPA above 3.0.",
        "broken_query": "SELECT DISTINCT major FROM students WHERE is_active = 1 AND gpa > 3.0",
        "correct_query": "SELECT major FROM students WHERE is_active = 1 GROUP BY major HAVING MIN(COALESCE(gpa, 0)) > 3.0",
        "hint": "The query returns majors where at least one student qualifies, not where ALL qualify.",
    },
    {
        "task_type": "logic_fix", "difficulty": "expert", "schema_name": "university",
        "description": "For each student, show their cumulative credits earned across completed courses, ordered by semester.",
        "broken_query": "SELECT s.name, e.semester, SUM(c.credits) OVER () as cumulative_credits FROM students s JOIN enrollments e ON s.id = e.student_id JOIN courses c ON e.course_id = c.id WHERE e.completed = 1",
        "correct_query": "SELECT s.name, e.semester, SUM(c.credits) OVER (PARTITION BY s.id ORDER BY e.semester ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as cumulative_credits FROM students s JOIN enrollments e ON s.id = e.student_id JOIN courses c ON e.course_id = c.id WHERE e.completed = 1",
        "hint": "The cumulative total is the same on every row — it's a grand total, not a running total per student.",
    },

    
    {
        "task_type": "syntax_fix", "difficulty": "easy", "schema_name": "ecommerce",
        "description": "Get all products in the Electronics or Furniture category.",
        "broken_query": "SELECT name, category, price FROM products WHERE category IN 'Electronics', 'Furniture'",
        "correct_query": "SELECT name, category, price FROM products WHERE category IN ('Electronics', 'Furniture')",
        "hint": "The query has a syntax error in the filter.",
    },
    {
        "task_type": "syntax_fix", "difficulty": "easy", "schema_name": "ecommerce",
        "description": "Create a display label combining product name and category with a colon separator.",
        "broken_query": "SELECT name + ': ' + category AS label FROM products",
        "correct_query": "SELECT name || ': ' || category AS label FROM products",
        "hint": "The concatenation doesn't work in this database engine.",
    },
    {
        "task_type": "syntax_fix", "difficulty": "easy", "schema_name": "ecommerce",
        "description": "Find all suppliers with a NULL contract end date.",
        "broken_query": "SELECT name, country FROM suppliers WHERE contract_end_date = NULL",
        "correct_query": "SELECT name, country FROM suppliers WHERE contract_end_date IS NULL",
        "hint": "The query returns no results.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "ecommerce",
        "description": "Calculate each order item's total cost after applying discount, treating NULL discounts as 0.",
        "broken_query": "SELECT id, (quantity * unit_price) - discount as total FROM order_items",
        "correct_query": "SELECT id, (quantity * unit_price) - COALESCE(discount, 0) as total FROM order_items",
        "hint": "Some rows show NULL totals.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "ecommerce",
        "description": "Show each product's name and its supplier's name.",
        "broken_query": "SELECT p.name as product, s.name as supplier FROM products p JOIN suppliers s ON p.supplier_id = s.name",
        "correct_query": "SELECT p.name as product, s.name as supplier FROM products p JOIN suppliers s ON p.supplier_id = s.id",
        "hint": "The join returns no results.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "ecommerce",
        "description": "Find customers who signed up in 2024.",
        "broken_query": "SELECT name, signup_date FROM customers WHERE strftime('%y', signup_date) = '2024'",
        "correct_query": "SELECT name, signup_date FROM customers WHERE strftime('%Y', signup_date) = '2024'",
        "hint": "The query returns no results even though 2024 customers exist.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "ecommerce",
        "description": "Show all products and the count of times they've been ordered, including products never ordered.",
        "broken_query": "SELECT p.name, COUNT(oi.id) as times_ordered FROM products p INNER JOIN order_items oi ON p.id = oi.product_id GROUP BY p.name",
        "correct_query": "SELECT p.name, COUNT(oi.id) as times_ordered FROM products p LEFT JOIN order_items oi ON p.id = oi.product_id GROUP BY p.name",
        "hint": "Products with zero orders are missing from the results.",
    },
    
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "ecommerce",
        "description": "Calculate running total of order revenue (quantity × unit_price) ordered by date.",
        "broken_query": "SELECT o.order_date, SUM(oi.quantity * oi.unit_price) as revenue, SUM(SUM(oi.quantity * oi.unit_price)) OVER () as running_total FROM orders o JOIN order_items oi ON o.id = oi.order_id GROUP BY o.order_date",
        "correct_query": "SELECT o.order_date, SUM(oi.quantity * oi.unit_price) as revenue, SUM(SUM(oi.quantity * oi.unit_price)) OVER (ORDER BY o.order_date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_total FROM orders o JOIN order_items oi ON o.id = oi.order_id GROUP BY o.order_date",
        "hint": "The running total column shows the same grand total on every row.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "ecommerce",
        "description": "Find products that have never been ordered.",
        "broken_query": "SELECT name FROM products WHERE id NOT IN (SELECT product_id FROM order_items WHERE discount IS NOT NULL)",
        "correct_query": "SELECT p.name FROM products p WHERE NOT EXISTS (SELECT 1 FROM order_items oi WHERE oi.product_id = p.id)",
        "hint": "The subquery only checks a subset of order items, not all of them.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "ecommerce",
        "description": "Show each customer's name and total spending, including customers with only cancelled orders who should show 0.",
        "broken_query": "SELECT c.name, SUM(oi.quantity * oi.unit_price) as total_spent FROM customers c JOIN orders o ON c.id = o.customer_id JOIN order_items oi ON o.id = oi.order_id WHERE o.status != 'cancelled' GROUP BY c.id",
        "correct_query": "SELECT c.name, COALESCE(SUM(CASE WHEN o.status != 'cancelled' THEN oi.quantity * oi.unit_price ELSE 0 END), 0) as total_spent FROM customers c LEFT JOIN orders o ON c.id = o.customer_id LEFT JOIN order_items oi ON o.id = oi.order_id GROUP BY c.id, c.name",
        "hint": "Customers with only cancelled orders are missing, and some customers without any orders don't appear at all.",
    },
    {
        "task_type": "optimization", "difficulty": "hard", "schema_name": "ecommerce",
        "description": "Get the most expensive product per category. Current query uses a slow correlated subquery.",
        "broken_query": "SELECT c.name, c.category, c.price FROM products c WHERE c.price = (SELECT MAX(p2.price) FROM products p2 WHERE p2.category = c.category)",
        "correct_query": "SELECT name, category, price FROM (SELECT name, category, price, RANK() OVER (PARTITION BY category ORDER BY price DESC) as rnk FROM products) WHERE rnk = 1",
        "hint": "Replace the correlated subquery with a window function approach.",
    },
    
    {
        "task_type": "logic_fix", "difficulty": "expert", "schema_name": "ecommerce",
        "description": "Show total, delivered, cancelled, and pending order counts per customer region using conditional aggregation.",
        "broken_query": "SELECT c.region, COUNT(*) as total, (SELECT COUNT(*) FROM orders o2 JOIN customers c2 ON o2.customer_id = c2.id WHERE c2.region = c.region AND o2.status = 'delivered') as delivered FROM orders o JOIN customers c ON o.customer_id = c.id GROUP BY c.region",
        "correct_query": "SELECT c.region, COUNT(*) as total, SUM(CASE WHEN o.status = 'delivered' THEN 1 ELSE 0 END) as delivered, SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END) as cancelled, SUM(CASE WHEN o.status = 'pending' THEN 1 ELSE 0 END) as pending FROM orders o JOIN customers c ON o.customer_id = c.id GROUP BY c.region",
        "hint": "The query is missing status breakdowns and uses an inefficient approach.",
    },
    {
        "task_type": "logic_fix", "difficulty": "expert", "schema_name": "ecommerce",
        "description": "Find customers whose most recent order total is less than their first order total.",
        "broken_query": "SELECT c.name FROM customers c JOIN orders o ON c.id = o.customer_id JOIN order_items oi ON o.id = oi.order_id WHERE SUM(oi.quantity * oi.unit_price) < (SELECT MIN(oi2.quantity * oi2.unit_price) FROM order_items oi2)",
        "correct_query": "SELECT c.name FROM customers c WHERE (SELECT SUM(oi.quantity * oi.unit_price) FROM orders o JOIN order_items oi ON o.id = oi.order_id WHERE o.customer_id = c.id AND o.order_date = (SELECT MAX(o2.order_date) FROM orders o2 WHERE o2.customer_id = c.id)) < (SELECT SUM(oi3.quantity * oi3.unit_price) FROM orders o3 JOIN order_items oi3 ON o3.id = oi3.order_id WHERE o3.customer_id = c.id AND o3.order_date = (SELECT MIN(o4.order_date) FROM orders o4 WHERE o4.customer_id = c.id))",
        "hint": "The query has a misplaced aggregate and compares against a global value instead of per-customer values.",
    },
    {
        "task_type": "logic_fix", "difficulty": "expert", "schema_name": "ecommerce",
        "description": "For each product category, show the month-over-month revenue change using LAG.",
        "broken_query": "SELECT category, order_month, revenue, LAG(category) OVER (PARTITION BY category ORDER BY order_month) as prev_revenue FROM (SELECT p.category, strftime('%Y-%m', o.order_date) as order_month, SUM(oi.quantity * oi.unit_price) as revenue FROM products p JOIN order_items oi ON p.id = oi.product_id JOIN orders o ON oi.order_id = o.id GROUP BY p.category, strftime('%Y-%m', o.order_date))",
        "correct_query": "SELECT category, order_month, revenue, LAG(revenue) OVER (PARTITION BY category ORDER BY order_month) as prev_revenue FROM (SELECT p.category, strftime('%Y-%m', o.order_date) as order_month, SUM(oi.quantity * oi.unit_price) as revenue FROM products p JOIN order_items oi ON p.id = oi.product_id JOIN orders o ON oi.order_id = o.id GROUP BY p.category, strftime('%Y-%m', o.order_date))",
        "hint": "The previous revenue column shows category names instead of numbers.",
    },

    
    {
        "task_type": "syntax_fix", "difficulty": "easy", "schema_name": "library",
        "description": "Get all books ordered by published year.",
        "broken_query": "SELECT title, published_year FROM books ORDERY BY published_year",
        "correct_query": "SELECT title, published_year FROM books ORDER BY published_year",
        "hint": "The query has a syntax error.",
    },
    {
        "task_type": "syntax_fix", "difficulty": "easy", "schema_name": "library",
        "description": "Show each loan's member ID and return date, defaulting to 'On Loan' if not yet returned.",
        "broken_query": "SELECT member_id, IFNULL('On Loan', return_date) FROM loans",
        "correct_query": "SELECT member_id, IFNULL(return_date, 'On Loan') FROM loans",
        "hint": "The fallback value appears on every row, even returned loans.",
    },
    {
        "task_type": "syntax_fix", "difficulty": "easy", "schema_name": "library",
        "description": "Find all books by author ID 1 or 3.",
        "broken_query": "SELECT title, author_id FROM books WHERE author_id IN 1, 3",
        "correct_query": "SELECT title, author_id FROM books WHERE author_id IN (1, 3)",
        "hint": "The query has a syntax error.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "library",
        "description": "Calculate how many days overdue each returned book was (returned after due date).",
        "broken_query": "SELECT l.id, b.title, julianday(due_date) - julianday(return_date) as days_overdue FROM loans l JOIN books b ON l.book_id = b.id WHERE return_date IS NOT NULL",
        "correct_query": "SELECT l.id, b.title, julianday(return_date) - julianday(due_date) as days_overdue FROM loans l JOIN books b ON l.book_id = b.id WHERE return_date IS NOT NULL",
        "hint": "Overdue books show negative values instead of positive.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "library",
        "description": "Get the first 4 characters of each book's title as a short code.",
        "broken_query": "SELECT title, SUBSTR(title, 0, 4) as code FROM books",
        "correct_query": "SELECT title, SUBSTR(title, 1, 4) as code FROM books",
        "hint": "The codes are one character too short.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "library",
        "description": "Show each book's title and its author's name.",
        "broken_query": "SELECT b.title, a.name as author FROM books b JOIN authors a ON b.author_id = a.name",
        "correct_query": "SELECT b.title, a.name as author FROM books b JOIN authors a ON b.author_id = a.id",
        "hint": "The join produces no results.",
    },
    {
        "task_type": "logic_fix", "difficulty": "medium", "schema_name": "library",
        "description": "Count loans per member including members who never borrowed anything.",
        "broken_query": "SELECT m.name, COUNT(l.id) as loan_count FROM members m INNER JOIN loans l ON m.id = l.member_id GROUP BY m.name",
        "correct_query": "SELECT m.name, COUNT(l.id) as loan_count FROM members m LEFT JOIN loans l ON m.id = l.member_id GROUP BY m.name",
        "hint": "A member with zero loans is missing from the output.",
    },
    
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "library",
        "description": "Find books that have never been borrowed by any member.",
        "broken_query": "SELECT title FROM books WHERE id NOT IN (SELECT book_id FROM reservations)",
        "correct_query": "SELECT b.title FROM books b WHERE NOT EXISTS (SELECT 1 FROM loans l WHERE l.book_id = b.id)",
        "hint": "The subquery checks the wrong table entirely.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "library",
        "description": "Find members with unpaid fines, showing member name and total unpaid amount.",
        "broken_query": "WITH unpaid AS (SELECT loan_id, SUM(amount) as total_unpaid FROM fines WHERE paid = 0 GROUP BY loan_id) SELECT m.name, u.total_unpaid FROM members m JOIN loans l ON m.id = l.member_id JOIN unpaid u ON l.id = u.loan_id WHERE u.total > 0",
        "correct_query": "WITH unpaid AS (SELECT loan_id, SUM(amount) as total_unpaid FROM fines WHERE paid = 0 GROUP BY loan_id) SELECT m.name, u.total_unpaid FROM members m JOIN loans l ON m.id = l.member_id JOIN unpaid u ON l.id = u.loan_id WHERE u.total_unpaid > 0",
        "hint": "The query errors on a column that doesn't exist.",
    },
    {
        "task_type": "logic_fix", "difficulty": "hard", "schema_name": "library",
        "description": "Show each author and their total number of active loans, including authors with no active loans.",
        "broken_query": "SELECT a.name, COUNT(l.id) as active_loans FROM authors a JOIN books b ON a.id = b.author_id JOIN loans l ON b.id = l.book_id WHERE l.return_date IS NULL GROUP BY a.id",
        "correct_query": "SELECT a.name, COUNT(CASE WHEN l.return_date IS NULL THEN 1 END) as active_loans FROM authors a LEFT JOIN books b ON a.id = b.author_id LEFT JOIN loans l ON b.id = l.book_id GROUP BY a.id, a.name",
        "hint": "Authors with no active loans are missing, and the WHERE clause interferes with the LEFT JOIN logic.",
    },
    {
        "task_type": "optimization", "difficulty": "hard", "schema_name": "library",
        "description": "Find authors who have at least one book in the library. Current query uses GROUP BY + HAVING which is slow.",
        "broken_query": "SELECT a.name FROM authors a LEFT JOIN books b ON a.id = b.author_id GROUP BY a.name HAVING COUNT(b.id) > 0",
        "correct_query": "SELECT a.name FROM authors a WHERE EXISTS (SELECT 1 FROM books b WHERE b.author_id = a.id)",
        "hint": "Rewrite for better performance.",
    },
    # --- EXPERT ---
    {
        "task_type": "logic_fix", "difficulty": "expert", "schema_name": "library",
        "description": "Rank members by their total number of loans, with ties getting the same rank and no gaps.",
        "broken_query": "SELECT m.name, COUNT(l.id) as loan_count, RANK() OVER (ORDER BY COUNT(l.id) DESC) as rnk FROM members m LEFT JOIN loans l ON m.id = l.member_id GROUP BY m.id, m.name",
        "correct_query": "SELECT m.name, COUNT(l.id) as loan_count, DENSE_RANK() OVER (ORDER BY COUNT(l.id) DESC) as rnk FROM members m LEFT JOIN loans l ON m.id = l.member_id GROUP BY m.id, m.name",
        "hint": "The ranking skips numbers after ties.",
    },
    {
        "task_type": "logic_fix", "difficulty": "expert", "schema_name": "library",
        "description": "For each member show their most recent loan date and the book title, using LAST_VALUE.",
        "broken_query": "SELECT DISTINCT member_id, LAST_VALUE(b.title) OVER (PARTITION BY l.member_id ORDER BY l.loan_date) as last_book FROM loans l JOIN books b ON l.book_id = b.id",
        "correct_query": "SELECT DISTINCT member_id, LAST_VALUE(b.title) OVER (PARTITION BY l.member_id ORDER BY l.loan_date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as last_book FROM loans l JOIN books b ON l.book_id = b.id",
        "hint": "The LAST_VALUE doesn't return the actual last book for each member.",
    },
    {
        "task_type": "logic_fix", "difficulty": "expert", "schema_name": "library",
        "description": "Find the second most borrowed book by loan count, handling ties correctly.",
        "broken_query": "SELECT b.title, COUNT(l.id) as loan_count FROM books b JOIN loans l ON b.id = l.book_id GROUP BY b.id, b.title ORDER BY loan_count DESC LIMIT 1 OFFSET 1",
        "correct_query": "SELECT title, loan_count FROM (SELECT b.title, COUNT(l.id) as loan_count, DENSE_RANK() OVER (ORDER BY COUNT(l.id) DESC) as rnk FROM books b JOIN loans l ON b.id = l.book_id GROUP BY b.id, b.title) WHERE rnk = 2",
        "hint": "If two books tie for first place, this returns the wrong result.",
    },
]