import pygame
import random

pygame.init()
pygame.mixer.init() #music player

# ----- SCREEN -----
WIDTH, HEIGHT = 800, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Casino Games")

font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 40)

# ----- MUSIC -----
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# ----- COLOURS -----
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
RED = (200, 0, 0)
GREEN = (0, 160, 0)
DARKGREEN = (53, 101, 77)

HOVER_GREY = (170, 170, 170)
ACTIVE_BLUE = (50, 120, 255)
DARK_RED = (150, 0, 0)
DARK_BLACK = (30, 30, 30)

# ----- ROULETTE NUMBERS -----
RED_NUMBERS = {
    1,3,5,7,9,12,14,16,18,
    19,21,23,25,27,30,32,34,36
}

BLACK_NUMBERS = {
    2,4,6,8,10,11,13,15,17,
    20,22,24,26,28,29,31,33,35
}

# ----- UI BUTTONS -----
# Menu
BlackjackButton = pygame.Rect(220, 220, 145, 35)
RouletteButton = pygame.Rect(420, 220, 145, 35)

switch_to_roulette_button = pygame.Rect(600, 20, 170, 30)
switch_to_blackjack_button = pygame.Rect(600, 20, 170, 30)

# Roulette
bet_button = pygame.Rect(145, 170, 120, 35)
red_button = pygame.Rect(80, 220, 120, 35)
black_button = pygame.Rect(220, 220, 120, 35)
input_box = pygame.Rect(105, 100, 200, 35)
number_box = pygame.Rect(105, 300, 200, 35)
RouletteImg = pygame.image.load("Roulette.png").convert_alpha()

# Blackjack
hit_button = pygame.Rect(80, 320, 120, 35)
stand_button = pygame.Rect(220, 320, 120, 35)

# ----- GAME STATE -----
RouletteActive = False
BlackjackActive = False
balance = 100

# Roulette variables
bet_text = ""
number_text = ""
active_bet = False
active_number = False
chosen_color = None
chosen_number = None
message = ""
message_color = BLACK

# Blackjack variables
player_hand = []
dealer_hand = []
blackjack_bet = 0
blackjack_round = False

# ----- BLACKJACK -----
values = {
    "2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,
    "J":10,"Q":10,"K":10,"A":11
}

def draw_card():
    return random.choice(list(values.keys()))

def hand_value(hand):
    total = sum(values[c] for c in hand)
    aces = hand.count("A")
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def draw_text(text, x, y, color=BLACK, big=False):
    f = big_font if big else font
    screen.blit(f.render(text, True, color), (x, y))

def get_color(number):
    if number == 0:
        return "Green"
    if number in RED_NUMBERS:
        return "Red"
    return "Black"

