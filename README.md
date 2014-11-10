Home Shell - Python Version
=========

Esta versão do sistema [Home Shell - PHP](http://github.com/alisonbento/home-shell/) foi desenvolvida utilizando versões mais "out of the box" com relação a versão em PHP.
Esperamos que com esta nova abordagem, o trabalho de instalação seja mais fácil e exija menos trabalho configurando servidores

### Antigo projeto ###
Para melhores definições do que é o Home Shell, por favor acesse a [Página principal do projeto Home Shell PHP](http://github.com/alisonbento/home-shell/)

### O que mudou? ###
Estamos utilizando tecnologias mais portáveis para o desenvolvimento, de modo a facilitar na hora de instalar ou usar seu Home Shell.
De novidades, temos:
* Python 2.7
  * Virtualenv
* SQLite 3

### Requisitos de instalação ###
#### Linux ####
Primeiro, instale o *virtualenv* para python 2.x:
```$ sudo apt-get install python-virtualenv```

Em seguida, modifique a permissão do arquivo *setup.py* para que possa ser executado:
```$ sudo chmod +x setup.py```

Por fim, execute o arquivo
```$ ./setup.sh```

Tudo certo! Você já pode executar o Home Shell

#### Windows ####
* Habilite [PowerShell Scripts](http://technet.microsoft.com/en-us/library/ee176949.aspx)

* Instalando **Python 2.7.x** (recomendamos a versão 32 bits)
  * Acesse a página principal do [Python](https://www.python.org/)
  * No menu, acesse a opção downloads
  * Selecione a opção **Python 2.7.x**
  * Aguarde o download terminar e execute o arquivo baixado
  * Siga as instruções na tela
 
* Instalando **Pip**
  * Baixe o arquivo [get-pip.py](https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py)
  * Execute o arquivo baixado usando o comando (tenha certeza de estar no diretório correto)
```
PS C:\> python get-pip.py
```

  * Caso queira verificar se a instalação funcionou, execute
```
PS C:\> pip
```

* Instalando **python-virtualenv**
  * Execute o comando
```
PS C:\> pip install python-virtualenv
PS C:\> pip install virtualenvwrapper-powershell
```

* Instalando a aplicação
  * Execute o arquivo ```setup.bat```

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
* Execute a aplicação por meio do script ```venv\Scripts\python app.py```
