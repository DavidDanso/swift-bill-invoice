# Swift Bill Invoice App

An invoice management web application built with Django, PostgreSQL, and AWS services (S3 for file storage and RDS for database).

## Features

- User authentication and authorization
- Create, edit, and delete invoices
- Generate PDF invoices
- Email invoices to clients
- Dashboard for overview of invoices
- Search and filter functionality for invoices
- Upload and download invoice files (PDFs)
- Responsive design for mobile and desktop

## Setup

### Prerequisites

- Python 3.x
- PostgreSQL
- AWS account with S3 and RDS setup

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/DavidDanso/swift-bill-invoice.git

2. #### Navigate to the project directory:
    ```
    cd swift-bill-invoice/
    ```
    
3. Create a virtual environment:

   ```bash
   python3 -m venv env

4. Activate the virtual environment:
   
   ### On macOS and Linux:

   ```bash
   source env/bin/activate

5. Install the required dependencies::

   ```bash
   pip install -r requirements.txt

### Configuring PostgreSQL, AWS S3, and RDS

1. Configure PostgreSQL:

   - Download PostgreSQL [ https://www.postgresql.org ]
   - Create a new database in PostgreSQL.
   - Use the database name, username, password, host, and port details to configure the project's settings.
  
2. Configure AWS S3 and RDS:

   - Set up an AWS account if you haven't already.
   - Create an S3 bucket to store invoice files.
   - Set up an RDS instance with PostgreSQL as the database engine.
   - Configure the necessary permissions for S3 and RDS, and note down the access credentials.
  
3. Modify Django settings:

   - Modify the DATABASES setting in your project's settings.py file to use AWS RDS.
   - Configure AWS S3 settings in settings.py.
  
## Connecting Django to Database:
In your project's settings.py file, modify the DATABASES setting to use AWS RDS:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'YOUR_DB_NAME',
        'USER': 'YOUR_DB_USERNAME',
        'PASSWORD': 'YOUR_DB_PASSWORD',
        'HOST': 'YOUR_DB_HOST',
        'PORT': 'YOUR_DB_PORT',
    }
}
```

### Configure AWS S3 settings in settings.py:

```
AWS_STORAGE_BUCKET_NAME = 'YOUR_S3_BUCKET_NAME'
AWS_ACCESS_KEY_ID = 'YOUR_AWS_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY = 'YOUR_AWS_SECRET_ACCESS_KEY'
AWS_S3_REGION_NAME = 'YOUR_AWS_REGION_NAME'
```

## Running the Server:

Create initial migrations:
Run the following command to create initial migrations based on your models:
```
python3 manage.py makemigrations
```

Apply migrations:
Apply the migrations to the database:
```
python3 manage.py migrate
```

Run Server:
```
python3 manage.py runserver
```

`Visit http://localhost:8000 in your web browser to access the site.`

## Superuser Account
Create a superuser account:
To access the admin interface and manage users, create a superuser account using the following command:
```
python3 manage.py createsuperuser
```

<table width="100%"> 
  <tr>
    <td width="70%">      
    &nbsp; 
    <br>
    <p align="center">
      Home Page
    </p>
    <img src="https://github.com/DavidDanso/swift-bill-invoice/blob/main/static/images/UI/home-page.png?raw=true" />
    </td> 
    <td width="40%">
    <br>
    <p align="center">
      Invoice Interface
    </p>
    <img src="https://github.com/DavidDanso/swift-bill-invoice/blob/main/static/images/UI/invoice.png?raw=true" />
    </td>
  </tr>

  <tr>
    <td width="50%">      
    &nbsp; 
    <br>
    <p align="center">
      Signup Screen
    </p>
    <img src="https://github.com/DavidDanso/swift-bill-invoice/blob/main/static/images/UI/signup.png?raw=true" />
    </td> 
    <td width="50%">
    <br>
    <p align="center">
     Login Screen
    </p>
    <img src="https://github.com/DavidDanso/swift-bill-invoice/blob/main/static/images/UI/login.png?raw=true" />
    </td>
  </tr>

  <tr>
    <td width="50%">      
    &nbsp; 
    <br>
    <p align="center">
      Welcome Screen
    </p>
    <img src="https://github.com/DavidDanso/swift-bill-invoice/blob/main/static/images/UI/welcome-page.png?raw=true" />
    </td> 
    <td width="50%">
    <br>
    <p align="center">
     Client Page
    </p>
    <img src="https://github.com/DavidDanso/swift-bill-invoice/blob/main/static/images/UI/create_client.png?raw=true" />
    </td>
  </tr>

  <tr>
    <td width="50%">      
    &nbsp; 
    <br>
    <p align="center">
      Invoice Page
    </p>
    <img src="https://github.com/DavidDanso/swift-bill-invoice/blob/main/static/images/UI/create_invoice.png?raw=true" />
    </td> 
    <td width="50%">
    <br>
    <p align="center">
     Profile Page
    </p>
    <img src="https://github.com/DavidDanso/swift-bill-invoice/blob/main/static/images/UI/profile.png?raw=true" />
    </td>
  </tr>

  <tr>
    <td width="100%">
    <br>
    <p align="center">
     Dashboard Page
    </p>
    <img src="https://github.com/DavidDanso/swift-bill-invoice/blob/main/static/images/UI/dashboard.png?raw=true" />
    </td>
  </tr>
</table>


## Author
David Danso - Initial work - [GitHub Profile](https://github.com/DavidDanso)

##### Email: davidkellybrownson@gmail.com

### Happy Coding!
