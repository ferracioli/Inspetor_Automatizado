# main.py refatorado
import sys
sys.stdout.reconfigure(encoding='utf-8')

import time
import threading
import tkinter as tk
from tkinter import scrolledtext
from argparse import ArgumentParser
from playsound import playsound
from agent.code_validator import CodeValidatorAgent
from integrations.git_integrations import GitHandler
from config import REPO_PATH

class CodeSentinelGUI(tk.Tk):
    def __init__(self, repo_path, interval):
        super().__init__()
        self.repo_path = repo_path
        self.interval = interval
        self.agent = CodeValidatorAgent()
        self.git_handler = GitHandler(REPO_PATH)
        self.processed_files = set()
        self.running = False
        
        self.title("CodeSentinel AI - Monitoramento em Tempo Real")
        self.geometry("600x500")
        self._setup_ui()
        self._setup_bindings()
        
    def _setup_ui(self):
        """Configura os componentes da interface gráfica"""
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Área de logs
        self.logs_area = scrolledtext.ScrolledText(
            self.main_frame,
            wrap=tk.WORD,
            state='normal',
            font=('Consolas', 10)
        )
        self.logs_area.pack(expand=True, fill='both')
        
        # Controles
        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack(fill='x', pady=5)
        
        self.btn_start = tk.Button(
            self.control_frame,
            text="Iniciar Monitoramento",
            command=self.toggle_monitoring
        )
        self.btn_start.pack(side='left', padx=5)
        
        self.lbl_status = tk.Label(
            self.control_frame,
            text="Status: Parado",
            fg="red"
        )
        self.lbl_status.pack(side='right', padx=5)
        
    def _setup_bindings(self):
        """Configura eventos de teclado"""
        self.bind('<Control-q>', lambda e: self.destroy())
        
    def toggle_monitoring(self):
        """Inicia/para o monitoramento do repositório"""
        if not self.running:
            self.running = True
            self.btn_start.config(text="Parar Monitoramento")
            self.lbl_status.config(text="Status: Monitorando", fg="green")
            threading.Thread(
                target=self._monitor_repository,
                daemon=True
            ).start()
        else:
            self.running = False
            self.btn_start.config(text="Iniciar Monitoramento")
            self.lbl_status.config(text="Status: Parado", fg="red")
    
    def _monitor_repository(self):
        """Thread principal de monitoramento"""
        while self.running:
            try:
                self._check_new_files()
                time.sleep(self.interval)
            except Exception as e:
                self._log_error(f"Erro no monitoramento: {str(e)}")
                break
    
    def _check_new_files(self):
        """Verifica novos arquivos no repositório"""
        python_files = self.git_handler.get_latest_python_files()
        new_files = [f for f in python_files if f not in self.processed_files]
        # playsound('sound.wav')

        if new_files:
            self._log_info(f"Encontrados {len(new_files)} novos arquivos para validar")
            for file_path in new_files:
                self._process_file(file_path)
    
    def _process_file(self, file_path):
        """Processa e valida um arquivo individual"""
        self._log_info(f"Validando: {file_path}")
        code = self.git_handler.get_file_content(file_path)
        
        if code:
            try:
                # result = self.agent.validate_code(
                #             code, 
                #             context=f"Arquivo: {file_path}"
                #         )

                # Chama a validação com streaming
                self.agent.validate_code(
                    code,
                    context=f"Arquivo: {file_path}",
                    callback=self._handle_stream_response,
                    file_path=file_path

                )
                self.processed_files.add(file_path)
            except Exception as e:
                self._log_error(f"Erro na validação: {str(e)}")
        else:
            self._log_warning(f"Não foi possível ler o arquivo: {file_path}")
    
    def _handle_stream_response(self, chunk, file_path):
        """Manipula a resposta em tempo real do agente"""
        self.logs_area.insert(tk.END, f"[{file_path}] {chunk}")
        self.logs_area.see(tk.END)
        self.update_idletasks()
        self._trigger_alert()
        
        # Verifica alertas críticos
        if any(kw in chunk.lower() for kw in {'critical', 'security', 'error'}):
            self._trigger_alert()
    
    def _trigger_alert(self):
        """Dispara alerta sonoro e visual"""
        try:
            playsound('sound.wav')
            self.logs_area.tag_add('alert', 'end-1c linestart', 'end-1c lineend')
            self.logs_area.tag_config('alert', background='#ffcccc')
        except Exception as e:
            self._log_error(f"Erro no alerta: {str(e)}")
    
    def _log_info(self, message):
        self.logs_area.insert(tk.END, f"[INFO] {message}\n")
    
    def _log_warning(self, message):
        self.logs_area.insert(tk.END, f"[WARN] {message}\n", 'warning')
    
    def _log_error(self, message):
        self.logs_area.insert(tk.END, f"[ERRO] {message}\n", 'error')
    
    def _log_success(self, message):
        self.logs_area.insert(tk.END, f"[SUCESSO] {message}\n", 'success')

if __name__ == "__main__":
    parser = ArgumentParser(description="Agente de Validação de Código Python")
    parser.add_argument("--repo", default="./", help="Caminho para o repositório Git")
    parser.add_argument("--interval", type=int, default=300, help="Intervalo de verificação em segundos")
    
    args = parser.parse_args()
    
    app = CodeSentinelGUI(args.repo, args.interval)
    app.mainloop()
