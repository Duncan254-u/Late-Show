1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-username/lateshow-firstname-lastname.git
cd lateshow-firstname-lastname
2. Create and Activate a Virtual Environment
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Run Database Migrations
bash
Copy
Edit
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
5. Seed the Database
bash
Copy
Edit
python seed.py
6. Start the Server
bash
Copy
Edit
flask run

 Endpoints
 
Method	Endpoint	Description
GET	/episodes	List all episodes
GET	/episodes/<id>	Retrieve details of a single episode
GET	/guests	List all guests
POST	/appearances	Create a new guest appearance

Test these endpoints using the included Postman collection.

 Features
Models: Episode, Guest, and Appearance

Validation: Ratings must be integers between 1 and 5

Serialization: Controlled JSON output with Marshmallow

Relationships: Foreign keys with cascading deletes

Error Handling: Clean error messages for invalid input

 Tech Stack
 Python 3.11+

 Flask

SQLAlchemy

Marshmallow

Postman (for API testing)

 PostgreSQL (or SQLite for local dev)
