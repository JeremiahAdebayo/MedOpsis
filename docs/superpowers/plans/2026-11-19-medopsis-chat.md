# MedOpsis text-chat implementation checklist

User approval: the user explicitly confirmed that the plan is approved. Execute directly in this session; do not ask for design/plan approval again. The approved specification is ../specs/2026-11-19-medopsis-chat-design.md.

## Global constraints

Text chat only, Python/FastAPI, Groq openai/gpt-oss-120b, en/yo/ig/ha, Kotlin/SQLite app-side. No voice/image implementation, agents, vector database, server chat storage, deployment, paid calls, or real patient data. Preserve all validation, authentication, source-review, privacy, and error contracts from the approved specification. Default reference asset is absent until clinician-reviewed content is supplied; do not fabricate clinical approval.

Work in the existing feat/text-chat branch. Keep all implementation and self-review sequential; no automatic agent handoffs or additional worktree setup. Scope is the backend and its tests/documentation, not the rest of the platform.

## Tasks

- [x] Bootstrap an isolated .venv with backend/requirements.txt and backend/requirements-dev.txt; protect local artifacts with .gitignore.
- [x] Add a failing HTTP authentication test in tests/test_chat.py, observe RED, then create backend/app/main.py with fail-closed access.
- [x] Implement strict request/reply schemas in ai_services/chat/models.py through test-first slices: languages, roles, history, nonblank text, exact content preservation, UTF-8 limits, and reply/reference validation.
- [x] Implement ai_services/chat/knowledge.py: bounded local approved pack loading, unique source IDs, HTTPS metadata, actual context-size checks; tests use explicitly synthetic fixtures only.
- [x] Implement ai_services/chat/auth.py: RS256 JWT verification against server-configured issuer/audience/HTTPS JWKS; reject token-controlled key URLs; test real signatures with synthetic keys and controlled retrieval.
- [x] Implement ai_services/chat/provider.py: one Groq client, bounded strict JSON output, no redirects/tools/retries/paid fallback, correct safe error mapping and reference resolution. Mock external transport in tests, never claim those are live model results.
- [x] Integrate the authenticated streamed-size-limited POST /chat route and OpenAPI contract; verify conversation/report/language forwarding and errors without health-data or credential leaks.
- [x] Document .env.example, docs/setup.md, docs/api_documentation.md and README.md with commands actually exercised; run the full suite and a local HTTP smoke test.
- [ ] If authorized project credentials and verified free-account controls are available, perform a synthetic live-model smoke test; otherwise report this blocker explicitly. Clinical/native-language review, app identity integration and patient-release governance remain separate external gates.

## Execution and verification

For each behaviour: write its test, run .venv/bin/python -m pytest tests/test_chat.py -q --basetemp="$TMPDIR/medopsis-pytest", observe the missing behaviour, implement minimally, rerun, then self-review the diff. Commit verified task batches locally. All pytest temporary artifacts stay under TMPDIR. Before claiming delivery, run the complete suite and actual local HTTP request; label any mocked dependencies. Do not push or deploy without authorization.

## Verified execution

Automated suite: 51 tests passed. Provider and signing-key retrieval are mocked/controlled; JWT signatures and application code are real. Loopback Uvicorn HTTP checks: OpenAPI 200, missing bearer 401, dummy bearer with unconfigured issuer 503. No Groq inference, real app issuer, clinical review, native-language evaluation, deployment or paid operation has been verified/performed. A project-specific authorized free-tier key and real approved content/identity configuration are remaining integration inputs.
