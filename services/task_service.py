from repositories.task_repository import TaskRepository


class TaskService:

    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def create_task(self, title: str, owner: str):
        return self.repo.create(title, owner)
        
    def get_tasks(self, owner: str):
        return self.repo.get_all(owner)
    
    def update_done(self, task_id: int, done: bool, owner: str):
        return self.repo.update_done(task_id, done, owner)

    def delete_task(self, task_id: int, owner: str):
        return self.repo.delete(task_id, owner)

    