"""
Djesse Jackson 2712207
Project 2
parser_2712207.py
A syntax analyzer system for simple arithmetic expressions based on parser.c
"""

import sys

# Global declarations
# Variables
charClass = None
lexeme = [None] * 100
nextChar = None
lexLen = None
nextToken = None
in_fp = None
expValue = None
strStmt = ""

# Character Classes
LETTER = 0
DIGIT = 1
UNKNOWN = 99

# Token codes
INT_LIT = 10
IDENT = 11
ASSIGN_OP = 20
ADD_OP = 21
SUB_OP = 22
MULT_OP = 23
DIV_OP = 24
LEFT_PAREN = 25
RIGHT_PAREN = 26
SEMI_COLON = 27
PRINT = 28
EOF = ''

varMap = {}
# Main driver

def main():

    if len(sys.argv) < 2:
        print("Usage: parser input_file")
        return -1
    global in_fp
    in_fp = open(sys.argv[1], "r") 
    if in_fp == None:
        print("ERROR - Cannot open input file: " + sys.argv[1])
        return -2
    else:
        getChar()
        lex()
        stmtList()

        """
        do
            lex()
        while (nextToken != EOF)
        """
        in_fp.close()
        return 0
    
# a function to lookup operators and parenthesis and returns the token
def lookup(ch):
    global nextToken
    match ch:
        case '(':
            addChar()
            nextToken = LEFT_PAREN
        case ')':
            addChar()
            nextToken = RIGHT_PAREN
        case '+':
            addChar()
            nextToken = ADD_OP
        case '-':
            addChar()
            nextToken = SUB_OP
        case '*':
            addChar()
            nextToken = MULT_OP
        case '/':
            addChar()
            nextToken = DIV_OP
        case '=':
            addChar()
            nextToken = ASSIGN_OP
        case ';':
            addChar()
            nextToken = SEMI_COLON
        case _:
            addChar()
            nextToken = EOF
    return nextToken

# a function to add nextChar to lexeme
def addChar():

    global lexLen
    global lexeme
    global nextChar

    if lexLen <= 98:
        lexeme[lexLen] = nextChar
        lexLen+= 1
        lexeme[lexLen] = ''
    else:
        print("Error - lexeme is too long ")

# A function to get the next character of input and determine its character class
def getChar():

    global nextChar
    global charClass

    nextChar = in_fp.read(1)
    if nextChar != EOF:
        if nextChar.isalpha():
            charClass = LETTER
        elif nextChar.isdigit():
            charClass = DIGIT
        else:
            charClass = UNKNOWN
    else:
        charClass = EOF

# a function to call getChar until it returns a non-whitespace character
def getNonBlank():

    while nextChar.isspace():
        getChar()

def isPrint():
    if (lexeme[0].upper() == 'P' and lexeme[1].upper() == 'R' and lexeme[2].upper() == 'I' and lexeme[3].upper() == 'N' and lexeme[4].upper() == 'T' and lexeme[5] == ''):
        return 1
    else:
        return 0

# Lex: a simple lexical analyzer for arithmetic expressions
def lex():

    global lexLen
    global nextToken
    global DIGIT
    global LETTER
    global UNKNOWN
    global EOF
    global charClass
    global strStmt
    
    lexLen = 0
    getNonBlank()
    match charClass:
        # Parse identifiers
        case int(LETTER):
            addChar()
            getChar()
            while (charClass == LETTER or charClass == DIGIT):
                addChar()
                getChar()
            if(isPrint()):
                nextToken = PRINT
            else:
                nextToken = IDENT
        # Parse integer literals
        case int(DIGIT):
            addChar()
            getChar()
            while(charClass == DIGIT):
                addChar()
                getChar()
            nextToken = INT_LIT
        # Parenthesis and operators
        case int(UNKNOWN):
            lookup(nextChar)
            getChar()
        case '':
            nextToken = EOF
            lexeme[0] = 'E'
            lexeme[1] = 'O'
            lexeme[2] = 'F'
            lexeme[3] = None
    for item in lexeme:
        if item != '':
            strStmt += str(item)
        else:
            break
    strStmt += " "
    if (nextToken == SEMI_COLON):
        print(str(strStmt))
        strStmt = ""
    return nextToken

def updateVar(var, value):
    global varMap
    varMap[var] = value

def getVarValue(var):
    global varMap
    it = varMap.get(var, -1)
    if (it != -1):
        return it
    else:
        return False

def stmtList():
    global nextToken
    if (nextToken == EOF):
        print(">>> Empty .tiny file.")
    else:
        while (nextToken != EOF):
            stmt()

def stmt():
    var = ""
    global lexeme
    global nextToken

    if (nextToken == IDENT):
        for item in lexeme:
            if item != '':
                var += str(item)
            else:
                break
        lex()
        if(nextToken == ASSIGN_OP):
            lex()
            expValue = expr()
            updateVar(var, expValue)
    elif(nextToken == PRINT):
        lex()
        expValue = expr()
        if (nextToken == SEMI_COLON):
            print(">>> " + expValue)
    if (nextToken == SEMI_COLON):
        lex()
    else:
        error("stmt():missing ';'." + str(nextToken) + str(lexeme))

def expr():
    ret1 = term()
    while (nextToken == ADD_OP or nextToken == SUB_OP):
        token = nextToken
        lex()
        ret2 = term()
        if (token == ADD_OP):
            ret1 += ret2
        else:
            ret1 -= ret2
    return ret1

def term():
    ret1 = factor()
    while (nextToken == MULT_OP or nextToken == DIV_OP):
        token = nextToken
        lex()
        ret2 = factor()
        if(token == MULT_OP):
            ret1 *= ret2
        else:
            ret1 /= ret2
    return ret1

def factor():

    global expValue
    var = ""
    if (nextToken == IDENT or nextToken == INT_LIT):
        for item in lexeme:
            if item != '':
                var += str(item)
            else:
                break
        token = nextToken
        if (token == IDENT):
            if(getVarValue(var) == False):
                err = "factor() point 3: The identifier " + var + " is not defined"
                print(lexeme)
                error(err)
        else:
            expValue = int(var)
        lex()
    else:
        if (nextToken == LEFT_PAREN):
            lex()
            expValue = expr()
            if(nextToken == RIGHT_PAREN):
                lex()
            else:
                error("factor() point 1")
        else:
            error("factor() point 2")
    return expValue

def error(name):
    print("Error: in " + name)


if __name__ == '__main__':
    main()