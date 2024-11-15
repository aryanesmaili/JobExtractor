import scrapy


class JobInjaJobListItem(scrapy.Item):
    job_title = scrapy.Field()
    job_link = scrapy.Field()
    job_company_name = scrapy.Field()
    job_city = scrapy.Field()
    job_contract_type = scrapy.Field()

    company_image_url = scrapy.Field()
    company_category = scrapy.Field()
    company_population = scrapy.Field()
    company_website = scrapy.Field()
    job_minimum_work_experience = scrapy.Field()
    job_salary = scrapy.Field()
    job_content = scrapy.Field()
    national_service_status = scrapy.Field()

#       jobURL: "", Done
#       CompanyTitle:"", Done
#       CompanyWebsite : "", Done
#       CompanyStaffCount: "", Done
#       CompanyLocationCity: "", Done
#       AdTitle: "", Done
#       MinimumWorkExperienceRequiredYears: "",
#       MilitaryServiceState: True for needed False for not needed None for not mentioned,
#       JobSalary: "int salary if mentioned, None if it is negotiable",
#       JobWorkingHours: fulltime or part time or else,
#       JobField: what tech field is it? web(backend) or embedded systems or AI etc,
#       HardSkillsRequired: "",
#       SoftSkillsRequired: "",
#       Benefits: "",
#       CompanyAddress: "",
