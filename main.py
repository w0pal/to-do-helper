#!/usr/bin/env python3
"""
Pomodoro To-Do Helper CLI Application
A productivity tool that combines task management with Pomodoro technique
"""

import os
import sys
from models.task_manager import TaskManager
from models.pomodoro_session import PomodoroSession

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    print("\n" + "="*50)
    print("🍅 POMODORO TO-DO HELPER 🍅")
    print("="*50)
    print("1. View all tasks")
    print("2. Add new task")
    print("3. Start Pomodoro session")
    print("4. Mark task as complete")
    print("5. View statistics & score")
    print("6. Delete task")
    print("7. Exit")
    print("="*50)

def main():
    task_manager = TaskManager()
    
    while True:
        display_menu()
        choice = input("Choose menu (1-7): ").strip()
        
        if choice == '1':
            clear_screen()
            task_manager.display_all_tasks()
            input("\nPress Enter to return to menu...")
            
        elif choice == '2':
            clear_screen()
            print("🆕 ADD NEW TASK")
            print("-" * 30)
            title = input("Task title: ").strip()
            if not title:
                print("❌ Task title cannot be empty!")
                continue
                
            description = input("Description (optional): ").strip()
            
            print("\nDifficulty level:")
            print("1. Easy (1 point)")
            print("2. Medium (3 points)")
            print("3. Hard (5 points)")
            difficulty = input("Choose level (1-3): ").strip()
            
            difficulty_map = {'1': 'easy', '2': 'medium', '3': 'hard'}
            difficulty = difficulty_map.get(difficulty, 'medium')
            
            task_manager.add_task(title, description, difficulty)
            print("✅ Task successfully added!")
            
        elif choice == '3':
            clear_screen()
            tasks = task_manager.get_pending_tasks()
            if not tasks:
                print("❌ No tasks available!")
                input("Press Enter to return...")
                continue
                
            print("📋 SELECT TASK FOR POMODORO")
            print("-" * 35)
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task.title} ({task.difficulty})")
                
            try:
                task_idx = int(input("\nSelect task number: ")) - 1
                if 0 <= task_idx < len(tasks):
                    selected_task = tasks[task_idx]
                    pomodoro = PomodoroSession(selected_task, task_manager)
                    pomodoro.start_session()
                else:
                    print("❌ Invalid task number!")
            except ValueError:
                print("❌ Invalid input!")
                
        elif choice == '4':
            clear_screen()
            tasks = task_manager.get_pending_tasks()
            if not tasks:
                print("❌ No tasks to complete!")
                input("Press Enter to return...")
                continue
                
            print("✅ MARK TASK AS COMPLETE")
            print("-" * 25)
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task.title}")
                
            try:
                task_idx = int(input("\nSelect task number: ")) - 1
                if 0 <= task_idx < len(tasks):
                    task_manager.complete_task(tasks[task_idx].task_id)
                    print("🎉 Task successfully completed!")
                else:
                    print("❌ Invalid task number!")
            except ValueError:
                print("❌ Invalid input!")
                
        elif choice == '5':
            clear_screen()
            task_manager.display_statistics()
            input("\nPress Enter to return to menu...")
            
        elif choice == '6':
            clear_screen()
            tasks = task_manager.get_all_tasks()
            if not tasks:
                print("❌ No tasks to delete!")
                input("Press Enter to return...")
                continue
                
            print("🗑️ DELETE TASK")
            print("-" * 15)
            for i, task in enumerate(tasks, 1):
                status = "✅" if task.completed else "⏳"
                print(f"{i}. {status} {task.title}")
                
            try:
                task_idx = int(input("\nSelect task number to delete: ")) - 1
                if 0 <= task_idx < len(tasks):
                    confirm = input(f"Are you sure you want to delete '{tasks[task_idx].title}'? (y/n): ")
                    if confirm.lower() == 'y':
                        task_manager.delete_task(tasks[task_idx].task_id)
                        print("🗑️ Task successfully deleted!")
                else:
                    print("❌ Invalid task number!")
            except ValueError:
                print("❌ Invalid input!")
                
        elif choice == '7':
            print("👋 Thank you for using Pomodoro To-Do Helper!")
            sys.exit(0)
            
        else:
            print("❌ Invalid choice! Please select 1-7.")
            
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
