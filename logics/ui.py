import traceback

import gradio as gr
from logics.config import LYRIC_DEFAULT, GENRE_PRESETS
from logics.t2m import t2m_process_wrapper

from logics.vc import handle_vc_input, vc_pipeline


def create_voice_conversion_ui():

    with gr.Column():
        gr.Markdown("<h1>🎤 Convert Any Song into Your Voice</h1>")
        gr.Markdown("Upload a song or paste a YouTube link, provide a voice sample, and hear the magic!")

        with gr.Row():
            with gr.Column(scale=1):
                input_type = gr.Radio(["Upload Audio", "YouTube Link"], value="Upload Audio", label="Choose Input Type")

                youtube_link = gr.Textbox(label="YouTube Link", placeholder="https://www.youtube.com/watch?v=...", visible=False)
                gr.Examples(
                    examples=[
                        ["https://youtu.be/orJSJGHjBLI?si=kM9ylFUrdvzql6EF"],
                        ["https://youtu.be/dQw4w9WgXcQ?si=OUryR1fysDn37PS9"]
                    ],
                    inputs=[youtube_link],
                    label="🎬 Example YouTube Links"
                )

                uploaded_audio = gr.Audio(sources=["upload"], type="filepath", label="Upload Your Favorite Song", visible=True)
                gr.Examples(
                    examples=[
                        ["assets/audio/SongGio.mp3"],
                    ],
                    inputs=[uploaded_audio],
                    label="🎵 Example Songs to Upload"
                )

                user_voice = gr.Audio(sources=["upload", "microphone"], type="filepath", label="Your Voice Sample (1-2 min recommended)")
                gr.Examples(
                    examples=[
                        ["assets/voice/CaptainAmerica.mp3"],
                        ["assets/voice/DoMixi.wav"],
                        ["assets/voice/DonaldTrump.wav"],
                        ["assets/voice/IronMan.mp3"],
                        ["assets/voice/KhaBanh.wav"],
                        ["assets/voice/Ronaldo.mp3"],
                        ["assets/voice/SonTungMTP.wav"],
                        ["assets/voice/Thaygiaoba.wav"],
                    ],
                    inputs=[user_voice],
                    label="🗣️ Example Voices"
                )

                with gr.Accordion("Advanced Settings", open=False):
                    pitch_input = gr.Number(value=0, label="Pitch Shift (semitones)", step=1)
                    watermark_checkbox = gr.Checkbox(label="Disable Watermark", value=True)
                    gain_slider = gr.Slider(-30, 10, value=-10, step=1, label="Vocal Gain (dB)")

                convert_button = gr.Button("Convert Song", variant="primary")

            with gr.Column(scale=1):
                gr.Markdown("<h3>Outputs</h3>")
                final_output = gr.Audio(label="Final Song with Your Voice")
                converted_vocals = gr.Audio(label="Converted Vocals Only")
                instrumental_out = gr.Audio(label="Instrumental Only")

        def run_vc_pipeline_gradio(input_type, yt_link, up_audio, voice_sample, disable_watermark, pitch, gain):
            try:
                if not voice_sample: raise gr.Error("You must provide a voice sample!")
                input_audio = handle_vc_input(input_type, yt_link, up_audio)

                output_paths = vc_pipeline(input_audio, voice_sample, disable_watermark, pitch, gain)

                print(f"✅ Returning paths to Gradio: {output_paths}")
                return output_paths

            except ValueError as e:
                raise gr.Error(str(e))
            except Exception as e:
                traceback.print_exc()
                raise gr.Error(f"An unexpected error occurred: {str(e)}")

        gr.Markdown("---")
        gr.Markdown("### ✨ Click an example to try it out! ✨")
        gr.Examples(
            examples=[
                [
                    "Upload Audio",
                    "",
                    "assets/audio/SongGio.mp3",
                    "assets/voice/KhaBanh.wav",
                    True,
                    0,
                    -3
                ],
                [
                    "Upload Audio",
                    "",
                    "assets/audio/SongGio.mp3",
                    "assets/voice/SonTungMTP.wav",
                    True,
                    0,
                    -5
                ],

                [
                    "YouTube Link",
                    "https://youtu.be/D5-ehZf-m_8?si=CiA7prVl1fM6qyvf",
                    None,
                    "assets/voice/KhaBanh.wav",
                    True,
                    0,
                    -3
                ],

                [
                    "YouTube Link",
                    "https://youtu.be/j8U06veqxdU?si=bcPysAAaWptqJHej",
                    None,
                    "assets/voice/DoMixi.wav",
                    True,
                    0,
                    -3
                ],

                [
                    "YouTube Link",
                    "https://www.youtube.com/watch?v=60ItHLz5WEA",
                    None,
                    "assets/voice/DonaldTrump.wav",
                    True,
                    0,
                    -3
                ],

                [
                    "YouTube Link",
                    "https://youtu.be/JGwWNGJdvx8?si=Nx-y2EyNect8qsO_",
                    None,
                    "assets/voice/DonaldTrump.wav",
                    True,
                    0,
                    -3
                ],

                [
                    "YouTube Link",
                    "https://youtu.be/orJSJGHjBLI?si=v37PMepOIc6hxRTG",
                    None,
                    "assets/voice/DonaldTrump.wav",
                    True,
                    0,
                    -3
                ],

                [
                    "YouTube Link",
                    "https://youtu.be/HUxDdmDd-u8?si=a4X_8i5whw_PKP-Z",
                    None,
                    "assets/voice/DoMixi.wav",
                    True,
                    0,
                    -3
                ]
            ],
            inputs=[input_type, youtube_link, uploaded_audio, user_voice, watermark_checkbox, pitch_input, gain_slider],
            outputs=[final_output, converted_vocals, instrumental_out],
            fn=run_vc_pipeline_gradio,
            cache_examples=True,
            label="Examples (YouTube examples may take time to load initially)"
        )


        def toggle_inputs(choice):
            return {youtube_link: gr.update(visible=choice == "YouTube Link"),
                    uploaded_audio: gr.update(visible=choice == "Upload Audio")}

        input_type.change(fn=toggle_inputs, inputs=[input_type], outputs=[youtube_link, uploaded_audio])

        convert_button.click(fn=run_vc_pipeline_gradio,
                             inputs=[input_type, youtube_link, uploaded_audio, user_voice, watermark_checkbox,
                                     pitch_input, gain_slider],
                             outputs=[final_output, converted_vocals, instrumental_out])


