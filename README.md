# AI-Based Voice Cloning System

A Python application that generates speech from user-provided text in a voice that mimics the speaking style of a supplied reference audio recording. Built with **Kokoro-ONNX** (text-to-speech engine) and **Kanade-ONNX** (voice-style tokenizer), running on CUDA or CPU via ONNX Runtime.

> ⚠️ **Ethical use notice**: Only use voice recordings that you own or have explicit permission to clone. Unauthorized voice cloning can be illegal in many jurisdictions and is a violation of consent.

---

## Features

- **Reference audio input** with format (`.wav`, `.flac`, `.mp3`, `.ogg`, `.m4a`), size (< 25 MB), and duration (3–30 s) validation.
- **Text input** validation: rejects empty strings and text over 500 characters.
- **Speech generation** using pretrained **Kokoro-ONNX** + **Kanade-ONNX** models.
- **Gradio web UI** for upload → generate → play → download.
- **Command-line interface** for scripted generation.
- **Chunked inference** that automatically splits long audio to fit within available VRAM (works on a 6 GB laptop GPU).
- **User-friendly error messages** for invalid inputs and model inference failures.

---

## Architecture

| Component | Role |
|---|---|
| **Kanade-ONNX** | Extracts voice-style tokens (prosody, rhythm, pitch contour) from the reference audio. |
| **Kokoro-ONNX** | Synthesizes speech from text, conditioned on the style tokens. |
| **Misaki + spaCy** | Converts text to phonemes (grapheme-to-phoneme). |
| **ONNX Runtime** | Executes the ONNX models on CUDA (preferred) or CPU (fallback). |
| **Gradio** | Web interface for upload, playback, and download. |

> **Note on what this project clones**: KokoClone performs **style transfer**, not timbre cloning. The generated voice inherits the *rhythm and prosody* of the reference but uses one of Kokoro's built-in voices for timbre. For true zero-shot voice cloning (matching vocal identity), models such as **XTTS-v2**, **OpenVoice v2**, or **F5-TTS** would be required.

---

## Project Structure
AI-Based-Voice-Cloning-System/
├── app.py # Gradio web interface
├── cli.py # Command-line interface
├── inference.py # Direct programmatic inference
├── validation.py # Audio and text input validation
├── core/
│ ├── init.py
│ ├── cloner.py # KokoClone main class
│ └── chunked_convert.py # VRAM-aware audio chunking
├── samples/
│ ├── reference.wav # Authorized reference recording (own voice)
│ ├── generated_output.wav
│ └── generated_long_demo.wav
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── LICENSE
└── README.md

text

---

## Requirements

- **Python 3.12–3.13**
- **Windows / Linux / macOS**
- **GPU** (optional): CUDA 12.x compatible NVIDIA GPU with ≥ 6 GB VRAM. CPU fallback works but is slower.
- **Disk**: ~5 GB for the virtual environment, ~150 MB for the project and models.
- **Network**: Internet access on first run to download models from Hugging Face.

---

## Installation

### 1. Clone and enter the project

