### Equipe:

Victor Crispim

Larah Queiroz

# Descrição:

O sistema é um site simples para gerenciamento de usuários e veículos, oferecendo operações de cadastro, consulta, edição e remoção. 

Ele utiliza padrões do GoF, como Factory Method, Builder, Singleton e Strategy, para organizar a criação de objetos, o acesso aos dados e a construção dos veículos. Também utilizando princípios do GRASP, como Controller, Creator, Information Expert e Low Coupling, para distribuir melhor as responsabilidades entre as classes.


## Propósito do sistema:

O sistema tem o objetivo de realizar o cadastro e gerenciamento de usuários e veículos de forma simples. Ele foi desenvolvido em Python utilizando a biblioteca Streamlit, que fornece a interface gráfica para interação com o usuário.  

Além disso, os dados cadastrados são armazenados em arquivos no formato JSON, permitindo que as informações continuem disponíveis mesmo após o encerramento do site.

#
### O sistema é dividido em duas partes principais:

#### 👤 Gerenciamento de usuários:

•	Cadastrar um usuário informando nome, e-mail e senha.

•	Listar os usuários cadastrados.

•	Editar nome e senha de um usuário.

•	Remover um usuário.

•	Verificar se o e-mail já está cadastrado.

•	Validar se os campos obrigatórios foram preenchidos.

 ### _______________________ E _______________________
#### 🚗 Gerenciamento de veículos:

•	Cadastrar um veículo informando placa, modelo e ano.

•	Listar os veículos cadastrados.

•	Editar modelo e ano.

•	Remover um veículo.

•	Verificar se a placa já está cadastrada.

•	Validar os dados informados.

•	Padronizar a placa em letras maiúsculas.

•	Persistência dos dados
#

## Principais usuários:

Os principais usuários do sistema são pessoas responsáveis pelo cadastro e gerenciamento de usuários e veículos. Por exemplo, em um contexto de uma empresa ou estacionamento, um funcionário poderia utilizar o sistema para cadastrar clientes e seus veículos, consultar os registros, atualizar informações ou excluir cadastros.

O site possui uma interface simples, com um menu lateral que permite escolher entre a parte de usuários e a parte de veículos.
