import os
import unittest
import json

from flaskr import create_app
from models import db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_user = os.getenv("DATABASE_USER")
        self.database_password = os.getenv("DATABASE_PASSWORD")
        self.database_user = 'postgres'
        self.database_password = 'password'
        self.database_host = "localhost:5432"
        self.database_path = f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}/{self.database_name}"

        # Create app with the test configuration
        self.app = create_app(
            {
                "SQLALCHEMY_DATABASE_URI": self.database_path,
                "SQLALCHEMY_TRACK_MODIFICATIONS": False,
                "TESTING": True,
            }
        )
        self.client = self.app.test_client()

        # Bind the app to the current context and create all tables
        with self.app.app_context():
            db.create_all()
            # Insert sample Science category and question
            science_category = Category(type="Science")
            db.session.add(science_category)
            db.session.commit()
            
            science_question = Question(
                question="What is the boiling point of water?",
                answer="100°C",
                category=science_category.id,
                difficulty=1,
            )
            db.session.add(science_question)
            db.session.commit()
            # Insert sample Art category and question
            art_category = Category(type="Art")
            db.session.add(art_category)
            db.session.commit()
            art_question = Question(
                question="Who painted the Mona Lisa?",
                answer="Leonardo da Vinci",
                category=art_category.id,
                difficulty=2,
            )
            db.session.add(art_question)
            db.session.commit()

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_categories(self):
        res = self.client.get("/categories")
        data = json.loads(res.data)

        expected_categories = {"1": "Science", "2": "Art"}
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["categories"], expected_categories)
        self.assertEqual(data["total_categories"], 2)

    def test_get_questions_by_category(self):
        res = self.client.get("/categories/1/questions")
        data = json.loads(res.data)

        expected_questions = [
            {
                "answer": "100°C",
                "category": 1,
                "difficulty": 1,
                "id": 1,
                "question": "What is the boiling point of water?",
            }
        ]
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["questions"], expected_questions)
        self.assertEqual(data["total_questions"], 1)
        self.assertEqual(data["current_category"], "Science")

    def test_404_get_questions_by_category(self):
        res = self.client.get("/categories/9/questions")

        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "Resource not found")

    def test_get_questions(self):
        res = self.client.get("/questions")
        data = json.loads(res.data)

        expected_questions = [
            {
                "answer": "100°C",
                "category": 1,
                "difficulty": 1,
                "id": 1,
                "question": "What is the boiling point of water?",
            },
            {
                "answer": "Leonardo da Vinci",
                "category": 2,
                "difficulty": 2,
                "id": 2,
                "question": "Who painted the Mona Lisa?",
            },
        ]
        expected_categories = {"1": "Science", "2": "Art"}
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["questions"], expected_questions)
        self.assertEqual(data["total_questions"], 2)
        self.assertEqual(data["current_category"], None)
        self.assertEqual(data["categories"], expected_categories)

    def test_delete_question(self):
        res = self.client.delete("/questions/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["deleted"], 1)
        self.assertEqual(data["total_questions"], 1)

    def test_404_delete_question(self):
        res = self.client.delete("/questions/4")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "Resource not found")

    def test_create_question(self):
        new_question = {
            "question": "What is the capital of France?",
            "answer": "Paris",
            "category": 1,
            "difficulty": 2
        }
        res = self.client.post("/questions", json=new_question)
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["created"], 3)
    
    def test_422_create_question(self):
        new_question = {}
        res = self.client.post("/questions", json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], "Unprocessable")


    def test_search_question(self):
        res = self.client.post("/questions/search", json={"searchTerm": "boiling"})
        data = json.loads(res.data)

        expected_questions = [{'answer': '100°C', 'category': 1, 'difficulty': 1, 'id': 1, 'question': 'What is the boiling point of water?'}]
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertEqual(data["questions"], expected_questions)
        self.assertEqual(data["total_questions"], 1)
        self.assertEqual(data["current_category"], None)

    def test_question_by_category(self):
        res = self.client.get("/questions/category/science")
        data = json.loads(res.data)

        expected_questions = [{'answer': '100°C', 'category': "Science", 'difficulty': 1, 'question': 'What is the boiling point of water?'}]
        self.assertTrue(data["success"])
        self.assertEqual(data["questions"], expected_questions)

    def test_404_question_by_category(self):
        res = self.client.get("/questions/category/asdasd")
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], "Resource not found")

    def test_quizzes(self):
        res = self.client.post("/quizzes", json={
            "quiz_category": {
                "id": 2,
                "type": "Art"
            },
            "previous_questions": []
        })
        data = json.loads(res.data)

        expected_questions = {'answer': 'Leonardo da Vinci', 'category': 'Art', 'difficulty': 2, 'id': 2, 'question': 'Who painted the Mona Lisa?'}
        self.assertTrue(data["success"])
        self.assertEqual(data["question"], expected_questions)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
