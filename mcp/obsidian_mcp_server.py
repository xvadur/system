"""
Full-featured Obsidian MCP Server
Provides complete vault management: search, create, read, update, delete, etc.
"""
import os
import json
from typing import Optional
import httpx
import ssl
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.requests import Request


logger = logging.getLogger(__name__)

# Obsidian credentials (read from environment)
OBSIDIAN_TOKEN = os.getenv("MCP_TOKEN", "changeme")
OBSIDIAN_API_URL = os.getenv("OBSIDIAN_API_URL", "https://127.0.0.1:27124")
OBSIDIAN_API_TOKEN = os.getenv("OBSIDIAN_API_KEY", "changeme")

# Path to Chronology JSONs (Auto-detected relative to workspace root if possible, or env var)
# Workspace root assumption: We are in xvadur_agent/mcp/examples
# Target: xvadur_brave/n8n/chronology_json
DEFAULT_CHRONOLOGY_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "../../../../xvadur_brave/n8n/chronology_json"
))
CHRONOLOGY_PATH = os.getenv("CHRONOLOGY_PATH", DEFAULT_CHRONOLOGY_PATH)

print(f"DEBUG: Loaded MCP_TOKEN starting with: {OBSIDIAN_TOKEN[:4]}...")
print(f"DEBUG: Loaded OBSIDIAN_API_KEY starting with: {OBSIDIAN_API_TOKEN[:4]}...")
print(f"DEBUG: Chronology Path resolved to: {CHRONOLOGY_PATH}")


def verify_token(token: Optional[str]) -> bool:
    """Verify Bearer token."""
    return token == OBSIDIAN_TOKEN


async def get_obsidian_client():
    """Create HTTP client that ignores SSL verification (localhost only)."""
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    return httpx.AsyncClient(verify=ssl_context)


def extract_auth_token(request: Request) -> Optional[str]:
    """Extract Bearer token from Authorization header."""
    auth_header = request.headers.get("Authorization", "")
    return auth_header[7:] if auth_header.startswith("Bearer ") else None


# ============================================================================
# ENDPOINT: /health
# ============================================================================
async def health_check(request: Request):
    """Health check endpoint."""
    return JSONResponse({"status": "ok", "service": "Obsidian MCP Server"}, status_code=200)


