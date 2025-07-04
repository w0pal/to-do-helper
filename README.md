# 🍅 Pomodoro To-Do Helper

## Application Inspiration

This application is inspired by my personal experience as someone with ADHD tendencies who often struggles to focus on tasks. I frequently feel overwhelmed when looking at long task lists and don't know where to start.

The Pomodoro Technique has helped me break down large tasks into smaller, more manageable sessions. Combined with lofi music and a point system, it makes the learning and working process more enjoyable and motivating. This application was created with the hope of helping people with similar conditions stay productive and motivated.

## Main Features

- ✅ **Task Management**: Add, delete, and manage tasks with difficulty levels
- 🍅 **Pomodoro Timer**: 25-minute timer with visual countdown and progress bar
- 🎵 **Music Integration**: Automatically opens YouTube for lofi music when session starts
- 🏆 **Points & Level System**: Gamification with points and levels for motivation
- 📊 **Detailed Statistics**: Focus tracking, session count, and achievements
- 💾 **JSON Storage**: All data automatically saved in JSON format
- 🎯 **ADHD-Friendly**: Special design to help people with attention deficit

## OOP Structure

### Classes & Inheritance
- `BaseTask` (Abstract Class) - Base class for all task types
- `Task` (extends BaseTask) - Regular task implementation
- `PomodoroTask` (extends Task) - Task with enhanced Pomodoro features
- `TaskManager` - Manages all task operations and data persistence
- `PomodoroSession` - Handler for Pomodoro sessions with music integration

### Polymorphism
- `get_points()` - Different implementations for Task and PomodoroTask
- `get_display_info()` - Custom display for each task type
- `to_dict()` / `from_dict()` - Different serialization per class

## Installation & Running

### Requirements
- Python 3.7+
- Internet connection (for YouTube music)
- Default browser installed

### Installation Steps

1. Clone or download this project
```bash
git clone <repository-url>
cd to-do-helper
```

2. Run the application
```bash
python main.py
```

### How to Use

1. **Add Task**: Choose menu 2, enter title and select difficulty level
2. **Start Pomodoro**: Choose menu 3, select task, and start 25-minute session
3. **Automatic Music**: App will open browser and play lofi music
4. **Complete Task**: Mark task as complete to earn points
5. **View Progress**: Check statistics and level in menu 5

### Point System

- **Easy Task**: 1 point + 2 points per Pomodoro session
- **Medium Task**: 3 points + 2 points per Pomodoro session
- **Hard Task**: 5 points + 2 points per Pomodoro session
- **PomodoroTask Bonus**: +5 points if reaching target sessions

### Level System

1. **Beginner 🌱**: 0-9 points
2. **Developing 🌿**: 10-24 points
3. **Productive 🌳**: 25-49 points
4. **Master 🏆**: 50-99 points
5. **Grandmaster 👑**: 100+ points

## File Structure

```
to-do-helper/
├── main.py                 # Application entry point
├── models/
│   ├── __init__.py
│   ├── task.py             # Task classes with inheritance
│   ├── task_manager.py     # Task management & persistence
│   └── pomodoro_session.py # Pomodoro timer & music integration
├── data/
│   ├── .gitkeep
│   └── tasks.json          # Data storage (auto-generated)
└── README.md
```

## Demo Video

[Demo video link will be added here]

## Technical Features

- **Abstract Base Class**: `BaseTask` with abstract methods
- **Inheritance**: `Task` -> `PomodoroTask` hierarchy
- **Polymorphism**: Method overriding for different behaviors
- **JSON Persistence**: Auto-save with custom serialization
- **Error Handling**: Comprehensive try-catch blocks
- **Cross-platform**: Works on Windows, macOS, and Linux

## Usage Tips

1. **For ADHD**: Start with easy tasks to build momentum
2. **Music**: Use headphones for maximum focus
3. **Break Time**: Don't skip breaks, important for productivity
4. **Gamification**: Set daily targets to reach new levels
5. **Consistency**: Use daily to build habit

---

*Made with ❤️ for better productivity*
