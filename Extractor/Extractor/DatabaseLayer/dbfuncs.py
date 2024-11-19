from ..DatabaseLayer.JobCreateDTO import JobCreateDTO
from ..DatabaseLayer.dbtable import DatabaseManager


def save_to_database(db_row: JobCreateDTO) -> bool:
    db_manager = DatabaseManager()
    db_record = db_manager.create_record(db_row)
    if db_record is not None:
        return True
    return False
