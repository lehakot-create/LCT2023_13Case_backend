
## Запуск в Docker

docker-compose up
==========================================================================================

http://0.0.0.0:8000/api/v1/auth/users/ - POST запрос создает пользователя
JSON request:
{
	"email": "some_name",
	"password": "some_pass"
}
==========================================================================================

http://0.0.0.0:8000/api/v1/auth/token/login/ - вход пользоватля по токену

JSON request:
{
	"email": "some_name",
	"password": "some_pass"
}
==========================================================================================

http://0.0.0.0:8000/api/v1/auth/token/logout/ - выход пользоватля по токену

Headers:
"Authorization": "Token 740ffd4612e03a6ff62aadfdfa5535adbcb444b8"