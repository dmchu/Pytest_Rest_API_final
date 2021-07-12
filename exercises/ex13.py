import requests
import pytest


user_agent_params = [
    ('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'),
    ('Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1'),
    ('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'),
    ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0'),
    ('Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1')
]

expected_values = [
    ({'platform': 'Mobile', 'browser': 'No', 'device': 'Android'}),
    ({'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'}),
    ({'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}),
    ({'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}),
    ({'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'})
]

@pytest.mark.parametrize("user_agent_param", user_agent_params)
def test_user_agent_functionality(user_agent_param):
    expected_params = expected_values[user_agent_params.index(user_agent_param)]
    URL = "https://playground.learnqa.ru/ajax/api/user_agent_check"
    headers = {"User-Agent": user_agent_param}
    response = requests.get(URL,headers=headers)
    data = response.json()

    actual_platform = data.get("platform")
    actual_browser = data.get("browser")
    actual_device = data.get("device")

    expected_platform = expected_params.get("platform")
    expected_browser = expected_params.get("browser")
    expected_device = expected_params.get("device")

    assert actual_platform == expected_platform, f"Expected platform was '{expected_platform}'," \
                                                 f" but actual platform was '{actual_platform}'"
    assert actual_browser == expected_browser, f"Expected browser was '{expected_browser}'," \
                                                 f" but actual browser was '{actual_browser}'"
    assert actual_device == expected_device, f"Expected device was '{expected_device}'," \
                                                 f" but actual device was '{actual_device}'"

