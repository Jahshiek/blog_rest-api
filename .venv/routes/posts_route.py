# routes/posts_route.py
from flask import Blueprint, jsonify, request
from models.Messages import Post, Tag
from extensions import db,redis_client
import json

posts_bp = Blueprint('posts', __name__)




# Create a new blog post
@posts_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    print("Raw request body:", request.data)

    if request.method == 'POST':
        data = request.get_json()

        # Get the individual fields
        title = data.get("title")
        content = data.get("content")
        category = data.get("category")
        tag_names = data.get("tags")

        print(f"title: {title}, content: {content}, category: {category}")

        if not title or not content or not category:
            return jsonify({"error": "Missing required fields"}), 400

        new_post = Post(title=title, content=content, category=category)

        tags = []
        for tag_name in tag_names:
            existing_tag = Tag.query.filter_by(name=tag_name).first()
            if not existing_tag:
                new_tag = Tag(name=tag_name)
                db.session.add(new_tag)
                db.session.flush()
            else:
                new_tag = existing_tag
            tags.append(new_tag)

        # Move this outside the loop
        new_post.tags = tags  

        db.session.add(new_post)
        db.session.commit()

        return jsonify({"message": "Post created successfully", "data": new_post.to_json()}), 201
    #Handle Get
    return jsonify({"message": "Use POST to create a post"}), 405


# Update an existing blog post
@posts_bp.route('/update/<int:id>', methods=['PUT'])
def update_post(id):
    post = Post.query.get(id)

    if not post:
        jsonify({"error": "Youre not modifying the right post"}), 400

    data = request.get_json()
    print(data)
    title = data.get("title")
    content = data.get("content")
    category = data.get( "category")
    
    if not title or not content or not category:
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        post.title = title
        post.content = content
        post.category = category

        db.session.commit()
        return jsonify({"message": "Message Created successfully", "data": post.to_json()}), 201
    except:
        return jsonify({"error": "Message could not be updated"})

    


# Delete an existing blog post
# @posts_bp.route('/delete/<int:id>', methods=['DELETE'])
# def delete_post(id):
#     post = Post.query.get(id)

#     if not post:
#         jsonify({"error": "post does not exist"}), 400
    
#     db.session.delete(post)
#     db.session.commit()

#     return jsonify({"Message": "Post deleted succesfully"}), 201

# Delete an existing blog post
@posts_bp.route('/delete/<int:id>', methods=['DELETE', 'POST'])
# @csrf.exempt
def delete_post(id):

    print(f"Delete endpoint reached for post ID: {id}")
    post = Post.query.get(id)

    if not post:
        return jsonify({"error": "message does not exist"}), 400
    
    cache_id = f"post{id}"
    if redis_client.exists(cache_id):
        redis_client.delete(cache_id)

    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Message deleted successfully"}), 200

# Get a single blog post

@posts_bp.route('/post/<int:id>', methods=['GET'])
def single_post(id):
    cache_key = f"individual_post_{id}"
    individual_cached_post = redis_client.get(cache_key)

    if individual_cached_post:
        return jsonify({"source": "cacahe", "data": json.loads(individual_cached_post)})
    
    
    post = Post.query.get(id)
    if not post:
        jsonify({"error": "Post does not exist"}), 404
        
    redis_client.setex(cache_key, 3600, json.dumps(post.to_json()))
    return jsonify({"source":"Api", "data": post.to_json()}), 200


        

@posts_bp.route('/all', methods=['GET'])
def all_posts():
    cache_key = "all_posts"
    cached_posts = redis_client.get(cache_key)
 # check cache
    if cached_posts:
        return jsonify({"source": "cache", "data":json.loads(cached_posts)})
    else:
# query database
        posts = Post.query.all()
    
        json_posts = [post.to_json() for post in posts]
        if not json_posts:
            return jsonify({"Message": "no posts to show"}), 404
        
        redis_client.setex(cache_key, 3600, json.dumps(json_posts))
        return jsonify({"source":"Api", "data": json_posts}), 200



