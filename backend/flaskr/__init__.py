from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db
from sqlalchemy.sql.expression import func

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get("SQLALCHEMY_DATABASE_URI")
        setup_db(app, database_path=database_path)

    CORS(app)
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,PATCH,POST,DELETE,OPTIONS"
        )
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories", methods=["GET"])
    def get_categories():
        try:
            categories = Category.query.order_by(Category.id).all()
            formatted_categories = {
                c.id: c.type
                for c in categories
            }

            return jsonify(
                {
                    "success": True,
                    "categories": formatted_categories,
                    "total_categories": len(formatted_categories),
                }
            )
        except Exception as e:
            db.session.rollback()
        finally:
            db.session.close()

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):

        category = Category.query.get(category_id)
        if category is None:
            abort(404)

        questions_by_category_id = Question.query.filter(
            Question.category == category_id
        ).all()
        formatted_questions = [
            question.format() for question in questions_by_category_id
        ]

        return jsonify(
            {
                "success": True,
                "questions": formatted_questions,
                "total_questions": len(formatted_questions),
                "current_category": category.type if category else None,
            }
        )

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions", methods=["GET"])
    def get_questions():
        try:
            page = request.args.get("page", 1, type=int)
            questions = Question.query.order_by(Question.id).paginate(
                page=page, per_page=QUESTIONS_PER_PAGE, error_out=False
            )
            formatted_questions = [question.format() for question in questions.items]
            categories = Category.query.order_by(Category.id).all()
            formatted_categories = {
                c.id: c.type
                for c in categories
            }

            return jsonify(
                {
                    "success": True,
                    "questions": formatted_questions,
                    "total_questions": questions.total,
                    "current_category": None,
                    "categories": formatted_categories
                }
            )
        except Exception as e:
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        question = Question.query.get(question_id)

        if question is None:
            abort(404)

        db.session.delete(question)
        db.session.commit()

        return jsonify(
            {
                "success": True,
                "deleted": question_id,
                "total_questions": Question.query.count(),
            }
        )

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def create_question():
        try:
            body = request.get_json()
            question = Question(
                question=body.get("question", None),
                answer=body.get("answer", None),
                category=body.get("category", None),
                difficulty=body.get("difficulty", None),
            )
            db.session.add(question)
            db.session.commit()

            return jsonify(
                {
                    "success": True,
                    "created": question.id,
                }
            )
        except Exception as e:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions/search", methods=["POST"])
    def search_question():
        try:
            body = request.get_json()
            search = body.get("searchTerm", None)

            questions = Question.query.filter(
                Question.question.ilike(f"%{search}%")
            ).all()
            formatted_questions = [question.format() for question in questions]

            return jsonify(
                {
                    "success": True,
                    "questions": formatted_questions,
                    "total_questions": len(formatted_questions),
                    "current_category": None
                }
            )
        except Exception as e:
            db.session.rollback()
        finally:
            db.session.close()

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/questions/category/<string:category>", methods=["GET"])
    def question_by_category(category):
        category_by_type = Category.query.filter(Category.type.ilike(category)).first()
        if category_by_type is None:
            abort(404)

        questions = (
            db.session.query(Question, Category)
            .join(Category, Question.category == Category.id, isouter=True)
            .filter(Category.type.ilike(f"%{category}%"))
            .all()
        )

        formatted_questions = []
        for q, c in questions:
            question = {
                "question": q.question,
                "answer": q.answer,
                "difficulty": q.difficulty,
                "category": c.type,
            }
            formatted_questions.append(question)

        return jsonify(
            {
                "success": True,
                "questions": formatted_questions,
            }
        )

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def quizzes():
        try:
            body = request.get_json()
            category = body.get("quiz_category", None)
            asked_ids = body.get("previous_questions", None)

            query = (
                db.session.query(Question, Category)
                .join(Category, Question.category == Category.id, isouter=True)
                .filter(Question.id.notin_(asked_ids))
                .order_by(func.random())
            )

            if category["id"] != 0:
                query = query.filter(Category.id == category["id"])

            result = query.first()
            if result:
                q, c = result
                question = {
                        "id": q.id,
                        "question" : q.question,
                        "answer" : q.answer,
                        "difficulty" : q.difficulty,
                        "category": c.type,
                    }
            else:
                question = None

            return jsonify(
                {
                    "success": True,
                    "question": question,
                }
            )

        except Exception as e:
            db.session.rollback()
        finally:
            db.session.close()
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify(
            {"success": False, "error": 404, "message": "Resource not found"}
        ), 404

    @app.errorhandler(400)
    def bad_request(error):

        return jsonify({"success": False, "error": 400, "message": "Bad Request"}), 400

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"success": False, "error": 422, "message": "Unprocessable"}), 422

    return app
