# Quebra Fone – Bot de Efeitos Sonoros para Discord com Interface Gráfica (GUI) em Pygame

<img src="assets/icon.png" alt="Quebra Fone Logo" width="100">


**Quebra Fone** é um bot divertido e prático para Discord, que permite tocar efeitos sonoros em canais de voz através de uma interface gráfica intuitiva desenvolvida com Pygame. Ideal para animar conversas, partidas e reuniões!

## ✨ Destaques

* **Interface Gráfica Interativa:** Janela dedicada feita com Pygame para controle total dos sons.
* **Escolha de Servidor e Canal de Voz:** Tudo pela GUI, sem comandos manuais.
* **Botões para cada Efeito Sonoro:** Clique para tocar, simples assim.
* **Personalização com Emojis e Ícones:** Associe imagens a cada som para facilitar a identificação.
* **Totalmente Customizável:** Basta adicionar seus áudios e ícones nas pastas apropriadas.
* **Desconexão Automática:** Ao fechar a janela, o bot se despede automaticamente do canal de voz.

---

## 🔧 Requisitos

* Python 3.8 ou superior
* Bibliotecas: `discord.py`, `pygame`
* Token de bot do Discord ([Tutorial para obter um token](https://discord.com/developers/applications))
* Arquivos de áudio (.mp3, .wav, .ogg)
* Arquivos de imagem (.png) para os ícones (opcional, mas recomendável)

---

## 🚀 Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/SeuUsuario/Quebra-Fone.git
   cd Quebra-Fone
   ```

2. **Crie e ative um ambiente virtual (opcional, mas recomendado):**

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

   *(O arquivo `requirements.txt` deve conter `discord.py` e `pygame`)*

---

## ⚙️ Configuração

1. **Crie o arquivo `config.json`:**

   ```json
   {
    "DISCORD_BOT_TOKEN": "SEU_TOKEN_DO_BOT_AQUI",
    "DISCORD_BOT_INVITE": "SEU_LINK_CONVITE_BOT",
    "EFEITOS_DIR": "efeitos",
    "EMOJIS_DIR": "emojis",
    "VAR_ORDER": "creation_time",
    "VAR_TIME_LIMIT_EFFECT": 5
   }
   ```

   * Substitua pelo seu token real.
   * Os diretórios são opcionais (valores padrão: `efeitos` e `emojis`).

2. **Adicione seus efeitos sonoros:**
   Coloque seus arquivos de áudio na pasta especificada (`efeitos/` por padrão).

3. **Adicione ícones ou emojis (opcional):**
   Coloque arquivos `.png` na pasta `emojis/`, com o **mesmo nome** do áudio correspondente.
   Exemplo:

   * `risada.mp3` → `risada.png`
   * Um `default.png` será usado se não houver imagem correspondente.

---

## ▶️ Como Executar

Certifique-se de que o ambiente virtual está ativado e rode:

```bash
python main.py
```

---

## 🐫 Como Usar a Interface

1. Ao abrir, a GUI mostra os servidores onde o bot está.
2. Clique em um servidor e, em seguida, em um canal de voz.
3. A tela principal exibirá os botões de som com os ícones.
4. Clique nos botões para tocar os sons no canal de voz.
5. Feche a janela para desconectar o bot.

---

## 📂 Estrutura do Projeto

```
.
├── config.json          # Arquivo de configuração (você cria)
├── main.py              # Arquivo principal do bot
├── requirements.txt     # Dependências
├── assets/icon.ico             # Ícone do bot (opcional)
├── src/                 # Código modularizado
│   ├── audio.py         # Funções de áudio
│   ├── emoji.py         # Carregamento de ícones
│   └── utils.py         # Funções auxiliares
├── efeitos/     # Coloque seus arquivos de áudio aqui
│   └── exemplo.mp3
├── emojis/              # Coloque seus ícones aqui
│   ├── default.png
│   └── exemplo.png
└── README.md            # Este arquivo
```

---

## 📸 Capturas de Tela

<!-- Substitua pelos seus arquivos reais -->

```
![Seleção de Servidor](screenshots/server_select.png)
![Seleção de Canal](screenshots/channel_select.png)
![Botões de Sons](screenshots/effects_buttons.png)
```

---

[⬇️ Download App Windows](https://github.com/EngDiego/application-phone-breaker/raw/main/dist/QuebraFone.zip)

> 💡 **Usuários de Windows (sem Python instalado):**
>
> Após baixar e **descompactar** o arquivo `.zip`, localize e edite o arquivo `config.json` que está na pasta extraída.
>
> Nele, você precisa preencher duas informações obrigatórias:
>
> ```json
> {
>   "DISCORD_BOT_TOKEN": "SEU_TOKEN_DO_BOT_AQUI",
>   "DISCORD_BOT_INVITE": "SEU_LINK_CONVITE_BOT"
> }
> ```
>
> Essas informações são obtidas ao **criar seu bot no site do Discord**:  
> 👉 [https://discord.com/developers/applications/](https://discord.com/developers/applications/)
>
> Para um passo a passo completo de como criar o bot, gerar o link de convite e configurar o token, acesse o guia:  
> 📘 [setup.md](setup.md)

---

## 💪 Contribuindo

Contribuições são bem-vindas! Abra uma issue ou envie um pull request se quiser colaborar.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais informações.

---

## ❤️ Créditos

Desenvolvido por \[Diego Soprana Gomes].

Divirta-se com o **Quebra Fone** e compartilhe a bagunça sonora! 🎧🚀
