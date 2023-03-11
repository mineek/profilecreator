import os
import json
import plistlib
import uuid

manifests = {}
for filename in os.listdir("manifests"):
    for file in os.listdir("manifests/" + filename):
        if file.endswith(".json"):
            with open("manifests/" + filename + "/" + file, "r") as f:
                try:
                    manifests[file.split(".json")[0]] = json.load(f)
                except:
                    print("Error loading manifest " + file + " ignoring...")

profile = {}

def random_uuid():
    return str(uuid.uuid4())

def empty_profile(name):
    profile = {
        "PayloadContent": [],
        "PayloadDescription": "Created with @mineekdev's profile creator",
        "PayloadDisplayName": name,
        "PayloadIdentifier": "com.mineek.profilecreator." + random_uuid(),
        "PayloadType": "Configuration",
        "PayloadUUID": random_uuid(),
        "PayloadVersion": 1
    }
    return profile

def create_payload(manifest):
    identifier = manifest["title"].split(" (")[1].split(")")[0]
    payload = {
        "PayloadDisplayName": manifest["title"],
        "PayloadIdentifier": identifier + "." + random_uuid(),
        "PayloadType": identifier,
        "PayloadUUID": random_uuid(),
        "PayloadVersion": 1
    }
    for key in manifest["properties"]:
        payload[key] = input(manifest["properties"][key]["title"] + " ( press enter to skip ): ")
        if payload[key] == "":
            del payload[key]
    return payload

def save_profile(profile):
    if not os.path.exists("profiles"):
        os.makedirs("profiles")
    with open("profiles/" + profile["PayloadDisplayName"] + ".mobileconfig", "wb") as f:
        plistlib.dump(profile, f)

def main():
    print("Welcome, %s" % os.getlogin())
    name = input("Enter a name for your profile ( this will be shown on your device ): ")

    if not os.path.exists("saves"):
        os.makedirs("saves")

    try:
        with open("saves/" + name + ".json", "r") as f:
            continue_ = input("Profile already exists, continue working on it? (y/n): ")
            if continue_ == "y":
                profile = json.load(f)
            else:
                profile = empty_profile(name)
    except:
        profile = empty_profile(name)

    chosenManifests = []
    for i, manifest in enumerate(manifests):
        print(str(i) + ": " + manifest + " - " + manifests[manifest]["title"])
    while True:
        chosen = input("Choose a manifest to add ( press enter to stop ): ")
        if chosen == "":
            break
        else:
            print("Added " + list(manifests.keys())[int(chosen)])
            chosenManifests.append(list(manifests.keys())[int(chosen)])

    for manifest in chosenManifests:
        if manifest in manifests:
            print("You'll now be configuring " + manifests[manifest]["title"])
            profile["PayloadContent"].append(create_payload(manifests[manifest]))
        else:
            print("Manifest " + manifest + " not found")

    save_profile(profile)
    with open("saves/" + name + ".json", "w") as f:
        json.dump(profile, f)
    print("Saved profile to profiles/" + name + ".mobileconfig")

if __name__ == "__main__":
    main()