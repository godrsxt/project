from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
import random
import time

class TypingTest(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        
        # Sample word list (you can expand this)
        self.words = [
            "the", "be", "to", "of", "and", "a", "in", "that", "have", "I",
            "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
            "this", "but", "his", "by", "from", "they", "we", "say", "her", "she"
        ]
        
        # Initialize variables
        self.current_text = ""
        self.start_time = None
        self.is_test_active = False
        self.correct_chars = 0
        self.total_chars = 0
        
        # Create UI elements
        self.target_label = Label(
            text="Press 'Start Test' to begin",
            size_hint_y=0.2,
            font_size='20sp'
        )
        self.add_widget(self.target_label)
        
        self.input_field = TextInput(
            multiline=False,
            size_hint_y=0.2,
            font_size='20sp',
            disabled=True
        )
        self.input_field.bind(text=self.on_text_change)
        self.add_widget(self.input_field)
        
        self.stats_label = Label(
            text="WPM: 0 | Accuracy: 0%",
            size_hint_y=0.2
        )
        self.add_widget(self.stats_label)
        
        self.start_button = Button(
            text="Start Test",
            size_hint_y=0.2
        )
        self.start_button.bind(on_press=self.start_test)
        self.add_widget(self.start_button)

    def generate_text(self):
        # Generate a random sequence of words
        word_count = 10
        selected_words = random.sample(self.words, word_count)
        return " ".join(selected_words)

    def start_test(self, instance):
        self.current_text = self.generate_text()
        self.target_label.text = self.current_text
        self.input_field.disabled = False
        self.input_field.text = ""
        self.start_time = time.time()
        self.is_test_active = True
        self.correct_chars = 0
        self.total_chars = 0
        self.input_field.focus = True

    def on_text_change(self, instance, value):
        if not self.is_test_active:
            return

        # Calculate statistics
        self.total_chars = len(value)
        self.correct_chars = sum(1 for i, c in enumerate(value) 
                               if i < len(self.current_text) and c == self.current_text[i])
        
        # Calculate accuracy
        accuracy = (self.correct_chars / max(1, self.total_chars)) * 100
        
        # Calculate WPM
        elapsed_time = time.time() - self.start_time
        minutes = elapsed_time / 60
        wpm = (self.total_chars / 5) / max(minutes, 0.01)  # Standard WPM calculation
        
        # Update stats display
        self.stats_label.text = f"WPM: {int(wpm)} | Accuracy: {accuracy:.1f}%"
        
        # Check if test is complete
        if len(value) >= len(self.current_text):
            self.finish_test()

    def finish_test(self):
        self.is_test_active = False
        self.input_field.disabled = True
        self.start_button.text = "Start New Test"

class TypingTestApp(App):
    def build(self):
        return TypingTest()

if __name__ == '__main__':
    TypingTestApp().run()
