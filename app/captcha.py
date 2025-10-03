import random 

def generate_captcha():
    a,b = random.randint(1,9), random.randint(1,9)
    question = f"{a} + {b}"
    answer = a + b
    return question, answer