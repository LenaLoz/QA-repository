import aiohttp
import asyncio
from tabulate import tabulate

API_KEY = "2nPhryFZQP2GRSGdgaRojCLs3xwK5GOv"
BASE_URL = "http://dataservice.accuweather.com"

#Эта функция является асинхронной сопрограммой в Python, которая используется для выполнения асинхронного HTTP-запроса
# и получения ответа в формате JSON. Давайте разберем её по шагам:

# session: Параметр, который должен быть объектом ClientSession из библиотеки aiohttp. Этот объект используется для выполнения HTTP-запросов.
# url: Строка, представляющая URL-адрес, на который будет совершен запрос.
# params: Необязательный параметр, который может быть использован для передачи параметров запроса, например, строки запроса URL.
# async with session.get(url, params=params) as response:
# async with: Контекстный менеджер, адаптированный для асинхронного использования. Он позволяет асинхронно войти в контекст и гарантирует
# закрытие ресурсов (например, сетевых соединений) по завершении блока кода или при возникновении исключения.
#
# session.get(url, params=params): Асинхронный метод get объекта session, который отправляет HTTP GET запрос на указанный url
# с параметрами params. Возвращаемый объект является асинхронным контекстным менеджером, который можно использовать в async with блоке.
# response: Переменная, в которую будет сохранен ответ сервера после выполнения запроса.
# response.raise_for_status()
# Этот метод объекта ответа (response) проверяет, не вернул ли сервер ошибку (статусный код HTTP 4xx или 5xx).
# Если сервер вернул ошибку, метод raise_for_status выбросит исключение aiohttp.ClientResponseError.
# return await response.json()
#
# await: Ключевое слово, используемое для "ожидания" результата асинхронной операции.
# В данном случае, оно ожидает завершения метода json(), который асинхронно читает ответ сервера и преобразует его из
# JSON формата в Python объект (обычно словарь или список).
# response.json(): Асинхронный метод, который извлекает тело ответа в формате JSON. Поскольку чтение тела ответа и его преобразование в JSON
# также являются асинхронными операциями, перед методом используется await.
# В результате, когда другая асинхронная функция вызывает fetch_json, она должна использовать await для ожидания результата.

async def fetch_json(session, url, params=None):
    async with session.get(url, params=params) as response:
        response.raise_for_status()
        return await response.json()


async def get_weather(session, city):
    location_url = f"{BASE_URL}/locations/v1/cities/search"
    location_params = {"apikey": API_KEY, "q": city}

    try:
        location_data = await fetch_json(session, location_url, params=location_params)

        if location_data:
            location_key = location_data[0]["Key"]
            weather_url = f"{BASE_URL}/currentconditions/v1/{location_key}"
            weather_params = {"apikey": API_KEY, "details": True}

            weather_data = await fetch_json(session, weather_url, params=weather_params)

            if weather_data:
                weather_info = [
                    city,
                    weather_data[0]["Temperature"]["Metric"]["Value"],
                    weather_data[0]["RelativeHumidity"],
                    weather_data[0]["WeatherText"]
                ]
                return weather_info

        return [city, "No data", "No data", "No data"]

    except aiohttp.ClientError as e:
        print(f"Error occurred while fetching weather data for {city}: {e}")
        return [city, "Error", "Error", "Error"]


class WeatherBot:
    def __init__(self):
        self.cities = []

    def add_city(self, city):
        if city not in self.cities:
            self.cities.append(city)

    async def display_weather(self):
        async with aiohttp.ClientSession() as session:
            weather_data = await asyncio.gather(*(get_weather(session, city) for city in self.cities))
            print(tabulate(weather_data, headers=["City", "Temperature (C)", "Humidity (%)", "Description"],
                           tablefmt="grid"))

    async def run(self):
        await self.display_weather()


async def main():
    bot = WeatherBot()
    bot.add_city("Almeria")
    bot.add_city("Kharkov")
    bot.add_city("London")
    await bot.run()


if __name__ == '__main__':
    asyncio.run(main())

