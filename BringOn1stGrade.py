"""
BringOn1stGrade.py

Kindergarten Math Game.

My 5-year-old son is in kindergarten and was recently given access to a math app that he can play on
a tablet. The game included an initial test to aid with placing him at the correct starter level. The placement
test had a timer in the shape of a progress bar at the bottom of the screen. For him the timer was a disturbance and
resulted in my son panicking and performing under his actual skill level as perceived by his dad.

So here is a similar game with a hidden timer concept. The timer is not threaded. I looked into a solution like that,
but this much simpler solution using the time module does exactly what I wanted (which is fortunate seeing as I do not
understand threading): Checks time at certain checkpoints instead of interrupting the student in the middle of a
problem. In reality, this means that the student always gets to finish the last problem no matter if the timer has been
exceeded. An exceeded timer is still technically a "fail", and the last problem, even if correctly answered, will not
count, but that information is not apparent to the student.
"""
# TODO: Add option at initialization to choose between apparent timed and untimed mode. Right now the default is
# TODO: that the placement tests run with a hidden timer and the training functions display the time spent after 10
# TODO: correct answers.


import random
import time


"""
These constants hold the number of seconds given for each of the problems posed in the placement test and the
addition/subtraction training respectively. Note that the PLACEMENT_TIMEOUT is "per question" and the
TRAINING_TIMEOUT is "per round". 
"""
PLACEMENT_TIMEOUT = 8
TRAINING_TIMEOUT = 20 # Default is 120s, but for the purposes of showing the app, I reduced it to 20s.


"""
The game runs an initial placement test for addition. Student is placed in a skill bracket from 1-5 and that level
is saved to the addition_skill_level variable and then passed into the addition function which is repeated until the
student reaches level 5 and 'graduates'. After this: Similar placement test, gameplay and graduation for subtraction...
....which concludes the curriculum for kindergarten math. Oh, how I long for the simpler times!
"""
def main():
    # Skill level is set for addition.
    addition_skill_level = addition_placement_test()
    # Addition training is repeated until the student reaches level 5 and graduates.
    while addition_skill_level <= 5:
        addition_skill_level = addition(addition_skill_level)
    print("Congratulations! You have mastered addition! \nNow, let's do some subtraction!")
    # Skill level is set for subtraction.
    subtraction_skill_level = subtraction_placement_test()
    # Subtraction training is repeated until the student reaches level 5 and graduates.
    while subtraction_skill_level <= 5:
        subtraction_skill_level = subtraction(subtraction_skill_level)
    print("Congratulations! You have mastered addition AND subtraction! \nKindergarten math is no match for you!"
          "\nBring on 1st grade!")


"""
The placement test poses as a warm-up exercise. However, a hidden timer is running to see if the student can solve
the problems within a given time frame. The timer is hidden so as to not put stress on the student. If the students
exceeds the time limit OR answers the question incorrectly, the skill level of the last correctly and timely answered
question is returned.
"""
def addition_placement_test():
    level = 1
    # Input prompt to avoid timer starting.
    input("Let's do a few warm-up problems! Press enter when you are ready!")
    # Record the time when the placement test is started.
    start_time = time.time()
    # Test runs up to level 5, but may be broken before.
    while level < 5:
        # Minimum and maximum parameters for random calls are set.
        minrand_a, maxrand_a, minrand_b, maxrand_b = set_addition_rands(level)
        a = random.randint(minrand_a, maxrand_a)
        b = random.randint(minrand_b, maxrand_b)
        # Poses the created problem to the student. Answer is kept as a string for now.
        answer_str = input("What is " + str(a) + " + " + str(b) + "? ")
        # Answer is passed on and type-checked. Integer is returned to answer_int.
        answer_int = check_if_int(answer_str)
        if answer_int == a + b:
            print("Good job! ")
        # In case of a wrong answer, the placement test ends and the level is set to the previous level and loop breaks.
        else:
            print("Warm-up done! Let's move on!")
            if level != 1:
                level -= 1
            break
        # This happens just as the answer is input.
        current_time = time.time()
        # elapsed_time variable stores how many seconds the student spent.
        elapsed_time = current_time - start_time
        # Did the student exceed the time limit? If so....
        if elapsed_time > PLACEMENT_TIMEOUT:
            print("Warm-up done! Let's move on!")
            if level != 1:
                level -= 1
            break
        # ...if not: The timer resets...
        else:
            start_time = time.time()
            # ...and the skill level goes up before the next iteration of the placement test.
            level +=1
    # The calculated start skill level for the addition training is returned.
    return level

