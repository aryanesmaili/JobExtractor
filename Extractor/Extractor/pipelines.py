from itemadapter import ItemAdapter
from typing import Optional, List, Union
from Extractor.Extractor.items import JobInjaJobListItem
from enum import Enum
from Database import save_to_database
import re
import colabfuncs


class ContractType(Enum):
    """Enumeration representing contract types."""
    full_time = 'full_time'
    part_time = 'part_time'
    internship = 'internship'
    remote = 'remote'


class NationalServiceStatus(Enum):
    """Enumeration representing national service statuses."""
    full_exemption = 'Exemption'
    educational_exemption = 'Educational_Exemption'
    not_needed = 'Not_needed'


class DatabaseRecord:
    """Class to represent a record to be saved in the database."""

    @staticmethod
    def convert_persian_numbers_to_int(text: str) -> str:
        """
        Convert Persian numbers in a string to integers.

        Args:
            text (str): The text containing Persian numbers.

        Returns:
            str: The text with Persian numbers converted to integers.
        """
        # Define a dictionary mapping Persian numbers to their integer equivalents
        persian_to_int = {'۰': 0, '۱': 1, '۲': 2, '۳': 3, '۴': 4, '۵': 5, '۶': 6, '۷': 7, '۸': 8, '۹': 9}

        # Use regular expression to find all Persian number sequences
        persian_numbers = re.findall('[۰-۹]+', text)

        # Replace each Persian number sequence with its integer equivalent
        for persian_num in persian_numbers:
            int_representation = ''.join(str(persian_to_int[digit]) for digit in persian_num)
            text = text.replace(persian_num, str(int_representation))

        return text

    @staticmethod
    def detect_contract_type(text) -> Union[ContractType, None]:
        """
        Detect the contract type from text.

        Args:
            text (str): The text to be analyzed.

        Returns:
            Union[ContractType, None]: The detected contract type or None if not found.
        """
        match text:
            case _ if "تمام" in text:
                return ContractType.full_time
            case _ if "پاره" in text:
                return ContractType.part_time
            case _ if "کارآموزی" in text:
                return ContractType.internship
            case _ if "دورکاری" in text:
                return ContractType.remote
            case _:
                return None

    @staticmethod
    def detect_national_service_status(text: str) -> Union[NationalServiceStatus, None]:
        """
        Detect the national service status from text.

        Args:
            text (str): The text to be analyzed.

        Returns:
            Union[NationalServiceStatus, None]: The detected national service status or None if not found.
        """
        match text:
            case _ if "دائم" in text:
                return NationalServiceStatus.full_exemption
            case _ if "تحصیلی" in text:
                return NationalServiceStatus.educational_exemption
            case _ if "مهم نیست" in text:
                return NationalServiceStatus.not_needed
            case _:
                return None

    def __init__(self, item: JobInjaJobListItem):
        """
        Initialize a DatabaseRecord object.

        Args:
            item (JobInjaJobListItem): The item to extract data from.
        """
        self.job_title: str = item.job_title
        self.job_link: str = item.job_link
        self.job_company_name: str = item.job_company_name
        self.job_city: str = item.job_city
        self.job_contract_type: ContractType = self.detect_contract_type(item.job_contract_type)
        self.company_image_url: str = item.company_image_url
        self.company_category: str = item.company_category
        self.company_population: str = item.company_population
        self.company_website: Union[str, None] = item.company_website
        self.job_minimum_work_experience: Union[str, None] = item.job_minimum_work_experience
        self.minimum_job_salary: Union[str, None] = self.convert_persian_numbers_to_int(item.minimum_job_salary)
        self.national_service_status: Union[NationalServiceStatus, None] = self.detect_national_service_status(
            item.national_service_status)

        # the part that gets sent to external services.
        items_to_be_processed = [self.job_title, item.job_content]
        processed_data = colabfuncs.process_data_from_notebook(colabfuncs.send_data_to_notebook(items_to_be_processed))
        self.job_field = processed_data[0]
        self.job_hard_skills_required: List[str] = processed_data[1]
        self.job_soft_skills_required: Union[List[str], None] = processed_data[2]
        self.job_benefits: Union[List[str], None] = processed_data[3]
        self.company_address: Union[str, None] = processed_data[4]


class ExtractorPipeline:
    """Class to process extracted items and save them to the database."""

    def process_item(self, item, spider):
        """
        Process an extracted item and save it to the database.

        Args:
            item: The extracted item.
            spider: The spider that extracted the item.

        Returns:
            item: The processed item.
        """
        db_row = DatabaseRecord(item)
        save_to_database(db_row)
        return item
