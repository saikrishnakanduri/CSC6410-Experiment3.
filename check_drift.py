
import json

# Load the expected and actual network settings.
with open("intended.json", encoding="utf-8") as file:
    intended = json.load(file)["student-host:host"]

with open("observed.json", encoding="utf-8") as file:
    observed = json.load(file)["student-host:host"]

differences = []

# Compare host settings included in intended.json.
for field, expected in intended.items():
    if field == "interface":
        continue

    actual = observed.get(field)
    if expected != actual:
        differences.append((field, expected, actual))

# Match network interfaces by their names.
actual_interfaces = {
    item["name"]: item
    for item in observed.get("interface", [])
}

for interface in intended.get("interface", []):
    name = interface["name"]
    actual_interface = actual_interfaces.get(name)

    if actual_interface is None:
        differences.append((f"interface {name}", "present", "missing"))
        continue

    for field, expected in interface.items():
        if field == "name":
            continue

        actual = actual_interface.get(field)

        if expected != actual:
            differences.append(
                (f"interface {name} / {field}", expected, actual)
            )

# Print one line for each configuration difference.
if differences:
    print("CONFIGURATION DRIFT FOUND")
    for field, expected, actual in differences:
        print(f"{field}: intended={expected}, observed={actual}")
else:
    print("NO CONFIGURATION DRIFT FOUND")
