# DraftGuard

A tightly integrated CKEditor 5 plugin that brings real-time AI augmentation and compliance validation into the patent drafting workflow.

## Project Vision

DraftGuard is an embedded, domain-specific copilot for the patent lifecycle. It injects a context-aware suggestion engine powered by an LLM backend—triggered inline via toolbar or typing context—that recommends clause completions, reformulations, and relevant prior art, all without leaving the editor.

Beyond simple generation, it enforces formal structure (e.g., Background → Summary → Claims), validates claim dependencies (e.g., claim 5 referencing non-existent claim 7), checks for antecedent basis violations (undefined elements), and surfaces red-underlined live feedback for USPTO compliance issues. Visual confidence scores accompany suggestions to guide user trust, and every insertion respects CKEditor's structured model. This tool doesn't just generate—it critiques, guides, and polishes, all within the legal author's native environment.

## Key Features

-   **Real-time AI Augmentation**: Context-aware suggestions for clause completions and reformulations.
-   **Inline Prior Art Search**: Recommends relevant prior art without leaving the editor.
-   **Live Compliance Validation**:
    -   Enforces formal patent structure (Background → Summary → Claims).
    -   Validates claim dependencies.
    -   Checks for antecedent basis violations.
-   **Live Feedback**: USPTO compliance issues are highlighted with red underlines.
-   **Visual Confidence Scores**: Suggestions are accompanied by scores to guide user trust.
-   **Seamless Integration**: Built as a CKEditor 5 plugin, respecting its structured data model and undo/redo history.

## Technical Implementation Plan

### Frontend: CKEditor 5 Plugin (`PatentCopilotPlugin`)

-   **Initialization**: The main `PatentCopilotPlugin` initializes the full system and registers a toolbar button.
-   **Real-time Triggers**: Listens to `editor.model.document.on('change:data')` with a debounce mechanism to trigger suggestions and validation.
-   **Context Extraction**: Dynamically selects the relevant span (entire claim, paragraph, or section) based on the task.
-   **UI Components**:
    -   Suggestions are displayed via a contextual balloon UI, showing the LLM completion and a visual confidence score (stars, color gradients, or % bars).
    -   Validation errors (e.g., antecedent basis issues) are rendered using CKEditor Markers with red underlines and tooltips.
-   **Model Integrity**: All UI insertions use `editor.model.change()` to maintain undo/redo integrity and schema correctness.
-   **Performance Metrics**: A UI overlay will display demo metrics:
    ```ts
    interface DemoMetrics {
      suggestionsAccepted: number;
      errorsPreventedLive: number;
      draftingTimeReduced: string; // "67% faster"
      rulesEnforced: string[];
    }
    ```

### Backend: FastAPI Monolith

The backend is a **FastAPI monolith** with clearly separated internal services.

-   **Orchestration Service**: Routes requests to internal handlers based on task type (suggestion, validation, search).
-   **LLM Service**: Handles prompt construction, response formatting, and confidence scoring using **GPT-4o** via the OpenAI API.
-   **Validation Service**:
    -   Runs deterministic rule checks: claim dependency parsing, structural section validation, and antecedent basis detection.
    -   Uses caching for high-frequency rules:
        ```python
        @lru_cache(maxsize=1000)
        def validate_claim_structure(claim_text: str) -> ValidationResult:
            # Expensive rule checking
            pass
        ```
    -   Compliance ruleset is defined in a structured JSON config and applied dynamically.
-   **Prior Art Service**: Encodes claims using a patent-tuned BERT model and searches a **pgvector + PostgreSQL** database populated with USPTO patent embeddings.

### Communication: Real-time & REST

-   **Websocket Channel**: A **websocket channel** is used for low-latency validation and live error streaming.
-   **Fallback Mechanism**: If the websocket connection fails, the system falls back to the REST API.
    ```ts
    if (websocketConnection.failed) {
      fallbackToRestAPI();
      showUserNotification("Switched to backup mode");
    }
    ```

### API Details

The REST API is designed to be clean, versioned, and demo-friendly.

-   **Endpoints**:
    -   `POST /api/v1/completions` — returns AI-generated clause
    -   `POST /api/v1/reformulations` — returns alternative phrasings
    -   `POST /api/v1/validations/live` — returns syntax/compliance violations
    -   `GET  /api/v1/prior-art/search` — returns similar patents based on vector similarity
    -   `WS   /api/v1/realtime/validate` — websocket stream for real-time validation
-   **Standard Response Schema**:
    ```json
    {
      "suggestions": ["text 1", "text 2"],
      "confidence": 0.89,
      "processing_time_ms": 234,
      "rules_applied": ["USPTO_CLAIM_FORMAT", "ANTECEDENT_BASIS"]
    }
    ```

### Security

-   Authentication will be handled via JWT.
-   TLS will be enforced for all traffic.
-   All traffic will be tied to specific users/organizations.

### Deployment

A **demo-ready deployment pipeline** will be created using a multi-stage Docker build.

```dockerfile
FROM node:18 as frontend
# build ckEditor plugin + bundle UI

FROM python:3.11 as backend
# install FastAPI, pgvector, orchestration

FROM nginx
# serve static frontend + proxy backend routes
```
