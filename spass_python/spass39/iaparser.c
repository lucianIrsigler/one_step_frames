/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison implementation for Yacc-like parsers in C

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

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Identify Bison output, and Bison version.  */
#define YYBISON 30802

/* Bison version string.  */
#define YYBISON_VERSION "3.8.2"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 0

/* Push parsers.  */
#define YYPUSH 0

/* Pull parsers.  */
#define YYPULL 1


/* Substitute the variable and function names.  */
#define yyparse         ia_parse
#define yylex           ia_lex
#define yyerror         ia_error
#define yydebug         ia_debug
#define yynerrs         ia_nerrs
#define yylval          ia_lval
#define yychar          ia_char

/* First part of user prologue.  */
#line 41 "iaparser.y"


#include "flags.h"
#include "ia.h"
#include "symbol.h"
#include "term.h"
#include "foldfg.h"
#include "clause.h"

extern NAT dfg_LINENUMBER;    /* Defined in dfgparser.y */
LIST       ia_PROOFREQUEST;   /* A pair! */
FLAGSTORE  ia_FLAGS;

void yyerror(const char*);
int  yylex(void);		/* Defined in iascanner.l */

static SYMBOL ia_Symbol(char*, NAT);
static TERM   ia_CreateQuantifier(SYMBOL, LIST, TERM);

 void  ia_StringFree(char* String)
{
  memory_Free(String, sizeof(char)*(strlen(String)+1));
}

 TERM ia_TermCreate(char* Name, LIST Arguments)
/* Look up the symbol, check its arity and create the term */
{
  return term_Create(ia_Symbol(Name,list_Length(Arguments)), Arguments);
}

/**************************************************************/
/* Functions to check the arity of symbols                    */
/**************************************************************/

static void ia_SymCheck(SYMBOL, NAT);

/**************************************************************/
/* Functions that handle variable names                       */
/**************************************************************/

/* List of quantified variables in the current input formula. */
/* This list is used to find symbols that by mistake weren't  */
/* declared in the symbol declaration section                 */
/* --> free variables                                         */
/* This is a list of lists, since each time a quantifier is   */
/* reached, a new list is added to the global list.           */
static LIST ia_VARLIST;
static BOOL ia_VARDECL;

static void   ia_VarStart(void);
static void   ia_VarStop(void);
static void   ia_VarBacktrack(void);
static void   ia_VarCheck(void);
static SYMBOL ia_VarLookup(char*);

#define YY_INPUT(buf,result,max_size) \
{ \
  int c = getc(ia_in); \
  result = (c == EOF) ? YY_NULL : (buf[0] = c, 1); \
}

#define YYERROR_VERBOSE


#line 143 "iaparser.c"

# ifndef YY_CAST
#  ifdef __cplusplus
#   define YY_CAST(Type, Val) static_cast<Type> (Val)
#   define YY_REINTERPRET_CAST(Type, Val) reinterpret_cast<Type> (Val)
#  else
#   define YY_CAST(Type, Val) ((Type) (Val))
#   define YY_REINTERPRET_CAST(Type, Val) ((Type) (Val))
#  endif
# endif
# ifndef YY_NULLPTR
#  if defined __cplusplus
#   if 201103L <= __cplusplus
#    define YY_NULLPTR nullptr
#   else
#    define YY_NULLPTR 0
#   endif
#  else
#   define YY_NULLPTR ((void*)0)
#  endif
# endif

#include "iaparser.h"
/* Symbol kind.  */
enum yysymbol_kind_t
{
  YYSYMBOL_YYEMPTY = -2,
  YYSYMBOL_YYEOF = 0,                      /* "end of file"  */
  YYSYMBOL_YYerror = 1,                    /* error  */
  YYSYMBOL_YYUNDEF = 2,                    /* "invalid token"  */
  YYSYMBOL_IA_AND = 3,                     /* IA_AND  */
  YYSYMBOL_IA_EQUAL = 4,                   /* IA_EQUAL  */
  YYSYMBOL_IA_EQUIV = 5,                   /* IA_EQUIV  */
  YYSYMBOL_IA_EXISTS = 6,                  /* IA_EXISTS  */
  YYSYMBOL_IA_FALSE = 7,                   /* IA_FALSE  */
  YYSYMBOL_IA_FORALL = 8,                  /* IA_FORALL  */
  YYSYMBOL_IA_IMPLIED = 9,                 /* IA_IMPLIED  */
  YYSYMBOL_IA_IMPLIES = 10,                /* IA_IMPLIES  */
  YYSYMBOL_IA_NOT = 11,                    /* IA_NOT  */
  YYSYMBOL_IA_OR = 12,                     /* IA_OR  */
  YYSYMBOL_IA_PROVE = 13,                  /* IA_PROVE  */
  YYSYMBOL_IA_TRUE = 14,                   /* IA_TRUE  */
  YYSYMBOL_IA_NUM = 15,                    /* IA_NUM  */
  YYSYMBOL_IA_ID = 16,                     /* IA_ID  */
  YYSYMBOL_17_ = 17,                       /* '('  */
  YYSYMBOL_18_ = 18,                       /* ','  */
  YYSYMBOL_19_ = 19,                       /* ')'  */
  YYSYMBOL_20_ = 20,                       /* '.'  */
  YYSYMBOL_21_ = 21,                       /* '['  */
  YYSYMBOL_22_ = 22,                       /* ']'  */
  YYSYMBOL_YYACCEPT = 23,                  /* $accept  */
  YYSYMBOL_proofrequest = 24,              /* proofrequest  */
  YYSYMBOL_termlist = 25,                  /* termlist  */
  YYSYMBOL_term = 26,                      /* term  */
  YYSYMBOL_27_1 = 27,                      /* $@1  */
  YYSYMBOL_28_2 = 28,                      /* $@2  */
  YYSYMBOL_29_3 = 29,                      /* $@3  */
  YYSYMBOL_30_4 = 30,                      /* $@4  */
  YYSYMBOL_binsymbol = 31,                 /* binsymbol  */
  YYSYMBOL_nsymbol = 32,                   /* nsymbol  */
  YYSYMBOL_quantsymbol = 33,               /* quantsymbol  */
  YYSYMBOL_id = 34,                        /* id  */
  YYSYMBOL_qtermlist = 35,                 /* qtermlist  */
  YYSYMBOL_qterm = 36,                     /* qterm  */
  YYSYMBOL_labellistopt = 37,              /* labellistopt  */
  YYSYMBOL_labellist = 38                  /* labellist  */
};
typedef enum yysymbol_kind_t yysymbol_kind_t;




#ifdef short
# undef short
#endif

/* On compilers that do not define __PTRDIFF_MAX__ etc., make sure
   <limits.h> and (if available) <stdint.h> are included
   so that the code can choose integer types of a good width.  */

#ifndef __PTRDIFF_MAX__
# include <limits.h> /* INFRINGES ON USER NAME SPACE */
# if defined __STDC_VERSION__ && 199901 <= __STDC_VERSION__
#  include <stdint.h> /* INFRINGES ON USER NAME SPACE */
#  define YY_STDINT_H
# endif
#endif

