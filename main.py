# referencing https://www.reddit.com/r/Python/comments/lw50ne/making_a_synthesizer_using_python/ for sound synthesis

import math
import pyaudio
import itertools
import numpy as np
import pygame as pg
import sys

pg.font.init()

WIDTH, HEIGHT = 850, 500
WIN = pg.display.set_mode((WIDTH, HEIGHT))

pg.display.set_caption("Virtual Piano - Luke Robinson")

# constants

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
BLUE = (155, 213, 255)

BUFFER_SIZE = 256
SAMPLE_RATE = 44100
NOTE_AMP = 0.1

KEY_WIDTH = 50
KEY_HEIGHT = 75
WHITE_KEY_Y = 150
BLACK_KEY_Y = 50

FONT = pg.font.SysFont('century', 20)
KEY_FONT = pg.font.SysFont('century', 15)

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

KEY_LIST = [KEY_C, KEY_CS, KEY_D, KEY_DS, KEY_E, KEY_F, 
            KEY_FS, KEY_G, KEY_GS, KEY_A, KEY_AS, KEY_B, KEY_C2]

# global fields
octave = 4
a4 = 440
note_freqs = {}

# initializing output stream for audio
stream = pyaudio.PyAudio().open(
    rate=SAMPLE_RATE,
    channels=1,
    format=pyaudio.paInt16,
    output=True,
    frames_per_buffer=BUFFER_SIZE,
)

# two functions from the reference for sound synthesis

def get_sin_oscillator(freq=55, amp=1, sample_rate=SAMPLE_RATE):
    increment = (2 * math.pi * freq) / sample_rate
    return (
        math.sin(v) * amp * NOTE_AMP for v in itertools.count(start=0, step=increment)
    )

def get_samples(notes_dict, num_samples=BUFFER_SIZE):
    return [
        sum([int(next(osc) * 32767) for _, osc in notes_dict.items()])
        for _ in range(num_samples)
    ]

def get_note(index, octave):
    if index == 0:
        return f"C{octave}"
    elif index == 1:
        return f"C#{octave}"
    elif index == 2:
        return f"D{octave}"
    elif index == 3:
        return f"D#{octave}"
    elif index == 4:
        return f"E{octave}"
    elif index == 5:
        return f"F{octave}"
    elif index == 6:
        return f"F#{octave}"
    elif index == 7:
        return f"G{octave}"
    elif index == 8:
        return f"G#{octave}"
    elif index == 9:
        return f"A{octave}"
    elif index == 10:
        return f"A#{octave}"
    elif index == 11:
        return f"B{octave}"
    elif index == 12:
        return f"C{octave+1}"

def get_freq(note):
    return note_freqs[note]

def set_octave(new_val):
    global octave
    if (new_val in range(3, 6)):
        octave = new_val

def set_a4(new_hz):
    global a4
    a4 = new_hz

# input text box to change a4 frequency
a4_user_text = ""
a4_input_rect = pg.Rect(WIDTH/2 + 50, 350, 140, 32)
a4_active = False

# input text box to change octave
oct_user_text = ""
oct_input_rect = pg.Rect(WIDTH/2 - 200, 350, 140, 32)
oct_active = False

def draw_window():

    bg = pg.Rect(0, 0, WIDTH, HEIGHT)
    pg.draw.rect(WIN, BLUE, bg)

    # drawing the keys

    for key in WHITE_KEY_LIST:
        pg.draw.rect(WIN, WHITE, key)
    
    for key in BLACK_KEY_LIST:
        pg.draw.rect(WIN, BLACK, key)
    
    # text on keys for reference to keyboard and notes
    c_text = KEY_FONT.render("C - a", True, BLACK)
    WIN.blit(c_text, (50, WHITE_KEY_Y))
    cs_text = KEY_FONT.render("C# - w", True, WHITE)
    WIN.blit(cs_text, (100, BLACK_KEY_Y))
    d_text = KEY_FONT.render("D - s", True, BLACK)
    WIN.blit(d_text, (150, WHITE_KEY_Y))
    ds_text = KEY_FONT.render("D# - e", True, WHITE)
    WIN.blit(ds_text, (200, BLACK_KEY_Y))
    e_text = KEY_FONT.render("E - d", True, BLACK)
    WIN.blit(e_text, (250, WHITE_KEY_Y))
    f_text = KEY_FONT.render("F - f", True, BLACK)
    WIN.blit(f_text, (350, WHITE_KEY_Y))
    fs_text = KEY_FONT.render("F# - t", True, WHITE)
    WIN.blit(fs_text, (400, BLACK_KEY_Y))
    g_text = KEY_FONT.render("G - g", True, BLACK)
    WIN.blit(g_text, (450, WHITE_KEY_Y))
    gs_text = KEY_FONT.render("G# - y", True, WHITE)
    WIN.blit(gs_text, (500, BLACK_KEY_Y))
    a_text = KEY_FONT.render("A - h", True, BLACK)
    WIN.blit(a_text, (550, WHITE_KEY_Y))
    as_text = KEY_FONT.render("A# - u", True, WHITE)
    WIN.blit(as_text, (600, BLACK_KEY_Y))
    b_text = KEY_FONT.render("B - j", True, BLACK)
    WIN.blit(b_text, (650, WHITE_KEY_Y))
    c2_text = KEY_FONT.render("c - k", True, BLACK)
    WIN.blit(c2_text, (750, WHITE_KEY_Y))
    
    # text boxes and their labels

    pg.draw.rect(WIN, WHITE, a4_input_rect)
    a4_box_text = FONT.render(a4_user_text, True, BLACK)
    WIN.blit(a4_box_text, (a4_input_rect.x+5, a4_input_rect.y+5))

    a4_text = FONT.render(f"A4 = {a4} Hz", True, BLACK)
    WIN.blit(a4_text, (WIDTH/2 + 50, 300))

    pg.draw.rect(WIN, WHITE, oct_input_rect)
    oct_box_text = FONT.render(oct_user_text, True, BLACK)
    WIN.blit(oct_box_text, (oct_input_rect.x+5, oct_input_rect.y+5))

    oct_text = FONT.render(f"Octave (3-5): {octave}", True, BLACK)
    WIN.blit(oct_text, (WIDTH/2 - 200, 300))

    pg.display.update()

