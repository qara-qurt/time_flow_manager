import os
import psutil
import datetime
import json
import time

# Time of delay data collection
DELAY = 600


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
    process_counts = {}
    while True:
        try:
            # Get current process
            all_processes = psutil.process_iter()

            # Filter by name and time for write to dict and save it
            for process in all_processes:
                try:
                    # Get data from process
                    app_name = process.name()
                    create_time_timestamp = process.create_time()
                    exe = process.exe()
                    path = process.cwd()
                    create_time = datetime.datetime.fromtimestamp(create_time_timestamp)

                    # Filter
                    # Should check default browser and not add
                    if not is_system_process(process) and app_name != 'chrome':
                        app_history.append({
                            'name': app_name,
                            'time': create_time.strftime('%Y-%m-%d %H:%M:%S'),
                            'exe': exe,
                            'path': path,
                        })

                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass

            count_of_process()
            # Save history file only if there are new entries
            if app_history:
                save_app_history(app_history)
                app_history = []  # Clear the list after saving

            # Delay
            time.sleep(DELAY)

        except KeyboardInterrupt:
            save_app_history(app_history)
            break


# Find most used - test
def count_of_process():
    now = datetime.datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    folder_path = './data/application'
    output_file = os.path.join(folder_path, f"{date_str}.json")

    with open(output_file, 'r') as json_file:
        data = json.load(json_file)

    process_count = {}
    for p in data:
        process_name = p['name']
        process_time = p['time']
        process_exe = p['exe']
        process_path = p['path']

        if process_name not in process_count:
            process_count[process_name] = []

        process_count[process_name].append({
            'exe': process_exe,
            'path': process_path,
            'time': process_time
        })


# -------------- Filter algorithms ---------------

# Check process is system
def is_system_process(process):
    # Define a list of system-related directories
    system_dirs = ['/usr/lib', '/usr/libexec', '/sbin']

    # Get the path of the executable associated with the process
    try:
        process_exe = process.exe()
        for dir in system_dirs:
            if process_exe.startswith(dir):
                return True
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

    return False
