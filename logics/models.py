import torch
from logics.config import DEVICE, ACESTEP_CHECKPOINT_PATH, USE_BF16, USE_TORCH_COMPILE, CPU_OFFLOAD, OVERLAPPED_DECODE

try:
    from chatterbox.src.chatterbox.vc import ChatterboxVC
    from acestep.pipeline_ace_step import ACEStepPipeline
except ImportError as e:
    print(f"Warning: Could not import custom libraries (chatterbox, acestep). {e}")
    print("The application will run, but model loading will fail.")

    class ChatterboxVC:
        @staticmethod
        def from_pretrained(device):
            raise NotImplementedError("ChatterboxVC library not found.")

    class ACEStepPipeline:
        def __init__(self, *args, **kwargs):
            raise NotImplementedError("ACEStepPipeline library not found.")
        def __call__(self, *args, **kwargs):
            raise NotImplementedError("ACEStepPipeline library not found.")

VC_MODEL = None
ACESTEP_MODEL = None

def get_or_load_vc_model():
    global VC_MODEL
    if VC_MODEL is None:
        print("🔄 Loading Voice Conversion model (ChatterboxVC)...")
        VC_MODEL = ChatterboxVC.from_pretrained(DEVICE)
        print("✅ Voice Conversion model loaded.")
    return VC_MODEL

def get_or_load_acestep_model():
    global ACESTEP_MODEL
    if ACESTEP_MODEL is None:
        print("🔄 Loading Text-to-Music model (ACEStep)...")
        ACESTEP_MODEL = ACEStepPipeline(
            checkpoint_dir=ACESTEP_CHECKPOINT_PATH,
            dtype="bfloat16" if USE_BF16 else "float32",
            torch_compile=USE_TORCH_COMPILE,
            cpu_offload=CPU_OFFLOAD,
            overlapped_decode=OVERLAPPED_DECODE
        )
        print("✅ Text-to-Music model loaded.")
    return ACESTEP_MODEL


def unload_vc_model():
    global VC_MODEL
    if VC_MODEL is not None:
        print("🧹 Unloading Voice Conversion model to free up memory...")
        del VC_MODEL
        VC_MODEL = None
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        print("✅ VC Model unloaded.")


def unload_acestep_model():
    global ACESTEP_MODEL
    if ACESTEP_MODEL is not None:
        print("🧹 Unloading Text-to-Music model to free up memory...")
        del ACESTEP_MODEL
        ACESTEP_MODEL = None
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        print("✅ T2M Model unloaded.")