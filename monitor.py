import argparse
import logging
import time

import requests


logging.basicConfig(
    filename="monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def check_website(url):
    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        response_time = time.time() - start_time

        if response.status_code == 200:
            status = "Online"
        elif 400 <= response.status_code < 500:
            status = f"Client error ({response.status_code})"
        elif 500 <= response.status_code < 600:
            status = f"Server error ({response.status_code})"
        else:
            status = f"HTTP {response.status_code}"

        logging.info(
            "%s - %s - %.2fs",
            url,
            status,
            response_time
        )

        return {
            "url": url,
            "status": status,
            "status_code": response.status_code,
            "response_time": response_time
        }

    except requests.exceptions.Timeout:
        logging.warning("%s - Timeout", url)

        return {
            "url": url,
            "status": "Timeout"
        }

    except requests.exceptions.ConnectionError:
        logging.warning("%s - Connection failed", url)

        return {
            "url": url,
            "status": "Connection failed"
        }

    except requests.exceptions.RequestException as error:
        logging.error("%s - Request failed: %s", url, error)

        return {
            "url": url,
            "status": f"Request failed: {error}"
        }


def display_result(result):
    print("\n" + "-" * 45)
    print(f"Website       : {result['url']}")
    print(f"Status        : {result['status']}")

    if "status_code" in result:
        print(f"HTTP Status   : {result['status_code']}")
        print(f"Response Time : {result['response_time']:.2f}s")

    print("-" * 45)


def main():
    parser = argparse.ArgumentParser(
        description="Check whether websites are available"
    )

    parser.add_argument(
        "urls",
        nargs="+",
        help="Website URLs to monitor"
    )

    args = parser.parse_args()

    for url in args.urls:
        result = check_website(url)
        display_result(result)


if __name__ == "__main__":
    main()