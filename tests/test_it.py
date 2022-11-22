from selenium.webdriver.common.by import By


"""TC_001.00.05| Login Page >
User is unable to login with empty username and password"""


def test_login_page_with_empty_fields(b):
    b.find_element(By.ID, "user-name").clear()
    b.find_element(By.ID, "password").clear()

    b.find_element(By.ID, "login-button").click()

    assert (
            b.find_element(
                By.XPATH, '//h3[text() = "Epic sadface: Username is requir"]'
            )
            and b.current_url == "https://www.saucedemo.com/"
    )


def test_login_page_with_empty_fields_2(b):
    user_name = b.find_element(By.ID, "user-name")
    password = b.find_element(By.ID, "password")
    assert user_name.get_attribute("value") == "2"
    assert password.get_attribute("value") == ""

    b.find_element(By.ID, "login-button").click()

    assert (
            b.find_element(
                By.XPATH, '//h3[text() = "Epic sadface: Username is required"]'
            )
            and b.current_url == "https://www.saucedemo.com/"
    )







