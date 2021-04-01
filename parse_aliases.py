import json


def get(category: str, inp: str):
    separate = inp.strip().split(" ")

    with open("files/aliases.json", "r") as fp:
        aliases = json.load(fp)

    # List of all words where aliases are replaced
    parsed = []

    for alias in separate:
        if not alias.startswith("$"):
            continue

        alias = alias[1:]

        if alias.lower() in aliases[category]:
            # Albums should be parsed separately
            if category == "albums":
                return aliases[category][alias.lower()]

            # Anything to append afterwards (usually separators)
            post_fix = ""

            if alias.endswith(","):
                post_fix = ","

            parsed.append(aliases[category][alias.lower()] + post_fix)
        else:
            parsed.append(f"${alias}")

    return " ".join(parsed)
