import requests

def get_advice():
    try:
        response = requests.get("https://api.adviceslip.com/advice", timeout=10)
        response.raise_for_status()
        data = response.json()
        print(data['slip']['advice'])
    except Exception as e:
        print(f"Error fetching advice: {e}")

if __name__ == "__main__":
    get_advice()
