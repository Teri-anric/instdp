# Instdp 🇺🇦
## Простий для використання _не офіційний_ фраємворк для instagram
### Disclaimer або Відмова від відповідальності  
Розробник даного програмного забезпечення 
не несе відповідальності за будь-які проблеми, 
що можуть виникнути з використанням цього програмного продукту 
для ваших облікових записів та даних. 
Використовуйте це програмне забезпечення на власний ризик і обізнаність.
### Встановлення
Через команду pip  
```commandline
pip install git+https://github.com/Teri-anric/instdp.git
```

### Використання  
Необхідно створити клієнта з бібліотеки 
[instagrapi](https://github.com/subzeroid/instagrapi)
увійти та передати його деспечеру
```python
from instagrapi import Client
from instdp import DirectDispatcher

username, password = os.environ.get('USER').split(maxsplit=1)

cl = Client()
# змінюємо пристрій і агента для мінізування блокування
c.set_device({
    "app_version": "289.0.0.25.49",
    "android_version": 29,
    "android_release": "10",
    "dpi": "480dpi",
    "resolution": "1080x2031",
    "manufacturer": "HUAWEI",
    "device": "HWEML",
    "model": "EML-L29",
    "cpu": "kirin970",
    "version_code": "488780865",
})
c.set_user_agent("Instagram 289.0.0.25.49 Android (29/10; 480dpi; 1080x2031; HUAWEI; EML-L29; HWEML; kirin970; it_IT; 488780865)")
# set Ukraine 
c.set_locale("uk_UA")

c.login(username=username, password=password)

dp = DirectDispatcher(client=cl)
```

**!! Змінюйте юзер агента інакше шанси отримати бан максимальні !!**

Тепер заєреструємо обробник повідомлень
```python
from instagrapi.types import DirectMessage

@dp.message()
def echo(msg: DirectMessage, dispatcher: DirectDispatcher):
    dispatcher.answer_message(msg, msg.text)
```
Також є обробники помилок
```python
from instagrapi.types import DirectThread

@dp.exception_handler(Exception)
def show_error(e: Exception, thread: DirectThread):
    print('error from chat name: ', thread.thread_title)
    print('error:', e)
```
В обробнику можна отримати такі аргументи:
- cl або client - Робочий клієнт з instagrapi
- dp або dispatcher - Сам обєкт диспечеру
- th або thread - Чат повідомлення
- message - Повідомлення (тільки для exception_handler)
- handler - Обробник в якому сталося помилка (тільки для exception_handler)

Також можна добавити свої аргументи через диспечер:
```python
dp[key] = value
```

Лишилося запустити опитування  
```python
dp.polling_direct()
```