# ----- MAIN LOOP -----
running = True
while running:
    screen.fill(DARKGREEN)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if BlackjackActive and switch_to_roulette_button.collidepoint(event.pos):
                BlackjackActive = False
                RouletteActive = True
                message = ""
                chosen_color = None
                number_text = ""   
                click_sound = pygame.mixer.Sound("Button_Click_Sound.mp3")
                click_sound.play()

            elif RouletteActive and switch_to_blackjack_button.collidepoint(event.pos):
                RouletteActive = False
                BlackjackActive = True
                message = ""
                blackjack_round = False
                player_hand = []
                dealer_hand = []
                click_sound.play()

        # -------------------- ROULETTE --------------------
        if RouletteActive:
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound = pygame.mixer.Sound("Button_Click_Sound.mp3")
                
                active_bet = input_box.collidepoint(event.pos)
                active_number = number_box.collidepoint(event.pos)

                # Pick color
                if red_button.collidepoint(event.pos):
                    chosen_color = "Red"
                    click_sound.play()
                if black_button.collidepoint(event.pos):
                    chosen_color = "Black"
                    click_sound.play()

                # Spin button
                if bet_button.collidepoint(event.pos):
                    if not bet_text.isdigit():
                        message = "Enter bet amount"
                        message_color = RED
                        error_sound = pygame.mixer.Sound("error.mp3")
                        error_sound.set_volume(1.5)
                        error_sound.play()
                    elif chosen_color is None:
                        message = "Pick a color first"
                        message_color = RED
                        error_sound = pygame.mixer.Sound("error.mp3")
                        error_sound.set_volume(1.5)
                        error_sound.play()
                    else:
                        bet = int(bet_text)
                        if bet <= 0 or bet > balance:
                            message = "Not enough balance"
                            message_color = RED
                            error_sound = pygame.mixer.Sound("error.mp3")
                            error_sound.set_volume(1.5)
                            error_sound.play()
                        else:
                            balance -= bet
                            spin = random.randint(0, 36)
                            result_color = get_color(spin)
                            click_sound.play()

                            roulette_sound = pygame.mixer.Sound("roulette-casino.mp3")
                            roulette_sound.set_volume(2)
                            roulette_sound.play()
                            pygame.time.delay(3000)

                            # NUMBER BET
                            if number_text.isdigit():
                                chosen_number = int(number_text)
                                if chosen_number == spin:
                                    balance += bet * 10
                                    message = f"NUMBER HIT! {spin} ({result_color})"
                                    message_color = GREEN
                                    win_sound = pygame.mixer.Sound("money.mp3")
                                    win_sound.set_volume(2)
                                    win_sound.play()
                                else:
                                    message = f"Lost! {spin} ({result_color})"
                                    message_color = RED
                                    lose_sound = pygame.mixer.Sound("lose_sound.mp3")
                                    lose_sound.set_volume(2)
                                    lose_sound.play()
                            # COLOR BET
                            else:
                                if result_color == chosen_color:
                                    balance += bet * 2.5
                                    message = f"Won! ({result_color})"
                                    message_color = GREEN
                                    win_sound = pygame.mixer.Sound("money.mp3")
                                    win_sound.set_volume(2)
                                    win_sound.play()
                                else:
                                    message = f"Lost! ({result_color})"
                                    message_color = RED
                                    lose_sound = pygame.mixer.Sound("lose_sound.mp3")
                                    lose_sound.set_volume(2)
                                    lose_sound.play()

                            bet_text = ""
                            number_text = ""
                            chosen_number = None

                            

        # -------------------- BLACKJACK --------------------
        elif BlackjackActive:
            if event.type == pygame.MOUSEBUTTONDOWN:
                active_bet = input_box.collidepoint(event.pos)

                # Start round
                if bet_button.collidepoint(event.pos) and not blackjack_round:
                    if bet_text.isdigit():
                        blackjack_bet = int(bet_text)
                        if 0 < blackjack_bet <= balance:
                            balance -= blackjack_bet
                            player_hand = [draw_card(), draw_card()]
                            dealer_hand = [draw_card(), draw_card()]
                            blackjack_round = True
                            message = ""
                            bet_text = ""
                            click_sound.play()

                # HIT
                if blackjack_round and hit_button.collidepoint(event.pos):
                    player_hand.append(draw_card())
                    if hand_value(player_hand) > 21:
                        message = "BUST! You lose"
                        message_color = RED
                        blackjack_round = False
                        lose_sound = pygame.mixer.Sound("lose_sound.mp3")
                        lose_sound.set_volume(2)
                        lose_sound.play()
                        click_sound.play()

                # STAND
                if blackjack_round and stand_button.collidepoint(event.pos):
                    while hand_value(dealer_hand) < 17:
                        dealer_hand.append(draw_card())

                    click_sound.play()
                    p = hand_value(player_hand)
                    d = hand_value(dealer_hand)
                    if d > 21 or p > d:
                        balance += blackjack_bet * 2
                        message = "YOU WIN!"
                        message_color = GREEN
                        win_sound = pygame.mixer.Sound("money.mp3")
                        win_sound.play()
                    elif p == d:
                        balance += blackjack_bet
                        message = "PUSH"
                        message_color = BLACK
                    else:
                        message = "DEALER WINS"
                        message_color = RED
                        lose_sound = pygame.mixer.Sound("lose_sound.mp3")
                        lose_sound.set_volume(2)
                        lose_sound.play()

                    blackjack_round = False

        # ----- KEYBOARD INPUT -----
        if event.type == pygame.KEYDOWN:
            if active_bet:
                if event.key == pygame.K_BACKSPACE:
                    bet_text = bet_text[:-1]
                elif event.unicode.isdigit():
                    bet_text += event.unicode

            if active_number:
                if event.key == pygame.K_BACKSPACE:
                    number_text = number_text[:-1]
                elif event.unicode.isdigit() and len(number_text) < 2:
                    number_text += event.unicode

        # ----- MENU BUTTONS -----
        click_sound = pygame.mixer.Sound("Button_Click_Sound.mp3")
        if event.type == pygame.MOUSEBUTTONDOWN and not (RouletteActive or BlackjackActive):
            if RouletteButton.collidepoint(event.pos):
                RouletteActive = True
                BlackjackActive = False
                click_sound.play()
            if BlackjackButton.collidepoint(event.pos):
                BlackjackActive = True
                RouletteActive = False
                click_sound.play()

    # -----DRAW UI -----
    if RouletteActive:
        # Buttons
        bet_color = HOVER_GREY if bet_button.collidepoint(mouse_pos) else GREY
        pygame.draw.rect(screen, bet_color, bet_button)
        draw_text("SPIN", bet_button.x + 35, bet_button.y + 8)

        red_color = DARK_RED if chosen_color == "Red" else RED
        if red_button.collidepoint(mouse_pos):
            red_color = (255, 80, 80)
        pygame.draw.rect(screen, red_color, red_button)
        draw_text("RED", red_button.x + 40, red_button.y + 8, WHITE)

        black_color = DARK_BLACK if chosen_color == "Black" else BLACK
        if black_button.collidepoint(mouse_pos):
            black_color = (60, 60, 60)
        pygame.draw.rect(screen, black_color, black_button)
        draw_text("BLACK", black_button.x + 30, black_button.y + 8, WHITE)

        # Input boxes
        pygame.draw.rect(screen, ACTIVE_BLUE if active_bet else BLACK, input_box, 3 if active_bet else 2)
        pygame.draw.rect(screen, ACTIVE_BLUE if active_number else BLACK, number_box, 3 if active_number else 2)
        draw_text(bet_text, input_box.x + 10, input_box.y + 8)
        draw_text(number_text, number_box.x + 10, number_box.y + 8)

        draw_text(f"Balance: ${balance}", 100, 50, big=True)
        draw_text("Bet Amount", 100, 80)
        draw_text("Optional Number (10x payout)", 70, 270)

        # Roulette image
        RouletteImg_scaled = pygame.transform.smoothscale(RouletteImg, (300, 300))
        screen.blit(RouletteImg_scaled, (420, 100))

        if chosen_color:
            draw_text(f"Chosen color: {chosen_color}", 470, 225)

        draw_text(message, 515, 252, message_color)

        pygame.draw.rect(screen, GREY, switch_to_roulette_button)
        draw_text("Go to Blackjack", switch_to_roulette_button.x + 10, switch_to_roulette_button.y + 8)

    elif BlackjackActive:
        # Buttons
        pygame.draw.rect(screen, GREY, bet_button)
        draw_text("DEAL", bet_button.x + 35, bet_button.y + 8)

        if blackjack_round:
            pygame.draw.rect(screen, GREY, hit_button)
            pygame.draw.rect(screen, GREY, stand_button)
            draw_text("HIT", hit_button.x + 40, hit_button.y + 8)
            draw_text("STAND", stand_button.x + 25, stand_button.y + 8)

        pygame.draw.rect(screen, ACTIVE_BLUE if active_bet else BLACK, input_box, 3 if active_bet else 2)
        draw_text(bet_text, input_box.x + 10, input_box.y + 8)
        draw_text(f"Balance: ${balance}", 100, 50, big=True)
        draw_text("Bet Amount", 100, 80)

        draw_text(f"Player: {' '.join(player_hand)} ({hand_value(player_hand)})", 80, 230)
        draw_text(f"Dealer: {' '.join(dealer_hand)} ({hand_value(dealer_hand)})", 80, 280)
        draw_text(message, 80, 250, message_color)

        pygame.draw.rect(screen, GREY, switch_to_roulette_button)
        draw_text("Go to Roulette", switch_to_roulette_button.x + 10, switch_to_roulette_button.y + 8)
        
        draw_text("1. Look at your hand", 380, 100)
        draw_text("2. Choose if you want to HIT or STAND", 380, 120)
        draw_text("3. HIT: go for another round", 380, 140)
        draw_text("4. STAND: end the round", 380, 160)
        draw_text("5. After standing, whoever has the", 380, 180)
        draw_text("    closer number to 21 wins", 380, 200)
        draw_text("6. If your number goes above 21 LOSE!", 380, 220)


    else:
        # Menu buttons
        red_color = DARK_RED
        if RouletteButton.collidepoint(mouse_pos):
            red_color = (255, 80, 80)
        pygame.draw.rect(screen, red_color, RouletteButton)
        draw_text("ROULETTE", RouletteButton.x + 20, RouletteButton.y + 8, WHITE)

        black_color = DARK_BLACK
        if BlackjackButton.collidepoint(mouse_pos):
            black_color = (60, 60, 60)
        pygame.draw.rect(screen, black_color, BlackjackButton)
        draw_text("BLACKJACK", BlackjackButton.x + 10, BlackjackButton.y + 8, WHITE)

    pygame.display.update()

pygame.quit()
