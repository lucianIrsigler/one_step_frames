/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

#ifndef YY_TPTP_TPTPPARSER_H_INCLUDED
# define YY_TPTP_TPTPPARSER_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int tptp_debug;
#endif

/* Token kinds.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    YYEMPTY = -2,
    YYEOF = 0,                     /* "end of file"  */
    YYerror = 256,                 /* error  */
    YYUNDEF = 257,                 /* "invalid token"  */
    AMPERSAND = 258,               /* AMPERSAND  */
    COLON = 259,                   /* COLON  */
    COMMA = 260,                   /* COMMA  */
    EQUALS = 261,                  /* EQUALS  */
    EQUALS_GREATER = 262,          /* EQUALS_GREATER  */
    EXCLAMATION = 263,             /* EXCLAMATION  */
    EXCLAMATION_EQUALS = 264,      /* EXCLAMATION_EQUALS  */
    LBRKT = 265,                   /* LBRKT  */
    LESS_EQUALS = 266,             /* LESS_EQUALS  */
    LESS_EQUALS_GREATER = 267,     /* LESS_EQUALS_GREATER  */
    LESS_TILDE_GREATER = 268,      /* LESS_TILDE_GREATER  */
    LPAREN = 269,                  /* LPAREN  */
    PERIOD = 270,                  /* PERIOD  */
    QUESTION = 271,                /* QUESTION  */
    RBRKT = 272,                   /* RBRKT  */
    RPAREN = 273,                  /* RPAREN  */
    TILDE = 274,                   /* TILDE  */
    TILDE_AMPERSAND = 275,         /* TILDE_AMPERSAND  */
    TILDE_VLINE = 276,             /* TILDE_VLINE  */
    VLINE = 277,                   /* VLINE  */
    _DLR_cnf = 278,                /* _DLR_cnf  */
    _DLR_fof = 279,                /* _DLR_fof  */
    _DLR_fot = 280,                /* _DLR_fot  */
    _LIT_cnf = 281,                /* _LIT_cnf  */
    _LIT_fof = 282,                /* _LIT_fof  */
    _LIT_include = 283,            /* _LIT_include  */
    comment_line = 284,            /* comment_line  */
    distinct_object = 285,         /* distinct_object  */
    dollar_dollar_word = 286,      /* dollar_dollar_word  */
    dollar_word = 287,             /* dollar_word  */
    lower_word = 288,              /* lower_word  */
    real = 289,                    /* real  */
    signed_integer = 290,          /* signed_integer  */
    single_quoted = 291,           /* single_quoted  */
    unsigned_integer = 292,        /* unsigned_integer  */
    upper_word = 293,              /* upper_word  */
    unrecognized = 294             /* unrecognized  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 119 "tptpparser.y"
  
  char*     string;
  SYMBOL    symbol;
  TERM      term;
  LIST      list;
  BOOL      bool;

#line 111 "tptpparser.h"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE tptp_lval;


int tptp_parse (void);


#endif /* !YY_TPTP_TPTPPARSER_H_INCLUDED  */
