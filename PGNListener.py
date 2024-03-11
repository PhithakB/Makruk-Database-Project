# Generated from PGN.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .PGNParser import PGNParser
else:
    from PGNParser import PGNParser

# This class defines a complete listener for a parse tree produced by PGNParser.
class PGNListener(ParseTreeListener):

    # Enter a parse tree produced by PGNParser#parse.
    def enterParse(self, ctx:PGNParser.ParseContext):
        pass

    # Exit a parse tree produced by PGNParser#parse.
    def exitParse(self, ctx:PGNParser.ParseContext):
        pass


    # Enter a parse tree produced by PGNParser#pgn_database.
    def enterPgn_database(self, ctx:PGNParser.Pgn_databaseContext):
        pass

    # Exit a parse tree produced by PGNParser#pgn_database.
    def exitPgn_database(self, ctx:PGNParser.Pgn_databaseContext):
        pass


    # Enter a parse tree produced by PGNParser#pgn_game.
    def enterPgn_game(self, ctx:PGNParser.Pgn_gameContext):
        pass

    # Exit a parse tree produced by PGNParser#pgn_game.
    def exitPgn_game(self, ctx:PGNParser.Pgn_gameContext):
        pass


    # Enter a parse tree produced by PGNParser#tag_section.
    def enterTag_section(self, ctx:PGNParser.Tag_sectionContext):
        pass

    # Exit a parse tree produced by PGNParser#tag_section.
    def exitTag_section(self, ctx:PGNParser.Tag_sectionContext):
        pass


    # Enter a parse tree produced by PGNParser#tag_pair.
    def enterTag_pair(self, ctx:PGNParser.Tag_pairContext):
        pass

    # Exit a parse tree produced by PGNParser#tag_pair.
    def exitTag_pair(self, ctx:PGNParser.Tag_pairContext):
        pass


    # Enter a parse tree produced by PGNParser#tag_name.
    def enterTag_name(self, ctx:PGNParser.Tag_nameContext):
        pass

    # Exit a parse tree produced by PGNParser#tag_name.
    def exitTag_name(self, ctx:PGNParser.Tag_nameContext):
        pass


    # Enter a parse tree produced by PGNParser#tag_value.
    def enterTag_value(self, ctx:PGNParser.Tag_valueContext):
        pass

    # Exit a parse tree produced by PGNParser#tag_value.
    def exitTag_value(self, ctx:PGNParser.Tag_valueContext):
        pass


    # Enter a parse tree produced by PGNParser#movetext_section.
    def enterMovetext_section(self, ctx:PGNParser.Movetext_sectionContext):
        pass

    # Exit a parse tree produced by PGNParser#movetext_section.
    def exitMovetext_section(self, ctx:PGNParser.Movetext_sectionContext):
        pass


    # Enter a parse tree produced by PGNParser#element_sequence.
    def enterElement_sequence(self, ctx:PGNParser.Element_sequenceContext):
        pass

    # Exit a parse tree produced by PGNParser#element_sequence.
    def exitElement_sequence(self, ctx:PGNParser.Element_sequenceContext):
        pass


    # Enter a parse tree produced by PGNParser#element.
    def enterElement(self, ctx:PGNParser.ElementContext):
        pass

    # Exit a parse tree produced by PGNParser#element.
    def exitElement(self, ctx:PGNParser.ElementContext):
        pass


    # Enter a parse tree produced by PGNParser#move_number_indication.
    def enterMove_number_indication(self, ctx:PGNParser.Move_number_indicationContext):
        pass

    # Exit a parse tree produced by PGNParser#move_number_indication.
    def exitMove_number_indication(self, ctx:PGNParser.Move_number_indicationContext):
        pass


    # Enter a parse tree produced by PGNParser#san_move.
    def enterSan_move(self, ctx:PGNParser.San_moveContext):
        pass

    # Exit a parse tree produced by PGNParser#san_move.
    def exitSan_move(self, ctx:PGNParser.San_moveContext):
        pass


    # Enter a parse tree produced by PGNParser#comment.
    def enterComment(self, ctx:PGNParser.CommentContext):
        pass

    # Exit a parse tree produced by PGNParser#comment.
    def exitComment(self, ctx:PGNParser.CommentContext):
        pass


    # Enter a parse tree produced by PGNParser#recursive_variation.
    def enterRecursive_variation(self, ctx:PGNParser.Recursive_variationContext):
        pass

    # Exit a parse tree produced by PGNParser#recursive_variation.
    def exitRecursive_variation(self, ctx:PGNParser.Recursive_variationContext):
        pass


    # Enter a parse tree produced by PGNParser#game_termination.
    def enterGame_termination(self, ctx:PGNParser.Game_terminationContext):
        pass

    # Exit a parse tree produced by PGNParser#game_termination.
    def exitGame_termination(self, ctx:PGNParser.Game_terminationContext):
        pass



del PGNParser