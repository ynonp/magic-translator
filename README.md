# Magic Translator

A FastAPI-based translation service powered by Ollama Cloud and the `gemini-3-flash-preview` model.

## Prerequisites

- Python 3.14.3 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- An Ollama Cloud API key

## Installation

1. Clone the repository:

```bash
cd magic-translator
```

2. Install dependencies using uv:

```bash
uv sync
```

This will create a virtual environment and install all required dependencies.

## Configuration

Create a `.env` file in the project root with your Ollama Cloud API key:

```bash
OLLAMA_API_KEY=your-api-key-here
```

## Running the Application

Start the FastAPI server using uv:

```bash
uv run uvicorn main:app --reload
```

The server will start at `http://localhost:8000`.

### API Endpoints

- **POST /translate** - Translate text to multiple languages
  - Request body:
    ```json
    {
      "text": "Hello, world!",
      "languages": ["es", "fr", "de"]
    }
    ```
  - Response:
    ```json
    {
      "en": "Hello, world!",
      "es": "Hola, mundo!",
      "fr": "Bonjour le monde!",
      "de": "Hallo, Welt!"
    }
    ```

- **GET /** - Serves the HTML frontend from the `static/` directory

## Supported Languages

The following language codes are supported:

| Code | Language   |
|------|------------|
| en   | English    |
| es   | Spanish    |
| fr   | French     |
| de   | German     |
| it   | Italian    |
| pt   | Portuguese |
| ru   | Russian    |
| zh   | Chinese    |
| ja   | Japanese   |
| ko   | Korean     |
| ar   | Arabic     |
| hi   | Hindi      |
| he   | Hebrew     |
| tr   | Turkish    |
| pl   | Polish     |
| nl   | Dutch      |
| sv   | Swedish    |
| vi   | Vietnamese |
| th   | Thai       |
| uk   | Ukrainian  |

## Development

### Running Tests

(Add your test command here if you have tests set up)

### Adding New Dependencies

```bash
uv add <package-name>
```

### Updating Dependencies

```bash
uv sync --upgrade
```

## Project Structure

```
magic-translator/
├── main.py          # FastAPI application
├── static/          # HTML frontend files
├── pyproject.toml   # Project configuration
├── uv.lock          # Dependency lock file
└── .env             # Environment variables (not in version control)
```

## License

MIT
