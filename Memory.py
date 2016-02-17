# implementation of card game - Memory
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
CAN_W = 800
CAN_H = 100
CARD_CNT = 16
CARD_W = CAN_W / CARD_CNT
OFFSET = 2
exposedCards = {}
cardVal = []
state = 0
lastCardClicks = [-1,-1]
turnCount = 0
# helper function to initialize globals
def new_game():
    global exposedCards, cardVal, turnCount, lastCardClicks, state
    exposedCards = {}
    cardVal = range(8) + range(8)
    random.shuffle(cardVal)
    state = 0
    turnCount = 0
    lastCardClicks = [-1,-1]

# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposedCards, state, lastCardClicks, turnCount
    xCoord = pos[0]
    crdIdx = xCoord // CARD_W
    isExposed = exposedCards.get(crdIdx)
    if (not isExposed):
        exposedCards[crdIdx] = True
        if state == 0:
            state = 1
            lastCardClicks[0] = crdIdx
        elif state == 1:
            state = 2
            turnCount += 1            
            lastCardClicks[1] = crdIdx
        else:
            state = 1
            if cardVal[lastCardClicks[0]] != cardVal[lastCardClicks[1]]:
                exposedCards[lastCardClicks[0]] = False
                exposedCards[lastCardClicks[1]] = False           
            lastCardClicks = [crdIdx,-1]
            
# cards are logically 50x100 pixels in size    
def draw(canvas):
    trnStr = "Turns = " + str(turnCount)
    label.set_text(trnStr)
    for crdIdx in range(16):
        xCoord1 = (crdIdx * CARD_W)
        xCoord2 = xCoord1 + CARD_W - OFFSET / 2
        isExposed = exposedCards.get(crdIdx)
        if (isExposed):
            canvas.draw_polygon([(xCoord1,0),(xCoord2 , 0),(xCoord2, CAN_H),(xCoord1, CAN_H)],OFFSET/2, 'White', 'Brown')
            strLoc = [xCoord1 + 0.1 * (xCoord2 - xCoord1)  , CAN_H - (0.25 * CAN_H)]
            val = str(cardVal[crdIdx])
            canvas.draw_text(val, strLoc, 80, 'White')
        else:
            canvas.draw_polygon([(xCoord1,0),(xCoord2 , 0),(xCoord2, CAN_H),(xCoord1, CAN_H)],OFFSET/2, 'White', 'Blue')



# create frame and add a button and labels
frame = simplegui.create_frame("Memory", CAN_W, CAN_H)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric