# fizzbuzz

MAX_NUMBER = 100

for number in range(1, MAX_NUMBER+1):
    multiple_of_3 = number%3 == 0
    multiple_of_5 = number%5 == 0

    if multiple_of_3 and multiple_of_5:
        print('FizzBuzz')
    else:
        if multiple_of_3:
            print('Fizz')
        elif multiple_of_5:
            print('Buzz')
        else:
            print(number)