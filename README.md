# AI Governance Gateway

A careful middle-man that sits between a user and an AI-Model and asks questions like:
_"Should I even let the AI answer this?"_,
_"If it answers, is the answer safe?"_,
_"Can I explain later why this answer was given?"_

This is a system designed to track WHY a descision was made by an AI system while also putting guardrails in place to decide IF a decision should be made by an AI.

This is an LLM wrapper API with auditability, policy enforcement and verification.

## Governance Philosophy
This project is built around the belief that AI-enabled systems must be governed like any other high-risk backend dependency.

While the system does not claim regulatory compliance, its design is intentionally informed by governance principles found in regulated environments such as healthcare, finance, and public-sector systems.

The goal is to demonstrate how systems should be structured when auditability and data stewardship matter.

### Regulatory Inspiration

The governance model in this service is inspired by (but does not claim compliance with) widely respected industry frameworks, including:

- **Health Insurance Portability and Accountability Act (HIPAA)**
    Emphasis on data minimization, access control, and auditability of sensitive information.

- **SOC 2–style control thinking**
    Particularly around change traceability, monitoring, and accountability for system behavior.

- **International Organization for Standardization ISO 27001 principles**
    Including least privilege, explicit policy enforcement, and defense-in-depth.

This project is demonstrative and educational: it shows how these principles can be applied to AI systems without overstating legal guarantees.

### Core Governance Principles
1. ***Explicit Policy Enforcement***
    Every request is evaluated against deterministic, rule-based policies before any AI processing occurs. If a request violates policy, it is denied before reaching an AI model.

    Policies are:
        human-readable
        testable
        explainable
        enforced consistently

2. ***Deny-by-Default*** for Unsafe Combinations
    Certain combinations of input context are treated as inherently unsafe.
   
   For example:
   confidential data + external audience → denied

    This mirrors real-world regulatory expectations, where some data flows are prohibited regardless of intent or downstream safeguards.

4. ***Data Minimization***
    Inputs are hashed using a deterministic cryptographic hash. The hash enables audit, replay detection, and verification. Sensitive content is never persisted

5. ***Explainability and Auditability by Design***
    Every request produces an explicit, reviewable decision, including:
        a clear allow/deny outcome
        human-readable policy reasons
        machine-readable risk flags

    Each decision is recorded in an immutable audit log which captures:
        request metadata (without raw input content)
        applied policies and rationale
        detected risk signals
        timestamps

    This ensures that system behavior can be reviewed after the fact, failures can be explained rather than inferred, and accountability is maintained in regulated or high-risk environments. Governance does not rely on “trusting the model,” and audit logging is treated as a core system capability, not an afterthought!

### Intended Audience
This system is designed for:
    engineers evaluating whether an AI system should be deployed
    teams operating in regulated or high-risk domains
    reviewers assessing governance maturity, not just functionality

It is intentionally conservative, explicit, and opinionated in its constraints.

### Personal Note :)
This project reflects my interest in building AI-enabled backend systems that are testable, auditable, and suitable for regulated environments.
The focus is not on maximizing AI capability, but on making AI systems defensible, reviewable, and safe to operate.

## Prompt Versioning
Prompts are treated as versioned system artifacts.
They are stored as files to support:
    - change review
    - auditability
    - regression testing across versions

## License
MIT 

## Contact
*   LinkedIn: [linkedin.com](https://www.linkedin.com/in/sasha-naude/)
*   Email: sasha.naude1@gmail.com
