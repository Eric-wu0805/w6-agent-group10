import sys
from ddgs import DDGS

def search_places(query):
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=3)
            if results:
                places = [res.get('title', '').split('|')[0].strip() or res.get('body', '')[:20] for res in results]
                print("、".join(places))
            else:
                print("查無相關景點")
    except Exception as e:
        print(f"Search error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        search_places(sys.argv[1])
    else:
        print("Usage: python search_places.py <query>")
