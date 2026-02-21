#!/usr/bin/env python3
import os
import shutil
import sys
from pathlib import Path
import stat
import time

class FileManager:
    def __init__(self):
        self.current_path = Path.home()
        self.show_hidden = False
    
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def get_size(self, path):
        if path.is_file():
            size = path.stat().st_size
            if size < 1024:
                return f"{size}B"
            elif size < 1024**2:
                return f"{size/1024:.1f}KB"
            elif size < 1024**3:
                return f"{size/1024**2:.1f}MB"
            else:
                return f"{size/1024**3:.1f}GB"
        return ""
    
    def get_permissions(self, path):
        st = path.stat()
        mode = st.st_mode
        permissions = ""
        for who in "USR", "GRP", "OTH":
            for what in "R", "W", "X":
                if mode & getattr(stat, f"S_I{what}{who}"):
                    permissions += what.lower()
                else:
                    permissions += "-"
        return permissions
    
    def list_directory(self):
        try:
            items = list(self.current_path.iterdir())
            
            if not self.show_hidden:
                items = [item for item in items if not item.name.startswith('.')]
            
            # Separar diretórios e arquivos
            dirs = sorted([item for item in items if item.is_dir()])
            files = sorted([item for item in items if item.is_file()])
            
            print(f"\n📍 Local: {self.current_path}")
            print("="*70)
            print(f"{'Permissões':<12} {'Tamanho':<10} {'Modificado':<20} Nome")
            print("="*70)
            
            # Mostrar diretórios primeiro
            for item in dirs:
                mod_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(item.stat().st_mtime))
                perms = self.get_permissions(item)
                print(f"{perms:<12} {'<DIR>':<10} {mod_time:<20} \033[1;34m{item.name}/\033[0m")
            
            # Depois os arquivos
            for item in files:
                size = self.get_size(item)
                mod_time = time.strftime('%Y-%m-%d %H:%M', time.localtime(item.stat().st_mtime))
                perms = self.get_permissions(item)
                print(f"{perms:<12} {size:<10} {mod_time:<20} {item.name}")
            
            print("="*70)
            print(f"Total: {len(dirs)} pastas, {len(files)} arquivos")
            
        except PermissionError:
            print("❌ Sem permissão para acessar este diretório")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def change_directory(self, path):
        try:
            new_path = self.current_path / path
            if new_path.exists() and new_path.is_dir():
                self.current_path = new_path.resolve()
            else:
                print("❌ Diretório não encontrado")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def go_back(self):
        if self.current_path != self.current_path.parent:
            self.current_path = self.current_path.parent
    
    def create_file(self, name):
        try:
            file_path = self.current_path / name
            if not file_path.exists():
                file_path.touch()
                print(f"✅ Arquivo '{name}' criado")
            else:
                print("❌ Arquivo já existe")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def create_folder(self, name):
        try:
            folder_path = self.current_path / name
            if not folder_path.exists():
                folder_path.mkdir()
                print(f"✅ Pasta '{name}' criada")
            else:
                print("❌ Pasta já existe")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def delete_item(self, name):
        try:
            item_path = self.current_path / name
            if item_path.exists():
                confirm = input(f"Tem certeza que deseja deletar '{name}'? (s/N): ")
                if confirm.lower() == 's':
                    if item_path.is_file():
                        item_path.unlink()
                    else:
                        shutil.rmtree(item_path)
                    print(f"✅ '{name}' deletado")
            else:
                print("❌ Item não encontrado")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def copy_item(self, source, destination):
        try:
            source_path = self.current_path / source
            dest_path = self.current_path / destination
            
            if not source_path.exists():
                print("❌ Arquivo fonte não encontrado")
                return
            
            if source_path.is_file():
                shutil.copy2(source_path, dest_path)
            else:
                shutil.copytree(source_path, dest_path)
            
            print(f"✅ Copiado '{source}' para '{destination}'")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def move_item(self, source, destination):
        try:
            source_path = self.current_path / source
            dest_path = self.current_path / destination
            
            if not source_path.exists():
                print("❌ Arquivo fonte não encontrado")
                return
            
            shutil.move(str(source_path), str(dest_path))
            print(f"✅ Movido '{source}' para '{destination}'")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def view_file(self, name):
        try:
            file_path = self.current_path / name
            if file_path.is_file():
                # Tentar ler como texto
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        print(f"\n📄 Conteúdo de '{name}':")
                        print("-"*50)
                        print(content)
                        print("-"*50)
                except UnicodeDecodeError:
                    print("📄 Arquivo binário (não é possível exibir como texto)")
            else:
                print("❌ Não é um arquivo")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def search_files(self, pattern):
        try:
            print(f"\n🔍 Buscando por '{pattern}'...")
            found = []
            for root, dirs, files in os.walk(self.current_path):
                for name in files + dirs:
                    if pattern.lower() in name.lower():
                        full_path = Path(root) / name
                        rel_path = full_path.relative_to(self.current_path)
                        found.append(str(rel_path))
                
                # Limitar para não buscar em muitas pastas
                if len(found) >= 50:
                    break
            
            if found:
                print(f"\n📌 Encontrados {len(found)} itens:")
                for i, item in enumerate(found[:20], 1):
                    print(f"  {i}. {item}")
                if len(found) > 20:
                    print(f"  ... e mais {len(found)-20} itens")
            else:
                print("Nenhum item encontrado")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def toggle_hidden(self):
        self.show_hidden = not self.show_hidden
        status = "ativados" if self.show_hidden else "desativados"
        print(f"📁 Arquivos ocultos {status}")

