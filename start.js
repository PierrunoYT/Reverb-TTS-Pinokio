module.exports = {
  daemon: true,
  run: [
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        message: "python -u app.py",
        on: [{
          // Gradio's banner, not the first URL: weight downloads print HF URLs first.
          event: "/Running on local URL:\\s+(https?:\\/\\/\\S+)/",
          done: true
        }]
      }
    },
    {
      method: "local.set",
      params: {
        url: "{{input.event[1]}}"
      }
    },
  ]
}
