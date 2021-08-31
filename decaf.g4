grammar decaf;  

// Tokens inician con mayuscula

//A fragment will never be counted as a token, it only serves to simplify a grammar.

fragment DIGIT: [0-9] ; 

LETTER: ('a'..'z'|'A'..'Z')+ ;

WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines

NUM : '-'? DIGIT (DIGIT)*;



//Parse Rules 
// inician con minuscula

start : 'class' 'Program' '{' (declaration)* '}';

id_tok : LETTER (LETTER|DIGIT)*;

declaration : structDeclaration
            | varDeclaration
            | methodDeclaration
            ;

varDeclaration  : varType id_tok ';'
                | varType id_tok '[' NUM ']' ';'
                ;

structDeclaration : 'struct' id_tok '{' (varDeclaration)* '}' (';')?;

varType : 'int'
        | 'char'
        | 'boolean'
        | 'struct' id_tok
        | structDeclaration
        | 'void'
        ;

methodDeclaration : methodType id_tok '(' (parameter (',' parameter)*)* ')' block ;

methodType  : 'int'
            | 'char'
            | 'boolean'
            | 'void'
            ;

parameter   : parameterType id_tok
            | parameterType id_tok '[' ']'
            | 'void'
            ;


parameterType   : 'int'
                | 'char'
                | 'boolean'
                ;

block : '{' (varDeclaration)* (statement)* returnStatement? '}' ;

statement   : 'if' '(' expression ')' block ('else' block)?
            | 'while' '(' expression ')' block
            | methodCall ';'
            | block
            | location '=' expression
            | (expression)? ';'
            ;

returnStatement : 'return' (expression)? ';';

location : (id_tok | id_tok '[' expression ']') ( '.' location)? ;

uni_op  : '-' 
        | '!'
        ;

expression  : location
            | methodCall
            | literal
            | expression op expression
            | uni_op expression
            | uni_op expression
            | '(' expression ')'
            ;

methodCall : id_tok '(' arg? (',' arg)* ')';

arg : expression ;

op  : arith_op 
    | rel_op 
    | eq_op 
    | cond_op
    ;

arith_op    : '+' 
            | '-' 
            | '*' 
            | '/' 
            | '%'
            ;

rel_op  : '<' 
        | '>' 
        | '<=' 
        | '>='
        ;

eq_op   : '==' 
        | '!='
        ;


cond_op : '&&' 
        | '||'
        ;

literal : int_literal 
        | char_literal
        | bool_literal
        ;

int_literal : NUM ;

char_literal : '\'' LETTER '\'' ;

bool_literal    : 'true' 
                | 'false'
                ;

