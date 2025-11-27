import kivy
from kivy.app import App
from kivy.uix.label import Label

class GitHubActionApp(App):
    def build(self):
        return Label(text='Built by GitHub Actions!', font_size=50)

if __name__ == '__main__':
    GitHubActionApp().run()


