import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from settings import valid_password, valid_email, valid_login, valid_account, valid_phone, invalid_phone, invalid_email, invalid_password, invalid_login, invalid_account


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome()
    pytest.driver.get('https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth?client_id=account_b2c&redirect_uri=https://b2c.passport.rt.ru/account_b2c/login&response_type=code&scope=openid&state=9328d728-dc48-451d-82b6-676f9b041ee6&theme&auth_type')


    yield

    pytest.driver.quit()

# №1 Успешная авторизация по электронной почте
def test_valid_auth_email():
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 't-btn-tab-mail').click()
    pytest.driver.find_element(By.ID, 'username').send_keys(valid_email)
    pytest.driver.find_element(By.ID, 'password').send_keys(valid_password)
    pytest.driver.find_element(By.ID, 'kc-login').click()

    """ Проверяется, что после успешной авторизации электронная почта в учётных данных соотвествует электронной почте, 
       под которой прошла авторизация"""
    email = WebDriverWait(pytest.driver, 5).until(ec.presence_of_element_located(
        (By.CSS_SELECTOR, 'div:nth-child(2) > div > span.dots-table-item__right > span')))
    email.title = email.get_attribute('title')
    assert email.title == valid_email

# №2 Успешная авторизация по номеру телефона
def test_valid_auth_phone():
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys(valid_phone)
    pytest.driver.find_element(By.ID, 'password').send_keys(valid_password)
    pytest.driver.find_element(By.ID, 'kc-login').click()

    """ Проверяется, что после успешной авторизации номер телефона в учётных данных соотвествует номеру телефона, 
        под которым прошла авторизация"""
    phone = WebDriverWait(pytest.driver, 5).until(ec.presence_of_element_located(
        (By.CSS_SELECTOR, 'div:nth-child(1) > div > span.dots-table-item__right > span')))
    phone.title = phone.get_attribute('title')
    assert phone.title == valid_phone

# №3 Успешная авторизация по логину
def test_valid_auth_login():
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 't-btn-tab-login').click()
    pytest.driver.find_element(By.ID, 'username').send_keys(valid_login)
    pytest.driver.find_element(By.ID, 'password').send_keys(valid_password)
    pytest.driver.find_element(By.ID, 'kc-login').click()

    """ Проверяется, что после успешной авторизации открыта страница с учётными данными"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, 'user-avatar')))

# №4 Успешная авторизация по лицевому счёту
def test_valid_auth_account():
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 't-btn-tab-ls').click()
    pytest.driver.find_element(By.ID, 'username').send_keys(valid_account)
    pytest.driver.find_element(By.ID, 'password').send_keys(valid_password)
    pytest.driver.find_element(By.ID, 'kc-login').click()

    """ Проверяется, что после успешной авторизации открыта страница с учётными данными"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, 'user-avatar')))

