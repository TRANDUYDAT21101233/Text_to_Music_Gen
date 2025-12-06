import gradio as gr
import traceback

from logics.models import get_or_load_acestep_model

def t2m_process_wrapper(format, audio_duration, prompt, lyrics, **kwargs):
    try:
        model = get_or_load_acestep_model()
        print(f"🎶 Generating music from text: '{prompt[:50]}...'")
        audio_path, metadata = model(format, audio_duration, prompt, lyrics, **kwargs)
        print("✅ Music generation finished.")
        return audio_path
    except Exception as e:
        traceback.print_exc()
        raise gr.Error(f"Error during music generation: {e}")

def t2m_model(format, audio_duration, prompt, lyrics, infer_step=60, guidance_scale=15.0, scheduler_type="euler",
                cfg_type="apg", omega_scale=20.0, manual_seeds=None,
                guidance_interval=0.5, guidance_interval_decay=0.0,
                min_guidance_scale=3.0, use_erg_tag=False, use_erg_lyric=False,
                use_erg_diffusion=False, oss_steps="", guidance_scale_text=0.0,
                guidance_scale_lyric=0.0, audio2audio_enable=False,
                ref_audio_strength=0.5, ref_audio_input=None,
                lora_name_or_path="none", lora_weight=1.0):
    # try:
    model = get_or_load_acestep_model()
    audio_path, _ = model(format, audio_duration, prompt, lyrics, infer_step=60, guidance_scale=15.0, scheduler_type="euler",
            cfg_type="apg", omega_scale=20.0, manual_seeds=None,
            guidance_interval=0.5, guidance_interval_decay=0.0,
            min_guidance_scale=3.0, use_erg_tag=False, use_erg_lyric=False,
            use_erg_diffusion=False, oss_steps="", guidance_scale_text=0.0,
            guidance_scale_lyric=0.0, audio2audio_enable=False,
            ref_audio_strength=0.5, ref_audio_input=None,
            lora_name_or_path="none", lora_weight=1.0)
    return audio_path
    # except Exception as e:
    #     raise print("cannot solve")

