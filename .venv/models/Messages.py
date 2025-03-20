from extensions import db

post_tags = db.Table(
    "post_tags",
    db.Column("post_id", db.Integer, db.ForeignKey("post.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # Many-to-Many Relationship
    tags = db.relationship("Tag", secondary=post_tags, backref=db.backref("posts", lazy="dynamic"))

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'tags': [tag.name for tag in self.tags],  # Include tags in the response
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat()
             }


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
             }



#     {
#   "id": 1,
#   "title": "My First Blog Post",
#   "content": "This is the content of my first blog post.",
#   "category": "Technology",
#   "tags": ["Tech", "Programming"],
#   "createdAt": "2021-09-01T12:00:00Z",
#   "updatedAt": "2021-09-01T12:00:00Z"
# # }