# Что такое Event Loop?
# Event loop — это конструкция, которая ожидает и отправляет события или сообщения в программе.
# Он работает путем повторения цикла, который ожидает наступления событий и затем запускает обратные вызовы (callback functions), связанные с этими событиями.
# В контексте асинхронного программирования, цикл событий позволяет программам выполнять операции ввода-вывода (I/O) без блокирования основного потока исполнения.
# Как работает Event Loop?
# Инициализация цикла: Перед началом работы цикл событий должен быть инициализирован. В Python это делается путем вызова loop = asyncio.get_event_loop().
# Запуск цикла: Цикл запускается вызовом loop.run_forever() или loop.run_until_complete(), где второй вариант запускает цикл до завершения переданной в него задачи.
# Регистрация событий и обратных вызовов: Прежде чем цикл начнет свою работу, в него нужно добавить события (например, асинхронные функции) и соответствующие обратные вызовы.
# Это делается с помощью функций, таких как loop.create_task() или путем непосредственной регистрации обратного вызова.
# Ожидание событий: Во время выполнения, цикл событий ожидает наступления событий (например, готовности I/O операции).
# Обработка событий: Когда событие наступает (например, данные готовы для чтения из сокета), цикл событий использует обратный вызов или корутину,
# связанную с этим событием, для его обработки.
# Выполнение обратных вызовов: Обратные вызовы запускаются в порядке их добавления или на основе приоритета (если таковой имеется).
# Это может включать запуск корутин, которые являются асинхронными функциями в Python.
# Повторение цикла: После обработки текущих событий и выполнения соответствующих обратных вызовов, цикл событий повторяется, возвращаясь к ожиданию новых событий.
asyncio.get_event_loop()
# Функция asyncio.get_event_loop() в Python является частью библиотеки asyncio, которая предоставляет инфраструктуру для написания однопоточных асинхронных программ
# с использованием корутин, мультиплексирования ввода-вывода, конкурентности и других функций.
# В контексте асинхронного программирования, "event loop" или цикл событий отвечает за выполнение асинхронного кода, обработку событий и координацию задач.
# Основные моменты функции asyncio.get_event_loop():
# Получение текущего цикла событий: Когда вы вызываете asyncio.get_event_loop(), функция пытается получить текущий цикл событий для текущего контекста выполнения.
# Если цикл событий еще не был установлен, функция попытается создать новый цикл событий и установить его как текущий для контекста.
# Контекст выполнения: В Python версии 3.7 и выше, asyncio.get_event_loop() будет искать цикл событий в текущем контексте выполнения, что означает,
# что в разных асинхронных контекстах могут использоваться разные циклы событий. Это особенно актуально при использовании асинхронных функций в разных потоках.
#
# Устаревание в Python 3.10 и выше: Начиная с Python 3.10, asyncio.get_event_loop() считается устаревшей в контексте асинхронных функций.
# Вместо неё предпочтительнее использовать asyncio.get_running_loop(), которая возвращает уже запущенный цикл событий и вызывает исключение, если таковой отсутствует,
# что помогает избежать случайного создания нового цикла событий в непредназначенном контексте.
#
# Взаимодействие с политиками цикла событий: asyncio.get_event_loop() взаимодействует с текущей "политикой цикла событий" (event loop policy), которая определяет поведение
# создания и получения циклов событий.
# Политика цикла событий может быть изменена для кастомизации поведения в различных средах.
# Создание цикла событий: Если функция asyncio.get_event_loop() вызвана в потоке, в котором еще не запущен ни один цикл событий, она создаст новый цикл событий,
# используя фабричный метод, определенный текущей политикой цикла событий.
# Закрытие цикла событий: Если цикл событий был закрыт, asyncio.get_event_loop() создаст новый цикл событий, даже если предыдущий был закрыт в том же контексте.
import asyncio

# Получение текущего цикла событий
loop = asyncio.get_event_loop()

# Планирование выполнения корутины
loop.run_until_complete(asyncio.sleep(1))

# Закрытие цикла событий после завершения работы
loop.close()

