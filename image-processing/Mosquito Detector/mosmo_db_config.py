from pymongo import MongoClient
from datetime import datetime

PASSWORD = 'b6cZBOe084OonRuo'
USERNAME = 'danielheist260'

class MosquitoDatabase:
    def __init__(self, uri=f"mongodb+srv://danielheist260:{PASSWORD}@mosmo.ewgga.mongodb.net/", db_name="mosmo"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.mosquito_collection = self.db["mosquito"]
        self.disease_collection = self.db["disease"]
        self.detection_collection = self.db["mosquito_detected"]

    def add_mosquito_detection(self, species_name):
        detection_time = datetime.now()
        self.detection_collection.insert_one({
            "species_name": species_name,
            "detection_time": detection_time
        })
        print(f"Added mosquito detection: {species_name} at {detection_time}")

    def is_mosquito_collection_empty(self):
        return self.mosquito_collection.count_documents({}) == 0

    def add_static_mosquito_info(self):
        if not self.is_mosquito_collection_empty():
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

        # Insert diseases and keep track of IDs
        disease_ids = {}
        for disease in set(d for d_list in dangers.values() for d in d_list):
            disease_doc = self.disease_collection.find_one({"name": disease})
            if not disease_doc:
                disease_id = self.disease_collection.insert_one({"name": disease}).inserted_id
            else:
                disease_id = disease_doc["_id"]
            disease_ids[disease] = disease_id

        # Insert mosquitoes with references to diseases
        for name, description in mosquitoes.items():
            mosquito_data = {
                "name": name,
                "description": description,
                "diseases": [disease_ids[d] for d in dangers[name]],
                "image_path": ""
            }
            self.mosquito_collection.insert_one(mosquito_data)

        print("Mosquito and disease data inserted successfully.")

    def close_connection(self):
        self.client.close()
        print("Database connection closed.")

# Example usage:
db = MosquitoDatabase()
db.add_static_mosquito_info()
# db.add_mosquito_detection('Aedes Aegypti')
db.close_connection()
