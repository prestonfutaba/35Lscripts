#!/usr/bin/python

import random, sys
import argparse

def main():
    """Output randomly selected lines from FILE."""
    # Initializing parser and flags
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--echo",
                        help="treat each ARG as an input line", type=str, nargs="*")
    parser.add_argument("-n", "--head-count",
                        help="output at most COUNT lines", type=int)
    parser.add_argument("-r", "--repeat",
                        help="output lines can be repeated", action="store_true")
    parser.add_argument("-i", "--input-range",
                        help="treat each number LO through HI as an input line", type=str)
    # Use parse_known_args to return any text that isn't matched with a flag
    args, unknown = parser.parse_known_args()
    # edited_f is the list that I'm going to build, from either the file, stdin, or input range
    edited_f = []
    stdin = False
    # Raising error, copied from errors I've encountered from shuf
    if args.echo != None and args.input_range:
        print("shuf.py: cannot combine -e and -i options")
        sys.exit(1)
    if len(unknown) > 1 and args.echo == None:
        print("shuf: extra operand '"+ unknown[-1]+"'")
        sys.exit(1)
    if len(unknown) > 0 and args.input_range:
        print("shuf: extra operand '"+ unknown[-1]+"'")
        sys.exit(1)
    if args.echo!=None and len(unknown)==0 and args.repeat:
        print("shuf: no lines to repeat")
        sys.exit(1)
    # Deal with inputting the data into the shuf.py function, output array containing lines to potentially print
    # flags is the case when I don't have an echo flag or input range flag
    flags = True
    # bounds is potentially used later, so need to initialize it with values that won't stop it from running later
    bounds = [0, 100000000]
    if (args.echo==None and args.input_range==None):
        flags = False
    if args.input_range:
        bounds = args.input_range.split('-')
        edited_f = list(range(int(bounds[0]), int(bounds[1])+1))
    if (len(unknown)==0 and not flags):
        # Read from standard input
        stdin = True
        read_in = sys.stdin.readline().rstrip('\n')
    if(len(unknown)==1 and unknown[0]=='-' and args.echo==None):
        stdin = True
        read_in = sys.stdin.readline().rstrip('\n')
    else:
        if (len(unknown)==1 and unknown[0]!="-"):
            edited_f = []
            f = open(unknown[0], "r").readlines()
            # Creates list called f which holds the lines from the file
            for line in f:
                edited_f.append(line.rstrip('\n'))
    # Reading in from stdin when provied " " or "-", until they press ^D
    if stdin:
        while (read_in != ""):
            edited_f.append(read_in)
            read_in = sys.stdin.readline()
            if read_in == '\n':
                continue
            else:
                read_in = read_in.rstrip('\n')
    # shuffling array how we would like (repeats, head_count)
    # print out shuffled array from second stage
    if args.echo:
        if not args.head_count:
            if args.repeat:
                # Loop forever until user interrupts, since 0!=1 all the time
                while (1 != 0):
                    print(random.choice(args.echo))
            else:
                for i in random.sample(args.echo, len(args.echo)):
                    print(i)
        else:
            if args.repeat:
                # Situation where repeat and head count is true, with echo, print up to "head_count" args
                for i in range(args.head_count):
                    print(random.choice(args.echo))
            else:
                # Randomized array from echo provided arguments, read whichever is smaller, head count or
                # number of arguments
                rArray = random.sample(args.echo, len(args.echo))
                for i in range(min(args.head_count,len(rArray))):
                    print(rArray[i])
    else:
        # Condition if --echo is not true
        # Specifically when echo flag is raised but no other arguments are given
        if args.echo != None and len(unknown)==0:
            print('')
            sys.exit(1)
        # Situation where echo flag is raised and arguments come after -e
        if args.echo != None:
            if len(args.echo)==0:
                edited_f = unknown
        if args.repeat:
            if args.head_count:
                # Randomly choose an arg for "head_count" number of times
                for i in range(args.head_count):
                    print (random.choice(edited_f))
            else:
                while (1 != 0):
                    print(random.choice(edited_f))
        else:
            rArray = random.sample(edited_f, len(edited_f))
            # If head count flag is enabled, without repeat, choose whichever is smallest
            # from range of input, number of args inputted, or head count
            if args.head_count:
                for i in range(min(args.head_count, int(bounds[1])-int(bounds[0])+1, len(edited_f))):
                    print(rArray[i])
            else:
                for i in range(len(edited_f)):
                    print(rArray[i])
if __name__ == "__main__":
    main()
