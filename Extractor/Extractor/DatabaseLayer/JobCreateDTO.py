import re
from enum import Enum
from typing import Union, List

from ..Processor.OutputModel import JobDetails
from ..items import JobInjaJobListItem


class ContractType(Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    INTERNSHIP = "internship"
    REMOTE = "remote"


class NationalServiceStatus(Enum):
    """Enumeration representing national service statuses."""
    FULL_EXEMPTION = 'Exemption'
    EDUCATIONAL_EXEMPTION = 'Educational_Exemption'
    NOT_NEEDED = 'Not_needed'


class JobCreateDTO:
    """Class to represent a record to be saved in the database."""
    notebook_url = ""

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
                return ContractType.FULL_TIME
            case _ if "پاره" in text:
                return ContractType.PART_TIME
            case _ if "کارآموزی" in text:
                return ContractType.INTERNSHIP
            case _ if "دورکاری" in text:
                return ContractType.REMOTE
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
                return NationalServiceStatus.FULL_EXEMPTION
            case _ if "تحصیلی" in text:
                return NationalServiceStatus.EDUCATIONAL_EXEMPTION
            case _ if "مهم نیست" in text:
                return NationalServiceStatus.NOT_NEEDED
            case _:
                return None

    def __init__(self, raw_scraped_item: JobInjaJobListItem, ai_processed_item: JobDetails):
        """
        Initialize a DatabaseRecord object.

        Args:
            raw_scraped_item (JobInjaJobListItem): The item to extract data from.
        """
        self.job_title: str = raw_scraped_item['job_title']
        self.job_link: str = raw_scraped_item['job_link']
        self.job_company_name: str = raw_scraped_item['job_company_name']
        self.job_city: str = raw_scraped_item["job_city"]
        self.job_contract_type: ContractType = self.detect_contract_type(raw_scraped_item["job_contract_type"])
        self.company_image_url: str = raw_scraped_item["company_image_url"]
        self.company_category: str = raw_scraped_item["company_category"]
        self.company_population: str = raw_scraped_item["company_population"]
        self.company_website: Union[str, None] = raw_scraped_item["company_website"]
        self.job_minimum_work_experience: Union[str, None] = raw_scraped_item["job_minimum_work_experience"]
        self.minimum_job_salary: Union[str, None] = self.convert_persian_numbers_to_int(raw_scraped_item["job_salary"])
        self.national_service_status: Union[NationalServiceStatus, None] = self.detect_national_service_status(
            raw_scraped_item["national_service_status"])

        self.job_field: str = ai_processed_item.job_field
        self.job_hard_skills_required: List[str] = []
        self.job_soft_skills_required: Union[List[str], None] = []
        self.job_benefits: Union[List[str], None] = []
        self.company_address: Union[str, None] = ""