# №5 Вход в ЛК зарегистрированного пользователя по кнопке Enter
def test_log_in_by_enter():
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'username')))
    login = pytest.driver.find_element(By.ID, 'username')
    login.clear()
    login.send_keys(valid_email)
    password = pytest.driver.find_element(By.ID, 'password')
    password.clear()
    password.send_keys(valid_password)
    password.send_keys(Keys.RETURN)

    """ Проверяемтся, что после успешной авторизации открыта страница с учётными данными"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, 'user-avatar')))


# №6 Неуспешная авторизация с невалидной электронной почтой и валидным паролем
def test_invalid_email():
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 't-btn-tab-mail').click()
    pytest.driver.find_element(By.ID, 'username').send_keys(invalid_email)
    pytest.driver.find_element(By.ID, 'password').send_keys(valid_password)
    pytest.driver.find_element(By.ID, 'kc-login').click()

    """ Проверяется, что после неуспешной авторизации открыта страница авторизации 
    и есть возможность повторного логина"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'kc-login')))

    """ Проверяется, что после неуспешной авторизации появляется сообщение об ошибке"""
    form_error = WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'form-error-message')))
    form_error.data = form_error.get_attribute('data-error')
    assert form_error.data == 'Неверный логин или пароль'

    """ Проверяется, что элемент 'Забыли пароль' окрашен в оранжевый цвет"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located(
        (By.CLASS_NAME, 'rt-link.rt-link--orange.login-form__forgot-pwd.login-form__forgot-pwd--animated')))

# №7 Проверка попытки авторизации с невалидным номером телефона и валидным паролем
def test_invalid_phone():
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 't-btn-tab-phone').click()
    pytest.driver.find_element(By.ID, 'username').send_keys(invalid_phone)
    pytest.driver.find_element(By.ID, 'password').send_keys(valid_password)
    pytest.driver.find_element(By.ID, 'kc-login').click()

    """ Проверяется, что после неуспешной авторизации открыта страница авторизации 
    и есть возможность повторного логина"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'kc-login')))

    """ Проверяется, что после неуспешной авторизации появляется сообщение об ошибке"""
    form_error = WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'form-error-message')))
    form_error.data = form_error.get_attribute('data-error')
    assert form_error.data == 'Неверный логин или пароль'

    """ Проверяется, что элемент 'Забыли пароль' окрашен в оранжевый цвет"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located(
        (By.CLASS_NAME, 'rt-link.rt-link--orange.login-form__forgot-pwd.login-form__forgot-pwd--animated')))

# №8 Неуспешная авторизация с валидной электронной почтой и невалидным паролем
def test_invalid_password_valid_email():
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys(valid_email)
    pytest.driver.find_element(By.ID, 'password').send_keys(invalid_password)
    pytest.driver.find_element(By.ID, 'kc-login').click()

    """ Проверяется, что после неуспешной авторизации открыта страница авторизации 
    и есть возможность повторного логина"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'kc-login')))

    """ Проверяется, что после неуспешной авторизации появляется сообщение об ошибке"""
    form_error = WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'form-error-message')))
    form_error.data = form_error.get_attribute('data-error')
    assert form_error.data == 'Неверный логин или пароль'

    """ Проверяется, что элемент 'Забыли пароль' окрашен в оранжевый цвет"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located(
        (By.CLASS_NAME, 'rt-link.rt-link--orange.login-form__forgot-pwd.login-form__forgot-pwd--animated')))

# №9 Неуспешная авторизация с валидным номером телефона и невалидным паролем
def test_invalid_password_valid_phone():
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys(valid_phone)
    pytest.driver.find_element(By.ID, 'password').send_keys(invalid_password)
    pytest.driver.find_element(By.ID, 'kc-login').click()

    """ Проверяется, что после неуспешной авторизации открыта страница авторизации 
    и есть возможность повторного логина"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'kc-login')))

    """ Проверяется, что после неуспешной авторизации появляется сообщение об ошибке"""
    form_error = WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'form-error-message')))
    form_error.data = form_error.get_attribute('data-error')
    assert form_error.data == 'Неверный логин или пароль'

    """ Проверяется, что элемент 'Забыли пароль' окрашен в оранжевый цвет"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located(
        (By.CLASS_NAME, 'rt-link.rt-link--orange.login-form__forgot-pwd.login-form__forgot-pwd--animated')))

# №10 Неуспешная авторизация с невалидным логином и валидным паролем
def test_invalid_login():
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys(invalid_login)
    pytest.driver.find_element(By.ID, 'password').send_keys(valid_password)
    pytest.driver.find_element(By.ID, 'kc-login').click()

    """ Проверяется, что после неуспешной авторизации открыта страница авторизации 
    и есть возможность повторного логина"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'kc-login')))

    """ Проверяется, что после неуспешной авторизации появляется сообщение об ошибке"""
    form_error = WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'form-error-message')))
    form_error.data = form_error.get_attribute('data-error')
    assert form_error.data == 'Неверный логин или пароль'

    """ Проверяется, что элемент 'Забыли пароль' окрашен в оранжевый цвет"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located(
        (By.CLASS_NAME, 'rt-link.rt-link--orange.login-form__forgot-pwd.login-form__forgot-pwd--animated')))

# №11 Неуспешная авторизация с невалидным номером лицевого счёта и валидным паролем
def test_invalid_account():
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys(invalid_account)
    pytest.driver.find_element(By.ID, 'password').send_keys(valid_password)
    pytest.driver.find_element(By.ID, 'kc-login').click()

    """ Проверяется, что после неуспешной авторизации открыта страница авторизации 
    и есть возможность повторного логина"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'kc-login')))

    """ Проверяется, что после неуспешной авторизации появляется сообщение об ошибке"""
    form_error = WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'form-error-message')))
    form_error.data = form_error.get_attribute('data-error')
    assert form_error.data == 'Неверный логин или пароль'

    """ Проверяется, что элемент 'Забыли пароль' окрашен в оранжевый цвет"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located(
        (By.CLASS_NAME, 'rt-link.rt-link--orange.login-form__forgot-pwd.login-form__forgot-pwd--animated')))

# №12 Неуспешная авторизация с валидным логином и невалидным паролем
def test_valid_login_invalid_password():
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys(valid_login)
    pytest.driver.find_element(By.ID, 'password').send_keys(invalid_password)
    pytest.driver.find_element(By.ID, 'kc-login').click()

    """ Проверяется, что после неуспешной авторизации открыта страница авторизации 
    и есть возможность повторного логина"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'kc-login')))

    """ Проверяется, что после неуспешной авторизации появляется сообщение об ошибке"""
    form_error = WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'form-error-message')))
    form_error.data = form_error.get_attribute('data-error')
    assert form_error.data == 'Неверный логин или пароль'

    """ Проверяется, что элемент 'Забыли пароль' окрашен в оранжевый цвет"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located(
        (By.CLASS_NAME, 'rt-link.rt-link--orange.login-form__forgot-pwd.login-form__forgot-pwd--animated')))

# №13 Неуспешная авторизация с валидным номером лицевого счёта и невалидным паролем
def test_valid_account_invalid_password():
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys(valid_account)
    pytest.driver.find_element(By.ID, 'password').send_keys(invalid_password)
    pytest.driver.find_element(By.ID, 'kc-login').click()

    """ Проверяется, что после неуспешной авторизации открыта страница авторизации 
    и есть возможность повторного логина"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'kc-login')))

    """ Проверяется, что после неуспешной авторизации появляется сообщение об ошибке"""
    form_error = WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'form-error-message')))
    form_error.data = form_error.get_attribute('data-error')
    assert form_error.data == 'Неверный логин или пароль'

    """ Проверяется, что элемент 'Забыли пароль' окрашен в оранжевый цвет"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located(
        (By.CLASS_NAME, 'rt-link.rt-link--orange.login-form__forgot-pwd.login-form__forgot-pwd--animated')))

# №14 Неуспешная авторизация с с незаполненным полем ввода почты
def test_empty_email():
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 't-btn-tab-mail').click()
    pytest.driver.find_element(By.ID, 'kc-login').click()

    """ Проверяется, что после неуспешной авторизации открыта страница авторизации 
    и есть возможность повторного логина"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'kc-login')))

    """ Проверяется, что после неуспешной авторизации появляется сообщение об ошибке под полем ввода логина"""
    form_error_email = WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.CLASS_NAME, 'rt-input-container__meta.rt-input-container__meta--error')))
    assert form_error_email.text == 'Введите адрес, указанный при регистрации'

