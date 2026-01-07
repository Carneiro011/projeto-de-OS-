# 🚀 GUIA RÁPIDO DE USO

## 🎯 Início Rápido (3 passos)

### 1️⃣ Instalar e Rodar
```bash
pip install -r requirements.txt
python app.py
```

### 2️⃣ Acessar
- Navegador: `http://localhost:5000`
- Login: `admin` / `admin123`

### 3️⃣ Pronto!
Sistema já está funcionando com todos os recursos.

---

## 👨‍💼 PARA ADMINISTRADORES

### Primeira Configuração (Faça isso primeiro!)

#### 1. Alterar Senha do Admin
```
1. Login: admin / admin123
2. Menu → Usuários
3. Editar admin
4. Nova senha → Salvar
```

#### 2. Criar Usuários
```
Menu → Usuários → Novo Usuário

📝 Dados necessários:
- Nome completo
- Nome de usuário (sem espaços)
- Telefone (79999999999) ⚠️ IMPORTANTE para WhatsApp
- Perfil (Técnico ou Comunicação)
- Senha (mínimo 6 caracteres)
```

### Fluxo de Trabalho Diário

#### 🔧 Gerenciar Ordens de Serviço

**Criar Nova OS:**
```
1. Dashboard TI → Nova OS
2. Preencher dados:
   ✓ Unidade de origem
   ✓ Local de prestação
   ✓ Tipo de equipamento
   ✓ Descrição detalhada
   ✓ Prazo limite
3. Salvar (status: Entrada)
```

**Notificar Técnicos:**
```
1. Dashboard TI → Notificar Técnicos
2. Ver lista de OS pendentes
3. Clicar "Enviar WhatsApp" para cada técnico
4. WhatsApp abre automaticamente
5. Enviar mensagem
```

**Acompanhar Status:**
```
Dashboard TI → Ver cards coloridos:
🟡 Entrada: OS criadas, aguardando técnico
🔵 Andamento: Técnico trabalhando
⚪ Aguardando Peça: Esperando componente
🟢 Pronto: Concluída
🔴 Sem Conserto: Não foi possível
```

#### 👥 Gerenciar Usuários

**Resetar Senha:**
```
1. Usuários → Lista
2. Botão 🔑 (chave)
3. Nova senha → Confirmar
```

**Desativar Usuário:**
```
1. Usuários → Editar
2. Desmarcar "Usuário Ativo"
3. Salvar
```

---

## 🔧 PARA TÉCNICOS

### Como Receber e Aceitar OS

#### 📱 Via WhatsApp (Recomendado)
```
1. Você recebe mensagem:
   🔧 Nova OS #123 disponível!
   📋 Equipamento: Computador
   ...
   ✅ Aceitar OS: [LINK]

2. Clique no link
3. Sistema abre no navegador
4. OS automaticamente atribuída a você
5. Status muda para "Andamento"
```

#### 💻 Via Sistema
```
1. Login no sistema
2. Dashboard TI
3. Ver "OS Disponíveis para Aceitar"
4. Clicar "Aceitar"
```

### Atualizar Status da OS

```
1. Dashboard TI → Minhas OS
2. Clicar em "Editar" (✏️)
3. Mudar status:
   - Andamento: Trabalhando
   - Aguardando Peça: Falta componente
   - Aprovado/Pronto: Finalizado ✅
   - Sem Conserto: Impossível consertar
4. Preencher observações
5. Salvar
```

### Imprimir OS para Assinaturas

```
1. Dashboard TI → Minhas OS
2. Clicar em "Imprimir" (🖨️)
3. Nova aba abre
4. Ctrl + P ou botão Imprimir
5. Levar para coleta de assinaturas
```

---

## 📢 PARA COMUNICAÇÃO

### Criar Briefing com Imagens

#### Passo a Passo Completo:
```
1. Login no sistema
2. Dashboard Comunicação → Novo Briefing
3. Preencher formulário:
   ✓ Secretaria responsável
   ✓ Responsável pelo evento
   ✓ WhatsApp de contato
   ✓ Descrição da ação
   ✓ Data, hora e local
   ✓ Objetivos
   ✓ Meios digitais/impressos
```

#### 📸 Upload de Imagens:
```
4. Rolar até "Upload de Imagens"
5. Clicar "Escolher arquivo"
6. Selecionar múltiplas imagens:
   - Ctrl + Clique (várias de uma vez)
   - Ou arrastar arquivos
7. Aguardar upload
8. Enviar Briefing
```

#### ⚠️ Limites:
- Máximo: 16MB por imagem
- Formatos: JPG, PNG, GIF
- Sem limite de quantidade

### Acompanhar Briefings

