from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

from .OutputModel import JobDetails


def ai_process(userinput) -> JobDetails:
    # Create the output parser
    parser = PydanticOutputParser(pydantic_object=JobDetails)

    # Get format instructions
    format_instructions = parser.get_format_instructions()

    template = """
    Please follow the format below strictly:
     Field Descriptions:
     job_field: The general field of the job (e.g., "Web Backend", "Embedded Systems", "AI").
     job_hard_skills_required: A list of technical skills needed for the job. Each skill should be an object containing:
         skill_type: Type of the skill (e.g., "Programming Language", "Framework", "Tool").
         skill: The specific skill (e.g., "C", "ASP.NET Core").
         description: what the input has said about this skill.
     job_soft_skills_required: A list of soft skills required for the job. Each skill should be an object containing:
         skill: The name of the soft skill (e.g., "Teamwork", "Time Management").
         priority: The priority of the skill (e.g., "High", "Medium").
         description: what the input has said about this skill.
         (Leave empty if no soft skills are required).
     job_benefits: A list of benefits provided by the employer (e.g., "competitive salary", "flexible hours").
         benefit_name: Name of the benefit (e.g., "Compensation", "Career Growth").
         description: A detailed description of the benefit.
         (Leave empty if no benefits are provided).
     company_address: The company's address, including city, region, and area (e.g., "New York, USA").
         address: The full address or null if not provided.
    
    Input:
    {input}
    
    Answer:
    your answers must fully be in english.
    follow this format strictly:
    
    {{
        "job_field": "<string>",
        "job_hard_skills_required": [
            {{
                "skill_type": "<string>",
                "skill": "<string>",
                "description": "<string>"
            }},
            ...
        ],
        "job_soft_skills_required": [
            {{
                "skill": "<string>",
                "priority": "<string>",
                "description": "<string>"
            }},
            ...
        ],
        "job_benefits": [
            {{
                "benefit_name": "<string>",
                "description": "<string>"
            }},
            ...
        ],
        "company_address": {{
            "address": "<string>"
        }}
    }}
    
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", template),
    ])

    llm = OllamaLLM(model="llama3.2")
    chain = prompt | llm

    # Add the format instructions to the input
    full_input = f"Extract job details from this job description: {userinput}"

    # Generate response
    response = chain.invoke({"input": full_input, "format_instructions": format_instructions})

    # Parse the output
    parsed_result = parser.parse(response)

    # Print the parsed result
    return parsed_result
