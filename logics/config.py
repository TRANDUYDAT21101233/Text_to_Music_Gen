import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

ACESTEP_CHECKPOINT_PATH = "acestep/ACE-Step-v1-3.5B"
USE_BF16 = True
USE_TORCH_COMPILE = True
CPU_OFFLOAD = True
OVERLAPPED_DECODE = True

LYRIC_DEFAULT = """[verse]
Neon lights they flicker bright
City hums in dead of night
Rhythms pulse through concrete veins
Lost in echoes of refrains

[chorus]
Turn it up and let it flow
Feel the fire let it grow
In this rhythm we belong
Hear the night sing out our song
"""

GENRE_PRESETS = {
    "Pop": "pop, synth, catchy, upbeat, 120 bpm, radio-friendly, polished vocals",
    "Modern Pop": "pop, synth, drums, guitar, 120 bpm, upbeat, catchy, vibrant, female vocals, polished vocals",
    "Rock": "rock, electric guitar, live drums, 130 bpm, energetic, gritty, male vocals, raw vocals",
    "Alternative Rock": "alternative rock, distorted guitar, bass, indie vibe, 128 bpm, edgy, emotional vocals",
    "Hip Hop": "hip hop, 808 bass, hi-hats, synth, 90 bpm, bold, urban, rhythmic vocals",
    "Trap": "trap, 808s, snare rolls, dark vibe, 70 bpm, aggressive, punchy, autotuned vocals",
    "Lo-fi": "lo-fi, chill beats, ambient, vinyl crackle, 75 bpm, relaxing, nostalgic",
    "EDM": "edm, synths, bass drop, club, 128 bpm, energetic, pulsating",
    "Electronic": "electronic, synths, drum machine, repetitive beats, 125 bpm, futuristic, danceable, instrumental focus",
    "House": "house, deep bass, piano chords, 120 bpm, groovy, danceable",
    "Techno": "techno, repetitive beats, synth loops, 130 bpm, minimal, underground vibe",
    "Trance": "trance, arpeggiated synths, build-ups, 140 bpm, euphoric, dreamy",
    "Drum and Bass": "dnb, fast tempo, breakbeats, 174 bpm, energetic, rolling bass",
    "Dubstep": "dubstep, heavy bass, wobbles, 140 bpm, glitchy, robotic sounds",
    "Reggae": "reggae, offbeat guitar, mellow, 80 bpm, soulful, island vibe, smooth vocals",
    "Dancehall": "dancehall, Caribbean rhythm, upbeat, 100 bpm, catchy, groove-heavy",
    "Classical": "classical, orchestral, strings, piano, 60 bpm, elegant, instrumental",
    "Baroque": "baroque, harpsichord, chamber orchestra, 55 bpm, detailed, formal",
    "Jazz": "jazz, saxophone, piano, double bass, 110 bpm, improvisational, smooth vocals",
    "Blues": "blues, guitar, harmonica, 12-bar, 90 bpm, soulful, expressive",
    "Soul": "soul, warm vocals, organ, bass, 85 bpm, emotional, rich harmonies",
    "R&B": "r&b, smooth beats, synth, 85 bpm, romantic, silky vocals",
    "Neo Soul": "neo soul, mellow, jazzy chords, groovy, 90 bpm, female vocals",
    "Metal": "metal, distorted guitar, double kick drums, 160 bpm, aggressive, screamed vocals",
    "Hard Rock": "hard rock, power chords, heavy drums, 150 bpm, intense, raw",
    "Country": "country, acoustic guitar, fiddle, 100 bpm, rustic, male vocals, storytelling",
    "Folk": "folk, acoustic, banjo, soft melodies, 95 bpm, narrative lyrics",
    "Indie": "indie, dreamy guitar, synth pop, 115 bpm, atmospheric, light vocals",
    "Ambient": "ambient, pads, soundscape, slow, 60 bpm, spacious, instrumental",
    "Cinematic": "cinematic, orchestra, epic, trailer music, 90 bpm, emotional, dramatic",
    "Gospel": "gospel, choir, organ, clapping, 100 bpm, uplifting, spiritual",
    "World": "world, ethnic instruments, percussions, 90 bpm, cultural, traditional sounds",
    "K-Pop": "k-pop, dance beats, layered vocals, 125 bpm, energetic, polished",
    "J-Pop": "j-pop, electronic, catchy hooks, 130 bpm, anime style, bright vocals",
    "Synthwave": "synthwave, retro synths, 80s style, 100 bpm, neon vibe, instrumental",
    "Chillwave": "chillwave, lo-fi synths, ambient vibe, 85 bpm, dreamy, faded vocals",
    "Experimental": "experimental, glitch, atonal, 90 bpm, avant-garde, unpredictable",
    "Soundtrack": "soundtrack, cinematic, emotional, orchestral, 80 bpm, mood-driven",
    "Trap Metal": "trap metal, 808 bass, metal guitar, 150 bpm, aggressive, fusion",
    "Punk": "punk, distorted guitar, fast drums, 160 bpm, rebellious, raw vocals"
}

EMOTION_PRESETS = {
    "Happy": "joyful, cheerful, upbeat, positive, feel-good",
    "Sad": "melancholic, slow, emotional, reflective, sorrowful",
    "Angry": "aggressive, harsh, intense, powerful, explosive",
    "Romantic": "passionate, intimate, tender, sweet, dreamy",
    "Inspiring": "uplifting, motivational, epic, grand, heroic",
    "Peaceful": "calm, soothing, chill, mellow, peaceful",
    "Dark": "ominous, eerie, haunting, brooding, moody",
    "Energetic": "high tempo, driving, dynamic, powerful, active",
    "Hopeful": "optimistic, warm, uplifting, emotional, forward-looking",
    "Lonely": "isolated, empty, introspective, ambient, sparse",
    "Mysterious": "enigmatic, eerie, slow build, ambient, cinematic",
    "Cheerful": "quirky, bouncy, fun, upbeat, cartoonish",
    "Tense": "suspenseful, edgy, sharp, fast-paced, unstable",
    "Dreamy": "soft, ambient, floating, surreal, spaced-out",
    "Triumphant": "victorious, bold, inspiring, orchestral, rising"
}

GENDER_PRESETS = {
    "Male":  "male vocals, deep tone, masculine",
    "Female": "female vocals, light tone, feminine",
    # "Instrumental": "instrumental, no vocals",
    "Duet": "male and female vocals, duet, blended harmonies",
}
