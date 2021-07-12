
def test_lengh_of_input():
    phrase = input("Set a phrase less than 15 characters: ")
    assert len(phrase) < 15, "The lengh of phrase is longer than 15 characters"
