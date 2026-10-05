# Project Summary: Online Library Management System (OLMS)

The **Online Library Management System (OLMS)** is a robust, full-stack web application designed to help librarians manage book inventories, track book issuance, and allow students to browse the library catalog and access digital resources.

## 🛠️ Technology Stack
*   **Backend:** Python with the Django Framework (v6.1.1)
*   **Database:** SQLite (default for development)
*   **Frontend Logic:** TypeScript (`app.ts` compiled to JavaScript)
*   **Frontend UI:** HTML5, CSS3 (using custom Vanilla CSS for a clean, responsive aesthetic)
*   **Serving:** Waitress (WSGI server configured for local deployment)

## 🏗️ Core Architecture & Features

The application is strictly divided into two distinct roles, each with specialized capabilities:

### 1. Librarian (Admin) Features
*   **Dashboard Analytics:** At-a-glance metrics showing total books, authors, categories, registered students, and active vs. returned book loans.
*   **Catalog Management:** Full CRUD (Create, Read, Update, Delete) capabilities for:
    *   **Categories:** Group books by genre or topic.
    *   **Authors:** Manage author profiles.
    *   **Books:** Add books with details like ISBN, price, and digital file attachments.
*   **Issue Tracking System:** Assign books to students, track due dates, and mark books as returned.
*   **Student Management:** View all registered students and their individual borrowing history.

### 2. Student Features
*   **Registration & Profiles:** Secure account creation, authentication, and profile management.
*   **Book Catalog:** A searchable, filterable list of all books available in the library (powered by a real-time TypeScript search script).
*   **Borrowing History:** A dedicated "My Books" dashboard tracking their currently borrowed and returned books.
*   **Digital Notes Portal:** Access to a centralized repository of study materials, documents, and videos.

---

## 🚀 Recent Enhancements & Custom Features

During our development session, we significantly expanded the capabilities of the system:

1. **Digital Asset Integration (The `all notes` Feature):**
   *   Added a secure file-serving endpoint to dynamically read and serve documents directly from the local machine (`C:\Users\Sanjay G L\Downloads\library\all notes`).
   *   Implemented a recursive file crawler (`os.walk`) that penetrates deep into subdirectories to automatically index all 101+ digital notes, PDFs, DOCX, and video files.

2. **The "All Notes" UI:**
   *   Created a dedicated, user-friendly page available from the main navigation bar.
   *   Displays the total count of available resources.
   *   Features a streamlined table with one-click **"Download / Open"** buttons, allowing files to securely stream directly into the browser.

3. **Robust Security Fixes:**
   *   Successfully debugged and neutralized a critical `403 Forbidden` CSRF validation error caused by a rogue, cross-project Service Worker.
   *   Implemented an automated "kill-switch" route (`/sw.js`) that intercepts the browser's background worker requests and gracefully unregisters the corrupted cache layer, restoring full form submission functionality.

4. **Documentation:**
   *   Completely restructured the `README.md` to provide crystal-clear installation steps, command-line arguments, and default login credentials.
