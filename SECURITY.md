# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| main branch | Yes |

## Reporting a Vulnerability

If you discover a security vulnerability in Keel, please report it responsibly:

1. **Do not** open a public GitHub issue
2. Email the maintainers at the address listed in the repository settings
3. Include a description of the vulnerability, steps to reproduce, and potential impact

### Response Timeline

- **Acknowledgment:** within 3 business days
- **Assessment:** within 10 business days
- **Fix or mitigation:** depends on severity, but we aim for 30 days for critical issues

## Scope

Keel is a documentation and rule distribution system. Security concerns most relevant to this project include:

- Rules that could instruct AI agents to perform unsafe operations
- Sync prompt injection vulnerabilities
- Exposure of secrets or credentials in rule content