# ============================================================================
# HELPER: Recursive Vault Walk
# ============================================================================
async def walk_vault(client, path="/", token=None):
    """Recursively list all files in the vault."""
    files = []
    try:
        # The API expects /vault/ for root, /vault/FolderName/ for subdirectories
        api_path = f"/vault{path}" if path != "/" else "/vault/"
        
        response = await client.get(
            f"{OBSIDIAN_API_URL}{api_path}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10.0,
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # The API returns {"files": ["file1.md", "file2.md", "folder/"]}
            items = []
            if isinstance(data, dict) and "files" in data:
                items = data["files"]
            elif isinstance(data, dict):
                # Sometimes it returns {key: [items]} structure
                for value in data.values():
                    if isinstance(value, list):
                        items.extend(value)
            elif isinstance(data, list):
                items = data
            
            for item in items:
                if isinstance(item, str):
                    if item.endswith("/"):
                        # It's a folder - recurse into it
                        folder_path = f"{path}{item}" if path != "/" else f"/{item}"
                        sub_files = await walk_vault(client, folder_path, token)
                        files.extend(sub_files)
                    else:
                        # It's a file - add with full path
                        file_path = f"{path}{item}" if path != "/" else f"/{item}"
                        # Remove leading slash for consistency
                        files.append(file_path.lstrip("/"))
                        
    except Exception as e:
        logger.error(f"Error walking {path}: {e}")
    
    return files


# ============================================================================
# ENDPOINT: /files
# ============================================================================
async def get_files(request: Request):
    """Get list of all files in Obsidian vault (recursive)."""
    token = extract_auth_token(request)
    if not verify_token(token):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    try:
        async with await get_obsidian_client() as client:
            files = await walk_vault(client, "/", OBSIDIAN_API_TOKEN)
            
            return JSONResponse({
                "total": len(files),
                "files": files, # Return all files, client can paginate if needed
                "timestamp": datetime.now().isoformat(),
            })
    except Exception as e:
        logger.error(f"Get files error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


# ============================================================================
# ENDPOINT: /search
# ============================================================================
async def search_vault(request: Request):
    """Search for files/content in Obsidian vault."""
    token = extract_auth_token(request)
    if not verify_token(token):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    try:
        body = await request.json()
        query = body.get("query", "").lower()
        max_results = body.get("max_results", 20)
    except:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    
    if not query:
        return JSONResponse({"error": "Query required"}, status_code=400)
    
    try:
        async with await get_obsidian_client() as client:
            # 1. Try Obsidian's native search first (if available via API)
            # The Local REST API has a /search/simple endpoint
            search_response = await client.get(
                f"{OBSIDIAN_API_URL}/search/simple",
                params={"q": query},
                headers={"Authorization": f"Bearer {OBSIDIAN_API_TOKEN}"},
                timeout=10.0,
            )
            
            results = []
            
            if search_response.status_code == 200:
                data = search_response.json()
                # API returns list of objects with 'filename', 'score', etc.
                # or sometimes just a list of matches depending on version
                if isinstance(data, list):
                     for item in data:
                        if isinstance(item, dict) and "filename" in item:
                            results.append(item["filename"])
                        elif isinstance(item, str):
                            results.append(item)
            
            # 2. If native search returns nothing or fails, fallback to manual scan
            if not results:
                logger.info("Native search yielded no results, falling back to manual scan...")
                all_files = await walk_vault(client, "/", OBSIDIAN_API_TOKEN)
                for file in all_files:
                    if query in file.lower():
                        results.append(file)
            
            return JSONResponse({
                "query": query,
                "count": len(results),
                "results": results[:max_results],
            })

    except Exception as e:
        logger.error(f"Search error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


# ============================================================================
# ENDPOINT: /read
# ============================================================================
async def read_file(request: Request):
    """Read content of a specific file."""
    token = extract_auth_token(request)
    if not verify_token(token):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    try:
        body = await request.json()
        filepath = body.get("filepath", "")
    except:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    
    if not filepath:
        return JSONResponse({"error": "Filepath required"}, status_code=400)
    
    try:
        async with await get_obsidian_client() as client:
            response = await client.get(
                f"{OBSIDIAN_API_URL}/vault/{filepath}",
                headers={"Authorization": f"Bearer {OBSIDIAN_API_TOKEN}"},
                timeout=5.0,
            )
            
            if response.status_code == 200:
                return JSONResponse({
                    "filepath": filepath,
                    "content": response.text,
                    "size": len(response.text),
                })
            elif response.status_code == 404:
                return JSONResponse({"error": "File not found"}, status_code=404)
            else:
                return JSONResponse({"error": f"Obsidian API error: {response.status_code}"}, status_code=500)
    except Exception as e:
        logger.error(f"Read file error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


# ============================================================================
# ENDPOINT: /create-entry
# ============================================================================
async def create_entry(request: Request):
    """Create a new file/entry in Obsidian vault."""
    token = extract_auth_token(request)
    if not verify_token(token):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    try:
        body = await request.json()
        content = body.get("content", "")
        filename = body.get("filename", "entry.md")
        folder = body.get("folder", "")
    except:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    
    if not content:
        return JSONResponse({"error": "Content required"}, status_code=400)
    
    try:
        file_path = f"{folder}/{filename}" if folder else filename
        
        async with await get_obsidian_client() as client:
            response = await client.put(
                f"{OBSIDIAN_API_URL}/vault/{file_path}",
                content=content.encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {OBSIDIAN_API_TOKEN}",
                    "Content-Type": "text/plain; charset=utf-8"
                },
                timeout=5.0,
            )
            
            if response.status_code in (200, 201, 204):
                return JSONResponse({
                    "success": True,
                    "path": file_path,
                    "action": "created",
                    "timestamp": datetime.now().isoformat(),
                })
            else:
                return JSONResponse({
                    "error": f"Obsidian API error: {response.status_code}",
                    "details": response.text,
                }, status_code=500)
    except Exception as e:
        logger.error(f"Create entry error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


# ============================================================================
# ENDPOINT: /update
# ============================================================================
async def update_file(request: Request):
    """Update content of an existing file."""
    token = extract_auth_token(request)
    if not verify_token(token):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    try:
        body = await request.json()
        filepath = body.get("filepath", "")
        content = body.get("content", "")
        overwrite = body.get("overwrite", True)
    except:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    
    if not filepath or not content:
        return JSONResponse({"error": "Filepath and content required"}, status_code=400)
    
    try:
        async with await get_obsidian_client() as client:
            # First read existing content if not overwriting
            if not overwrite:
                read_response = await client.get(
                    f"{OBSIDIAN_API_URL}/vault/{filepath}",
                    headers={"Authorization": f"Bearer {OBSIDIAN_API_TOKEN}"},
                    timeout=5.0,
                )
                if read_response.status_code == 200:
                    existing = read_response.text
                    content = existing + "\n\n" + content
            
            # Update file
            response = await client.put(
                f"{OBSIDIAN_API_URL}/vault/{filepath}",
                content=content.encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {OBSIDIAN_API_TOKEN}",
                    "Content-Type": "text/plain; charset=utf-8"
                },
                timeout=5.0,
            )
            
            if response.status_code in (200, 201, 204):
                return JSONResponse({
                    "success": True,
                    "path": filepath,
                    "action": "updated",
                    "overwrite": overwrite,
                    "timestamp": datetime.now().isoformat(),
                })
            elif response.status_code == 404:
                return JSONResponse({"error": "File not found"}, status_code=404)
            else:
                return JSONResponse({"error": f"Obsidian API error: {response.status_code}"}, status_code=500)
    except Exception as e:
        logger.error(f"Update file error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


# ============================================================================
# ENDPOINT: /append
# ============================================================================
async def append_to_file(request: Request):
    """Append content to an existing file."""
    token = extract_auth_token(request)
    if not verify_token(token):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    try:
        body = await request.json()
        filepath = body.get("filepath", "")
        content = body.get("content", "")
        separator = body.get("separator", "\n")
    except:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    
    if not filepath or not content:
        return JSONResponse({"error": "Filepath and content required"}, status_code=400)
    
    try:
        async with await get_obsidian_client() as client:
            # Read existing content
            read_response = await client.get(
                f"{OBSIDIAN_API_URL}/vault/{filepath}",
                headers={"Authorization": f"Bearer {OBSIDIAN_API_TOKEN}"},
                timeout=5.0,
            )
            
            if read_response.status_code == 200:
                existing = read_response.text
                new_content = existing + separator + content
            elif read_response.status_code == 404:
                new_content = content
            else:
                return JSONResponse({"error": "Cannot read file"}, status_code=500)
            
            # Write updated content
            response = await client.put(
                f"{OBSIDIAN_API_URL}/vault/{filepath}",
                content=new_content.encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {OBSIDIAN_API_TOKEN}",
                    "Content-Type": "text/plain; charset=utf-8"
                },
                timeout=5.0,
            )
            
            if response.status_code in (200, 201, 204):
                return JSONResponse({
                    "success": True,
                    "path": filepath,
                    "action": "appended",
                    "lines_added": len(content.split("\n")),
                    "timestamp": datetime.now().isoformat(),
                })
            else:
                return JSONResponse({"error": f"Obsidian API error: {response.status_code}"}, status_code=500)
    except Exception as e:
        logger.error(f"Append error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


# ============================================================================
# ENDPOINT: /delete
# ============================================================================
async def delete_file(request: Request):
    """Delete a file from Obsidian vault."""
    token = extract_auth_token(request)
    if not verify_token(token):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    try:
        body = await request.json()
        filepath = body.get("filepath", "")
        confirm = body.get("confirm", False)
    except:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    
    if not filepath:
        return JSONResponse({"error": "Filepath required"}, status_code=400)
    
    if not confirm:
        return JSONResponse({"error": "Set confirm=true to delete file"}, status_code=400)
    
    try:
        async with await get_obsidian_client() as client:
            response = await client.delete(
                f"{OBSIDIAN_API_URL}/vault/{filepath}",
                headers={"Authorization": f"Bearer {OBSIDIAN_API_TOKEN}"},
                timeout=5.0,
            )
            
            if response.status_code in (200, 204):
                return JSONResponse({
                    "success": True,
                    "path": filepath,
                    "action": "deleted",
                    "timestamp": datetime.now().isoformat(),
                })
            elif response.status_code == 404:
                return JSONResponse({"error": "File not found"}, status_code=404)
            else:
                return JSONResponse({"error": f"Obsidian API error: {response.status_code}"}, status_code=500)
    except Exception as e:
        logger.error(f"Delete file error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


# ============================================================================
# ENDPOINT: /create-daily-note
# ============================================================================
async def create_daily_note(request: Request):
    """Create a daily note with standard template."""
    token = extract_auth_token(request)
    if not verify_token(token):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    try:
        body = await request.json()
        date = body.get("date", datetime.now().strftime("%Y-%m-%d"))
        content = body.get("content", "")
        folder = body.get("folder", "daily")
    except:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    
    try:
        # Create standard daily note template
        template = f"""# {date}

## Plán na deň
- [ ] Položka 1
- [ ] Položka 2

## Poznámky

## Peniaze

## Hotové

"""
        if content:
            template += f"\n## Vlastný obsah\n{content}\n"
        
        filename = f"{date}.md"
        file_path = f"{folder}/{filename}"
        
        async with await get_obsidian_client() as client:
            response = await client.put(
                f"{OBSIDIAN_API_URL}/vault/{file_path}",
                content=template.encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {OBSIDIAN_API_TOKEN}",
                    "Content-Type": "text/plain; charset=utf-8"
                },
                timeout=5.0,
            )
            
            if response.status_code in (200, 201, 204):
                return JSONResponse({
                    "success": True,
                    "path": file_path,
                    "date": date,
                    "template": "daily-note",
                    "timestamp": datetime.now().isoformat(),
                })
            else:
                return JSONResponse({"error": f"Obsidian API error: {response.status_code}"}, status_code=500)
    except Exception as e:
        logger.error(f"Create daily note error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


# ============================================================================
# ENDPOINT: /create-from-template
# ============================================================================
async def create_from_template(request: Request):
    """Create a note based on an existing template."""
    token = extract_auth_token(request)
    if not verify_token(token):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    try:
        body = await request.json()
        template_name = body.get("template_name", "")
        filename = body.get("filename", "")
        folder = body.get("folder", "")
        variables = body.get("variables", {}) # Dict of {key: value} to replace {{key}}
    except:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    
    if not template_name or not filename:
        return JSONResponse({"error": "template_name and filename required"}, status_code=400)
    
    try:
        async with await get_obsidian_client() as client:
            # 1. Try to find the template
            # Assuming templates are in "Templates/" folder, but we can search for it
            template_path = f"Templates/{template_name}"
            if not template_path.endswith(".md"):
                template_path += ".md"
                
            # Read template content
            response = await client.get(
                f"{OBSIDIAN_API_URL}/vault/{template_path}",
                headers={"Authorization": f"Bearer {OBSIDIAN_API_TOKEN}"},
                timeout=5.0,
            )
            
            if response.status_code != 200:
                # Try searching for it if not found in default location
                # For now, just error out to keep it simple
                return JSONResponse({"error": f"Template '{template_name}' not found at {template_path}"}, status_code=404)
            
            content = response.text
            
            # 2. Process variables
            # Replace {{date}} with today's date if not provided
            if "date" not in variables:
                variables["date"] = datetime.now().strftime("%Y-%m-%d")
            
            if "time" not in variables:
                variables["time"] = datetime.now().strftime("%H:%M")
                
            if "title" not in variables:
                variables["title"] = filename.replace(".md", "")
            
            # Perform replacements
            for key, value in variables.items():
                content = content.replace(f"{{{{{key}}}}}", str(value))
            
            # 3. Create the new file
            file_path = f"{folder}/{filename}" if folder else filename
            if not file_path.endswith(".md"):
                file_path += ".md"
                
            create_response = await client.put(
                f"{OBSIDIAN_API_URL}/vault/{file_path}",
                content=content.encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {OBSIDIAN_API_TOKEN}",
                    "Content-Type": "text/plain; charset=utf-8"
                },
                timeout=5.0,
            )
            
            if create_response.status_code in (200, 201, 204):
                return JSONResponse({
                    "success": True,
                    "path": file_path,
                    "template": template_name,
                    "timestamp": datetime.now().isoformat(),
                })
            else:
                return JSONResponse({"error": f"Failed to create file: {create_response.status_code}"}, status_code=500)
                
    except Exception as e:
        logger.error(f"Template error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


# ============================================================================
# ENDPOINT: /generate-daily-protocol
# ============================================================================
async def generate_daily_protocol(request: Request):
    """Generate daily protocol using CrewAI from chronology JSON."""
    token = extract_auth_token(request)
    if not verify_token(token):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    try:
        body = await request.json()
        json_path = body.get("json_path", "")
        save_to_obsidian = body.get("save_to_obsidian", True)
        folder = body.get("folder", "Calendar")
    except:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    
    if not json_path:
        return JSONResponse({"error": "json_path required"}, status_code=400)
    
    try:
        import subprocess
        import json as json_lib
        
        # Run CrewAI script
        crewai_script = "/Users/_xvadur/Desktop/Magnum Opus/xvadur_agent/mcp/crewAI/nlp_engine/src/nlp_text_analysis_automation/xvadur_protocol.py"
        
        result = subprocess.run(
            ["python3", crewai_script, json_path],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode != 0:
            return JSONResponse({
                "error": "CrewAI processing failed",
                "details": result.stderr
            }, status_code=500)
        
        # Extract the generated protocol from output
        output_lines = result.stdout.split('\n')
        protocol_start = False
        protocol_lines = []
        
        for line in output_lines:
            if "GENERATED DAILY PROTOCOL:" in line:
                protocol_start = True
                continue
            if protocol_start and line.strip():
                protocol_lines.append(line)
        
        protocol_content = '\n'.join(protocol_lines)
        
        # Save to Obsidian if requested
        if save_to_obsidian:
            # Extract date from JSON
            with open(json_path, 'r') as f:
                data = json_lib.load(f)
            
            date = data.get('date', 'unknown')
            filename = f"Log-{date}.md"
            file_path = f"{folder}/{filename}"
            
            async with await get_obsidian_client() as client:
                create_response = await client.put(
                    f"{OBSIDIAN_API_URL}/vault/{file_path}",
                    content=protocol_content.encode("utf-8"),
                    headers={
                        "Authorization": f"Bearer {OBSIDIAN_API_TOKEN}",
                        "Content-Type": "text/plain; charset=utf-8"
                    },
                    timeout=10.0,
                )
                
                if create_response.status_code not in (200, 201, 204):
                    return JSONResponse({
                        "error": "Failed to save to Obsidian",
                        "status_code": create_response.status_code
                    }, status_code=500)
        
        return JSONResponse({
            "success": True,
            "protocol": protocol_content,
            "saved_to": file_path if save_to_obsidian else None,
            "timestamp": datetime.now().isoformat()
        })
        
    except subprocess.TimeoutExpired:
        return JSONResponse({"error": "CrewAI processing timeout (>5min)"}, status_code=500)
    except Exception as e:
        logger.error(f"Daily protocol generation error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


# ============================================================================
# ENDPOINT: /stats
# ============================================================================
async def get_stats(request: Request):
    """Get statistics about vault."""
    token = extract_auth_token(request)
    if not verify_token(token):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    try:
        async with await get_obsidian_client() as client:
            response = await client.get(
                f"{OBSIDIAN_API_URL}/vault/",
                headers={"Authorization": f"Bearer {OBSIDIAN_API_TOKEN}"},
                timeout=5.0,
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Count items
                total_items = 0
                folders = 0
                files = 0
                
                if isinstance(data, dict):
                    for key, value in data.items():
                        if isinstance(value, (list, tuple)):
                            for item in value:
                                if isinstance(item, str):
                                    total_items += 1
                                    if item.endswith("/"):
                                        folders += 1
                                    else:
                                        files += 1
                
                return JSONResponse({
                    "total_items": total_items,
                    "folders": folders,
                    "files": files,
                    "vault_path": os.path.expanduser("~/Desktop/xvadur_brave"),
                    "chronology_path": CHRONOLOGY_PATH,
                    "timestamp": datetime.now().isoformat(),
                })
            else:
                return JSONResponse({"error": "Cannot get vault stats"}, status_code=500)
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


# ============================================================================
# ENDPOINT: /chronology/list
# ============================================================================
async def list_chronology(request: Request):
    """List available chronology JSON logs."""
    token = extract_auth_token(request)
    if not verify_token(token):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    try:
        if not os.path.exists(CHRONOLOGY_PATH):
             return JSONResponse({"error": f"Chronology path not found: {CHRONOLOGY_PATH}"}, status_code=404)

        files = [f for f in os.listdir(CHRONOLOGY_PATH) if f.endswith('.json')]
        files.sort() # Sort by date (filename)
        
        return JSONResponse({
            "count": len(files),
            "files": files,
            "path": CHRONOLOGY_PATH
        })
    except Exception as e:
        logger.error(f"Chronology list error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


# ============================================================================
# ENDPOINT: /chronology/read
# ============================================================================
async def read_chronology(request: Request):
    """Read a specific chronology JSON log."""
    token = extract_auth_token(request)
    if not verify_token(token):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    try:
        body = await request.json()
        date = body.get("date", "")
        filename = body.get("filename", "")
        
        target_file = ""
        if filename:
            target_file = filename
        elif date:
            target_file = f"{date}.json"
            
        if not target_file:
             return JSONResponse({"error": "Either 'date' (YYYY-MM-DD) or 'filename' required"}, status_code=400)
             
        if not target_file.endswith(".json"):
            target_file += ".json"

        full_path = os.path.join(CHRONOLOGY_PATH, target_file)
        
        if not os.path.exists(full_path):
            return JSONResponse({"error": f"File not found: {target_file}"}, status_code=404)
            
        with open(full_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
            
        return JSONResponse({
            "filename": target_file,
            "date": content.get("date", "unknown"),
            "content": content
        })
            
    except Exception as e:
        logger.error(f"Chronology read error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


# ============================================================================
# ENDPOINT: /rag/search
# ============================================================================
async def rag_search(request: Request):
    """
    Semantic search v RAG indexe (664 promptov → 1,204 chunkov).
    Používa FAISS index a OpenAI embeddings pre vyhľadávanie relevantných promptov.
    """
    token = extract_auth_token(request)
    if not verify_token(token):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    try:
        body = await request.json()
        query = body.get("query", "")
        top_k = body.get("top_k", 5)
        min_score = body.get("min_score", 0.4)
        
        if not query:
            return JSONResponse({"error": "Query parameter required"}, status_code=400)
        
        # Import RAG helper funkcií
        import sys
        from pathlib import Path
        
        # Cesta k RAG helper skriptu
        workspace_root = Path(__file__).parent.parent.parent.parent
        rag_helper_path = workspace_root / "xvadur_brave" / "scripts" / "rag_agent_helper.py"
        
        if not rag_helper_path.exists():
            return JSONResponse({
                "error": "RAG helper script not found",
                "path": str(rag_helper_path)
            }, status_code=500)
        
        # Volanie RAG search cez subprocess
        import subprocess
        import asyncio
        
        # Aktivácia virtual environmentu a spustenie RAG search
        venv_python = workspace_root / "temp_pdf_env" / "bin" / "python3"
        if not venv_python.exists():
            # Fallback na systémový Python
            venv_python = "python3"
        
        cmd = [
            str(venv_python),
            str(rag_helper_path),
            query,
            str(top_k),
            str(min_score)
        ]
        
        # Spustenie subprocess
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(workspace_root)
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            error_msg = stderr.decode('utf-8') if stderr else "Unknown error"
            logger.error(f"RAG search error: {error_msg}")
            return JSONResponse({
                "error": "RAG search failed",
                "details": error_msg
            }, status_code=500)
        
        # Parsovanie JSON výstupu
        try:
            result = json.loads(stdout.decode('utf-8'))
            return JSONResponse(result)
        except json.JSONDecodeError as e:
            logger.error(f"RAG search JSON parse error: {e}")
            return JSONResponse({
                "error": "Failed to parse RAG search results",
                "raw_output": stdout.decode('utf-8')[:500]
            }, status_code=500)
            
    except Exception as e:
        logger.error(f"RAG search error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


# ============================================================================
# ENDPOINT: /rag/query
# ============================================================================
async def rag_query(request: Request):
    """
    RAG Query s automatickou syntézou odpovede.
    
    Namiesto surových promptov vráti syntetizovanú odpoveď, ktorá obsahuje
    hlavné informácie z relevantných promptov. Toto je to, čo užívateľ chce -
    syntetizovanú odpoveď, nie surové prompty.
    """
    token = extract_auth_token(request)
    if not verify_token(token):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    try:
        body = await request.json()
        query = body.get("query", "")
        top_k = body.get("top_k", 10)
        min_score = body.get("min_score", 0.4)
        model = body.get("model", "gpt-4o-mini")
        
        if not query:
            return JSONResponse({"error": "Query parameter required"}, status_code=400)
        
        # Import RAG helper funkcií
        import sys
        from pathlib import Path
        
        # Cesta k RAG helper skriptu
        workspace_root = Path(__file__).parent.parent.parent.parent
        rag_helper_path = workspace_root / "xvadur_brave" / "scripts" / "rag_agent_helper.py"
        
        if not rag_helper_path.exists():
            return JSONResponse({
                "error": "RAG helper script not found",
                "path": str(rag_helper_path)
            }, status_code=500)
        
        # Volanie RAG query cez subprocess (s mode="query" pre syntézu)
        import subprocess
        import asyncio
        
        # Aktivácia virtual environmentu a spustenie RAG query
        venv_python = workspace_root / "temp_pdf_env" / "bin" / "python3"
        if not venv_python.exists():
            venv_python = "python3"
        
        cmd = [
            str(venv_python),
            str(rag_helper_path),
            query,
            str(top_k),
            str(min_score),
            "true",  # use_hybrid
            "query",  # mode - syntetizovaná odpoveď
            model  # model pre syntézu
        ]
        
        # Spustenie subprocess
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(workspace_root)
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            error_msg = stderr.decode('utf-8') if stderr else "Unknown error"
            logger.error(f"RAG query error: {error_msg}")
            return JSONResponse({
                "error": "RAG query failed",
                "details": error_msg
            }, status_code=500)
        
        # Parsovanie JSON výstupu
        try:
            result = json.loads(stdout.decode('utf-8'))
            return JSONResponse(result)
        except json.JSONDecodeError as e:
            logger.error(f"RAG query JSON parse error: {e}")
            return JSONResponse({
                "error": "Failed to parse RAG query results",
                "raw_output": stdout.decode('utf-8')[:500]
            }, status_code=500)
            
    except Exception as e:
        logger.error(f"RAG query error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


# ============================================================================
# Setup routes
# ============================================================================
routes = [
    Route("/health", health_check, methods=["GET"]),
    Route("/files", get_files, methods=["GET"]),
    Route("/search", search_vault, methods=["POST"]),
    Route("/read", read_file, methods=["POST"]),
    Route("/create-entry", create_entry, methods=["POST"]),
    Route("/update", update_file, methods=["POST"]),
    Route("/append", append_to_file, methods=["POST"]),
    Route("/delete", delete_file, methods=["POST"]),
    Route("/create-daily-note", create_daily_note, methods=["POST"]),
    Route("/create-from-template", create_from_template, methods=["POST"]),
    Route("/generate-daily-protocol", generate_daily_protocol, methods=["POST"]),
    Route("/stats", get_stats, methods=["GET"]),
    Route("/chronology/list", list_chronology, methods=["GET"]),
    Route("/chronology/read", read_chronology, methods=["POST"]),
    Route("/rag/search", rag_search, methods=["POST"]),
    Route("/rag/query", rag_query, methods=["POST"]),
]

app = Starlette(routes=routes)


if __name__ == "__main__":
    port = int(os.getenv("MCP_PORT", "27125"))
    print(f"Starting Full Obsidian MCP Server on http://127.0.0.1:{port}/")
    print(f"Available endpoints: /health, /files, /search, /read, /create-entry, /update, /append, /delete, /create-daily-note, /create-from-template, /generate-daily-protocol, /stats, /chronology/list, /chronology/read, /rag/search, /rag/query")
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