# №15 Неуспешная авторизация с незаполненным полем ввода номера телефона
def test_empty_phone():
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'kc-login').click()

    """ Проверяется, что после неуспешной авторизации открыта страница авторизации 
    и есть возможность повторного логина"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'kc-login')))

    """ Проверяется, что после неуспешной авторизации появляется сообщение об ошибке под полем ввода логина"""
    form_error_phone = WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.CLASS_NAME, 'rt-input-container__meta.rt-input-container__meta--error')))
    assert form_error_phone.text == 'Введите номер телефона'

# №16 Неуспешная попытка авторизации с незаполненным полем ввода логина
def test_empty_login():
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 't-btn-tab-login').click()
    pytest.driver.find_element(By.ID, 'kc-login').click()
    """ Проверяется, что после неуспешной авторизации открыта страница авторизации 
    и есть возможность повторного логина"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'kc-login')))

    """ Проверяется, что после неуспешной авторизации появляется сообщение об ошибке под полем ввода логина"""
    form_error_login = WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.CLASS_NAME, 'rt-input-container__meta.rt-input-container__meta--error')))
    assert form_error_login.text == 'Введите логин, указанный при регистрации'

# №17 Неуспешная попытка авторизации с незаполненным полем ввода логина
def test_empty_account():
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 't-btn-tab-ls').click()
    pytest.driver.find_element(By.ID, 'kc-login').click()

    """ Проверяется, что после неуспешной авторизации открыта страница авторизации 
    и есть возможность повторного логина"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'kc-login')))

    """ Проверяется, что после неуспешной авторизации появляется сообщение об ошибке под полем ввода логина"""
    form_error_login = WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.CLASS_NAME, 'rt-input-container__meta.rt-input-container__meta--error')))
    assert form_error_login.text == 'Введите номер вашего лицевого счета'


# №18 Неуспешная попытка авторизации с незаполненным полем ввода пароля
def test_empty_password():
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 't-btn-tab-mail').click()
    pytest.driver.find_element(By.ID, 'username').send_keys(valid_email)
    pytest.driver.find_element(By.ID, 'kc-login').click()

    """ Проверяется, что после неуспешной авторизации открыта страница авторизации 
    и есть возможность повторного логина"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'kc-login')))

