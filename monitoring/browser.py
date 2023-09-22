import datetime
import json
import os

from browser_history import get_history


def save_browser_history():
    history = history_browser()

    now = datetime.datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    folder_path = './data/browser_history'
    output_file = os.path.join(folder_path, f"{date_str}.json")

    # Check dir is existed
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Write the unique history to the JSON file
    with open(output_file, 'w') as json_file:
        json.dump(history, json_file, default=str, indent=4)

    print(f"История запуска приложений добавлена в файл {output_file}")


def history_browser():
    history = get_history()
    res = []
    for h in history.histories:
        res.append({
            'url': h[1],
            'time': h[0]
        })

    return res
