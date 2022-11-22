import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import os

driver = None


# @pytest.fixture(scope='module', params=["smtp.gmail.com, 'mail.python.org"])
# def call_data()
@pytest.fixture(scope="session")
def b(browser):
    global driver
    if driver is not None:
        return driver
    if browser == 'chrome':
        options = webdriver.ChromeOptions()
        options.headless = False
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )

    else:
        options = webdriver.FirefoxOptions()
        options.headless = False
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

    return driver


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        default="chrome",
        help="define browser: chrome or firefox, --browser=firefox"
    )


@pytest.fixture(scope='session')
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope='session', autouse=True)
def print_browser(b):
    print('\n---------Test started----------\n')
    b.get('https://www.saucedemo.com/')
    print(type(b))
    yield (b)
    b.quit()
    print('\n---------Test ended-----------\n')


def pytest_html_report_title(report):
    report.title = "Hello, new name"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call":
        extra.append(pytest_html.extras.url(driver.current_url))
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            test_name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
            driver.get_screenshot_as_file('screens/screenshot-%s.png' % test_name)
            extra.append(pytest_html.extras.image('screens/screenshot-%s.png' % test_name))
        report.extra = extra
