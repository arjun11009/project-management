from flask import Blueprint, request, jsonify
from models import db, Project, Task
from sqlalchemy.exc import IntegrityError

bp = Blueprint('routes', __name__)

@bp.route('/projects', methods=['GET', 'POST'])
def handle_projects():
    if request.method == 'POST':
        try:
            data = request.json
            if not data.get('name'):
                return jsonify({'error': 'Project name is required'}), 400
                
            project = Project(
                name=data['name'],
                description=data.get('description', '')
            )
            db.session.add(project)
            db.session.commit()
            return jsonify({'message': 'Project created', 'project': project.to_dict()}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Project name already exists'}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        projects = Project.query.all()
        return jsonify([p.to_dict() for p in projects])

@bp.route('/tasks', methods=['GET', 'POST'])
def handle_tasks():
    if request.method == 'POST':
        try:
            data = request.json
            if not data.get('title') or not data.get('project_id'):
                return jsonify({'error': 'Title and project_id are required'}), 400

            task = Task(
                title=data['title'],
                status=data.get('status', 'To Do'),
                project_id=data['project_id'],
                assigned_to=data.get('assigned_to')
            )
            db.session.add(task)
            db.session.commit()
            return jsonify({'message': 'Task created', 'task': task.to_dict()}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    else:
        tasks = Task.query.all()
        return jsonify([t.to_dict() for t in tasks])

@bp.route('/tasks/<int:task_id>', methods=['PATCH'])
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    try:
        data = request.json
        if 'status' in data:
            task.status = data['status']
            db.session.commit()
            return jsonify({'message': 'Task status updated', 'task': task.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500