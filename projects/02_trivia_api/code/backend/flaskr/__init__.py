import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy.sql import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  objects = [obj.format() for obj in selection]
  current_objects = objects[start:end]

  return current_objects

def paginate_questions_search(page, selection):
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  objects = [obj.format() for obj in selection]
  current_objects = objects[start:end]

  return current_objects

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @ Set up CORS. Allow '*' for origins.
  '''
  CORS(app)


  def get_formated_categories():
    categories = Category.query.order_by(Category.id).all()
    categories = [category.format() for category in categories]

    return categories



  '''
  @ Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,OPTIONS')
    return response

  ''' 
  An endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def retrieve_categories():
    categories = get_formated_categories()
    categories_dict = {cat['id']:cat['type'] for cat in categories}

    if len(categories) == 0:
      abort(404)
    else:
      return jsonify({
        'success':True,
        'categories': categories_dict
        })


  ''' 
  An endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def retrieve_questions():
    category_id = request.args.get('cat', -1, type=int)
    if (category_id == -1):
      selection = Question.query.order_by(Question.id).all()
    else:
      selection = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)
    
    categories = get_formated_categories()
    categories_dict = {cat['id']:cat['type'] for cat in categories}

    if len(current_questions) == 0:
      abort(404)
    else:
      return jsonify({
        'success':True,
        'questions': current_questions,
        'total_questions': len(selection),
        'categories': categories_dict,
        'current_category': category_id
        })



  ''' 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods = ['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)

      question.delete()

      return jsonify({
            'success': True,
            'deleted': question.id,
            })

    except:
      abort(422)

  '''
  An endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  '''
  A POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions', methods=['POST'])
  def create_search_question():
    body = request.get_json()
    print(body)
    if 'searchTerm' in body:
      category_id = (lambda x: x if x != None else -1) (body.get('currentCategory'))
      page = body.get('page',1)

      if category_id > 0:
        selection = Question.query.filter(Question.question.ilike('%'+ body['searchTerm'] +'%'), Question.category == category_id).order_by(Question.id).all()
      else:
        selection = Question.query.filter(Question.question.ilike('%'+ body['searchTerm'] +'%')).order_by(Question.id).all()
      
      current_questions = paginate_questions_search(page, selection)
    
      if len(current_questions) == 0:
        abort(404)
      else:
        return jsonify({
          'success':True,
          'questions': current_questions,
          'total_questions': len(selection),
          'current_category': category_id
          })

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_difficulty = body.get('difficulty', None)
    new_category = body.get('category', None)

    try:
     
     
      question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
      question.insert()
      selection = Question.query.order_by(Question.id).all()
      
      current_questions = paginate_questions(request, selection)

      return jsonify({
            'success': True,
            'created': question.id
            })

    except:
      abort(422)

  
  ''' 
  A GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def retrieve_questions_by_category_id(category_id):
    try:
      selection = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
      current_questions = paginate_questions(request, selection)

      if len(current_questions) == 0:
        abort(404)
      else:
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'current_category': category_id
            })

    except:
      abort(422)


  '''
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def retrieve__quiz_questions_by_category_id():
    body = request.get_json()
    print(body)
    previous_questions = body.get('previous_questions')
    
    category_id = (lambda x: int(x['id']) if int(x['id']) > 0 else -1) (body.get('quiz_category'))
    
    try:
      
      
      if previous_questions == None and category_id == -1:
        selection = Question.query.order_by(func.random()).first()
      elif previous_questions != None and category_id == -1:
        selection = Question.query.filter(~Question.id.in_(previous_questions)).order_by(func.random()).first()
      elif previous_questions == None and category_id != -1:
        selection = Question.query.filter(Question.category == category_id).order_by(func.random()).first()
      else:
        selection = Question.query.filter(Question.category == category_id, ~Question.id.in_(previous_questions)).order_by(func.random()).first()

      return jsonify({
            'success': True,
            'previousQuestions': previous_questions,
            'question': (lambda x: x.format() if x != None else None) (selection)
            })

    except:
      abort(422)

  '''
  Error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Resource Not Found"
        }), 404

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "Bad request"
        }), 400

  @app.errorhandler(422)
  def Unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "Unprocessable"
        }), 422
  
  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
        "success": False, 
        "error": 405,
        "message": "Method not allowed"
        }), 405
  
  return app

    