/* Narrow types that promote to a signed type and that can represent a
   signed or unsigned integer of at least N bits.  In tables they can
   save space and decrease cache pressure.  Promoting to a signed type
   helps avoid bugs in integer arithmetic.  */

#ifdef __INT_LEAST8_MAX__
typedef __INT_LEAST8_TYPE__ yytype_int8;
#elif defined YY_STDINT_H
typedef int_least8_t yytype_int8;
#else
typedef signed char yytype_int8;
#endif

#ifdef __INT_LEAST16_MAX__
typedef __INT_LEAST16_TYPE__ yytype_int16;
#elif defined YY_STDINT_H
typedef int_least16_t yytype_int16;
#else
typedef short yytype_int16;
#endif

/* Work around bug in HP-UX 11.23, which defines these macros
   incorrectly for preprocessor constants.  This workaround can likely
   be removed in 2023, as HPE has promised support for HP-UX 11.23
   (aka HP-UX 11i v2) only through the end of 2022; see Table 2 of
   <https://h20195.www2.hpe.com/V2/getpdf.aspx/4AA4-7673ENW.pdf>.  */
#ifdef __hpux
# undef UINT_LEAST8_MAX
# undef UINT_LEAST16_MAX
# define UINT_LEAST8_MAX 255
# define UINT_LEAST16_MAX 65535
#endif

#if defined __UINT_LEAST8_MAX__ && __UINT_LEAST8_MAX__ <= __INT_MAX__
typedef __UINT_LEAST8_TYPE__ yytype_uint8;
#elif (!defined __UINT_LEAST8_MAX__ && defined YY_STDINT_H \
       && UINT_LEAST8_MAX <= INT_MAX)
typedef uint_least8_t yytype_uint8;
#elif !defined __UINT_LEAST8_MAX__ && UCHAR_MAX <= INT_MAX
typedef unsigned char yytype_uint8;
#else
typedef short yytype_uint8;
#endif

#if defined __UINT_LEAST16_MAX__ && __UINT_LEAST16_MAX__ <= __INT_MAX__
typedef __UINT_LEAST16_TYPE__ yytype_uint16;
#elif (!defined __UINT_LEAST16_MAX__ && defined YY_STDINT_H \
       && UINT_LEAST16_MAX <= INT_MAX)
typedef uint_least16_t yytype_uint16;
#elif !defined __UINT_LEAST16_MAX__ && USHRT_MAX <= INT_MAX
typedef unsigned short yytype_uint16;
#else
typedef int yytype_uint16;
#endif

#ifndef YYPTRDIFF_T
# if defined __PTRDIFF_TYPE__ && defined __PTRDIFF_MAX__
#  define YYPTRDIFF_T __PTRDIFF_TYPE__
#  define YYPTRDIFF_MAXIMUM __PTRDIFF_MAX__
# elif defined PTRDIFF_MAX
#  ifndef ptrdiff_t
#   include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  endif
#  define YYPTRDIFF_T ptrdiff_t
#  define YYPTRDIFF_MAXIMUM PTRDIFF_MAX
# else
#  define YYPTRDIFF_T long
#  define YYPTRDIFF_MAXIMUM LONG_MAX
# endif
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif defined __STDC_VERSION__ && 199901 <= __STDC_VERSION__
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned
# endif
#endif

#define YYSIZE_MAXIMUM                                  \
  YY_CAST (YYPTRDIFF_T,                                 \
           (YYPTRDIFF_MAXIMUM < YY_CAST (YYSIZE_T, -1)  \
            ? YYPTRDIFF_MAXIMUM                         \
            : YY_CAST (YYSIZE_T, -1)))

#define YYSIZEOF(X) YY_CAST (YYPTRDIFF_T, sizeof (X))


/* Stored state numbers (used for stacks). */
typedef yytype_int8 yy_state_t;

/* State numbers in computations.  */
typedef int yy_state_fast_t;

#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(Msgid) dgettext ("bison-runtime", Msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(Msgid) Msgid
# endif
#endif


#ifndef YY_ATTRIBUTE_PURE
# if defined __GNUC__ && 2 < __GNUC__ + (96 <= __GNUC_MINOR__)
#  define YY_ATTRIBUTE_PURE __attribute__ ((__pure__))
# else
#  define YY_ATTRIBUTE_PURE
# endif
#endif

#ifndef YY_ATTRIBUTE_UNUSED
# if defined __GNUC__ && 2 < __GNUC__ + (7 <= __GNUC_MINOR__)
#  define YY_ATTRIBUTE_UNUSED __attribute__ ((__unused__))
# else
#  define YY_ATTRIBUTE_UNUSED
# endif
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YY_USE(E) ((void) (E))
#else
# define YY_USE(E) /* empty */
#endif

/* Suppress an incorrect diagnostic about yylval being uninitialized.  */
#if defined __GNUC__ && ! defined __ICC && 406 <= __GNUC__ * 100 + __GNUC_MINOR__
# if __GNUC__ * 100 + __GNUC_MINOR__ < 407
#  define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN                           \
    _Pragma ("GCC diagnostic push")                                     \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")
# else
#  define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN                           \
    _Pragma ("GCC diagnostic push")                                     \
    _Pragma ("GCC diagnostic ignored \"-Wuninitialized\"")              \
    _Pragma ("GCC diagnostic ignored \"-Wmaybe-uninitialized\"")
# endif
# define YY_IGNORE_MAYBE_UNINITIALIZED_END      \
    _Pragma ("GCC diagnostic pop")
#else
# define YY_INITIAL_VALUE(Value) Value
#endif
#ifndef YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
# define YY_IGNORE_MAYBE_UNINITIALIZED_END
#endif
#ifndef YY_INITIAL_VALUE
# define YY_INITIAL_VALUE(Value) /* Nothing. */
#endif

#if defined __cplusplus && defined __GNUC__ && ! defined __ICC && 6 <= __GNUC__
# define YY_IGNORE_USELESS_CAST_BEGIN                          \
    _Pragma ("GCC diagnostic push")                            \
    _Pragma ("GCC diagnostic ignored \"-Wuseless-cast\"")
# define YY_IGNORE_USELESS_CAST_END            \
    _Pragma ("GCC diagnostic pop")
#endif
#ifndef YY_IGNORE_USELESS_CAST_BEGIN
# define YY_IGNORE_USELESS_CAST_BEGIN
# define YY_IGNORE_USELESS_CAST_END
#endif


#define YY_ASSERT(E) ((void) (0 && (E)))

#if !defined yyoverflow

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_USE_ALLOCA
#  if YYSTACK_USE_ALLOCA
#   ifdef __GNUC__
#    define YYSTACK_ALLOC __builtin_alloca
#   elif defined __BUILTIN_VA_ARG_INCR
#    include <alloca.h> /* INFRINGES ON USER NAME SPACE */
#   elif defined _AIX
#    define YYSTACK_ALLOC __alloca
#   elif defined _MSC_VER
#    include <malloc.h> /* INFRINGES ON USER NAME SPACE */
#    define alloca _alloca
#   else
#    define YYSTACK_ALLOC alloca
#    if ! defined _ALLOCA_H && ! defined EXIT_SUCCESS
#     include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
      /* Use EXIT_SUCCESS as a witness for stdlib.h.  */
