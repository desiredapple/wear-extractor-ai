import os

def generate_stats_file(file_path: str) -> None:
    stats = [f"{r} - {len(files)}\n"
    for r, _, files in os.walk(f"./data/wildberries")]
    review_number = sum([int(st.split()[-1])
    if st.find("review_gallery") != -1
    else 0
    for st in stats])
    showcase_number = sum([
    int(st.split()[-1]) if st.find("showcase") != -1 else 0
    for st in stats])
    stats.append(f"review all - {review_number}\n")
    stats.append(f"showcase all - {showcase_number}\n")
    with open(file_path, "w") as file:
        file.writelines(stats)
