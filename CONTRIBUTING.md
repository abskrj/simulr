# Contributing to Physics Simulation Dashboard

Thank you for your interest in contributing to the Physics Simulation Dashboard! This guide will help you get started with contributing to the project.

## 🎯 How to Contribute

There are many ways to contribute to this project:

- 🐛 **Report bugs** - Help us identify and fix issues
- 💡 **Suggest features** - Share ideas for new functionality
- 📖 **Improve documentation** - Help make our docs better
- 🔧 **Fix bugs** - Submit pull requests for bug fixes
- ✨ **Add features** - Implement new functionality
- 🧪 **Add tests** - Improve test coverage
- 🎨 **Improve UI/UX** - Make the interface more user-friendly

## 🚀 Getting Started

### 1. Fork the Repository

Click the "Fork" button at the top right of the repository page to create your own copy.

### 2. Clone Your Fork

```bash
git clone https://github.com/abskrj/simulr.git
cd simulr
```

### 3. Set Up Development Environment

Follow the development setup instructions in the [README.md](README.md#development).

### 4. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

## 📋 Development Guidelines

### Code Style

**Python (Backend):**
- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints for all functions
- Maximum line length: 88 characters (Black formatter)
- Use meaningful variable and function names

**TypeScript/JavaScript (Frontend):**
- Follow [Prettier](https://prettier.io/) formatting
- Use TypeScript for all new code
- Follow React best practices
- Use meaningful component and variable names

**General:**
- Write clear, concise comments
- Use descriptive commit messages
- Keep functions small and focused
- Write tests for new functionality

### Code Formatting

We use automated formatters to maintain consistent code style:

```bash
# Python formatting
cd backend
black .
isort .

# Frontend formatting
cd frontend
npm run format
```

### Testing

**Backend Tests:**
```bash
cd backend
pytest
pytest --cov=app  # With coverage
```

**Frontend Tests:**
```bash
cd frontend
npm test
npm run test:coverage
```

**Integration Tests:**
```bash
docker-compose -f docker-compose.test.yml up
```

### Documentation

- Update README.md for user-facing changes
- Add docstrings to Python functions
- Comment complex logic
- Update API documentation for endpoint changes

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Clear description** of the issue
2. **Steps to reproduce** the problem
3. **Expected behavior** vs actual behavior
4. **Environment details** (OS, Python version, etc.)
5. **Screenshots** if applicable
6. **Error messages** or logs

**Bug Report Template:**
```markdown
## Bug Description
Brief description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Windows 10, macOS 12, Ubuntu 20.04]
- Python: [e.g., 3.11.5]
- Node.js: [e.g., 18.17.0]
- Browser: [e.g., Chrome 116, Firefox 117]

## Additional Context
Any other relevant information
```

## 💡 Feature Requests

When suggesting new features:

1. **Check existing issues** to avoid duplicates
2. **Clearly describe** the feature and its benefits
3. **Provide use cases** and examples
4. **Consider implementation** complexity
5. **Discuss alternatives** if applicable

**Feature Request Template:**
```markdown
## Feature Description
Clear description of the proposed feature

## Use Case
Why is this feature needed? What problem does it solve?

## Proposed Solution
How should this feature work?

## Alternatives Considered
Other approaches that were considered

## Additional Context
Any other relevant information
```

## 📝 Pull Request Process

### Before Submitting

1. **Test your changes** thoroughly
2. **Run all tests** and ensure they pass
3. **Update documentation** if needed
4. **Follow code style** guidelines
5. **Write clear commit messages**

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): description

feat(api): add new simulation endpoint
fix(frontend): resolve 3D rendering issue
docs(readme): update installation instructions
style(backend): fix code formatting
test(api): add unit tests for chat service
```

### Pull Request Template

When creating a pull request, include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## How Has This Been Tested?
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

### Review Process

1. **Automated checks** must pass (tests, linting, etc.)
2. **Code review** by maintainers
3. **Address feedback** if requested
4. **Final approval** and merge

## 🏗️ Project Structure

Understanding the project structure helps when contributing:

```
physics-simulation-dashboard/
├── backend/
│   ├── app/
│   │   ├── api/           # API route handlers
│   │   ├── models/        # Pydantic data models
│   │   ├── services/      # Business logic
│   │   ├── templates/     # Example structures
│   │   └── utils/         # Utility functions
│   ├── tests/             # Backend tests
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── hooks/         # Custom React hooks
│   │   ├── services/      # API client services
│   │   └── types/         # TypeScript type definitions
│   ├── tests/             # Frontend tests
│   └── package.json       # Node.js dependencies
├── scripts/               # Deployment and utility scripts
├── docs/                  # Additional documentation
└── docker-compose.yml     # Docker orchestration
```

## 🎨 Design Guidelines

### UI/UX Principles

- **Simplicity**: Keep interfaces clean and intuitive
- **Accessibility**: Ensure features are accessible to all users
- **Responsiveness**: Design for desktop and mobile
- **Performance**: Optimize for fast loading and smooth interactions

### Color Scheme

- Primary: Physics simulation blue (#0066cc)
- Secondary: Force vector red (#cc0000)
- Accent: Stress indicator yellow (#ffaa00)
- Neutral: Gray scale for backgrounds and text

## 🔧 Development Tips

### Backend Development

- Use FastAPI's automatic API documentation
- Implement proper error handling
- Add logging for debugging
- Use dependency injection for services
- Write comprehensive tests

### Frontend Development

- Use React hooks for state management
- Implement proper error boundaries
- Optimize Three.js performance
- Use TypeScript for type safety
- Write component tests

### Database Changes

- Create migration scripts for database changes
- Test migrations thoroughly
- Document schema changes
- Consider backward compatibility

## 📚 Resources

### Learning Materials

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Three.js Documentation](https://threejs.org/docs/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

### Tools

- [VS Code](https://code.visualstudio.com/) - Recommended IDE
- [Docker Desktop](https://www.docker.com/products/docker-desktop) - For containerization
- [Postman](https://www.postman.com/) - API testing
- [Git](https://git-scm.com/) - Version control

## 🤝 Community

### Communication

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For general questions and ideas
- **Discord**: Real-time chat with contributors
- **Email**: For private or sensitive matters

### Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). Please be respectful and inclusive in all interactions.

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors are recognized in several ways:

- Listed in the project's contributors page
- Mentioned in release notes for significant contributions
- Invited to join the core team for outstanding contributors
- Featured in project documentation

---

**Questions?** Don't hesitate to ask! Open an issue or start a discussion if you need help getting started.

**Thank you for contributing to Physics Simulation Dashboard!** 🎉 