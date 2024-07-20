********************
There is a video that should be able to explain all of this some more
The video will also include sample runs of the program, and how to run the program itself
********************


********************
After you have installed python and pip, open command prompt and run the following commands one by one
Then close out that terminal
********************


pip install Flask
pip install Flask-SQLAlchemy
pip install flask-cors
pip install virtualenv
pip install mysqlclient
pip install mysql-connector-python


********************
Go online and download mySQL if you have not, and open the MySQL Command Line Client
You will then be asked for your pasword that you made during the mySQL configuration
Once logged in, run these commands one by one to create the necessary database and tables
********************


CREATE DATABASE cmsc_447_individ_database;

USE cmsc_447_individ_database;

CREATE TABLE Student(studentID VARCHAR(50) PRIMARY KEY, studentName VARCHAR(255) NOT NULL, creditsEarned INT);

CREATE TABLE Instructor(instructorID VARCHAR(50) PRIMARY KEY, instructorName VARCHAR(255) NOT NULL, courseDepartment VARCHAR(100));

CREATE TABLE Course(courseID VARCHAR(50) PRIMARY KEY, courseTitle VARCHAR(255) NOT NULL, instructorID VARCHAR(50), courseCredits INT, FOREIGN KEY (instructorID) REFERENCES Instructor(instructorID));

CREATE TABLE Enrollment(enrollmentID VARCHAR(50) PRIMARY KEY, studentID VARCHAR(50), courseID VARCHAR(50), studentCourseGrade VARCHAR(2), FOREIGN KEY (studentID) REFERENCES Student(studentID), FOREIGN KEY (courseID) REFERENCES Course(courseID));
 

********************
Once that has been done open, close the MySQL command line client, and go to file explorer
Navigate to where the project is installed
Click on the "CMSC 447 Individual Project" folder
Open app.py with notepad
line 7 has the following: 
	
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost:3307/cmsc_447_individ_database'

Change root with your MySQL username, and change password with your MySQL password (both were created during the initital configuration of MySQL)
If you didn't choose a username during the configuration, then root is probably the username, as it's the default
Also, change 3307 to whatever port was chosen during the MySQL configuration, it is set to 3306 by default
********************


********************
Open a comand prompt and navigate to where the project is installed on your computer
Run these commands
********************


cd "CMSC 447 Individual Project"

virtualenv venv

venv\Scripts\activate

flask run


********************
Open a new command prompt and navigate to where the project is installed on your computer
Run these commands

********************


cd "CMSC 447 Individual Project"

venv\Scripts\activate

cd client

npm install axios

npm start


********************
You should be taken to the app around 10 seconds later
Press f12 to open the console.log. Messages will pop up to the user as data gets added/deleted
To view data the database while the app is running, you will need to have the MySQL command line client open and then run the following command
********************


USE cmsc_447_individ_database;


********************
Then use the commands below whenever you wish to view the tables
********************

SELECT * FROM Student;

SELECT * FROM Instructor;

SELECT * FROM Course;

SELECT * FROM Enrollment;



