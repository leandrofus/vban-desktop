async function startVBAN() {
    const host = document.getElementById("host").value;
    const port = document.getElementById("port").value;
    const stream = document.getElementById("stream").value;
    const vban_path = document.getElementById("vban_path").value;

    await fetch("/vban/start", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({host, port, stream, vban_path})
    });
}

async function stopVBAN() {
    await fetch("/vban/stop", { method: "POST" });
}

// Inicializar inputs con configuración actual
fetch("/vban/status")
    .then(r => r.json())
    .then(cfg => {
        document.getElementById("host").value = cfg.host;
        document.getElementById("port").value = cfg.port;
        document.getElementById("stream").value = cfg.stream;
        document.getElementById("vban_path").value = cfg.vban_path;
    });

