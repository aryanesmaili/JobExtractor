import json
from typing import Tuple, List

import requests


def send_data_to_external_service(url: str, data: List[str]) -> str:
    """
    sends the part of scraped data to the notebook to be processed.
    :param data: the data to send.
    :param url: the url to send the data to.
    :return: the response from the notebook.
    """
    payload = {
        "job_title": data[0],
        "job_ad_body": data[1]
    }
    response = requests.post(url, json=payload)
    return response.text


def process_incoming_data(data: str) -> Tuple[str, List[str], List[str], List[str], str]:
    """
    processes the response from the notebook.
    :param data: the data to process
    :return: the response from the notebook processed.
    """
    data = json.loads(data)
    job_field: str = data["job_field"]
    hard_skills: List[str] = data["hard_skills"].split(",")
    soft_skills: List[str] = data["soft_skills"].split(",")
    job_benefits: List[str] = data["job_benefits"].split(",")
    company_address: str = data["company_address"]

    return job_field, hard_skills, soft_skills, job_benefits, company_address