#     ifndef EXIT_SUCCESS
#      define EXIT_SUCCESS 0
#     endif
#    endif
#   endif
#  endif
# endif

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's 'empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (0)
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined EXIT_SUCCESS \
       && ! ((defined YYMALLOC || defined malloc) \
             && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef EXIT_SUCCESS
#    define EXIT_SUCCESS 0
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined EXIT_SUCCESS
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined EXIT_SUCCESS
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* !defined yyoverflow */

#if (! defined yyoverflow \
     && (! defined __cplusplus \
         || (defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yy_state_t yyss_alloc;
  YYSTYPE yyvs_alloc;
};

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (YYSIZEOF (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (YYSIZEOF (yy_state_t) + YYSIZEOF (YYSTYPE)) \
      + YYSTACK_GAP_MAXIMUM)

# define YYCOPY_NEEDED 1

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack_alloc, Stack)                           \
    do                                                                  \
      {                                                                 \
        YYPTRDIFF_T yynewbytes;                                         \
        YYCOPY (&yyptr->Stack_alloc, Stack, yysize);                    \
        Stack = &yyptr->Stack_alloc;                                    \
        yynewbytes = yystacksize * YYSIZEOF (*Stack) + YYSTACK_GAP_MAXIMUM; \
        yyptr += yynewbytes / YYSIZEOF (*yyptr);                        \
      }                                                                 \
    while (0)

#endif

#if defined YYCOPY_NEEDED && YYCOPY_NEEDED
/* Copy COUNT objects from SRC to DST.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(Dst, Src, Count) \
      __builtin_memcpy (Dst, Src, YY_CAST (YYSIZE_T, (Count)) * sizeof (*(Src)))
#  else
#   define YYCOPY(Dst, Src, Count)              \
      do                                        \
        {                                       \
          YYPTRDIFF_T yyi;                      \
          for (yyi = 0; yyi < (Count); yyi++)   \
            (Dst)[yyi] = (Src)[yyi];            \
        }                                       \
      while (0)
#  endif
# endif
#endif /* !YYCOPY_NEEDED */

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  4
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   83

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  23
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  16
/* YYNRULES -- Number of rules.  */
#define YYNRULES  36
/* YYNSTATES -- Number of states.  */
#define YYNSTATES  77

/* YYMAXUTOK -- Last valid token kind.  */
#define YYMAXUTOK   271


/* YYTRANSLATE(TOKEN-NUM) -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex, with out-of-bounds checking.  */
#define YYTRANSLATE(YYX)                                \
  (0 <= (YYX) && (YYX) <= YYMAXUTOK                     \
   ? YY_CAST (yysymbol_kind_t, yytranslate[YYX])        \
   : YYSYMBOL_YYUNDEF)

/* YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to TOKEN-NUM
   as returned by yylex.  */
static const yytype_int8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
      17,    19,     2,     2,    18,     2,    20,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,    21,     2,    22,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16
};

#if YYDEBUG
/* YYRLINE[YYN] -- Source line where rule number YYN was defined.  */
static const yytype_uint8 yyrline[] =
{
       0,   129,   129,   130,   142,   143,   146,   147,   148,   149,
     151,   153,   155,   157,   158,   157,   163,   164,   163,   172,
     173,   174,   175,   178,   179,   182,   183,   186,   187,   190,
     191,   194,   204,   225,   226,   229,   230
};
#endif

/** Accessing symbol of state STATE.  */
#define YY_ACCESSING_SYMBOL(State) YY_CAST (yysymbol_kind_t, yystos[State])

#if YYDEBUG || 0
/* The user-facing name of the symbol whose (internal) number is
   YYSYMBOL.  No bounds checking.  */
static const char *yysymbol_name (yysymbol_kind_t yysymbol) YY_ATTRIBUTE_UNUSED;

/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "\"end of file\"", "error", "\"invalid token\"", "IA_AND", "IA_EQUAL",
  "IA_EQUIV", "IA_EXISTS", "IA_FALSE", "IA_FORALL", "IA_IMPLIED",
  "IA_IMPLIES", "IA_NOT", "IA_OR", "IA_PROVE", "IA_TRUE", "IA_NUM",
  "IA_ID", "'('", "','", "')'", "'.'", "'['", "']'", "$accept",
  "proofrequest", "termlist", "term", "$@1", "$@2", "$@3", "$@4",
  "binsymbol", "nsymbol", "quantsymbol", "id", "qtermlist", "qterm",
  "labellistopt", "labellist", YY_NULLPTR
};

static const char *
yysymbol_name (yysymbol_kind_t yysymbol)
{
  return yytname[yysymbol];
}
#endif

#define YYPACT_NINF (-29)

#define yypact_value_is_default(Yyn) \
  ((Yyn) == YYPACT_NINF)

#define YYTABLE_NINF (-1)

#define yytable_value_is_error(Yyn) \
  0

/* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
   STATE-NUM.  */
static const yytype_int8 yypact[] =
{
     -12,    12,    35,     0,   -29,   -29,   -29,   -29,   -29,   -29,
     -29,   -29,   -29,    19,   -29,   -29,   -29,   -29,    20,    22,
      40,    41,    42,     0,    31,     0,     0,    43,    39,    18,
       8,    38,    44,     7,   -29,   -29,   -29,     9,   -29,   -29,
     -29,    -5,    46,     0,     0,   -29,    16,    16,   -29,    16,
     -29,    47,    48,   -29,    53,    45,   -29,    45,   -29,    51,
     -29,    16,    16,    50,    52,   -29,    54,   -29,    57,    58,
     -29,     0,     0,    59,    60,   -29,   -29
};

/* YYDEFACT[STATE-NUM] -- Default reduction number in state STATE-NUM.
   Performed when YYTABLE does not specify something else to do.  Zero
   means the default is an error.  */
static const yytype_int8 yydefact[] =
{
       2,     0,     0,     0,     1,    23,    19,    20,    25,     8,
      26,    21,    22,     0,    24,     7,    28,    27,     0,     0,
       0,     0,     6,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     4,    13,    16,     0,     9,    33,
      35,     0,     0,     0,     0,    11,     0,     0,    12,     0,
      34,     0,     0,     5,    31,    14,    29,    17,    36,     0,
      10,     0,     0,     0,     0,     3,     0,    30,     0,     0,
      32,     0,     0,     0,     0,    15,    18
};

/* YYPGOTO[NTERM-NUM].  */
static const yytype_int8 yypgoto[] =
{
     -29,   -29,    37,    -3,   -29,   -29,   -29,   -29,   -29,   -29,
     -29,   -28,    30,    21,   -29,   -29
};

/* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int8 yydefgoto[] =
{
       0,     2,    33,    34,    46,    63,    47,    64,    19,    20,
      21,    22,    55,    56,    31,    41
};

/* YYTABLE[YYPACT[STATE-NUM]] -- What to do in state STATE-NUM.  If
   positive, shift that token.  If negative, reduce the rule whose
   number is the opposite.  If YYTABLE_NINF, syntax error.  */
static const yytype_int8 yytable[] =
{
      18,     1,    40,     5,     6,     7,     8,     9,    10,    11,
      12,    13,    14,    49,    15,    16,    17,    50,    54,    54,
      29,    58,    32,    16,    17,    44,    45,    44,    48,     3,
      39,    16,    17,    66,    54,     4,    23,    38,    24,    25,
      52,    53,     5,     6,     7,     8,     9,    10,    11,    12,
      13,    14,    30,    15,    16,    17,    42,    26,    27,    28,
      36,    51,    43,    62,    35,    37,    59,    60,    73,    74,
      61,    65,    68,    70,    69,    71,    72,    57,    75,    76,
       0,     0,     0,    67
};

static const yytype_int8 yycheck[] =
{
       3,    13,    30,     3,     4,     5,     6,     7,     8,     9,
      10,    11,    12,    18,    14,    15,    16,    22,    46,    47,
      23,    49,    25,    15,    16,    18,    19,    18,    19,    17,
      22,    15,    16,    61,    62,     0,    17,    19,    18,    17,
      43,    44,     3,     4,     5,     6,     7,     8,     9,    10,
      11,    12,    21,    14,    15,    16,    18,    17,    17,    17,
      21,    15,    18,    18,    21,    28,    19,    19,    71,    72,
      17,    20,    22,    19,    22,    18,    18,    47,    19,    19,
      -1,    -1,    -1,    62
};

/* YYSTOS[STATE-NUM] -- The symbol kind of the accessing symbol of
   state STATE-NUM.  */
static const yytype_int8 yystos[] =
{
       0,    13,    24,    17,     0,     3,     4,     5,     6,     7,
       8,     9,    10,    11,    12,    14,    15,    16,    26,    31,
      32,    33,    34,    17,    18,    17,    17,    17,    17,    26,
      21,    37,    26,    25,    26,    21,    21,    25,    19,    22,
      34,    38,    18,    18,    18,    19,    27,    29,    19,    18,
      22,    15,    26,    26,    34,    35,    36,    35,    34,    19,
      19,    17,    18,    28,    30,    20,    34,    36,    22,    22,
      19,    18,    18,    26,    26,    19,    19
};

/* YYR1[RULE-NUM] -- Symbol kind of the left-hand side of rule RULE-NUM.  */
static const yytype_int8 yyr1[] =
{
       0,    23,    24,    24,    25,    25,    26,    26,    26,    26,
      26,    26,    26,    27,    28,    26,    29,    30,    26,    31,
      31,    31,    31,    32,    32,    33,    33,    34,    34,    35,
      35,    36,    36,    37,    37,    38,    38
};

/* YYR2[RULE-NUM] -- Number of symbols on the right-hand side of rule RULE-NUM.  */
static const yytype_int8 yyr2[] =
{
       0,     2,     0,     9,     1,     3,     1,     1,     1,     4,
       6,     4,     4,     0,     0,    10,     0,     0,    10,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       3,     1,     4,     2,     3,     1,     3
};


enum { YYENOMEM = -2 };

#define yyerrok         (yyerrstatus = 0)
#define yyclearin       (yychar = YYEMPTY)

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab
#define YYNOMEM         goto yyexhaustedlab


#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)                                    \
  do                                                              \
    if (yychar == YYEMPTY)                                        \
      {                                                           \
        yychar = (Token);                                         \
        yylval = (Value);                                         \
        YYPOPSTACK (yylen);                                       \
        yystate = *yyssp;                                         \
        goto yybackup;                                            \
      }                                                           \
    else                                                          \
      {                                                           \
        yyerror (YY_("syntax error: cannot back up")); \
        YYERROR;                                                  \
      }                                                           \
  while (0)

/* Backward compatibility with an undocumented macro.
   Use YYerror or YYUNDEF. */
#define YYERRCODE YYUNDEF


/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)                        \
do {                                            \
  if (yydebug)                                  \
    YYFPRINTF Args;                             \
} while (0)




# define YY_SYMBOL_PRINT(Title, Kind, Value, Location)                    \
do {                                                                      \
  if (yydebug)                                                            \
    {                                                                     \
      YYFPRINTF (stderr, "%s ", Title);                                   \
      yy_symbol_print (stderr,                                            \
                  Kind, Value); \
      YYFPRINTF (stderr, "\n");                                           \
    }                                                                     \
} while (0)


/*-----------------------------------.
| Print this symbol's value on YYO.  |
`-----------------------------------*/

static void
yy_symbol_value_print (FILE *yyo,
                       yysymbol_kind_t yykind, YYSTYPE const * const yyvaluep)
{
  FILE *yyoutput = yyo;
  YY_USE (yyoutput);
  if (!yyvaluep)
    return;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YY_USE (yykind);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}


/*---------------------------.
| Print this symbol on YYO.  |
`---------------------------*/

static void
yy_symbol_print (FILE *yyo,
                 yysymbol_kind_t yykind, YYSTYPE const * const yyvaluep)
{
  YYFPRINTF (yyo, "%s %s (",
             yykind < YYNTOKENS ? "token" : "nterm", yysymbol_name (yykind));

  yy_symbol_value_print (yyo, yykind, yyvaluep);
  YYFPRINTF (yyo, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

static void
yy_stack_print (yy_state_t *yybottom, yy_state_t *yytop)
{
  YYFPRINTF (stderr, "Stack now");
  for (; yybottom <= yytop; yybottom++)
    {
      int yybot = *yybottom;
      YYFPRINTF (stderr, " %d", yybot);
    }
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)                            \
do {                                                            \
  if (yydebug)                                                  \
    yy_stack_print ((Bottom), (Top));                           \
} while (0)


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

static void
yy_reduce_print (yy_state_t *yyssp, YYSTYPE *yyvsp,
                 int yyrule)
{
  int yylno = yyrline[yyrule];
  int yynrhs = yyr2[yyrule];
  int yyi;
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %d):\n",
             yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      YYFPRINTF (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr,
                       YY_ACCESSING_SYMBOL (+yyssp[yyi + 1 - yynrhs]),
                       &yyvsp[(yyi + 1) - (yynrhs)]);
      YYFPRINTF (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)          \
do {                                    \
  if (yydebug)                          \
    yy_reduce_print (yyssp, yyvsp, Rule); \
} while (0)

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args) ((void) 0)
# define YY_SYMBOL_PRINT(Title, Kind, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif






/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

static void
yydestruct (const char *yymsg,
            yysymbol_kind_t yykind, YYSTYPE *yyvaluep)
{
  YY_USE (yyvaluep);
  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yykind, yyvaluep, yylocationp);

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  YY_USE (yykind);
  YY_IGNORE_MAYBE_UNINITIALIZED_END
}


