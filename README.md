# GitHub Follower Manager

A lightweight, multi-language desktop application built with Python and Tkinter to manage your GitHub followings and followers.

## Features

* **Non-Followers (Unfollow):** Identify users you follow who don't follow you back.
* **Pending Followers (Follow Back):** Identify users following you whom you haven't followed back.
* **Batch Operations:** Mass-follow or unfollow users directly with one click.
* **Multi-Language Support:** English (default), Türkçe, 中文, Deutsch.
* **Themes:** Toggle between Dark and Light mode interfaces.

## Prerequisites

* Python 3.8+
* `requests` library

Install dependencies:
```bash
pip install requests
```

## How to Use

1. Run the application:

   Bash
   ```
   python main.py
   ```

2. Enter your **GitHub Username**.
3. Enter your **Personal Access Token** (requires `user:follow` scope for batch follow/unfollow actions).
4. Click an option to list users and execute batch actions.
