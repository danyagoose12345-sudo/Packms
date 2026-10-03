import winreg as reg
import os
import sys
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("ОШИБКА: Этот скрипт нужно запустить от Имени Администратора!")
    sys.exit()

current_dir = os.path.dirname(os.path.abspath(__file__))
ico_folder = os.path.join(current_dir, "ico_files")
script_path = os.path.join(current_dir, "ratempedit.py")
pythonw_path = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")

# Словарь новых названий типов документов для Windows
extension_details = {
    ".rtmp-text": ("rtmp-text.ico", "RaTemp Standard"),
    ".we-can": ("we-can.ico", "Weed Canfing Document"),
    ".of-tka": ("of-tka.ico", "Offing Tkanat Document"),
    ".source": ("source.ico", "San Office RTMP Document"),
    ".of-main": ("of-main.ico", "Offing Mainer Document")
}

def register_extension(ext, icon_name, description):
    icon_path = os.path.join(ico_folder, icon_name)
    prog_id = f"RaTempEdit{ext.replace('.', '_')}"
    
    try:
        # 1. Привязываем расширение к нашему индификатору программы
        with reg.CreateKey(reg.HKEY_CLASSES_ROOT, ext) as key:
            reg.SetValue(key, "", reg.REG_SZ, prog_id)
            
        # 2. Устанавливаем официальное описание типа файла в Windows
        with reg.CreateKey(reg.HKEY_CLASSES_ROOT, prog_id) as key:
            reg.SetValue(key, "", reg.REG_SZ, description)
            
        # 3. Привязываем красивую иконку
        if os.path.exists(icon_path):
            icon_key_path = f"{prog_id}\\DefaultIcon"
            with reg.CreateKey(reg.HKEY_CLASSES_ROOT, icon_key_path) as key:
                reg.SetValue(key, "", reg.REG_SZ, icon_path)
        
        # 4. Прописываем команду автоматического открытия по двойному клику
        shell_key_path = f"{prog_id}\\shell\\open\\command"
        with reg.CreateKey(reg.HKEY_CLASSES_ROOT, shell_key_path) as key:
            command_str = f'"{pythonw_path}" "{script_path}" "%1"'
            reg.SetValue(key, "", reg.REG_SZ, command_str)
            
        print(f"Расширение {ext} ({description}) полностью обновлено!")
    except Exception as e:
        print(f"Не удалось зарегистрировать {ext}: {e}")

for ext, (icon, desc) in extension_details.items():
    register_extension(ext, icon, desc)

# Сброс кэша Windows для немедленного обновления интерфейса
ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)
print("\n[ ГОТОВО ] Перезапустите проводник. Теперь типы файлов отображаются красиво!")
