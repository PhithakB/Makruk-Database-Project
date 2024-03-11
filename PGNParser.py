# Generated from PGN.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,22,90,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,1,0,1,0,1,0,1,1,5,1,35,8,1,10,1,12,1,38,9,1,1,2,1,2,1,
        2,1,3,5,3,44,8,3,10,3,12,3,47,9,3,1,4,1,4,1,4,1,4,1,4,1,5,1,5,1,
        6,1,6,1,7,1,7,1,7,1,8,1,8,5,8,63,8,8,10,8,12,8,66,9,8,1,9,1,9,1,
        9,1,9,3,9,72,8,9,1,10,1,10,4,10,76,8,10,11,10,12,10,77,1,11,1,11,
        1,12,1,12,1,13,1,13,1,13,1,13,1,14,1,14,1,14,0,0,15,0,2,4,6,8,10,
        12,14,16,18,20,22,24,26,28,0,2,1,0,4,6,2,0,1,3,12,12,82,0,30,1,0,
        0,0,2,36,1,0,0,0,4,39,1,0,0,0,6,45,1,0,0,0,8,48,1,0,0,0,10,53,1,
        0,0,0,12,55,1,0,0,0,14,57,1,0,0,0,16,64,1,0,0,0,18,71,1,0,0,0,20,
        73,1,0,0,0,22,79,1,0,0,0,24,81,1,0,0,0,26,83,1,0,0,0,28,87,1,0,0,
        0,30,31,3,2,1,0,31,32,5,0,0,1,32,1,1,0,0,0,33,35,3,4,2,0,34,33,1,
        0,0,0,35,38,1,0,0,0,36,34,1,0,0,0,36,37,1,0,0,0,37,3,1,0,0,0,38,
        36,1,0,0,0,39,40,3,6,3,0,40,41,3,14,7,0,41,5,1,0,0,0,42,44,3,8,4,
        0,43,42,1,0,0,0,44,47,1,0,0,0,45,43,1,0,0,0,45,46,1,0,0,0,46,7,1,
        0,0,0,47,45,1,0,0,0,48,49,5,13,0,0,49,50,3,10,5,0,50,51,3,12,6,0,
        51,52,5,14,0,0,52,9,1,0,0,0,53,54,5,20,0,0,54,11,1,0,0,0,55,56,5,
        9,0,0,56,13,1,0,0,0,57,58,3,16,8,0,58,59,3,28,14,0,59,15,1,0,0,0,
        60,63,3,18,9,0,61,63,3,26,13,0,62,60,1,0,0,0,62,61,1,0,0,0,63,66,
        1,0,0,0,64,62,1,0,0,0,64,65,1,0,0,0,65,17,1,0,0,0,66,64,1,0,0,0,
        67,72,3,20,10,0,68,72,3,22,11,0,69,72,5,19,0,0,70,72,3,24,12,0,71,
        67,1,0,0,0,71,68,1,0,0,0,71,69,1,0,0,0,71,70,1,0,0,0,72,19,1,0,0,
        0,73,75,5,10,0,0,74,76,5,11,0,0,75,74,1,0,0,0,76,77,1,0,0,0,77,75,
        1,0,0,0,77,78,1,0,0,0,78,21,1,0,0,0,79,80,5,20,0,0,80,23,1,0,0,0,
        81,82,7,0,0,0,82,25,1,0,0,0,83,84,5,15,0,0,84,85,3,16,8,0,85,86,
        5,16,0,0,86,27,1,0,0,0,87,88,7,1,0,0,88,29,1,0,0,0,6,36,45,62,64,
        71,77
    ]

