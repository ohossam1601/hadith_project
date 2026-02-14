
import os
import sys
import json
import re

def get_hadith_id(filename):
    return filename.replace('.txt', '')

def claim_next_hadith(hadith_dir="hadith", claimed_dir="claimed"):
    """
    Finds the first unclaimed hadith, claims it (creates dir), and returns its content.
    """
    try:
        if not os.path.exists(hadith_dir):
            return json.dumps({"error": f"Directory '{hadith_dir}' not found."})

        # Ensure claimed directory exists
        if not os.path.exists(claimed_dir):
            os.makedirs(claimed_dir)

        # Get all available hadith files, sorted numerically
        all_hadiths = sorted(
            [f for f in os.listdir(hadith_dir) if f.endswith('.txt')],
            key=lambda x: int(get_hadith_id(x)) if get_hadith_id(x).isdigit() else float('inf')
        )

        # Get all currently claimed IDs
        claimed_ids = set(os.listdir(claimed_dir))

        next_hadith_file = None
        for hadith_file in all_hadiths:
            hid = get_hadith_id(hadith_file)
            if hid not in claimed_ids:
                next_hadith_file = hadith_file
                break
        
        if not next_hadith_file:
            return json.dumps({"status": "done", "message": "No unclaimed hadiths found."})

        next_id = get_hadith_id(next_hadith_file)
        
        # CLAIM: Create the directory atomically (sort of, rely on filesystem)
        claim_path = os.path.join(claimed_dir, next_id)
        os.makedirs(claim_path, exist_ok=True) # Using exist_ok=True just in case of race, though in this single-user env it's fine.

        # READ CONTENT
        file_path = os.path.join(hadith_dir, next_hadith_file)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return json.dumps({
            "status": "success",
            "id": next_id,
            "filename": next_hadith_file,
            "content": content
        }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    print(claim_next_hadith())
