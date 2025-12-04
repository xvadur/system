"""Helper funkcie pre MCP integráciu."""

from datetime import datetime
import subprocess
import os
from typing import Optional, Dict, List

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None

try:
    import pytz
except ImportError:
    pytz = None

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

def _get_github_repo_info() -> tuple[str, str]:
    """Získa GitHub repository owner a name.
    
    Returns:
        (owner, repo) tuple
    """
    try:
        # Skús zistiť z git remote
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            capture_output=True,
            text=True,
            check=True
        )
        remote_url = result.stdout.strip()
        
        # Parsuj URL (podporuje https:// a git@ formáty)
        if 'github.com' in remote_url:
            if remote_url.startswith('https://'):
                # https://github.com/owner/repo.git
                parts = remote_url.replace('https://github.com/', '').replace('.git', '').split('/')
            elif remote_url.startswith('git@'):
                # git@github.com:owner/repo.git
                parts = remote_url.split(':')[1].replace('.git', '').split('/')
            else:
                parts = remote_url.split('/')[-2:]
            
            if len(parts) >= 2:
                return (parts[0], parts[1].replace('.git', ''))
    except Exception:
        pass
    
    # Fallback: defaultné hodnoty z README.md
    return ("xvadur", "system")

def create_github_issue(title: str, body: str, labels: Optional[List[str]] = None) -> Dict:
    """Vytvorí GitHub Issue cez GitHub MCP (ak je dostupný).
    
    Args:
        title: Názov Issue
        body: Popis Issue
        labels: Zoznam labelov (default: ["quest", "task"])
    
    Returns:
        Dict s kľúčmi: {"number": int, "url": str, "success": bool, "error": str}
    """
    owner, repo = _get_github_repo_info()
    labels = labels or ["quest", "task"]
    
    try:
        # Tu by bola implementácia volania GitHub MCP
        # V Cursor IDE by to bolo:
        # response = mcp_ide_proxy.call_tool('mcp_MCP_DOCKER_issue_write', {
        #     'owner': owner,
        #     'repo': repo,
        #     'method': 'create',
        #     'title': title,
        #     'body': body,
        #     'labels': labels
        # })
        # return {
        #     "number": response.get('number'),
        #     "url": f"https://github.com/{owner}/{repo}/issues/{response.get('number')}",
        #     "success": True
        # }
        raise ValueError("MCP not available in this context")
    except Exception:
        # Fallback: GitHub REST API
        github_token = os.getenv('GITHUB_TOKEN')
        if github_token:
            try:
                import requests
                url = f"https://api.github.com/repos/{owner}/{repo}/issues"
                headers = {
                    "Authorization": f"token {github_token}",
                    "Accept": "application/vnd.github.v3+json"
                }
                data = {
                    "title": title,
                    "body": body,
                    "labels": labels
                }
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                issue_data = response.json()
                return {
                    "number": issue_data.get("number"),
                    "url": issue_data.get("html_url"),
                    "success": True
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"GitHub API error: {str(e)}"
                }
        else:
            return {
                "success": False,
                "error": "MCP not available and GITHUB_TOKEN not set"
            }

def close_github_issue(issue_number: int, comment: Optional[str] = None) -> bool:
    """Zatvorí GitHub Issue cez GitHub MCP (ak je dostupný).
    
    Args:
        issue_number: Číslo Issue
        comment: Voliteľný komentár pred zatvorením
    
    Returns:
        True ak úspešné, False ak zlyhalo
    """
    owner, repo = _get_github_repo_info()
    
    try:
        # Tu by bola implementácia volania GitHub MCP
        # V Cursor IDE by to bolo:
        # if comment:
        #     mcp_ide_proxy.call_tool('mcp_MCP_DOCKER_add_issue_comment', {
        #         'owner': owner,
        #         'repo': repo,
        #         'issue_number': issue_number,
        #         'body': comment
        #     })
        # mcp_ide_proxy.call_tool('mcp_MCP_DOCKER_issue_write', {
        #     'owner': owner,
        #     'repo': repo,
        #     'method': 'update',
        #     'issue_number': issue_number,
        #     'state': 'closed'
        # })
        # return True
        raise ValueError("MCP not available in this context")
    except Exception:
        # Fallback: GitHub REST API
        github_token = os.getenv('GITHUB_TOKEN')
        if github_token:
            try:
                import requests
                
                # Pridaj komentár ak je zadaný
                if comment:
                    comment_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
                    headers = {
                        "Authorization": f"token {github_token}",
                        "Accept": "application/vnd.github.v3+json"
                    }
                    requests.post(comment_url, headers=headers, json={"body": comment})
                
                # Zatvor Issue
                url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
                headers = {
                    "Authorization": f"token {github_token}",
                    "Accept": "application/vnd.github.v3+json"
                }
                response = requests.patch(url, headers=headers, json={"state": "closed"})
                response.raise_for_status()
                return True
            except Exception:
                return False
        else:
            return False

def get_github_issue(issue_number: int) -> Optional[Dict]:
    """Načíta informácie o GitHub Issue.
    
    Args:
        issue_number: Číslo Issue
    
    Returns:
        Dict s informáciami o Issue alebo None ak zlyhalo
    """
    owner, repo = _get_github_repo_info()
    
    try:
        # Tu by bola implementácia volania GitHub MCP
        # V Cursor IDE by to bolo:
        # response = mcp_ide_proxy.call_tool('mcp_MCP_DOCKER_issue_read', {
        #     'owner': owner,
        #     'repo': repo,
        #     'issue_number': issue_number,
        #     'method': 'get'
        # })
        # return response
        raise ValueError("MCP not available in this context")
    except Exception:
        # Fallback: GitHub REST API
        github_token = os.getenv('GITHUB_TOKEN')
        if github_token:
            try:
                import requests
                url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
                headers = {
                    "Authorization": f"token {github_token}",
                    "Accept": "application/vnd.github.v3+json"
                }
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                return response.json()
            except Exception:
                return None
        else:
            return None