/* Lookahead token kind.  */
int yychar;

/* The semantic value of the lookahead symbol.  */
YYSTYPE yylval;
/* Number of syntax errors so far.  */
int yynerrs;




/*----------.
| yyparse.  |
`----------*/

int
yyparse (void)
{
    yy_state_fast_t yystate = 0;
    /* Number of tokens to shift before error messages enabled.  */
    int yyerrstatus = 0;

    /* Refer to the stacks through separate pointers, to allow yyoverflow
       to reallocate them elsewhere.  */

    /* Their size.  */
    YYPTRDIFF_T yystacksize = YYINITDEPTH;

    /* The state stack: array, bottom, top.  */
    yy_state_t yyssa[YYINITDEPTH];
    yy_state_t *yyss = yyssa;
    yy_state_t *yyssp = yyss;

    /* The semantic value stack: array, bottom, top.  */
    YYSTYPE yyvsa[YYINITDEPTH];
    YYSTYPE *yyvs = yyvsa;
    YYSTYPE *yyvsp = yyvs;

  int yyn;
  /* The return value of yyparse.  */
  int yyresult;
  /* Lookahead symbol kind.  */
  yysymbol_kind_t yytoken = YYSYMBOL_YYEMPTY;
  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;



#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N))

  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yychar = YYEMPTY; /* Cause a token to be read.  */

  goto yysetstate;


/*------------------------------------------------------------.
| yynewstate -- push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;


/*--------------------------------------------------------------------.
| yysetstate -- set current state (the top of the stack) to yystate.  |
`--------------------------------------------------------------------*/
yysetstate:
  YYDPRINTF ((stderr, "Entering state %d\n", yystate));
  YY_ASSERT (0 <= yystate && yystate < YYNSTATES);
  YY_IGNORE_USELESS_CAST_BEGIN
  *yyssp = YY_CAST (yy_state_t, yystate);
  YY_IGNORE_USELESS_CAST_END
  YY_STACK_PRINT (yyss, yyssp);

  if (yyss + yystacksize - 1 <= yyssp)
#if !defined yyoverflow && !defined YYSTACK_RELOCATE
    YYNOMEM;
#else
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYPTRDIFF_T yysize = yyssp - yyss + 1;

# if defined yyoverflow
      {
        /* Give user a chance to reallocate the stack.  Use copies of
           these so that the &'s don't force the real ones into
           memory.  */
        yy_state_t *yyss1 = yyss;
        YYSTYPE *yyvs1 = yyvs;

        /* Each stack pointer address is followed by the size of the
           data in use in that stack, in bytes.  This used to be a
           conditional around just the two extra args, but that might
           be undefined if yyoverflow is a macro.  */
        yyoverflow (YY_("memory exhausted"),
                    &yyss1, yysize * YYSIZEOF (*yyssp),
                    &yyvs1, yysize * YYSIZEOF (*yyvsp),
                    &yystacksize);
        yyss = yyss1;
        yyvs = yyvs1;
      }
# else /* defined YYSTACK_RELOCATE */
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
        YYNOMEM;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
        yystacksize = YYMAXDEPTH;

      {
        yy_state_t *yyss1 = yyss;
        union yyalloc *yyptr =
          YY_CAST (union yyalloc *,
                   YYSTACK_ALLOC (YY_CAST (YYSIZE_T, YYSTACK_BYTES (yystacksize))));
        if (! yyptr)
          YYNOMEM;
        YYSTACK_RELOCATE (yyss_alloc, yyss);
        YYSTACK_RELOCATE (yyvs_alloc, yyvs);
#  undef YYSTACK_RELOCATE
        if (yyss1 != yyssa)
          YYSTACK_FREE (yyss1);
      }
# endif

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;

      YY_IGNORE_USELESS_CAST_BEGIN
      YYDPRINTF ((stderr, "Stack size increased to %ld\n",
                  YY_CAST (long, yystacksize)));
      YY_IGNORE_USELESS_CAST_END

      if (yyss + yystacksize - 1 <= yyssp)
        YYABORT;
    }
#endif /* !defined yyoverflow && !defined YYSTACK_RELOCATE */


  if (yystate == YYFINAL)
    YYACCEPT;

  goto yybackup;


/*-----------.
| yybackup.  |
`-----------*/
yybackup:
  /* Do appropriate processing given the current state.  Read a
     lookahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to lookahead token.  */
  yyn = yypact[yystate];
  if (yypact_value_is_default (yyn))
    goto yydefault;

  /* Not known => get a lookahead token if don't already have one.  */

  /* YYCHAR is either empty, or end-of-input, or a valid lookahead.  */
  if (yychar == YYEMPTY)
    {
      YYDPRINTF ((stderr, "Reading a token\n"));
      yychar = yylex ();
    }

  if (yychar <= YYEOF)
    {
      yychar = YYEOF;
      yytoken = YYSYMBOL_YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else if (yychar == YYerror)
    {
      /* The scanner already issued an error message, process directly
         to error recovery.  But do not keep the error token as
         lookahead, it is too special and may lead us to an endless
         loop in error recovery. */
      yychar = YYUNDEF;
      yytoken = YYSYMBOL_YYerror;
      goto yyerrlab1;
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yytable_value_is_error (yyn))
        goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the lookahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);
  yystate = yyn;
  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END

  /* Discard the shifted token.  */
  yychar = YYEMPTY;
  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     '$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];


  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
  case 2: /* proofrequest: %empty  */
#line 129 "iaparser.y"
                                        { YYABORT; }
#line 1209 "iaparser.c"
    break;

  case 3: /* proofrequest: IA_PROVE '(' term ',' labellistopt ',' IA_NUM ')' '.'  */
#line 130 "iaparser.y"
                                                                        {
					  ia_VarCheck();
					  ia_PROOFREQUEST = list_PairCreate((yyvsp[-6].term),(yyvsp[-4].list));
					  flag_SetFlagIntValue(ia_FLAGS,flag_TIMELIMIT,(yyvsp[-2].number));
					  YYACCEPT;
                                        }
#line 1220 "iaparser.c"
    break;

  case 4: /* termlist: term  */
#line 142 "iaparser.y"
                                        { (yyval.list) = list_List((yyvsp[0].term)); }
#line 1226 "iaparser.c"
    break;

  case 5: /* termlist: termlist ',' term  */
#line 143 "iaparser.y"
                                        { (yyval.list) = list_Nconc((yyvsp[-2].list), list_List((yyvsp[0].term))); }
#line 1232 "iaparser.c"
    break;

  case 6: /* term: id  */
#line 146 "iaparser.y"
                                { (yyval.term) = ia_TermCreate((yyvsp[0].string), list_Nil()); }
#line 1238 "iaparser.c"
    break;

  case 7: /* term: IA_TRUE  */
#line 147 "iaparser.y"
                                { (yyval.term) = term_Create(fol_True(),list_Nil()); }
#line 1244 "iaparser.c"
    break;

  case 8: /* term: IA_FALSE  */