asyncio.get_running_loop()
# Функция asyncio.get_running_loop() является частью библиотеки asyncio в Python и предназначена для получения объекта цикла событий,
# который в данный момент выполняет код.
# Эта функция была введена в Python 3.7 и стала предпочтительным способом получения текущего цикла событий в контексте асинхронной корутины или задачи.
# Основные моменты функции asyncio.get_running_loop():
# Возвращение запущенного цикла событий: Функция возвращает цикл событий, который в данный момент запущен. Если функция вызывается в контексте,
# где нет запущенного цикла событий, будет брошено исключение RuntimeError.
# Использование в корутинах: Эта функция чаще всего используется внутри асинхронных функций (корутин),
# где необходимо получить доступ к текущему циклу событий, например, для создания задач (Task) или для работы с низкоуровневыми асинхронными операциями.
# Безопасность: asyncio.get_running_loop() безопаснее в использовании, чем asyncio.get_event_loop(),
# так как последняя может случайно создать новый цикл событий, если она вызывается в контексте, где цикл событий ещё не был установлен.
# get_running_loop() просто бросит исключение,
# что предотвращает неявное создание новых циклов событий.
# Отладка и обработка ошибок: Исключение, вызванное asyncio.get_running_loop(), ясно указывает на то, что функция была вызвана вне асинхронного контекста,
# что помогает разработчикам быстрее находить и исправлять ошибки в своем асинхронном коде.
# Замена устаревших функций: asyncio.get_running_loop() рекомендуется к использованию вместо asyncio.get_event_loop() в новом коде,
# особенно в тех случаях, когда код зависит от выполнения в контексте активного цикла событий.
import asyncio

async def async_function():
    loop = asyncio.get_running_loop()  # Получение текущего запущенного цикла событий
    # ... выполняем асинхронные операции, используя loop ...

asyncio.run(async_function())
# В этом примере async_function() вызывает asyncio.get_running_loop() для получения текущего цикла событий.
# Если async_function() не выполняется внутри цикла событий, вызов функции get_running_loop() приведет к исключению RuntimeError.
# Важные моменты при работе с asyncio.get_running_loop():
# Не использовать вне асинхронного контекста: Поскольку asyncio.get_running_loop() предназначена для использования внутри асинхронного контекста,
# вызов её вне такового приведет к ошибке.
# Использование в асинхронных функциях: Идеально подходит для использования внутри асинхронных функций,
# где необходим доступ к циклу событий для асинхронных операций.
# Замена asyncio.get_event_loop() в новом коде: В новом асинхронном коде следует использовать asyncio.get_running_loop()
# вместо asyncio.get_event_loop() для избегания создания неожиданных циклов событий и потенциальных ошибок.
# asyncio.get_running_loop() является ключевым инструментом для современной асинхронной разработки на Python,
# обеспечивая ясность и безопасность при работе с циклами событий.

loop.run_until_complete(fn())
# Функция loop.run_until_complete(future) является одной из центральных функций в библиотеке asyncio до версии Python 3.7, когда была введена функция asyncio.run().
# Она используется для запуска асинхронного кода до завершения переданной в неё "фьючерс"-подобной сущности, которая может быть корутиной,
# Future объектом, или асинхронным генератором.
# Вот подробное объяснение того, как работает loop.run_until_complete():
# Создание цикла событий
# Прежде всего, для использования loop.run_until_complete(), необходимо иметь объект цикла событий, который можно получить с помощью asyncio.get_event_loop():
# loop = asyncio.get_event_loop()
# Подготовка асинхронной функции
# Далее, у вас должна быть асинхронная функция (корутина), которую вы хотите выполнить:
async def async_function():
    await asyncio.sleep(1)
    return "Результат выполнения"
# Запуск асинхронной функции
# Теперь вы можете запустить эту асинхронную функцию с помощью loop.run_until_complete():
# result = loop.run_until_complete(async_function())
# Что происходит внутри run_until_complete()
# Обертывание в Future: Если переданный объект не является экземпляром Future, run_until_complete() автоматически оборачивает его в объект Future.
# Это необходимо, потому что цикл событий работает с Future объектами для отслеживания состояния асинхронных операций.
# Запуск цикла событий: Функция запускает цикл событий, который берет на себя управление выполнением программы.
# Цикл событий будет выполнять различные задачи (такие как ввод-вывод, таймеры и т.д.), пока Future объект не будет помечен как выполненный (done).
# Ожидание результата: run_until_complete() блокирует выполнение программы до тех пор, пока переданный в неё Future объект не будет выполнен.
# Как только это произойдет, цикл событий остановится.
# Возвращение результата: После завершения Future объекта, run_until_complete() возвращает его результат.
# Если в процессе выполнения возникло исключение, оно будет выброшено в этот момент.
# Закрытие цикла событий
# После выполнения асинхронной операции, цикл событий следует закрыть, чтобы освободить ресурсы:
# loop.close()
# Ошибки и исключения
# Если в процессе выполнения асинхронной операции возникает исключение, оно будет выброшено при вызове run_until_complete().
# Это позволяет отловить исключение обычным образом с помощью блока try/except.
# Примечания
# Начиная с Python 3.7, для запуска асинхронного кода рекомендуется использовать функцию asyncio.run(),
# так как она обрабатывает многие аспекты управления циклом событий автоматически.
# Функция loop.run_until_complete() не предназначена для вызова из асинхронного кода, так как она блокирует поток до завершения асинхронной операции.
# Если run_until_complete() вызывается повторно с тем же циклом событий, это может привести к нежелательным побочным эффектам,
# так как цикл событий предполагается быть одноразовым объектом для одной "сессии" выполнения.
# Использование loop.run_until_complete() было стандартным способом запуска асинхронного кода в ранних версиях asyncio, и знание о том, как она работает,
# все еще полезно для понимания основ асинхронного программирования в Python и для работы с устаревшим кодом.
loop.close()

