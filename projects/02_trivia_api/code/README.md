# Full Stack API Final Project

## Full Stack Trivia

A web general questions application that includes quizzes and questions in different categories such as Science, Geography, History, Entertainment, Sports & Art.

Application features are as follows:

1) Display questions - both all questions and by category. Questions show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

## Getting Started

### Pre-requisites and Local Development

Developers using this project should already have Python3, pip and node installed on their local machines.

### Backend

From the backend folder run pip install requirements.txt. All required packages are included in the requirements file.
To run the application run the following commands:
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the __init__.py file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the Flask documentation.
The application is running on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.

### Frontend

From the frontend folder, run the following commands to start the client:
```
npm install // only once to install dependencies
npm start
```
By default, the frontend will run on localhost:3000.

## Tests

In order to run tests navigate to the backend folder and run the following commands:
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
The first time you run the tests, omit the dropdb command.
All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started

* Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
* Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "Bad Request"
}
```

The API will return three error types when requests fail:
* 400: Bad Request
* 404: Resource Not Found
* 422: Unprocessable
* 405: Method Not Allowed
* 500: Internal Server Error

### GET /questions

* General
  * Returns a list of questions objects, success value, categories, current category id and total number of questions
  * Results are paginated in groups of 10. Include an optional request argument to choose page number, starting from 1 & another optional argument to choose category id.
* Sample: curl http://127.0.0.1:5000/questions?page=1&cat=1
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": 1, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
```

### POST /questions

* General:
  * Creates a new question using the submitted question, answer, difficulty and category id. Returns the id of the created question, success value.
  
* Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d "{'question':'How many continents are in the world?', 'answer':'7', 'difficulty':'2', 'category':'3'}"
```
{
   "created": 26,
  "success": true
}
```
### DELETE /questions/{question_id}

* General:
  * Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value.
  
* Sample: curl -X DELETE http://127.0.0.1:5000/questions/16
```
{
  "deleted": 16,
  "success": true
}
```

### POST /questions -d {'searchTerm':string, 'currentCategory':int[optional]}

* General:
  * Get questions based on a search term. Returns a list of questions objects, success value, current category id and total number of questions for which the search term 
  is a substring of the question.
  
* Sample:  curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"199", "currentCategory":5}'
```
{
  "current_category": 5,
  "questions": [
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 24,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

### GET /categories

* General:
  * Returns a json object with category id as key and its corresponding category as value and success value
  
* Sample:  curl http://127.0.0.1:5000/categories
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

### GET /categories/{category_id}/questions

* General:
  * Get questions based on a category id. Returns a list of questions objects, success value, current category id and total number of questions of the specified category id.
  
* Sample:  curl http://127.0.0.1:5000/categories/2/questions
```
{
  "current_category": 2, 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ], 
  "success": true, 
  "total_questions": 4
}
```

### POST /quizzes

* General:
  * Get questions to play the quiz. 
  * This endpoint should take category and previous questions IDs as parameters and return a random question within the given category, if provided, and that is not one of the previous questions.
  
* Sample:  curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"previous_questions":[20],"quiz_category":{"type":"Science","id":"1"}}'
```
{
  "previousQuestions": [
    20
  ], 
  "question": {
    "answer": "Alexander Fleming", 
    "category": 1, 
    "difficulty": 3, 
    "id": 21, 
    "question": "Who discovered penicillin?"
  }, 
  "success": true
}
```

## Authors
Mohammed Hany

## Acknowledgements

Special Thanks is given to the Instructors & Reviewers of Udacity Full stack nanodegree program who help towards developing this project.
