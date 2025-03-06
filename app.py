import requests
import time
import threading
import os
from rich.console import Console
from rich.panel import Panel

console = Console()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def display_banner(title):
    banner = "(PyeulShares)" * 10  # Repeat 10 times
    console.print(Panel(banner, title=f"[yellow]● {title}[/]", width=65, style="bold bright_white"))

def load_cookies():
    clear_screen()
    display_banner("PASTE MULTIPLE TOKENS")
    console.print("[yellow]Paste your access tokens (one per line, then press Enter when done):[/yellow]")
    tokens = input().strip().split()
    return [token for token in tokens if token.startswith("EAAAA")]

def share_post(token, share_url, share_count, interval=0.1):
    url = "https://graph.facebook.com/me/feed"
    headers = {"User-Agent": "Mozilla/5.0"}
    data = {
        "link": share_url,
        "privacy": '{"value":"SELF"}',
        "access_token": token
    }

    success_count = 0
    for i in range(share_count):
        try:
            response = requests.post(url, data=data, headers=headers)
            response_data = response.json()
            if "id" in response_data:
                success_count += 1
                console.print(f"[bold cyan]({success_count}/{share_count})[/bold cyan] [green]Shared successfully.")
            else:
                console.print(f"[red]Failed to share: {response_data}")
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error: {e}")
        time.sleep(interval)

    console.print(f"[bold cyan]Total Successful Shares: {success_count}[/bold cyan]\n")

def spam_share_multiple():
    clear_screen()
    display_banner("MULTI-COOKIE SPAM SHARE")
    tokens = load_cookies()
    if not tokens:
        return
    
    share_url = input("Enter post link: ").strip()
    share_count = int(input("Enter Share Count per account: ").strip())

    threads = []
    for token in tokens:
        thread = threading.Thread(target=share_post, args=(token, share_url, share_count))
        thread.daemon = True
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

    console.print("[green]Finished sharing posts from all accounts.")
    input("\nPress Enter to return to menu...")

def spam_share_single():
    clear_screen()
    display_banner("SINGLE TOKEN SHARE")
    token = input("Enter Facebook access token: ").strip()
    if not token.startswith("EAAAA"):
        console.print("[red]Invalid token format!")
        return

    share_url = input("Enter post link: ").strip()
    share_count = int(input("Enter Share Count: ").strip())

    share_post(token, share_url, share_count, interval=0.1)
    console.print("[green]Finished sharing post.")
    input("\nPress Enter to return to menu...")

def main_menu():
    while True:
        clear_screen()
        display_banner("FACEBOOK TOOL")
        console.print(Panel("""
[green]1. Multi-Cookie Spam Share
[green]2. Single Token Share
[green]3. Exit
        """, width=65, style="bold bright_white"))
        
        choice = input("Select an option: ").strip()
        if choice == "1":
            spam_share_multiple()
        elif choice == "2":
            spam_share_single()
        elif choice == "3":
            console.print("[red]Exiting... Goodbye!")
            break
        else:
            console.print("[red]Invalid choice! Try again.")
            time.sleep(2)

if __name__ == '__main__':
    main_menu()
