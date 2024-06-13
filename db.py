import sqlite3
import json

# Function to create database and tables
def create_tables():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE Category (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE Model (
            id INTEGER PRIMARY KEY,
            name TEXT,
            category_id INTEGER,
            rmse REAL,
            loss REAL,
            parameters TEXT,
            FOREIGN KEY (category_id) REFERENCES Category(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE Attribute (
            id INTEGER PRIMARY KEY,
            name TEXT,
            value TEXT,
            model_id INTEGER,
            FOREIGN KEY (model_id) REFERENCES Model(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE Image (
            id INTEGER PRIMARY KEY,
            path TEXT,
            model_id INTEGER,
            FOREIGN KEY (model_id) REFERENCES Model(id)
        )
    ''')

    conn.commit()
    conn.close()

# Function to insert data from JSON into SQLite
def insert_data():
    with open('data2.json', 'r') as file:
        data = json.load(file)

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    for category_name, models in data.items():
        cursor.execute('INSERT INTO Category (name) VALUES (?)', (category_name,))
        category_id = cursor.lastrowid

        for model_name, attributes in models.items():
            rmse = attributes.get('rmse')
            loss = attributes.get('loss')
            parameters = json.dumps(attributes.get('best_params'))

            cursor.execute('''
                INSERT INTO Model (name, category_id, rmse, loss, parameters) VALUES (?, ?, ?, ?, ?)
            ''', (model_name, category_id, rmse, loss, parameters))
            model_id = cursor.lastrowid

            for attribute_name, attribute_value in attributes.items():
                if attribute_name not in ['rmse', 'loss', 'best_params', 'image']:
                    if isinstance(attribute_value, dict):
                        for key, value in attribute_value.items():
                            cursor.execute('INSERT INTO Attribute (name, value, model_id) VALUES (?, ?, ?)', (attribute_name + '_' + key, value, model_id))
                    else:
                        cursor.execute('INSERT INTO Attribute (name, value, model_id) VALUES (?, ?, ?)', (attribute_name, attribute_value, model_id))

            images = attributes.get('image', [])
            for image_path in images:
                cursor.execute('INSERT INTO Image (path, model_id) VALUES (?, ?)', (image_path, model_id))

    conn.commit()
    conn.close()

# Main function
def main():
    create_tables()
    insert_data()

if __name__ == "__main__":
    main()