# №19 Переход на страницу регистрации со страницы авторизации
def test_registration_btn():
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'kc-register')))
    pytest.driver.find_element(By.ID, 'kc-register').click()

    """ Проверяется наличие заголовка формы регистрации"""
    title_registration_page = WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.CLASS_NAME, 'card-container__title')))
    assert title_registration_page.text == 'Регистрация'

    """ Проверяется наличие элементов формы регистрации"""
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.NAME, 'firstName')))
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.NAME, 'lastName')))
    WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[2]/div/div/input')))
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'address')))
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'password')))
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'password-confirm')))
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.NAME, 'register')))

# №20 Переход на страницу восстановления пароля
def test_forgot_password_btn():
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'forgot_password')))
    pytest.driver.find_element(By.ID, 'forgot_password').click()

    """ Проверяется наличие заголовка формы восстановления пароля"""
    title_forgot_password_page = WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.CLASS_NAME, 'card-container__title')))
    assert title_forgot_password_page.text == 'Восстановление пароля'

# №21 Переход по кнопке "Вернуться назад" на страницу авторизации со страницы восстановления пароля
def test_reset_back_btn():
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 'forgot_password')))
    pytest.driver.find_element(By.ID, 'forgot_password').click()
    pytest.driver.find_element(By.ID, 'reset-back').click()
    """ Проверяется наличие заголовка формы авторизации"""
    title_auth_page = WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.CLASS_NAME, 'card-container__title')))
    assert title_auth_page.text == 'Авторизация'

# №22 Проверка переключения таба при вводе почты
def test_email_btn():
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 't-btn-tab-mail')))
    pytest.driver.find_element(By.ID, 'username').send_keys(valid_email)
    pytest.driver.find_element(By.ID, 'password').click()

    """ Проверяется, что название активного таба = Почта"""
    email_btn = WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.CLASS_NAME, 'rt-tab.rt-tab--small.rt-tab--active')))
    assert email_btn.text == 'Почта'

# №23 Проверка переключения таба при вводе номера телефона
def test_phone_btn():
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, 't-btn-tab-mail')))
    pytest.driver.find_element(By.ID, 't-btn-tab-mail').click()
    pytest.driver.find_element(By.ID, 'username').send_keys(valid_phone)
    pytest.driver.find_element(By.ID, 'password').click()

    """ Проверяется, что название активного таба = Телефон"""
    email_btn = WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.CLASS_NAME, 'rt-tab.rt-tab--small.rt-tab--active')))
    assert email_btn.text == 'Телефон'