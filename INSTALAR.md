# ============================================
#  M2 SISTEMA - GUIA DE INSTALAÇÃO
#  Passo a passo completo (sem enrolação)
# ============================================


# ─────────────────────────────────────────────
#  PASSO 1: INSTALAR O PYTHON
# ─────────────────────────────────────────────

1. Abre o navegador e vai em:

       https://www.python.org/downloads/

2. Clica no botão amarelão "Download Python 3.x.x"
   (o número pode variar, tipo 3.13.2 — tanto faz, pega o mais recente)

3. Vai baixar um arquivo tipo "python-3.13.2-amd64.exe"
   Executa ele (duplo clique)

4. ⚠️  MUITO IMPORTANTE ⚠️
   Na PRIMEIRA tela do instalador, lá EMBAIXO, tem dois checkbox:
   
   ☐ Install launcher for all users
   ☐ Add Python to PATH            ← MARCA ESSE AQUI!!!
   
   Se não marcar esse, nada vai funcionar depois.

5. Clica em "Install Now" (a opção de cima)

6. Espera instalar. Vai aparecer "Setup was successful". Fecha.

7. Pra confirmar que deu certo:
   - Aperta  tecla Windows + R
   - Digita:  cmd
   - Aperta Enter
   - No prompt preto que abriu, digita:

         python --version

   - Tem que aparecer algo tipo:  Python 3.13.2
   - Se aparecer "não é reconhecido", desinstala e instala de novo
     marcando aquele checkbox do PATH


# ─────────────────────────────────────────────
#  PASSO 2: CRIAR O BANCO DE DADOS NO PGADMIN
# ─────────────────────────────────────────────

1. Abre o pgAdmin (aquele do elefante azul)
   Ele vai pedir uma senha - é a senha MASTER do pgAdmin
   (se nunca definiu, pode ser que peça pra criar uma agora)

2. No lado ESQUERDO, vai ter uma árvore assim:
   
   ▼ Servers
      ▼ PostgreSQL 15  (ou 14, 16... tanto faz o número)
   
   Clica na setinha do PostgreSQL pra expandir.
   Pode pedir a senha do postgres - digita a senha que você
   definiu quando instalou o PostgreSQL.

3. Agora vai aparecer:

   ▼ Servers
      ▼ PostgreSQL 15
         ▼ Databases
            📁 postgres
            📁 db_neo_...   (esse é o banco do Neo)

4. Clica com o BOTÃO DIREITO em cima de "Databases"

5. No menu que aparece, clica em: "Create" → "Database..."

6. Vai abrir uma janela. Preenche SOMENTE:

   Database:  db_m2_sistema

   (não mexe em mais nada, deixa tudo como está)

7. Clica no botão "Save"

8. PRONTO! Agora na árvore vai aparecer:

   ▼ Databases
      📁 db_m2_sistema    ← esse aqui é o novo!
      📁 db_neo_...
      📁 postgres


# ─────────────────────────────────────────────
#  PASSO 3: DESCOMPACTAR O SISTEMA
# ─────────────────────────────────────────────

1. Pega o arquivo m2sistema.zip que você baixou do Claude

2. Clica com o BOTÃO DIREITO no arquivo

3. "Extrair tudo..." (ou "Extract All...")

4. Escolhe onde quer colocar. Sugestão:

       C:\m2sistema

   (mais simples possível, sem espaço no nome)

5. Clica em "Extrair"

6. Vai ficar assim:
   
   C:\m2sistema\
      ├── run.py
      ├── app.py
      ├── config.py
      ├── requirements.txt
      ├── .env.exemplo
      ├── INSTALAR.md  (este arquivo)
      ├── models\
      ├── routes\
      ├── templates\
      ├── static\
      └── utils\


# ─────────────────────────────────────────────
#  PASSO 4: CONFIGURAR A SENHA DO BANCO
# ─────────────────────────────────────────────

1. Vai na pasta onde descompactou (ex: C:\m2sistema)

2. Procura o arquivo ".env.exemplo"
   
   ⚠️ Se não aparece, é porque o Windows esconde arquivos
   que começam com ponto. Nesse caso:
   - No Explorador de Arquivos, clica em "Exibir" (lá em cima)
   - Marca "Itens ocultos"
   - Agora vai aparecer

