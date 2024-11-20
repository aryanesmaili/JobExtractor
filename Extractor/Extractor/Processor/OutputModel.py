from typing import List, Optional

from pydantic import BaseModel, Field


class HardSkill(BaseModel):
    skill_type: str = Field(..., description="The category of the skill (e.g., Programming Language, Framework, Tool)")
    skill: str = Field(..., description="The specific skill (e.g., C#, ASP.NET Core)")
    description: str = Field(..., description="Details about the skill")


class SoftSkill(BaseModel):
    skill: str = Field(..., description="A soft skill (e.g., Teamwork, Time Management)")
    priority: str = Field(..., description="The priority of the soft skill (e.g., High, Medium)")
    description: str = Field(..., description="Details about the skill")


class Benefit(BaseModel):
    benefit_name: str = Field(..., description="The category of the benefit (e.g., Compensation, Career Growth)")
    description: str = Field(..., description="Details about the benefit")


class CompanyAddress(BaseModel):
    address: Optional[str] = Field(None, description="The place where the company is located")


class JobDetails(BaseModel):
    job_field: str = Field(..., description="The general field of the job (e.g., Web Backend, Embedded Systems, AI)")
    job_hard_skills_required: List[HardSkill] = Field(
        ..., description="A list of all technical requirements and skills needed for the job"
    )
    job_soft_skills_required: Optional[List[SoftSkill]] = Field(
        None, description="A list of soft skills required, or empty if none are specified"
    )
    job_benefits: List[Benefit] = Field(
        ..., description="A list of benefits provided by the job"
    )
    company_address: Optional[CompanyAddress] = Field(
        None, description="The company's address, or empty if not provided in the input"
    )
