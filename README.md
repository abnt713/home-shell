Home Shell
=========

Home Shell é um sistema de domótica que utiliza a sua rede wifi ou local para controlar diversos aparelhos! Basta baixar, instalar e executar para começar a automatizar sua casa / apto / laboratório e assim vai.

### Antigo projeto ###
A antiga versão [Home Shell PHP](http://github.com/alisonbento/home-shell/) está **descontinuada** uma vez que:
* Complexo de instalar
* Download de várias bibliotecas
* Várias e várias alterações se necessário mudar o diretório

Com isso, migramos para Python, porque:
* É multiplataforma
* Virtualenv
* Mais fácil de manter e alterar

### O que mudou e o que devo ter? ###
Estamos utilizando tecnologias mais portáveis para o desenvolvimento, de modo a facilitar na hora de instalar ou usar seu Home Shell.
De novidades, temos:
* Python 2.7
  * Virtualenv
* SQLite 3

### Requisitos de instalação ###
#### Linux ####
Primeiro, instale o *virtualenv* para python 2.x:
```
$ sudo apt-get install python-virtualenv
```

Em seguida, modifique a permissão do arquivo *setup.py* para que possa ser executado:
```
$ sudo chmod +x setup.py
```

Por fim, execute o arquivo
```
$ ./setup.sh
```

Tudo certo! Você já pode executar o Home Shell

#### Windows ####
Ainda não testamos como instalar o Home Shell no Windows, mas vamos providenciar um método até a primeira release

### Executando ###

#### Linux ####
Modifique as permissões do arquivo *app.py*
```
$ sudo chmod +x app.py
```

Agora, execute o arquivo
```
$ ./app.py
```

#### Windows ####
* Execute a aplicação por meio do script 
```
PS C:\> venv\Scripts\python app.py
```
