#!/usr/bin/env python3
"""
🛡️ AI-Powered Security Audit Tool with Multilingual Support
Author: Security Scanner v8.0 - Multilingual AI Auditor
Description: GitHub repos va local CMS/librariyalarni to'liq security audit qilish
OWASP Top 10 2025 + Qo'shimcha zaifliklar + 3 tilli qo'llab-quvvat
"""

import argparse
import os
import sys
import json
import time
import subprocess
import shutil
import tempfile
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import uuid
from datetime import datetime
from pathlib import Path
import html
from groq import Groq
import requests
from typing import List, Dict, Any, Optional, Tuple, Set
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import mimetypes
import magic
import fnmatch
import re
import hashlib
import pickle
from collections import defaultdict
import getpass

# Windows terminalida ranglarni yoqish
if os.name == 'nt':
    os.system('')

# ==================== COLORS ====================
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
MAGENTA = "\033[1;35m"
WHITE = "\033[1;37m"
BOLD = "\033[1m"
RESET = "\033[0m"

# ==================== MULTILINGUAL SUPPORT ====================
class Multilingual:
    """3 tilli qo'llab-quvvat: English, Русский, O'zbek"""
    
    LANGUAGES = {
        "en": f"{BLUE}English{RESET}",
        "ru": f"{BLUE}Русский{RESET}", 
        "uz": f"{BLUE}O'zbek{RESET}"
    }

    # To'liq qizil rangli ASCI Logo
    LOGO_RED = f"""{RED}
    ██████████                                █████████                      
   ░░███░░░░███                              ███░░░░░███                     
    ░███   ░░███  ██████   ██████  ████████ ░███    ░░░   ██████   ██████    
    ░███    ░███ ███░░███ ███░░███░░███░░███░░█████████  ███░░███ ███░░███   
    ░███    ░███░███████ ░███████  ░███ ░███ ░░░░░░░░███░███████ ░███ ░░░    
    ░███    ███ ░███░░░  ░███░░░   ░███ ░███ ███    ░███░███░░░  ░███  ███   
    ██████████  ░░██████ ░░██████  ░███████ ░░█████████ ░░██████ ░░██████    
    ░░░░░░░░░░    ░░░░░░   ░░░░░░   ░███░░░   ░░░░░░░░░   ░░░░░░   ░░░░░░    
                                    ░███                                     
                                    █████                                    
                                    ░░░░░
                         
                         
                         {BOLD}{RED}DeepSec  Security Audit Tool{RESET}{RED}                         
                           Version 1.1 • TheDeepOpc                           
                    https://github.com/TheDeepopc/deepsec                    
                                                                               
                               wwww.thedeep.uz                               
                                    {RESET}"""
    
    # Language selection prompt (Hoshiyalar qizil)
    LANGUAGE_SELECTION = {
        "en": f"""
{LOGO_RED}
{RED}                                                                                  
      {YELLOW}[1]{RESET} English                                                                  
      {YELLOW}[2]{RESET} Русский                                                                 
      {YELLOW}[3]{RESET} O'zbek                                                                   
   {RESET}""",
        "ru": f"""{RED}                                                                                                                                                                     {RESET}
 {LOGO_RED} 
{RED}                                      
  
     {YELLOW}[1]{RESET} English                                                                  
     {YELLOW}[2]{RESET} Русский                                                                 
     {YELLOW}[3]{RESET} O'zbek                                                                   
{RESET}""",
        "uz": f"""{RED}                                                                                                                                                                     {RESET}
 {LOGO_RED} 
{RED}                                                                               
                                                
  
     {YELLOW}[1]{RESET} English                                                                  
     {YELLOW}[2]{RESET} Русский                                                                 
     {YELLOW}[3]{RESET} O'zbek                                                                   
{RESET}"""
    }
    
    # Main menu text (Hoshiyalar qizil)
    MAIN_MENU = {
    "en": {
        "title": f"""{RED}                                                                                                                                                                     {RESET}
 {LOGO_RED} 

{RED}                                                                                                                                                                  {RESET}""",
        "options":  f"""{BLUE}    [1]{RESET} {BLUE} Audit GitHub Repository{RESET}
{BLUE}    [2]{RESET} {BLUE} Audit Local Project{RESET}
{BLUE}    [3]{RESET} {BLUE} Settings{RESET}
{BLUE}    [4]{RESET} {BLUE} Help{RESET}
{BLUE}    [5]{RESET} {BLUE} Exit{RESET}""",
        "github_prompt": f"{WHITE}Enter GitHub repository URL: {RESET}",
        "local_prompt": f"{WHITE}Enter local project path: {RESET}",
        "output_prompt": f"{WHITE}Enter output filename [security_report.html]: {RESET}",
        "settings_title": f"{YELLOW}⚙️ SETTINGS{RESET}",
        "settings_options": f"{YELLOW}[1]{RESET} Change Language\n{YELLOW}[2]{RESET} API Configuration\n{YELLOW}[3]{RESET} Back",
        "help_text": f"""{BLUE}  HELP GUIDE:{RESET}
• Option 1: Enter GitHub URL (e.g., https://github.com/user/repo)
• Option 2: Enter local folder path
• The tool will analyze barcha kod fayllarini zaifliklar uchun
• AI-powered analysis with {BOLD}OWASP Top 10 2025{RESET}""",
        "exit_msg": f"{GREEN}  Goodbye!{RESET}",
        "error_invalid": f"{GREEN}  Invalid option. Please try again.{RESET}",
        "scanning": f"{GREEN}  Scanning project...{RESET}",
        "cloning": f"{GREEN}  Cloning repository...{RESET}",
        "analysis": f"{MAGENTA}  AI Analysis in progress...{RESET}",
        "report_generated": f"{GREEN}  Report generated: {RESET}",
        "no_api_key": f"{RED}  API key not found. Please configure in settings.{RESET}",
    },
    "ru": {
        "title": f"""{RED}                                                                                                                                                                     {RESET}
 {LOGO_RED} 
{RED}                                                                                                                                                                  {RESET}""",
        "options": f"""{BLUE}    [1]{RESET} {BLUE}📡 Аудит GitHub репозитория{RESET}
{BLUE}    [2]{RESET} {BLUE}  Аудит локального проекта{RESET}
{BLUE}    [3]{RESET} {BLUE}  Настройки{RESET}
{BLUE}    [4]{RESET} {BLUE}  Помощь{RESET}
{BLUE}    [5]{RESET} {BLUE}   Выход{RESET}""",
        "github_prompt": f"{WHITE}Введите URL репозитория GitHub: {RESET}",
        "local_prompt": f"{WHITE}Введите путь к локальному проекту: {RESET}",
        "output_prompt": f"{WHITE}Введите имя файла отчета [security_report.html]: {RESET}",
        "settings_title": f"{YELLOW}  НАСТРОЙКИ{RESET}",
        "settings_options": f"{YELLOW}[1]{RESET} Изменить язык\n{YELLOW}[2]{RESET} Настройка API\n{YELLOW}[3]{RESET} Назад",
        "help_text": f"""{BLUE}  СПРАВКА:{RESET}
• Опция 1: Введите URL GitHub
• Опция 2: Введите путь к папке
• Инструмент проанализирует все файлы на уязвимости
• Анализ на основе ИИ с {BOLD}OWASP Top 10 2025{RESET}""",
        "exit_msg": f"{GREEN} До свидания!{RESET}",
        "error_invalid": f"{RED} Неверный вариант.{RESET}",
        "scanning": f"{GREEN}  Сканирование проекта...{RESET}",
        "cloning": f"{GREEN}  Клонирование репозитория...{RESET}",
        "analysis": f"{MAGENTA}  Анализ ИИ в процессе...{RESET}",
        "report_generated": f"{GREEN}  Отчет создан: {RESET}",
        "no_api_key": f"{RED}  Ключ API не найден.{RESET}",
    },
    "uz": {
        "title": f"""{RED}                                                                                                                                                                     {RESET}
 {LOGO_RED} 
{RED}                                                                                                                                                                  {RESET}""",
        "options": f"""{BLUE}    [1]{RESET} {BLUE}📡 GitHub Repositoriyasini Audit qilish{RESET}
{BLUE}    [2]{RESET} {BLUE}  Lokal Loyihani Audit qilish{RESET}
{BLUE}    [3]{RESET} {BLUE}   Sozlamalar{RESET}
{BLUE}    [4]{RESET} {BLUE}  Yordam{RESET}
{BLUE}    [5]{RESET} {BLUE}  Chiqish{RESET}""",
        "github_prompt": f"{WHITE}GitHub repositoriya URL manzilini kiriting: {RESET}",
        "local_prompt": f"{WHITE}Lokal loyiha joylashuvini kiriting: {RESET}",
        "output_prompt": f"{WHITE}Hisobot fayli nomini kiriting [security_report.html]: {RESET}",
        "settings_title": f"{YELLOW}⚙️ SOZLAMALAR{RESET}",
        "settings_options": f"{YELLOW}[1]{RESET} Tilni o'zgartirish\n{YELLOW}[2]{RESET} API Konfiguratsiyasi\n{YELLOW}[3]{RESET} Qaytish",
        "help_text": f"""{BLUE}📖 YORDAM QO'LLANMA:{RESET}
• Variant 1: GitHub URL manzilini kiriting
• Variant 2: Lokal papka joylashuvini kiriting
• Vosita barcha kod fayllarini zaifliklar uchun tahlil qiladi
• Sun'iy intellekt tahlili {BOLD}OWASP Top 10 2025{RESET} bilan""",
        "exit_msg": f"{YELLOW}  Xayr!{RESET}",
        "error_invalid": f"{RED}  Noto'g'ri variant.{RESET}",
        "scanning": f"{RED}  Loyiha skanerlash...{RESET}",
        "cloning": f"{RED}  Repository klonlanmoqda...{RESET}",
        "analysis": f"{MAGENTA}  Sun'iy intellekt tahlili jarayonda...{RESET}",
        "report_generated": f"{GREEN}  Hisobot yaratildi: {RESET}",
        "no_api_key": f"{RED}  API kaliti topilmadi.{RESET}",
    }}
    
    # Logging messages
    LOG_MESSAGES = {
        "en": {
            "info": f"{BLUE}[INFO]{RESET}",
            "success": f"{GREEN}[SUCCESS]{RESET}",
            "warning": f"{YELLOW}[WARNING]{RESET}", 
            "error": f"{RED}[ERROR]{RESET}",
            "critical": f"{RED}{BOLD}[CRITICAL]{RESET}",
            "file_found": "Found",
            "vulnerability_found": "Vulnerability found:",
            "scan_complete": "Scan complete",
            "total_vulnerabilities": "Total vulnerabilities:",
            "critical_count": f"{RED}Critical:{RESET}",
            "high_count": f"{MAGENTA}High:{RESET}",
            "medium_count": f"{YELLOW}Medium:{RESET}",
            "low_count": f"{GREEN}Low:{RESET}",
        },
        "ru": {
            "info": f"{BLUE}[ИНФО]{RESET}",
            "success": f"{GREEN}[УСПЕХ]{RESET}",
            "warning": f"{YELLOW}[ПРЕДУПРЕЖДЕНИЕ]{RESET}",
            "error": f"{RED}[ОШИБКА]{RESET}",
            "critical": f"{RED}{BOLD}[КРИТИЧЕСКИЙ]{RESET}",
            "file_found": "Найдено",
            "vulnerability_found": "Обнаружена уязвимость:",
            "scan_complete": "Сканирование завершено",
            "total_vulnerabilities": "Всего уязвимостей:",
            "critical_count": f"{RED}Критических:{RESET}",
            "high_count": f"{MAGENTA}Высоких:{RESET}",
            "medium_count": f"{YELLOW}Средних:{RESET}",
            "low_count": f"{GREEN}Низких:{RESET}",
        },
        "uz": {
            "info": f"{BLUE}[MA'LUMOT]{RESET}",
            "success": f"{GREEN}[MUVAFFAQIYAT]{RESET}",
            "warning": f"{YELLOW}[OGOHLANTIRISH]{RESET}",
            "error": f"{RED}[XATO]{RESET}",
            "critical": f"{RED}{BOLD}[MUHIM]{RESET}",
            "file_found": "Topildi",
            "vulnerability_found": "Zaiflik topildi:",
            "scan_complete": "Skanerlash tugadi",
            "total_vulnerabilities": "Jami zaifliklar:",
            "critical_count": f"{RED}Muhim:{RESET}",
            "high_count": f"{MAGENTA}Yuqori:{RESET}",
            "medium_count": f"{YELLOW}O'rta:{RESET}",
            "low_count": f"{GREEN}Past:{RESET}",
        }
    }
    def __init__(self):
        self.current_lang = self.detect_system_language()
        
    def detect_system_language(self):
        """Sistema tilini aniqlash"""
        import locale
        try:
            sys_lang = locale.getdefaultlocale()[0]
            if sys_lang:
                if 'ru' in sys_lang.lower():
                    return 'ru'
                elif 'uz' in sys_lang.lower():
                    return 'uz'
        except:
            pass
        return 'en'
    
    def select_language(self):
        """Foydalanuvchidan tilni tanlash"""
        print(self.LANGUAGE_SELECTION['en'])
        choice = input("Select [1-3]: ").strip()
        
        if choice == '1':
            self.current_lang = 'en'
        elif choice == '2':
            self.current_lang = 'ru'
        elif choice == '3':
            self.current_lang = 'uz'
        else:
            self.current_lang = 'en'
        
        print(f"\n✅ Language selected: {self.LANGUAGES[self.current_lang]}")
        return self.current_lang
    
    def get_text(self, key: str, subkey: str = None):
        """Matnni joriy tilda olish"""
        if subkey:
            return self.MAIN_MENU[self.current_lang].get(key, {}).get(subkey, key)
        return self.MAIN_MENU[self.current_lang].get(key, key)
    
    def get_log(self, key: str):
        """Log xabarini olish"""
        return self.LOG_MESSAGES[self.current_lang].get(key, key)