asyncio.run(fn())
# Функция asyncio.run(main()) является высокоуровневой функцией для запуска асинхронного кода, введенной в Python 3.7.
# Она предназначена для запуска корутины, являющейся точкой входа в асинхронное приложение, и управляет циклом событий за вас.
# Это делает её использование более удобным и безопасным, по сравнению с ручным управлением циклом событий.
# Вот подробное объяснение того, как работает asyncio.run():
# Создание и завершение цикла событий
# Функция asyncio.run(main()) автоматически создает новый цикл событий, запускает переданную корутину main() и блокирует вызывающий поток до тех пор,
# пока корутина не завершится. После завершения корутины цикл событий закрывается. Это упрощает управление ресурсами и предотвращает ошибки,
# связанные с циклом событий.
# Использование
# Чтобы использовать asyncio.run(), сначала вы определяете асинхронную функцию (корутину), которая будет точкой входа в ваше асинхронное приложение:
import asyncio

async def main():
    await asyncio.sleep(1)
    print("Hello, asyncio!")
#Затем запускаете её с помощью asyncio.run():
asyncio.run(main())
# Что происходит внутри asyncio.run()
# Создание нового цикла событий: asyncio.run() автоматически создает новый цикл событий для текущего потока, если такой еще не существует.
# Запуск корутины: Переданная корутина оборачивается в задачу (Task), которая управляется циклом событий. Это позволяет корутине выполняться асинхронно.
# Блокировка до завершения: Вызывающий поток блокируется, пока корутина (и все связанные с ней асинхронные операции) не завершится.
# Возвращение результата: После завершения корутины asyncio.run() возвращает результат её выполнения. Если корутина завершается с исключением,
# оно будет выброшено в вызывающий поток.
# Закрытие цикла событий: После выполнения корутины цикл событий закрывается. Это гарантирует, что все ресурсы, связанные с циклом событий,
# будут корректно освобождены.
# Ошибки и исключения
# Если в процессе выполнения корутины возникает исключение, оно будет выброшено при вызове asyncio.run().
# Это позволяет отловить исключение обычным образом с помощью блока try/except.
# Примечания
# Функция asyncio.run() предназначена для использования как основная точка входа в асинхронное приложение и не должна быть вызвана из другой асинхронной функции
# или корутины.
# Поскольку asyncio.run() закрывает цикл событий, его нельзя использовать для запуска нескольких асинхронных программ в рамках одного и того же потока.
# Если вам нужно запускать несколько асинхронных задач, следует использовать другие механизмы управления задачами внутри одного активного цикла событий.
# asyncio.run() создает и управляет своим собственным циклом событий, что делает её несовместимой с программами,
# которые уже управляют своим циклом событий (например, при использовании loop.run_until_complete()).
# Использование asyncio.run() является предпочтительным способом запуска асинхронного кода в новых программах на Python, начиная с версии 3.7,
# поскольку оно упрощает управление асинхронным выполнением и обеспечивает корректное закрытие ресурсов.

