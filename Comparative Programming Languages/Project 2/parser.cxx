/* parser.c - a syntax analyzer system for simple
arithmetic expressions */
#include <stdio.h>
#include <ctype.h>
#include <string>
#include <map>
using namespace std;

/* Global declarations */
/* Variables */
int charClass;
char lexeme [100];
char nextChar;
int lexLen;
int nextToken;
FILE *in_fp;
float expValue;
string strStmt;

/* Function declarations */
void addChar();
void getChar();
void getNonBlank();
int lex();
float expr();
float term();
float factor();
void error(const char *name);
void stmt();
void stmtList();

/* Character classes */
#define LETTER 0
#define DIGIT 1
#define UNKNOWN 99

/* Token codes */
#define INT_LIT 10
#define IDENT 11
#define ASSIGN_OP 20
#define ADD_OP 21
#define SUB_OP 22
#define MULT_OP 23
#define DIV_OP 24
#define LEFT_PAREN 25
#define RIGHT_PAREN 26
#define SEMI_COLON 27
#define PRINT 28

map<string, float> varMap;

/******************************************************/
/* main driver */
int main(int argc, char **argv) {
  if (argc < 2) {
    printf("Usage: parser input_file\n");
    return -1;
  }
  /* Open the input data file and process its contents */
  if ((in_fp = fopen(argv[1], "r")) == NULL) {
    printf("ERROR - cannot open input_file: %s \n", argv[1]);
    return -2;
  }
  else {
    getChar();
    lex();
    stmtList();
    /*
    do {
      lex();
    } while (nextToken != EOF);
    */
    fclose(in_fp);
    return 0;
  }
}

/*****************************************************/
/* lookup - a function to lookup operators and parentheses
and return the token */
int lookup(char ch) {
  switch (ch) {
    case '(':
      addChar();
      nextToken = LEFT_PAREN;
      break;
    case ')':
      addChar();
      nextToken = RIGHT_PAREN;
      break;
    case '+':
      addChar();
      nextToken = ADD_OP;
      break;
    case '-':
      addChar();
      nextToken = SUB_OP;
      break;
    case '*':
      addChar();
      nextToken = MULT_OP;
      break;
    case '/':
      addChar();
      nextToken = DIV_OP;
      break;
    case '=':
      addChar();
      nextToken = ASSIGN_OP;
      break;
    case ';':
      addChar();
      nextToken = SEMI_COLON;
      break;
    default:
      addChar();
      nextToken = EOF;
      break;
  }
  return nextToken;
}

/*****************************************************/
/* addChar - a function to add nextChar to lexeme */
void addChar() {
  if (lexLen <= 98) {
    lexeme[lexLen++] = nextChar;
    lexeme[lexLen] = 0;
  }
  else {
    printf("Error - lexeme is too long \n");
  }
}

/*****************************************************/
/* getChar - a function to get the next character of
input and determine its character class */
void getChar() {
  if ((nextChar = getc(in_fp)) != EOF) {
    if (isalpha(nextChar))
      charClass = LETTER;
    else if (isdigit(nextChar))
      charClass = DIGIT;
    else
      charClass = UNKNOWN;
  }
  else {
    charClass = EOF;
  }
}

/*****************************************************/
/* getNonBlank - a function to call getChar until it
returns a non-whitespace character */
void getNonBlank() {
  while (isspace(nextChar))
    getChar();
}

int isPrint() {
  if (toupper(lexeme[0]) == 'P' &&
      toupper(lexeme[1]) == 'R' &&
      toupper(lexeme[2]) == 'I' &&
      toupper(lexeme[3]) == 'N' &&
      toupper(lexeme[4]) == 'T' &&
      lexeme[5] == 0)
    return 1;
  else
    return 0;
}

/*****************************************************/
/* lex - a simple lexical analyzer for arithmetic
expressions */
int lex() {
  lexLen = 0;
  getNonBlank();
  switch (charClass) {
    /* Parse identifiers */
    case LETTER:
      addChar();
      getChar();
      while (charClass == LETTER || charClass == DIGIT) {
        addChar();
        getChar();
      }
      if (isPrint()) {
        nextToken = PRINT;
      }
      else {
        nextToken = IDENT;
      }
      break;
    /* Parse integer literals */
    case DIGIT:
      addChar();
      getChar();
      while (charClass == DIGIT) {
        addChar();
        getChar();
      }
      nextToken = INT_LIT;
      break;
    /* Parentheses and operators */
    case UNKNOWN:
      lookup(nextChar);
      getChar();
      break;
    /* EOF */
    case EOF:
      nextToken = EOF;
      lexeme[0] = 'E';
      lexeme[1] = 'O';
      lexeme[2] = 'F';
      lexeme[3] = 0;
      break;
  } /* End of switch */
  /*
  printf("Next token is: %d, Next lexeme is %s\n",
          nextToken, lexeme);
  */
  strStmt.append(lexeme);
  strStmt.append(" ");
  if (nextToken == SEMI_COLON) {
    printf("%s\n", strStmt.c_str());
    strStmt = "";
  }
  return nextToken;
} /* End of function lex */

void updateVar(string var, float value) {
  varMap[var] = value;
}

bool getVarValue(string var, float& val) {
  map<string, float>::iterator it;
  it = varMap.find(var);
  if (it != varMap.end()) {
    val = it->second;
    return true;
  }
  else {
    val = -1;
    return false;
  }
}

/* stmtList
   <stmt-list> ::= empty | <stmt> { <stmt> } 
   */
void stmtList() {
  if (nextToken == EOF) {
    printf(">>> Empty .tiny file.\n");
  }
  else {
    while (nextToken != EOF) {
      stmt();
    }
  }
}

/* stmt
   <stmt> ::= id = <expr> ; |
              print <expr> ;
   */
void stmt() {
  if (nextToken == IDENT) {
    /* printf("%s\n",lexeme);*/
    string var = lexeme;
    lex();
    if (nextToken == ASSIGN_OP) {
      lex();
      expValue = expr();
      updateVar(var, expValue);
    }
  }
  else if (nextToken == PRINT) {
    lex();
    expValue = expr();
    if (nextToken == SEMI_COLON) {
      printf(">>> %f\n", expValue);
    }
  }
  if (nextToken == SEMI_COLON) {
    lex();
  }
  else {
    error("stmt():missing ';'.");
  }
}
 
/* expr
   Parses strings in the language generated by the rule:
   <expr> -> <term> {(+ | -) <term>}
   */
float expr() {
  float ret1, ret2;
  /* Parse the first term */
  ret1 = term();
  /* As long as the next token is + or -, get
     the next token and parse the next term */
  while (nextToken == ADD_OP || nextToken == SUB_OP) {
    int token = nextToken;
    lex();
    ret2 = term();
    if (token == ADD_OP) {
      ret1 += ret2;
    }
    else {
      ret1 -= ret2;
    }
  }
  return ret1;
} /* End of function expr */

/* term
   Parses strings in the language generated by the rule:
   <term> -> <factor> {(* | /) <factor>}
   */
float term() {
  float ret1, ret2;
  /* Parse the first factor */
  ret1 = factor();
  /* As long as the next token is * or /, get the
     next token and parse the next factor */
  while (nextToken == MULT_OP || nextToken == DIV_OP) {
    int token = nextToken;
    lex();
    ret2 = factor();
    if (token == MULT_OP) {
      ret1 *= ret2;
    }
    else {
      ret1 /= ret2;
    }
  }
  return ret1;
} /* End of function term */

/* factor
   Parses strings in the language generated by the rule:
   <factor> -> id | int_constant | ( <expr> )
   */
float factor() {
  /* Determine which RHS */
  if (nextToken == IDENT || nextToken == INT_LIT) {
    string var = lexeme;
    int token = nextToken;
    if (token == IDENT) {
      if (!getVarValue(var, expValue)) {
        string err = "factor() point 3: The identifier " + var + " is not defined";
	    error(err.c_str());
      }
    }
    else {
      expValue = atoi(var.c_str());
    }
    /* Get the next token */
    lex();
  }
  /* If the RHS is ( <expr>), call lex to pass over the
     left parenthesis, call expr, and check for the right
     parenthesis */
  else {
    if (nextToken == LEFT_PAREN) {
      lex();
      expValue = expr();
      if (nextToken == RIGHT_PAREN)
        lex();
      else
        error("factor() point 1");
    } /* End of if (nextToken == ... */
    /* It was not an id, an integer literal, or a left
       parenthesis */
    else
      error("factor() point 2");
  } /* End of else */
  return expValue;
} /* End of function factor */

void error(const char *name) {
  printf("Error: in %s\n", name); 
}

