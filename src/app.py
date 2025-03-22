from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, Button
from textual.containers import Vertical, Horizontal
import time
from src.math_generator import generate_question

class StopwatchApp(App):
    """A Textual app to manage stopwatches."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Vertical(
            Static("Welcome to Mental Math Practice!", id="welcome"),
            Static("", id="question"),
            Horizontal(
                Input(placeholder="Your answer", id="answer"),
                Button("Submit", id="submit"),
                id="input_area",
            ),
            Static("", id="result"),
            id="content",
        )
        yield Footer()

    def on_mount(self) -> None:
        """Generate the first question when the app starts."""
        self.generate_question()
        self.start_timer()
        self.correct_answers = 0
        self.total_questions = 0

    def start_timer(self) -> None:
        """Start the 60-second timer."""
        self.start_time = time.time()
        self.set_timer(1, self.update_timer)

    def generate_question(self) -> None:
        """Generate a new mental math question."""
        question_text, answer = generate_question()
        self.answer = answer

        self.query_one("#question").update(question_text)
        self.query_one("#answer").value = ""  # Clear previous answer
        self.query_one("#answer").focus()  # Put the focus on the input

    def update_timer(self) -> None:
        """Update the timer display."""
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = 60 - elapsed_time

        if remaining_time <= 0:
            self.show_statistics()
        else:
            self.query_one("#welcome").update(
                f"Time remaining: {remaining_time} seconds"
            )
            self.set_timer(1, self.update_timer)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "submit":
            self.check_answer()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle enter key press in the input field."""
        self.check_answer()

    def check_answer(self) -> None:
        """Check the user's answer and display the result."""
        try:
            user_answer = int(self.query_one("#answer").value)
            self.total_questions += 1
            if user_answer == self.answer:
                result_text = "Correct!"
                self.correct_answers += 1
            else:
                result_text = f"Incorrect. The correct answer is {self.answer}."
            self.query_one("#result").update(result_text)
        except ValueError:
            self.query_one("#result").update("Please enter a valid number.")

        self.generate_question()  # Generate the next question

    def show_statistics(self) -> None:
        """Display the statistics at the end of the timer."""
        accuracy = (
            (self.correct_answers / self.total_questions) * 100
            if self.total_questions > 0
            else 0
        )
        statistics_text = f"Time's up!\nCorrect answers: {self.correct_answers}\nTotal questions: {self.total_questions}\nAccuracy: {accuracy:.2f}%"
        self.query_one("#question").update(statistics_text)
        self.query_one("#input_area").display = False  # hide input area
        self.query_one("#result").display = False  # hide results
        self.query_one("#welcome").update("")  # remove timer display

def main():
    app = StopwatchApp()
    app.run()

if __name__ == "__main__":
    main()
