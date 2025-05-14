# LINUX
1. cd \application-phone-breaker
2. python -m venv .venv
3. .venv\bin\activate
4. pip install -r requirements.txt
5. python main.py

# Windows
1. cd \application-phone-breaker
2. python -m venv .venv
3. .venv\Scripts\activate
4. pip install -r requirements.txt
5. python main.py

# Windows - Make exec
1. pip install pynacl pyinstaller 
2. pyinstaller main.py --console --onedir --name "QuebraFone"  --add-data "config.json;." --add-data "assets;assets" --add-data "efeitos;efeitos" --add-data "emojis;emojis" --icon "assets/icon.ico" --collect-all discord --collect-all nacl --collect-all cffi --hidden-import=discord.opus --hidden-import=_cffi_backend --noconfirm
3. pyinstaller main.py --windowed --onedir --name "QuebraFone"  --add-data "config.json;." --add-data "assets;assets" --add-data "efeitos;efeitos" --add-data "emojis;emojis" --icon "assets/icon.ico" --collect-all discord --collect-all nacl --collect-all cffi --hidden-import=discord.opus --hidden-import=_cffi_backend --noconfirm
4. robocopy ".pack\standart" ".\dist\QuebraFone" /E
5. robocopy ".pack\brabo" ".\dist\QuebraFone" /E
6. .\dist\QuebraFone\QuebraFone.exe          

# Linux Zip arquivos
zip -r quebra_fone_source.zip . \
    --exclude "*.zip" \
    --exclude "quebra_fone_source.zip" \
    --exclude "venv/*" \
    --exclude ".venv/*" \
    --exclude "__pycache__/*" \
    --exclude "*.pyc" \
    --exclude "build/*" \
    --exclude "dist/*" \
    --exclude ".git/*" \
    --exclude ".vscode/*" \
    --exclude ".idea/*" \
    --exclude ".mypy_cache/*" \
    --exclude "*.swp" \
    --exclude "*.bak"

