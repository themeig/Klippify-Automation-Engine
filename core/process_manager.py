import paths
import os
import sys
import time
import json
import uuid
import threading
import subprocess
from datetime import datetime
from pathlib import Path

BASE_DIR = paths.PROJECT_ROOT
TASKS_STATE_FILE = BASE_DIR / "active_tasks_state.json"

class ProcessManager:
    def __init__(self):
        self.lock = threading.Lock()
        self.tasks = {}  # task_id -> task_dict
        self._load_state()

    def _load_state(self):
        if TASKS_STATE_FILE.exists():
            try:
                with open(TASKS_STATE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Mark any previously 'running' tasks as interrupted since server restarted
                    for tid, t in data.items():
                        if t.get("status") == "running":
                            t["status"] = "interrupted"
                            t["logs"].append(f"[{datetime.now().strftime('%H:%M:%S')}] Server riavviato: processo interrotto.")
                    self.tasks = data
            except Exception as e:
                print(f"[ProcessManager] Errore caricamento stato: {e}")
                self.tasks = {}

    def _save_state(self):
        try:
            with open(TASKS_STATE_FILE, "w", encoding="utf-8") as f:
                # Keep last 50 tasks
                saved = {k: v for k, v in list(self.tasks.items())[-50:]}
                json.dump(saved, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ProcessManager] Errore salvataggio stato: {e}")

    def create_task(self, task_type, name, meta=None):
        task_id = f"task_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task = {
            "id": task_id,
            "type": task_type,  # 'gemini', 'tiktok', 'clipping', 'klippify_sync', 'general'
            "name": name,
            "status": "running",
            "start_time": now_str,
            "start_timestamp": time.time(),
            "end_time": None,
            "duration_seconds": 0,
            "pid": None,
            "meta": meta or {},
            "logs": [f"[{datetime.now().strftime('%H:%M:%S')}] Processo inizializzato: {name}"]
        }
        with self.lock:
            self.tasks[task_id] = task
            self._save_state()
        return task_id

    def log(self, task_id, message):
        with self.lock:
            if task_id in self.tasks:
                ts = datetime.now().strftime("%H:%M:%S")
                log_entry = f"[{ts}] {message}"
                self.tasks[task_id]["logs"].append(log_entry)
                # Keep last 200 logs per task
                if len(self.tasks[task_id]["logs"]) > 200:
                    self.tasks[task_id]["logs"] = self.tasks[task_id]["logs"][-200:]
                self._save_state()

    def finish_task(self, task_id, status="completed", error=None):
        with self.lock:
            if task_id in self.tasks:
                t = self.tasks[task_id]
                t["status"] = status
                t["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                t["duration_seconds"] = round(time.time() - t["start_timestamp"], 1)
                if error:
                    t["error"] = str(error)
                    t["logs"].append(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ ERRORE: {error}")
                else:
                    t["logs"].append(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Processo completato con successo.")
                self._save_state()

    def start_subprocess_task(self, task_type, name, cmd, cwd=None, meta=None, shell=False):
        task_id = self.create_task(task_type, name, meta=meta)
        
        def run_proc():
            try:
                self.log(task_id, f"Esecuzione comando: {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
                
                # Start process capturing stdout/stderr
                proc = subprocess.Popen(
                    cmd,
                    cwd=str(cwd or BASE_DIR),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    encoding="utf-8",
                    errors="replace",
                    shell=shell
                )
                
                with self.lock:
                    if task_id in self.tasks:
                        self.tasks[task_id]["pid"] = proc.pid
                        self._save_state()

                self.log(task_id, f"Processo di sistema avviato (PID: {proc.pid})")

                # Read output in real-time
                for line in iter(proc.stdout.readline, ''):
                    if not line:
                        break
                    clean_line = line.rstrip('\r\n')
                    if clean_line:
                        self.log(task_id, clean_line)

                proc.stdout.close()
                return_code = proc.wait()

                # Check if logs contain fatal errors even if return code is 0
                has_fatal_log = False
                fatal_detail = None
                with self.lock:
                    logs = self.tasks.get(task_id, {}).get("logs", [])
                    for l in logs:
                        l_lower = l.lower()
                        if "[fatal error]" in l_lower or "traceback (most recent call last)" in l_lower or "unicodeencodeerror" in l_lower:
                            has_fatal_log = True
                            fatal_detail = l
                            break

                if return_code == 0 and not has_fatal_log:
                    self.finish_task(task_id, status="completed")
                else:
                    err_msg = fatal_detail or f"Processo terminato con codice di errore {return_code}"
                    self.finish_task(task_id, status="error", error=err_msg)

            except Exception as e:
                self.finish_task(task_id, status="error", error=str(e))

        t = threading.Thread(target=run_proc, daemon=True)
        t.start()
        return task_id

    def kill_task(self, task_id):
        with self.lock:
            if task_id not in self.tasks:
                return False, "Task non trovato"
            
            task = self.tasks[task_id]
            pid = task.get("pid")
            
            # Kill OS process if running
            if pid:
                try:
                    # Windows taskkill /F /T kills process and all child processes
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(pid)], capture_output=True, text=True)
                    self.log(task_id, f"🛑 Inviato segnale di terminazione forzata al PID {pid}")
                except Exception as e:
                    self.log(task_id, f"Errore terminazione PID {pid}: {e}")

            task["status"] = "terminated"
            task["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            task["duration_seconds"] = round(time.time() - task["start_timestamp"], 1)
            task["logs"].append(f"[{datetime.now().strftime('%H:%M:%S')}] 🛑 Processo terminato manualmente dall'utente.")
            self._save_state()
            return True, f"Processo {task_id} terminato con successo."

    def kill_all_active_tasks(self):
        killed = 0
        with self.lock:
            running_ids = [tid for tid, t in self.tasks.items() if t.get("status") == "running"]
        
        for tid in running_ids:
            ok, _ = self.kill_task(tid)
            if ok:
                killed += 1
        return killed

    def clear_finished(self):
        with self.lock:
            self.tasks = {k: v for k, v in self.tasks.items() if v.get("status") == "running"}
            self._save_state()
        return True

    def get_tasks_list(self):
        with self.lock:
            result = []
            now = time.time()
            # Sort with running first, then newest start_timestamp
            all_items = list(self.tasks.values())
            all_items.sort(key=lambda x: (1 if x.get("status") == "running" else 0, x.get("start_timestamp", 0)), reverse=True)
            
            for t in all_items:
                t_copy = dict(t)
                if t_copy.get("status") == "running":
                    duration = round(now - t_copy.get("start_timestamp", now), 1)
                    t_copy["duration_seconds"] = duration
                    t_copy["is_stuck_warning"] = duration > 180  # Warning if running > 3 minutes
                else:
                    t_copy["is_stuck_warning"] = False
                result.append(t_copy)
            return result

# Global singleton
process_manager = ProcessManager()

# Module-level convenience wrappers pointing to global singleton
def create_task(task_type, name, meta=None):
    return process_manager.create_task(task_type, name, meta)

def log(task_id, message):
    return process_manager.log(task_id, message)

def finish_task(task_id, status="completed", error=None):
    return process_manager.finish_task(task_id, status, error)

def start_subprocess_task(task_type, name, cmd, cwd=None, meta=None, shell=False):
    return process_manager.start_subprocess_task(task_type, name, cmd, cwd, meta, shell)

def kill_task(task_id):
    return process_manager.kill_task(task_id)

def kill_all_active_tasks():
    return process_manager.kill_all_active_tasks()

def clear_finished():
    return process_manager.clear_finished()

def get_tasks_list():
    return process_manager.get_tasks_list()