"""
Same as addition placement test, but for subtraction training.
"""
def subtraction_placement_test():
    level = 1
    input("Let's do a few warm-up problems! Press enter when you are ready!")
    start_time = time.time()
    while level < 5:
        minrand_a, maxrand_a, minrand_b, maxrand_b = set_subtraction_rands(level)
        a = random.randint(minrand_a, maxrand_a)
        b = random.randint(minrand_b, maxrand_b)
        answer_str = input("What is " + str(a) + " - " + str(b) + "? ")
        answer_int = check_if_int(answer_str)
        if answer_int == a - b:
            print("Good job! ")
        else:
            print("Warm-up done! Let's move on!")
            if level != 1:
                level -= 1
            break
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > PLACEMENT_TIMEOUT:
            print("Warm-up done! Let's move on!")
            if level != 1:
                level -= 1
            break
        else:
            start_time = time.time()
            level += 1
    return level


"""
The addition function holds lists with set values for creating randomized problems for the student to solve.
The problems created are based on the current skill level. 10 correct answers are needed to reach the next skill level.
In this version, no penalty is imposed for a wrong answer. However, a hidden timer (default: TRAINING_TIMEOUT = 120) is
running in the background. If the time limit is exceeded at the time the student enters the 10th correct answer, the
student is told to practice a bit more on the same skill level e.g. the function repeats for the same skill level. 
"""
# TODO: Extension for later: When a wrong answer is given, save the operand set and bring the problem back at the end
# TODO: of the series.
def addition(level):
    input("You are currently at level " + str(level) + " of 5 in addition. Press enter to play!")
    start_time = time.time()
    correct_answers = 0
    # The variables used to create the addition problems are filled by passing the current level into the
    # set_addition_rands() function.
    minrand_a, maxrand_a, minrand_b, maxrand_b = set_addition_rands(level)
    while correct_answers < 10:
        # The operands for the addition problems are randomly set using the min- and max-rand values created.
        a = random.randint(minrand_a, maxrand_a)
        b = random.randint(minrand_b, maxrand_b)
        # Poses the created problem to the student. Answer is kept as a string for now.
        answer_str = input("What is " + str(a) +" + " + str(b) + "? ")
        # Answer is passed on and type-checked. Integer is returned.
        answer_int = check_if_int(answer_str)
        if answer_int == a + b:
            print("Correct!")
            correct_answers += 1
        else:
            print("Incorrect. Try this instead:")
    current_time = time.time()
    elapsed_time = current_time - start_time
    if elapsed_time > TRAINING_TIMEOUT:
        print("You did well, but you still need more practice on this level! See if you can get\n"
              "10 correct answers in less than " + str(TRAINING_TIMEOUT) + " seconds! This time you spent "
              + str(int(elapsed_time)) + " seconds. Go again!")
        return level
    else:
        print("You have passed level " + str(level) + " in " + str(int(elapsed_time)) + " seconds! You rock!")
        level += 1
        return level


"""
Subtraction version of the addition function with same functionality.
"""
def subtraction(level):
    input("You are currently at level " + str(level) + " of 5 in subtraction. Press enter to play!")
    start_time = time.time()
    correct_answers = 0
    minrand_a, maxrand_a, minrand_b, maxrand_b = set_subtraction_rands(level)
    while correct_answers < 10:
        a = random.randint(minrand_a, maxrand_a)
        b = random.randint(minrand_b, maxrand_b)
        answer_str = input("What is " + str(a) + " - " + str(b) + "? ")
        answer_int = check_if_int(answer_str)
        if answer_int == a - b:
            print("Correct!")
            correct_answers += 1
        else:
            print("Incorrect. Try this instead:")
    current_time = time.time()
    elapsed_time = current_time - start_time
    if elapsed_time > TRAINING_TIMEOUT:
        print("You did well, but you still need more practice on this level! See if you can get\n"
              "10 correct answers in less than " + str(TRAINING_TIMEOUT) + " seconds! This time you spent "
              + str(int(elapsed_time)) + " seconds. Go again!")
        return level
    else:
        print("You have passed level " + str(level) + " in " + str(int(elapsed_time)) + " seconds! You rock!")
        level += 1
        return level


