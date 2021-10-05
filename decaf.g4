grammar decaf;  


//Parse Rules 
// inician con minuscula

start : 'class' 'Program' '{' (declaration)* '}'                # programStart ;

declaration : structDeclaration                                 # declarationStruct
            | varDeclaration                                    # declarationVar
            | methodDeclaration                                 # declarationMethod
            ;

varDeclaration  : varType id_tok ';'                            # varDec
                | varType id_tok '[' num ']' ';'                # arrayDec
                ;

structDeclaration : 'struct' id_tok '{' (varDeclaration)* '}' (';')? # structDec ;

varType : 'int'                                                 # intVarType
        | 'char'                                                # charVarType
        | 'boolean'                                             # booleanVarType
        | 'struct' id_tok                                       # structVarType
        | structDeclaration                                     # structDecVarType
        | 'void'                                                # voidVarType
        ;

methodDeclaration : methodType id_tok '(' (parameter (',' parameter)*)* ')' block # methodDec ;

methodType  : 'int'                                             # intMethod
            | 'char'                                            # charMethod
            | 'boolean'                                         # booleanMethod
            | 'void'                                            # voidMethod
            ;

parameter   : parameterType id_tok                              # idParam
            | parameterType id_tok '[' ']'                      # arrayParam
            | 'void'                                            # voidParam
            ;


parameterType   : 'int'                                         # intParam
                | 'char'                                        # charParam
                | 'boolean'                                     # booleanParam
                ;

block : '{' (varDeclaration)* (statement)* '}'                  # blockDec ;

statement   : 'if' '(' expression ')' block                     # ifStmt
            |'if' '(' expression ')' block 'else' block         # ifElseStmt
            | 'while' '(' expression ')' block                  # whileStmt
            | 'return' (expression)? ';'                        # returnStmt
            | methodCall ';'                                    # methodStmt
            | block                                             # blockStmt
            | location '=' expression ';'                       # assignmentStmt
            | expression ';'                                    # expressionStmt
            ;

location : id_tok                                               # idLocation
         | id_tok '.' location                                  # idLocationDot
         | id_tok '[' expression ']'                            # arrayLocation
         | id_tok '[' expression ']' '.' location               # arrayLocationDot
         ;

expression  : location                                          # locationExpr
            | methodCall                                        # methodCallExpr
            | literal                                           # literalExpr
            | expression op=('*'|'/'|'%') expression            # firstArithExpr
            | expression op=('+'|'-') expression                # secondArithExpr
            | expression op=('<'|'>'|'<='|'>=') expression      # relExpr
            | expression op=('=='|'!=') expression              # eqExpr
            | expression op=('&&'|'||') expression              # condExpr
            | op='-' expression                                 # negativeExpr
            | op='!' expression                                 # notExpr
            | '(' expression ')'                                # parExpr
            ;

methodCall : id_tok '(' arg? (',' arg)* ')'                     # methodCallDec;                    

arg : expression                                                # argDec ;

literal : int_literal                                           # intLiteral 
        | CHAR_LITERAL                                          # charLiteral
        | bool_literal                                          # boolLiteral
        ;

int_literal : num                                               # numLiteral ;

bool_literal    : 'true'                                        # trueLiteral 
                | 'false'                                       # falseLiteral
                ;

id_tok : ID                                                     # idDec ;

num : DIGIT+                                                    # numDec ;

// Tokens inician con mayuscula

CHAR_LITERAL : '\'' LETTER '\'' ;

ID : LETTER ALPHA_num* ;

DIGIT: [0-9]+ ; 

LETTER: [a-zA-Z] | '_' ;

ALPHA_num : LETTER | DIGIT ;

WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines

COMMENTS: '//' ~('\r' | '\n')* -> channel(HIDDEN);