from app.captcha import generate_captcha

def test_generate_captcha():
    question, answer = generate_captcha()
    assert "+" in question
    assert isinstance(answer, int)
    assert eval(question) == answer