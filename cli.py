import argparse
import sys
from core.cloner import KokoClone
import sys
from validation import (
    validate_reference_audio,
    validate_text,
    validate_output_path,
)

def main() -> None:
    """Entry point for the KokoClone command-line tool."""
    parser = argparse.ArgumentParser(description="KokoClone: Zero-Shot Multilingual Voice Cloning")
    parser.add_argument(
        "--mode",
        choices=["tts", "convert"],
        default="tts",
        help="Operation mode: 'tts' (text → cloned speech) or 'convert' (audio → re-voiced speech)",
    )
    parser.add_argument("--text", type=str, help="[tts mode] Text to synthesize")
    parser.add_argument(
        "--lang",
        type=str,
        default="en",
        help="[tts mode] Language code (en, hi, fr, ja, zh, it, pt, es)",
    )
    parser.add_argument(
        "--source",
        type=str,
        help="[convert mode] Path to source audio file to re-voice (.wav)",
    )
    parser.add_argument("--ref", type=str, required=True, help="Path to reference voice audio file (.wav)")
    parser.add_argument("--out", type=str, default="output.wav", help="Output file path (.wav)")

    args = parser.parse_args()

    # ---- Input validation ----
    try:
        audio_info = validate_reference_audio(args.ref)
        clean_text = validate_text(args.text)
        out_path = validate_output_path(args.out)
    except (ValueError, FileNotFoundError) as exc:
        print(f"[input-error] {exc}", file=sys.stderr)
        sys.exit(1)

    print(
        f"[validation] reference={audio_info['duration_sec']}s "
        f"@ {audio_info['sample_rate']} Hz, "
        f"{audio_info['channels']} ch, {audio_info['size_mb']} MB"
    )
    print(f"[validation] text={len(clean_text)} characters")

    cloner = KokoClone()

    if args.mode == "tts":
        if not args.text:
            parser.error("--text is required when --mode is 'tts'")
        try:
            cloner.generate(
                text=clean_text,
                lang=args.lang,
                reference_audio=audio_info["path"],
                output_path=out_path,
            )
        except Exception as exc:
            print(f"[generation-error] {exc}", file=sys.stderr)
            sys.exit(2)

    elif args.mode == "convert":
        if not args.source:
            parser.error("--source is required when --mode is 'convert'")

        try:
            cloner.convert(
                source_audio=args.source,
                reference_audio=args.ref,
                output_path=args.out,
            )
        except Exception as exc:
            print(f"Error during voice conversion: {exc}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()