# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```


### Set up Environment Variables

Create a `.env` file in the project root with the following values (replace with your own credentials):

```env
DATABASE_USER=your_db_username
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost:5432
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## API reference

### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category  
- Request Arguments: None  
- Returns: An object with categories and their ids  

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

---

### GET '/categories/<int:category_id>/questions'
- Fetches questions based on category id  
- Request Arguments: `category_id` (integer)  
- Returns: A list of questions for the category, total number of questions, and current category  

```json
{
  "success": true,
  "questions": [
    {
      "id": 1,
      "question": "What is the capital of France?",
      "answer": "Paris",
      "category": 3,
      "difficulty": 2
    }
  ],
  "total_questions": 1,
  "current_category": "Geography"
}
```

---

### GET '/questions'
- Fetches paginated questions (10 per page)  
- Request Arguments: `page` (optional, default=1)  
- Returns: A list of questions, total number of questions, categories, and current category  

```json
{
  "success": true,
  "questions": [
    {
      "id": 2,
      "question": "Who painted the Mona Lisa?",
      "answer": "Leonardo da Vinci",
      "category": 2,
      "difficulty": 2
    }
  ],
  "total_questions": 20,
  "current_category": null,
  "categories": {
    "1": "Science",
    "2": "Art"
  }
}
```

---

### DELETE '/questions/<int:question_id>'
- Deletes a question by ID  
- Request Arguments: `question_id` (integer)  
- Returns: The id of the deleted question and updated total  

```json
{
  "success": true,
  "deleted": 5,
  "total_questions": 19
}
```

---

### POST '/questions'
- Creates a new question  
- Request Body:  
```json
{
  "question": "What is the capital of India?",
  "answer": "New Delhi",
  "category": 3,
  "difficulty": 2
}
```  
- Returns: The id of the created question  

```json
{
  "success": true,
  "created": 25
}
```

---

### POST '/questions/search'
- Searches for questions containing a search term  
- Request Body:  
```json
{
  "searchTerm": "title"
}
```  
- Returns: A list of matching questions  

```json
{
  "success": true,
  "questions": [
    {
      "id": 6,
      "question": "What is the title of the national anthem of USA?",
      "answer": "The Star-Spangled Banner",
      "category": 4,
      "difficulty": 2
    }
  ],
  "total_questions": 1,
  "current_category": null
}
```

---

### GET '/questions/category/<string:category>'
- Fetches questions by category name  
- Request Arguments: `category` (string)  
- Returns: A list of questions belonging to the given category  

```json
{
  "success": true,
  "questions": [
    {
      "question": "What is H2O commonly known as?",
      "answer": "Water",
      "difficulty": 1,
      "category": "Science"
    }
  ]
}
```

---

### POST '/quizzes'
- Fetches a random question for quiz play  
- Request Body:  
```json
{
  "previous_questions": [1, 2],
  "quiz_category": {"id": 1, "type": "Science"}
}
```  
- Returns: A random question not asked before in the given category  

```json
{
  "success": true,
  "question": {
    "id": 7,
    "question": "What planet is known as the Red Planet?",
    "answer": "Mars",
    "difficulty": 2,
    "category": "Science"
  }
}
```

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 

## Testing

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python -m unittest test_flaskr.py
```

## Authors
Rahul Gupta

## Acknowledgements 
Forked from Udacity API-development-and-Documentation
