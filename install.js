module.exports = {
  requires: {
    bundle: "ai"
  },
  run: [
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        message: [
          "python -c \"from pathlib import Path; Path('env/.installed').unlink(missing_ok=True)\"",
          "uv pip install -r requirements.txt",
        ],
      },
    },
    {
      method: "script.start",
      params: {
        uri: "torch.js",
        params: {
          venv: "env",
          path: "app",
        },
      },
    },
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        message: "python -c \"import torch, gradio; from reverb_tts import TTS; from pathlib import Path; Path('env/.installed').touch(); print('Reverb-TTS dependencies verified. CUDA:', torch.cuda.is_available())\"",
      },
    },
    {
      when: "{{exists('app/env/.installed')}}",
      method: "input",
      params: {
        title: "Install Complete",
        description: "Reverb-TTS installed successfully. Click Start to launch the app (weights download on first start).",
      },
    },
  ],
}
