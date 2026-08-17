from repositories.task_repository import TaskRepository


class TaskService:

    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def create_task(self, title: str):
        return self.repo.create(title)
        
    def get_tasks(self):
        return self.repo.get_all()
    
    def toggle_task(self, task_id: int):
        return self.repo.toggle(task_id)

    def delete_task(self, task_id: int):
        return self.repo.delete(task_id)

    