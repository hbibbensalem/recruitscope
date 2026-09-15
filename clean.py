import pandas as pd
import json
import re

# ---------- ÉTAPE 1 : Chargement ----------

df = pd.read_excel('data/PFEcontacts.xlsx')


# ---------- ÉTAPE 2 : Parser le JSON ----------

def extraire_company(json_brut):
    try:
        return json.loads(json_brut)["Company"]
    except (TypeError, json.JSONDecodeError, KeyError):
        return None


df["company"] = df["attributes"].apply(extraire_company)


# ---------- ÉTAPE 3 : Normalisation email ----------

df["email"] = df["email"].str.strip().str.lower()


# ---------- ÉTAPE 4 : Supprimer les lignes sans email ----------

df = df.dropna(subset=["email"])


# ---------- ÉTAPE 5 : Validation du format ----------

regex_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'  

df = df[df["email"].str.match(regex_email, na=False)]


# ---------- ÉTAPE 6 : Déduplication ----------

avant = len(df)

df = df.drop_duplicates(
    subset=["email"],
    keep="first"
)

print(f"Doublons supprimés : {avant - len(df)}")


# ---------- ÉTAPE 7 : Normalisation company ----------

df["company_clean"] = df["company"].str.strip().str.lower()


# ---------- ÉTAPE 8 : Domaine email ----------

df["email_domain"] = df["email"].str.split("@").str[1]


# ---------- EXPORT ----------

df.to_excel(
    'data/contacts_nettoyes.xlsx',
    index=False
)

print(f"Fichier final : {len(df)} contacts propres")