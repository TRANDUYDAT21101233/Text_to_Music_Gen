import gradio as gr
import yt_dlp
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from logics.models import get_or_load_vc_model
from yt_dlp import YoutubeDL, DownloadError
import shutil
import os
import uuid
import subprocess
import tempfile
from urllib.parse import urlparse, parse_qs

import librosa
import numpy as np
import soundfile as sf
from pydub import AudioSegment
from yt_dlp import YoutubeDL, DownloadError


def is_playlist(url):
    query = parse_qs(urlparse(url).query)
    return 'list' in query


def extract_audio(youtube_url: str, duration_limit: int = 300) -> str:
    if is_playlist(youtube_url):
        raise ValueError("❌ Playlist detected. Please provide a single YouTube video link.")

    unique_id = uuid.uuid4().hex
    filename_base = f"yt_audio_{unique_id}"

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, filename_base)

        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'outtmpl': output_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }],
            'download_sections': ['*00:00-05:00'],
            # 'external_downloader': 'aria2c',
            # 'external_downloader_args': ['-x', '16', '-k', '1M'],
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
        except DownloadError as e:
            raise RuntimeError(f"❌ Download failed: {e}")
        except Exception as e:
            raise RuntimeError(f"❌ Unexpected error during download: {e}")

        final_path = output_path + ".m4a"

        if not os.path.exists(final_path):
            raise FileNotFoundError(f"❌ Audio file not found after yt_dlp processing: {final_path}")

        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        output_file = os.path.join(output_dir, f"{filename_base}.m4a")
        os.rename(final_path, output_file)

        return output_file


def convert_to_wav(input_path, output_path="input_song.wav"):
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format="wav")
    return output_path


def run_demucs(input_wav_path):
    try:
        subprocess.run(
            ["demucs", "-n", "htdemucs", "--two-stems=vocals", input_wav_path, "-o", "out"],
            # ["demucs", "-n", "mdx_extra_q", "--two-stems=vocals", input_wav_path, "-o", "out"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"❌ Demucs failed: {e.stderr}")


def voice_conversion_chunked(input_audio_path, target_voice_audio_path, chunk_sec=30, overlap_sec=0.1,
                              disable_watermark=True, pitch_shift=0):
    vc_model = get_or_load_vc_model()
    model_sr = vc_model.sr

    wav, sr = sf.read(input_audio_path)
    if wav.ndim > 1:
        wav = wav.mean(axis=1)
    if sr != model_sr:
        wav = librosa.resample(wav.astype(np.float32), orig_sr=sr, target_sr=model_sr)
        sr = model_sr

    total_sec = len(wav) / model_sr

    if total_sec <= chunk_sec:
        wav_out = vc_model.generate(
            input_audio_path,
            target_voice_path=target_voice_audio_path,
            apply_watermark=not disable_watermark,
            pitch_shift=pitch_shift
        )
        out_wav = wav_out.squeeze().cpu().numpy()
        return model_sr, out_wav

    chunk_samples = int(chunk_sec * model_sr)
    overlap_samples = int(overlap_sec * model_sr)
    step_samples = chunk_samples - overlap_samples
    out_chunks = []

    for start in range(0, len(wav), step_samples):
        end = min(start + chunk_samples, len(wav))
        chunk = wav[start:end]
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_chunk:
            sf.write(temp_chunk.name, chunk, model_sr)
            out_chunk = vc_model.generate(
                temp_chunk.name,
                target_voice_path=target_voice_audio_path,
                apply_watermark=not disable_watermark,
                pitch_shift=pitch_shift
            )
        os.remove(temp_chunk.name)
        out_chunk_np = out_chunk.squeeze().cpu().numpy()
        out_chunks.append(out_chunk_np)

    result = out_chunks[0]
    for i in range(1, len(out_chunks)):
        overlap = min(overlap_samples, len(out_chunks[i]), len(result))
        if overlap > 0:
            fade_out = np.linspace(1, 0, overlap)
            fade_in = np.linspace(0, 1, overlap)
            result[-overlap:] = result[-overlap:] * fade_out + out_chunks[i][:overlap] * fade_in
            result = np.concatenate([result, out_chunks[i][overlap:]])
        else:
            result = np.concatenate([result, out_chunks[i]])

    return model_sr, result



def vc_pipeline( path_save_audio_predict_vocal,
                path_save_audio_predict_music,
                path_save_audio_predict_vocal_music,audio_filepath, 
                user_voice, disable_watermark=True, pitch_shift=0, volume=-10):
    
    os.makedirs("out", exist_ok=True)
    os.makedirs("test", exist_ok=True)
    path_youtube_wav = "input_song.wav"

    input_wav_path = convert_to_wav(audio_filepath, path_youtube_wav)

    print("🔄 Running Demucs...")
    run_demucs(input_wav_path)

    base_name = os.path.splitext(os.path.basename(input_wav_path))[0]
    vocal_path = f"out/htdemucs/{base_name}/vocals.wav"
    instrumental_path = f"out/htdemucs/{base_name}/no_vocals.wav"
    # shutil.move(vocal_path, path_save_audio_predict_vocal)
    shutil.move(instrumental_path, path_save_audio_predict_music)

    if not os.path.exists(vocal_path) or not os.path.exists(path_save_audio_predict_music):
        raise FileNotFoundError(
            f"❌ Demucs did not produce expected files: '{vocal_path}' and '{path_save_audio_predict_music}'.")

    print("🔄 Converting vocals to target voice...")
    sr, converted_vocals = voice_conversion_chunked(vocal_path, user_voice, disable_watermark=disable_watermark,
                                                    pitch_shift=pitch_shift)

    converted_path = path_save_audio_predict_vocal
    sf.write(converted_path, converted_vocals, sr)

    print("🔄 Mixing converted vocals with instrumental...")
    vocal = AudioSegment.from_file(converted_path)
    instrumental = AudioSegment.from_file(path_save_audio_predict_music)

    min_duration = min(len(vocal), len(instrumental))
    vocal = vocal[:min_duration]
    instrumental = instrumental[:min_duration]

    vocal += volume
    final_mix = instrumental.overlay(vocal)

    output_path = path_save_audio_predict_vocal_music
    final_mix.export(output_path, format="wav")

    print("✅ Pipeline finished successfully!")
    return output_path, converted_path, path_save_audio_predict_music


def handle_vc_input(input_type, youtube_link, uploaded_audio):
    if input_type == "YouTube Link" and youtube_link:
        print(f"📥 Downloading from YouTube: {youtube_link}")
        audio_path = extract_audio(youtube_link)
    elif input_type == "Upload Audio" and uploaded_audio:
        audio_path = uploaded_audio
    else:
        raise ValueError("Invalid input method or missing input. Please upload a file or provide a YouTube link.")
    return audio_path



