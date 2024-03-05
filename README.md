# DNB ESG Data Hub - Takehome Assignment Prototype

This repository contains a prototype for calculating and reporting the Green Asset Ratio (GAR) for DNB's balance sheet, as defined in the EU Green Taxonomy. The prototype is implemented using Python with FastAPI and SQLite, and includes simple front-end visualization of GAR insights.

## Repository Structure:

- `.gitignore`: Specifies files to be ignored by version control.
- `LICENSE`: The license file.
- `README.md`: Documentation to guide users through the repository.
- `customer.py`: Defines the Pydantic model for customer data validation.
- `database.py`: Contains the database connection setup and session management.
- `gar_calc.py`: Script for calculating the Green Asset Ratio, then loading data into database.
- `index.html`: A simple front-end HTML to display plots.
- `main.py`: The FastAPI application main file with API endpoints.
- `models.py`: SQLAlchemy ORM models for the database schema.
- `taxonomy.json`: The EU Green Taxonomy file.
- `requirements.txt`: Lists all the Python dependencies required for the project.

## Setup and Installation:

1. Clone this repository.
2. Ensure you have Python installed on your system.
3. Install the required dependencies by running `pip install -r requirements.txt`.
4. Update 'gar_calc.py' to point to your own csv file, then run the program.
5. In esg_project directory run uvicorn main:app --reload
6. Open the index.html in a browser to view the plots. The front-end is set up to fetch data from the FastAPI application.

## Considerations

- Secure the API endpoints.
- Replace SQLite with a more scalable database system.
- Optimize database queries and use async endpoints for better performance. Could also pre-calculate plots and store the jsons, then simply retrieve plot instead of calculating it.
- Implement authentication and authorization for sensitive data access.

## Screenshots

![Alt text](screenshots/ratio.png?raw=true "Green ratio")
![Alt text](screenshots/exposure.png?raw=true "Exposure plot")
