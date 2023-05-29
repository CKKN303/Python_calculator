'''Task:
Write program that allows user to choose between:
1. Manually entering equations and displaying results, saving the equations to a text file
2. Importing a text file containing equations and displaying the results

- Prep section:
Import re module and define function which uses regex to search for equations format of 'number' 'operator' 'number'.
From Operator module, import commonly used operators: add, sub, mul, truediv

Create dictionary of approved operator symbols
Create equation pattern for regex to compile

Define calculator function which searches for defined regex with if/else statement to approve operator.
With try/except block, error handling within the function will account for: AttributeError, ZeroDivisionError, general Exception

- User-interactive section:
Within an outer while loop, request user choose between manual entry and file import
- If valid prompts are given
    1: Manual data entry -
        Inner while loop: allows the user to enter multiple calculations, evaluating input for given exit clause with each iteration
            - Call above defined function to calculate equation
            - Write equation to a .txt file. Save equation with each iteration of loop to prevent loss of data in case of unforeseen error ending program.
            - Display answer to the equation
            - If user exits program, display message letting them know equations have been saved to text file
    2: File Import -
        - Try requesting name of .txt file to open from user (provide 'q' as exit option)
        - Use except block to safeguard against FileNotFound Exception (if invalid input provided, prompt file name input again.)
        - Open .txt file (checking file len() to account for empty file, provide error message)
        - print out all of the equations from the .txt file together with the results.
- Else invalid input provided: continue program and prompt menu input again
- Place escape clause at this level: Prompt user to press 'q' again if they wish to exit, if input == 'q', break program'''

import re
from operator import add, sub, mul, truediv

# Operator dictionary for imported operators
operators = {'+': add, '-': sub, '*': mul, '/': truediv}

# RegEx pattern for manually entered equations in the loop below
equation_pattern = re.compile(r'^(\d+\.*\d*)\s*(.)\s*(\d+\.*\d*)$')

# Calculator function
def calculate(equation):
    # Try statement searches for defined equation pattern in user input
    try:
        x, o, y = equation_pattern.match(equation).groups()
        if op := operators.get(o):
            return f'{equation} = {op(float(x), float(y))}'
        else:
            return f'Unknown operator: {o}'
    # Exceptions accounted for in user input
    except AttributeError:
        return "Calculation could not be performed. Please check your equation is the correct format and try again."
    except ZeroDivisionError:
        return "You cannot divide by zero."
    except Exception as e:
        return f'Unable to process "{equation}" due to {e}'

# Outer loop prompting user to choose from calculator types (manual or import), accounting for wrong input type and escape clause
while True:
    #Provides user with menu options
    print('''Please choose from the following options:
1. Manual Data Entry - enter two numbers and an operator
2. File Import - import equations from a text file''')
    
    # Prompts user to choose between manual data entry and file import for calculating equations
    calculator_choice = input("Enter the option number to proceed (or 'q' to quit):\n").lower()

    # Allows the user to end the program
    if calculator_choice == 'q':
        break

    # Inner loop for manual data entry for calculating equations
    if calculator_choice == '1':
        while True:
            equation = input("Enter a simple equation 'X Y' where X and Y are numbers, and your operator is one of the following: +, -, *, / (or 'q' to quit): ")

            # Allows user to exit inner loop when pressing 'q' in equation request input
            if equation == 'q':
                # Prints confirmation of file name and saved equations when the program has been ended
                print(f'Calculations entered have been saved to the text file "{file_name}".')    
                break
            
            # Calls calculate() function above and prints result
            equation_result = calculate(equation)
            print(equation_result)

            # Saves equation and result to .txt file
            file_name = "Equations.txt"
            with open(file_name, "a") as f:
                f.write(f"{equation_result}\n")

    # Inner loop for file import option
    elif calculator_choice == '2':
        while True:
            filename = input("Enter the name of the text file (or 'q' to quit): ")

            # Allows user to exit inner loop when pressing 'q' in file name input
            if filename == 'q':
                break
            
            # Opens text file given by user, calculates results and prints them
            try:
                with open(filename, 'r') as infile:
                    equations = infile.readlines()

                # Checks if file is empty by checking length
                if len(equations) == 0:
                    print("The file is empty.")
                # Calls calculate() function above and displays result(s)
                else:
                    for i, equation in enumerate(equations, start=1):
                        equation = equation.strip()
                        equation_result = calculate(equation)
                        print(f"[{i}]: {equation_result}")

            # Accounts for non-existent file
            except FileNotFoundError:
                print(f"The file '{filename}' does not exist. Please enter a valid file name.")

    # Handles wrong input in the menu choice loop
    else:
        print("Please enter a valid option number.")
        continue
    
    # Confirms user choice to exit program by pressing 'q' again or allowing user to continue
    print("\nPress 'q' to quit or any other key to continue...")
    choice = input()
    if choice == 'q':
        break