def create_text2music_ui():
    """Creates the Gradio UI components for the Text-to-Music tab."""
    with gr.Column():
        gr.Markdown("<h1>🎶 Generate Music from Text & Lyrics</h1>")
        gr.Markdown(
            "Use **Genre preset** to auto-fill tags, or choose `Custom` to write your own. Add lyrics to guide the generation. **Click an example below to start!**")
        with gr.Row():
            with gr.Column(scale=1):
                prompt_input = gr.Textbox(lines=2, label="Tags / Prompt", placeholder="e.g., pop, synth, 120 bpm...")
                lyrics_input = gr.Textbox(lines=10, max_lines=200, label="Lyrics", value=LYRIC_DEFAULT,
                                          placeholder="Write your lyrics here...")

                genre_preset = gr.Dropdown(choices=["Custom"] + list(GENRE_PRESETS.keys()), value="Custom",
                                           label="Genre Preset")
                audio_duration = gr.Slider(minimum=10.0, maximum=240.0, step=5.0, value=60.0,
                                           label="Audio Duration (seconds)")

                generate_btn = gr.Button("Generate Music", variant="primary")

            with gr.Column(scale=1):
                gr.Markdown("<h3>Generated Audio</h3>")
                output_audio = gr.Audio(type="filepath", label="Your Generated Song")

        # --- CORRECTLY CONFIGURED EXAMPLES TO LOAD PRE-EXISTING FILES ---
