#!/usr/bin/env python3
"""
Google Dorker - Advanced Reconnaissance Tool
============================================

A sophisticated tool for generating Google Dork queries for security research
and penetration testing. This tool prioritizes functionality while maintaining
ethical guidelines.

Author: Security Researcher
Version: 1.0
License: Educational/Research Use Only

WARNING: This tool is for authorized security testing only.
Use responsibly and in accordance with applicable laws and regulations.
"""

import random
import string
import json
import time
import argparse
import sys
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum
import urllib.parse

class DorkCategory(Enum):
    """Categories of Google Dorks"""
    FILE_DISCOVERY = "file_discovery"
    DIRECTORY_LISTING = "directory_listing"
    VULNERABILITY_SCANNING = "vulnerability_scanning"
    INFORMATION_DISCLOSURE = "information_disclosure"
    TECHNOLOGY_DETECTION = "technology_detection"
    ADMIN_PANELS = "admin_panels"
    SENSITIVE_FILES = "sensitive_files"
    DATABASE_DUMPS = "database_dumps"
    BACKUP_FILES = "backup_files"
    LOG_FILES = "log_files"
    IOT_DEVICES = "iot_devices"
    SHOPPING_INFO = "shopping_info"
    PASSWORD_INFO = "password_info"

@dataclass
class DorkQuery:
    """Represents a Google Dork query with metadata"""
    query: str
    category: DorkCategory
    description: str
    risk_level: str
    use_case: str
    example_target: str = ""

