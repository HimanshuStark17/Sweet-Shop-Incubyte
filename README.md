# Sweet Shop Management System

A full-stack web application for managing a sweet shop with user authentication, inventory management, and purchase functionality.


## ✨ Features

### User Features
- 🔐 User registration and login with JWT authentication
- 🍭 Browse catalog of available sweets
- 🔍 Search sweets by name or description
- 🏷️ Filter sweets by category
- 🛒 Purchase sweets with real-time quantity updates
- 📊 View purchase history
- 🚫 Disabled purchase button when items are out of stock

### Admin Features
- ➕ Add new sweets to inventory
- ✏️ Edit existing sweet details
- 🗑️ Delete sweets from catalog
- 📈 Manage inventory quantities and prices
- 👥 Role-based access control

### General Features
- 📱 Responsive design (mobile & desktop)
- 🎨 Modern gradient UI with Tailwind CSS
- 🔄 Real-time data updates
- 🔒 Secure password hashing
- 🛡️ Protected API routes with JWT tokens

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **PostgreSQL** - Database
- **psycopg2** - PostgreSQL adapter
- **Flask-CORS** - Cross-origin resource sharing
- **PyJWT** - JSON Web Token authentication
- **Werkzeug** - Password hashing

### Frontend
- **React 18+**
- **Tailwind CSS** - Styling
- **Lucide React** - Icons
- **Fetch API** - HTTP requests

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- [Python 3.8+](https://www.python.org/downloads/)
- [PostgreSQL 12+](https://www.postgresql.org/download/)
- [Node.js 14+](https://nodejs.org/) (for frontend)
- [npm](https://www.npmjs.com/) (comes with Node.js)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/sweetshop.git
cd sweetshop
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install
```

## 🗄️ Database Setup

### 1. Create Database

**Using psql:**
```bash
psql -U postgres
CREATE DATABASE sweetshop;
\q
```

**Using pgAdmin:**
1. Open pgAdmin
2. Right-click on "Databases"
3. Select "Create" → "Database"
4. Name: `sweetshop`
5. Click "Save"

### 2. Configure Database Connection

Edit `backend/app.py` (lines 11-16):

```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'sweetshop',
    'user': 'postgres',
    'password': 'your_password'  # Change this!
}
```

### 3. Initialize Tables

Tables will be automatically created when you first run the backend server. Alternatively, run:

```sql
-- Connect to sweetshop database
\c sweetshop

-- Tables will be created automatically by app.py
-- Or manually create using the SQL in backend/init_db.sql
```

### 4. Insert Sample Data (Optional)

```sql
INSERT INTO sweets (name, description, price, quantity, category) VALUES
('Gulab Jamun', 'Deep-fried milk solids soaked in sugar syrup', 50.00, 20, 'Traditional'),
('Rasgulla', 'Soft cottage cheese balls in sugar syrup', 40.00, 25, 'Traditional'),
('Jalebi', 'Crispy coiled batter soaked in sugar syrup', 30.00, 30, 'Traditional'),
('Kaju Katli', 'Diamond-shaped cashew fudge', 100.00, 10, 'Premium');
```

## 🎮 Running the Application

### Start Backend Server

```bash
# Make sure you're in backend directory with venv activated
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Run server
python app.py
```

Backend will run on: `http://localhost:5000`

### Start Frontend Server

```bash
# Open new terminal and navigate to frontend
cd frontend

# Start React app
npm start
```

Frontend will open automatically on: `http://localhost:3000`

## 👤 Creating Admin User

Regular users are created through registration. To make a user admin:

```sql
-- Connect to database
psql -U postgres -d sweetshop

-- Make user admin (replace 'username' with actual username)
UPDATE users SET is_admin = true WHERE username = 'testuser';

-- Verify
SELECT username, is_admin FROM users;

-- Exit
\q
```

**Then logout and login again to see admin features!**

## 🌐 API Endpoints

### Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/register` | Register new user | No |
| POST | `/api/login` | Login user | No |

### Sweets (Public)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/sweets` | Get all sweets | No |
| GET | `/api/sweets/:id` | Get single sweet | No |
| GET | `/api/categories` | Get all categories | No |

### Sweets (Admin Only)
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/sweets` | Add new sweet | Admin |
| PUT | `/api/sweets/:id` | Update sweet | Admin |
| DELETE | `/api/sweets/:id` | Delete sweet | Admin |

### Orders
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/purchase` | Purchase sweet | User |
| GET | `/api/orders` | Get user orders | User |

## 📁 Project Structure

```
sweetshop/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   └── venv/                  # Virtual environment
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── index.js          # Entry point
│   │   └── ...
│   ├── package.json          # Node dependencies
│   └── node_modules/
└── README.md
```

## 🤖 My AI Usage

### AI Tools Used
During the development of this Sweet Shop Management System, I utilized **Claude AI (Anthropic)** as my primary AI assistant throughout the entire development process.

### How I Used AI

#### 1. **Project Architecture & Planning**
- **What I did:** I described my requirements for a sweet shop management system with user authentication, inventory management, and purchase functionality.
- **How AI helped:** Claude helped me design the complete system architecture, suggesting a Flask backend with PostgreSQL database and React frontend. It recommended the tech stack considering scalability, security, and ease of implementation.
- **Example prompt:** "I need a full frontend+backend code for a sweetshop management system using PostgreSQL database with user registration, login, dashboard, search/filter functionality, purchase buttons, and admin features."

#### 2. **Backend Development (Python/Flask)**
- **What I did:** I requested a complete RESTful API with authentication.
- **How AI helped:** 
  - Generated the entire Flask application structure with proper routing
  - Implemented JWT-based authentication with secure password hashing
  - Created database models and relationships (users, sweets, orders tables)
  - Set up proper error handling and validation
  - Implemented role-based access control (admin vs regular users)
- **Code generated:** Complete `app.py` file with all API endpoints, database initialization, and middleware functions.

#### 3. **Database Design & SQL Queries**
- **What I did:** I needed help setting up PostgreSQL database and writing queries.
- **How AI helped:**
  - Provided complete SQL schema for creating tables with proper relationships
  - Generated insert statements for sample data
  - Created advanced queries for analytics (sales reports, inventory management)
  - Provided troubleshooting queries for database maintenance
- **Deliverable:** Comprehensive SQL query file with 13 sections covering all database operations.

#### 4. **Frontend Development (React)**
- **What I did:** I requested separate login and register screens with a modern UI.
- **How AI helped:**
  - Built a complete React application with state management using hooks
  - Implemented three distinct views (Login, Register, Dashboard)
  - Created responsive UI components with Tailwind CSS
  - Integrated API calls with proper error handling
  - Fixed form handling issues (removed HTML form tags, used onClick handlers)
  - Resolved localStorage implementation for token management
- **Iterations:** Modified the frontend 3 times based on my feedback (combined auth modal → separate screens → fixed form handling).

#### 5. **Debugging & Troubleshooting**
- **What I did:** I encountered various errors during setup and runtime.
- **How AI helped:**
  - **Error:** "ModuleNotFoundError: No module named 'flask'"
    - **Solution:** Claude provided step-by-step virtual environment setup and package installation commands
  - **Error:** "relation 'users' does not exist"
    - **Solution:** Created initial setup SQL script with proper table creation order
  - **Error:** "Module not found: web-vitals"
    - **Solution:** Provided npm install command and explained the cause
  - **Error:** "Unexpected use of 'confirm'"
    - **Solution:** Changed `confirm()` to `window.confirm()` to fix ESLint error

#### 6. **Documentation**
- **What I did:** I needed comprehensive documentation for the project.
- **How AI helped:**
  - Created a professional README.md with badges, detailed sections, and formatting
  - Generated step-by-step setup instructions in both English and Hindi
  - Provided troubleshooting guides with common errors and solutions
  - Created SQL query documentation with examples and use cases

#### 7. **Requirements & Dependencies**
- **What I did:** I needed a proper requirements.txt file.
- **How AI helped:** Generated a complete requirements.txt with specific versions of all Python packages needed (Flask, Flask-CORS, psycopg2-binary, PyJWT, Werkzeug).

### Specific Examples of AI Assistance

**Example 1: API Endpoint Structure**
```
My request: "I need purchase functionality with authentication"
AI response: Created a complete /api/purchase endpoint with:
- JWT token verification
- Stock availability checking
- Automatic quantity reduction
- Order record creation
- Transaction handling
```

**Example 2: Frontend State Management**
```
My request: "First login and register screen should be visible"
AI response: Implemented view-based routing using useState:
- currentView state to switch between 'login', 'register', 'dashboard'
- Automatic redirect after successful registration
- Token persistence using localStorage
```

**Example 3: Security Implementation**
```
My request: "Admin users should be able to add/edit/delete sweets"
AI response: Created complete RBAC system:
- Admin-only decorator functions
- Token-based authentication middleware
- Protected routes with proper authorization checks
```

### Reflection on AI Impact

#### Positive Impacts:

1. **Accelerated Development:**
   - What would have taken 2-3 days of coding was completed in a few hours
   - I could focus on understanding concepts rather than syntax
   - Rapid prototyping and iteration based on feedback

2. **Learning & Understanding:**
   - AI explained WHY certain approaches were better (e.g., JWT vs sessions)
   - Learned best practices for Flask API development
   - Understood React hooks and state management through working examples
   - Gained knowledge of PostgreSQL relationships and query optimization

3. **Comprehensive Solutions:**
   - Got complete, production-ready code instead of snippets
   - Proper error handling was included from the start
   - Security considerations (password hashing, SQL injection prevention) were built-in

4. **Debugging Efficiency:**
   - Instead of searching Stack Overflow for hours, got instant solutions
   - AI understood context and provided targeted fixes
   - Learned to read error messages more effectively

5. **Documentation Quality:**
   - Professional README with all necessary sections
   - Step-by-step guides in multiple languages (English/Hindi)
   - Clear explanations for setup and troubleshooting

#### Challenges & Limitations:

1. **Initial Code Issues:**
   - First version used HTML `<form>` tags which weren't supported in the artifact environment
   - Required iteration to fix (changed to onClick handlers)
   - Learned that AI-generated code needs testing and validation

2. **Context Understanding:**
   - Had to clarify requirements multiple times (e.g., "separate login and register screens")
   - AI initially created a modal-based auth system, which I had to request to change

3. **Environment-Specific Issues:**
   - Some solutions assumed standard environments
   - Needed to adapt for Windows vs Linux commands
   - Required troubleshooting for specific local setup issues

4. **Dependency on AI:**
   - Risk of not fully understanding all generated code
   - Important to review and understand each part
   - Should not blindly copy-paste without comprehension

#### What I Learned:

1. **How to effectively use AI:**
   - Be specific in prompts ("I want separate screens" vs "I want auth")
   - Iterate based on results
   - Ask for explanations when concepts are unclear

2. **Technical Skills Gained:**
   - Full-stack development workflow
   - REST API design principles
   - React component architecture
   - PostgreSQL database design
   - JWT authentication implementation
   - Security best practices

3. **Problem-Solving Approach:**
   - Break problems into smaller tasks
   - Test incrementally (backend first, then frontend)
   - Use AI for debugging but understand the root cause

#### Best Practices When Using AI for Development:

1. ✅ **Start with clear requirements** - Be specific about what you need
2. ✅ **Review generated code** - Don't blindly trust; understand what it does
3. ✅ **Test incrementally** - Test each component before moving forward
4. ✅ **Ask for explanations** - When you don't understand something, ask why
5. ✅ **Iterate based on feedback** - Refine the solution through conversation
6. ✅ **Use for learning** - Treat AI as a tutor, not just a code generator
7. ✅ **Verify security** - Double-check authentication and validation logic
8. ✅ **Document everything** - AI can help create comprehensive documentation

### Conclusion

Using Claude AI significantly enhanced my development workflow. It acted as:
- **A senior developer** providing architecture guidance
- **A coding assistant** generating boilerplate and complex logic
- **A debugging partner** helping identify and fix errors
- **A documentation writer** creating comprehensive guides
- **A teacher** explaining concepts and best practices

The key was maintaining active engagement - asking questions, requesting modifications, and ensuring I understood the generated code. This project demonstrated that AI is a powerful tool that amplifies productivity when used thoughtfully, but it's essential to maintain critical thinking and code review practices.

**Time Saved:** Approximately 70-80% reduction in development time  
**Learning Gained:** Equivalent to multiple tutorials and documentation reading  
**Code Quality:** Professional-grade with proper error handling and security  
**Overall Experience:** Highly positive - AI transformed my development workflow

## 📸 Screenshots

### Login Screen
Beautiful gradient login interface with username and password fields.
![WhatsApp Image 2025-12-15 at 22 59 10_d7e8a257](https://github.com/user-attachments/assets/f77332cf-b869-4edf-88ee-89d4de10b3ae)


### Register Screen
Separate registration page with username, email, and password fields.
![WhatsApp Image 2025-12-15 at 22 59 42_148a187e](https://github.com/user-attachments/assets/83716990-c779-456a-bd13-48d47b2632b0)



## 🐛 Troubleshooting

### Backend Issues

**Problem:** `ModuleNotFoundError: No module named 'flask'`
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Problem:** `could not connect to server`
```bash
# Solution: Check PostgreSQL is running
# Windows: Services → PostgreSQL
# Mac: brew services list
# Linux: sudo systemctl status postgresql
```

**Problem:** `database "sweetshop" does not exist`
```sql
-- Solution: Create database
CREATE DATABASE sweetshop;
```

### Frontend Issues

**Problem:** `Module not found: Error: Can't resolve 'web-vitals'`
```bash
# Solution: Install missing package
npm install web-vitals
```

**Problem:** `Port 3000 already in use`
```bash
# Solution: Use different port
PORT=3001 npm start
```

**Problem:** CORS errors
```bash
# Solution: Make sure backend is running
# Check Flask-CORS is installed
pip install Flask-Cors
```




