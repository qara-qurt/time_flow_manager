from monitoring.application import track_app_history
from monitoring.browser import save_browser_history


if __name__ == '__main__':
    track_app_history()
    save_browser_history()

