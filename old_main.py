from synthesizer import Player, Synthesizer, Waveform
import pygame as pg
import sys

# initializing pygame and window

pg.init()

WIDTH, HEIGHT = 850, 500
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("synthesizer")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

KEY_WIDTH = 50
KEY_HEIGHT = 75
WHITE_KEY_Y = 150
BLACK_KEY_Y = 50

# white keys
KEY_C = pg.Rect(50, WHITE_KEY_Y, KEY_WIDTH, KEY_HEIGHT)
KEY_D = pg.Rect(150, WHITE_KEY_Y, KEY_WIDTH, KEY_HEIGHT)
KEY_E = pg.Rect(250, WHITE_KEY_Y, KEY_WIDTH, KEY_HEIGHT)
KEY_F = pg.Rect(350, WHITE_KEY_Y, KEY_WIDTH, KEY_HEIGHT)
KEY_G = pg.Rect(450, WHITE_KEY_Y, KEY_WIDTH, KEY_HEIGHT)
KEY_A = pg.Rect(550, WHITE_KEY_Y, KEY_WIDTH, KEY_HEIGHT)
KEY_B = pg.Rect(650, WHITE_KEY_Y, KEY_WIDTH, KEY_HEIGHT)
KEY_C2 = pg.Rect(750, WHITE_KEY_Y, KEY_WIDTH, KEY_HEIGHT)

WHITE_KEY_LIST = [KEY_C, KEY_D, KEY_E, KEY_F, KEY_G, KEY_A, KEY_B, KEY_C2]

# black keys
KEY_CS = pg.Rect(100, BLACK_KEY_Y, KEY_WIDTH, KEY_HEIGHT)
KEY_DS = pg.Rect(200, BLACK_KEY_Y, KEY_WIDTH, KEY_HEIGHT)
KEY_FS = pg.Rect(400, BLACK_KEY_Y, KEY_WIDTH, KEY_HEIGHT)
KEY_GS = pg.Rect(500, BLACK_KEY_Y, KEY_WIDTH, KEY_HEIGHT)
KEY_AS = pg.Rect(600, BLACK_KEY_Y, KEY_WIDTH, KEY_HEIGHT)

BLACK_KEY_LIST = [KEY_CS, KEY_DS, KEY_FS, KEY_GS, KEY_AS]

FPS = 60

def draw_window():
    
    for key in WHITE_KEY_LIST:
        pg.draw.rect(WIN, WHITE, key)
    
    for key in BLACK_KEY_LIST:
        pg.draw.rect(WIN, WHITE, key)
    
    pg.display.update()

# initializing synth

player = Player()
player.open_stream()
synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)

def gen_single_note(note, note_length):
    player.play_wave(synthesizer.generate_constant_wave(note, note_length))

ratio = 2**(1/12)
def gen_maj_triad(freq):

    note1 = freq
    note2 = note1 * (ratio**4)
    note3 = note2 * (ratio**3)

    return [note1, note2, note3]

# ASCII values:
    # a, w, s, e, d, f, t, g, y, h, u, j, k = 97, 119, 115, 101, 100, 102, 116, 103, 121, 104, 117, 106, 107

note_length = 0.5

def single_note_handler(keys):
    if keys[pg.K_a]:
        gen_single_note("C3", note_length)
    if keys[pg.K_w]:
        gen_single_note("C#3", note_length)
    if keys[pg.K_s]:
        gen_single_note("D3", note_length)
    if keys[pg.K_e]:
        gen_single_note("D#3", note_length)
    if keys[pg.K_d]:
        gen_single_note("E3", note_length)
    if keys[pg.K_f]:
        gen_single_note("F3", note_length)
    if keys[pg.K_t]:
        gen_single_note("F#3", note_length)
    if keys[pg.K_g]:
        gen_single_note("G3", note_length)
    if keys[pg.K_y]:
        gen_single_note("G#3", note_length)
    if keys[pg.K_h]:
        gen_single_note("A3", note_length)
    if keys[pg.K_u]:
        gen_single_note("A#3", note_length)
    if keys[pg.K_j]:
        gen_single_note("B3", note_length)
    if keys[pg.K_k]:
        gen_single_note("C4", note_length)

def chord_handler(keys):
    if count == 3:
        if keys[pg.K_a] and keys[pg.K_d] and keys[pg.K_g]:
            chord = gen_maj_triad(130.81)
            player.play_wave(synthesizer.generate_chord(chord, 1.0))

# main loop

def main():
    clock = pg.time.Clock()
    run = True
    while run:

        clock.tick(FPS)

        for event in pg.event.get():

            if event.type == pg.QUIT:
                run = False
                pg.quit()
                sys.exit(1)
            
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                #FIXME: play key that is clicked
        
        keys = pg.key.get_pressed()

        global count 
        count = keys.count(True)

        if count == 1:
            single_note_handler(keys)
        elif count > 1:
            chord_handler(keys)

        draw_window()

if __name__ == "__main__":
    main()