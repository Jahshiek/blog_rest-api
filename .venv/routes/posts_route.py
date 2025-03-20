# routes/posts_route.py
from flask import Blueprint, jsonify, request
from models.Messages import Post, Tag
from extensions import db

posts_bp = Blueprint('posts', __name__)



@posts_bp.route('/', methods=['GET'])
def home():
    return 'this is the <h1>HOME PAGE</h1>'
#########################################################################
# Create a new blog post
@posts_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    ("Raw request body:", request.data)
    if request.method == "POST":
        data = request.get_json()

        title = data.get("title")
        content = data.get("content")
        category = data.get( "category")
        tag_names = data.get("tags")
    print(f"title: {title}, content: {content}, category: {category}")

    if not title or not content or not category:
        return jsonify({"error": "Missing required fields"}), 400
    
    new_post = Post(title=title, content=content, category=category)

    tags = []
    for tag_name in tag_names:
        existing_tag = Tag.query.filter_by(name=tag_name).first()
        if not existing_tag:
            existing_tag = Tag(name=tag_name)
            db.session.add(existing_tag)
        tags.append(existing_tag)
    
    new_post.tags = tags

    db.session.add(new_post)
    db.session.commit()

    return jsonify({"message": "Message created successfully", "data": new_post.to_json()}), 201



{
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post.",
  "category": "Technology",
  "tags": ["Tech", "Programming"]
}

# user inputs that data, get that from the request obj

#########################################################################
# Update an existing blog post
@posts_bp.route('/update/<int:id>', methods=['PUT'])
def update_post(id):
    ("Raw request body:", request.data)
    data = request.get_json()

    title = data.get("title")
    content = data.get("content")
    category = data.get( "category")
    tag_names = data.get("tags")

    if not title or not content or not category:
        return jsonify({"error": "Missing required fields"}), 400
    
    updated_Post = Post(title=title, content=content, category=category)

    db.session.add(updated_Post)
    db.session.commit()

    return jsonify({"message": "Missing required fields", "data": updated_Post.to_json()}), 201
#########################################################################
# Delete an existing blog post
@posts_bp.route('/delete/<int:id>', methods=['DELETE', 'POST'])
# @csrf.exempt
def delete_post(id):
    print(f"Delete endpoint reached for post ID: {id}")
    post = Post.query.get(id)

    if not post:
        return jsonify({"error": "message does not exist"}), 400

    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Message deleted successfully"}), 201

#########################################################################

# Get a single blog post
@posts_bp.route('/uniquepost/<int:id>', methods=['GET'])
def get_single_post(id):
    post = Post.query.get(id)

    if post:
        return jsonify({"post": post.to_json()})
    return jsonify({"error": "post does not exist"}), 404

#########################################################################
# Get all blog posts
@posts_bp.route('/posts', methods=['GET'])
def get_all_posts():
    posts = Post.query.all()
    json_posts = list(map(lambda x: x.to_json(), posts))
    if json_posts:
        return jsonify({"posts": json_posts})
    return jsonify({"error":" there are no posts to display"}), 404
#########################################################################
# Filter blog posts by a search term
@posts_bp.route('/posts?term=<term>', methods=['GET'])
def get_post_by_name(term):
    return 'this is the <h1>all posts PAGE</h1>'


# @posts_bp.route('/simpledelete', methods=['DELETE'])
# def simple_delete():
#     print("Simple delete route hit")
#     return jsonify({"message": "Simple delete route works"}), 200