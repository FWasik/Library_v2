# Library_v2 (Virtual Library)

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Screenshots](#screenshots)

## General info
My first "big app". Virtual Library, a web application for handling library orders (create, delete, read).
The application also provides a user authorization and authentication system (also with CRUD). 
Both provided by JWT. The application uses PostgreSQL. Images are stored on Cloudinary.


## Technologies
* Python: 3.9.2
* Django: 3.2.9
* Django REST Framework: 3.12.4
* JavaScript
* React.js: 17.0.2
* PostgreSQL: 13.2
* Docker
* Cloudinary (for image storage)


## Setup
Firstly, we need to install some of the technologies, like Python, React.js, Docker
and PostgreSQL. Needed sites:
https://www.python.org/downloads/   
https://pl.reactjs.org/     
https://www.postgresql.org/     
https://www.docker.com/

Requirements must be install. Install from requirements.txt:
```
pip install -r requirements.txt 
```

Install from Pipfile (with pipenv):
```
pipenv install
```

Testing app:
```
py manage.py test
```

WARNING!    
Test for users will not be run by this command. 
To run test for users use this command:
```
py manage.py test Authentication.tests.{class_to_test}.{method_to_test}
```



### Run
Running application (backend):
```
py manage.py runserver
```

Running applictation (frontend)
```
npm start
```


## Screenshots
Some screenshots of the app:
<img src="https://res.cloudinary.com/gondolin/image/upload/v1645822450/Screenshots/Library/1_ttvban.png"/>
<br />
<br />
<br />
<img src="https://res.cloudinary.com/gondolin/image/upload/v1645822470/Screenshots/Library/2_menf3g.png"/>
<br />
<br />
<br />
<img src="https://res.cloudinary.com/gondolin/image/upload/v1645822454/Screenshots/Library/4_og2a7b.png" width="700px" height="500px"/>
<br />
<br />
<br />
<img src="https://res.cloudinary.com/gondolin/image/upload/v1645822454/Screenshots/Library/3_idxcvm.png" width="600px" height="400px"/>
<br />
<br />
<br />
<img src="https://res.cloudinary.com/gondolin/image/upload/v1645822373/Screenshots/Library/5_igg7s3.png"/>
<br />
<br />
<br />
<img src="https://res.cloudinary.com/gondolin/image/upload/v1645822397/Screenshots/Library/6_ealexw.png"/>
<br />
<br />
<br />
<img src="https://res.cloudinary.com/gondolin/image/upload/v1645824574/Screenshots/Library/12_faey9n.png" width="700px" height="600px"/>
<br />
<br />
<br />
<img src="https://res.cloudinary.com/gondolin/image/upload/v1645822376/Screenshots/Library/7_vnwqts.png" width="400px" height="300px"/>
<br />
<br />
<br />
<img src="https://res.cloudinary.com/gondolin/image/upload/v1645825195/Screenshots/Library/9_rhxmqw.png"/>
<br />
<br />
<br />
<img src="https://res.cloudinary.com/gondolin/image/upload/v1645822376/Screenshots/Library/10_rqy7d7.png" width="400px" height="300px"/>
<br />
<br />
<br />
<img src="https://res.cloudinary.com/gondolin/image/upload/v1645822396/Screenshots/Library/11_wx9tkw.png" width="500px" height="400px"/>
