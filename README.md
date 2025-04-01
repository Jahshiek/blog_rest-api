# Blogging Platform API - README  

## Overview  

This is a simple RESTful API built with **Flask** for a personal blogging platform. It supports **CRUD (Create, Read, Update, Delete)** operations on blog posts. The project follows RESTful best practices and includes **Redis caching** for improved performance.  

🔗 **Project URL**: [Blogging Platform API](https://roadmap.sh/projects/blogging-platform-api)  

---

## Features  

- **Create** a new blog post  
- **Retrieve** a single blog post or all posts  
- **Update** an existing blog post  
- **Delete** a blog post  
- **Search** blog posts by title, content, or category  
- **Redis Caching** for faster response times  

---

## Tech Stack  

- **Backend:** Flask  
- **Database:** SQLite / PostgreSQL  
- **Caching:** Redis  
- **HTTP Methods:** GET, POST, PUT, DELETE  

---

## Installation  

### 1️⃣ Clone the Repository  

```bash
git clone https://github.com/your-repo/blogging-platform-api.git
cd blogging-platform-api
```

### 2️⃣ Create a Virtual Environment  

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```

### 3️⃣ Install Dependencies  

```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables  

Create a `.env` file in the root directory and add:  

```env
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=sqlite:///blog.db  # Change to PostgreSQL if needed
REDIS_URL=redis://localhost:6379/0
```

### 5️⃣ Start the Redis Server  

Make sure **Redis** is installed and running:  

```bash
redis-server
```

### 6️⃣ Run the Application  

```bash
flask run
```

The API will be available at **http://127.0.0.1:5000**  

---

## API Endpoints  

### Create a Blog Post  

**POST** `/posts`  

#### Request Body  

```json
{
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post.",
  "category": "Technology",
  "tags": ["Tech", "Programming"]
}
```

#### Response  

```json
{
  "id": 1,
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post.",
  "category": "Technology",
  "tags": ["Tech", "Programming"],
  "createdAt": "2024-10-07T12:00:00Z",
  "updatedAt": "2024-10-07T12:00:00Z"
}
```

---

### Get All Blog Posts  

**GET** `/posts`  

#### Response  

```json
[
  {
    "id": 1,
    "title": "My First Blog Post",
    "content": "This is the content of my first blog post.",
    "category": "Technology",
    "tags": ["Tech", "Programming"],
    "createdAt": "2024-10-07T12:00:00Z",
    "updatedAt": "2024-10-07T12:00:00Z"
  }
]
```

---

### Get a Single Blog Post  

**GET** `/posts/{id}`  

#### Response  

```json
{
  "id": 1,
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post.",
  "category": "Technology",
  "tags": ["Tech", "Programming"],
  "createdAt": "2024-10-07T12:00:00Z",
  "updatedAt": "2024-10-07T12:00:00Z"
}
```

---

### Update a Blog Post  

**PUT** `/posts/{id}`  

#### Request Body  

```json
{
  "title": "Updated Blog Post",
  "content": "This is the updated content.",
  "category": "Tech",
  "tags": ["Flask", "Python"]
}
```

#### Response  

```json
{
  "id": 1,
  "title": "Updated Blog Post",
  "content": "This is the updated content.",
  "category": "Tech",
  "tags": ["Flask", "Python"],
  "createdAt": "2024-10-07T12:00:00Z",
  "updatedAt": "2024-10-07T12:30:00Z"
}
```

---

### Delete a Blog Post  

**DELETE** `/posts/{id}`  

#### Response  

```json
{
  "message": "Blog post deleted successfully."
}
```

---

### Search Blog Posts  

**GET** `/posts?term=tech`  

#### Response  

```json
[
  {
    "id": 1,
    "title": "My First Blog Post",
    "content": "This is the content of my first blog post.",
    "category": "Technology",
    "tags": ["Tech", "Programming"],
    "createdAt": "2024-10-07T12:00:00Z",
    "updatedAt": "2024-10-07T12:00:00Z"
  }
]
```

---

## Error Handling  

| Status Code | Meaning                         |
|------------|--------------------------------|
| 201        | Blog post created successfully |
| 200        | Request successful             |
| 400        | Bad request (validation error) |
| 404        | Blog post not found            |
| 500        | Internal server error          |

---

## Redis Caching  

- **GET /posts** and **GET /posts/{id}** responses are cached in **Redis** for **60 seconds** to reduce database load.  
- To clear the cache, restart Redis or manually remove keys using `redis-cli`.  

---

## Future Improvements  

 **Authentication & Authorization** 
 **Rate Limiting** to prevent abuse  

---

## Contributing  

Contributions are welcome! To contribute:  

1. **Fork** this repo  
2. Create a **new branch** (`feature/new-feature`)  
3. **Commit** changes  
4. Submit a **pull request**  


---

## Contact  

📧 **Email:** Wjahshiek@gmail.com  
📍 **Location:** NY  

