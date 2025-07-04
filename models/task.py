from abc import ABC, abstractmethod
from datetime import datetime
import uuid

class BaseTask(ABC):
    """Abstract base class for all task types"""
    
    def __init__(self, title, description=""):
        self.task_id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.created_at = datetime.now().isoformat()
        self.completed = False
        self.completed_at = None
    
    @abstractmethod
    def get_points(self):
        """Calculate points for completing this task"""
        pass
    
    @abstractmethod
    def get_display_info(self):
        """Get formatted display information"""
        pass
    
    def complete(self):
        """Mark task as completed"""
        self.completed = True
        self.completed_at = datetime.now().isoformat()
    
    def to_dict(self):
        """Convert task to dictionary for JSON storage"""
        return {
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at,
            'completed': self.completed,
            'completed_at': self.completed_at,
            'type': self.__class__.__name__
        }

class Task(BaseTask):
    """Regular task implementation"""
    
    def __init__(self, title, description="", difficulty="medium"):
        super().__init__(title, description)
        self.difficulty = difficulty
        self.pomodoro_sessions = 0
    
    def get_points(self):
        """Calculate points based on difficulty"""
        point_map = {
            'easy': 1,
            'medium': 3,
            'hard': 5
        }
        base_points = point_map.get(self.difficulty, 3)
        # Bonus points for pomodoro sessions
        bonus_points = self.pomodoro_sessions * 2
        return base_points + bonus_points
    
    def get_display_info(self):
        """Get formatted display information"""
        status = "✅" if self.completed else "⏳"
        points = self.get_points()
        return f"{status} {self.title} ({self.difficulty.upper()}) - {points} poin"
    
    def add_pomodoro_session(self):
        """Add a completed pomodoro session"""
        self.pomodoro_sessions += 1
    
    def to_dict(self):
        """Convert task to dictionary for JSON storage"""
        data = super().to_dict()
        data.update({
            'difficulty': self.difficulty,
            'pomodoro_sessions': self.pomodoro_sessions
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create task instance from dictionary"""
        task = cls(data['title'], data['description'], data['difficulty'])
        task.task_id = data['task_id']
        task.created_at = data['created_at']
        task.completed = data['completed']
        task.completed_at = data['completed_at']
        task.pomodoro_sessions = data.get('pomodoro_sessions', 0)
        return task

class PomodoroTask(Task):
    """Task specifically designed for Pomodoro technique - demonstrates inheritance"""
    
    def __init__(self, title, description="", difficulty="medium", estimated_pomodoros=1):
        super().__init__(title, description, difficulty)
        self.estimated_pomodoros = estimated_pomodoros
        self.focus_sessions = []
    
    def get_points(self):
        """Enhanced point calculation for Pomodoro tasks"""
        base_points = super().get_points()
        # Bonus for completing estimated pomodoros
        if self.pomodoro_sessions >= self.estimated_pomodoros:
            base_points += 5
        return base_points
    
    def get_display_info(self):
        """Enhanced display info for Pomodoro tasks"""
        base_info = super().get_display_info()
        progress = f"({self.pomodoro_sessions}/{self.estimated_pomodoros} 🍅)"
        return f"{base_info} {progress}"
    
    def add_focus_session(self, duration, focus_rating):
        """Add a focus session record"""
        session = {
            'timestamp': datetime.now().isoformat(),
            'duration': duration,
            'focus_rating': focus_rating
        }
        self.focus_sessions.append(session)
        self.add_pomodoro_session()
    
    def get_average_focus(self):
        """Calculate average focus rating"""
        if not self.focus_sessions:
            return 0
        return sum(session['focus_rating'] for session in self.focus_sessions) / len(self.focus_sessions)
    
    def to_dict(self):
        """Convert task to dictionary for JSON storage"""
        data = super().to_dict()
        data.update({
            'estimated_pomodoros': self.estimated_pomodoros,
            'focus_sessions': self.focus_sessions
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create PomodoroTask instance from dictionary"""
        task = cls(
            data['title'], 
            data['description'], 
            data['difficulty'],
            data.get('estimated_pomodoros', 1)
        )
        task.task_id = data['task_id']
        task.created_at = data['created_at']
        task.completed = data['completed']
        task.completed_at = data['completed_at']
        task.pomodoro_sessions = data.get('pomodoro_sessions', 0)
        task.focus_sessions = data.get('focus_sessions', [])
        return task
