# Physics Simulation Dashboard

> **Transform natural language into interactive 3D physics simulations**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

A revolutionary physics simulation platform that converts natural language descriptions into interactive 3D visualizations. Simply describe your physics scenario in plain English, and watch as AI generates detailed structural simulations with force vectors, stress analysis, and interactive controls.

## ✨ Features

- 🗣️ **Natural Language Input**: Describe simulations in plain English
- 🎯 **3D Visualization**: Interactive Three.js-powered 3D rendering
- 🔧 **Structural Analysis**: Comprehensive stress and force visualization
- 💬 **Chat Interface**: Iterative simulation refinement through conversation
- 🎮 **Interactive Controls**: Click, zoom, rotate, and explore your simulations
- 🌈 **Color-Coded Stress**: Visual stress indicators across structural elements
- 📊 **Force Vectors**: Real-time force direction and magnitude display
- 🔄 **Session Management**: Save and continue simulation sessions
- 🎨 **Modern UI**: Clean, responsive interface built with React
- 🚀 **High Performance**: Optimized for complex structural calculations

## 🎬 Demo

<!-- Add screenshots or GIF demos here -->
```
[Demo GIF/Screenshots will be added here]
```

**Try these example prompts:**
- "Show me how stress distributes across a steel truss bridge"
- "What happens to a skyscraper frame during wind loads?"
- "Analyze the forces in a simple cantilever beam"

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/physics-simulation-dashboard.git
   cd physics-simulation-dashboard
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

3. **Start the application**
   ```bash
   # Linux/Mac
   ./scripts/start.sh
   
   # Windows
   .\scripts\start.ps1
   ```

4. **Access the application**
   - Frontend: http://localhost
   - API Documentation: http://localhost:8000/docs

### Manual Installation

<details>
<summary>Click to expand manual installation steps</summary>

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

#### Redis Setup
```bash
# Install Redis locally or use Docker
docker run -d -p 6379:6379 redis:alpine
```

</details>

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│               Load Balancer                 │
│                 (Nginx)                     │
│          Frontend + API Proxy               │
├─────────────────────────────────────────────┤
│                                             │
│  React Frontend          FastAPI Backend   │
│  (Three.js + Vite)      (Python + OpenAI)  │
│                                             │
├─────────────────────────────────────────────┤
│                Redis                        │
│         (Session Storage)                   │
└─────────────────────────────────────────────┘
```

### Tech Stack

**Frontend:**
- React 18+ with TypeScript
- Three.js for 3D rendering
- Vite for build tooling
- Tailwind CSS for styling

**Backend:**
- FastAPI (Python 3.11+)
- OpenAI GPT-4 for natural language processing
- Redis for session management
- Pydantic for data validation

**Infrastructure:**
- Docker & Docker Compose
- Nginx as reverse proxy
- GitHub Actions for CI/CD

## 📖 Usage

### Basic Usage

1. **Enter your simulation request** in natural language:
   ```
   "Show me the stress distribution on a suspension bridge"
   ```

2. **Interact with the 3D visualization**:
   - Click and drag to rotate
   - Scroll to zoom
   - Click on elements to highlight

3. **Refine your simulation** through chat:
   ```
   "Make the bridge longer and add more cables"
   ```

### Advanced Features

- **Session Management**: Your simulations are saved automatically
- **Export Options**: Download simulation data and images
- **Collaboration**: Share simulation sessions with team members
- **Custom Materials**: Define specific material properties

## 🔧 API Documentation

### Core Endpoints

#### Generate Simulation
```http
POST /api/simulate
Content-Type: application/json

{
  "description": "steel truss bridge with wind load",
  "complexity": "medium"
}
```

#### Chat Interface
```http
POST /api/chat
Content-Type: application/json

{
  "message": "make the bridge longer",
  "session_id": "uuid-here"
}
```

#### Get Examples
```http
GET /api/examples
```

For complete API documentation, visit `/docs` when running the application.

## 🛠️ Development

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Redis (local or Docker)

### Development Setup

1. **Clone and setup**
   ```bash
   git clone https://github.com/yourusername/physics-simulation-dashboard.git
   cd physics-simulation-dashboard
   ```

2. **Backend development**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

3. **Frontend development**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Docker development**
   ```bash
   docker-compose up --build
   ```

### Project Structure

```
physics-simulation-dashboard/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── models/       # Pydantic models
│   │   ├── services/     # Business logic
│   │   └── templates/    # Example structures
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── hooks/        # Custom hooks
│   │   └── services/     # API services
│   ├── Dockerfile
│   └── package.json
├── scripts/              # Deployment scripts
├── docker-compose.yml
└── README.md
```

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# Integration tests
docker-compose -f docker-compose.test.yml up
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribution Steps

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Run tests**
   ```bash
   npm test
   pytest
   ```
5. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
6. **Push to your branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for all frontend code
- Add tests for new features
- Update documentation for API changes
- Use conventional commits

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for GPT-4 API
- **Three.js** community for 3D rendering
- **FastAPI** for the excellent web framework
- **React** team for the frontend framework

## 📞 Support

- 📧 **Email**: support@yourproject.com
- 💬 **Discord**: [Join our community](https://discord.gg/yourproject)
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/physics-simulation-dashboard/issues)
- 📖 **Documentation**: [Full Documentation](https://docs.yourproject.com)

## 🗺️ Roadmap

- [ ] **Mobile App**: React Native mobile application
- [ ] **Advanced Materials**: Custom material property definitions
- [ ] **Collaboration Tools**: Real-time collaborative editing
- [ ] **Plugin System**: Extensible plugin architecture
- [ ] **Cloud Deployment**: One-click cloud deployment options
- [ ] **AI Models**: Support for multiple AI model providers
- [ ] **Performance Optimization**: WebGL and WebAssembly optimizations

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/physics-simulation-dashboard)
![GitHub forks](https://img.shields.io/github/forks/yourusername/physics-simulation-dashboard)
![GitHub issues](https://img.shields.io/github/issues/yourusername/physics-simulation-dashboard)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/physics-simulation-dashboard)

---

**Made with ❤️ by the Physics Simulation Dashboard team**

*Star ⭐ this repository if you find it helpful!* 