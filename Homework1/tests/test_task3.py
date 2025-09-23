from task3 import check_number_sign, get_first_n_primes, sum_with_while_loop

def test_check_number_sign():
    assert check_number_sign(5) == "Positive"
    assert check_number_sign(-3) == "Negative"
    assert check_number_sign(0) == "Zero"

def test_get_first_n_primes():
    expected_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert get_first_n_primes(10) == expected_primes

def test_sum_with_while_loop():
    assert sum_with_while_loop(100) == 5050

