# 📘 Guia de Configuração do Bot (setup.md)

Este guia explica como **criar um bot no Discord**, **gerar o token de autenticação**, **gerar o link de convite com permissões corretas** e **configurar o arquivo `config.json`** do Quebra Fone para que o bot possa tocar áudios em um canal de voz.

---

## 1. Criando o Bot no Discord

1. Acesse: [https://discord.com/developers/applications](https://discord.com/developers/applications)
2. Clique em **"New Application"** (Nova aplicação).
3. Dê um nome ao bot (ex: `QuebraFone`) e clique em **Create**.

---

## 2. Criando o Bot e Obtendo o Token

1. Dentro da aplicação criada, no menu lateral, clique em **Bot**.

2. Clique em **"Add Bot"** e confirme.

3. Ative a opção **"Public Bot"** se quiser que outras pessoas o adicionem.

4. Em **TOKEN**, clique em **"Reset Token"** ou **"Copy"** para copiar o **Token do Bot**.

   > ⚠️ **Atenção:** Guarde esse token com segurança. Ele dá acesso total ao seu bot.

5. Cole esse token no arquivo `config.json` no campo `DISCORD_BOT_TOKEN`:

   ```json
   {
     "DISCORD_BOT_TOKEN": "SEU_TOKEN_AQUI"
   }
   ```

---

## 3. Gerando o Link de Convite (Invite URL)

1. Ainda na interface do Developer Portal, clique em **OAuth2 > URL Generator**.

2. Marque as seguintes opções:

   * **Scopes:**

     * `bot`
   * **Bot Permissions:**

     * `Connect`
     * `Speak`
     * `Use Application Commands` *(opcional)*

3. Copie a URL gerada na parte inferior da página.

4. Este é o link que você usará para **adicionar o bot ao seu servidor Discord**.

5. Cole esse link no campo `DISCORD_BOT_INVITE` do `config.json`:

   ```json
   {
     "DISCORD_BOT_INVITE": "https://discord.com/api/oauth2/authorize?..."
   }
   ```

---

## 4. Dando Permissões ao Bot no Servidor

1. Acesse o link gerado e escolha o servidor onde deseja adicionar o bot.
2. Confirme as permissões solicitadas e clique em **Autorizar**.
3. O bot agora está presente no seu servidor.

---

## 5. Estrutura Mínima do `config.json`

```json
{
  "DISCORD_BOT_TOKEN": "SEU_TOKEN_AQUI",
  "DISCORD_BOT_INVITE": "SEU_LINK_DE_CONVITE",
  "EFEITOS_DIR": "efeitos",
  "EMOJIS_DIR": "emojis",
  "VAR_ORDER": "creation_time",
  "VAR_TIME_LIMIT_EFFECT": 5
}
```

> Você pode alterar os diretórios se desejar, mas os padrões funcionam bem.

---

## 6. Pronto!

Agora, ao rodar `main.py`, o bot conectará nos servidores aos quais ele tem acesso e tocará os áudios no canal de voz selecionado pela interface.

> Em caso de problemas, verifique se o token está correto e se o bot tem permissão de conectar e falar no canal de voz desejado.

---

**Divirta-se com o Quebra Fone!**