#line 148 "iaparser.y"
                                { (yyval.term) = term_Create(fol_False(),list_Nil()); }
#line 1250 "iaparser.c"
    break;

  case 9: /* term: IA_NOT '(' term ')'  */
#line 150 "iaparser.y"
                                { (yyval.term) = term_Create(fol_Not(),list_List((yyvsp[-1].term))); }
#line 1256 "iaparser.c"
    break;

  case 10: /* term: binsymbol '(' term ',' term ')'  */
#line 152 "iaparser.y"
                                { (yyval.term) = term_Create((yyvsp[-5].symbol), list_Cons((yyvsp[-3].term), list_List((yyvsp[-1].term)))); }
#line 1262 "iaparser.c"
    break;

  case 11: /* term: nsymbol '(' termlist ')'  */
#line 154 "iaparser.y"
                                        { (yyval.term) = term_Create((yyvsp[-3].symbol), (yyvsp[-1].list)); }
#line 1268 "iaparser.c"
    break;

  case 12: /* term: id '(' termlist ')'  */
#line 156 "iaparser.y"
                                { (yyval.term) = ia_TermCreate((yyvsp[-3].string), (yyvsp[-1].list)); }
#line 1274 "iaparser.c"
    break;

  case 13: /* $@1: %empty  */
#line 157 "iaparser.y"
                                        { ia_VarStart(); }
#line 1280 "iaparser.c"
    break;

  case 14: /* $@2: %empty  */
#line 158 "iaparser.y"
                                        { ia_VarStop(); }
#line 1286 "iaparser.c"
    break;

  case 15: /* term: quantsymbol '(' '[' $@1 qtermlist $@2 ']' ',' term ')'  */
#line 160 "iaparser.y"
                                { ia_VarBacktrack();
				  (yyval.term) = ia_CreateQuantifier((yyvsp[-9].symbol),(yyvsp[-5].list),(yyvsp[-1].term));
				}
#line 1294 "iaparser.c"
    break;

  case 16: /* $@3: %empty  */
#line 163 "iaparser.y"
                                        { ia_VarStart(); }
#line 1300 "iaparser.c"
    break;

  case 17: /* $@4: %empty  */
#line 164 "iaparser.y"
                                        { ia_VarStop(); }
#line 1306 "iaparser.c"
    break;

  case 18: /* term: id '(' '[' $@3 qtermlist $@4 ']' ',' term ')'  */
#line 166 "iaparser.y"
                                { misc_StartUserErrorReport();
				  misc_UserErrorReport("\n Line %d: SPASS can't handle the quantifier %s.\n", dfg_LINENUMBER, (yyvsp[-9].string));
				  misc_FinishUserErrorReport();
				}
#line 1315 "iaparser.c"
    break;

  case 19: /* binsymbol: IA_EQUAL  */
#line 172 "iaparser.y"
                                        { (yyval.symbol) = fol_Equality(); }
#line 1321 "iaparser.c"
    break;

  case 20: /* binsymbol: IA_EQUIV  */
#line 173 "iaparser.y"
                                        { (yyval.symbol) = fol_Equiv();    }
#line 1327 "iaparser.c"
    break;

  case 21: /* binsymbol: IA_IMPLIED  */
#line 174 "iaparser.y"
                                        { (yyval.symbol) = fol_Implied();  }
#line 1333 "iaparser.c"
    break;

  case 22: /* binsymbol: IA_IMPLIES  */
#line 175 "iaparser.y"
                                        { (yyval.symbol) = fol_Implies();  }
#line 1339 "iaparser.c"
    break;

  case 23: /* nsymbol: IA_AND  */
#line 178 "iaparser.y"
                                        { (yyval.symbol) = fol_And(); }
#line 1345 "iaparser.c"
    break;

  case 24: /* nsymbol: IA_OR  */
#line 179 "iaparser.y"
                                { (yyval.symbol) = fol_Or();  }
#line 1351 "iaparser.c"
    break;

  case 25: /* quantsymbol: IA_EXISTS  */
#line 182 "iaparser.y"
                                        { (yyval.symbol) = fol_Exist(); }
#line 1357 "iaparser.c"
    break;

  case 26: /* quantsymbol: IA_FORALL  */
#line 183 "iaparser.y"
                                        { (yyval.symbol) = fol_All(); }
#line 1363 "iaparser.c"
    break;

  case 27: /* id: IA_ID  */
#line 186 "iaparser.y"
                                        { (yyval.string) = (yyvsp[0].string); }
#line 1369 "iaparser.c"
    break;

  case 28: /* id: IA_NUM  */
#line 187 "iaparser.y"
                                        { (yyval.string) = string_IntToString((yyvsp[0].number)); }
#line 1375 "iaparser.c"
    break;

  case 29: /* qtermlist: qterm  */
#line 190 "iaparser.y"
                                        { (yyval.list) = list_List((yyvsp[0].term)); }
#line 1381 "iaparser.c"
    break;

  case 30: /* qtermlist: qtermlist ',' qterm  */
#line 191 "iaparser.y"
                                        { (yyval.list) = list_Nconc((yyvsp[-2].list), list_List((yyvsp[0].term))); }
#line 1387 "iaparser.c"
    break;

  case 31: /* qterm: id  */
#line 194 "iaparser.y"
                                        { SYMBOL s = ia_Symbol((yyvsp[0].string),0);
					  if (!symbol_IsVariable(s)) {
					    misc_StartUserErrorReport();
					    misc_UserErrorReport("\n Line %d: %s",dfg_LINENUMBER,
								 symbol_Name(s));
					    misc_UserErrorReport(" is not a variable.\n");
					    misc_FinishUserErrorReport();
					  }
					  (yyval.term) = term_Create(s, list_Nil());
					}
#line 1402 "iaparser.c"
    break;

  case 32: /* qterm: id '(' id ')'  */
#line 204 "iaparser.y"
                                        { SYMBOL p, v;
					  p = ia_Symbol((yyvsp[-3].string), 1);
					  if (!symbol_IsPredicate(p)) {
					    misc_StartUserErrorReport();
					    misc_UserErrorReport("\n Line %d: %s",dfg_LINENUMBER,
								 symbol_Name(p));
					    misc_UserErrorReport(" is not a predicate.\n");
					    misc_FinishUserErrorReport();
					  }
					  v = ia_Symbol((yyvsp[-1].string), 0);
					  if (!symbol_IsVariable(v)) {
					    misc_StartUserErrorReport();
					    misc_UserErrorReport("\n Line %d: %s",dfg_LINENUMBER,
								 symbol_Name(v));
					    misc_UserErrorReport(" is not a variable.\n");
					    misc_FinishUserErrorReport();
					  }
					  (yyval.term) = term_Create(p, list_List(term_Create(v,list_Nil())));
					}
#line 1426 "iaparser.c"
    break;

  case 33: /* labellistopt: '[' ']'  */
#line 225 "iaparser.y"
                                        { (yyval.list) = list_Nil(); }
#line 1432 "iaparser.c"
    break;

  case 34: /* labellistopt: '[' labellist ']'  */