loop.create_task(fn())
# Функция loop.create_task(coro) представляет собой метод объекта цикла событий (event loop) в библиотеке asyncio Python, который используется для планирования
# выполнения корутины.
# Этот метод оборачивает корутину в объект asyncio.Task, который является подклассом asyncio.Future.
# Task управляет выполнением корутины и позволяет ей выполняться асинхронно.
# Давайте разберемся, как это работает, шаг за шагом:
# Шаг 1: Получение цикла событий
# Прежде всего, вам нужно получить текущий цикл событий, с которым вы будете работать:
loop = asyncio.get_event_loop()
# Если вы используете asyncio в контексте, где цикл событий уже запущен (например, в асинхронном веб-сервере),
# вам может быть необходимо использовать asyncio.get_running_loop().
# Шаг 2: Определение корутины
# Затем вы определяете корутину, которую хотите запустить:
async def my_coroutine():
    await asyncio.sleep(1)
    print("Корутина выполнена")
# Шаг 3: Создание задачи
# Используя метод create_task(), вы создаете задачу из корутины:
task = loop.create_task(my_coroutine())
# Шаг 4: Запуск цикла событий (если необходимо)
# Если цикл событий еще не запущен, вы запускаете его, чтобы начать выполнение задач:
loop.run_until_complete(task)
#Или, если вы хотите запустить несколько задач:
loop.run_until_complete(asyncio.gather(task1, task2, task3))
# Что происходит внутри create_task()
# Создание объекта Task: Корутина оборачивается в объект Task. Это специальный тип Future, который используется для отслеживания состояния выполнения корутины.
# Планирование выполнения: Task планируется к выполнению в цикле событий. Это означает, что когда цикл событий будет готов обработать следующее событие,
# он проверит, может ли Task быть выполнен (например, корутина ожидает ввода/вывода или таймера).
# Уведомление о завершении: Как только корутина внутри Task завершается,
# Task устанавливает свое состояние в done и уведомляет всех ожидающих результат.

# Особенности и детали
# Отмена задачи: Task можно отменить в любой момент, вызвав метод task.cancel(). Это приведет к возникновению исключения asyncio.CancelledError
# в корутине при следующей попытке возобновить её выполнение.
# Возвращение результата: Когда корутина завершается, результат её выполнения сохраняется в объекте Task. Вы можете получить его с помощью метода task.result().
# Исключения: Если корутина завершается с исключением, оно будет сохранено в объекте Task. Вы можете получить его с помощью метода task.exception().
# Callback-функции: В Task можно добавить callback-функции, которые будут вызваны по завершении задачи.
# Получение текущей задачи: Вы можете получить текущую задачу в рамках корутины с помощью asyncio.current_task().
# Ожидание задач: Вы можете ожидать завершения задачи, используя await task.
# Пример с callback-функцией
async def my_coroutine():
    await asyncio.sleep(1)
    return "Результат"

def callback(future):
    print("Callback:", future.result())

loop = asyncio.get_event_loop()
task = loop.create_task(my_coroutine())
task.add_done_callback(callback)
loop.run_until_complete(task)
# В этом примере, после завершения корутины, будет вызвана функция callback, которая напечатает результат, возвращенный корутиной.
# Использование loop.create_task() является стандартным способом запуска асинхронных задач в контексте уже запущенного цикла событий.
# Это позволяет создавать и управлять асинхронными операциями в более низкоуровневом стиле по сравнению с asyncio.run(),
# который является более высокоуровневым и рекомендуется для запуска асинхронного кода в новых программах Python.

loop.run_forever()
# loop.run_forever() — это метод объекта цикла событий (event loop) в библиотеке asyncio Python, который запускает цикл событий и заставляет его работать до тех пор,
# пока он не будет остановлен вызовом loop.stop(). Этот метод предназначен для запуска долгоживущих асинхронных приложений,
# таких как серверы и постоянно работающие фоновые задачи.

# Давайте разберемся, как работает loop.run_forever(), в очень детальном изложении:
# Цикл событий (Event Loop)
# Перед тем как погрузиться в детали run_forever(), важно понять, что такое цикл событий.
# Цикл событий — это основной механизм библиотеки asyncio, который управляет асинхронным выполнением кода, событиями ввода-вывода,
# обработкой сетевых соединений и другими операциями. Он отслеживает все асинхронные инструкции и вызывает их, когда соответствующие условия выполнены.