def main():
    run = True
    notes_dict = {}
    global octave
    global a4_user_text
    global a4_active
    global oct_user_text
    global oct_active
    global note_freqs

    while run:
        
        note_freqs = {
            "C3":a4*(math.pow(2, -21/12)), "C#3":a4*(math.pow(2, -20/12)), "D3":a4*(math.pow(2, -19/12)), "D#3":a4*(math.pow(2, -18/12)), "E3":a4*(math.pow(2, -17/12)), "F3":a4*(math.pow(2, -16/12)), 
            "F#3":a4*(math.pow(2, -15/12)), "G3":a4*(math.pow(2, -14/12)), "G#3":a4*(math.pow(2, -13/12)), "A3":a4/2, "A#3":a4*(math.pow(2, -11/12)), "B3":a4*(math.pow(2, -10/12)),
    
            "C4":a4*(math.pow(2, -9/12)), "C#4":a4*(math.pow(2, -8/12)), "D4":a4*(math.pow(2, -7/12)), "D#4":a4*(math.pow(2, -6/12)), "E4":a4*(math.pow(2, -5/12)), "F4":a4*(math.pow(2, -4/12)), 
            "F#4":a4*(math.pow(2, -3/12)), "G4":a4*(math.pow(2, -2/12)), "G#4":a4*(math.pow(2, -1/12)), "A4":a4, "A#4":a4*(math.pow(2, 1/12)), "B4":a4*(math.pow(2, 2/12)),

            "C5":a4*(math.pow(2, 3/12)), "C#5":a4*(math.pow(2, 4/12)), "D5":a4*(math.pow(2, 5/12)), "D#5":a4*(math.pow(2, 6/12)), "E5":a4*(math.pow(2, 7/12)), "F5":a4*(math.pow(2, 8/12)), 
            "F#5":a4*(math.pow(2, 9/12)), "G5":a4*(math.pow(2, 10/12)), "G#5":a4*(math.pow(2, 11/12)), "A5":a4*2, "A#5":a4*(math.pow(2, 13/12)), "B5":a4*(math.pow(2, 14/12)),

            "C6":a4*(math.pow(2, 15/12))
        }

        for event in pg.event.get():

            if event.type == pg.QUIT:
                run = False
                pg.quit()
                sys.exit(1)
            
            # event handling for text boxes

            if event.type == pg.MOUSEBUTTONDOWN:
                if a4_input_rect.collidepoint(event.pos):
                    a4_active = True
                elif oct_input_rect.collidepoint(event.pos):
                    oct_active = True
                else:
                    a4_active = False
                    oct_active = False
  
            if event.type == pg.KEYDOWN:
                if a4_active == True:
                    if event.key == pg.K_BACKSPACE:
                        a4_user_text = a4_user_text[:-1]
                    
                    elif event.key == pg.K_RETURN:
                        set_a4(int(a4_user_text))

                    else:
                        a4_user_text += event.unicode

                elif oct_active == True:
                    if event.key == pg.K_BACKSPACE:
                        oct_user_text = oct_user_text[:-1]
                    
                    elif event.key == pg.K_RETURN:
                        set_octave(int(oct_user_text))

                    else:
                        oct_user_text += event.unicode
        
        # detecting pressed keys and playing corresponding frequencies

        keys = pg.key.get_pressed()

        pressed = [keys[pg.K_a], keys[pg.K_w], keys[pg.K_s], 
                    keys[pg.K_e], keys[pg.K_d], keys[pg.K_f], 
                    keys[pg.K_t], keys[pg.K_g], keys[pg.K_y], 
                    keys[pg.K_h], keys[pg.K_u], keys[pg.K_j], 
                    keys[pg.K_k]]

        if notes_dict:
            # play the notes
            samples = get_samples(notes_dict)
            samples = np.int16(samples).tobytes()
            stream.write(samples)

        index = 0
        for key_status in pressed:
            # add or remove notes from dict
            note = get_note(index, octave)
            if key_status == False and note in notes_dict:
                del notes_dict[note]
            elif key_status == True and note not in notes_dict:
                freq = get_freq(note)
                notes_dict[note] = get_sin_oscillator(freq=freq, amp=1)
            index += 1

        draw_window()

if __name__ == "__main__":
    main()