```bash
git clone https://github.com/EaruvaTeja/AI-Based-Voice-Cloning-System.git
cd AI-Based-Voice-Cloning-System
2. Create a virtual environment
bash
python -m venv venv

# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
3. Install PyTorch (CUDA build)
bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu128
For CPU-only: pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

4. Install pinned spaCy and misaki
spaCy 4.0.0-dev fails to build on Windows. Pin 3.8.15.

bash
pip install spacy==3.8.15
pip install "misaki[en]" "spacy-curated-transformers<0.4" "spacy==3.8.15"
5. Install kokoro-onnx and the Kanade tokenizer
bash
pip install kokoro-onnx
pip install git+https://github.com/frothywater/kanade-tokenizer
6. Install GPU ONNX Runtime (CUDA 12 build)
The PyPI onnxruntime-gpu is built against CUDA 13 and will not load with torch cu128. Install the CUDA 12 build from Microsoft's index:

bash
pip uninstall onnxruntime -y
pip install --force-reinstall --no-deps "onnxruntime-gpu==1.27.0" --index-url https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/onnxruntime-cuda-12/pypi/simple/
Verify:

bash
python -c "import onnxruntime as ort; print(ort.get_available_providers())"
# Expected: ['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider']
7. Install the remaining dependencies
bash
pip install gradio huggingface_hub soundfile jsonargparse safetensors tqdm vocos
8. First run (auto-downloads models)
bash
python cli.py --text "Hello, this is a test." --lang en --ref samples/reference.wav --out samples/first_run.wav
If the network is unstable and downloads fail, pre-download these files manually:

File	Destination
wavlm_base_plus.pth from https://download.pytorch.org/torchaudio/models/wavlm_base_plus.pth	~/.cache/torch/hub/checkpoints/
voices-v1.0.bin from https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin	./voice/
Usage
Command-line interface
bash
python cli.py \
    --text "Your text goes here." \
    --lang en \
    --ref samples/reference.wav \
    --out samples/output.wav
Arguments:

Flag	Description
--text	Text to synthesize (max 500 chars).
--lang	Language code (en, ja, zh supported via misaki).
--ref	Path to reference audio (3–30 s).
--out	Output WAV path.
Example with validation:

bash
$ python cli.py --text "" --ref samples/reference.wav --out x.wav
[input-error] Text input is empty.
Web interface
bash
python app.py
Open http://127.0.0.1:7860 in a browser (do not use 0.0.0.0). Then:

Enter text in the textbox.

Select language.

Upload the reference audio.

Click Generate.

Play or download the generated audio.

Sample Outputs
File	Description
samples/reference.wav	Authorized reference recording (~20 s, own voice).
samples/generated_output.wav	Speech generated from reference.wav using a short English sentence.
samples/generated_long_demo.wav	Longer English paragraph demonstrating style transfer.
Limitations
Timbre mismatch: KokoClone transfers speaking style (prosody, rhythm, pauses) but not vocal identity. The timbre belongs to Kokoro's built-in voice bank, not the reference speaker. True timbre cloning requires a different model (XTTS-v2, OpenVoice v2, F5-TTS).

Reference length: Best results with 5–10 seconds of clean, single-speaker, quiet audio. Longer references can cause pitch drift.

Language coverage: Primarily English, Japanese, and Mandarin via misaki. Other languages may produce degraded output.

VRAM limit: On a 6 GB GPU, audio is chunked into ~7.4 s segments. Longer sentences are stitched, which can introduce minor artefacts at chunk boundaries.

Inference speed: ~1–2 seconds per short sentence on an RTX 4050. CPU-only runs are 5–10× slower.

Warnings: Two harmless warnings appear on every run:

TensorRT DLL not found → ONNX Runtime falls back to CUDA (still GPU).

FlashAttention not installed → Kanade falls back to PyTorch SDPA.

Troubleshooting
Symptom	Fix
ModuleNotFoundError: kanade_tokenizer	pip install git+https://github.com/frothywater/kanade-tokenizer
spacy build fails	Pin spacy==3.8.15 (see Installation step 4).
onnxruntime falls back to CPU	Install onnxruntime-gpu==1.27.0 from the CUDA 12 index (step 6).
WinError 10054 during download	Download the file manually (see step 8).
Browser shows ERR_ADDRESS_INVALID	Use http://127.0.0.1:7860, not http://0.0.0.0:7860.
Ethical Use
This project is intended for authorized voice cloning only — research, personal projects, accessibility, and consensual content creation. Do not use it to impersonate individuals without their explicit permission, to create fraudulent audio, or to deceive others. Misuse may violate laws in your jurisdiction.

Acknowledgements
Kokoro-ONNX: github.com/thewh1teagle/kokoro-onnx

Kanade-Tokenizer: github.com/frothywater/kanade-tokenizer

KokoClone (reference implementation): github.com/Ashish-Patnaik/kokoclone

License
See LICENSE.