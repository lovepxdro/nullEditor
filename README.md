# nullEditor

Um editor de código minimalista, "arcaico" e centrado no teclado, construído em Python e PySide6. Este projeto foi criado como um exercício de aprendizado pessoal, com foco em forçar o usuário a interagir diretamente com suas ferramentas de desenvolvimento.

Não é uma IDE "inteligente". É um ambiente visualmente unificado para os três pilares do desenvolvimento: o editor de texto, o explorador de arquivos e o terminal.

`![Screenshot do nullEditor](screenshot.png)`

## Filosofia

O `nullEditor` é intencionalmente simples. Ele parte do princípio de que um desenvolvedor deve saber como compilar seu código, gerenciar seus arquivos e navegar pelo sistema. A IDE não oferece "ajudas", mas sim um painel único e focado para evitar a troca de janelas.

* **Sem Menus:** A interação é feita por atalhos de teclado, forçando o aprendizado.
* **Editor "Burro":** O editor não possui syntax highlighting. Ele trata todo código (Python, Java, C, etc.) como texto puro.
* **Terminal como Cérebro:** A compilação, execução, controle de versão (Git) e todas as outras tarefas são feitas explicitamente pelo usuário no terminal integrado.

## Funcionalidades

### Geral
* Layout de 3 painéis: Editor (centro), Explorador de Arquivos (direita) e Terminal (embaixo).
* Tema escuro coeso.
* Interface totalmente sem menus.
* Feedback visual (`*` no título) para alterações não salvas.
* Alerta de segurança ao tentar fechar ou abrir um novo arquivo com alterações não salvas.

### Painel do Editor
* Editor de texto agnóstico de linguagem.
* Numeração de linhas.
* Destaque da linha atual.

### Painel Explorador de Arquivos
* Inicia com um botão "Abrir Pasta" para selecionar um diretório de projeto.
* Botão "Trocar Pasta" para mudar de projeto rapidamente.
* Exibição limpa mostrando apenas nomes de arquivos e pastas (sem tamanho, data, etc.).
* Filtro para exibir todos os arquivos, incluindo arquivos ocultos (ex: `.gitignore`).
* **Duplo-clique** em um arquivo para abri-lo no editor.
* **Menu de contexto (clique direito)** com as seguintes ações:
    * Novo Arquivo
    * Nova Pasta
    * Renomear
    * Deletar (com caixa de diálogo de confirmação)

### Painel do Terminal
* Emulador de terminal completo integrado.
* Inicia o `cmd.exe` (Windows) ou `/bin/bash` (Linux/macOS) de forma persistente.
* Começa na pasta "home" do usuário.
* **Sincronização automática:** O terminal muda de diretório (`cd`) automaticamente para a pasta que você abre no Explorador de Arquivos.
* Suporta comandos interativos (ex: `python`, `git commit`).
* Intercepta comandos como `cls` e `clear` para limpar a tela do widget.

## Atalhos de Teclado

Como não há menus, estas são as ações principais:

* `Ctrl+S`: **Salvar** o arquivo atual.
* `Ctrl+Shift+S`: **Salvar como...** (abre a caixa de diálogo).
* `Ctrl+O`: **Abrir arquivo...** (abre a caixa de diálogo).

## Como Executar (Ambiente de Desenvolvimento)

1.  **Clone o repositório:**
    ```bash
    git clone [URL-DO-SEU-REPOSITÓRIO-GIT]
    cd nullEditor
    ```

2.  **Crie um ambiente virtual:**
    ```bash
    python -m venv venv
    ```

3.  **Ative o ambiente:**
    * No Windows: `.\venv\Scripts\activate`
    * No Linux/macOS: `source venv/bin/activate`

4.  **Instale as dependências:**
    ```bash
    pip install PySide6
    ```

5.  **Execute a aplicação:**
    ```bash
    python run.py
    ```

## Para Construir um Executável (Opcional)

Você pode empacotar esta aplicação em um único arquivo `.exe` (ou binário) usando o PyInstaller.

1.  Instale o PyInstaller:
    ```bash
    pip install pyinstaller
    ```

2.  Execute o comando de build:
    ```bash
    pyinstaller --onefile --windowed --name nullEditor --icon=src/resources/icons/app_icon.ico run.py
    ```
    (Nota: Você pode precisar converter seu `.png` para um `.ico` para o ícone funcionar no Windows.)