```
Dashboard Comunicação → Ver lista

Status:
📥 Recebido: Enviado, aguardando análise
⚙️ Em Produção: Equipe trabalhando
✅ Concluído: Finalizado
```

---

## 🔍 CONSULTAS RÁPIDAS

### Ver seu IP (para acessar de outros PCs)

**Windows:**
```cmd
ipconfig
```
Procure: "Endereço IPv4"

**Linux/Mac:**
```bash
ip addr
# ou
ifconfig
```

### Descobrir se o Sistema Está Rodando

```
Abra navegador: http://localhost:5000

Se abrir a tela de login = ✅ Funcionando!
Se erro = ❌ Sistema não está rodando
```

### Testar Acesso de Outro PC

```
1. No servidor, descubra o IP (ex: 192.168.1.100)
2. No outro PC, abra navegador
3. Digite: http://192.168.1.100:5000
4. Se abrir = ✅ Rede OK!
```

---

## 💡 DICAS E TRUQUES

### 🎯 Técnicos

**✅ Aceite OS rapidamente pelo WhatsApp**
- Link já te leva direto para aceitar
- Evita esquecer de aceitar no sistema

**✅ Atualize o status frequentemente**
- Cliente acompanha em tempo real
- Admin sabe o que está acontecendo

**✅ Use observações**
- Registre o que foi feito
- Ajuda em futuras manutenções

### 📢 Comunicação

**✅ Fotos em alta qualidade**
- Mínimo 1920x1080px
- JPG com qualidade alta

**✅ Preencha todos os campos**
- Mais informação = melhor resultado
- Equipe entende melhor o que fazer

**✅ Meios impressos precisam de licitação**
- Leia o aviso no formulário
- Banner, folder, etc precisam de processo

### 👨‍💼 Administradores

**✅ Cadastre telefones dos técnicos**
- Sem telefone = sem notificação WhatsApp
- Formato: 79999999999 (DDD + número)

**✅ Defina prazos realistas**
- Técnicos veem o prazo
- Ajuda no planejamento

**✅ Faça backup do banco**
```bash
cp secretaria.db secretaria_backup_$(date +%Y%m%d).db
```

---

## 🆘 PROBLEMAS COMUNS

### "Não consigo acessar de outro PC"

**Solução:**
```
1. Verifique o IP do servidor
2. Firewall do Windows:
   - Painel de Controle
   - Firewall
   - Permitir app
   - Adicionar Python
3. Tente: http://IP:5000
```

### "Link do WhatsApp não funciona"

**Solução:**
```
1. Técnico precisa estar cadastrado
2. Técnico precisa ter telefone
3. Sistema precisa estar acessível na rede
4. Técnico pode fazer login normal e aceitar manualmente
```

### "Imagens não aparecem no briefing"

**Solução:**
```
1. Verificar tamanho (máx 16MB)
2. Verificar formato (JPG, PNG, GIF)
3. Verificar se pasta existe:
   static/uploads/briefings/
```

### "Esqueci minha senha"

**Solução:**
```
Admin pode resetar:
1. Usuários → Lista
2. Botão 🔑 (chave)
3. Nova senha

Se for o admin que esqueceu:
1. Deletar banco: rm secretaria.db
2. Rodar: python app.py
3. Login: admin / admin123
```

---

## 📱 ATALHOS ÚTEIS

### Teclado
- `Ctrl + P` - Imprimir página
- `F5` - Atualizar página
- `Ctrl + F` - Buscar na página
- `Ctrl + W` - Fechar aba

### Navegação
- `Dashboard TI` - Ver todas as OS
- `Dashboard Comunicação` - Ver briefings
- `Usuários` - Gerenciar (admin)
- `Notificar Técnicos` - Enviar WhatsApp (admin)

---

## 📞 CONTATOS

**Problemas técnicos:**
- Verifique os logs no terminal
- Leia o README.md completo
- Entre em contato com TI

**Dúvidas de uso:**
- Consulte este guia rápido
- Pergunte ao administrador

---

## ✅ CHECKLIST DE INÍCIO

### Primeira vez usando:
- [ ] Instalou dependências (`pip install -r requirements.txt`)
- [ ] Rodou o sistema (`python app.py`)
- [ ] Fez login como admin (admin/admin123)
- [ ] Alterou senha do admin
- [ ] Criou usuários técnicos
- [ ] Cadastrou telefones dos técnicos
- [ ] Criou usuários de comunicação
- [ ] Testou criar uma OS de teste
- [ ] Testou notificação WhatsApp
- [ ] Testou impressão de OS
- [ ] Testou upload de imagem
- [ ] Testou acesso de outro PC na rede

### Tudo OK? 🎉
Parabéns! Sistema está pronto para uso!

---

**Sistema de Gestão de OS e Briefings**  
*Versão 2.0 - Guia Rápido*  
*Janeiro 2026*