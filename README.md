# AI-Based Voice Cloning System

A Python-based application that generates speech from user-provided text while mimicking the speaking style of a reference audio recording. The project uses **Kokoro-ONNX** for speech synthesis and **Kanade-ONNX** for voice-style extraction, with support for both GPU (CUDA) and CPU execution through ONNX Runtime.

> ⚠️ **Ethical Use Notice:** Only use voice recordings that you own or have explicit permission to clone. Unauthorized voice cloning may violate privacy, consent, and applicable laws.

---

## Features

- Upload a reference audio file (`.wav`, `.flac`, `.mp3`, `.ogg`, `.m4a`)
- Audio validation (format, size, and duration checks)
- Text input validation (empty text and length restrictions)
- Voice-style extraction using Kanade-ONNX
- Speech generation using Kokoro-ONNX
- Gradio-based web interface
- Command Line Interface (CLI) support
- Automatic chunked inference for limited GPU memory
- CUDA and CPU execution support
- Audio playback and download functionality
- User-friendly error handling and validation messages

---

## Project Demo

### Workflow

1. Upload a reference voice recording.
2. Enter the text to be synthesized.
3. Select the language.
4. Generate speech.
5. Listen to or download the generated audio.

---

## Architecture

| Component | Purpose |
|------------|------------|
| Kanade-ONNX | Extracts voice-style embeddings (prosody, rhythm, pitch patterns) |
| Kokoro-ONNX | Generates speech from text using extracted style information |
| Misaki + spaCy | Converts text into phoneme representations |
| ONNX Runtime | Executes the ONNX models on GPU or CPU |
| Gradio | Provides an interactive web interface |

### Voice Cloning Limitation

This project performs **style transfer**, not full voice identity cloning.

The generated speech reproduces:

- Speaking rhythm
- Prosody
- Pauses
- Pitch contours

The output still uses Kokoro's internal voice timbre.

For complete voice identity cloning, models such as:

- XTTS-v2
- OpenVoice v2
- F5-TTS

would be more suitable.

---

## Project Structure

```text
AI-Based-Voice-Cloning-System/
│
├── app.py
├── cli.py
├── inference.py
├── validation.py
│
├── core/
│   ├── __init__.py
│   ├── cloner.py
│   └── chunked_convert.py
│
├── samples/
│   ├── reference.wav
│   ├── generated_output.wav
│   └── generated_long_demo.wav
│
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── LICENSE
└── README.md
```

---

## Requirements

### Software

- Python 3.12 or 3.13
- Windows / Linux / macOS

### Hardware

**Optional GPU**

- NVIDIA GPU
- CUDA 12.x support
- Minimum 6 GB VRAM

**CPU**

- Fully supported (slower inference)

### Storage

- Approx. 5 GB virtual environment size
- Approx. 150 MB project files and models

### Network

- Internet connection required on first run to download model files

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/EaruvaTeja/AI-Based-Voice-Cloning-System.git
cd AI-Based-Voice-Cloning-System
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

---

### 3. Install PyTorch

#### CUDA Build

```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu128
```

#### CPU Build

```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

---

### 4. Install spaCy and Misaki

```bash
pip install spacy==3.8.15
pip install "misaki[en]" "spacy-curated-transformers<0.4" "spacy==3.8.15"
```

---

### 5. Install Kokoro-ONNX and Kanade Tokenizer

```bash
pip install kokoro-onnx
pip install git+https://github.com/frothywater/kanade-tokenizer
```

---

### 6. Install ONNX Runtime (CUDA 12)

```bash
pip uninstall onnxruntime -y

pip install --force-reinstall --no-deps \
onnxruntime-gpu==1.27.0 \
--index-url https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/onnxruntime-cuda-12/pypi/simple/
```

Verify installation:

```bash
python -c "import onnxruntime as ort; print(ort.get_available_providers())"
```

Expected Output:

```text
['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider']
```

---

### 7. Install Remaining Dependencies

```bash
pip install gradio huggingface_hub soundfile jsonargparse safetensors tqdm vocos
```

---

### 8. First Run

```bash
python cli.py \
--text "Hello, this is a test." \
--lang en \
--ref samples/reference.wav \
--out samples/first_run.wav
```

Models will automatically download during the first execution.

---

## Command-Line Usage

```bash
python cli.py \
--text "Your text goes here." \
--lang en \
--ref samples/reference.wav \
--out samples/output.wav
```

### Arguments

| Argument | Description |
|-----------|-------------|
| --text | Input text (max 500 characters) |
| --lang | Language code (en, ja, zh) |
| --ref | Reference audio path |
| --out | Output WAV file path |

### Example Validation Error

```bash
python cli.py --text "" --ref samples/reference.wav --out output.wav
```

Output:

```text
[input-error] Text input is empty.
```

---

## Web Interface

Launch the Gradio application:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:7860
```

### Steps

1. Enter text.
2. Select language.
3. Upload reference audio.
4. Click **Generate**.
5. Listen or download the generated audio.

---

## Sample Outputs

| File | Description |
|--------|------------|
| reference.wav | Original authorized reference voice |
| generated_output.wav | Example generated speech |
| generated_long_demo.wav | Long-form style transfer example |

---

## Performance

| Hardware | Expected Speed |
|-----------|---------------|
| RTX 4050 (6GB) | ~1-2 seconds per short sentence |
| CPU Only | 5-10× slower |

---

## Limitations

### Voice Identity

The project transfers speaking style rather than speaker identity.

### Reference Audio Quality

Best results are obtained with:

- 5-10 seconds duration
- Single speaker
- Minimal background noise
- Clear pronunciation

### Supported Languages

Currently optimized for:

- English
- Japanese
- Mandarin Chinese

### VRAM Constraints

On 6 GB GPUs, long audio synthesis is automatically split into chunks, which may introduce minor stitching artifacts.

---

## Troubleshooting

| Issue | Solution |
|---------|------------|
| ModuleNotFoundError: kanade_tokenizer | Install Kanade tokenizer from GitHub |
| spaCy build failure | Use spaCy 3.8.15 |
| ONNX Runtime using CPU | Install CUDA 12 GPU build |
| WinError 10054 | Download model files manually |
| ERR_ADDRESS_INVALID | Use http://127.0.0.1:7860 |

---

## Ethical Use

This project is intended for:

- Research
- Education
- Accessibility
- Personal projects
- Consensual content creation

Do not use this project to:

- Impersonate individuals
- Create fraudulent audio
- Spread misinformation
- Generate unauthorized cloned voices

Users are responsible for ensuring compliance with local laws and obtaining appropriate permissions.

---

## Acknowledgements

- Kokoro-ONNX  
  https://github.com/thewh1teagle/kokoro-onnx

- Kanade Tokenizer  
  https://github.com/frothywater/kanade-tokenizer

- KokoClone Reference Implementation  
  https://github.com/Ashish-Patnaik/kokoclone

---

## License

This project is provided under the license specified in the LICENSE file.
