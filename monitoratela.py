import os
import subprocess
import ctypes
from ctypes import wintypes
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Constantes de eventos de sessão
WTS_SESSION_LOCK = 7
WTS_SESSION_UNLOCK = 8

# Tipos adicionais não disponíveis em ctypes.wintypes
HCURSOR = wintypes.HANDLE
HICON = wintypes.HANDLE
HBRUSH = wintypes.HANDLE
WNDPROCTYPE = ctypes.WINFUNCTYPE(ctypes.c_long, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)

def is_process_running(process_name):
    """Verifica se o processo está em execução."""
    try:
        tasks = subprocess.check_output('tasklist', shell=True).decode('cp1252', errors='ignore')
        return process_name.lower() in tasks.lower()
    except Exception as e:
        print(f"Erro ao verificar processos: {e}")
        return False

def start_program(programa, process_name):
    """Inicia o programa se não estiver em execução."""
    if not is_process_running(process_name):
        subprocess.Popen(programa)
        print(f"Programa iniciado: {programa}")
    else:
        print(f"O programa já está em execução: {process_name}")

def stop_program(process_name):
    """Encerra o programa se estiver em execução."""
    if is_process_running(process_name):
        try:
            os.system(f'taskkill /f /im {process_name}')
            print(f"Programa encerrado: {process_name}")
        except Exception as e:
            print(f"Erro ao encerrar o programa: {e}")
    else:
        print(f"O programa já está encerrado: {process_name}")

def session_change_callback(event_type, programa, process_name):
    """Callback para tratar mudanças na sessão."""
    if event_type == WTS_SESSION_LOCK:
        print("Sessão bloqueada.")
        stop_program(process_name)
    elif event_type == WTS_SESSION_UNLOCK:
        print("Sessão desbloqueada.")
        start_program(programa, process_name)

def session_change_listener(programa, process_name):
    """Monitora eventos de bloqueio e desbloqueio de sessão usando a API Wtsapi32."""
    print("Monitorando eventos de bloqueio e desbloqueio...")

    Wtsapi32 = ctypes.WinDLL("Wtsapi32.dll")
    user32 = ctypes.WinDLL("User32.dll")

    WTSRegisterSessionNotification = Wtsapi32.WTSRegisterSessionNotification
    WTSRegisterSessionNotification.argtypes = [wintypes.HWND, wintypes.DWORD]
    WTSRegisterSessionNotification.restype = wintypes.BOOL

    WTSUnRegisterSessionNotification = Wtsapi32.WTSUnRegisterSessionNotification
    WTSUnRegisterSessionNotification.argtypes = [wintypes.HWND]
    WTSUnRegisterSessionNotification.restype = wintypes.BOOL

    class WNDCLASS(ctypes.Structure):
        _fields_ = [
            ("style", wintypes.UINT),
            ("lpfnWndProc", WNDPROCTYPE),
            ("cbClsExtra", wintypes.INT),
            ("cbWndExtra", wintypes.INT),
            ("hInstance", wintypes.HINSTANCE),
            ("hIcon", HICON),
            ("hCursor", HCURSOR),
            ("hbrBackground", HBRUSH),
            ("lpszMenuName", wintypes.LPCWSTR),
            ("lpszClassName", wintypes.LPCWSTR),
        ]

    def wnd_proc(hwnd, msg, wparam, lparam):
        """Processa mensagens de sistema."""
        try:
            if msg == 0x02B1:  # WM_WTSSESSION_CHANGE
                session_change_callback(wparam, programa, process_name)
            return user32.DefWindowProcW(
                wintypes.HWND(hwnd),
                wintypes.UINT(msg),
                wintypes.WPARAM(wparam),
                wintypes.LPARAM(lparam & 0xFFFFFFFFFFFFFFFF)  # Garante valor válido
            )
        except Exception as e:
            print(f"Erro no wnd_proc: {e}")
            return 0

    wnd_class = WNDCLASS()
    wnd_class.lpfnWndProc = WNDPROCTYPE(wnd_proc)
    wnd_class.lpszClassName = "SessionChangeListener"
    class_atom = user32.RegisterClassW(ctypes.byref(wnd_class))

    hwnd = user32.CreateWindowExW(0, class_atom, "SessionChangeListener", 0, 0, 0, 0, 0, None, None, None, None)

    if not hwnd:
        print(f"Erro ao criar janela: {ctypes.GetLastError()}")
        return

    if not WTSRegisterSessionNotification(hwnd, 1):
        print("Erro ao registrar notificações de sessão.")
        return

    print("Monitoramento iniciado. Pressione Ctrl+C para encerrar.")

    try:
        msg = wintypes.MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))
    except KeyboardInterrupt:
        print("Encerrando monitoramento...")
    except Exception as e:
        print(f"Erro no loop de mensagens: {e}")
    finally:
        WTSUnRegisterSessionNotification(hwnd)
        user32.DestroyWindow(hwnd)
        user32.UnregisterClassW(class_atom, None)

if __name__ == "__main__":
    # Oculta a janela principal do tkinter
    Tk().withdraw()
    programa = askopenfilename(title="Selecione o programa a ser monitorado")
    process_name = os.path.basename(programa)

    if not programa:
        print("Nenhum arquivo foi selecionado.")
    elif not os.path.isfile(programa):
        print("Erro: O caminho fornecido não é válido ou o arquivo não existe.")
    else:
        start_program(programa, process_name)
        session_change_listener(programa, process_name)
