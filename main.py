# main.py
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.screen import MDScreen
from random import shuffle

# --- Quiz Data (Same as your Pygame data) ---
QUIZ_DATA = [
    {
        "question": "The extremely long question asks: What famous historical event occurred in 1912, involving a massive ship that struck an iceberg in the North Atlantic Ocean?",
        "options": ["The launch of the USS Enterprise", "The sinking of the RMS Titanic after hitting an iceberg", "The opening of the Panama Canal", "The start of the First World War in Europe"],
        "correct_answer": "The sinking of the RMS Titanic after hitting an iceberg"
    },
    {
        "question": "Which gas makes up most of Earth's atmosphere?",
        "options": ["Oxygen", "Carbon Dioxide", "Argon", "Nitrogen"],
        "correct_answer": "Nitrogen"
    }, 
    {
        "question": "What is the smallest planet in our solar system?",
        "options": ["Earth", "Mars", "Mercury", "Venus"],
        "correct_answer": "Mercury"
    }, 
    {
        "question": "The extremely long question asks: What famous historical event occurred in 1912, involving a massive ship that struck an iceberg in the North Atlantic Ocean?",
        "options": ["The launch of the USS Enterprise", "The sinking of the RMS Titanic after hitting an iceberg", "The opening of the Panama Canal", "The start of the First World War in Europe"],
        "correct_answer": "The sinking of the RMS Titanic after hitting an iceberg"
    },
    {
        "question": "  who are you ",
        "options": [" rush ", " god ", " xy ", " op "],
        "correct_answer": " god "
    }, 
    {
        "question": "who you are",
        "options": ["god", "devil", "evil", "gaint"],
        "correct_answer": "god"
    },
    {
        "question": "how you are",
        "options": ["good", "happy", "bad", "sad"],
        "correct_answer": "happy"
    },
    {
        "question": "where you are",
        "options": ["", "earth", "sun ", "mars"],
        "correct_answer": "earth"
    }, 
    {
        "question": "A for",
        "options": ["apple", "banana", "orange", "lemon"],
        "correct_answer": "apple"
    },
    {
        "question": "B for ______",
        "options": ["grapes", "cucumber", "ginger", "banana"],
        "correct_answer": "banana"
    }, 
    {
        "question": "C for ____",
        "options": ["door", "bell", "cat", "dog"],
        "correct_answer": "cat"
    },
    {
        "question": "d for ___",
        "options": ["door", "cat", "chess", "bell"],
        "correct_answer": "door"
    },
    {
        "question": "which is country",
        "options": ["gold", "silver", "india", "door"],
        "correct_answer": "india"
    },
    {
        "question": "z for _____",
        "options": ["yak", "bell", "goa", "zebra"],
        "correct_answer": "zebra"
    },
    {
        "question": "k for _____",
        "options": ["king", "goal", "queen", "window"],
        "correct_answer": "king"
    }
]

