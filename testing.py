from synthesizer import Player, Synthesizer, Waveform
import pygame as pg
import sys

pg.init()

player = Player()
player.open_stream()
synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=0.5, use_osc2=True, osc2_waveform = Waveform.triangle, osc2_volume=0.5)

# player.play_wave(synthesizer.generate_constant_wave(440.0, 3.0))

# chord = [440.0, 550.0, 660.0]
# player.play_wave(synthesizer.generate_chord(chord, 3.0))

# chord = ["C2", "C3", "G3", "C4", "E4", "G4", "B4", "D5", "F#5"]
# player.play_wave(synthesizer.generate_chord(chord, 3.0))

ratio = 2**(1/12)

def gen_maj_triad(freq):

    note1 = freq
    note2 = note1 * (ratio**4)
    note3 = note2 * (ratio**3)

    return [note1, note2, note3]


def gen_just_maj_chord(freq):

    note1 = freq
    note2 = freq * (5 / 4)
    note3 = freq * (3 / 2)
    note4 = freq * (15 / 8)
    note5 = freq * (9 / 4)

    return [note1, note2, note3, note4, note5]

# chord = gen_just_maj_chord(220.0)
chord = gen_maj_triad(220.0)
player.play_wave(synthesizer.generate_chord(chord, 2.0))
chord = gen_just_maj_chord(220.0)
player.play_wave(synthesizer.generate_chord(chord, 2.0))

WIDTH, HEIGHT = 850, 500
WIN = pg.display.set_mode((WIDTH, HEIGHT))

def draw_window():
    pg.display.update()

def main():
    clock = pg.time.Clock()
    run = True
    while run:

        clock.tick(60)
        
        for event in pg.event.get():

            if event.type == pg.QUIT:
                run = False
                pg.quit()
                sys.exit(1)

        keys = pg.key.get_pressed()

        pressed = [keys[pg.K_a], keys[pg.K_w], keys[pg.K_s], 
                    keys[pg.K_e], keys[pg.K_d], keys[pg.K_f], 
                    keys[pg.K_t], keys[pg.K_g], keys[pg.K_y], 
                    keys[pg.K_h], keys[pg.K_u], keys[pg.K_j], 
                    keys[pg.K_k]]
        print(pressed)

        draw_window()

if __name__ == "__main__":
    main()