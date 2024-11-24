# JobExtractor

JobExtractor is a Python-based project designed to scrape, process, and store job listings from the Iranian job-finding website Jobinja. The system utilizes Scrapy, LangChain, Redis, and PostgreSQL, organized into three distinct processes for efficient data flow and processing.

## Features

- **Web Scraping**: Collects job data from Jobinja using Scrapy
- **AI-Powered Processing**: Utilizes the Llama 3.2 model through LangChain to process raw scraped data
- **Queue Management**: Handles data flow between processes using Redis queues
- **Database Storage**: Stores processed job information in a PostgreSQL database with custom ORM-mapped classes
- **Docker Integration**: Both Redis and PostgreSQL run in Docker containers for a consistent and portable environment

## Architecture

The project is organized into three processes using Python's multiprocessing module:

### 1. Scraper Process
- Scrapes job listings from Jobinja using Scrapy
- Adds raw scraped data to the raw_data Redis queue through the ExtractorPipeline class

### 2. AI Process
- Retrieves data from the raw_data queue
- Processes the data using a LangChain pipeline with the Llama 3.2 model
- Publishes the processed data into the database Redis queue

### 3. Database Process
- Fetches processed job data from the database Redis queue
- Saves the data to a PostgreSQL database
- Uses custom ORM-mapped classes such as HardSkill, SoftSkill, Benefit, and CompanyAddress

## Technologies Used

- **Python**: Core programming language for all processes
- **Scrapy**: Web scraping framework
- **LangChain**: Framework for AI processing
- **Redis**: In-memory data store used for queueing
- **PostgreSQL**: Relational database for storing processed data
- **Docker**: Containerization for Redis and PostgreSQL
- **SqlAlchemy**: ORM to Interact with PostgreSQL Database.
  
## License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details.
