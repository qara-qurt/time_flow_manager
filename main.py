from monitoring.application import track_app_history
from monitoring.browser import save_browser_history


if __name__ == '__main__':
    save_browser_history()
    track_app_history()

