from constant import *
from square import Square
from piece import *
from move import Move
class Board:
    def __init__(self):
        self.squares=[[0,0,0,0,0,0,0,0] for col in range(COLS)]
        self.last_move=None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self,piece,move):
        initial=move.initial
        final=move.final
        #console board move update
        self.squares[initial.row][initial.col].piece=None
        self.squares[final.row][final.col].piece=piece
        #move
        piece.moved=True
        #clear moves
        piece.clear_moves()
        #set last move
        self.last_move=move

    def valid_move(self,piece,move):
        return move in piece.moves

    def calc_moves(self,piece,row,col):

        def pawn_moves():
            #steps
            steps=1 if piece.moved else 2
            #vertical moves
            start=row+piece.dir
            end=row+(piece.dir*(1+steps))

            for possible_move_row in range(start,end,piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        #create final and initial squares
                        initial=Square(row,col)
                        final=Square(possible_move_row,col)
                        #create the new move
                        move=Move(initial,final)
                        #append the move
                        piece.add_moves(move)
                    else:
                        #we are blocked
                        break
                else:
                    #not in range
                    break
            #diagonal moves
            possible_move_row=row+piece.dir
            possible_move_cols=[col-1,col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row,possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        #create initial and final square
                        initial=Square(row,col)
                        final=Square(possible_move_row,possible_move_col)
                        #create the new move
                        move=Move(initial,final)
                        #append the new move
                        piece.add_moves(move)

        def straight_line_moves(incrs):
            for incr in incrs:
                row_incr,col_incr=incr
                possible_move_row=row+row_incr
                possible_move_col=col+col_incr
                while True:
                    if Square.in_range(possible_move_row,possible_move_col):
                        #create initial and final square for new moves
                        initial=Square(row,col)
                        final=Square(possible_move_row,possible_move_col)
                        #create new move
                        move=Move(initial,final)

                        #empty
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            #append new moves
                            piece.add_moves(move)

                        #has enemy piece
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            #append new moves
                            piece.add_moves(move)
                            break
                        #has own team piece
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                     #not in range (break)
                    else:break
                    #incrementing incr
                    possible_move_row=possible_move_row+row_incr
                    possible_move_col=possible_move_col+col_incr

        def king_moves():
            adjs=[
                (row-1,col+0),
                (row+1,col+0),
                (row+1,col+1),
                (row+1,col-1),
                (row-1,col+1),
                (row-1,col-1),
                (row+0,col-1),
                (row+0,col+1),
            ]
            #normal moves
            for possible_move in adjs:
                possible_move_row,possible_move_col=possible_move

                if Square.in_range(possible_move_row,possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        #create squares
                        initial=Square(row,col)
                        final=Square(possible_move_row,possible_move_col)#piece=piece
                        #create new moves
                        move=Move(initial,final)
                        #append new move
                        piece.add_moves(move)

            #castling move
            #queen castling move
            #king castling move

        def knight_moves():
            #8 possible moves
            possible_moves=[
                (row-2,col+1),
                (row-1,col+2),
                (row+1,col+2),
                (row+2,col+1),
                (row+2,col-1),
                (row+1,col-2),
                (row-1,col-2),
                (row-2,col-1),
            ]

            for possible_move in possible_moves:
                possible_move_row,possible_move_col=possible_move

                if Square.in_range(possible_move_row,possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        #create squares
                        initial=Square(row,col)
                        final=Square(possible_move_row,possible_move_col)#piece=piece
                        #create new moves
                        move=Move(initial,final)
                        #append new move
                        piece.add_moves(move)

        if isinstance(piece,Pawn):#equivalent to piece.name=='pawn'
            pawn_moves()
        elif isinstance(piece,Knight):
            knight_moves()
        elif isinstance(piece,Bishop):
            straight_line_moves([
                (1,-1),#down-left
                (1,1),#down-right
                (-1,1),#up-right
                (-1,-1),#up-left
            ])
        elif isinstance(piece,Rook):
            straight_line_moves([
                (1,0),
                (0,1),
                (-1,0),
                (0,-1),
            ])
        elif isinstance(piece,Queen):
            straight_line_moves([
                (1,0),
                (0,1),
                (-1,0),
                (0,-1),
                (1,-1),#down-left
                (1,1),#down-right
                (-1,1),#up-right
                (-1,-1),#up-left
            ])
        elif isinstance(piece,King):
            king_moves()

    def _create(self):
       
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col]=Square(row,col)

    def _add_pieces(self,color):
        
        row_pawn,row_other =(6,7) if color=='white' else (1,0) 
        #pawns
        for col in range(COLS):
            self.squares[row_pawn][col]=Square(row_pawn,col,Pawn(color))
            
        #knights   
        self.squares[row_other][1]=Square(row_other,1, Knight(color))
        self.squares[row_other][6]=Square(row_other,6, Knight(color))
        
        #bishops
        self.squares[row_other][2]=Square(row_other,2, Bishop(color))
        self.squares[row_other][5]=Square(row_other,5, Bishop(color))
        
        #rooks
        self.squares[row_other][0]=Square(row_other,0, Rook(color))
        self.squares[row_other][7]=Square(row_other,7, Rook(color))
        #queen
        self.squares[row_other][3]=Square(row_other,3, Queen(color))
        
        #king
        self.squares[row_other][4]=Square(row_other,4, King(color))