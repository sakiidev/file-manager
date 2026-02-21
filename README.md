# 📁 Gerenciador de Arquivos para Terminal

Um gerenciador de arquivos completo e intuitivo para ser usado diretamente no terminal!

## ✨ Funcionalidades

### 📂 Navegação
- `cd <pasta>` - Entrar em pastas
- `..` - Voltar para pasta anterior
- Visualização com cores (pastas em azul)

### 📝 Operações com Arquivos
- `touch <nome>` - Criar novo arquivo
- `mkdir <nome>` - Criar nova pasta
- `rm <nome>` - Deletar arquivos/pastas (com confirmação)
- `cp <orig> <dest>` - Copiar arquivos/pastas
- `mv <orig> <dest>` - Mover/renomear itens

### 👀 Visualização
- `view <arquivo>` - Ver conteúdo de arquivos de texto
- `search <termo>` - Buscar arquivos recursivamente
- `hidden` - Alternar visualização de arquivos ocultos
- Listagem detalhada com permissões, tamanho e data

### 📊 Informações Exibidas
- Permissões do arquivo (formato Unix)
- Tamanho em formato legível (B, KB, MB, GB)
- Data da última modificação
- Contagem total de pastas e arquivos

## 🚀 Como Usar

1. **Execute o programa:**
   ```bash
   python file_manager.py
