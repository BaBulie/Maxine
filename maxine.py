import itertools
import cursor
import time
import sys
import os
from termcolor import colored, cprint
from preferredsoundplayer import *
import random

cursor.hide()

# Import tic lists
file_mini = open('mini_tics.txt', 'r')
file_vocal = open('vocal_tics.txt', 'r')
file_physical = open('physical_tics.txt', 'r')

f_mini = file_mini.readlines()
f_vocal = file_vocal.readlines()
f_physical = file_physical.readlines()

mini_tics = []
for line in f_mini:
    mini_tics.append(line.strip())
vocal_tics = []
for line in f_vocal:
    vocal_tics.append(line.strip())
physical_tics = []
for line in f_physical:
    physical_tics.append(line.strip())

# Assign sound files
announce = "announce.wav"
mini = "tic.wav"

# Let the user pick day quality
print("Please choose day quality.")
print(colored("Good:", 'green'), "1 | ", colored("Medium:", 'yellow'), "2 | ", colored("Bad:", 'red'), "3 | ", colored("Weigthed random:", 'magenta'), "4")
day_choice = input("Choice: ")

# Day probabilites
good_day_probability = 5
medium_day_probability = 3
bad_day_probability = 1
total_day_probability = good_day_probability + medium_day_probability + bad_day_probability # Helper variable for calculating %

# Tic type probabilities
vocal_probability = 20
physical_probability = 15
faint_probability = 1
total_tic_probability = vocal_probability + physical_probability + faint_probability # Helper variable for calculating %

# Pick a day quality (good, medium, bad) and set probabilities
if day_choice == "1":
    day_type = 1
    day_text = colored("Waiting for tic(s)...", "green", attrs=['underline'])
elif day_choice == "2":
    day_type = 2
    day_text = colored("Waiting for tic(s)...", "yellow", attrs=['underline'])
elif day_choice == "3":
    day_type = 3
    day_text = colored("Waiting for tic(s)...", "red", attrs=['underline'])
else:
    day_type = random.choices(population=[1, 2, 3], weights=[good_day_probability, medium_day_probability, bad_day_probability], k=1)[0]
    day_text = colored("Waiting for tic(s)...", "magenta", attrs=['underline'])

# Set wait times based on the day quality
if day_type == 1:
    min_time = 4200 # 1 hour 10 minutes
    max_time = 5400 # 1 hour 30 minutes
elif day_type == 2:
    min_time = 3000 # 50 minutes
    max_time = 4200 # 1 hour 10 minutes
elif day_type == 3:
    min_time = 1800 # 30 minutes
    max_time = 3000 # 50 minutes

min_mini = min_time / 2
max_mini = max_time / 2

# Minimum and maximum burst amount per day type
if day_type == 1:
    min_burst = 1
    max_burst = 3
elif day_type == 2:
    min_burst = 2
    max_burst = 4
elif day_type == 3:
    min_burst = 3
    max_burst = 5

# Minimum and maximum burst wait times
min_burst_time = 8
max_burst_time = 18

# MAIN LOOP
while True:
    os.system('cls')

    if day_choice == "4":
        cprint("Day probabilites", attrs=['underline'])
        print("Good day:", round((good_day_probability/total_day_probability)*100, 1), "%")
        print("Medium day:", round((medium_day_probability/total_day_probability)*100, 1), "%")
        print("Bad day:", round((bad_day_probability/total_day_probability)*100, 1), "%\n")

    cprint("Tic type probabilites", attrs=['underline'])
    print("Vocal:", round((vocal_probability/total_tic_probability)*100, 1), "%")
    print("Physical:", round((physical_probability/total_tic_probability)*100, 1), "%")
    print("Faint:", round((faint_probability/total_tic_probability)*100, 1), "%\n")
    
    print(day_text)
    
    time_left = random.randint(min_time, max_time)
    mini_left = random.randint(min_mini, max_mini)
    spinner = itertools.cycle(['[M     ]', '[ A    ]', '[  X   ]', '[   I  ]', '[    N ]', '[     E]'])
    while time_left > 29:
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        sys.stdout.write('\r')
        time.sleep(1)
        time_left -= 1

        # Mini tics
        mini_left -= 1
        if mini_left < 1:
            mini_left = random.randint(min_mini, max_mini)
            soundplay(mini)
            os.system('cls')

            # Display the list of mini tics
            cprint("\nMini tics!", "green", attrs=['underline'])
            print("\n", random.choice(mini_tics), "\n", random.choice(mini_tics))
            time.sleep(20)
            
            os.system('cls')
            print(day_text)

    # Get the user's attention
    os.system('cls')
    soundplay(announce)

    while time_left > 0:
        cprint("                    TIC INCOMING!                    ", "black", "on_red")
        time.sleep(1)
        time_left -= 1
        
    os.system('cls')
    burst_amount = random.randint(min_burst, max_burst)
    current_tic = 0
    while current_tic < burst_amount:
        print("\n")
        
        tic_type = random.choices(population=[1, 2, 3], weights=[vocal_probability, physical_probability, faint_probability], k=1)[0]
        
        if tic_type == 1:
            tic = colored(random.choice(vocal_tics), "green", attrs=["bold"])
        elif tic_type == 2:
            tic = colored(random.choice(physical_tics), "cyan", attrs=["bold"])
        elif tic_type == 3:
            tic = colored("Oh no! You feel dizzy and FAINT within the time limit!", "black", "on_red")
            current_tic = burst_amount - 1  # To end the sequence if a faint happens

        print(tic)

        # Setup the progress bar
        if tic_type == 3:
            toolbar_width = random.randint(60, 117)
        else:
            toolbar_width = random.randint(min_burst_time, max_burst_time)
        
        sys.stdout.write("[%s]" % (" " * toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (toolbar_width+1))
        
        for i in range(toolbar_width):
            time.sleep(1)
            sys.stdout.write(">")
            sys.stdout.flush()

        current_tic += 1

        # Reset sequence
        if current_tic == burst_amount:
            if tic_type == 3:
                reset_text = "You wake up in: "
                reset_time = random.randint(120, 240)
            else:
                reset_text = "Tic(s) done, resetting in: "
                reset_time = 30

            print("\n", "\n")
            while reset_time > 0:
                print(reset_text, reset_time, " ", end='\r')
                reset_time -= 1
                time.sleep(1)