#line 226 "iaparser.y"
                                        { (yyval.list) = (yyvsp[-1].list); }
#line 1438 "iaparser.c"
    break;

  case 35: /* labellist: id  */
#line 229 "iaparser.y"
                                        { (yyval.list) = list_List((yyvsp[0].string)); }
#line 1444 "iaparser.c"
    break;

  case 36: /* labellist: labellist ',' id  */
#line 230 "iaparser.y"
                                        { (yyval.list) = list_Nconc((yyvsp[-2].list), list_List((yyvsp[0].string))); }
#line 1450 "iaparser.c"
    break;


#line 1454 "iaparser.c"

      default: break;
    }
  /* User semantic actions sometimes alter yychar, and that requires
     that yytoken be updated with the new translation.  We take the
     approach of translating immediately before every use of yytoken.
     One alternative is translating here after every semantic action,
     but that translation would be missed if the semantic action invokes
     YYABORT, YYACCEPT, or YYERROR immediately after altering yychar or
     if it invokes YYBACKUP.  In the case of YYABORT or YYACCEPT, an
     incorrect destructor might then be invoked immediately.  In the
     case of YYERROR or YYBACKUP, subsequent parser actions might lead
     to an incorrect destructor call or verbose syntax error message
     before the lookahead is translated.  */
  YY_SYMBOL_PRINT ("-> $$ =", YY_CAST (yysymbol_kind_t, yyr1[yyn]), &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;

  *++yyvsp = yyval;

  /* Now 'shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */
  {
    const int yylhs = yyr1[yyn] - YYNTOKENS;
    const int yyi = yypgoto[yylhs] + *yyssp;
    yystate = (0 <= yyi && yyi <= YYLAST && yycheck[yyi] == *yyssp
               ? yytable[yyi]
               : yydefgoto[yylhs]);
  }

  goto yynewstate;


/*--------------------------------------.
| yyerrlab -- here on detecting error.  |
`--------------------------------------*/
yyerrlab:
  /* Make sure we have latest lookahead translation.  See comments at
     user semantic actions for why this is necessary.  */
  yytoken = yychar == YYEMPTY ? YYSYMBOL_YYEMPTY : YYTRANSLATE (yychar);
  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
      yyerror (YY_("syntax error"));
    }

  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse lookahead token after an
         error, discard it.  */

      if (yychar <= YYEOF)
        {
          /* Return failure if at end of input.  */
          if (yychar == YYEOF)
            YYABORT;
        }
      else
        {
          yydestruct ("Error: discarding",
                      yytoken, &yylval);
          yychar = YYEMPTY;
        }
    }

  /* Else will try to reuse lookahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:
  /* Pacify compilers when the user code never invokes YYERROR and the
     label yyerrorlab therefore never appears in user code.  */
  if (0)
    YYERROR;
  ++yynerrs;

  /* Do not reclaim the symbols of the rule whose action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;      /* Each real token shifted decrements this.  */

  /* Pop stack until we find a state that shifts the error token.  */
  for (;;)
    {
      yyn = yypact[yystate];
      if (!yypact_value_is_default (yyn))
        {
          yyn += YYSYMBOL_YYerror;
          if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYSYMBOL_YYerror)
            {
              yyn = yytable[yyn];
              if (0 < yyn)
                break;
            }
        }

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
        YYABORT;


      yydestruct ("Error: popping",
                  YY_ACCESSING_SYMBOL (yystate), yyvsp);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  YY_IGNORE_MAYBE_UNINITIALIZED_BEGIN
  *++yyvsp = yylval;
  YY_IGNORE_MAYBE_UNINITIALIZED_END


  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", YY_ACCESSING_SYMBOL (yyn), yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturnlab;


/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturnlab;


/*-----------------------------------------------------------.
| yyexhaustedlab -- YYNOMEM (memory exhaustion) comes here.  |
`-----------------------------------------------------------*/
yyexhaustedlab:
  yyerror (YY_("memory exhausted"));
  yyresult = 2;
  goto yyreturnlab;


/*----------------------------------------------------------.
| yyreturnlab -- parsing is finished, clean up and return.  |
`----------------------------------------------------------*/
yyreturnlab:
  if (yychar != YYEMPTY)
    {
      /* Make sure we have latest lookahead translation.  See comments at
         user semantic actions for why this is necessary.  */
      yytoken = YYTRANSLATE (yychar);
      yydestruct ("Cleanup: discarding lookahead",
                  yytoken, &yylval);
    }
  /* Do not reclaim the symbols of the rule whose action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
                  YY_ACCESSING_SYMBOL (+*yyssp), yyvsp);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif

  return yyresult;
}

#line 233 "iaparser.y"



void yyerror(const char *s)
{
  misc_StartUserErrorReport();
  misc_UserErrorReport("\n Line %i: %s\n", dfg_LINENUMBER, s);
  misc_FinishUserErrorReport();

}

LIST ia_GetNextRequest(FILE* Input, FLAGSTORE Flags)
/**************************************************************
  INPUT:   An input file containing one proof request from KIV.
  RETURNS: The proof request as pair (formula, labellist),
           list_Nil(), if EOF was reached.
  EFFECT:  Reads ONE proof request from the file.
           <Input> may also be a UNIX pipe.
***************************************************************/
{
  extern FILE* ia_in;  /* defined in kivscanner */

  ia_in           = Input;
  ia_PROOFREQUEST = list_Nil();
  ia_FLAGS        = Flags;
  ia_parse();
  
  return ia_PROOFREQUEST;
}


/**************************************************************/
/* Static Functions                                           */
/**************************************************************/

static SYMBOL ia_Symbol(char* Name, NAT Arity)
/**************************************************************
  INPUT:   The name of a symbol and the actual arity of the symbol.
  RETURNS: The corresponding SYMBOL.
  EFFECT:  This function checks if the <Name> was declared as
           symbol or variable. If not, an error message is printed
	   to stderr.
	   The <Name> is deleted.
***************************************************************/
{
  SYMBOL symbol;

  symbol = symbol_Lookup(Name);
  if (symbol != 0) {
    ia_StringFree(Name);
    ia_SymCheck(symbol, Arity); /* Check the arity */
  } else {
    /* Variable */
    if (Arity > 0) {
      misc_StartUserErrorReport();
      misc_UserErrorReport("\n Line %d: Undefined symbol %s.\n",dfg_LINENUMBER,Name);
      misc_FinishUserErrorReport();
    }
    symbol = ia_VarLookup(Name);
  }
  return symbol;
}


