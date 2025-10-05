# Google Dorker 🔍

A sophisticated reconnaissance tool for generating Google Dork queries for authorized security research and penetration testing.

## ⚠️ ETHICAL WARNING

**This tool is for authorized security testing only!**

- Only use on systems you own or have explicit permission to test
- Unauthorized access to computer systems is illegal in most jurisdictions
- Use responsibly and in accordance with applicable laws and regulations
- The authors are not responsible for misuse of this tool
- Always obtain proper authorization before conducting security assessments

## Features

### 🎯 Core Functionality
- **Advanced Query Generation**: Complex algorithms for creating targeted Google Dork queries
- **Categorized Dorks**: 10 different categories of reconnaissance queries
- **Risk Assessment**: Each query includes risk level and use case information
- **GUI Interface**: Hacker terminal with Matrix-style falling code animation
- **Interactive Mode**: User-friendly command-line interface
- **Batch Processing**: Generate multiple queries for comprehensive assessment

### 📊 Dork Categories

1. **File Discovery** - Find specific file types (PDF, DOC, XLS, etc.)
2. **Directory Listing** - Discover open directory listings
3. **Vulnerability Scanning** - Find common vulnerabilities and error messages
4. **Information Disclosure** - Locate sensitive information and credentials
5. **Technology Detection** - Identify web technologies and server information
6. **Admin Panels** - Find administrative interfaces and login pages
7. **Sensitive Files** - Discover backup files and temporary data
8. **Database Dumps** - Locate SQL dumps and database files
9. **Backup Files** - Find compressed archives and backups
10. **Log Files** - Discover access logs and error logs
11. **IoT Devices** - Find cameras, routers, printers, and smart devices
12. **Shopping Info** - Discover pricing, inventory, and e-commerce data
13. **Password Info** - Locate password files, credentials, and authentication data


## Installation

### Prerequisites
- Python 3.7 or higher
- Internet connection for Google searches

### Quick Setup
```bash
# Clone or download the tool
git clone <repository-url>
cd google-dorker

# Install dependencies (optional)
pip install -r requirements.txt

# Make executable (Linux/Mac)
chmod +x google_dorker.py
```

## Usage

### GUI Version (Hacker Terminal Interface)
```bash
# Launch the GUI with Matrix-style animation
python launch_gui.py

# Windows users can double-click
launch_gui.bat
```

### Interactive Mode (Recommended)
```bash
python google_dorker.py --interactive
```

### Command Line Usage

#### Basic Usage
```bash
# Generate 10 basic dork queries for a target
python google_dorker.py -t example.com

# Generate queries for specific category
python google_dorker.py -t example.com -c file_discovery

# Generate advanced queries with keywords
python google_dorker.py -t example.com -k admin,login,config

# Save results to file
python google_dorker.py -t example.com -o results.json
```

#### Advanced Options
```bash
# Generate more queries
python google_dorker.py -t example.com -n 20

# Hide ethical warnings (not recommended)
python google_dorker.py -t example.com --no-warnings

# Generate OSINT queries
python google_dorker.py -t example.com --osint
```

### Example Output
```
[1] FILE_DISCOVERY
Query: site:example.com filetype:pdf
Description: Discover documents on target website (pdf files)
Risk Level: Medium
Use Case: Find pdf files on example.com
Google URL: https://www.google.com/search?q=site%3Aexample.com+filetype%3Apdf
--------------------------------------------------------------------------------

[2] DIRECTORY_LISTING
Query: site:example.com intitle:index.of
Description: Find directory listings on target
Risk Level: High
Use Case: Security assessment of example.com
Google URL: https://www.google.com/search?q=site%3Aexample.com+intitle%3Aindex.of
--------------------------------------------------------------------------------
```

## Configuration

The tool uses `config.json` for settings:

```json
{
  "settings": {
    "delay_between_requests": 2,
    "max_queries_per_category": 5,
    "default_query_count": 10,
    "enable_ethical_warnings": true
  },
  "categories": {
    "file_discovery": {
      "enabled": true,
      "priority": 1,
      "risk_threshold": "medium"
    }
  }
}
```

## Algorithm Details

### Query Generation Algorithm
1. **Template Selection**: Choose from 50+ pre-defined dork templates
2. **Target Integration**: Insert target domain into appropriate query positions
3. **Extension Variation**: Generate multiple queries for different file types
4. **Risk Assessment**: Assign risk levels based on potential impact
5. **Categorization**: Organize queries by reconnaissance purpose

### Advanced Features
- **Smart Template Matching**: Algorithms select most effective templates for target
- **Risk-Based Filtering**: Filter queries by risk level
- **Contextual Keywords**: Generate relevant keywords based on target analysis
- **Query Optimization**: Remove redundant or ineffective queries

## Legal and Ethical Considerations

### Authorized Use Only
- Penetration testing with written authorization
- Security research on owned systems
- Educational purposes in controlled environments
- Bug bounty programs with explicit scope

### Prohibited Uses
- Unauthorized access to systems
- Malicious reconnaissance
- Privacy violations
- Any illegal activities

### Best Practices
1. **Always obtain written authorization** before testing
2. **Document findings** responsibly
3. **Follow responsible disclosure** for vulnerabilities
4. **Comply with local laws** and regulations

## Contributing

Contributions are welcome! Please ensure:

1. All contributions maintain ethical standards
2. New dork templates include proper risk assessments
3. Documentation is updated for new features
4. Code follows security best practices

## License

This tool is provided for educational and authorized security testing purposes only. Users are responsible for compliance with applicable laws and regulations.

## Disclaimer

The authors and contributors of this tool are not responsible for any misuse or damage caused by this software. Use at your own risk and ensure you have proper authorization before conducting any security assessments.

## Support

For questions, issues, or contributions:
- Create an issue in the repository
- Follow responsible disclosure for security issues
- Ensure all communications maintain ethical standards

---

**Remember: With great power comes great responsibility. Use this tool ethically and legally! 🛡️**
