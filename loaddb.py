from pymongo import MongoClient
import json
from datetime import datetime, timedelta
from bson import ObjectId
import random

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['university_db']  # Create a database named university_db

# Read the JSON schema
with open('JSON_db.json', 'r') as file:
    schema = json.load(file)

# Clear existing collections
for collection in db.list_collection_names():
    db[collection].drop()

# Create collections
for collection in schema:
    collection_name = collection['name']
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)

# Sample data
courses_data = [
    {
        'id': 1,
        'name': 'Computer Science',
        'subjects': [1, 2, 3, 4]  # Will be updated with actual subject IDs
    },
    {
        'id': 2,
        'name': 'Business Administration',
        'subjects': [5, 6, 7, 8]
    },
    {
        'id': 3,
        'name': 'Engineering',
        'subjects': [9, 10, 11, 12]
    }
]

subjects_data = [
    # Computer Science subjects
    {'id': 1, 'name': 'Programming Fundamentals', 'description': 'Introduction to programming concepts'},
    {'id': 2, 'name': 'Database Systems', 'description': 'Study of database design and management'},
    {'id': 3, 'name': 'Web Development', 'description': 'Modern web development technologies'},
    {'id': 4, 'name': 'Artificial Intelligence', 'description': 'Introduction to AI and machine learning'},
    
    # Business Administration subjects
    {'id': 5, 'name': 'Marketing', 'description': 'Principles of marketing and market analysis'},
    {'id': 6, 'name': 'Financial Management', 'description': 'Corporate finance and investment'},
    {'id': 7, 'name': 'Business Strategy', 'description': 'Strategic planning and management'},
    {'id': 8, 'name': 'Operations Management', 'description': 'Business operations and logistics'},
    
    # Engineering subjects
    {'id': 9, 'name': 'Mechanics', 'description': 'Classical mechanics and dynamics'},
    {'id': 10, 'name': 'Electronics', 'description': 'Electronic circuits and systems'},
    {'id': 11, 'name': 'Materials Science', 'description': 'Study of materials and their properties'},
    {'id': 12, 'name': 'Thermodynamics', 'description': 'Heat and energy transfer'}
]

# Create teachers
teachers_data = [
    {
        'id': 1,
        'name': 'Dr. Sarah Johnson',
        'email': 'sarah.johnson@university.edu',
        'type': 'teacher',
        'courses': [1],  # Computer Science
        'documents': []
    },
    {
        'id': 2,
        'name': 'Prof. Michael Chen',
        'email': 'michael.chen@university.edu',
        'type': 'teacher',
        'courses': [2],  # Business Administration
        'documents': []
    },
    {
        'id': 3,
        'name': 'Dr. Emily Rodriguez',
        'email': 'emily.rodriguez@university.edu',
        'type': 'teacher',
        'courses': [3],  # Engineering
        'documents': []
    }
]

# Create students
students_data = []
for i in range(15):
    student = {
        'id': i + 4,  # Start from 4 since teachers are 1-3
        'name': f'Student {i+1}',
        'email': f'student{i+1}@university.edu',
        'type': 'student',
        'courses': [random.randint(1, 3)],  # Random course assignment
        'documents': []
    }
    students_data.append(student)

# Insert courses and subjects
for course in courses_data:
    db['courses'].insert_one(course)

for subject in subjects_data:
    db['subjects'].insert_one(subject)

# Insert users (teachers and students)
for teacher in teachers_data:
    db['users'].insert_one(teacher)

for student in students_data:
    db['users'].insert_one(student)

# Create documents
document_types = ['Lecture Notes', 'Assignment', 'Exam', 'Project', 'Study Guide']
document_titles = [
    'Introduction to Programming',
    'Database Design Principles',
    'Web Development Basics',
    'AI Fundamentals',
    'Marketing Strategy',
    'Financial Analysis',
    'Business Planning',
    'Operations Management',
    'Mechanical Systems',
    'Circuit Design',
    'Materials Properties',
    'Heat Transfer'
]

# Create documents for teachers
for teacher in teachers_data:
    for i in range(3):  # 3 documents per teacher
        doc = {
            'id': len(list(db['documents'].find())) + 1,
            'title': f'{document_titles[i]} - {document_types[i]}',
            'upload_date': datetime.now() - timedelta(days=random.randint(1, 30)),
            'file_url': f'https://university.edu/documents/{teacher["id"]}_{i+1}.pdf',
            'type': document_types[i],
            'grade': None,
            'teacher_id': teacher['id'],
            'subject_id': teacher['courses'][0] * 4 - 3 + i,  # Related to teacher's course
            'owner': ObjectId()
        }
        db['documents'].insert_one(doc)
        # Update teacher's documents
        db['users'].update_one(
            {'id': teacher['id']},
            {'$push': {'documents': doc['id']}}
        )

# Create documents for students
for student in students_data:
    for i in range(2):  # 2 documents per student
        doc = {
            'id': len(list(db['documents'].find())) + 1,
            'title': f'Assignment {i+1} - {document_titles[student["courses"][0] * 4 - 4 + i]}',
            'upload_date': datetime.now() - timedelta(days=random.randint(1, 30)),
            'file_url': f'https://university.edu/documents/{student["id"]}_{i+1}.pdf',
            'type': 'Assignment',
            'grade': random.randint(60, 100),
            'teacher_id': student['courses'][0],  # Course teacher
            'subject_id': student['courses'][0] * 4 - 3 + i,  # Related to student's course
            'owner': ObjectId()
        }
        db['documents'].insert_one(doc)
        # Update student's documents
        db['users'].update_one(
            {'id': student['id']},
            {'$push': {'documents': doc['id']}}
        )

print("Database has been created with sample data!")
print("\nCollections created:", db.list_collection_names())

# Print sample data from each collection
for collection_name in db.list_collection_names():
    print(f"\nSample data from {collection_name}:")
    for doc in db[collection_name].find():
        print(doc)
