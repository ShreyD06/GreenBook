from random import randint, choice, shuffle

def random_name():
    consonants = 'qwrtypsdfghjklzxcvbnm'
    vowels = 'aeiou'
    first_name_length = randint(5, 10)
    last_name_length = randint(7, 20)
    fnvowels = first_name_length//2
    fncons = first_name_length - fnvowels
    lnvowels = last_name_length//2
    lncons = last_name_length - lnvowels
    return ''.join(shuffle(
