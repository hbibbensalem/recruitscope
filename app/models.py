from sqlalchemy import Column, Integer, String, DateTime, Boolean, Index
from sqlalchemy.sql import func
from app.database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String(255), unique=True, nullable=False, index=True)
    email_domain = Column(String(255), nullable=True, index=True)

    company = Column(String(255), nullable=True)
    company_clean = Column(String(255), nullable=True, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Champs qu'on remplira PLUS TARD avec l'agent IA (enrichissement)
    company_domain_ai = Column(String(255), nullable=True)   # secteur d'activité déduit par l'IA
    is_enriched = Column(Boolean, default=False, nullable=False)
    enriched_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("ix_contacts_company_enriched", "company_clean", "is_enriched"),
    )

    def __repr__(self):
        return f"<Contact(email={self.email}, company={self.company_clean})>"


class Company(Base):
    """
    Table séparée pour dédupliquer les entreprises.
    Une company peut avoir plusieurs contacts -> évite de répéter
    l'enrichissement IA pour chaque contact de la même entreprise.
    """
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name_clean = Column(String(255), unique=True, nullable=False, index=True)
    website = Column(String(500), nullable=True)

    sector = Column(String(255), nullable=True)          # ex: "FinTech", "E-commerce"
    open_positions = Column(String(2000), nullable=True)  # JSON stocké en texte, ou passer à JSONB plus tard

    is_enriched = Column(Boolean, default=False, nullable=False)
    enriched_at = Column(DateTime(timezone=True), nullable=True)
    last_enrichment_error = Column(String(500), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    enrichment_attempts = Column(Integer, default=0, nullable=False)
