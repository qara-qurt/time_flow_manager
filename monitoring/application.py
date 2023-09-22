import os
import psutil
import datetime
import json
import time


# Time of delay data collection
DELAY = 3600


# Save history of applications to JSON
def save_app_history(app_history):
    now = datetime.datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    folder_path = './data/application'
    output_file = os.path.join(folder_path, f"{date_str}.json")

    # Check dir is existed
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Read current list
    current_history = []

    if os.path.exists(output_file):
        with open(output_file, 'r') as json_file:
            current_history = json.load(json_file)

    # Combine current history with new data
    current_history.extend(app_history)

    # Remove duplicates based on 'name' and 'time' fields
    unique_history = []
    seen = set()
    for app in current_history:
        key = (app['name'], app['time'])
        if key not in seen:
            unique_history.append(app)
            seen.add(key)

    # Write the unique history to the JSON file
    with open(output_file, 'w') as json_file:
        json.dump(unique_history, json_file, default=str, indent=4)

    print(f"История запуска приложений добавлена в файл {output_file}")


# tracking application launch
def track_app_history():
    app_history = []
    while True:
        try:
            # Get current process
            all_processes = psutil.process_iter()

            # Filter by name and time for write to dict and save it
            for process in all_processes:
                try:
                    app_name = process.name()
                    create_time_timestamp = process.create_time()
                    exe = process.exe()
                    path = process.cwd()
                    create_time = datetime.datetime.fromtimestamp(create_time_timestamp)
                    app_history.append({
                        'name': app_name,
                        'time': create_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'exe': exe,
                        'path': path,
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass

            # Save history file only if there are new entries
            if app_history:
                save_app_history(app_history)
                app_history = []  # Clear the list after saving

            # Delay
            time.sleep(DELAY)

        except KeyboardInterrupt:
            save_app_history(app_history)
            break
