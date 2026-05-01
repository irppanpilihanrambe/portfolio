"""
Run once to create the initial admin user:
    python create_admin.py
"""
import asyncio
from sqlalchemy import select
from app.database import AsyncSessionLocal, init_db
from app.models import AdminUser, Project
from app.auth import hash_password
from app.config import get_settings

settings = get_settings()

SAMPLE_PROJECTS = [
    {
        "title": "Real-Time Streaming Pipeline",
        "category": "Data Engineering",
        "description": "Designed and deployed an end-to-end streaming pipeline processing 50M+ daily events with sub-second latency for a fintech platform.",
        "tech_stack": ["Apache Kafka", "Apache Spark", "Airflow", "Python", "GCP"],
        "order_index": 1,
    },
    {
        "title": "Executive BI Dashboard",
        "category": "Strategic Analytics",
        "description": "Built a unified BI platform consolidating 12 data sources, enabling C-suite decisions with near real-time KPI visibility.",
        "tech_stack": ["dbt", "BigQuery", "Looker", "SQL"],
        "order_index": 2,
    },
    {
        "title": "Enterprise DWH Migration",
        "category": "Data Warehouse",
        "description": "Led migration of 8TB on-premise warehouse to cloud-native architecture, reducing query costs by 60%.",
        "tech_stack": ["Snowflake", "dbt", "Terraform", "Python"],
        "order_index": 3,
    },
    {
        "title": "Customer Churn Prediction",
        "category": "Machine Learning",
        "description": "Developed an ML pipeline predicting churn with 89% accuracy, deployed on a feature store serving 3 business units.",
        "tech_stack": ["Python", "scikit-learn", "MLflow", "Feast"],
        "order_index": 4,
    },
    {
        "title": "Automated Data Quality Framework",
        "category": "Quality Assurance",
        "description": "Implemented data observability layer with automated anomaly detection, reducing data incidents by 75%.",
        "tech_stack": ["Great Expectations", "Monte Carlo", "SQL", "Airflow"],
        "order_index": 5,
    },
    {
        "title": "Semantic Layer & Metrics Store",
        "category": "Analytics Engineering",
        "description": "Architected a company-wide metrics store defining 200+ business metrics as a single source of truth.",
        "tech_stack": ["MetricFlow", "dbt Semantic Layer", "BigQuery", "Python"],
        "order_index": 6,
    },
]


async def main():
    await init_db()

    async with AsyncSessionLocal() as db:
        # Create admin user
        existing = await db.execute(
            select(AdminUser).where(AdminUser.username == settings.ADMIN_USERNAME)
        )
        if existing.scalar_one_or_none():
            print(f"[!] Admin '{settings.ADMIN_USERNAME}' already exists — skipping.")
        else:
            admin = AdminUser(
                username=settings.ADMIN_USERNAME,
                email=settings.ADMIN_EMAIL,
                hashed_password=hash_password(settings.ADMIN_PASSWORD),
            )
            db.add(admin)
            print(f"[+] Admin user '{settings.ADMIN_USERNAME}' created.")

        # Seed sample projects
        count_result = await db.execute(select(Project))
        if count_result.scalars().first() is None:
            for p in SAMPLE_PROJECTS:
                db.add(Project(**p))
            print(f"[+] {len(SAMPLE_PROJECTS)} sample projects seeded.")
        else:
            print("[!] Projects already exist — skipping seed.")

        await db.commit()

    print("\n✅ Done! You can now login at /admin")
    print(f"   Username : {settings.ADMIN_USERNAME}")
    print(f"   Password : {settings.ADMIN_PASSWORD}")


if __name__ == "__main__":
    asyncio.run(main())