# ==================== KNOWLEDGE BASE ====================
class SecurityKnowledgeBase:
    """Security vulnerabilities knowledge base - OWASP Top 10 2025 + Advanced"""
    
    # Common vulnerability patterns database
    VULN_PATTERNS = {
        "php": {
            # A05:2025 - Injection
            "rce": [
                r'eval\s*\(\s*\$_',
                r'system\s*\(\s*\$_',
                r'exec\s*\(\s*\$_',
                r'shell_exec\s*\(\s*\$_',
                r'passthru\s*\(\s*\$_',
                r'popen\s*\(\s*\$_',
                r'proc_open\s*\(\s*\$_',
                r'assert\s*\(\s*\$_',
                r'create_function\s*\([^)]*\$_',
                r'call_user_func\s*\(\s*["\']eval["\']',
            ],
            "sql_injection": [
                r'mysql_query\s*\([^)]*\$_',
                r'mysqli_query\s*\([^)]*\$_',
                r'pg_query\s*\([^)]*\$_',
                r'query\s*\([^)]*\$_',
                r'prepare\s*\([^)]*\$_',
                r'execute\s*\([^)]*\$_',
            ],
            "path_traversal": [
                r'include\s*\(\s*\$_',
                r'require\s*\(\s*\$_',
                r'file_get_contents\s*\(\s*\$_',
            ],
            "deserialization": [
                r'unserialize\s*\(\s*\$_',
            ],
            "xss": [
                r'echo\s*\$_',
                r'print\s*\$_',
                r'printf\s*\(\s*\$_',
            ],
        },
        "python": {
            "rce": [
                r'eval\s*\(\s*input',
                r'exec\s*\(\s*input',
                r'os\.system\s*\(\s*input',
                r'subprocess\.run\s*\(\s*input',
            ],
            "sql_injection": [
                r'cursor\.execute\s*\(\s*f"SELECT',
                r'cursor\.execute\s*\(\s*"SELECT.*\%s',
            ],
            "pickle": [
                r'pickle\.loads\s*\(\s*request',
            ],
        },
        "javascript": {
            "rce": [
                r'eval\s*\(\s*req\.',
                r'eval\s*\(\s*body\.',
                r'Function\s*\(\s*req\.',
            ],
            "sql_injection": [
                r'db\.query\s*\(\s*`SELECT.*\$',
                r'db\.execute\s*\(\s*`SELECT.*\$',
            ],
            "xss": [
                r'document\.write\s*\(\s*location\.',
                r'innerHTML\s*=\s*.*req\.',
            ],
        },
        "java": {
            "rce": [
                r'Runtime\.getRuntime\(\)\.exec\s*\(\s*request\.',
            ],
            "sql_injection": [
                r'Statement\.executeQuery\s*\(\s*".*"\+.*request',
            ],
            "deserialization": [
                r'ObjectInputStream.*readObject\s*\(\s*\)',
            ],
        },
    }
    
    @classmethod
    def get_patterns_for_language(cls, language: str) -> Dict[str, List[str]]:
        """Get vulnerability patterns for specific language"""
        return cls.VULN_PATTERNS.get(language.lower(), {})

