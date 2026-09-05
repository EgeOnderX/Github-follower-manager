import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Multi-language Support (i18n)
LOCALES = {
    "English": {
        "title": "GitHub Follower Manager",
        "input_frame": " GitHub Credentials ",
        "username": "GitHub Username:",
        "token": "Personal Access Token:",
        "lang_label": "Language:",
        "theme_label": "Theme:",
        "opt1_btn": "Option 1: Non-Followers (Unfollow)",
        "opt2_btn": "Option 2: Followers You Don't Follow",
        "result_frame": " Results List ",
        "action_default": "Select an Option Above",
        "action_unfollow": "Unfollow All ({count})",
        "action_follow": "Follow Back All ({count})",
        "fetching": "Fetching data from GitHub... Please wait.",
        "processing": "Processing users... Please wait.",
        "btn_finished": "Completed",
        "err_username": "Please enter your GitHub username.",
        "err_token": "Personal Access Token is required for this action!",
        "confirm_action": "Are you sure you want to {action} {count} users?",
        "action_unfollow_text": "unfollow",
        "action_follow_text": "follow",
        "success_title": "Success",
        "success_msg": "Operation Completed!\n{success}/{total} users processed successfully."
    },
    "Türkçe": {
        "title": "GitHub Takipçi Yöneticisi",
        "input_frame": " GitHub Hesabı ve Yetkilendirme ",
        "username": "GitHub Kullanıcı Adı:",
        "token": "Personal Access Token:",
        "lang_label": "Dil / Language:",
        "theme_label": "Tema / Theme:",
        "opt1_btn": "Opsiyon 1: Geri Takip Etmeyenler",
        "opt2_btn": "Opsiyon 2: Takip Etmediğin Takipçiler",
        "result_frame": " Sonuç Listesi ",
        "action_default": "Yukarıdan Bir Seçenek Seçin",
        "action_unfollow": "Tümünü Takipten Çıkar ({count})",
        "action_follow": "Tümünü Geri Takip Et ({count})",
        "fetching": "GitHub'dan veriler çekiliyor... Lütfen bekleyin.",
        "processing": "Kullanıcılar işleniyor... Lütfen bekleyin.",
        "btn_finished": "İşlem Bitti",
        "err_username": "Lütfen kullanıcı adınızı girin.",
        "err_token": "Takip etme / çıkarma işlemi için Token gereklidir!",
        "confirm_action": "{count} kullanıcıyı {action} istediğinize emin misiniz?",
        "action_unfollow_text": "takipten çıkarmak",
        "action_follow_text": "takip etmek",
        "success_title": "Başarılı",
        "success_msg": "İşlem Tamamlandı!\n{success}/{total} kullanıcı işlendi."
    },
    "中文": {
        "title": "GitHub 关注者管理器",
        "input_frame": " GitHub 凭据与授权 ",
        "username": "GitHub 用户名:",
        "token": "个人访问令牌 (Token):",
        "lang_label": "语言 / Language:",
        "theme_label": "主题 / Theme:",
        "opt1_btn": "选项 1: 未回关用户 (取消关注)",
        "opt2_btn": "选项 2: 未关注的粉丝 (相互关注)",
        "result_frame": " 结果列表 ",
        "action_default": "请在上方选择一个选项",
        "action_unfollow": "取消关注全部 ({count})",
        "action_follow": "关注全部 ({count})",
        "fetching": "正在从 GitHub 获取数据... 请稍候。",
        "processing": "正在处理用户... 请稍候。",
        "btn_finished": "处理完成",
        "err_username": "请输入您的 GitHub 用户名。",
        "err_token": "执行关注/取消关注操作需要 Token！",
        "confirm_action": "确定要对 {count} 名用户执行 {action} 操作吗？",
        "action_unfollow_text": "取消关注",
        "action_follow_text": "关注",
        "success_title": "成功",
        "success_msg": "操作完成！\n已成功处理 {success}/{total} 名用户。"
    },
    "Deutsch": {
        "title": "GitHub Follower Manager",
        "input_frame": " GitHub Anmeldedaten ",
        "username": "GitHub-Benutzername:",
        "token": "Personal Access Token:",
        "lang_label": "Sprache:",
        "theme_label": "Design:",
        "opt1_btn": "Opt 1: Nicht-Follower (Entfolgen)",
        "opt2_btn": "Opt 2: Ausstehende Follower (Zurückfolgen)",
        "result_frame": " Ergebnisse ",
        "action_default": "Wählen Sie oben eine Option",
        "action_unfollow": "Allen entfolgen ({count})",
        "action_follow": "Allen zurückfolgen ({count})",
        "fetching": "Daten werden von GitHub abgerufen...",
        "processing": "Benutzer werden verarbeitet...",
        "btn_finished": "Abgeschlossen",
        "err_username": "Bitte geben Sie Ihren GitHub-Benutzernamen ein.",
        "err_token": "Personal Access Token ist erforderlich!",
        "confirm_action": "Möchten Sie wirklich {count} Benutzern {action}?",
        "action_unfollow_text": "entfolgen",
        "action_follow_text": "folgen",
        "success_title": "Erfolg",
        "success_msg": "Vorgang abgeschlossen!\n{success}/{total} Benutzer verarbeitet."
    }
}

