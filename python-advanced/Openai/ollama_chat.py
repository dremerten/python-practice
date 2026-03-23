#!/usr/bin/env python3

import argparse
import itertools
import json
import os
import sys
import threading
import time

import requests
from dotenv import load_dotenv

load_dotenv()

DEFAULT_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:4b")
REQUEST_TIMEOUT = 300

SYSTEM_PROMPT = (
    "You are a helpful assistant. "
    "Give informative but not too verbose answers. "
    "Keep responses short, usually 4 to 8 sentences. "
    "Be clear, direct, and practical."
)

MODELS = {
    "1": ("gemma3:4b", "fast"),
    "2": ("qwen2.5:7b", "balanced"),
    "3": ("deepseek-r1:8b", "slow reasoning"),
    "4": ("deepseek-v3.1", "heavier thinking model"),
}


class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"

    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"
    GRAY = "\033[90m"


def c(text: str, color: str) -> str:
    return f"{color}{text}{Color.RESET}"


class Spinner:
    def __init__(self, message: str = "Thinking"):
        self.message = message
        self._stop = threading.Event()
        self._thread = None

    def start(self) -> None:
        def run():
            for frame in itertools.cycle(["|", "/", "-", "\\"]):
                if self._stop.is_set():
                    break
                sys.stdout.write(f"\r{c(frame, Color.CYAN)} {self.message}...")
                sys.stdout.flush()
                time.sleep(0.1)
            sys.stdout.write("\r" + " " * 60 + "\r")
            sys.stdout.flush()

        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=1)


def build_payload(
    model: str,
    prompt: str,
    think=False,
    num_predict: int = 140,
    temperature: float = 0.2,
    num_ctx: int = 1024,
    num_thread: int = 4,
):
    return {
        "model": model,
        "prompt": prompt,
        "system": SYSTEM_PROMPT,
        "stream": True,
        "think": think,
        "keep_alive": "30m",
        "options": {
            "num_thread": num_thread,
            "num_predict": num_predict,
            "temperature": temperature,
            "num_ctx": num_ctx,
            "top_k": 20,
            "top_p": 0.9,
            "repeat_penalty": 1.1,
        },
    }


def ask_ollama(
    url: str,
    model: str,
    question: str,
    think=False,
    show_thinking=False,
    num_predict: int = 140,
    temperature: float = 0.2,
    num_ctx: int = 1024,
    num_thread: int = 4,
) -> None:
    payload = build_payload(
        model=model,
        prompt=question,
        think=think,
        num_predict=num_predict,
        temperature=temperature,
        num_ctx=num_ctx,
        num_thread=num_thread,
    )

    spinner = Spinner("Waiting for first token")
    start_time = time.time()
    first_token_time = None
    full_text = ""
    thinking_text = ""
    final_stats = None
    spinner_started = False
    answer_started = False
    thinking_started = False

    try:
        with requests.post(
            url,
            json=payload,
            stream=True,
            timeout=REQUEST_TIMEOUT,
        ) as response:
            response.raise_for_status()

            spinner.start()
            spinner_started = True

            for raw_line in response.iter_lines(decode_unicode=True):
                if not raw_line:
                    continue

                try:
                    data = json.loads(raw_line)
                except json.JSONDecodeError:
                    continue

                if first_token_time is None and (data.get("response") or data.get("thinking")):
                    first_token_time = time.time()
                    if spinner_started:
                        spinner.stop()
                        spinner_started = False

                if data.get("thinking"):
                    chunk = data["thinking"]
                    thinking_text += chunk
                    if show_thinking:
                        if not thinking_started:
                            print(c("\n--- THINKING ---\n", Color.MAGENTA))
                            thinking_started = True
                        print(c(chunk, Color.GRAY), end="", flush=True)

                if data.get("response"):
                    chunk = data["response"]
                    full_text += chunk
                    if not answer_started:
                        print(c("\n--- ANSWER ---\n", Color.GREEN))
                        answer_started = True
                    print(chunk, end="", flush=True)

                if data.get("done"):
                    final_stats = data
                    break

        if spinner_started:
            spinner.stop()

        end_time = time.time()
        print("\n")
        print(c("--- METRICS ---", Color.YELLOW))

        if first_token_time is not None:
            print(f"Time to first token: {first_token_time - start_time:.2f}s")
        else:
            print("Time to first token: n/a")

        print(f"Total wall time: {end_time - start_time:.2f}s")

        if final_stats:
            total_duration_ns = final_stats.get("total_duration", 0)
            load_duration_ns = final_stats.get("load_duration", 0)
            eval_duration_ns = final_stats.get("eval_duration", 0)
            prompt_eval_count = final_stats.get("prompt_eval_count", 0)
            eval_count = final_stats.get("eval_count", 0)

            print(f"API total duration: {total_duration_ns / 1e9:.2f}s")
            print(f"Model load duration: {load_duration_ns / 1e9:.2f}s")
            print(f"Input tokens: {prompt_eval_count}")
            print(f"Output tokens: {eval_count}")

            if eval_count and eval_duration_ns:
                tps = eval_count / (eval_duration_ns / 1e9)
                print(f"Output tokens/sec: {tps:.2f}")

        if not full_text.strip():
            print(c("Warning: no answer text was received.", Color.RED))

    except requests.exceptions.RequestException as exc:
        if spinner_started:
            spinner.stop()
        print(c(f"\nRequest failed: {exc}", Color.RED))
    except KeyboardInterrupt:
        if spinner_started:
            spinner.stop()
        print(c("\nInterrupted by user.", Color.RED))


