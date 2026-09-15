import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# 1. Charger le fichier .env
load_dotenv()

# 2. Lire les variables d'environnement
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")

# 3. Vérifier que les variables existent
if not all([user, password, host, port, dbname]):
    raise ValueError("❌ Variables DB manquantes dans le fichier .env")

# 4. Créer la connexion PostgreSQL
engine = create_engine(
    f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
)

# 5. Lire le fichier Excel nettoyé
df = pd.read_excel("data/contacts_nettoyes.xlsx")

print(f"📄 {len(df)} contacts chargés depuis Excel")

# 6. Insérer les données dans PostgreSQL
df.to_sql(
    "contacts",
    engine,
    if_exists="replace",
    index=False
)

print(f"✅ {len(df)} contacts insérés dans PostgreSQL")