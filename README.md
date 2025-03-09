# BlogApp Backend

## Overview

BlogApp Backend is a Django REST Framework (DRF) based application designed to facilitate a seamless digital connection between lecturers and students in colleges and universities. The platform allows lecturers to post news, announcements, and other important information, while students can read and stay updated with the latest posts. This digital approach enhances communication, ensuring that students are always in the loop with what’s happening in their academic environment.

## Features

- **Lecturer Posts**: Lecturers can create, update, and delete posts.
- **Student Access**: Students can view all posts made by lecturers.
- **User Authentication**: Secure authentication system for both lecturers and students.
- **Post Categories**: Posts can be categorized for better organization.
- **Search Functionality**: Students can search for specific posts.
- **Comments**: Students can comment on posts to engage in discussions.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher**
- **PostgreSQL**
- **pip** (Python package installer)
- **virtualenv** (optional but recommended for creating isolated Python environments)

## Installation

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/Jamesnavigator2001/blogApp-backend.git
cd blogapp-backend
```

### 2. Set Up a Virtual Environment (Optional but Recommended)

It's a good practice to create a virtual environment to manage dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL Database

1. **Create a PostgreSQL Database**:

   ```bash
   sudo -u postgres psql
   CREATE DATABASE blogapp;
   CREATE USER blogappuser WITH PASSWORD 'yourpassword';
   ALTER ROLE blogappuser SET client_encoding TO 'utf8';
   ALTER ROLE blogappuser SET default_transaction_isolation TO 'read committed';
   ALTER ROLE blogappuser SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE blogapp TO blogappuser;
   \q
   ```

2. **Update Django Settings**:

   Open `settings.py` in your Django project and update the `DATABASES` configuration:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'blogapp',
           'USER': 'blogappuser',
           'PASSWORD': 'yourpassword',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

### 5. Run Migrations

Apply the initial database migrations:

```bash
python manage.py migrate
```

### 6. Create a Superuser

Create a superuser to access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up your superuser account.

### 7. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The application should now be running at `http://127.0.0.1:8000/`.

## API Endpoints

- **Posts**:
  - `GET /api/posts/` - List all posts.
  - `POST /api/posts/` - Create a new post (Lecturer only).
  - `GET /api/posts/{id}/` - Retrieve a specific post.
  - `PUT /api/posts/{id}/` - Update a specific post (Lecturer only).
  - `DELETE /api/posts/{id}/` - Delete a specific post (Lecturer only).

- **Comments**:
  - `GET /api/posts/{post_id}/comments/` - List all comments for a specific post.
  - `POST /api/posts/{post_id}/comments/` - Create a new comment on a post (Student only).
  - `DELETE /api/comments/{id}/` - Delete a specific comment (Student only).

- **Authentication**:
  - `POST /api/auth/register/` - Register a new user.
  - `POST /api/auth/login/` - Log in an existing user.
  - `POST /api/auth/logout/` - Log out the current user.

## Testing

To run the tests, use the following command:

```bash
python manage.py test
```

## Contributing

If you'd like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Django REST Framework for providing a powerful and flexible toolkit for building Web APIs.
- PostgreSQL for being a reliable and robust database system.

---

Thank you for using BlogApp Backend! If you have any questions or run into any issues, please feel free to open an issue on the GitHub repository. Happy coding! 🚀
