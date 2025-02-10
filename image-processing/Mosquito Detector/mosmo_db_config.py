import sqlite3
from datetime import datetime

# Register the adapter and converter for datetime
sqlite3.register_adapter(datetime, lambda val: val.isoformat())
sqlite3.register_converter("DATETIME", lambda val: datetime.fromisoformat(val.decode("utf-8")))

class MosquitoDatabase:
    def __init__(self, db_name='../../mosquito_detection.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS mosquito (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            image_path TEXT
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS mosquito_detected (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            species_name TEXT NOT NULL,
            detection_time DATETIME NOT NULL,
            FOREIGN KEY (species_name) REFERENCES mosquito(name)
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS disease (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS mosquito_disease (
            mosquito_id INTEGER NOT NULL,
            disease_id INTEGER NOT NULL,
            PRIMARY KEY (mosquito_id, disease_id),
            FOREIGN KEY (mosquito_id) REFERENCES mosquito(id),
            FOREIGN KEY (disease_id) REFERENCES disease(id)
        )
        ''')
        
        self.conn.commit()

    def add_mosquito_detection(self, species_name):
        detection_time = datetime.now()
        self.cursor.execute('''
        INSERT INTO mosquito_detected (species_name, detection_time) 
        VALUES (?, ?)
        ''', (species_name, detection_time))
        self.conn.commit()

    def is_mosquito_table_empty(self):
        self.cursor.execute('SELECT COUNT(*) FROM mosquito')
        count = self.cursor.fetchone()[0]
        return count == 0

    def add_static_mosquito_info(self):
        if not self.is_mosquito_table_empty():
            return

        mosquitoes = {
            "Aedes Aegypti": """Aedes aegypti is a mosquito species that is known for its capability in transmitting diseases such as dengue, chikungunya, yellow fever, and Zika virus. It highlights the importance of understanding how environmental factors influence the traits of mosquitoes.""",
            "Aedes Albopictus": """Aedes albopictus belongs to the aedes genus of mosquitoes, they can transmit several diseases through biting their hosts which includes dengue fever, chikungunya, and zika virus. Aedes albopictus continues to spread health risks to people living in tropical and subtropical regions, as well as in cold weather.""",
            "Aedes Vexans": """Aedes vexans, a mosquito species native to China, also carries mosquito-borne viruses, such as dengue fever virus and Japanese encephalitis virus, but research on this mosquito has been inadequate.""",
            "Aedes Niveus": """Important vector of periodic Wuchereria bancrofti filariasis in the Philippines. Aedes niveus are thought to play a significant role in the sylvatic dengue cycle in Borneo.""",
            "Culex Pipiens": "A mosquito species from the culex genus known to transmit West Nile Virus.",
            "Culex Quinquefasciatus": "A mosquito species from the culex genus known to transmit St. Louis Encephalitis and West Nile Virus.",
            "Culex Vishnui": "A mosquito species from the culex genus known to transmit japanese encephalitis virus.",
            "Culex Tritaeniorhynchus": "A Mosquito species from the culex genus known to transmit japanese encephalitis virus."
        }

        dangers = {
            "Aedes Aegypti": ["Dengue", "Chikungunya", "Yellow Fever", "Zika Virus"],
            "Culex Pipiens": ["West Nile Virus"],
            "Aedes Albopictus": ["Chikungunya", "Dengue Fever", "Zika Virus"],
            "Aedes Vexans": ["Dengue Fever", "Japanese Encephalitis"],
            "Aedes Niveus": ["Sylvatic Dengue"],
            "Culex Quinquefasciatus": ["West Nile Virus", "St. Louis Encephalitis"],
            "Culex Vishnui": ["Japanese Encephalitis"],
            "Culex Tritaeniorhynchus": ["Japanese Encephalitis"]
        }

        disease_ids = {}

        # Insert diseases into the disease table
        for disease_list in dangers.values():
            for disease in disease_list:
                if disease not in disease_ids:
                    self.cursor.execute('INSERT OR IGNORE INTO disease (name) VALUES (?)', (disease,))
                    self.conn.commit()
                    self.cursor.execute('SELECT id FROM disease WHERE name = ?', (disease,))
                    disease_ids[disease] = self.cursor.fetchone()[0]

        # Insert mosquitoes and their relationships to diseases
        for name, description in mosquitoes.items():
            self.cursor.execute('''
            INSERT INTO mosquito (name, description, image_path) 
            VALUES (?, ?, ?)
            ''', (name, description, ''))
            self.conn.commit()

            self.cursor.execute('SELECT id FROM mosquito WHERE name = ?', (name,))
            mosquito_id = self.cursor.fetchone()[0]

            for disease in dangers[name]:
                self.cursor.execute('''
                INSERT INTO mosquito_disease (mosquito_id, disease_id) 
                VALUES (?, ?)
                ''', (mosquito_id, disease_ids[disease]))

        self.conn.commit()

    def close_connection(self):
        self.conn.close()

# Example usage:
# db = MosquitoDatabase()
# db.add_static_mosquito_info()
# db.add_mosquito_detection('Aedes aegypti')
# db.close_connection()