# Использование loop.run_forever()
# Чтобы использовать run_forever(), сначала необходимо получить текущий цикл событий:
loop = asyncio.get_event_loop()
# После получения цикла событий, вы можете запланировать выполнение асинхронных задач с помощью loop.create_task() или других подобных механизмов.
# Затем, вызов loop.run_forever() запускает цикл событий:
loop.run_forever()
# Что происходит внутри run_forever()
# Запуск цикла: Когда вы вызываете run_forever(), цикл событий начинает свою работу. Это означает, что он входит в бесконечный цикл,
# где будет ожидать и обрабатывать события.
# Обработка событий: Цикл событий постоянно проверяет наличие новых событий для обработки.
# Это могут быть готовые к выполнению корутины, возвраты из ожидания ввода-вывода, таймеры и другие события.
# Выполнение корутин: Когда корутина готова к выполнению (например, завершилось ожидание ввода-вывода), цикл событий возобновляет ее выполнение.
# Если во время выполнения корутины возникают новые операции ввода-вывода или ожидания, цикл событий планирует их и продолжает обработку других событий.
# Бесконечный цикл: Цикл событий продолжает работать, пока не будет остановлен. Он не завершится сам по себе, как в случае с run_until_complete(),
# а будет выполняться бесконечно.
# Остановка цикла событий
#Цикл событий можно остановить из любой точки программы, вызвав loop.stop():
loop.stop()
# После вызова stop(), цикл событий завершит текущую итерацию своего бесконечного цикла и остановится.
# Это не означает мгновенную остановку; stop() устанавливает флаг, который сигнализирует циклу событий, что нужно завершить работу после обработки текущих событий.

# После остановки
# После остановки цикла событий с помощью stop(), цикл можно снова запустить с run_forever() или использовать run_until_complete()
# для выполнения конкретной корутины до завершения. Однако, перед повторным использованием цикла событий, часто требуется выполнить некоторую очистку
# или перенастройку.
#
# Примечания
# Очистка ресурсов: После остановки цикла событий важно корректно закрыть и очистить все связанные с ним ресурсы.
# Это может включать закрытие сетевых соединений и других открытых файловых дескрипторов.
# Обработка исключений: Все исключения, возникшие во время выполнения асинхронных задач, должны быть корректно обработаны.
# В противном случае они могут привести к непредвиденному поведению программы.
# Потокобезопасность: Метод run_forever() не является потокобезопасным. Это означает, что его нужно вызывать из того же потока, в котором цикл событий был создан.
#
# Использование loop.run_forever() подходит для сценариев, когда ваше приложение должно постоянно выполняться и реагировать на входящие события, например,
# в реальном времени или в серверных приложениях. Это мощный инструмент для управления асинхронным кодом, но требует тщательного управления и обработки потенциальных
# ошибок.

loop.stop()
# Метод loop.stop() является ключевой функцией асинхронной библиотеки asyncio в Python, который используется для остановки запущенного цикла событий.
# Это важный инструмент управления, который позволяет программистам прерывать выполнение цикла событий из кода. Давайте рассмотрим его очень и очень подробно.
# Что такое цикл событий?
# Цикл событий (event loop) — это центральный компонент асинхронного программирования в asyncio, который управляет распределением и выполнением различных задач в асинхронной программе.
# Он отвечает за запуск корутин, обработку ввода/вывода, выполнение обратных вызовов и другие асинхронные операции.
# Как работает loop.stop()
# Когда метод loop.stop() вызывается, он не останавливает цикл событий немедленно. Вместо этого, он устанавливает внутренний флаг,
# который сигнализирует циклу событий о необходимости завершить текущий цикл выполнения после обработки всех ожидающих событий.
# Это означает, что все запланированные задачи и обратные вызовы, которые уже находятся в очереди, будут выполнены, но после этого цикл событий завершит свою работу.
# Процесс остановки цикла событий
# Вызов метода stop(): Программист вызывает loop.stop() в какой-то момент выполнения программы.
# Установка флага остановки: Внутри цикла событий устанавливается флаг, который сигнализирует о необходимости остановки после завершения текущего цикла обработки событий.
# Завершение обработки событий: Цикл событий завершает обработку всех событий и задач, которые уже находятся в очереди на выполнение.
# Остановка цикла: После того как все ожидающие события и задачи обработаны, цикл событий останавливается.
# Это означает, что методы run_forever() или run_until_complete() вернут управление вызывающему коду.
# Последствия остановки
# После остановки цикла событий, он может быть повторно запущен с помощью run_forever() или run_until_complete(), если он не был закрыт с помощью loop.close().
# Однако, перед повторным запуском цикла событий, может потребоваться выполнение дополнительных действий, таких как планирование новых задач или корутин.
#Пример использования:
import asyncio
loop = asyncio.get_event_loop()
# Запланировать корутину или обратный вызов
loop.create_task(some_coroutine())
# Запустить цикл событий
try:
    loop.run_forever()