def show_menu(current_model: str, url: str) -> None:
    print(c("\n" + "=" * 50, Color.BLUE))
    print(c(" OLLAMA CLI ", Color.BOLD + Color.CYAN))
    print(c("=" * 50, Color.BLUE))
    print(f"Model:    {current_model}")
    print(c("1.", Color.GREEN), "Ask a question")
    print(c("2.", Color.GREEN), "Switch model")
    print(c("3.", Color.GREEN), "Quit")
    print(c("=" * 50, Color.BLUE))


def switch_model(current_model: str) -> str:
    print(c("\nAvailable models:", Color.CYAN))
    for key, (name, desc) in MODELS.items():
        current = " <- current" if name == current_model else ""
        print(f"{key}. {name} ({desc}){current}")

    choice = input("\nSelect model: ").strip()
    if choice in MODELS:
        new_model = MODELS[choice][0]
        print(c(f"Switched to {new_model}", Color.GREEN))
        return new_model

    print(c("Invalid choice. Keeping current model.", Color.RED))
    return current_model


def parse_args():
    parser = argparse.ArgumentParser(
        description="Interactive Ollama CLI with colors, spinner, and flags."
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help="Ollama generate endpoint URL",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="Model name",
    )
    parser.add_argument(
        "--ask",
        help="Ask a single question directly without opening the menu",
    )
    parser.add_argument(
        "--think",
        action="store_true",
        help="Enable thinking mode for supported models",
    )
    parser.add_argument(
        "--show-thinking",
        action="store_true",
        help="Print the thinking stream when available",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=140,
        help="Maximum generated tokens",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="Sampling temperature",
    )
    parser.add_argument(
        "--ctx",
        type=int,
        default=1024,
        help="Context window to request",
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=4,
        help="CPU threads to use",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print(c("Connected to Ollama CLI", Color.BOLD + Color.CYAN))
    print(f"Model:    {args.model}")

    if args.ask:
        ask_ollama(
            url=args.url,
            model=args.model,
            question=args.ask,
            think=args.think,
            show_thinking=args.show_thinking,
            num_predict=args.max_tokens,
            temperature=args.temperature,
            num_ctx=args.ctx,
            num_thread=args.threads,
        )
    else:
        current_model = args.model
        while True:
            show_menu(current_model, args.url)
            choice = input("Select option: ").strip()

            if choice == "1":
                question = input("\nAsk something: ").strip()
                if question:
                    ask_ollama(
                        url=args.url,
                        model=current_model,
                        question=question,
                        think=args.think,
                        show_thinking=args.show_thinking,
                        num_predict=args.max_tokens,
                        temperature=args.temperature,
                        num_ctx=args.ctx,
                        num_thread=args.threads,
                    )
            elif choice == "2":
                current_model = switch_model(current_model)
            elif choice == "3":
                print(c("\nGoodbye.", Color.CYAN))
                break
            else:
                print(c("Invalid option.", Color.RED))


if __name__ == "__main__":
    main()