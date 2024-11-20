from sqlalchemy import create_engine, Column, Integer, String, Enum, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..DatabaseLayer.JobCreateDTO import ContractType, NationalServiceStatus, JobCreateDTO

# Define SQLAlchemy engine and base
connection_string = f"postgresql://aryan:a123@localhost:5432/JobExt"

engine = create_engine(connection_string)
Base = declarative_base()


# Define DatabaseRecord table
class DatabaseRecord(Base):
    __tablename__ = 'processed_job_records'

    id = Column(Integer, primary_key=True)
    job_title = Column(String)
    job_link = Column(String)
    job_company_name = Column(String)
    job_city = Column(String)
    job_contract_type = Column(Enum(ContractType))
    company_image_url = Column(String)
    company_category = Column(String)
    company_population = Column(String)
    company_website = Column(String, nullable=True)
    job_minimum_work_experience = Column(String, nullable=True)
    minimum_job_salary = Column(String, nullable=True)
    national_service_status = Column(Enum(NationalServiceStatus), nullable=True)
    job_field = Column(String)
    job_hard_skills_required = Column(JSON)
    job_soft_skills_required = Column(JSON, nullable=True)
    job_benefits = Column(JSON, nullable=True)
    company_address = Column(String, nullable=True)


# Create the table
Base.metadata.create_all(engine)

def save_job_to_database(job_dto: JobCreateDTO):
    """
    Save a JobCreateDTO object to the processed_job_records table.

    Args:
        job_dto (JobCreateDTO): The job data to save.
    """
    # Create a new session
    session_local = sessionmaker(bind=engine)
    session = session_local()

    try:
        # Map JobCreateDTO to DatabaseRecord
        db_record = DatabaseRecord(
            job_title=job_dto.job_title,
            job_link=job_dto.job_link,
            job_company_name=job_dto.job_company_name,
            job_city=job_dto.job_city,
            job_contract_type=job_dto.job_contract_type,
            company_image_url=job_dto.company_image_url,
            company_category=job_dto.company_category,
            company_population=job_dto.company_population,
            company_website=job_dto.company_website,
            job_minimum_work_experience=job_dto.job_minimum_work_experience,
            minimum_job_salary=job_dto.minimum_job_salary,
            national_service_status=job_dto.national_service_status,
            job_field=job_dto.job_field,
            job_hard_skills_required=[skill.to_dict() for skill in job_dto.job_hard_skills_required],
            job_soft_skills_required=[skill.to_dict() for skill in job_dto.job_soft_skills_required] if job_dto.job_soft_skills_required else None,
            job_benefits=[benefit.to_dict() for benefit in job_dto.job_benefits] if job_dto.job_benefits else None,
            company_address=job_dto.company_address
        )

        # Add to session and commit
        session.add(db_record)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