"""
The function checks if the passed parameter is an integer. If it isn't, the function asks the user to input an integer
and returns it once an integer is input.
"""
def check_if_int(answer_str):
    # Variable to be checked if it is an integer is deliberately set to a string before the loop starts.
    answer_int = "Horsejazz"
    # This loop handles the case of the student inputting anything else than an integer.
    while type(answer_int) is not int:
        try:
            answer_int = int(answer_str)
        except ValueError:
            # The prompt asks the user for a "number" even though technically this exception also handles the
            # ValueError of a float being input (which is of course also a number). However, the target group is
            # kindergarten, so asking them for an "integer" seems like it would just confuse the student.
            answer_str = input("Please answer with a number: ")
    return answer_int


# Based on the passed parameter 'level', minimum and maximum values for generation of random operators are passed back.
def set_addition_rands(level):
    addition_level1a = [0, 3]
    addition_level1b = [1, 3]
    addition_level2a = [1, 4]
    addition_level2b = [2, 4]
    addition_level3a = [3, 6]
    addition_level3b = [4, 6]
    addition_level4a = [5, 8]
    addition_level4b = [5, 8]
    addition_level5a = [6, 10]
    addition_level5b = [6, 10]
    if level == 1:
        minrand_a = addition_level1a[0]
        maxrand_a = addition_level1a[1]
        minrand_b = addition_level1b[0]
        maxrand_b = addition_level1b[1]
        return minrand_a, maxrand_a, minrand_b, maxrand_b
    if level == 2:
        minrand_a = addition_level2a[0]
        maxrand_a = addition_level2a[1]
        minrand_b = addition_level2b[0]
        maxrand_b = addition_level2b[1]
        return minrand_a, maxrand_a, minrand_b, maxrand_b
    if level == 3:
        minrand_a = addition_level3a[0]
        maxrand_a = addition_level3a[1]
        minrand_b = addition_level3b[0]
        maxrand_b = addition_level3b[1]
        return minrand_a, maxrand_a, minrand_b, maxrand_b
    if level == 4:
        minrand_a = addition_level4a[0]
        maxrand_a = addition_level4a[1]
        minrand_b = addition_level4b[0]
        maxrand_b = addition_level4b[1]
        return minrand_a, maxrand_a, minrand_b, maxrand_b
    if level == 5:
        minrand_a = addition_level5a[0]
        maxrand_a = addition_level5a[1]
        minrand_b = addition_level5b[0]
        maxrand_b = addition_level5b[1]
        return minrand_a, maxrand_a, minrand_b, maxrand_b


# Based on the passed parameter 'level', minimum and maximum values for generation of random operators are passed back.
def set_subtraction_rands(level):
    subtraction_level1a = [4, 7]
    subtraction_level1b = [0, 4]
    subtraction_level2a = [7, 10]
    subtraction_level2b = [2, 6]
    subtraction_level3a = [10, 13]
    subtraction_level3b = [4, 8]
    subtraction_level4a = [13, 16]
    subtraction_level4b = [6, 10]
    subtraction_level5a = [16, 19]
    subtraction_level5b = [8, 12]
    if level == 1:
        minrand_a = subtraction_level1a[0]
        maxrand_a = subtraction_level1a[1]
        minrand_b = subtraction_level1b[0]
        maxrand_b = subtraction_level1b[1]
        return minrand_a, maxrand_a, minrand_b, maxrand_b
    if level == 2:
        minrand_a = subtraction_level2a[0]
        maxrand_a = subtraction_level2a[1]
        minrand_b = subtraction_level2b[0]
        maxrand_b = subtraction_level2b[1]
        return minrand_a, maxrand_a, minrand_b, maxrand_b
    if level == 3:
        minrand_a = subtraction_level3a[0]
        maxrand_a = subtraction_level3a[1]
        minrand_b = subtraction_level3b[0]
        maxrand_b = subtraction_level3b[1]
        return minrand_a, maxrand_a, minrand_b, maxrand_b
    if level == 4:
        minrand_a = subtraction_level4a[0]
        maxrand_a = subtraction_level4a[1]
        minrand_b = subtraction_level4b[0]
        maxrand_b = subtraction_level4b[1]
        return minrand_a, maxrand_a, minrand_b, maxrand_b
    if level == 5:
        minrand_a = subtraction_level5a[0]
        maxrand_a = subtraction_level5a[1]
        minrand_b = subtraction_level5b[0]
        maxrand_b = subtraction_level5b[1]
        return minrand_a, maxrand_a, minrand_b, maxrand_b


if __name__ == '__main__':
    main()