class PGNParser ( Parser ):

    grammarFileName = "PGN.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'1-0'", "'0-1'", "'1/2-1/2'", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'.'", "'*'", "'['", "']'", 
                     "'('", "')'", "'<'", "'>'" ]

    symbolicNames = [ "<INVALID>", "WHITE_WINS", "BLACK_WINS", "DRAWN_GAME", 
                      "REST_OF_LINE_COMMENT", "BRACE_COMMENT", "PARENTHESIS_COMMENT", 
                      "ESCAPE", "SPACES", "STRING", "INTEGER", "PERIOD", 
                      "ASTERISK", "LEFT_BRACKET", "RIGHT_BRACKET", "LEFT_PARENTHESIS", 
                      "RIGHT_PARENTHESIS", "LEFT_ANGLE_BRACKET", "RIGHT_ANGLE_BRACKET", 
                      "NUMERIC_ANNOTATION_GLYPH", "SYMBOL", "SUFFIX_ANNOTATION", 
                      "UNEXPECTED_CHAR" ]

    RULE_parse = 0
    RULE_pgn_database = 1
    RULE_pgn_game = 2
    RULE_tag_section = 3
    RULE_tag_pair = 4
    RULE_tag_name = 5
    RULE_tag_value = 6
    RULE_movetext_section = 7
    RULE_element_sequence = 8
    RULE_element = 9
    RULE_move_number_indication = 10
    RULE_san_move = 11
    RULE_comment = 12
    RULE_recursive_variation = 13
    RULE_game_termination = 14

    ruleNames =  [ "parse", "pgn_database", "pgn_game", "tag_section", "tag_pair", 
                   "tag_name", "tag_value", "movetext_section", "element_sequence", 
                   "element", "move_number_indication", "san_move", "comment", 
                   "recursive_variation", "game_termination" ]

    EOF = Token.EOF
    WHITE_WINS=1
    BLACK_WINS=2
    DRAWN_GAME=3
    REST_OF_LINE_COMMENT=4
    BRACE_COMMENT=5
    PARENTHESIS_COMMENT=6
    ESCAPE=7
    SPACES=8
    STRING=9
    INTEGER=10
    PERIOD=11
    ASTERISK=12
    LEFT_BRACKET=13
    RIGHT_BRACKET=14
    LEFT_PARENTHESIS=15
    RIGHT_PARENTHESIS=16
    LEFT_ANGLE_BRACKET=17
    RIGHT_ANGLE_BRACKET=18
    NUMERIC_ANNOTATION_GLYPH=19
    SYMBOL=20
    SUFFIX_ANNOTATION=21
    UNEXPECTED_CHAR=22

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ParseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def pgn_database(self):
            return self.getTypedRuleContext(PGNParser.Pgn_databaseContext,0)


        def EOF(self):
            return self.getToken(PGNParser.EOF, 0)

        def getRuleIndex(self):
            return PGNParser.RULE_parse

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParse" ):
                listener.enterParse(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParse" ):
                listener.exitParse(self)




    def parse(self):

        localctx = PGNParser.ParseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_parse)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 30
            self.pgn_database()
            self.state = 31
            self.match(PGNParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Pgn_databaseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def pgn_game(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PGNParser.Pgn_gameContext)
            else:
                return self.getTypedRuleContext(PGNParser.Pgn_gameContext,i)


        def getRuleIndex(self):
            return PGNParser.RULE_pgn_database

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPgn_database" ):
                listener.enterPgn_database(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPgn_database" ):
                listener.exitPgn_database(self)




    def pgn_database(self):

        localctx = PGNParser.Pgn_databaseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_pgn_database)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 36
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 1619070) != 0):
                self.state = 33
                self.pgn_game()
                self.state = 38
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Pgn_gameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def tag_section(self):
            return self.getTypedRuleContext(PGNParser.Tag_sectionContext,0)


        def movetext_section(self):
            return self.getTypedRuleContext(PGNParser.Movetext_sectionContext,0)


        def getRuleIndex(self):
            return PGNParser.RULE_pgn_game

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPgn_game" ):
                listener.enterPgn_game(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPgn_game" ):
                listener.exitPgn_game(self)




    def pgn_game(self):

        localctx = PGNParser.Pgn_gameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_pgn_game)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 39
            self.tag_section()
            self.state = 40
            self.movetext_section()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Tag_sectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def tag_pair(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PGNParser.Tag_pairContext)
            else:
                return self.getTypedRuleContext(PGNParser.Tag_pairContext,i)


        def getRuleIndex(self):
            return PGNParser.RULE_tag_section

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTag_section" ):
                listener.enterTag_section(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTag_section" ):
                listener.exitTag_section(self)




    def tag_section(self):

        localctx = PGNParser.Tag_sectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_tag_section)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 45
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==13:
                self.state = 42
                self.tag_pair()
                self.state = 47
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Tag_pairContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LEFT_BRACKET(self):
            return self.getToken(PGNParser.LEFT_BRACKET, 0)

        def tag_name(self):
            return self.getTypedRuleContext(PGNParser.Tag_nameContext,0)


        def tag_value(self):
            return self.getTypedRuleContext(PGNParser.Tag_valueContext,0)


        def RIGHT_BRACKET(self):
            return self.getToken(PGNParser.RIGHT_BRACKET, 0)

        def getRuleIndex(self):
            return PGNParser.RULE_tag_pair

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTag_pair" ):
                listener.enterTag_pair(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTag_pair" ):
                listener.exitTag_pair(self)




    def tag_pair(self):

        localctx = PGNParser.Tag_pairContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_tag_pair)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 48
            self.match(PGNParser.LEFT_BRACKET)
            self.state = 49
            self.tag_name()
            self.state = 50
            self.tag_value()
            self.state = 51
            self.match(PGNParser.RIGHT_BRACKET)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Tag_nameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYMBOL(self):
            return self.getToken(PGNParser.SYMBOL, 0)

        def getRuleIndex(self):
            return PGNParser.RULE_tag_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTag_name" ):
                listener.enterTag_name(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTag_name" ):
                listener.exitTag_name(self)




    def tag_name(self):

        localctx = PGNParser.Tag_nameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_tag_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 53
            self.match(PGNParser.SYMBOL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Tag_valueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(PGNParser.STRING, 0)

        def getRuleIndex(self):
            return PGNParser.RULE_tag_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTag_value" ):
                listener.enterTag_value(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTag_value" ):
                listener.exitTag_value(self)




    def tag_value(self):

        localctx = PGNParser.Tag_valueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_tag_value)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 55
            self.match(PGNParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Movetext_sectionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def element_sequence(self):
            return self.getTypedRuleContext(PGNParser.Element_sequenceContext,0)


        def game_termination(self):
            return self.getTypedRuleContext(PGNParser.Game_terminationContext,0)


        def getRuleIndex(self):
            return PGNParser.RULE_movetext_section

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMovetext_section" ):
                listener.enterMovetext_section(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMovetext_section" ):
                listener.exitMovetext_section(self)




    def movetext_section(self):

        localctx = PGNParser.Movetext_sectionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_movetext_section)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 57
            self.element_sequence()
            self.state = 58
            self.game_termination()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Element_sequenceContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PGNParser.ElementContext)
            else:
                return self.getTypedRuleContext(PGNParser.ElementContext,i)


        def recursive_variation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PGNParser.Recursive_variationContext)
            else:
                return self.getTypedRuleContext(PGNParser.Recursive_variationContext,i)


        def getRuleIndex(self):
            return PGNParser.RULE_element_sequence

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElement_sequence" ):
                listener.enterElement_sequence(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElement_sequence" ):
                listener.exitElement_sequence(self)




    def element_sequence(self):

        localctx = PGNParser.Element_sequenceContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_element_sequence)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 64
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 1606768) != 0):
                self.state = 62
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [4, 5, 6, 10, 19, 20]:
                    self.state = 60
                    self.element()
                    pass
                elif token in [15]:
                    self.state = 61
                    self.recursive_variation()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 66
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def move_number_indication(self):
            return self.getTypedRuleContext(PGNParser.Move_number_indicationContext,0)


        def san_move(self):
            return self.getTypedRuleContext(PGNParser.San_moveContext,0)


        def NUMERIC_ANNOTATION_GLYPH(self):
            return self.getToken(PGNParser.NUMERIC_ANNOTATION_GLYPH, 0)

        def comment(self):
            return self.getTypedRuleContext(PGNParser.CommentContext,0)


        def getRuleIndex(self):
            return PGNParser.RULE_element

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElement" ):
                listener.enterElement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElement" ):
                listener.exitElement(self)




    def element(self):

        localctx = PGNParser.ElementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_element)
        try:
            self.state = 71
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [10]:
                self.enterOuterAlt(localctx, 1)
                self.state = 67
                self.move_number_indication()
                pass
            elif token in [20]:
                self.enterOuterAlt(localctx, 2)
                self.state = 68
                self.san_move()
                pass
            elif token in [19]:
                self.enterOuterAlt(localctx, 3)
                self.state = 69
                self.match(PGNParser.NUMERIC_ANNOTATION_GLYPH)
                pass
            elif token in [4, 5, 6]:
                self.enterOuterAlt(localctx, 4)
                self.state = 70
                self.comment()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Move_number_indicationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTEGER(self):
            return self.getToken(PGNParser.INTEGER, 0)

        def PERIOD(self, i:int=None):
            if i is None:
                return self.getTokens(PGNParser.PERIOD)
            else:
                return self.getToken(PGNParser.PERIOD, i)

        def getRuleIndex(self):
            return PGNParser.RULE_move_number_indication

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMove_number_indication" ):
                listener.enterMove_number_indication(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMove_number_indication" ):
                listener.exitMove_number_indication(self)




    def move_number_indication(self):

        localctx = PGNParser.Move_number_indicationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_move_number_indication)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 73
            self.match(PGNParser.INTEGER)
            self.state = 75 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 74
                self.match(PGNParser.PERIOD)
                self.state = 77 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==11):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class San_moveContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYMBOL(self):
            return self.getToken(PGNParser.SYMBOL, 0)

        def getRuleIndex(self):
            return PGNParser.RULE_san_move

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSan_move" ):
                listener.enterSan_move(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSan_move" ):
                listener.exitSan_move(self)




    def san_move(self):

        localctx = PGNParser.San_moveContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_san_move)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 79
            self.match(PGNParser.SYMBOL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CommentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def REST_OF_LINE_COMMENT(self):
            return self.getToken(PGNParser.REST_OF_LINE_COMMENT, 0)

        def BRACE_COMMENT(self):
            return self.getToken(PGNParser.BRACE_COMMENT, 0)

        def PARENTHESIS_COMMENT(self):
            return self.getToken(PGNParser.PARENTHESIS_COMMENT, 0)

        def getRuleIndex(self):
            return PGNParser.RULE_comment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComment" ):
                listener.enterComment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComment" ):
                listener.exitComment(self)




    def comment(self):

        localctx = PGNParser.CommentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_comment)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 81
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 112) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Recursive_variationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LEFT_PARENTHESIS(self):
            return self.getToken(PGNParser.LEFT_PARENTHESIS, 0)

        def element_sequence(self):
            return self.getTypedRuleContext(PGNParser.Element_sequenceContext,0)


        def RIGHT_PARENTHESIS(self):
            return self.getToken(PGNParser.RIGHT_PARENTHESIS, 0)

        def getRuleIndex(self):
            return PGNParser.RULE_recursive_variation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRecursive_variation" ):
                listener.enterRecursive_variation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRecursive_variation" ):
                listener.exitRecursive_variation(self)




    def recursive_variation(self):

        localctx = PGNParser.Recursive_variationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_recursive_variation)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 83
            self.match(PGNParser.LEFT_PARENTHESIS)
            self.state = 84
            self.element_sequence()
            self.state = 85
            self.match(PGNParser.RIGHT_PARENTHESIS)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Game_terminationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHITE_WINS(self):
            return self.getToken(PGNParser.WHITE_WINS, 0)

        def BLACK_WINS(self):
            return self.getToken(PGNParser.BLACK_WINS, 0)

        def DRAWN_GAME(self):
            return self.getToken(PGNParser.DRAWN_GAME, 0)

        def ASTERISK(self):
            return self.getToken(PGNParser.ASTERISK, 0)

        def getRuleIndex(self):
            return PGNParser.RULE_game_termination

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGame_termination" ):
                listener.enterGame_termination(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGame_termination" ):
                listener.exitGame_termination(self)




    def game_termination(self):

        localctx = PGNParser.Game_terminationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_game_termination)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 87
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 4110) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





