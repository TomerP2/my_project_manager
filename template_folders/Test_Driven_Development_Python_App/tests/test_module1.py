from src.project_name import module1

def test_add(sample_numbers):
    a, b = sample_numbers
    assert module1.add(a, b) == 5