# Filter blog posts by a search term
@posts_bp.route('/search', methods=['GET'])
def searched_post():

        # Get the search term from the request
    searched_term = request.args.get("term")
    
    if not searched_term:
        return jsonify({"error": "No search term provided"}), 400  # Return a 400 if no search term is given
    
    # unique cache key based on the search term
    cache_key = f'search_term_{searched_term}'

    cached_term = redis_client.get(cache_key)

    if cached_term:
        return jsonify({"source" : "cache", "data" : json.loads(cached_term)})

    posts = Post.query.filter(Post.title.ilike(f'%{searched_term}%')).all()

    if posts:
        json_posts = [post.to_json() for post in posts]
        redis_client.setex(cache_key, 3600, json.dumps(json_posts))
        return jsonify({"data": json_posts}),201
    return  jsonify({"error": "No posts found matching the search term"}), 404
































# #########################################################################
# # Create a new blog post
# # @posts_bp.route('/create', methods=['GET', 'POST'])
# def create_post():
#     ("Raw request body:", request.data)
#     if request.method == "POST":
#         data = request.get_json()

#         title = data.get("title")
#         content = data.get("content")
#         category = data.get( "category")
#         tag_names = data.get("tags")
#     print(f"title: {title}, content: {content}, category: {category}")

#     if not title or not content or not category:
#         return jsonify({"error": "Missing required fields"}), 400
    
#     new_post = Post(title=title, content=content, category=category)

#     tags = []
#     for tag_name in tag_names:
#         existing_tag = Tag.query.filter_by(name=tag_name).first()
#         if not existing_tag:
#             existing_tag = Tag(name=tag_name)
#             db.session.add(existing_tag)
#         tags.append(existing_tag)
    
#     new_post.tags = tags

#     db.session.add(new_post)
#     db.session.commit()

#     return jsonify({"message": "Message created successfully", "data": new_post.to_json()}), 201
# #########################################################################





# # Update an existing blog post
# @posts_bp.route('/update/<int:id>', methods=['PUT'])
# def update_post(id):
#     ("Raw request body:", request.data)
#     data = request.get_json()

#     title = data.get("title")
#     content = data.get("content")
#     category = data.get( "category")
#     tag_names = data.get("tags")

#     if not title or not content or not category:
#         return jsonify({"error": "Missing required fields"}), 400
    
#     updated_Post = Post(title=title, content=content, category=category)

#     db.session.add(updated_Post)
#     db.session.commit()

#     return jsonify({"message": "Missing required fields", "data": updated_Post.to_json()}), 201
# #########################################################################




# # Delete an existing blog post
# @posts_bp.route('/delete/<int:id>', methods=['DELETE', 'POST'])
# # @csrf.exempt
# def delete_post(id):
#     print(f"Delete endpoint reached for post ID: {id}")
#     post = Post.query.get(id)

#     if not post:
#         return jsonify({"error": "message does not exist"}), 400

#     db.session.delete(post)
#     db.session.commit()
#     return jsonify({"message": "Message deleted successfully"}), 201
# #########################################################################



# # Get a single blog post
# @posts_bp.route('/uniquepost/<int:id>', methods=['GET'])
# def get_single_post(id):
#     post = Post.query.get(id)

#     if post:
#         return jsonify({"post": post.to_json()})
#     return jsonify({"error": "post does not exist"}), 404
# #########################################################################




# # Get all blog posts
# @posts_bp.route('/posts', methods=['GET'])
# def get_all_posts():
#     posts = Post.query.all()
#     json_posts = list(map(lambda x: x.to_json(), posts))
#     if json_posts:
#         return jsonify({"posts": json_posts})
#     return jsonify({"error":" there are no posts to display"}), 404
# #########################################################################



# # Filter blog posts by a search term
# @posts_bp.route('/search', methods=['GET'])
# def get_post_by_name():
#         term = request.args.get('term')
#         if not term:
#             return jsonify({"error": "No search term provided"}), 400
#         posts = Post.query.filter(Post.title.contains(term)).all()
#         if posts:
#             return jsonify({"data": [post.to_json() for post in posts]}), 201
#         return jsonify({"error": "page does not exist"}),404