#         gr.Examples(
#             examples=[
#                 [
#                     "j-pop, anime opening, upbeat, energetic, female vocal, synth, electric guitar, 160 bpm",
#                     """[verse]
# 星空の下、駆け出す衝動
# 胸の鼓動が、未来へと続く合図
# 迷いの森で、見つけた光
# 君の笑顔が、勇気をくれる
#
# [chorus]
# さあ、飛び立て！無限の空へ
# この想い、風に乗せて
# 世界はこんなにも、鮮やかに輝く
# 僕らの物語、今始まるよ""",
#                     "assets/jpop_sample.wav"
#                 ],
#                 [
#                     "folk, acoustic, singer-songwriter, heartfelt, male vocal, acoustic guitar, strings, 110 bpm",
#                     """[verse]
# Sunrise paints the window pane
# Washing gold on summer rain
# Empty coffee cup you left
# A quiet echo, love bereft
#
# [chorus]
# Oh, the ghost of you and I
# Beneath this wide and lonely sky
# A simple tune, a faded rhyme
# Lost somewhere in the hands of time""",
#                     "assets/folk_sample.wav"
#                 ],
#                 [
#                     "k-pop, ballad, emotional, sentimental, piano, strings, female vocal, 70 bpm",
#                     """[verse]
# 비가 오는 이 거리에서
# 홀로 너를 기다려
# 우산 속에 숨겨진 눈물
# 아무도 모를 거야
#
# [chorus]
# 사랑했다, 널 사랑했다
# 가슴속에 외쳐본다
# 이젠 더는 닿을 수 없는
# 그 이름, 너라는 사람아""",
#                     "assets/kpop_sample.wav"
#                 ],
#                 [
#                     "russian rock, post-punk, melancholic, driving bass, raw guitar, male vocal, 140 bpm",
#                     """[verse]
# Стены серых панельных домов
# В окне последний луч погас
# Город спит под тяжестью снов
# Это ночь для нас
#
# [chorus]
# Мы идём по пустым мостовым
# Фонари - молчаливый конвой
# Ветер поёт нам один мотив
# О том, что мы с тобой""",
#                     "assets/russian_sample.wav"
#                 ],
#                 [
#                     "gufeng, chinese traditional, elegant, sentimental, guzheng, dizi flute, female vocal, 65 bpm",
#                     """[verse]
# 月下独酌，影成双
# 清风拂面，一缕香
# 红尘往事，谁难忘
# 流年似水，慢慢淌
#
# [chorus]
# 一曲相思，为君唱
# 但愿人久，在身旁
# 看尽繁华，又何妨
# 执手相看，泪两行""",
#                     "assets/gufeng_sample.wav"
#                 ],
#             ],
#             fn=load_example,
#             inputs=[prompt_input, lyrics_input, output_audio],
#             outputs=[prompt_input, lyrics_input, output_audio],
#             cache_examples=True,
#             label="Examples (Click to fill in and hear demo)"
#         )

        genre_preset.change(fn=update_tags_from_genre, inputs=[genre_preset], outputs=[prompt_input])

        generate_btn.click(
            fn=lambda duration, p, l: t2m_process_wrapper(
                "wav", duration, p, l,
                infer_step=60, guidance_scale=15.0, scheduler_type="euler",
                cfg_type="apg", omega_scale=20.0, manual_seeds=None,
                guidance_interval=0.5, guidance_interval_decay=0.0,
                min_guidance_scale=3.0, use_erg_tag=False, use_erg_lyric=False,
                use_erg_diffusion=False, oss_steps="", guidance_scale_text=0.0,
                guidance_scale_lyric=0.0, audio2audio_enable=False,
                ref_audio_strength=0.5, ref_audio_input=None,
                lora_name_or_path="none", lora_weight=1.0
            ),
            inputs=[audio_duration, prompt_input, lyrics_input],
            outputs=[output_audio],
        )


# def load_example(prompt, lyrics, audio_path):
#     print(f"Loading example: '{prompt[:50]}...', with audio '{audio_path}'")
#     return prompt, lyrics, audio_path


def update_tags_from_genre(preset):
    if preset == "Custom":
        return gr.update(value="", interactive=True)
    return gr.update(value=GENRE_PRESETS.get(preset, ""), interactive=True)
