# courtesy of https://www.reddit.com/r/Python/comments/lw50ne/making_a_synthesizer_using_python/

def amp_mod(init_amp, env):
    return env * init_amp
    
def freq_mod(init_freq, env, mod_amt=0.01, sustain_level=0.7):
    return init_freq + ((env - sustain_level) * init_freq * mod_amt)