import subprocess
import xml.etree.ElementTree as ET
from collections import defaultdict
from colorama import init, Fore, Style

# Define log categories and commands
log_categories = {
    'System': ['log', 'show', '--predicate', 'eventMessage contains "System"', '--info'],
    'Application': ['log', 'show', '--predicate', 'eventMessage contains "App"', '--info'],
    'Security': ['log', 'show', '--predicate', 'eventMessage contains "Security"', '--info']
}

# Dictionary to store event counts by Event ID
event_counts = defaultdict(int)

# Dictionary to store the latest event in each category
latest_event = {
    'System': None,
    'Application': None,
    'Security': None
}

# Dictionary to store the total event count in each category
category_event_count = {
    'System': 0,
    'Application': 0,
    'Security': 0
}

# Initialize colorama
init(autoreset=True)

# Loop through each log category
for category, command in log_categories.items():
    print(Fore.GREEN + Style.BRIGHT + f"{category} log:")

    try:
        # Execute the log command
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode != 0:
            print(Fore.RED + f"Error reading {category} logs: {result.stderr}")
            continue

        # Parse the log output
        for line in result.stdout.splitlines():
            if not line.strip():
                continue

            # Extract Event ID and timestamp (if available)
            event_id = "Unknown"
            timestamp = "Unknown"

            if "eventID" in line:
                event_id = line.split("eventID:")[1].split()[0]
            if "timestamp" in line:
                timestamp = line.split("timestamp:")[1].split()[0]

            # Update the latest event in the category
            if not latest_event[category] or timestamp > latest_event[category]['timestamp']:
                latest_event[category] = {
                    'event_id': event_id,
                    'timestamp': timestamp,
                    'details': line
                }

            # Count events by Event ID
            event_counts[event_id] += 1

            # Increment the total count for the current category
            category_event_count[category] += 1

        # Print the last event for each category
        print(f"Last event in {category} category: Event ID = {latest_event[category]['event_id']}, Date and Time = {latest_event[category]['timestamp']}")

        # Print the total number of events in the current category
        print(f"Total number of events in {category} category: {category_event_count[category]}")

    except Exception as e:
        print(Fore.RED + f"An error occurred while processing {category} logs: {e}")

# Summary by Event ID
print(Fore.GREEN + Style.BRIGHT + "\nEvent summary by Event ID:")
for event_id, count in event_counts.items():
    if count > 10:  # If the number of events with this Event ID exceeds 10
        print(f"Event ID {event_id} occurred {count} times")