3. RENOMEIA esse arquivo de:
      .env.exemplo
   Para:
      .env
   
   (tira o ".exemplo" do final)
   O Windows pode avisar "tem certeza?" — clica Sim.

4. Abre o arquivo .env com o Bloco de Notas
   (botão direito → Abrir com → Bloco de Notas)

5. Dentro tem isso:

      SECRET_KEY=m2-informatica-secret-2026
      DB_HOST=localhost
      DB_PORT=5432
      DB_NAME=db_m2_sistema
      DB_USER=postgres
      DB_PASS=postgres

6. A ÚNICA coisa que talvez precise mudar é o DB_PASS
   Coloca a MESMA SENHA que você usa pra conectar no pgAdmin
   
   Exemplo: se sua senha do PostgreSQL é "minhasenha123":
   
      DB_PASS=minhasenha123
   
   Se sua senha é "postgres" mesmo, não precisa mudar nada.

7. Salva o arquivo (Ctrl+S) e fecha.


# ─────────────────────────────────────────────
#  PASSO 5: INSTALAR AS DEPENDÊNCIAS
# ─────────────────────────────────────────────

1. Aperta  tecla Windows + R
2. Digita:  cmd
3. Aperta Enter

4. No prompt preto, digita (e aperta Enter):

       cd C:\m2sistema

   (ou o caminho onde você descompactou)
   
   ⚠️ Se descompactou e ficou C:\m2sistema\m2sistema\ (pasta dentro
   de pasta), usa:  cd C:\m2sistema\m2sistema

5. Agora digita:

       pip install -r requirements.txt

6. Vai baixar um monte de coisa. Espera terminar.
   No final tem que aparecer "Successfully installed..."
   
   Se der erro "pip não é reconhecido":
   Tenta:  python -m pip install -r requirements.txt


# ─────────────────────────────────────────────
#  PASSO 6: RODAR O SISTEMA!!!
# ─────────────────────────────────────────────

1. No MESMO prompt de comando (cmd), digita:

       python run.py

2. Vai aparecer:

   ==================================================
     M2 INFORMATICA - Sistema de Gestao
     Abra no navegador: http://localhost:5000
   ==================================================

3. Abre o NAVEGADOR (Chrome, Edge, Firefox...)

4. Na barra de endereço digita:

       localhost:5000

5. VAI APARECER A TELA DE LOGIN! 🎉

6. Login:    MACIEL
   Senha:    m2admin


# ─────────────────────────────────────────────
#  COMO PARAR E INICIAR DE NOVO
# ─────────────────────────────────────────────

PARAR:
  No prompt preto onde tá rodando, aperta: Ctrl + C

INICIAR DE NOVO:
  1. Abre o cmd (Windows + R → cmd → Enter)
  2. cd C:\m2sistema
  3. python run.py
  4. Abre localhost:5000 no navegador


# ─────────────────────────────────────────────
#  PROBLEMAS COMUNS
# ─────────────────────────────────────────────

PROBLEMA: "python não é reconhecido como comando"
SOLUÇÃO:  Desinstala o Python e instala de novo, dessa vez
          MARCANDO o checkbox "Add Python to PATH"

PROBLEMA: Erro de conexão com o banco / "could not connect"
SOLUÇÃO:  1. Verifica se o PostgreSQL tá rodando
             (olha se tem o ícone do elefante perto do relógio)
          2. Verifica se a senha no .env tá certa
          3. Verifica se criou o banco "db_m2_sistema" no pgAdmin

PROBLEMA: "Address already in use" / "porta 5000 em uso"
SOLUÇÃO:  Algum programa já tá usando a porta 5000. Fecha ele,
          ou abre o run.py no Bloco de Notas e muda 5000 pra 5001

PROBLEMA: Tela branca / erro 500
SOLUÇÃO:  Olha o prompt preto (cmd) — vai ter o erro lá.
          Me manda um print que eu resolvo.


# ─────────────────────────────────────────────
#  LOGINS PADRÃO
# ─────────────────────────────────────────────
#
#  Usuário     Senha       Perfil
#  ─────────   ─────────   ──────────────
#  MACIEL      m2admin     Administrador
#  MURIELL     m2admin     Administrador
#  NEUSA       m2user      Usuário
#
# ─────────────────────────────────────────────
