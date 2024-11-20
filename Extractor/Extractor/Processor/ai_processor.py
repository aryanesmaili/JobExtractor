from langchain.output_parsers import PydanticOutputParser  # For parsing output into a Pydantic model
from langchain_core.prompts import ChatPromptTemplate  # To create a structured prompt for the language model
from langchain_ollama import OllamaLLM  # For using the Ollama LLM

from .OutputModel import JobDetails  # Importing the JobDetails Pydantic model for structured output
from ..items import JobInjaJobListItem  # Importing the input model for the job item


def ai_process(userinput: JobInjaJobListItem) -> JobDetails:
    """
    Processes job details from a job listing using a language model and returns
    structured information about the job.

    Args:
        userinput (JobInjaJobListItem): The input containing job title and job content.

    Returns:
        JobDetails: A structured object containing extracted job details.
    """

    # Create the output parser to map the LLM response to the JobDetails Pydantic model
    parser = PydanticOutputParser(pydantic_object=JobDetails)

    # Generate format instructions for the language model based on the Pydantic schema
    format_instructions = parser.get_format_instructions()

    # Define the template for the prompt with detailed instructions
    template = """
    Please follow the format below strictly and Don't say anything but the result object:
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

    # Create a prompt template for the language model using the above instructions
    prompt = ChatPromptTemplate.from_messages([
        ("system", template),
    ])

    # Initialize the language model (Ollama LLM with the specified model)
    llm = OllamaLLM(model="llama3.2")

    # Create a pipeline (chain) combining the prompt template and the LLM
    chain = prompt | llm

    # Prepare the input for the LLM by extracting relevant fields from the user input
    raw_input = {"Job_Title": userinput['job_title'], "Job_Content": userinput['job_content']}
    full_input = f"Extract job details from this job description: {raw_input}"

    # Generate a response from the LLM
    response = chain.invoke({"input": full_input, "format_instructions": format_instructions})

    # Parse the LLM response into the structured JobDetails object
    parsed_result = parser.parse(response)

    # Return the parsed result
    return parsed_result
