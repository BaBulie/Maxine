import itertools
import cursor
import time
import sys
import os
from termcolor import colored, cprint
from preferredsoundplayer import *
import random

def set_sounds():
    if os.path.isfile('announce.wav') == False:
        cprint("[Errno 2] No such file or directory: 'announce.wav'\n", "red")

    if os.path.isfile('tic.wav') == False:
        cprint("[Errno 2] No such file or directory: 'tic.wav'\n", "red")

    if (os.path.isfile('announce.wav') and os.path.isfile('tic.wav')) == False:
        sound_choice = input("> Would you like to continue without the listed sound(s)? Y/N: ").upper()
        if sound_choice == "N":
            sys.exit()


def import_tics():
    try:
        file_mini = open('mini_tics.txt', 'r')
        f_mini = file_mini.readlines()
    except FileNotFoundError as e:
        cprint(f'{e}', "red")
        with open('mini_tics.txt', 'a+') as file_mini:
            file_mini.write("Mini tic")
            time.sleep(1)
            print('> File created with placeholder tic.\n')
            f_mini = file_mini.readlines()
            time.sleep(1)

    try:
        file_vocal = open('vocal_tics.txt', 'r')
        f_vocal = file_vocal.readlines()
    except FileNotFoundError as e:
        cprint(f'{e}', "red")
        with open('vocal_tics.txt', 'a+') as file_vocal:
            file_vocal.write("Vocal tic")
            time.sleep(1)
            print('> File created with placeholder tic.\n')
            f_vocal = file_vocal.readlines()
            time.sleep(1)

    try:
        file_physical = open('physical_tics.txt', 'r')
        f_physical = file_physical.readlines()
    except FileNotFoundError as e:
        cprint(f'{e}', "red")
        with open('physical_tics.txt', 'a+') as file_physical:
            file_physical.write("Physical tic")
            time.sleep(1)
            print('> File created with placeholder tic.\n')
            f_physical = file_physical.readlines()
            time.sleep(1)

    mini_tics = []
    for line in f_mini:
        mini_tics.append(line.strip())
    vocal_tics = []
    for line in f_vocal:
        vocal_tics.append(line.strip())
    physical_tics = []
    for line in f_physical:
        physical_tics.append(line.strip())

    return mini_tics, vocal_tics, physical_tics


def get_probabilities():
    good_day_probability = 6
    medium_day_probability = 4
    bad_day_probability = 2
    total_day_probability = good_day_probability + medium_day_probability + bad_day_probability # Helper variable for calculating %

    vocal_probability = 20
    physical_probability = 15
    faint_probability = 1
    total_tic_probability = vocal_probability + physical_probability + faint_probability # Helper variable for calculating %

    return good_day_probability, medium_day_probability, bad_day_probability, total_day_probability, vocal_probability, physical_probability, faint_probability, total_tic_probability


def get_primary_times(good_day_probability, medium_day_probability, bad_day_probability):
    print("Please choose day quality.")
    print(colored("Good:", 'green'), "1 | ", colored("Medium:", 'yellow'), "2 | ", colored("Bad:", 'red'), "3 | ", colored("Weigthed random:", 'magenta'), "4")
    day_choice = input("Choice: ")

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

    if day_type == 1:
        min_time = 4200 # 1 hour 10 minutes
        max_time = 5400 # 1 hour 30 minutes
        min_burst = 1
        max_burst = 3
    elif day_type == 2:
        min_time = 3000 # 50 minutes
        max_time = 4200 # 1 hour 10 minutes
        min_burst = 2
        max_burst = 4
    elif day_type == 3:
        min_time = 1800 # 30 minutes
        max_time = 3000 # 50 minutes
        min_burst = 3
        max_burst = 5

    return day_choice, day_text, min_time, max_time, min_burst, max_burst


def get_secondary_times(min_time, max_time):
    min_mini_time = int(min_time / 3)
    max_mini_time = int(max_time / 3)
    min_burst_time = 8
    max_burst_time = 18

    return min_mini_time, max_mini_time, min_burst_time, max_burst_time


def print_probabilities(choice, good, medium, bad, total_day, vocal, physical, faint, total_tic):
        if choice == "4":
            cprint("Day probabilites", attrs=['underline'])
            print("Good day:", round((good/total_day)*100, 1), "%")
            print("Medium day:", round((medium/total_day)*100, 1), "%")
            print("Bad day:", round((bad/total_day)*100, 1), "%\n")

        cprint("Tic type probabilites", attrs=['underline'])
        print("Vocal:", round((vocal/total_tic)*100, 1), "%")
        print("Physical:", round((physical/total_tic)*100, 1), "%")
        print("Faint:", round((faint/total_tic)*100, 1), "%\n")


def main():
    cursor.hide()
    set_sounds()
    mini_tics, vocal_tics, physical_tics = import_tics()
    good_day_probability, medium_day_probability, bad_day_probability, total_day_probability, vocal_probability, physical_probability, faint_probability, total_tic_probability = get_probabilities()
    day_choice, day_text, min_time, max_time, min_burst, max_burst = get_primary_times(good_day_probability, medium_day_probability, bad_day_probability)
    min_mini_time, max_mini_time, min_burst_time, max_burst_time = get_secondary_times(min_time, max_time)

    while True:
        os.system('cls')
        
        print_probabilities(day_choice, good_day_probability, medium_day_probability, bad_day_probability, total_day_probability, 
                        vocal_probability, physical_probability, faint_probability, total_tic_probability)
        print(day_text)
        
        time_left = random.randint(min_time, max_time)
        mini_left = random.randint(min_mini_time, max_mini_time)
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
                mini_left = random.randint(min_mini_time, max_mini_time)
                if os.path.isfile('tic.wav'):
                    soundplay("tic.wav")
                os.system('cls')

                # Display the list of mini tics
                cprint("\nMini tics!\n", "green", attrs=['underline'])
                current_mini = 0
                while current_mini < random.randint(1,3):
                    print(random.choice(mini_tics))
                    current_mini += 1
                
                print("")
                reset_time = 20
                while reset_time > 0:
                    print("Continuing in: ", reset_time, " ", end='\r')
                    reset_time -= 1
                    time.sleep(1)
                
                os.system('cls')
                print_probabilities(day_choice, good_day_probability, medium_day_probability, bad_day_probability, total_day_probability, 
                        vocal_probability, physical_probability, faint_probability, total_tic_probability)
                print(day_text)

        # Get the user's attention
        os.system('cls')
        if os.path.isfile('announce.wav'):
            soundplay("announce.wav")

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

if __name__ == '__main__':
    main()