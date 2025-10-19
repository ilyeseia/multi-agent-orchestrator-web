import subprocess

def execute_workflow(project_id):
    """
    مثال لتشغيل Workflow خارجي للمشروع
    """
    try:
        # هنا يمكن وضع الأمر الفعلي لتشغيل المشروع
        result = subprocess.run(['echo', f'Running project {project_id}'], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)
