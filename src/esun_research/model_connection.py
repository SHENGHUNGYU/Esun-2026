"""Check pinned model identity and maintain only our authorized loopback SSH tunnel."""
import subprocess
import threading
import time
import httpx
from .llm import ModelConfig,OllamaModel
from .gateway import RemoteGateway

class ModelConnection:
    def __init__(self,config_path,ssh_host=None):
        self.config_path=config_path;self.ssh_host=ssh_host;self.process=None;self.lock=threading.Lock()
    def check(self):
        if not self.config_path or not self.config_path.exists():raise ValueError('尚未設定本地模型')
        config=ModelConfig.model_validate_json(self.config_path.read_bytes())
        with httpx.Client(timeout=5,trust_env=False,follow_redirects=False) as client:
            return OllamaModel(config)._identity(client)
    def ensure(self):
        with self.lock:
            try:return self.check()
            except httpx.ConnectError:pass
            except httpx.HTTPError as error:raise ValueError('模型服務無法連線，請確認遠端服務與通道。') from error
            config=ModelConfig.model_validate_json(self.config_path.read_bytes())
            if self.ssh_host not in RemoteGateway.ALLOWED_HOSTS or config.base_url!='http://127.0.0.1:11435':
                raise ValueError('模型通道未連線；請使用 scripts/start-agent.sh 啟動或恢復本地模型服務。')
            # Never replace another listener or terminate another process.
            self.process=subprocess.Popen(['ssh','-N','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes',
                '-o','ConnectTimeout=8','-o','ExitOnForwardFailure=yes','-o','ServerAliveInterval=15',
                '-o','ServerAliveCountMax=3','-L','127.0.0.1:11435:127.0.0.1:11434',
                'nelson@'+self.ssh_host],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            for _ in range(20):
                time.sleep(.25)
                try:return self.check()
                except httpx.ConnectError:
                    if self.process.poll() is not None:break
                except httpx.HTTPError:break
            if self.process.poll() is None:self.process.terminate()
            raise ValueError('模型 SSH 通道恢復失敗；請確認設備連線與遠端 Ollama 服務。')
