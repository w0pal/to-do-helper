import json
import os
from datetime import datetime
from typing import List, Dict, Any
from .task import Task, PomodoroTask

class TaskManager:
    """Manages all tasks and handles data persistence"""
    
    def __init__(self, data_file="data/tasks.json"):
        self.data_file = data_file
        self.tasks: List[Task] = []
        self.user_stats = {
            'total_points': 0,
            'completed_tasks': 0,
            'total_pomodoros': 0,
            'streak_days': 0,
            'last_activity': None
        }
        self._ensure_data_directory()
        self.load_data()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
    
    def add_task(self, title: str, description: str = "", difficulty: str = "medium", is_pomodoro: bool = False):
        """Add a new task"""
        if is_pomodoro:
            task = PomodoroTask(title, description, difficulty)
        else:
            task = Task(title, description, difficulty)
        
        self.tasks.append(task)
        self.save_data()
        return task
    
    def get_task_by_id(self, task_id: str) -> Task:
        """Get task by ID"""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None
    
    def complete_task(self, task_id: str) -> bool:
        """Mark task as completed and update stats"""
        task = self.get_task_by_id(task_id)
        if task and not task.completed:
            task.complete()
            self.user_stats['completed_tasks'] += 1
            self.user_stats['total_points'] += task.get_points()
            self.user_stats['last_activity'] = datetime.now().isoformat()
            self.save_data()
            return True
        return False
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task"""
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_data()
            return True
        return False
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        return self.tasks
    
    def get_pending_tasks(self) -> List[Task]:
        """Get all pending (incomplete) tasks"""
        return [task for task in self.tasks if not task.completed]
    
    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks"""
        return [task for task in self.tasks if task.completed]
    
    def add_pomodoro_session(self, task_id: str):
        """Add a pomodoro session to a task"""
        task = self.get_task_by_id(task_id)
        if task:
            task.add_pomodoro_session()
            self.user_stats['total_pomodoros'] += 1
            self.user_stats['last_activity'] = datetime.now().isoformat()
            self.save_data()
    
    def get_user_level(self) -> Dict[str, Any]:
        """Calculate user level based on points"""
        points = self.user_stats['total_points']
        
        if points < 10:
            level = 1
            level_name = "Beginner 🌱"
            next_level_points = 10
        elif points < 25:
            level = 2
            level_name = "Developing 🌿"
            next_level_points = 25
        elif points < 50:
            level = 3
            level_name = "Productive 🌳"
            next_level_points = 50
        elif points < 100:
            level = 4
            level_name = "Master 🏆"
            next_level_points = 100
        else:
            level = 5
            level_name = "Grandmaster 👑"
            next_level_points = points  # Max level reached
        
        return {
            'level': level,
            'name': level_name,
            'current_points': points,
            'next_level_points': next_level_points,
            'progress': min(100, (points / next_level_points) * 100) if next_level_points > points else 100
        }
    
    def display_all_tasks(self):
        """Display all tasks in a formatted way"""
        if not self.tasks:
            print("📭 No tasks created yet!")
            return
        
        pending = self.get_pending_tasks()
        completed = self.get_completed_tasks()
        
        print(f"📋 TASK LIST ({len(self.tasks)} total)")
        print("=" * 40)
        
        if pending:
            print("\n⏳ PENDING TASKS:")
            print("-" * 25)
            for task in pending:
                print(f"  {task.get_display_info()}")
                if task.description:
                    print(f"    📝 {task.description}")
                print()
        
        if completed:
            print("\n✅ COMPLETED TASKS:")
            print("-" * 18)
            for task in completed:
                print(f"  {task.get_display_info()}")
                if task.completed_at:
                    completed_date = datetime.fromisoformat(task.completed_at)
                    print(f"    🕒 Completed: {completed_date.strftime('%d/%m/%Y %H:%M')}")
                print()
    
    def display_statistics(self):
        """Display user statistics and achievements"""
        level_info = self.get_user_level()
        
        print("📊 STATISTICS & ACHIEVEMENTS")
        print("=" * 30)
        print(f"🏆 Level: {level_info['name']}")
        print(f"⭐ Total Points: {self.user_stats['total_points']}")
        
        if level_info['level'] < 5:
            remaining = level_info['next_level_points'] - level_info['current_points']
            print(f"📈 Progress to Level {level_info['level'] + 1}: {level_info['progress']:.1f}%")
            print(f"🎯 Need {remaining} more points to level up!")
        else:
            print("🎊 You have reached the maximum level!")
        
        print(f"\n📋 Completed Tasks: {self.user_stats['completed_tasks']}")
        print(f"🍅 Total Pomodoros: {self.user_stats['total_pomodoros']}")
        
        if self.user_stats['last_activity']:
            last_activity = datetime.fromisoformat(self.user_stats['last_activity'])
            print(f"🕒 Last Activity: {last_activity.strftime('%d/%m/%Y %H:%M')}")
        
        # Task breakdown by difficulty
        pending = self.get_pending_tasks()
        if pending:
            print(f"\n📈 ACTIVE TASK BREAKDOWN:")
            difficulties = {'easy': 0, 'medium': 0, 'hard': 0}
            for task in pending:
                difficulties[task.difficulty] += 1
            
            print(f"  🟢 Easy: {difficulties['easy']}")
            print(f"  🟡 Medium: {difficulties['medium']}")
            print(f"  🔴 Hard: {difficulties['hard']}")
    
    def save_data(self):
        """Save tasks and stats to JSON file"""
        data = {
            'tasks': [task.to_dict() for task in self.tasks],
            'user_stats': self.user_stats,
            'last_saved': datetime.now().isoformat()
        }
        
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error saving data: {e}")
    
    def load_data(self):
        """Load tasks and stats from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Load user stats
                if 'user_stats' in data:
                    self.user_stats.update(data['user_stats'])
                
                # Load tasks
                self.tasks = []
                for task_data in data.get('tasks', []):
                    if task_data.get('type') == 'PomodoroTask':
                        task = PomodoroTask.from_dict(task_data)
                    else:
                        task = Task.from_dict(task_data)
                    self.tasks.append(task)
                    
        except Exception as e:
            print(f"⚠️ Error loading data: {e}")
            print("🔄 Starting with fresh data...")
