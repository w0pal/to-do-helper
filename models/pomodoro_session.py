import time
import webbrowser
import os
from datetime import datetime

class PomodoroSession:
    """Handles Pomodoro technique sessions with music integration"""
    
    LOFI_PLAYLISTS = [
        "https://www.youtube.com/watch?v=jfKfPfyJRdk",  # lofi hip hop radio
        "https://www.youtube.com/watch?v=HuFYqnbVbzY",  # jazz lofi
    ]
    
    def __init__(self, task, task_manager):
        self.task = task
        self.task_manager = task_manager
        self.work_duration = 25 * 60  # 25 minutes in seconds
        self.short_break = 5 * 60     # 5 minutes in seconds
        self.long_break = 15 * 60     # 15 minutes in seconds
        self.session_count = 0        # Track number of completed sessions
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def play_lofi_music(self):
        """Open browser and play lofi music from YouTube"""
        try:
            import random
            playlist_url = random.choice(self.LOFI_PLAYLISTS)
            print("🎵 Opening lofi music in browser...")
            webbrowser.open(playlist_url)
            time.sleep(2)  # Give time for browser to load
            return True
        except Exception as e:
            print(f"⚠️ Cannot open music: {e}")
            return False
    
    def countdown_timer(self, duration, session_type="work"):
        """Display countdown timer"""
        total_seconds = duration
        
        while duration > 0:
            mins, secs = divmod(duration, 60)
            timer_display = f"{mins:02d}:{secs:02d}"
            
            # Create progress bar
            progress = ((total_seconds - duration) / total_seconds) * 100
            bar_length = 30
            filled_length = int(bar_length * progress // 100)
            bar = "█" * filled_length + "░" * (bar_length - filled_length)
            
            # Display
            self.clear_screen()
            print("🍅 POMODORO SESSION")
            print("=" * 40)
            print(f"📋 Task: {self.task.title}")
            print(f"⏱️  Session: {session_type.upper()}")
            print(f"🕒 Time: {timer_display}")
            print(f"📊 Progress: [{bar}] {progress:.1f}%")
            print("\n💡 Tips: Focus on one task, turn off notifications")
            print("⌨️  Press Ctrl+C to stop")
            
            time.sleep(1)
            duration -= 1
        
        # Session completed
        self.clear_screen()
        if session_type == "work":
            print("🎉 WORK SESSION COMPLETED!")
            print(f"✅ {self.work_duration // 60} productive minutes for: {self.task.title}")
        else:
            print("⏰ BREAK TIME FINISHED!")
            print("💪 Ready for the next session!")
    
    def get_focus_rating(self):
        """Get user's focus rating for the session"""
        while True:
            try:
                print("\n🎯 How focused were you during this session?")
                print("1 = Very unfocused")
                print("2 = Somewhat unfocused") 
                print("3 = Moderately focused")
                print("4 = Focused")
                print("5 = Very focused")
                
                rating = int(input("Focus rating (1-5): "))
                if 1 <= rating <= 5:
                    return rating
                else:
                    print("❌ Rating must be between 1-5!")
            except ValueError:
                print("❌ Invalid input!")
    
    def start_session(self):
        """Start a complete Pomodoro session"""
        try:
            self.clear_screen()
            print("🍅 STARTING POMODORO SESSION")
            print("=" * 30)
            print(f"📋 Task: {self.task.title}")
            print(f"⏱️  Duration: {self.work_duration // 60} minutes work")
            print("\n🎵 Will open lofi music in browser...")
            
            # Ask user if they want music
            play_music = input("\nPlay lofi music? (y/n): ").lower().strip()
            if play_music == 'y':
                self.play_lofi_music()
            
            input("\n🚀 Press Enter to start session...")
            
            # Work session
            start_time = datetime.now()
            self.countdown_timer(self.work_duration, "work")
            
            # Get focus rating
            focus_rating = self.get_focus_rating()
            
            # Record the session
            if hasattr(self.task, 'add_focus_session'):
                self.task.add_focus_session(self.work_duration, focus_rating)
            else:
                self.task.add_pomodoro_session()
            
            self.task_manager.add_pomodoro_session(self.task.task_id)
            
            # Increment session count
            self.session_count += 1
            
            # Show completion message
            print("\n🎊 POMODORO SESSION SUCCESSFUL!")
            print(f"⭐ +{2} bonus points for completing session!")
            print(f"🎯 Focus rating: {focus_rating}/5")
            print(f"📈 Sessions completed: {self.session_count}")
            
            # Determine break type based on session count
            break_choice = input("\nTake a break? (y/n): ").lower().strip()
            if break_choice == 'y':
                if self.session_count % 4 == 0:  # Every 4th session gets long break
                    print("\n🏖️ LONG BREAK TIME!")
                    print("💡 Take a longer rest - you've earned it!")
                    print(f"⏰ Duration: {self.long_break} seconds")
                    input("Press Enter to start long break...")
                    self.countdown_timer(self.long_break, "long break")
                else:
                    print("\n☕ SHORT BREAK TIME")
                    print("💡 Stand up, stretch, drink water!")
                    input("Press Enter to start break...")
                    self.countdown_timer(self.short_break, "short break")
            
            # Ask if task is completed
            task_done = input(f"\nIs task '{self.task.title}' completed? (y/n): ").lower().strip()
            if task_done == 'y':
                self.task_manager.complete_task(self.task.task_id)
                points_earned = self.task.get_points()
                print(f"🎉 TASK COMPLETED! +{points_earned} points!")
            else:
                continue_session = input("Continue another Pomodoro session? (y/n): ").lower().strip()
                if continue_session == 'y':
                    self.start_session()  # Recursive call for another session
            
        except KeyboardInterrupt:
            print("\n\n⏹️ Pomodoro session stopped.")
            save_partial = input("Save progress from this session? (y/n): ").lower().strip()
            if save_partial == 'y':
                # Record partial session
                if hasattr(self.task, 'add_focus_session'):
                    self.task.add_focus_session(self.work_duration // 2, 3)  # Average rating
                else:
                    self.task.add_pomodoro_session()
                self.task_manager.save_data()
                print("💾 Progress saved!")
        except Exception as e:
            print(f"❌ Error during Pomodoro session: {e}")