# ==================== AI CLIENT WITH MULTILINGUAL SUPPORT ====================
class AIClient:
    """AI client with multilingual support"""
    
    def __init__(self, api_key: str = None, language: str = 'en'):
        self.api_key = api_key or self.load_api_key()
        self.language = language
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        self.knowledge_base = SecurityKnowledgeBase()
        
    def load_api_key(self):
        """API key ni yuklash"""
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            return api_key
        
        try:
            with open(".env", "r") as f:
                for line in f:
                    if line.startswith("GROQ_API_KEY="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
        except:
            pass
        
        return None
    
    def get_language_prompt(self, language: str) -> str:
        """Tilga qarab prompt"""
        prompts = {
            "en": """You are an elite security researcher and penetration tester. 
            Analyze this code for REAL exploitable vulnerabilities.
            Focus on OWASP Top 10 2025 vulnerabilities.
            Provide detailed findings with exploit POC and fixes.""",
            
            "ru": """Вы опытный исследователь безопасности и пентестер.
            Проанализируйте этот код на наличие реальных эксплуатируемых уязвимостей.
            Сосредоточьтесь на OWASP Top 10 2025.
            Предоставьте подробные результаты с эксплойтами POC и исправлениями.""",
            
            "uz": """Siz tajribali xavfsizlik tadqiqotchisi va penetration tester.
            Ushbu kodni haqiqiy ekspluatatsiya qilinadigan zaifliklar uchun tahlil qiling.
            OWASP Top 10 2025 zaifliklariga e'tibor bering.
            Batafsil topilmalarni POC exploit va tuzatishlar bilan taqdim eting."""
        }
        return prompts.get(language, prompts['en'])
    
    def analyze_code(self, code: str, file_info: Dict, language: str = None) -> Dict:
        """Kodni tahlil qilish"""
        if not self.client:
            return self.offline_analysis(code, file_info)
        
        analysis_lang = language or self.language
        
        prompt = f"""
        {self.get_language_prompt(analysis_lang)}
        
        File: {file_info['path']}
        Size: {len(code)} characters
        Type: {file_info['type']}
        
        Code to analyze:
        ```
        {code[:50000]}
        ```
        
        Provide response in JSON format:
        {{
            "vulnerabilities_found": true/false,
            "vulnerabilities": [
                {{
                    "severity": "CRITICAL/HIGH/MEDIUM/LOW",
                    "type": "RCE/SQLi/LFI/XSS/XXE/IDOR/SSRF",
                    "description": "Vulnerability description in {analysis_lang}",
                    "file": "filename:line_number",
                    "code_snippet": "vulnerable code",
                    "explanation": "Why vulnerable in {analysis_lang}",
                    "impact": "Impact in {analysis_lang}",
                    "recommendation": "Fix in {analysis_lang}",
                    "exploit_poc": "Working exploit code",
                    "cvss_score": "X.X/10",
                    "confidence": "HIGH/MEDIUM/LOW"
                }}
            ],
            "summary": {{
                "total_vulnerabilities": X,
                "critical": X,
                "high": X,
                "medium": X,
                "low": X
            }},
            "technology_detected": ["PHP", "Python", etc],
            "security_score": 0-100,
            "verdict": "INSECURE/SECURE"
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a security expert."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.1,
                max_tokens=4000,
                timeout=300
            )
            
            result_text = response.choices[0].message.content
            
            try:
                json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group(0))
                else:
                    result = self.offline_analysis(code, file_info)
            except:
                result = self.offline_analysis(code, file_info)
            
            return result
            
        except Exception as e:
            return self.offline_analysis(code, file_info)
    
    def offline_analysis(self, code: str, file_info: Dict) -> Dict:
        """Offline tahlil"""
        file_lang = self.detect_language(file_info['path'])
        patterns = self.knowledge_base.get_patterns_for_language(file_lang)
        
        vulnerabilities = []
        for vuln_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                matches = re.finditer(pattern, code, re.IGNORECASE)
                for match in matches:
                    line_num = code[:match.start()].count('\n') + 1
                    vulnerabilities.append({
                        "severity": "MEDIUM",
                        "type": vuln_type.upper(),
                        "description": f"Pattern match: {pattern}",
                        "file": f"{file_info['path']}:{line_num}",
                        "code_snippet": match.group(0)[:200],
                        "explanation": "Matches known vulnerability pattern",
                        "impact": "Potential security issue",
                        "recommendation": "Review and secure this code",
                        "exploit_poc": "# Manual testing required",
                        "cvss_score": "5.0/10",
                        "confidence": "MEDIUM"
                    })
        
        return {
            "vulnerabilities_found": len(vulnerabilities) > 0,
            "vulnerabilities": vulnerabilities,
            "summary": {
                "total_vulnerabilities": len(vulnerabilities),
                "critical": 0,
                "high": 0,
                "medium": len(vulnerabilities),
                "low": 0
            },
            "technology_detected": [file_lang],
            "security_score": 100 - (len(vulnerabilities) * 10),
            "verdict": "INSECURE" if vulnerabilities else "SECURE"
        }
    
    def detect_language(self, filepath: str) -> str:
        """Fayl tilini aniqlash"""
        ext = os.path.splitext(filepath)[1].lower()
        language_map = {
            '.php': 'php',
            '.py': 'python',
            '.js': 'javascript',
            '.java': 'java',
            '.cs': 'csharp',
            '.go': 'go',
            '.rb': 'ruby',
            '.rs': 'rust',
        }
        return language_map.get(ext, 'unknown')

# ==================== MAIN APPLICATION ====================
class SecurityAuditApp:
    """Asosiy ilova"""
    
    def __init__(self):
        self.multilingual = Multilingual()
        self.ai_client = None
        self.current_language = 'en'
        self.settings = self.load_settings()
        
    def load_settings(self):
        """Sozlamalarni yuklash"""
        settings_file = "audit_settings.json"
        default_settings = {
            "language": "en",
            "output_dir": "reports",
            "api_key": "",
            "max_file_size": 100000,
            "scan_depth": 10
        }
        
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return default_settings
    
    def save_settings(self):
        """Sozlamalarni saqlash"""
        settings_file = "audit_settings.json"
        with open(settings_file, 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def clear_screen(self):
        """Ekranni tozalash"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        """Banner chop etish"""
        self.clear_screen()
        print(self.multilingual.get_text('title'))
        print()
    
    def main_menu(self):
        """Asosiy menyu"""
        while True:
            self.print_banner()
            print(self.multilingual.get_text('options'))
            print()
            
            choice = input(f"[1-5]: ").strip()
            
            if choice == '1':
                self.audit_github()
            elif choice == '2':
                self.audit_local()
            elif choice == '3':
                self.settings_menu()
            elif choice == '4':
                self.help_menu()
            elif choice == '5':
                print(self.multilingual.get_text('exit_msg'))
                sys.exit(0)
            else:
                print(self.multilingual.get_text('error_invalid'))
                time.sleep(2)
    
    def audit_github(self):
        """GitHub repositoriyasini audit qilish"""
        self.print_banner()
        print("📡 GITHUB REPOSITORY AUDIT")
        print("="*50)
        
        repo_url = input(self.multilingual.get_text('github_prompt')).strip()
        if not repo_url:
            return
        
        output_file = input(self.multilingual.get_text('output_prompt')).strip()
        if not output_file:
            output_file = "security_report.html"
        
        print(f"\n{self.multilingual.get_text('cloning')}")
        
        # Repo ni klon qilish
        temp_dir = self.clone_repository(repo_url)
        if not temp_dir:
            return
        
        try:
            # Audit qilish
            results = self.scan_project(temp_dir, output_file)
            
            # Hisobot yaratish
            self.generate_report(results, temp_dir, output_file)
            
            print(f"\n{self.multilingual.get_text('report_generated')}{output_file}")
            
        finally:
            # Tozalash
            shutil.rmtree(temp_dir, ignore_errors=True)
        
        input("\nPress Enter to continue...")
    
    def audit_local(self):
        """Lokal loyihani audit qilish"""
        self.print_banner()
        print("LOCAL PROJECT AUDIT")
        print("="*50)
        
        project_path = input(self.multilingual.get_text('local_prompt')).strip()
        if not project_path or not os.path.exists(project_path):
            print("Path does not exist!")
            time.sleep(2)
            return
        
        output_file = input(self.multilingual.get_text('output_prompt')).strip()
        if not output_file:
            output_file = "security_report.html"
        
        print(f"\n{self.multilingual.get_text('scanning')}")
        
        # Audit qilish
        results = self.scan_project(project_path, output_file)
        
        # Hisobot yaratish
        self.generate_report(results, project_path, output_file)
        
        print(f"\n{self.multilingual.get_text('report_generated')}{output_file}")
        input("\nPress Enter to continue...")
    
    def clone_repository(self, repo_url: str) -> str:
        """Repositoriyani klon qilish"""
        import tempfile
        
        # Temp papka yaratish
        temp_dir = tempfile.mkdtemp(prefix="audit_")
        
        try:
            print(f"Cloning to: {temp_dir}")
            
            # Git clone komandasi
            result = subprocess.run(
                ['git', 'clone', '--depth', '1', '--quiet', repo_url, temp_dir],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f" Clone failed: {result.stderr}")
                return None
            
            print("✅ Repository cloned successfully")
            return temp_dir
            
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def scan_project(self, project_path: str, output_file: str) -> List[Dict]:
        """Loyihani skaner qilish"""
        results = []
        
        # AI client yaratish
        self.ai_client = AIClient(language=self.current_language)
        if not self.ai_client.api_key:
            print(self.multilingual.get_text('no_api_key'))
            return results
        
        print(f"{self.multilingual.get_text('analysis')}")
        
        # Barcha fayllarni yig'ish
        code_files = []
        for root, dirs, files in os.walk(project_path):
            for file in files:
                filepath = os.path.join(root, file)
                
                # Faqat kod fayllari
                ext = os.path.splitext(file)[1].lower()
                if ext in ['.php', '.py', '.js', '.java', '.cs', '.go', '.rb']:
                    code_files.append(filepath)
        
        print(f"Found {len(code_files)} code files")
        
        # Har bir faylni tahlil qilish
        for i, filepath in enumerate(code_files, 1):
            print(f"  [{i}/{len(code_files)}] Analyzing: {os.path.basename(filepath)}")
            
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read(100000)
            except:
                continue
            
            analysis = self.ai_client.analyze_code(
                content,
                {"path": filepath, "type": os.path.splitext(filepath)[1]},
                self.current_language
            )
            
            if analysis.get('vulnerabilities_found'):
                results.append({
                    "file": filepath,
                    "analysis": analysis
                })
        
        return results
    
    def generate_report(self, results: List[Dict], project_path: str, output_file: str):
        """Hisobot yaratish"""
        lang_text = self.multilingual.MAIN_MENU[self.current_language]
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="{self.current_language}">
        <head>
            <meta charset="UTF-8">
            <title>Security Audit Report - {project_path}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 10px; }}
                .vulnerability {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .critical {{ border-left: 5px solid #e74c3c; background: #ffeaea; }}
                .high {{ border-left: 5px solid #e67e22; background: #fff3e0; }}
                .medium {{ border-left: 5px solid #f1c40f; background: #fffde7; }}
                .low {{ border-left: 5px solid #2ecc71; background: #e8f5e9; }}
                pre {{ background: #f5f5f5; padding: 10px; border-radius: 5px; overflow-x: auto; }}
                .summary {{ background: #e3f2fd; padding: 20px; border-radius: 10px; margin: 20px 0; }}
                .language-badge {{ background: #3498db; color: white; padding: 5px 10px; border-radius: 15px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1> Security Audit Report</h1>
                <h2>Project: {project_path}</h2>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <span class="language-badge">Language: {self.multilingual.LANGUAGES[self.current_language]}</span>
            </div>
            
            <div class="summary">
                <h3> Summary</h3>
                <p>Total Files Scanned: {len(results)}</p>
                <p>Vulnerabilities Found: {sum(1 for r in results if r['analysis']['vulnerabilities_found'])}</p>
            </div>
        """
        
        for result in results:
            if result['analysis']['vulnerabilities_found']:
                for vuln in result['analysis']['vulnerabilities']:
                    severity_class = vuln['severity'].lower()
                    
                    html_content += f"""
                    <div class="vulnerability {severity_class}">
                        <h3><span style="color: {'#e74c3c' if severity_class == 'critical' else '#e67e22' if severity_class == 'high' else '#f1c40f' if severity_class == 'medium' else '#2ecc71'}">
                            {vuln['severity']}: {vuln['type']}
                        </span></h3>
                        <p><strong>File:</strong> {vuln['file']}</p>
                        <p><strong>Description:</strong> {html.escape(vuln['description'])}</p>
                        
                        <h4>Vulnerable Code:</h4>
                        <pre>{html.escape(vuln['code_snippet'])}</pre>
                        
                        <h4>Exploit POC:</h4>
                        <pre>{html.escape(vuln.get('exploit_poc', 'N/A'))}</pre>
                        
                        <h4>Recommendation:</h4>
                        <p>{html.escape(vuln['recommendation'])}</p>
                        
                        <p><strong>CVSS Score:</strong> {vuln.get('cvss_score', 'N/A')}</p>
                        <p><strong>Confidence:</strong> {vuln.get('confidence', 'MEDIUM')}</p>
                    </div>
                    """
        
        html_content += """
        </body>
        </html>
        """
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def settings_menu(self):
        """Sozlamalar menyusi"""
        while True:
            self.print_banner()
            print(self.multilingual.get_text('settings_title'))
            print("="*50)
            print(self.multilingual.get_text('settings_options'))
            print()
            
            choice = input("[1-3]: ").strip()
            
            if choice == '1':
                self.change_language()
            elif choice == '2':
                self.api_settings()
            elif choice == '3':
                return
            else:
                print(self.multilingual.get_text('error_invalid'))
    
    def change_language(self):
        """Tilni o'zgartirish"""
        self.multilingual.select_language()
        self.current_language = self.multilingual.current_lang
        self.settings['language'] = self.current_language
        self.save_settings()
        print(f"\n✅ Language changed to {self.multilingual.LANGUAGES[self.current_language]}")
        time.sleep(2)
    
    def api_settings(self):
        """API sozlamalari"""
        self.print_banner()
        print("⚙️ API CONFIGURATION")
        print("="*50)
        
        current_key = self.settings.get('api_key', '')
        if current_key:
            print(f"Current API Key: {current_key[:10]}...")
        else:
            print("No API key configured")
        
        print("\n[1] Enter new API key")
        print("[2] Load from .env file")
        print("[3] Back")
        
        choice = input("\n[1-3]: ").strip()
        
        if choice == '1':
            new_key = getpass.getpass("Enter new API key: ").strip()
            if new_key:
                self.settings['api_key'] = new_key
                # .env fayliga saqlash
                with open(".env", "w") as f:
                    f.write(f'GROQ_API_KEY="{new_key}"\n')
                self.save_settings()
                print("✅ API key saved!")
            else:
                print("❌ No key entered")
        
        elif choice == '2':
            if os.path.exists(".env"):
                with open(".env", "r") as f:
                    for line in f:
                        if line.startswith("GROQ_API_KEY="):
                            key = line.split("=", 1)[1].strip().strip('"').strip("'")
                            self.settings['api_key'] = key
                            self.save_settings()
                            print("✅ API key loaded from .env")
                            break
            else:
                print("❌ .env file not found")
        
        time.sleep(2)
    
    def help_menu(self):
        """Yordam menyusi"""
        self.print_banner()
        print("ℹ️ HELP")
        print("="*50)
        print(self.multilingual.get_text('help_text'))
        print("\n" + "="*50)
        input("\nPress Enter to continue...")
    
    def run(self):
        """Ilovani ishga tushirish"""
        # Dastlab tilni tanlash
        self.multilingual.select_language()
        self.current_language = self.multilingual.current_lang
        
        # Sozlamalarni yuklash
        if 'language' in self.settings:
            self.current_language = self.settings['language']
            self.multilingual.current_lang = self.current_language
        
        # Asosiy menyuni ko'rsatish
        self.main_menu()

# ==================== PROGRAM ENTRY POINT ====================
def main():
    """Dastur kirish nuqtasi"""
    app = SecurityAuditApp()
    app.run()

if __name__ == "__main__":
    main()