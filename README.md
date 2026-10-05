# Online Library Management System

A full-featured Online Library Management System built with **Django**, **SQLite**, and **TypeScript**. It provides distinct functionalities for students and library staff to manage books, authors, categories, and borrowing records efficiently.

## Features

### For Students
- **Account Management**: Register, login, update profile, and password reset functionalities.
- **Dashboard**: View personal borrowing statistics (currently issued books, total books borrowed).
- **Browse Catalog**: View all available books, authors, and categories.
- **My Books**: Track currently borrowed books and their due dates.

### For Library Staff / Admin
- **Comprehensive Dashboard**: View system-wide statistics (total books, authors, categories, registered students, and active vs. returned issues).
- **Catalog Management**: Full CRUD (Create, Read, Update, Delete) operations for:
  - Books
  - Authors
  - Categories
- **Issue Management**:
  - Issue books to students
  - Track all issued books
  - Mark books as returned
- **Student Management**:
  - View all registered students with dynamic, debounced search powered by a **TypeScript** frontend API integration.
  - View detailed borrowing history for individual students.

## Tech Stack
- **Backend**: Django 5.0+, Python
- **Database**: SQLite (default)
- **Frontend**: HTML, CSS, TypeScript (for asynchronous search features)

## Project Structure
- `core/`: Contains the main Django application including models, views, forms, and templates.
- `olms/`: Django project configuration (settings, urls).
- `static/`: Contains static assets like TypeScript/JavaScript files and CSS.

## Installation & Setup

1. **Navigate to the inner project directory:**
   ```bash
   cd library
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database:**
   ```bash
   python manage.py migrate
   ```

4. **Seed the database with sample data:**
   ```bash
   python manage.py seed
   ```
   *This command creates a demo admin, a demo student, and a sample book.*

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```
   The application will be available at `http://127.0.0.1:8000`.

## Frontend Compilation
If you make changes to the frontend TypeScript files (`static/ts/app.ts`), you need to recompile them using the TypeScript compiler:
```bash
npx tsc
```

## Default Logins
- **Admin**: `admin` / `Test@123`
- **Student**: `john12345` / `Test@123` (or you can register a new student account).

*(Note: Password-reset emails are configured to print directly to the terminal during development).*
