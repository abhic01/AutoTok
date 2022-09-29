
""" 
As a Hokie, I, Abhilash Chauhan ,  will conduct myself with honor and integrity at all times.  
I will not lie, cheat, or steal, nor will I accept the actions of those who do.”

"""
#############################################################################
################ DO NOT MODIFY THIS CODE ####################################
#############################################################################
import argparse
from autograder import *


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='A Python application to evaluate and translate postfix expressions', allow_abbrev=True)
    parser.add_argument('-i', '--input_file', type=str,
                        help='name of input file containing postfix expressions separated by newline')
    parser.add_argument('-o', '--output_file', type=str, nargs='?',
                        help='name of the output file to save the output')
    parser.add_argument('-m', '--mode', type=str,
                        help='mode of the script--Evaluator, Translator, or Tester', choices=['eval', 's2s', 'test'], required=True)
    args = parser.parse_args()
    return args


def main():
    output_lines = []
    try:
        with open(args.input_file) as file:
            lines = file.readlines()
            if args.mode == 'eval':
                output_lines = map(lambda x: evaluate(x).strip(), lines)

            else:
                output_lines = map(lambda x: postToInfix(x).strip(), lines)
            with open(args.output_file, 'w') as f:
                f.write('\n'.join(output_lines))
    except FileNotFoundError:
        msg = "ERROR: " + args.input_file + " does not exist."
        print(msg)
#############################################################################
################ Write your code below this line ############################
#############################################################################

#List of valid operators that can be used in the equations
operators = ['+', '-', '/', '*']

"""
Helper function to help check if an input is valid
"""
def validInput(s):
    return sum(c.isdigit() for c in s) == (sum(c in operators for c in s) + 1)

"""
Helper function to calculate the result of an operation
"""
def calculate(cur2, cur, cur1):
    if cur == '+':
        return cur2 + cur1
    elif cur == '-':
        return cur2 - cur1
    elif cur == '/':
        return cur2 / cur1
    else:
        return cur2 * cur1

""" 
Task 1 implementation goes here. Feel free to add more functions or classes.
"""
def evaluate(postfix_equation_string):
    tokens = postfix_equation_string.split()
    if validInput(tokens):
        if tokens[0].isdigit() and tokens[1].isdigit() and tokens[-1] in operators:
            stack = []
            for cur in tokens:
                if cur.isdigit():
                    stack.append(cur)
                elif cur in operators:
                    cur1 = float(stack.pop())
                    cur2 = float(stack.pop())
                    stack.append(str(calculate(cur2, cur, cur1)))
            return stack.pop()
        return "ERROR: invalid input"
    return "ERROR: too many literals"

""" 
Task 2 implementation goes here. Feel free to add more functions or classes.
"""
def postToInfix(postfix_equation_string):
    tokens = postfix_equation_string.split()
    if validInput(tokens):
        if tokens[0].isdigit() and tokens[1].isdigit() and tokens[-1] in operators:
            stack = []
            for cur in tokens:
                if cur.isdigit():
                    stack.append(cur)
                elif cur in operators:
                    cur1 = stack.pop()
                    cur2 = stack.pop()
                    stack.append("(" + cur2 + ") " + cur + " (" + cur1 + ")")
            return stack.pop()
        return "ERROR: invalid input"
    return "ERROR: too many literals"

#############################################################################
################ Write your code above this line ############################
#############################################################################
if __name__ == '__main__':
    args = parse_arguments()
    if args.mode == "test":
        test()
    else:
        main()
