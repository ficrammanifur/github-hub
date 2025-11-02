import requests
import os
import sys

# -----------------------
# Config
# -----------------------
username = "ficrammanifur"
token = os.getenv("GH_TOKEN")
if not token:
    print("Error: GH_TOKEN environment variable not set!")
    sys.exit(1)

# -----------------------
# Kategori repositori (diperluas dan disesuaikan dengan format contoh)
# -----------------------
# Kategori utama dengan tabel (Featured Projects adalah subset dari Projects & Misc)
categories = {
    "Web & Frontend": [
        "ficram-portfolio",
        "flutter-interactive-portfolio",
        "flutter-project",
        "frontend",
        "PORTFOLIOO",
        "pemilu-himate-login",
        "himate-evote"
    ],
    "Backend & API": [
        "tofico-analyzer-backend",
        "backend",
        "my-fastap-app"
    ],
    "Robotics & IoT": [
        "robot-autonomous-hexapod-ros2-esp32",
        "Robothand_pt2",
        "Control-Motor-With-DABBLE-APP",
        "esp32-drone",
        "Gesture-Clone-Robot",
        "PakanIkanOtomatsi",
        "esp32-cam-tools",
        "pico-test",
        "Robohand",
        "robot-wall-folower",
        "smart-robotic-arm",
        "raspi-labs",
        "MQTT_ESP32_cam",
        "Pakan-Ayam-Otomatis",
        "esp32_control_led-ldr-pir-localhost",
        "Esp32-mqtt-project",
        "JemuranIot"
    ],
    "Machine Learning & AI": [
        "gemini_virtual_assistant",
        "detect-monkey-yolov8",
        "Predik-",
        "Google-Colab-YOLOv8",
        "deteksi-monyet",
        "yolo",
        "tets_ai",
        "ai_assistant",
        "Monitoring-Hama"
    ],
    "Tools & Scripts": [
        "tools-python",
        "coba-cpp",
        "DFS-test",
        "github-readme-streak-stats",
        "dynamic_modulation_oscilloscope",
        "lyrics-test"
    ],
    "Featured Projects": [  # Subset unggulan dari Projects & Misc
        "F1-Airflow-test-simulation",
        "Discover-Indonesia",
        "Real-Madrid-Match-Predictor"
    ]
}

# Emoji per kategori untuk deskripsi jika kosong (opsional, untuk estetika)
category_emojis = {
    "Web & Frontend": "🌐",
    "Backend & API": "🛠️",
    "Robotics & IoT": "🤖",
    "Machine Learning & AI": "🧠",
    "Tools & Scripts": "🛠️",
    "Featured Projects": "📦"
}

# -----------------------
# Ambil semua repo
# -----------------------
response = requests.get(
    f"https://api.github.com/user/repos?per_page=100&sort=updated",
    headers={"Authorization": f"token {token}"}
)
if response.status_code != 200:
    print("Error fetching repos:", response.status_code, response.text)
    sys.exit(1)
repos = response.json()
if not isinstance(repos, list):
    print("Unexpected API response:", repos)
    sys.exit(1)

# -----------------------
# Fungsi helper untuk mendapatkan deskripsi dengan fallback
# -----------------------
def get_description(repo, category):
    desc = repo.get("description", "").strip()
    if not desc:
        emoji = category_emojis.get(category, "")
        desc = f"{emoji} Project description not available"
    return desc

# -----------------------
# Tulis README.md dengan format tabel dan list
# -----------------------
with open("README.md", "w", encoding="utf-8") as f:
    # Header
    f.write('<div align="center">\n')
    f.write('# 🚀 GitHub Hub\n')
    f.write(f'> Daftar lengkap repositori saya — diperbarui otomatis\n')
    f.write('</div>\n')
    f.write('---\n\n')

    # Loop per kategori utama (tabel)
    for category, repo_names in categories.items():
        f.write(f'## {category_emojis.get(category, "📂")} {category}\n')
        f.write('| Repo | Deskripsi |\n')
        f.write('|------|-----------|\n')
        found_any = False
        for repo in repos:
            if repo.get("name") in repo_names:
                name = repo.get("name", "No name")
                url = repo.get("html_url", "#")
                desc = get_description(repo, category)
                f.write(f'| [{name}]({url}) | {desc} |\n')
                found_any = True
        if not found_any:
            f.write('| _No repositories in this category_ | _N/A_ |\n')
        f.write('\n')

    # Other Projects (list sederhana untuk uncategorized dan sisanya)
    all_category_names = [name for names in categories.values() for name in names]
    other_repos = [repo for repo in repos if repo.get("name") not in all_category_names]
    if other_repos:
        f.write('## 🎮 Other Projects\n')
        for repo in sorted(other_repos, key=lambda r: r.get("name", "")):
            name = repo.get("name", "No name")
            url = repo.get("html_url", "#")
            desc = get_description(repo, "Other Projects")
            f.write(f'- [{name}]({url}) — {desc}\n')
        f.write('\n')

    # Footer
    f.write('---\n')
    f.write('<div align="center">\n')
    f.write('### 🔗 Connect\n')
    f.write(f'Kunjungi [profile GitHub saya](https://github.com/{username}) untuk melihat lebih banyak\n')
    f.write('</div>\n')

print("✅ README.md updated successfully with table format!")
