import time
from models import db, Execution

def execute_workflow(project_id):
    execution = Execution(project_id=project_id, status="running")
    db.session.add(execution)
    db.session.commit()
    # Simulate some work
    time.sleep(5)
    execution.status = "completed"
    db.session.commit()
    return execution.id