THEMES = {
    "Dark": {
        "bg": "#1e1e1e",
        "fg": "#ffffff",
        "frame_bg": "#252526",
        "input_bg": "#3c3c3c",
        "input_fg": "#ffffff",
        "list_bg": "#2d2d2d",
        "list_fg": "#ffffff",
        "opt1_bg": "#b22222",
        "opt2_bg": "#104e8b",
        "action_bg": "#3fb950",  # Açık & Canlı Yeşil
        "action_disabled_bg": "#2d372e",
        "status_fg": "#aaa"
    },
    "Light": {
        "bg": "#f5f5f5",
        "fg": "#000000",
        "frame_bg": "#ffffff",
        "input_bg": "#ffffff",
        "input_fg": "#000000",
        "list_bg": "#ffffff",
        "list_fg": "#000000",
        "opt1_bg": "#d9534f",
        "opt2_bg": "#0275d8",
        "action_bg": "#2eb85c",  # Açık & Canlı Yeşil
        "action_disabled_bg": "#d0e3d4",
        "status_fg": "#555555"
    }
}

class GitHubFollowManager:
    def __init__(self, root):
        self.root = root
        self.current_lang = "English"
        self.current_theme = "Dark"
        self.active_mode = None
        self.current_data = []

        self.default_font = ("TkDefaultFont", 9)
        self.mono_font = ("Consolas" if os.name == "nt" else "Monospace", 10)

        self.root.geometry("640x670")
        self.root.minsize(600, 600)

        self._setup_ui()
        self.update_language(self.current_lang)
        self.apply_theme(self.current_theme)

    def t(self, key, **kwargs):
        text = LOCALES[self.current_lang].get(key, "")
        return text.format(**kwargs) if kwargs else text

    def _setup_ui(self):
        # Top Control Bar (Language & Theme)
        frame_top = tk.Frame(self.root, padx=10, pady=5)
        frame_top.pack(fill="x")
        self.frame_top = frame_top

        self.lbl_lang = tk.Label(frame_top, text="", font=self.default_font)
        self.lbl_lang.pack(side="left", padx=(0, 2))

        self.combo_lang = ttk.Combobox(
            frame_top, values=list(LOCALES.keys()), state="readonly", width=10
        )
        self.combo_lang.set(self.current_lang)
        self.combo_lang.pack(side="left", padx=(0, 15))
        self.combo_lang.bind("<<ComboboxSelected>>", lambda e: self.update_language(self.combo_lang.get()))

        self.lbl_theme = tk.Label(frame_top, text="", font=self.default_font)
        self.lbl_theme.pack(side="left", padx=(0, 2))

        self.combo_theme = ttk.Combobox(
            frame_top, values=["Dark", "Light"], state="readonly", width=8
        )
        self.combo_theme.set(self.current_theme)
        self.combo_theme.pack(side="left")
        self.combo_theme.bind("<<ComboboxSelected>>", lambda e: self.apply_theme(self.combo_theme.get()))

        # Credentials Input Frame
        self.frame_input = tk.LabelFrame(self.root, padx=10, pady=10)
        self.frame_input.pack(fill="x", padx=15, pady=5)

        self.lbl_username = tk.Label(self.frame_input)
        self.lbl_username.grid(row=0, column=0, sticky="w", pady=2)
        self.entry_username = tk.Entry(self.frame_input, width=32)
        self.entry_username.grid(row=0, column=1, pady=2, sticky="ew")

        self.lbl_token = tk.Label(self.frame_input)
        self.lbl_token.grid(row=1, column=0, sticky="w", pady=2)
        self.entry_token = tk.Entry(self.frame_input, width=32, show="*")
        self.entry_token.grid(row=1, column=1, pady=2, sticky="ew")

        self.frame_input.columnconfigure(1, weight=1)

        # Options / Fetch Buttons Frame
        frame_actions = tk.Frame(self.root)
        frame_actions.pack(fill="x", padx=15, pady=5)
        self.frame_actions = frame_actions

        self.btn_opt1 = tk.Button(
            frame_actions, command=lambda: self.start_thread(self.fetch_non_followers),
            fg="white", font=("Arial", 9, "bold"), pady=8, relief="flat", cursor="hand2"
        )
        self.btn_opt1.pack(side="left", expand=True, fill="x", padx=2)

        self.btn_opt2 = tk.Button(
            frame_actions, command=lambda: self.start_thread(self.fetch_fans),
            fg="white", font=("Arial", 9, "bold"), pady=8, relief="flat", cursor="hand2"
        )
        self.btn_opt2.pack(side="right", expand=True, fill="x", padx=2)

        # Status Indicator Label
        self.lbl_status = tk.Label(self.root, text="", font=("Arial", 9, "italic"))
        self.lbl_status.pack(fill="x", padx=15, pady=2)

        # Results List Box
        self.frame_list = tk.LabelFrame(self.root, padx=10, pady=10)
        self.frame_list.pack(fill="both", expand=True, padx=15, pady=5)

        self.listbox = tk.Listbox(self.frame_list, font=self.mono_font, relief="flat", highlightthickness=1)
        self.listbox.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.frame_list, orient="vertical", command=self.listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        # Bottom Action Button
        frame_bottom = tk.Frame(self.root)
        frame_bottom.pack(fill="x", padx=15, pady=10)
        self.frame_bottom = frame_bottom

        self.btn_action = tk.Button(
            frame_bottom, text="", state="disabled",
            font=("Arial", 10, "bold"), height=2, relief="flat", cursor="hand2"
        )
        self.btn_action.pack(fill="x")

    def update_language(self, lang):
        self.current_lang = lang
        self.root.title(self.t("title"))
        self.lbl_lang.config(text=self.t("lang_label"))
        self.lbl_theme.config(text=self.t("theme_label"))
        self.frame_input.config(text=self.t("input_frame"))
        self.lbl_username.config(text=self.t("username"))
        self.lbl_token.config(text=self.t("token"))
        self.btn_opt1.config(text=self.t("opt1_btn"))
        self.btn_opt2.config(text=self.t("opt2_btn"))
        self.frame_list.config(text=self.t("result_frame"))

        if self.current_data and self.active_mode:
            count = len(self.current_data)
            key = "action_unfollow" if self.active_mode == "unfollow" else "action_follow"
            self.btn_action.config(text=self.t(key, count=count))
        elif self.btn_action["state"] == "disabled" and self.btn_action["text"] != self.t("btn_finished"):
            self.btn_action.config(text=self.t("action_default"))

    def apply_theme(self, theme_name):
        self.current_theme = theme_name
        colors = THEMES[theme_name]

        self.root.config(bg=colors["bg"])
        self.frame_top.config(bg=colors["bg"])
        self.frame_actions.config(bg=colors["bg"])
        self.frame_bottom.config(bg=colors["bg"])

        for lbl in [self.lbl_lang, self.lbl_theme, self.lbl_username, self.lbl_token]:
            lbl.config(bg=colors["frame_bg"] if lbl in [self.lbl_username, self.lbl_token] else colors["bg"], fg=colors["fg"])

        self.lbl_status.config(bg=colors["bg"], fg=colors["status_fg"])

        for lf in [self.frame_input, self.frame_list]:
            lf.config(bg=colors["frame_bg"], fg=colors["fg"])

        for entry in [self.entry_username, self.entry_token]:
            entry.config(bg=colors["input_bg"], fg=colors["input_fg"], insertbackground=colors["fg"])

        self.listbox.config(bg=colors["list_bg"], fg=colors["list_fg"], highlightbackground=colors["bg"])

        self.btn_opt1.config(bg=colors["opt1_bg"])
        self.btn_opt2.config(bg=colors["opt2_bg"])

        if self.btn_action["state"] == "normal":
            self.btn_action.config(bg=colors["action_bg"], fg="white")
        else:
            self.btn_action.config(bg=colors["action_disabled_bg"], fg="#888888")

    def start_thread(self, target_function, *args):
        threading.Thread(target=target_function, args=args, daemon=True).start()

    def _set_ui_state(self, is_loading):
        state = "disabled" if is_loading else "normal"
        self.btn_opt1.config(state=state)
        self.btn_opt2.config(state=state)
        self.combo_lang.config(state="disabled" if is_loading else "readonly")
        self.combo_theme.config(state="disabled" if is_loading else "readonly")

    def _get_headers(self):
        token = self.entry_token.get().strip()
        headers = {"Accept": "application/vnd.github.v3+json"}
        if token:
            headers["Authorization"] = f"token {token}"
        return headers

    def _fetch_all_pages(self, url):
        items = []
        page = 1
        headers = self._get_headers()

        while True:
            try:
                res = requests.get(f"{url}?per_page=100&page={page}", headers=headers, timeout=10)
                if res.status_code != 200:
                    msg = res.json().get("message", "API Error")
                    self.root.after(0, lambda: messagebox.showerror("Error", f"API ({res.status_code}): {msg}"))
                    return None
                data = res.json()
                if not data:
                    break
                items.extend([user["login"] for user in data])
                page += 1
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", str(e)))
                return None

        return set(items)

    def fetch_non_followers(self):
        username = self.entry_username.get().strip()
        if not username:
            self.root.after(0, lambda: messagebox.showwarning("Warning", self.t("err_username")))
            return

        self._set_ui_state(True)
        self.lbl_status.config(text=self.t("fetching"))
        self.listbox.delete(0, tk.END)

        following = self._fetch_all_pages(f"https://api.github.com/users/{username}/following")
        followers = self._fetch_all_pages(f"https://api.github.com/users/{username}/followers")

        if following is not None and followers is not None:
            non_followers = sorted(list(following - followers))
            self.current_data = non_followers
            self.active_mode = "unfollow"

            self.root.after(0, lambda: self._update_list_ui(
                non_followers, 
                self.t("action_unfollow", count=len(non_followers)),
                lambda: self.start_thread(self.execute_mass_action, non_followers, "unfollow")
            ))

        self.lbl_status.config(text="")
        self._set_ui_state(False)

    def fetch_fans(self):
        username = self.entry_username.get().strip()
        if not username:
            self.root.after(0, lambda: messagebox.showwarning("Warning", self.t("err_username")))
            return

        self._set_ui_state(True)
        self.lbl_status.config(text=self.t("fetching"))
        self.listbox.delete(0, tk.END)

        following = self._fetch_all_pages(f"https://api.github.com/users/{username}/following")
        followers = self._fetch_all_pages(f"https://api.github.com/users/{username}/followers")

        if following is not None and followers is not None:
            pending_followers = sorted(list(followers - following))
            self.current_data = pending_followers
            self.active_mode = "follow"

            self.root.after(0, lambda: self._update_list_ui(
                pending_followers, 
                self.t("action_follow", count=len(pending_followers)),
                lambda: self.start_thread(self.execute_mass_action, pending_followers, "follow")
            ))

        self.lbl_status.config(text="")
        self._set_ui_state(False)

    def _update_list_ui(self, items, btn_text, command_func):
        for item in items:
            self.listbox.insert(tk.END, item)

        green_color = THEMES[self.current_theme]["action_bg"]
        disabled_color = THEMES[self.current_theme]["action_disabled_bg"]

        self.btn_action.config(
            text=btn_text if items else self.t("action_default"),
            bg=green_color if items else disabled_color,
            fg="white" if items else "#888888",
            state="normal" if items else "disabled",
            command=command_func
        )

    def execute_mass_action(self, target_list, mode):
        token = self.entry_token.get().strip()
        if not token:
            self.root.after(0, lambda: messagebox.showwarning("Warning", self.t("err_token")))
            return

        action_word = self.t("action_unfollow_text") if mode == "unfollow" else self.t("action_follow_text")
        
        confirm = messagebox.askyesno(
            "Confirm", 
            self.t("confirm_action", action=action_word, count=len(target_list))
        )
        if not confirm:
            return

        self._set_ui_state(True)
        self.lbl_status.config(text=self.t("processing"))

        headers = self._get_headers()
        success_count = 0

        for target_user in target_list:
            url = f"https://api.github.com/user/following/{target_user}"
            try:
                if mode == "unfollow":
                    res = requests.delete(url, headers=headers, timeout=10)
                else:
                    res = requests.put(url, headers=headers, timeout=10)

                if res.status_code in (204, 201):
                    success_count += 1
            except Exception:
                pass

        self.root.after(0, lambda: self._on_action_complete(success_count, len(target_list)))

    def _on_action_complete(self, success_count, total):
        messagebox.showinfo(
            self.t("success_title"),
            self.t("success_msg", success=success_count, total=total)
        )
        self.listbox.delete(0, tk.END)
        self.current_data = []
        self.active_mode = None
        
        disabled_color = THEMES[self.current_theme]["action_disabled_bg"]
        self.btn_action.config(state="disabled", text=self.t("btn_finished"), bg=disabled_color, fg="#888888")
        self.lbl_status.config(text="")
        self._set_ui_state(False)

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubFollowManager(root)
    root.mainloop()
