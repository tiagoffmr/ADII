Aplicações Distribuídas 2018/19 - Projeto 4 

Trabalho realizado por:
	- Diogo Frazão Nº51595
	- Tiago Robalo Nº51628
	- Vasco Bento Nº51636


Melhoramentos de implementação do Projeto 3:
	- Em relação ao projeto anterior melhorámos algumas exceções, assim como o aspeto dos prints, também adicionamos um maneira de 
	inserir nome de users, bandas e albuns que sejam um ou mais, para isso em vez de utilizar espaço para separar os nomes, é 
	utilizado um underscore( _ ).

Limitações na implementação:
	- Não foi possível para o nosso grupo corrrer o programa com verify = True.

Descriçao:
	- Neste projeto tomam-se medidas de desempenho e segurnaça. O servidor está apto para responder de forma eficiente a diversos 
	clientes. Tanto o servidor como o cliente verificam a autenticidade do interlocutor para que a comunicação seja confidencial 
	(cifrada), para tal servidor e cliente têm certificados de chave pública. Para o âmbito deste projeto os certificados são auto 
	assinados, porque apenas entidades específicas e aptas podem assinar certificados de forma válida. O nosso servidor foi 
	devidamente registado no GitHub e não tem qualquer acesso a informações do cliente (credenciais). Após ser feita a autenticação 
	o utilizador pode realizar diversos comandos.

-----------------------------------------------------------------------------------------------------------------------------------------
	

Ficheiro cliente.py

	python3 cliente.py
	
	Para o correto funcionamento deste ficheiro é necessário o client id e o client id secret como strings na linha 27 e 28, por uns da 
	sua conta GitHub, visto que no momento de entrega estará variavéis com strings vazias. Este ficheiro inicialmente faz um pedido de 
	autorização com o GitHub para que o utilizador seja autenticado e faça os comandos em segurança. Após a autenticação o utilizador pode
	utilizar estes comandos:

		-ADD:

			- Adicionar utilizador:
			ADD USER <nome> <username> <password> - Por exemplo: ADD USER tiago tiagoffmr olaola123
			
			- Adicionar banda:
			ADD BANDA <nome> <ano> <genero> - Por exemplo: ADD BANDA Cage_The_Elephant 2008 rock    
			(Generos possíveis: pop, rock, indy, metal, trance)
			
			- Adicionar album:
			ADD ALBUM <id_banda> <nome> <ano album> - Por exemplo: ADD ALBUM 1 Melophobia 2013

			- Adicionar um rate a um Album por Utilizador:
			ADD <id_user> <id_album> <rate> - Por exemplo: ADD 1 1 MB
			(Rates possíveis: M, MM, S, B, MB)

		- REMOVE:
		
			- Remover Utilizador:
			REMOVE USER <id_user> - Por exemplo: REMOVE USER 1 
		
			- Remover Banda:
			REMOVE BANDA <id_banda> - Por exemplo: REMOVE BANDA 1 

			- Remover Album:
			REMOVE ALBUM <id_album> - Por exemplo: REMOVE ALBUM 1 

			- Remover todos os utilizadores:
			REMOVE ALL USERS

			- Remover todos as bandas:
			REMOVE ALL BANDAS

			- Remover todos os albuns:
			REMOVE ALL ALBUNS

			- Remover todos os albuns de uma banda:
			REMOVE ALL ALBUNS_B <id_banda> - Por exemplo: REMOVE ALL ALBUNS_B 1 

			- Remover todos os albuns classificados por um utilizador
			REMOVE ALL ALBUNS_U <id_user> - Por exemplo: REMOVE ALL ALBUNS_U 1 

			- Remover todos os albuns classificados por um dado rate:
			REMOVE ALL ALBUNS <rate> - Por exemplo: REMOVE ALL ALBUNS MB
			(Rates possíveis: M, MM, S, B, MB)

		- SHOW:
		
			- Mostrar um certo utilizador:
			SHOW USER <id_user> - Por exemplo: SHOW USER 1 
		
			- Mostrar uma certa banda:
			SHOW BANDA <id_banda> - Por exemplo: SHOW BANDA 1 

			- Mostrar um certo album
			SHOW ALBUM <id_album> - Por exemplo: SHOW ALBUM 1 

			- Mostrar todos os utilizadores:
			SHOW ALL USERS

			- Mostrar todas as bandas:
			SHOW ALL BANDAS

			- Mostrar todos os albuns:
			SHOW ALL ALBUNs

			- Mostrar todos os albuns de uma certa banda:
			SHOW ALL ALBUNS_B <id_banda> - Por exemplo: SHOW ALL ALBUNS_B 1

			- Mostrar todos os albuns classificados por um certo utilizador:
			SHOW ALL ALBUNS_U <id_user> - Por exemplo: SHOW ALL ALBUNS_U 1

			- Mostrar todos os albuns classificados por um dado rate:
			SHOW ALL ALBUNS <rate> - Por exemplo: SHOW ALL ALBUNS MB
			(Rates possíveis: M, MM, S, B, MB)

		- UPDATE:

			- Atualiza o rate que um Utilizador fez a um dado Album
			UPDATE ALBUM <id_user> <id_album> <rate> - Por exemplo: UPDATE ALBUM 1 1 B

			- Atualiza a password de um dado Utilizador
			USER <id_user> <password> - Por exemplo: USER 1 adeusadeus321

Ficheiro servidor.py

	python3 servidor.py
	
	A função login é utilizada para autenticar o token enviado pelo cliente atráves de um request ao github e dá append numa lista que 
	contém todos os tokens. A cada pedido feito ao servidor é também enviado o token, que é comparado com a lista de tokens válidos até 
	ao momento, através da função authenticate.
	
Ficheiro spotify.py:

	Este ficheiro serve de complemento para o servidor. A função show_banda recebe um nome de uma banda e devolve uma lista com o nome desta, 
	o(s) géneros, o número de seguidores e a popularidade. A função show_album recebe um nome de uma album e devolve uma lista com o nome 
	deste, o ano em que foi lançado, o nome do artista e o número de canções. Não é necessário nenhum comando para correr esta parte do 
	projeto.