def main():
    fm = FileManager()
    
    while True:
        fm.clear_screen()
        print("\n" + "╔" + "═"*50 + "╗")
        print("║" + " "*15 + "GERENCIADOR DE ARQUIVOS" + " "*15 + "║")
        print("╚" + "═"*50 + "╝")
        
        fm.list_directory()
        
        print("\n📋 COMANDOS:")
        print("  cd <pasta>    - Entrar na pasta")
        print("  ..            - Voltar")
        print("  mkdir <nome>  - Criar pasta")
        print("  touch <nome>  - Criar arquivo")
        print("  rm <nome>     - Deletar")
        print("  cp <orig> <dest> - Copiar")
        print("  mv <orig> <dest> - Mover")
        print("  view <nome>   - Ver arquivo")
        print("  search <nome> - Buscar")
        print("  hidden        - Mostrar/ocultar arquivos ocultos")
        print("  clear         - Limpar tela")
        print("  exit          - Sair")
        
        cmd = input("\n$ ").strip().split()
        
        if not cmd:
            continue
        
        command = cmd[0].lower()
        
        if command == 'exit':
            print("👋 Até logo!")
            break
        
        elif command == 'clear':
            continue
        
        elif command == 'hidden':
            fm.toggle_hidden()
        
        elif command == '..':
            fm.go_back()
        
        elif command == 'cd' and len(cmd) > 1:
            fm.change_directory(cmd[1])
        
        elif command == 'mkdir' and len(cmd) > 1:
            fm.create_folder(cmd[1])
        
        elif command == 'touch' and len(cmd) > 1:
            fm.create_file(cmd[1])
        
        elif command == 'rm' and len(cmd) > 1:
            fm.delete_item(cmd[1])
        
        elif command == 'cp' and len(cmd) > 2:
            fm.copy_item(cmd[1], cmd[2])
        
        elif command == 'mv' and len(cmd) > 2:
            fm.move_item(cmd[1], cmd[2])
        
        elif command == 'view' and len(cmd) > 1:
            fm.view_file(cmd[1])
        
        elif command == 'search' and len(cmd) > 1:
            fm.search_files(cmd[1])
        
        else:
            print("❌ Comando inválido!")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()
