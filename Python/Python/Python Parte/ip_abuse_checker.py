import os
import requests
import ipaddress
import json


class AbuseIPDBChecker:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.abuseipdb.com/api/v2/check"

    def is_valid_ip(self, ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    def check_ip(self, ip, days=30):
        if not self.is_valid_ip(ip):
            return {"error": "Invalid IP address"}

        headers = {
            'Accept': 'application/json',
            'Key': self.api_key
        }
        params = {
            'ipAddress': ip,
            'maxAgeInDays': str(days)
        }

        try:
            response = requests.get(self.base_url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}

def main():
    # Enter your api key inside the quotes
    api_key = ''  
    checker = AbuseIPDBChecker(api_key)

    while True:
        ip = input("Enter an IP address to check (or 'quit' to exit): ")
        if ip.lower() == 'quit':
            break

        result = checker.check_ip(ip)
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