finally:
    # Метод stop() был вызван, и цикл событий остановлен.
    # Теперь можно безопасно закрыть цикл и освободить ресурсы.
    loop.close()
# Важные моменты:
# Асинхронная остановка: loop.stop() не блокирует и не останавливает выполнение программы немедленно;
# он лишь устанавливает флаг остановки, который будет учтен после обработки текущих событий.
# Безопасность: Остановка цикла событий безопасным образом гарантирует, что все запланированные задачи и обратные вызовы будут выполнены,
# что предотвращает потерю состояния или данные, зависящие от выполнения этих задач.
# Повторный запуск: Цикл событий можно запустить снова после остановки, если он не был закрыт.
# Освобождение ресурсов: После остановки цикла событий рекомендуется вызвать loop.close(), чтобы освободить системные ресурсы, связанные с циклом.
# Использование loop.stop() является важной частью управления жизненным циклом асинхронных приложений.
# Это позволяет разработчикам иметь контроль над выполнением программы и обеспечивает корректное завершение работы цикла событий.
loop.is_closed()/loop.is_running()
# loop.is_closed() и loop.is_running() являются методами объекта цикла событий (event loop) в библиотеке asyncio Python,
# которые предоставляют информацию о текущем состоянии цикла событий. Давайте детально рассмотрим, что каждый из этих методов делает,
# и в каких контекстах они обычно используются.
loop.is_closed()
# Метод is_closed() возвращает True, если цикл событий был закрыт. Это означает, что цикл событий больше не принимает новые задачи,
# и его нельзя повторно использовать для планирования новых корутин. Если метод возвращает False, цикл событий ещё открыт и может быть
# использован для запуска или планирования асинхронных операций.
# Когда цикл событий считается закрытым?
# Цикл событий становится закрытым в следующих случаях:
# После вызова метода loop.close(). Этот метод должен быть вызван после того, как цикл событий завершил свою работу и больше не нужен.
# Это важный шаг для освобождения ресурсов, связанных с циклом событий.
# Если цикл событий был уничтожен и его ресурсы были очищены сборщиком мусора.
# Пример использования:
loop = asyncio.get_event_loop()
# ... выполнение асинхронных операций ...
loop.close()

if loop.is_closed():
    print("Цикл событий закрыт и не может быть использован.")
# Почему это важно?
# Определение того, закрыт ли цикл событий, важно для предотвращения попыток повторного использования уже закрытого цикла.
# Это может привести к ошибкам во время выполнения, так как закрытый цикл событий не может выполнять новые задачи.
# loop.is_running()
# Метод is_running() возвращает True, если цикл событий в данный момент активен и обрабатывает события. Если метод возвращает False,
# это означает, что цикл событий в настоящее время не запущен. Этот метод полезен для проверки, находится ли цикл событий в процессе выполнения, чтобы, например,
# не пытаться повторно запустить уже работающий цикл событий или не выполнять какие-то действия, которые должны произойти только когда цикл не активен.
# Когда цикл событий считается запущенным?
# Цикл событий считается запущенным во время выполнения одного из своих методов run_forever() или run_until_complete() до тех пор,
# пока эти методы не завершат свою работу или не будут остановлены.

#Пример использования:
loop = asyncio.get_event_loop()

if not loop.is_running():
    loop.run_forever()

# В другом контексте, возможно в callback функции или в другой корутине:
if loop.is_running():
    print("Цикл событий уже запущен.")

# Почему это важно?
# Знание того, запущен ли цикл событий, помогает избежать ошибок управления потоком выполнения программы, таких как попытки запуска уже запущенного цикла или
# выполнения операций, которые предполагают, что цикл событий не активен. Это также может быть полезно для реализации логики, которая должна выполняться
# только когда цикл событий находится или не находится в определенном состоянии.
# Заключение
# Использование is_closed() и is_running() позволяет разработчикам более точно управлять жизненным циклом и состоянием цикла событий в асинхронных приложениях на Python.
# Это помогает предотвратить распространенные ошибки и гарантировать корректное управление ресурсами.