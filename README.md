# MedOpsis

AI-powered optical health-screening and medical-education platform. This branch implements the text-chat backend only; image recognition, voice, and Android are separate workstreams.

## What's here

- Stateless `POST /chat` API (FastAPI) with app-issued RS256 JWT authentication.
- Groq `qwen/qwen3.8-27b` generation with strict local validation.
- English, Yoruba, Igbo, and Hausa (`en`, `yo`, `ig`, `ha`).
- Bounded local approved-reference pack (absent by default).

## Start

See [setup](docs/setup.md) for environment variables, tests, and the loopback server.

## API

`POST /chat` requires a `language` code (`en`/`yo`/`ig`/`ha`), ordered `messages`, and an optional text-only `screening_report`. Full request/response and error contract: [API documentation](docs/api_documentation.md).

## Status

Backend verified locally (63 tests; synthetic live requests returned HTTP 200 in four languages). Not deployed or cleared for patient use.
