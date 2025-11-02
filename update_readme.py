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
# Kategori repositori
# -----------------------
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

if response.status_code != 200:
    print("Error fetching repos:", response.status_code, response.text)
    sys.exit(1)

repos = response.json()
if not isinstance(repos, list):
    print("Unexpected API response:", repos)
    sys.exit(1)

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
            if repo.get("name") in repo_names:
                name = repo.get("name", "No name")
                url = repo.get("html_url", "#")
                desc = repo.get("description") or ""
                f.write(f"- [{name}]({url}) — {desc}\n")
                found_any = True
        if not found_any:
            f.write("_Tidak ada repositori di kategori ini_\n")
        f.write("\n")
    
    # Tambahkan repositori yang tidak termasuk kategori manapun
    all_category_names = [name for names in categories.values() for name in names]
    uncategorized = [repo for repo in repos if repo.get("name") not in all_category_names]
    if uncategorized:
        f.write("## Lain-lain\n")
        for repo in uncategorized:
            name = repo.get("name", "No name")
            url = repo.get("html_url", "#")
            desc = repo.get("description") or ""
            f.write(f"- [{name}]({url}) — {desc}\n")
        f.write("\n")

print("✅ README.md updated successfully!")
