# Reverb-TTS (Pinokio launcher)

1-click launcher for [Reverb-TTS](https://huggingface.co/software-mansion/Reverb-TTS) by Software Mansion: a 297M-parameter TTS model that clones a voice from 3-10 s of speech plus its transcript. Supports English, German, French, Spanish, Italian, Polish and Portuguese.

Model weights are **CC BY-NC 4.0** (non-commercial only). Clone only voices you have the right to use.

## Usage

1. **Install**: creates `app/env`, installs `reverb-tts`, Gradio and the right PyTorch build for your GPU.
2. **Start**: launches the Gradio UI. Weights (~300 MB for int8) download from Hugging Face on first start.
3. In the UI, pick a **preset voice**, or choose **Clone a voice** and upload a 3-10 s reference clip with its exact transcript. Enter text, pick its language, then click **Generate**.

**Advanced** options: weights variant (`int8` default, `int4`, `fp16`, `fp32`), speed, sampler steps and seed.

## API

The UI exposes a `/generate` endpoint. Arguments are passed in this order: `text, language, mode, preset, ref_audio, ref_text, ref_language, variant, speed, steps, seed`. Replace the URL with the one shown in Pinokio.

### Python

```python
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
result = client.predict(
    "Hello from Reverb!", "English", "Preset voice", "en_male_narrator_1",
    None, "", "English", "int8", 1.0, 8, -1,
    api_name="/generate",
)
print(result)  # path to the generated wav
```

Cloning: pass `"Clone a voice"` as `mode`, `handle_file("ref.wav")` (from `gradio_client`) as `ref_audio`, and the transcript as `ref_text`.

### JavaScript

```javascript
import { Client } from "@gradio/client";

const client = await Client.connect("http://127.0.0.1:7860/");
const result = await client.predict("/generate", [
  "Hello from Reverb!", "English", "Preset voice", "en_male_narrator_1",
  null, "", "English", "int8", 1.0, 8, -1,
]);
console.log(result.data);
```

### Curl

```bash
curl -X POST http://127.0.0.1:7860/gradio_api/call/generate \
  -H "Content-Type: application/json" \
  -d '{"data": ["Hello from Reverb!", "English", "Preset voice", "en_male_narrator_1", null, "", "English", "int8", 1.0, 8, -1]}'
# returns {"event_id": "..."}; then:
curl -N http://127.0.0.1:7860/gradio_api/call/generate/<event_id>
```

### Direct Python (inside `app/env`)

```python
import soundfile as sf
from reverb_tts import TTS

tts = TTS.from_pretrained()
voice = tts.voice("reference.wav", "Exact transcript.", language="en")
sf.write("out.wav", tts.generate("Hello!", voice, language="en"), tts.sample_rate)
```
