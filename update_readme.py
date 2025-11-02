import requests
import os

username = "ficrammanifur"
token = os.getenv("GH_TOKEN")

# Ambil semua repo
response = requests.get(
    f"https://api.github.com/user/repos?per_page=100&sort=updated",
    headers={"Authorization": f"token {token}"}
)
repos = response.json()

# Tulis ulang README.md
with open("README.md", "w", encoding="utf-8") as f:
    f.write(f"# 🌐 {username}'s GitHub Hub\n\n")
    f.write("Daftar semua repositori saya, otomatis diperbarui 🚀\n\n")
    for repo in repos:
        name = repo["name"]
        url = repo["html_url"]
        desc = repo["description"] or ""
        f.write(f"- [{name}]({url}) — {desc}\n")

print("README.md updated successfully!")
