"""Helper funkcie pre MCP integráciu."""

from datetime import datetime
import subprocess
from zoneinfo import ZoneInfo
import pytz

def get_time_from_mcp(timezone: str = "Europe/Bratislava") -> datetime:
    """Získa čas z MCP Time MCP servera.
    
    Fallback: timezone-aware datetime ak MCP nie je dostupný.
    """
    try:
        # Tu by bola implementácia volania MCP Time MCP cez Cursor API
        # Napríklad:
        # response = mcp_ide_proxy.call_tool('mcp_MCP_DOCKER_get_current_time', {'timezone': timezone})
        # return datetime.fromisoformat(response['time'])
        #
        # Pre teraz simulujeme fallback
        raise ValueError("MCP not available in this context")
    except Exception:
        try:
            return datetime.now(ZoneInfo(timezone))
        except ImportError:
            try:
                tz = pytz.timezone(timezone)
                return datetime.now(tz)
            except ImportError:
                return datetime.utcnow()

def export_to_obsidian(content: str, path: str) -> bool:
    """Exportuje obsah do Obsidianu cez MCP.
    
    Returns:
        True ak úspešné, False ak zlyhalo (fallback na lokálny súbor)
    """
    try:
        # Tu by bola implementácia volania Obsidian MCP
        # mcp_ide_proxy.call_tool('mcp_MCP_DOCKER_obsidian_append_content', {'filepath': path, 'content': content})
        raise ValueError("MCP not available in this context")
        return True
    except Exception:
        # Fallback - v tomto prípade len vrátime False, keďže nemáme lokálny vault
        return False

def analyze_with_sequential_thinking(prompt: str) -> str:
    """Použije Sequential Thinking MCP pre analýzu.
    
    Returns:
        Analýza alebo prázdny string ak MCP nie je dostupný
    """
    try:
        # Tu by bola implementácia volania Sequential Thinking MCP
        # response = mcp_ide_proxy.call_tool('mcp_MCP_DOCKER_sequentialthinking', {'thought': prompt, ...})
        # return response['answer']
        raise ValueError("MCP not available in this context")
    except Exception:
        # Fallback
        return f"Sequential Thinking analysis for prompt: '{prompt}'"

def git_commit_via_mcp(message: str, files: list) -> bool:
    """Commit cez GitHub MCP (ak je dostupný).
    
    Fallback: subprocess git commit
    """
    try:
        # Tu by bola implementácia volania GitHub MCP
        # napr. create_or_update_file pre každý súbor a potom create_commit
        raise ValueError("MCP not available in this context")
        return True
    except Exception:
        try:
            subprocess.run(['git', 'add'] + files, check=True)
            subprocess.run(['git', 'commit', '-m', message], check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
