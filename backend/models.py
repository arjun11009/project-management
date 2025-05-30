from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    tasks = db.relationship('Task', backref='project', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'task_count': len(self.tasks)
        }

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='To Do')  # To Do, In Progress, Done
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    assigned_to = db.Column(db.String(100))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'status': self.status,
            'project_id': self.project_id,
            'assigned_to': self.assigned_to
        }