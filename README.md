# Connect4
* Brief Introduction of the project - 

  Welcome to this repository 'Connect4.' Let me quickly introduce this project to all of you. So, this project is basically a Django Rest Framework based backend implementation of a popular game 'Connect 4.' In this project, there are 2 main Rest APIs that have been impelemented.
  Following are the APIs:-

  1- /connect4/startgame
	* POST request
	* Take name1, name2 as parameters
	* return a unique token for the game

  2- /connect4/makemove
	* POST request
	* Take column and color as parameters
	* Validate the move
	* In case there is winner, it returns color of winner and winning positions.

  3- /connect4/getallmoves
	* GET request
	* Take no parameter
	* Returns the 2D matrix of all the moves so far.
  
---

* Technologies Used - 
  - Python 3
  - Django 3
  - Django Rest Framework
  
---

* Expected Contributions for beginners - 
  
  Design the complete frontend of the project so as to make it as a full-fledged application. You can use any framework for designing the frontend.
  Some suggestions are - 
  - HTML, CSS, JS with Bootstrap and JQuery.
  - ReactJS
  - AngularJS
  - VueJS etc.
  
  All the requirements of the frontend design are - 
  - First page will be a registration type page where both the players can enter their names.
  - After that, on first page itself there should be a start new game button where /connect4/startgame will hit and new game begins.
  - Next page after it will be a 6*7 grid where players will play. Players will have coins of colors Red & Yellow. They can click on any column & an API /connect4/makemove will hit.
  - Get API response and put the coin in respective row and column as directed by response.
  - In cases there is any winner, game should end highlighting the winner's connect 4.
  
---

* Steps to run the code locally - 

  - Star & fork the repository.
  
  - Clone the repo locally using the command 
    ```git clone```
    
  - Unzip the code files
  
  - Now create a virtual environment of python and activate it
	   ```pip install virtualenv
	    virtualenv venv
	    run .\venv\Scripts\activate on terminal
      
  - Install Django and Django-Rest-Framework using commands
	   ```pip install django
	   pip install djangorestframework
     
  - Once, all installation is done, run the command
	  ```python manage.py makemigrations
	  python manage.py migrate
	  python manage.py runserver
    
  - With this, the server will run and all the APIs can be accessed using http://localhost:8000/<api_name>
  
---

* End note - 
  
  - Feel free to fork, clone and share the repo.
  - Star the repo so that it can get more popular since it is a beginner friendly repository.
  - Contribute in created issues or raise your own issues and I will assign it to you.
  
 ## Happy Hacktober !!!!!