class GoogleDorker:
    """Main Google Dorker class with advanced query generation algorithms"""
    
    def __init__(self):
        self.dork_templates = self._initialize_dork_templates()
        self.ethical_warnings = self._get_ethical_warnings()
        
    def _initialize_dork_templates(self) -> Dict[DorkCategory, List[Dict]]:
        """Initialize comprehensive dork templates"""
        return {
            DorkCategory.FILE_DISCOVERY: [
                {
                    "template": "filetype:{ext} {target}",
                    "extensions": ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt", "csv"],
                    "description": "Find specific file types on target domain",
                    "risk": "Medium"
                },
                {
                    "template": "site:{target} filetype:{ext}",
                    "extensions": ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx"],
                    "description": "Discover documents on target website",
                    "risk": "Medium"
                }
            ],
            
            DorkCategory.DIRECTORY_LISTING: [
                {
                    "template": "site:{target} intitle:index.of",
                    "description": "Find directory listings on target",
                    "risk": "High"
                },
                {
                    "template": "site:{target} \"index of\"",
                    "description": "Alternative directory listing search",
                    "risk": "High"
                },
                {
                    "template": "site:{target} inurl:admin intitle:index.of",
                    "description": "Find admin directory listings",
                    "risk": "Critical"
                }
            ],
            
            DorkCategory.VULNERABILITY_SCANNING: [
                {
                    "template": "site:{target} inurl:phpmyadmin",
                    "description": "Find phpMyAdmin installations",
                    "risk": "Critical"
                },
                {
                    "template": "site:{target} inurl:wp-admin",
                    "description": "Find WordPress admin panels",
                    "risk": "High"
                },
                {
                    "template": "site:{target} \"SQL syntax near\"",
                    "description": "Find SQL error messages",
                    "risk": "Critical"
                },
                {
                    "template": "site:{target} \"mysql_fetch_array()\"",
                    "description": "Find MySQL error messages",
                    "risk": "High"
                }
            ],
            
            DorkCategory.INFORMATION_DISCLOSURE: [
                {
                    "template": "site:{target} \"password\" filetype:txt",
                    "description": "Find password files",
                    "risk": "Critical"
                },
                {
                    "template": "site:{target} \"username\" filetype:txt",
                    "description": "Find username files",
                    "risk": "High"
                },
                {
                    "template": "site:{target} \"config\" filetype:txt",
                    "description": "Find configuration files",
                    "risk": "High"
                },
                {
                    "template": "site:{target} \"database\" filetype:sql",
                    "description": "Find database files",
                    "risk": "Critical"
                }
            ],
            
            DorkCategory.TECHNOLOGY_DETECTION: [
                {
                    "template": "site:{target} \"powered by\"",
                    "description": "Identify web technologies",
                    "risk": "Low"
                },
                {
                    "template": "site:{target} \"server: apache\"",
                    "description": "Identify Apache servers",
                    "risk": "Low"
                },
                {
                    "template": "site:{target} \"x-powered-by\"",
                    "description": "Find server headers",
                    "risk": "Low"
                }
            ],
            
            DorkCategory.ADMIN_PANELS: [
                {
                    "template": "site:{target} inurl:admin",
                    "description": "Find admin panels",
                    "risk": "High"
                },
                {
                    "template": "site:{target} inurl:login",
                    "description": "Find login pages",
                    "risk": "Medium"
                },
                {
                    "template": "site:{target} inurl:panel",
                    "description": "Find control panels",
                    "risk": "High"
                },
                {
                    "template": "site:{target} inurl:manage",
                    "description": "Find management interfaces",
                    "risk": "High"
                }
            ],
            
            DorkCategory.SENSITIVE_FILES: [
                {
                    "template": "site:{target} filetype:bak",
                    "description": "Find backup files",
                    "risk": "High"
                },
                {
                    "template": "site:{target} filetype:old",
                    "description": "Find old files",
                    "risk": "Medium"
                },
                {
                    "template": "site:{target} filetype:tmp",
                    "description": "Find temporary files",
                    "risk": "Medium"
                },
                {
                    "template": "site:{target} \"robots.txt\"",
                    "description": "Find robots.txt files",
                    "risk": "Low"
                }
            ],
            
            DorkCategory.DATABASE_DUMPS: [
                {
                    "template": "site:{target} filetype:sql",
                    "description": "Find SQL database dumps",
                    "risk": "Critical"
                },
                {
                    "template": "site:{target} \"dump\" filetype:sql",
                    "description": "Find database dumps",
                    "risk": "Critical"
                },
                {
                    "template": "site:{target} \"backup\" filetype:sql",
                    "description": "Find SQL backups",
                    "risk": "Critical"
                }
            ],
            
            DorkCategory.BACKUP_FILES: [
                {
                    "template": "site:{target} filetype:zip",
                    "description": "Find ZIP archives",
                    "risk": "High"
                },
                {
                    "template": "site:{target} filetype:rar",
                    "description": "Find RAR archives",
                    "risk": "High"
                },
                {
                    "template": "site:{target} filetype:tar.gz",
                    "description": "Find compressed archives",
                    "risk": "High"
                }
            ],
            
            DorkCategory.LOG_FILES: [
                {
                    "template": "site:{target} filetype:log",
                    "description": "Find log files",
                    "risk": "High"
                },
                {
                    "template": "site:{target} \"access.log\"",
                    "description": "Find access logs",
                    "risk": "High"
                },
                {
                    "template": "site:{target} \"error.log\"",
                    "description": "Find error logs",
                    "risk": "High"
                }
            ],
            
            DorkCategory.IOT_DEVICES: [
                {
                    "template": "site:{target} inurl:8080",
                    "description": "Find devices on port 8080",
                    "risk": "High"
                },
                {
                    "template": "site:{target} inurl:8081",
                    "description": "Find devices on port 8081",
                    "risk": "High"
                },
                {
                    "template": "site:{target} \"camera\" OR \"webcam\"",
                    "description": "Find camera devices",
                    "risk": "Critical"
                },
                {
                    "template": "site:{target} \"router\" OR \"gateway\"",
                    "description": "Find router/gateway devices",
                    "risk": "Critical"
                },
                {
                    "template": "site:{target} \"printer\" OR \"scanner\"",
                    "description": "Find printer/scanner devices",
                    "risk": "High"
                },
                {
                    "template": "site:{target} \"nas\" OR \"storage\"",
                    "description": "Find NAS/storage devices",
                    "risk": "Critical"
                },
                {
                    "template": "site:{target} \"iot\" OR \"smart device\"",
                    "description": "Find IoT/smart devices",
                    "risk": "High"
                },
                {
                    "template": "site:{target} \"sensor\" OR \"monitor\"",
                    "description": "Find sensor/monitoring devices",
                    "risk": "High"
                },
                {
                    "template": "site:{target} \"thermostat\" OR \"climate\"",
                    "description": "Find climate control devices",
                    "risk": "Medium"
                },
                {
                    "template": "site:{target} \"security\" OR \"alarm\"",
                    "description": "Find security/alarm systems",
                    "risk": "Critical"
                }
            ],
            
            DorkCategory.SHOPPING_INFO: [
                {
                    "template": "site:{target} \"price\" OR \"cost\"",
                    "description": "Find pricing information",
                    "risk": "Low"
                },
                {
                    "template": "site:{target} \"inventory\" OR \"stock\"",
                    "description": "Find inventory information",
                    "risk": "Medium"
                },
                {
                    "template": "site:{target} \"discount\" OR \"sale\"",
                    "description": "Find discount/sale information",
                    "risk": "Low"
                },
                {
                    "template": "site:{target} \"cart\" OR \"checkout\"",
                    "description": "Find shopping cart/checkout pages",
                    "risk": "Medium"
                },
                {
                    "template": "site:{target} \"product\" filetype:csv",
                    "description": "Find product CSV files",
                    "risk": "High"
                },
                {
                    "template": "site:{target} \"customer\" OR \"buyer\"",
                    "description": "Find customer information",
                    "risk": "High"
                },
                {
                    "template": "site:{target} \"order\" OR \"purchase\"",
                    "description": "Find order/purchase information",
                    "risk": "High"
                },
                {
                    "template": "site:{target} \"payment\" OR \"billing\"",
                    "description": "Find payment/billing information",
                    "risk": "Critical"
                },
                {
                    "template": "site:{target} \"shipping\" OR \"delivery\"",
                    "description": "Find shipping/delivery information",
                    "risk": "Medium"
                },
                {
                    "template": "site:{target} \"review\" OR \"rating\"",
                    "description": "Find review/rating information",
                    "risk": "Low"
                }
            ],
            
            DorkCategory.PASSWORD_INFO: [
                {
                    "template": "site:{target} \"password\" filetype:txt",
                    "description": "Find password text files",
                    "risk": "Critical"
                },
                {
                    "template": "site:{target} \"password\" filetype:doc",
                    "description": "Find password documents",
                    "risk": "Critical"
                },
                {
                    "template": "site:{target} \"password\" filetype:pdf",
                    "description": "Find password PDF files",
                    "risk": "Critical"
                },
                {
                    "template": "site:{target} \"passwd\" OR \"shadow\"",
                    "description": "Find system password files",
                    "risk": "Critical"
                },
                {
                    "template": "site:{target} \"credentials\" OR \"auth\"",
                    "description": "Find credential/authentication files",
                    "risk": "Critical"
                },
                {
                    "template": "site:{target} \"secret\" OR \"key\"",
                    "description": "Find secret/key files",
                    "risk": "Critical"
                },
                {
                    "template": "site:{target} \"token\" OR \"api_key\"",
                    "description": "Find token/API key files",
                    "risk": "Critical"
                },
                {
                    "template": "site:{target} \"login\" filetype:txt",
                    "description": "Find login information files",
                    "risk": "Critical"
                },
                {
                    "template": "site:{target} \"user\" filetype:txt",
                    "description": "Find user information files",
                    "risk": "High"
                },
                {
                    "template": "site:{target} \"config\" filetype:txt",
                    "description": "Find configuration files with passwords",
                    "risk": "Critical"
                },
                {
                    "template": "site:{target} \"database\" filetype:txt",
                    "description": "Find database configuration files",
                    "risk": "Critical"
                },
                {
                    "template": "site:{target} \".env\" OR \"environment\"",
                    "description": "Find environment variable files",
                    "risk": "Critical"
                }
            ]
        }
    
    def _get_ethical_warnings(self) -> List[str]:
        """Get ethical usage warnings"""
        return [
            "WARNING: This tool is for authorized security testing only!",
            "WARNING: Only use on systems you own or have explicit permission to test.",
            "WARNING: Unauthorized access to computer systems is illegal in most jurisdictions.",
            "WARNING: Use responsibly and in accordance with applicable laws and regulations.",
            "WARNING: The authors are not responsible for misuse of this tool.",
            "WARNING: Always obtain proper authorization before conducting security assessments."
        ]
    
    def generate_dork_queries(self, target: str, category: DorkCategory = None, 
                            count: int = 10) -> List[DorkQuery]:
        """Generate Google Dork queries for a target"""
        queries = []
        
        if category:
            categories = [category]
        else:
            categories = list(DorkCategory)
        
        for cat in categories:
            if cat in self.dork_templates:
                for template_data in self.dork_templates[cat]:
                    if "extensions" in template_data:
                        # Handle templates with multiple extensions
                        for ext in template_data["extensions"][:2]:  # Limit to 2 per template
                            query_str = template_data["template"].format(
                                target=target, ext=ext
                            )
                            queries.append(DorkQuery(
                                query=query_str,
                                category=cat,
                                description=f"{template_data['description']} ({ext} files)",
                                risk_level=template_data["risk"],
                                use_case=f"Find {ext} files on {target}",
                                example_target=target
                            ))
                    else:
                        # Handle simple templates
                        query_str = template_data["template"].format(target=target)
                        queries.append(DorkQuery(
                            query=query_str,
                            category=cat,
                            description=template_data["description"],
                            risk_level=template_data["risk"],
                            use_case=f"Security assessment of {target}",
                            example_target=target
                        ))
        
        # Shuffle and limit results
        random.shuffle(queries)
        return queries[:count]
    
    def generate_advanced_queries(self, target: str, keywords: List[str] = None) -> List[DorkQuery]:
        """Generate advanced dork queries with custom keywords"""
        if not keywords:
            keywords = ["admin", "login", "config", "password", "database", "backup"]
        
        advanced_queries = []
        
        # Combine target with keywords
        for keyword in keywords:
            # Basic keyword search
            query = f"site:{target} {keyword}"
            advanced_queries.append(DorkQuery(
                query=query,
                category=DorkCategory.INFORMATION_DISCLOSURE,
                description=f"Search for '{keyword}' on target domain",
                risk_level="Medium",
                use_case=f"Keyword-based reconnaissance for {keyword}",
                example_target=target
            ))
            
            # File type combinations
            for ext in ["txt", "pdf", "doc", "sql"]:
                query = f"site:{target} {keyword} filetype:{ext}"
                advanced_queries.append(DorkQuery(
                    query=query,
                    category=DorkCategory.FILE_DISCOVERY,
                    description=f"Find {keyword} in {ext} files",
                    risk_level="High",
                    use_case=f"File-based keyword search for {keyword}",
                    example_target=target
                ))
        
        return advanced_queries[:15]  # Limit results
    
    def generate_osint_queries(self, target: str) -> List[DorkQuery]:
        """Generate OSINT-focused dork queries"""
        osint_queries = [
            DorkQuery(
                query=f'"{target}" filetype:pdf',
                category=DorkCategory.FILE_DISCOVERY,
                description="Find PDF documents mentioning the target",
                risk_level="Low",
                use_case="OSINT document discovery",
                example_target=target
            ),
            DorkQuery(
                query=f'"{target}" "contact" OR "email"',
                category=DorkCategory.INFORMATION_DISCLOSURE,
                description="Find contact information for the target",
                risk_level="Low",
                use_case="Contact information gathering",
                example_target=target
            ),
            DorkQuery(
                query=f'"{target}" "employee" OR "staff"',
                category=DorkCategory.INFORMATION_DISCLOSURE,
                description="Find employee information",
                risk_level="Medium",
                use_case="Personnel information gathering",
                example_target=target
            ),
            DorkQuery(
                query=f'"{target}" "security" OR "vulnerability"',
                category=DorkCategory.VULNERABILITY_SCANNING,
                description="Find security-related information",
                risk_level="Medium",
                use_case="Security information gathering",
                example_target=target
            )
        ]
        
        return osint_queries
    
    def display_queries(self, queries: List[DorkQuery], show_warnings: bool = True):
        """Display generated queries in a formatted way"""
        if show_warnings:
            print("\n".join(self.ethical_warnings))
            print("\n" + "="*80 + "\n")
        
        for i, dork in enumerate(queries, 1):
            print(f"[{i}] {dork.category.value.upper()}")
            print(f"Query: {dork.query}")
            print(f"Description: {dork.description}")
            print(f"Risk Level: {dork.risk_level}")
            print(f"Use Case: {dork.use_case}")
            print(f"Google URL: https://www.google.com/search?q={urllib.parse.quote(dork.query)}")
            print("-" * 80)
    
    def save_queries(self, queries: List[DorkQuery], filename: str):
        """Save queries to a JSON file"""
        data = []
        for dork in queries:
            data.append({
                "query": dork.query,
                "category": dork.category.value,
                "description": dork.description,
                "risk_level": dork.risk_level,
                "use_case": dork.use_case,
                "example_target": dork.example_target
            })
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Queries saved to {filename}")
    
    def interactive_mode(self):
        """Run interactive mode for query generation"""
        print("Google Dorker - Interactive Mode")
        print("=" * 50)
        
        while True:
            print("\nOptions:")
            print("1. Generate basic dork queries")
            print("2. Generate advanced queries with keywords")
            print("3. Generate OSINT queries")
            print("4. Generate queries by category")
            print("5. Show all categories")
            print("6. Exit")
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == "6":
                print("Goodbye! Stay ethical!")
                break
            
            target = input("Enter target domain (e.g., example.com): ").strip()
            if not target:
                print("Please enter a valid target domain.")
                continue
            
            if choice == "1":
                count = int(input("Number of queries to generate (default 10): ") or "10")
                queries = self.generate_dork_queries(target, count=count)
                self.display_queries(queries)
                
            elif choice == "2":
                keywords_input = input("Enter keywords (comma-separated): ").strip()
                keywords = [k.strip() for k in keywords_input.split(",")] if keywords_input else None
                queries = self.generate_advanced_queries(target, keywords)
                self.display_queries(queries)
                
            elif choice == "3":
                queries = self.generate_osint_queries(target)
                self.display_queries(queries)
                
            elif choice == "4":
                print("\nAvailable categories:")
                for i, category in enumerate(DorkCategory, 1):
                    print(f"{i}. {category.value}")
                
                try:
                    cat_choice = int(input("Select category number: ")) - 1
                    if 0 <= cat_choice < len(DorkCategory):
                        selected_category = list(DorkCategory)[cat_choice]
                        queries = self.generate_dork_queries(target, selected_category)
                        self.display_queries(queries)
                    else:
                        print("Invalid category selection.")
                except ValueError:
                    print("Please enter a valid number.")
                    
            elif choice == "5":
                print("\nDork Categories:")
                for category in DorkCategory:
                    print(f"- {category.value}: {category.value.replace('_', ' ').title()}")
            
            # Ask if user wants to save queries
            save = input("\nSave queries to file? (y/n): ").strip().lower()
            if save == 'y':
                filename = input("Enter filename (default: dork_queries.json): ").strip()
                if not filename:
                    filename = "dork_queries.json"
                self.save_queries(queries, filename)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Google Dorker - Advanced Reconnaissance Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python google_dorker.py -t example.com
  python google_dorker.py -t example.com -c file_discovery
  python google_dorker.py -t example.com -k admin,login,config
  python google_dorker.py --interactive
        """
    )
    
    parser.add_argument("-t", "--target", help="Target domain to generate dorks for")
    parser.add_argument("-c", "--category", help="Specific dork category")
    parser.add_argument("-k", "--keywords", help="Comma-separated keywords for advanced queries")
    parser.add_argument("-n", "--count", type=int, default=10, help="Number of queries to generate")
    parser.add_argument("-o", "--output", help="Output file to save queries")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--no-warnings", action="store_true", help="Hide ethical warnings")
    
    args = parser.parse_args()
    
    dorker = GoogleDorker()
    
    if args.interactive:
        dorker.interactive_mode()
        return
    
    if not args.target:
        print("Error: Target domain is required. Use --interactive for interactive mode.")
        parser.print_help()
        return
    
    queries = []
    
    if args.keywords:
        keywords = [k.strip() for k in args.keywords.split(",")]
        queries = dorker.generate_advanced_queries(args.target, keywords)
    elif args.category:
        try:
            category = DorkCategory(args.category)
            queries = dorker.generate_dork_queries(args.target, category, args.count)
        except ValueError:
            print(f"Error: Invalid category '{args.category}'")
            print("Available categories:", [c.value for c in DorkCategory])
            return
    else:
        queries = dorker.generate_dork_queries(args.target, count=args.count)
    
    dorker.display_queries(queries, not args.no_warnings)
    
    if args.output:
        dorker.save_queries(queries, args.output)

if __name__ == "__main__":
    main()
