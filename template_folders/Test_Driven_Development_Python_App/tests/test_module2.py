from src.project_name import module2

def test_multiply(sample_numbers):
    a, b = sample_numbers
    assert module2.multiply(a, b) == 6
