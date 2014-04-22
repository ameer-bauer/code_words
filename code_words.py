#!/usr/bin/env python3
#----------------
#Name: code_words
#Version: 1.2.1
#Date: 2014-03-30
#----------------
#About the codex.txt file...
#The expected format of the file is as follows:
#CATEGORY(1)
#ITEM(1),ITEM(2),...,ITEM(N)
#CATEGORY(2)
#ITEM(1),ITEM(2),...,ITEM(N)
# .
# .
# .
#CATEGORY(N)
#ITEM(1),ITEM(2),...,ITEM(N)
#EOF

import os
import sys
import argparse
import random

#Setup all of the flags and options to be passed from the CLI
parser = argparse.ArgumentParser(add_help=False, description='Welcome to code_words version 1.2.1, a program which allows you to randomly generate a sequence of words.')
parser.add_argument("-h", action='store_true', help="Display the help page.")
parser.add_argument("-s", nargs='?', help="Use a custom seed for the random number generator.", metavar='seed')
parser.add_argument("-f", nargs='?', help="Use a custom reference file for code word generation.", metavar='filename')
group = parser.add_mutually_exclusive_group()
group.add_argument('-lc', action='store_true', help="List categories and indices from the reference file.")
group.add_argument('-lv', action='store_true', help="Verbosely list word categories from the reference file.")
parser.add_argument("-g", nargs='+', type=int, help="Generate a code word via a list of category index numbers.", metavar='#')
args = parser.parse_args()

if args.h :
    print('Introduction to code_words v1.2.1:')
    print('  The code_words program is a code word generator which allows you to randomly')
    print('  generate a sequence of words chosen from a reference file.  Feel free to add')
    print('  or remove words & categories as you like, or create your own reference file.')
    print('  The categories can be re-used as many times in the generation process, in any')
    print('  order, as you see fit.  The default reference file (codex.txt) is used if the')
    print('  -f flag is omitted.  The codex.txt file contains categories similar to those')
    print('  found in Charles Stross\' Laundry series.  Enjoy!')
    print('\nSYNTAX\n  python3 code_words.py [-h] [-f [filename]] [-lc | -lv] [-g # [# ...]]')
    print('\nARGUMENTS')
    print('  -h Displays this help page.')
    print('  -s <seed string> Utilize a user-defined seed for the random number generator.')
    print('  -f <filename> References <filename> instead of codex.txt for word lists.')
    print('  -lc List categories and indices from the reference file.')
    print('  -lv Verbosely list word categories from the reference file.')
    print('  -g {c1 c2 ... cN} Generates a code word via the listed category indices.')
    print('\nEXAMPLE\n  python3 code_words.py -g 0 7 2 8 ... cN')
    print('    Outputs the sequence of words \"w1 w2 w3 w4 ... wM\":')
    print('      Where w1 is chosen from category 0, w2 from category 7 ... to wM from')
    print('      category cN referenced from the file codex.txt.')
    print('\n  python3 code_words.py -f foo.txt -lc')
    print('    Lists the categories contained in foo.txt.')
    print('\n  python3 code_words.py -f foo.txt -g 3 2 5')
    print('    Outputs the sequence of words \"w1 w2 w3\":')
    print('      Where w1 is chosen from category 3, w2 from category 2 and w3 from')
    print('      category 5 referenced from the file foo.txt.')
    print('\n  python3 code_words.py -s abc123^!@#QWERTY -f foo.txt -g 3 2 5')
    print('    Outputs the sequence of words \"w1 w2 w3\":')
    print('      Where w1 is chosen from category 3, w2 from category 2 and w3 from')
    print('      category 5 referenced from the file foo.txt utilizing the seed')
    print('      "abc123^!@#QWERTY"; always yielding the same sequence of code')
    print('      words. This is useful for sharing a sequence of words with others.')
    print('      The recommended minimum seed length is 16 characters.')
    sys.exit()

code_list = []
file_name = 'codex.txt' #Set the default reference file name.

if args.f :
    file_name = args.f

try :
    for raw in open(file_name, encoding = 'utf-8', mode = 'r'):
        line = raw[:-1] #Get rid of new line characters
        if ',' in line : #Split strings with CSV into a list
            code_list.append(line.split(','))
        else :
            code_list.append(line) #Set strings w/o a CSV to be a single string
    list_count = len(code_list) #Count the lines from codex.txt; it should be even

    if list_count % 2 != 0 :
        sys.exit(1) #The following except will catch this error
except :
    print('ERROR: Either can\'t find the file [',file_name,'] or incorrect reference file format.')
    sys.exit(1)

if args.lc :
    #Print the even lines of the codex.txt file, which should be the categories
    print('Listing category indices from reference file [', file_name,']\n')
    for x in range(list_count) :
        if x % 2 == 0 :
            print(int(x / 2), code_list[x])
    sys.exit()

if args.lv :
    print('Listing categories verbosely from reference file [', file_name,']')
    for x in range(list_count) :
        if x % 2 == 0 :
            print('\n', int(x / 2), end = ' ', sep = '')
        print(code_list[x])
    sys.exit()

if args.g :
    print('Code word generation from reference file [',file_name,']\n')
    for x in args.g : #Gen a random number and pick aa code word for each category index
        try :
            y = int(x) * 2
            if y < list_count and y >= 0 :
                if args.s :
                    s = args.s
                else :
                    s = os.urandom(16) #gen 16 bytes of crypto-sound sudo-random data
                random.seed(s)  #Initialize the random number generator with of random data
                l = len(code_list[y+1]) #Remember that lists count 0 -> x not 1 -> x hence the l-1 in r
                r = random.randint(0,l-1)
                print(code_list[y+1][r], end = ' ')
            else :
                sys.exit(1) #the following except will catch this error
        except :
            print('\nERROR: Invalid category index [', x, '] used.') 
            print('Please check available category indices with the -lc flag.')
            sys.exit(2)
    print('\n', end = '')
    sys.exit()

parser.print_help()
