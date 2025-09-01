[phases.setup]
nixPkgs = ["python3", "gcc"]

[phases.install]
commands = [
    "python -m venv /opt/venv",
    ". /opt/venv/bin/activate && pip install -r requirements.txt"
]

[start]
cmd = "python -m bot.main"