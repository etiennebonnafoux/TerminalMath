import random

def generate_question() -> tuple[str,int]:
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    operator = random.choice(["+", "-", "*"])

    if operator == "+":
        answer = num1 + num2
        question_text = f"What is {num1} + {num2}?"
    elif operator == "-":
        answer = num1 - num2
        question_text = f"What is {num1} - {num2}?"
    else:
        answer = num1 * num2
        question_text = f"What is {num1} * {num2}?"
    return question_text, answer