class QuizApp(MDApp):
    # Kivy properties to update UI labels/widgets automatically
    current_question = StringProperty("")
    options_list = ListProperty(["", "", "", ""])
    feedback_message = StringProperty("")
    feedback_color = ListProperty([0, 0, 0, 1]) # Black
    
    current_q_index = 0
    correct_answer = ""
    button_enabled = True

    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.theme_style = "Light"
        self.load_kv_file()
        return Builder.load_string(self.kv_string)

    def load_kv_file(self):
        # The KV file content is included here to simplify the file structure
        self.kv_string = """
<OptionButton@MDRectangleFlatButton>:
    text_color: 0, 0, 0, 1
    line_color: 0, 0, 0, 1
    font_size: '14sp'
    halign: 'center'
    valign: 'center'
    on_release: app.check_answer(self.text, self)
    md_bg_color: 1, 1, 1, 1 # White background

MDScreen:
    md_bg_color: 0.9, 0.9, 0.9, 1 # Light Grey background
    
    # ------------------ Quiz Content Screen ------------------
    MDBoxLayout:
        id: quiz_screen
        orientation: 'vertical'
        padding: [10, 20, 10, 20]
        spacing: 20
        size_hint_y: 1

        # 1. Question Box (Requirement 1 & Layout)
        MDCard:
            size_hint_y: 0.7 # Occupy a large portion of the top
            radius: [10]
            md_bg_color: 1, 1, 1, 1 # White
            line_color: 0, 1, 1, 1 # Cyan Border
            line_width: 3
            elevation: 8
            
            MDLabel:
                text: app.current_question
                font_style: 'H6'
                halign: 'center'
                valign: 'center'
                markup: True
                padding: [20, 20]

        # 2. Options Grid (Requirement 2 & Layout)
        GridLayout:
            id: options_grid
            cols: 2
            spacing: 10
            size_hint_y: 0.5

            OptionButton:
                id: opt_0
                text: app.options_list[0]
            OptionButton:
                id: opt_1
                text: app.options_list[1]
            OptionButton:
                id: opt_2
                text: app.options_list[2]
            OptionButton:
                id: opt_3
                text: app.options_list[3]
        
        # 3. Feedback Label
        MDLabel:
            id: feedback
            text: app.feedback_message
            halign: 'center'
            font_style: 'H5'
            theme_text_color: "Custom"
            text_color: app.feedback_color
            size_hint_y: None
            height: self.texture_size[1]
            
    # ------------------ Quiz Complete Screen ------------------
    MDBoxLayout:
        id: complete_screen
        orientation: 'vertical'
        padding: [20]
        spacing: 30
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint: 1, 1
        md_bg_color: 1, 1, 1, 1
        opacity: 0 # Initially hidden
        
        MDLabel:
            text: "🏆 QUIZ COMPLETE! 🏆"
            halign: 'center'
            font_style: 'H4'
            theme_text_color: "Custom"
            text_color: 0, 0.8, 0, 1 # Bright Green
            size_hint_y: None
            height: self.texture_size[1]
            
        MDLabel:
            text: "Thank you for playing!"
            halign: 'center'
            font_style: 'H6'
            theme_text_color: "Primary"
            size_hint_y: None
            height: self.texture_size[1]
        
"""

    def on_start(self):
        # Hide the complete screen at the start
        self.root.ids.complete_screen.opacity = 0 
        self.load_question()

    def load_question(self):
        """Loads the question data into the UI properties."""
        if self.current_q_index >= len(QUIZ_DATA):
            self.show_completion_screen()
            return
            
        quiz = QUIZ_DATA[self.current_q_index]
        self.current_question = quiz['question']
        self.options_list = quiz['options']
        self.correct_answer = quiz['correct_answer']
        self.feedback_message = ""
        self.button_enabled = True
        self.reset_button_colors()

    def reset_button_colors(self):
        """Resets all option buttons to their default white color and black text."""
        option_ids = ['opt_0', 'opt_1', 'opt_2', 'opt_3']
        for opt_id in option_ids:
            btn = self.root.ids[opt_id]
            btn.md_bg_color = [1, 1, 1, 1]  # White
            btn.text_color = [0, 0, 0, 1]   # Black
            btn.disabled = False            # Re-enable buttons

    def check_answer(self, selected_option, button_widget: MDRectangleFlatButton):
        """Checks the selected answer and schedules the next question."""
        if not self.button_enabled:
            return

        self.button_enabled = False
        
        # Disable all buttons immediately
        for child in self.root.ids.options_grid.children:
            child.disabled = True
            
        # Check result
        if selected_option.strip() == self.correct_answer.strip():
            self.feedback_message = "CORRECT!"
            self.feedback_color = [0, 0.8, 0, 1]  # Green
            button_widget.md_bg_color = [0.8, 1, 0.8, 1] # Light Green background
            
            # Schedule next question after 1.6 seconds (Requirement 2: 3 seconds converted to Kivy time)
            Clock.schedule_once(self.go_to_next_question, 1.6)
            
        else:
            self.feedback_message = "Incorrect. Try again."
            self.feedback_color = [0.8, 0, 0, 1]  # Red
            button_widget.md_bg_color = [1, 0.8, 0.8, 1] # Light Red background
            
            # Re-enable buttons and clear feedback after 1 second
            Clock.schedule_once(self.reset_on_incorrect, 1.0)
            
    def reset_on_incorrect(self, dt):
        """Called after an incorrect guess to re-enable buttons."""
        self.feedback_message = ""
        self.button_enabled = True
        self.reset_button_colors()
        
    def go_to_next_question(self, dt):
        """Advances to the next question."""
        self.current_q_index += 1
        self.load_question()

    def show_completion_screen(self):
        """Shows the Quiz Complete screen."""
        self.root.ids.quiz_screen.opacity = 0
        self.root.ids.quiz_screen.disabled = True
        
        self.root.ids.complete_screen.opacity = 1
        self.root.ids.complete_screen.disabled = False
        self.feedback_message = "Quiz Finished! Game Over."

if __name__ == '__main__':
    QuizApp().run()

