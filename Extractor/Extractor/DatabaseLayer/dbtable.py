from sqlalchemy import create_engine, Column, Integer, String, Enum, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..DatabaseLayer.JobCreateDTO import ContractType, NationalServiceStatus

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


# Function for CRUD operations
class DatabaseManager:
    def __init__(self):
        session = sessionmaker(bind=engine)
        self.session = session()

    def create_record(self, item):
        record = DatabaseRecord(
            job_title=item.job_title,
            job_link=item.job_link,
            job_company_name=item.job_company_name,
            job_city=item.job_city,
            job_contract_type=item.job_contract_type,
            company_image_url=item.company_image_url,
            company_category=item.company_category,
            company_population=item.company_population,
            company_website=item.company_website,
            job_minimum_work_experience=item.job_minimum_work_experience,
            minimum_job_salary=item.minimum_job_salary,
            national_service_status=item.national_service_status,
            job_field=item.job_field,
            job_hard_skills_required=item.job_hard_skills_required,
            job_soft_skills_required=item.job_soft_skills_required,
            job_benefits=item.job_benefits,
            company_address=item.company_address
        )
        self.session.add(record)
        self.session.commit()
        return record

    def get_record_by_id(self, record_id):
        return self.session.query(DatabaseRecord).filter_by(id=record_id).first()

    def update_record(self, record_id, **kwargs):
        record = self.get_record_by_id(record_id)
        if record:
            for attr, value in kwargs.items():
                setattr(record, attr, value)
            self.session.commit()
            return record
        return None

    def delete_record(self, record_id):
        record = self.get_record_by_id(record_id)
        if record:
            self.session.delete(record)
            self.session.commit()
            return True
        return False

# Usage Example:
# db_manager = DatabaseManager()
# new_record = db_manager.create_record(item)
# print(new_record.id)
# updated_record = db_manager.update_record(new_record.id, job_title='New Job Title')
# deleted = db_manager.delete_record(new_record.id)
# print(deleted)
