"""
Charge le fichier Excel nettoyé dans PostgreSQL via SQLAlchemy ORM,
avec upsert (insert ou update si l'email existe déjà) au lieu de
DROP + CREATE (if_exists="replace") qui perdait les contraintes et
les données déjà enrichies par l'agent IA.
"""

import pandas as pd
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.database import engine, SessionLocal, Base
from app.models import Contact, Company


def create_tables():
    """Crée les tables si elles n'existent pas.
    NOTE: en production/évolution du schéma, utiliser Alembic (migrations),
    pas create_all(), qui ne gère pas les modifications de colonnes.
    """
    Base.metadata.create_all(bind=engine)


def upsert_companies(df: pd.DataFrame, session) -> dict:
    """Insère les entreprises uniques. Retourne un mapping name_clean -> company_id."""
    companies = df["company_clean"].dropna().unique().tolist()

    if not companies:
        return {}

    stmt = pg_insert(Company).values(
        [{"name_clean": c} for c in companies]
    ).on_conflict_do_nothing(index_elements=["name_clean"])

    session.execute(stmt)
    session.commit()

    rows = session.query(Company.id, Company.name_clean).all()
    return {name: cid for cid, name in rows}


def upsert_contacts(df: pd.DataFrame, session):
    """Insère les contacts, met à jour l'email_domain/company si l'email existe déjà."""
    records = df.to_dict(orient="records")

    inserted, updated = 0, 0

    for row in records:
        stmt = pg_insert(Contact).values(
            email=row["email"],
            email_domain=row.get("email_domain"),
            company=row.get("company"),
            company_clean=row.get("company_clean"),
        )
        stmt = stmt.on_conflict_do_update(
            index_elements=["email"],
            set_={
                "company": stmt.excluded.company,
                "company_clean": stmt.excluded.company_clean,
                "email_domain": stmt.excluded.email_domain,
            },
        )
        result = session.execute(stmt)
        inserted += 1  # upsert: on ne distingue pas insert/update ici sans requête supplémentaire

    session.commit()
    return inserted


def main():
    print("Création des tables si nécessaire...")
    create_tables()

    print("Lecture du fichier Excel nettoyé...")
    df = pd.read_excel("data/contacts_nettoyes.xlsx")
    print(f"{len(df)} contacts chargés depuis Excel")

    session = SessionLocal()
    try:
        print("Upsert des entreprises...")
        company_map = upsert_companies(df, session)
        print(f"{len(company_map)} entreprises uniques en base")

        print("Upsert des contacts...")
        count = upsert_contacts(df, session)
        print(f"{count} contacts traités (insert ou update)")
    finally:
        session.close()

    print("Terminé.")


if __name__ == "__main__":
    main()
