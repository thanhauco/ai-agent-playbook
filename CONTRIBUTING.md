# Contributing to AI Agent Playbook

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-agent-playbook.git
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

- `langchain/`, `crewai/`, `autogen/`, `langgraph/` - Classic frameworks
- `pydantic_ai/`, `openai_agents/`, `llamaindex/`, `microsoft_agents/` - Modern frameworks (2025)
- `mcp/`, `a2a/` - Protocols
- `advanced/` - Advanced patterns
- `use_cases/` - Real-world examples
- `testing/` - Test examples
- `integrations/` - Integration examples

## Contributing Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Include docstrings for all functions and classes
- Keep examples self-contained and runnable

### Adding New Examples

1. Create a new file in the appropriate directory
2. Include clear comments and documentation
3. Add example usage at the bottom with `if __name__ == "__main__":`
4. Test the example works correctly
5. Update README.md if adding a new category

### Testing

Run tests before submitting:
```bash
pytest testing/ -v
```

### Commit Messages

Use clear, descriptive commit messages:
- ✅ "Add LlamaIndex RAG agent example"
- ✅ "Fix streaming agent error handling"
- ❌ "Update file"

### Pull Requests

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Test thoroughly
4. Commit with clear messages
5. Push to your fork
6. Create a Pull Request with description of changes

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on what is best for the community
- Show empathy towards others

## Questions?

Open an issue or start a discussion on GitHub.

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
