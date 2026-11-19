import os

import gradio as gr
from reverb_tts import TTS, SamplerConfig

LANGUAGES = {
    "English": "en",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Italian": "it",
    "Polish": "pl",
    "Portuguese": "pt",
}
VARIANTS = ["int8", "int4", "fp16", "fp32"]

_models = {}


def get_tts(variant):
    if variant not in _models:
        _models.clear()  # keep a single variant in memory
        _models[variant] = TTS.from_pretrained("software-mansion/Reverb-TTS", variant=variant)
    return _models[variant]


def synthesize(text, language, mode, preset, ref_audio, ref_text, ref_language, variant, speed, steps, seed):
    if not text or not text.strip():
        raise gr.Error("Enter some text to speak.")
    tts = get_tts(variant)
    if mode == "Preset voice":
        if not preset:
            raise gr.Error("Pick a preset voice.")
        voice = tts.preset_voice(preset)
    else:
        if not ref_audio:
            raise gr.Error("Upload or record a reference clip (3-10 s of clean speech).")
        if not ref_text or not ref_text.strip():
            raise gr.Error("Enter the exact transcript of the reference clip.")
        voice = tts.voice(ref_audio, ref_text, language=LANGUAGES[ref_language])
    audio = tts.generate(
        text,
        voice,
        language=LANGUAGES[language],
        seed=None if seed is None or seed < 0 else int(seed),
        speed=float(speed),
        sampler=SamplerConfig(steps=int(steps)),
    )
    return tts.sample_rate, audio


def preset_names():
    return get_tts(VARIANTS[0]).preset_voices()


with gr.Blocks(title="Reverb-TTS") as demo:
    gr.Markdown(
        "# Reverb-TTS\nZero-shot voice cloning in 7 languages. "
        "Weights: CC BY-NC 4.0 (non-commercial). Clone only voices you have the right to use."
    )
    with gr.Row():
        with gr.Column():
            text = gr.Textbox(label="Text", lines=6, value="Hello! This is Reverb speaking.")
            language = gr.Dropdown(list(LANGUAGES), value="English", label="Text language")
            mode = gr.Radio(["Preset voice", "Clone a voice"], value="Preset voice", label="Voice source")
            presets = preset_names()
            preset = gr.Dropdown(
                presets,
                value="en_male_narrator_1" if "en_male_narrator_1" in presets else (presets[0] if presets else None),
                label="Preset voice",
            )
            with gr.Group(visible=False) as clone_box:
                ref_audio = gr.Audio(label="Reference clip (3-10 s)", type="filepath", sources=["upload", "microphone"])
                ref_text = gr.Textbox(label="Exact transcript of the reference", lines=2)
                ref_language = gr.Dropdown(list(LANGUAGES), value="English", label="Reference language")
            with gr.Accordion("Advanced", open=False):
                variant = gr.Dropdown(VARIANTS, value="int8", label="Weights variant")
                speed = gr.Slider(0.5, 2.0, value=1.0, step=0.05, label="Speed")
                steps = gr.Slider(4, 32, value=8, step=1, label="Sampler steps")
                seed = gr.Number(value=-1, precision=0, label="Seed (-1 = random)")
            button = gr.Button("Generate", variant="primary")
        with gr.Column():
            output = gr.Audio(label="Output", type="numpy")

    mode.change(
        lambda m: (gr.update(visible=m == "Preset voice"), gr.update(visible=m == "Clone a voice")),
        mode,
        [preset, clone_box],
    )
    button.click(
        synthesize,
        [text, language, mode, preset, ref_audio, ref_text, ref_language, variant, speed, steps, seed],
        output,
        api_name="generate",
    )

if __name__ == "__main__":
    demo.queue().launch(server_name=os.environ.get("GRADIO_SERVER_NAME", "127.0.0.1"))
