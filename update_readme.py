import requests
import os

# -----------------------
# Config
# -----------------------
username = "ficrammanifur"
token = os.getenv("GH_TOKEN")

# Kategori repositori
categories = {
    "Web & Frontend": [
        "ficram-portfolio",
        "flutter-interactive-portfolio",
        "flutter-project",
        "frontend"
    ],
    "Backend & API": [
        "backend",
        "my-fastap-app",
        "tofico-analyzer-backend"
    ],
    "Robotics & IoT": [
        "Robothand_pt2",
        "robot-autonomous-hexapod-ros2-esp32",
        "ESP32_cam_tools",
        "Control-Motor-With-DABBLE-APP"
    ],
    "Machine Learning & AI": [
        "detect-monkey-yolov8",
        "gemini_virtual_assistant",
        "Predik-"
    ],
    "Tools & Scripts": [
        "tools-python",
        "coba-cpp",
        "DFS-test"
    ],
    "Projects & Misc": [
        "Discover-Indonesia",
        "F1-Airflow-test-simulation",
        "JemuranIot"
    ]
}

# -----------------------
# Ambil semua repo
# -----------------------
response = requests.get(
    f"https://api.github.com/user/repos?per_page=100&sort=updated",
    headers={"Authorization": f"token {token}"}
)
repos = response.json()

# -----------------------
# Tulis README.md
# -----------------------
with open("README.md", "w", encoding="utf-8") as f:
    f.write(f"# 🌐 {username}'s GitHub Hub\n\n")
    f.write("Daftar semua repositori saya, otomatis diperbarui 🚀\n\n")
    
    # Loop per kategori
    for category, repo_names in categories.items():
        f.write(f"## {category}\n")
        found_any = False
        for repo in repos:
            if repo["name"] in repo_names:
                name = repo["name"]
                url = repo["html_url"]
                desc = repo["description"] or ""
                f.write(f"- [{name}]({url}) — {desc}\n")
                found_any = True
        if not found_any:
            f.write("_Tidak ada repositori di kategori ini_\n")
        f.write("\n")

    # Opsional: tambahkan repositori yang tidak termasuk kategori manapun
    uncategorized = [repo for repo in repos if all(repo["name"] not in r for r in categories.values())]
    if uncategorized:
        f.write("## Lain-lain\n")
        for repo in uncategorized:
            name = repo["name"]
            url = repo["html_url"]
            desc = repo["description"] or ""
            f.write(f"- [{name}]({url}) — {desc}\n")
        f.write("\n")

print("README.md updated successfully!")
