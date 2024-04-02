## TEAM MEMBERS

- Andy Vo
- Lesmy Caroline Perez Rosales
- Moonhee Kim
- Rishi Vijaybahadursingh Sisodia
- Sk Tanveer Ali

# Project Name

OMS - Order Management System

## Project Architecture

Our Order Management System (OMS) project aims to modernize how we handle orders. By automating tasks and integrating orders from various sources like our physical store, website, and Facebook page, we'll prioritize efficiently, improve communication between teams, and ensure timely deliveries. This will enhance our efficiency and customer satisfaction significantly.

- **Project Directory Structure**: 
- OMS
  - accounts
    - migrations
      - 0001_initial.py
      - ...
    - __init__.py
    - templates
      - accounts
        - dashboard.html
        - delete_order.html
        - delete_user.html
        - employees.html
        - login.html
        - main.html
        - order_form.html
        - orders.html
        - register.html
        - sidebar.html
        - status.html
        - update_user_form.html
        - user_form.html
        - users.html
        - view_order.html
        - view_user.html
    - admin.py
    - apps.py
    - decorators.py
    - forms.py
    - models.py
    - orderFilters.py
    - tests.py
    - urls.py
    - userFilters.py
    - views.py
  - coms
    - __init__.py
    - asgi.py
    - settings.py
    - urls.py
    - wsgi.py
  - media
    - media
      - pexels-jonas-svidras-553236.jpg
      - ...
  - static
    - css
      - main.css
    - images
      - add-icon.svg
      - close-icon.svg
      - dashboard-icon.svg
      - delete-icon.svg
      - drop-down-icon.svg
      - edit-icon.svg
      - filter-icon.svg
      - log-out.svg
      - login-bg.png
      - logo.svg
      - main-laptop-github.jpg
      - main-logo.svg
      - mobile-mockup-github.jpg
      - normal-card.png
      - oms-mockup-github.jpg
      - oms-mood-board.jpg
      - oms-wireframe-github.jpg
      - pending-card.png
      - reports-icon.svg
      - reset-icon.svg
      - search-icon.svg
      - urgent-card.png
      - users-icon.svg
      - view-icon.svg
  - manage.py
  - .gitignore
  - 01-RFP.md
  - 02-Proposal.md
  - 03-Design_Guide.md
  - README.md

- **Database Schema**: TO ADD



## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/582-41W-VA/Project-OMS.git
    ```

2. Navigate to the project directory:

    ```bash
    cd web-project-2-monstermaash
    ```


3. Create a virtual environment:

    ```bash
    python3 -m venv venv
    ```


4. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

4. Install Django:

    ```bash
    pip install django
    ```

5. Install Packages:

You have to install the following packages to run the project:
- django_filter (for filters)
- django pillow (for uploading images)

    ```bash
    pip install django_filter 
    pip install django pillow 
    ```


## Usage


1. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

2. Start the development server:

    ```bash
    python manage.py runserver
    ```
This command will start the Django development server, and your project will be accessible at http://localhost:8000.

3. Open a web browser and navigate to the above URL to view the project.

    ```bash
    open http://localhost:8000
    ```
4. Open the admin panel: http://localhost:8000/admin/

5. Create the following groups:
 
- admin
- manager
- worker

<img src="https://github.com/582-41W-VA/Project-OMS/blob/0e586733e7e954bf7bca0878a6ad5122100b0d2e/OMS/static/images/create_goups.png">

6. In Users, select the superuser created and add admin permissions:

<img src="https://github.com/582-41W-VA/Project-OMS/blob/0e586733e7e954bf7bca0878a6ad5122100b0d2e/OMS/static/images/permissions1.png">


<img src="https://github.com/582-41W-VA/Project-OMS/blob/0e586733e7e954bf7bca0878a6ad5122100b0d2e/OMS/static/images/permissions2.png">

7. Go to homepage http://localhost:8000/ to start the application.


## Contributing

All contributions are welcome. Pull request will be reviewed before merging.

## License

all rights reserved




