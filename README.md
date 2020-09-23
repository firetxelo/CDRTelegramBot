Simple projetc to study python.

This is a bot that receive commands via Telegram and execute querys on a Zabbix Server.

You can check your active problems, view graphs and more.

Instalation:

	- Use Telegram BotFather to create a Bot
	- pip install -r requirements.txt
	- Set the env variables
		ZBXURL --> Url from zabbix server
		ZBXUSER --> Zabbix server user that had permission to view data
		ZBXPASS --> Password from this user.
		TGTOKEN --> Token of your telegram bot
	- In TelegramBot.py set your Telegram ID in variable ADMINS as a python list.
	- Run TelegramBot.py in nohup or as a service. The script must be always running.



New features will be added in the project every monday.


Commands.txt have a little description about commands that the bot can understand.
