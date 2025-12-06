import json
import itertools
from send_out import send_fish, get_message
from utils_parram import post_image_sto_v2, conver_time_epoch_to_date, remove_data, download_audio_file, download_link_youtube
from logics.vc import *
import json
from logics.models import get_or_load_vc_model, get_or_load_acestep_model
from logics.config import *
from logics.t2m import *
import shutil

PATH_SAVE = "musicai_audio_cache"

cv_model = get_or_load_vc_model()
get_or_load = get_or_load_acestep_model()

# Đường dẫn tới file JSON
schema_path = "data_input_cache/t2m/schema.json"
lyrics_path = "data_input_cache/t2m/lyrics.json"
# Đọc nội dung file
f_schema = open(schema_path, "r")
data_schema = json.load(f_schema)

f_lyrics= open(lyrics_path, "r")
data_lyrics = json.load(f_lyrics)

print(data_schema)
print(data_lyrics)


duration = data_schema["duration"]["enum"]
genre = data_schema["genre"]["enum"]
emotion = data_schema["emotion"]["enum"]
gender = data_schema["gender"]["enum"]
recording = data_schema["recording"]["enum"]


# # Tạo tất cả tổ hợp (Cartesian product)
# combinations = itertools.product(duration, genre, emotion, gender, recording)
k = 0
# Duyệt qua từng tổ hợp và in ra
for ly in data_lyrics['lyrics']:
    id_ly = ly['id']
    print(id_ly)
    content_ly = ly['content']
    path_save = PATH_SAVE + "/t2m/" + str(id_ly) + "/"
    if not os.path.exists(path_save):
        os.makedirs(path_save)
    # content_ly = """[verse]
    #             Neon lights they flicker bright
    #             City hums in dead of night
    #             Rhythms pulse through concrete veins
    #             Lost in echoes of refrains
                
    #             [chorus]
    #             Turn it up and let it flow
    #             Feel the fire let it grow
    #             In this rhythm we belong
    #             Hear the night sing out our song
    #             """
    combinations = itertools.product(duration, genre, emotion, gender, recording)
    for combo in combinations:
        print(k)
        k += 1
        d, g, e, gender_val, r = combo
        d = int(d)
        path_save_s = path_save + "musict2m_" + str(d) + "_" + str(g) + "_" + str(e) + "_" + str(gender_val) + "_" + str(r) + ".wav"
        print("path_save", path_save_s)
        if not os.path.exists(path_save_s):
            genre_tags = GENRE_PRESETS.get(g, "")
            emotion_tags = EMOTION_PRESETS.get(e, "")
            gender_tags = GENDER_PRESETS.get(gender_val, "")
            tags = f"{genre_tags}, {emotion_tags}, {gender_tags}"
            audio_path = t2m_model('wav', d, tags, content_ly)
            print("audio_path", audio_path)
            shutil.move(audio_path, path_save_s)
        else:
            print("using cache")

# lyrics_path = "data_input_cache/cvm/link_json.json"
# path_audio = "data_input_cache/cvm/audio"
# # Đọc nội dung file
# f_covert = open(lyrics_path, "r")
# data_conver_link = json.load(f_covert)

# for audio in os.listdir(path_audio):
#     link_audio = path_audio + "/" + audio
#     for music in data_conver_link:
#         link_youtube = music['link']
#         id_music = music['id']
#         path_save = PATH_SAVE + "/cvm/" + str(id_music) 
#         if not os.path.exists(path_save):
#             os.makedirs(path_save)
#         path_save_audio_predict_vocal = path_save + "musiccvm_vocal_" + str(audio)
#         path_save_audio_predict_music = path_save + "musiccvm_music_" + str(audio)
#         path_save_audio_predict_vocal_music = path_save + "musiccvm_vocal_music_" + str(audio)

#         path_save_audio_original_youtube = "musicai_audio_cache/cvm/" + str(id_music) +  "_dowload_youtube.m4a"
#         if not os.path.exists(path_save_audio_original_youtube):
            
#             download_link_youtube(link_youtube, path_save_audio_original_youtube)
        
#         print("path_save", path_save_audio_predict_vocal_music)
#         if not os.path.exists(path_save_audio_predict_vocal_music):
#             final_mix_path, converted_path, instrumental_path = vc_pipeline(
#                             path_save_audio_predict_vocal,
#                             path_save_audio_predict_music,
#                             path_save_audio_predict_vocal_music,
#                             audio_filepath=path_save_audio_original_youtube,
#                             user_voice=link_audio,
#                             disable_watermark=True,
#                             pitch_shift=0,
#                             volume=0,
#                         )
#             # shutil.move(audio_path, path_save_s)
#         else:
#             print("using cache")
