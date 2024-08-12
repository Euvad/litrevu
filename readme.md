# LitRevu

LitRevu is a Django-based web application for creating, viewing, and managing tickets and reviews. The application allows users to register, log in, follow other users, and interact with tickets and reviews.

## Features

- User registration and authentication.
- Create, view, edit, and delete tickets.
- Create, view, edit, and delete reviews.
- Users can follow other users to see their activities in their feed.
- Media upload for tickets (e.g., images).
- Responsive and user-friendly interface.

## Project Structure

The project is structured into the following Django apps:

- **accounts**: Manages user registration, authentication, and user profile.
- **tickets**: Handles the creation, viewing, and management of tickets.
- **reviews**: Manages the creation and management of reviews linked to tickets.
- **social**: Manages user interactions like following other users.
- **feed**: Displays a personalized feed for the user showing tickets and reviews.

## Prerequisites

- Python 3.11.x or higher
- Django 5.0.7
- SQLite (for development)

## Setup and Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/litrevu.git
   cd litrevu
   ```

2. **Create a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**:

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

7. **Access the application**:

   Open your browser and go to `http://127.0.0.1:8000/`.

## Usage

- **Register** a new account or log in with an existing one.
- **Create tickets** to request reviews or feedback.
- **Create reviews** for tickets, either your own or others.
- **Follow users** to keep track of their activity.
- **View your feed** to see the latest tickets and reviews from users you follow.

