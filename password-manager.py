from time import sleep
import mysql.connector
import sys
import pyperclip
from rich import print
from rich.prompt import Prompt

def setup():
    a = mysql.connector.connect(host="localhost", user="root", passwd="246853")
    c = a.cursor()

    try:
        c.execute("create database PasswordManager")
    except:
        pass

    c.execute("use PasswordManager")
    return a, c

def main():
    while True:
        prompt_user()
        sleep(1)

def prompt_user():
    a, c = setup()

    try:
        print('[bold cyan]Password Manager[/bold cyan]')
        print()
        print('[bold]Press[/bold]')
        print('[bold cyan](1)[/bold cyan] to enter a new password')
        print('[bold cyan](2)[/bold cyan] to view passwords')
        print('[bold cyan](3)[/bold cyan] to edit a password')
        print('[bold cyan](4)[/bold cyan] to delete a password')
        print('[bold cyan](5)[/bold cyan] to exit')
        prmpt = Prompt.ask('[bold]Enter your choice[/bold]')

    except:
        sys.exit('Invalid request')

    try:
        assert prmpt in ['1', '2', '3', '4', '5']

    except:
        sys.exit('Invalid request')

    if prmpt == '1':
        service = Prompt.ask('[bold]Enter the service[/bold]')
        c.execute(f"create table if not exists {service} (username varchar(255) primary key, password varchar(255))")
        username = Prompt.ask('[bold]Enter the username[/bold]')
        password = Prompt.ask('[bold]Enter the password[/bold]')
        c.execute(f"insert into {service} values ('{username}', '{password}')")
        a.commit()

    elif prmpt == '2':
        services = []
        c.execute("show tables")
        for i in c:
            services.append(i[0])

        for i, service in enumerate(services, start=1):
            print(f'[bold cyan]({i})[/bold cyan] {service}')

        service_index = int(Prompt.ask('[bold]Enter the service index[/bold]')) - 1
        service = services[service_index]

        c.execute(f"select username from {service}")
        usernames = [i[0] for i in c]

        for i, username in enumerate(usernames, start=1):
            print(f'[bold cyan]({i})[/bold cyan] {username}')

        username_index = int(Prompt.ask('[bold]Enter the username index[/bold]')) - 1
        username = usernames[username_index]

        c.execute(f"select password from {service} where username = '{username}'")
        password = c.fetchone()[0]

        print(f'[bold cyan]Password[/bold cyan]: {password}')

        pyperclip.copy(password)
        print('[bold cyan]Password copied to clipboard[/bold cyan]')

    elif prmpt == '3':
        services = []
        c.execute("show tables")
        for i in c:
            services.append(i[0])

        for i, service in enumerate(services, start=1):
            print(f'[bold cyan]({i})[/bold cyan] {service}')

        service_index = int(Prompt.ask('[bold]Enter the service index[/bold]')) - 1
        service = services[service_index]

        c.execute(f"select username from {service}")
        usernames = [i[0] for i in c]

        for i, username in enumerate(usernames, start=1):
            print(f'[bold cyan]({i})[/bold cyan] {username}')

        username_index = int(Prompt.ask('[bold]Enter the username index[/bold]')) - 1
        username = usernames[username_index]

        c.execute(f"select password from {service} where username = '{username}'")
        password = c.fetchone()[0]

        print(f'[bold cyan]Current Password[/bold cyan]: {password}')

        new_password = Prompt.ask('[bold]Enter the new password[/bold]')

        c.execute(f"update {service} set password = '{new_password}' where username = '{username}'")
        a.commit()
        print('[bold cyan]Password updated[/bold cyan]')

    elif prmpt == '4':
        services = []
        c.execute("show tables")
        for i in c:
            services.append(i[0])

        for i, service in enumerate(services, start=1):
            print(f'[bold cyan]({i})[/bold cyan] {service}')

        service_index = int(Prompt.ask('[bold]Enter the service index[/bold]')) - 1
        service = services[service_index]

        c.execute(f"select username from {service}")
        usernames = [i[0] for i in c]

        for i, username in enumerate(usernames, start=1):
            print(f'[bold cyan]({i})[/bold cyan] {username}')

        username_index = int(Prompt.ask('[bold]Which user do you want to delete?[/bold]')) - 1
        username = usernames[username_index]

        c.execute(f"delete from {service} where username = '{username}'")
        z = Prompt.ask('Are you sure you want to delete this password? ([bold cyan]y[/bold cyan]/[bold cyan]n[/bold cyan])')

        if z == 'y':
            a.commit()
            print('Password deleted')
        else:
            print('Password not deleted')

    elif prmpt == '5':
        print('[bold cyan]Goodbye[/bold cyan]')
        sys.exit()

if __name__ == '__main__':
    
    main()