static TERM ia_CreateQuantifier(SYMBOL Symbol, LIST VarTermList, TERM Term)
/**************************************************************
  INPUT:   A quantifier symbol, a list possibly containing sorts,
           and a term.
  RETURNS: The created quantifier term..
***************************************************************/
{
  LIST varlist, sortlist, scan;
  TERM helpterm;

  /* First collect the variable symbols in varlist and the sorts in sortlist */
  varlist = sortlist = list_Nil();
  for ( ; !list_Empty(VarTermList); VarTermList = list_Pop(VarTermList)) {
    helpterm = list_Car(VarTermList);
    if (term_IsVariable(helpterm)) {
      varlist = list_Nconc(varlist, list_List((POINTER)term_TopSymbol(helpterm)));
      term_Delete(helpterm);
    } else {
      SYMBOL var = term_TopSymbol(term_FirstArgument(helpterm));
      varlist  = list_Nconc(varlist, list_List((POINTER)var));
      sortlist = list_Nconc(sortlist, list_List(helpterm));
    }
  }

  varlist = list_PointerDeleteDuplicates(varlist);
  /* Now create terms from the variables */
  for (scan = varlist; !list_Empty(scan); scan = list_Cdr(scan))
    list_Rplaca(scan, term_Create((SYMBOL)list_Car(scan), list_Nil()));

  if (!list_Empty(sortlist)) {
    if (symbol_Equal(fol_All(), Symbol)) {
      /* The conjunction of all sortterms implies the Term */
      if (symbol_Equal(fol_Or(), term_TopSymbol(Term))) {
	/* Special treatment if <Term> is a term with "or" like */
	/* in clauses: add all sort terms negated to the args    */
	/* of the "or" */
	for (scan = sortlist; !list_Empty(scan); scan = list_Cdr(scan))
	  /* Negate the sort terms */
	  list_Rplaca(scan, term_Create(fol_Not(), list_List(list_Car(scan))));
	sortlist = list_Nconc(sortlist, term_ArgumentList(Term));
	term_RplacArgumentList(Term, sortlist);
      } else {
	/* No "or" term, so build the implication term */
	if (list_Empty(list_Cdr(sortlist))) {
	  /* Only one sort term */
	  list_Rplacd(sortlist, list_List(Term));
	  Term = term_Create(fol_Implies(), sortlist);
	} else {
	  /* More than one sort term */
	  helpterm = term_Create(fol_And(), sortlist);
	  Term = term_Create(fol_Implies(), list_Cons(helpterm, list_List(Term)));
	}
      }
    } else if (symbol_Equal(fol_Exist(), Symbol)) {
      /* Quantify the conjunction of all sort terms and <Term> */
      if (symbol_Equal(fol_And(), term_TopSymbol(Term))) {
	/* Special treatment if <Term> has an "and" as top symbol: */
	/* just add the sort terms to the args of the "and".       */
	sortlist = list_Nconc(sortlist, term_ArgumentList(Term));
	term_RplacArgumentList(Term, sortlist);
      } else {
	sortlist = list_Nconc(sortlist, list_List(Term));
	Term = term_Create(fol_And(), sortlist);
      }
    }
  }
  helpterm = fol_CreateQuantifier(Symbol, varlist, list_List(Term));
  return helpterm;
}


/**************************************************************/
/* Functions for the Symbol Table                             */
/**************************************************************/

static void ia_SymCheck(SYMBOL Symbol, NAT Arity)
/**************************************************************
  INPUT:   A symbol and the current arity of this symbol.
  RETURNS: Nothing.
  EFFECT:  This function compares the previous arity of 'Symbol'
           with the actual 'Arity'. If these values differ
	   a warning is printed to stderr and the program exits.
***************************************************************/
{
  /* Check if the specified arity corresponds with the actual arity */
  if (symbol_Arity(Symbol) != symbol_ArbitraryArity() &&
      symbol_Arity(Symbol) != Arity) {
    misc_StartUserErrorReport();
    misc_UserErrorReport("\n Line %u: Symbol %s", dfg_LINENUMBER, symbol_Name(Symbol));
    misc_UserErrorReport(" was declared with arity %u.\n", symbol_Arity(Symbol));
    misc_FinishUserErrorReport();
  }
}


/**************************************************************/
/* Functions for the Variable Table                           */
/**************************************************************/
  
typedef struct {
  char*  name;
  SYMBOL symbol;
} IA_VARENTRY, *IA_VAR;

 char* ia_VarName(IA_VAR Entry)
{
  return Entry->name;
}

 SYMBOL ia_VarSymbol(IA_VAR Entry)
{
  return Entry->symbol;
}

 IA_VAR ia_VarCreate(void)
{
  return (IA_VAR) memory_Malloc(sizeof(IA_VARENTRY));
}

static void ia_VarFree(IA_VAR Entry)
{
  ia_StringFree(Entry->name);
  memory_Free(Entry, sizeof(IA_VARENTRY));
}

static void ia_VarStart(void)
{
  ia_VARLIST = list_Push(list_Nil(), ia_VARLIST);
  ia_VARDECL = TRUE;
}

static void ia_VarStop(void)
{
  ia_VARDECL = FALSE;
}

static void ia_VarBacktrack(void)
{
  list_DeleteWithElement(list_Top(ia_VARLIST), (void (*)(POINTER)) ia_VarFree);
  ia_VARLIST = list_Pop(ia_VARLIST);
}

static void ia_VarCheck(void)
/* Should be called after a complete clause or formula was parsed */
{
  if (!list_Empty(ia_VARLIST)) {
    misc_StartErrorReport();
    misc_ErrorReport("\n In ia_VarCheck: List of variables should be empty!\n");
    misc_FinishErrorReport();
  }
  symbol_ResetStandardVarCounter();
}

static SYMBOL ia_VarLookup(char* Name)
/**************************************************************
  INPUT:   A variable name.
  RETURNS: The corresponding variable symbol.
  EFFECT:  If the variable name was quantified before, the
           corresponding symbol is returned and the <Name> is freed.
	   If the variable name was not quantified, and <ia_VARDECL>
	   is TRUE, a new variable is created, else an error
	   message is printed and the program exits.
***************************************************************/
{
  LIST   scan, scan2;
  SYMBOL symbol;

  symbol = symbol_Null();

  scan  = ia_VARLIST;
  scan2 = list_Nil();
  while (!list_Empty(scan) && list_Empty(scan2)) {
    scan2 = list_Car(scan);
    while (!list_Empty(scan2) &&
	   !string_Equal(ia_VarName(list_Car(scan2)), Name))
      scan2 = list_Cdr(scan2);
    scan = list_Cdr(scan);
  }

  if (!list_Empty(scan2)) {
    /* Found variable */
    ia_StringFree(Name);
    symbol = ia_VarSymbol(list_Car(scan2));
  } else {
    /* Variable not found */
    if (ia_VARDECL) {
      IA_VAR newEntry = ia_VarCreate();
      newEntry->name   = Name;
      newEntry->symbol = symbol_CreateStandardVariable();
      /* Add <newentry> to the first list in ia_VARLIST */
      list_Rplaca(ia_VARLIST, list_Cons(newEntry,list_Car(ia_VARLIST)));
      symbol = ia_VarSymbol(newEntry);
    } else {
      misc_StartUserErrorReport();
      misc_UserErrorReport("\n Line %u: Free Variable %s.\n", dfg_LINENUMBER, Name);
      misc_FinishUserErrorReport();
    }
  }
  return symbol;
}
