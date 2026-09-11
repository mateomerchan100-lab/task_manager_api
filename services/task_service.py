from repositories.task_repository import TaskRepository


class TaskService:

    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def create_task(self, title: str, owner: str):
        return self.repo.create(title, owner)
        
    def get_tasks(self, owner: str):
        return self.repo.get_all(owner)
    
    def toggle_task(self, task_id: int, owner: str):
        return self.repo.toggle(task_id, owner)

    def delete_task(self, task_id: int, owner: str):
        return self.repo.delete(task_id, owner)

    