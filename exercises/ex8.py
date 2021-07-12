import requests
import json
import time

def create_new_job() -> int:
    URL = "https://playground.learnqa.ru/ajax/api/longtime_job"

    first_response = requests.get(URL)
    data = json.loads(first_response.text)
    seconds = data.get("seconds")
    token = data.get("token")

    second_response = requests.get(URL, params = {"token": token})

    data_2 = json.loads(second_response.text)
    status = data_2.get("status")
    expected_status = "Job is NOT ready"
    assert expected_status, status
    time.sleep(seconds)

    third_response = requests.get(URL, params = {"token": token})

    data_3 = json.loads(third_response.text)
    status_after = data_3.get("status")
    expected_status_after = "Job is ready"
    assert expected_status_after, status_after
    result = data_3.get("result")
    print(result)
    return result



if __name__ == "__main__":
    create_new_job()