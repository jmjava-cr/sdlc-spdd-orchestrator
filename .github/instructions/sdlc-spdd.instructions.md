---
name: sdlc-spdd-orchestrator
description: "SDLC-SPDD Orchestrator framework for disciplined AI-assisted software delivery. Use when: planning features using REASONS Canvas, initializing new projects with SPDD scaffolding, architecting solutions with design contracts, implementing tasks against explicit contracts, or maintaining orchestrator templates."
applyTo: ["**/*.md", "scripts/**", "templates/**", "agent-context/**"]
---

# SDLC-SPDD Orchestrator - Copilot Instructions

## Project Overview

The SDLC-SPDD Orchestrator is a framework that combines:
- **SDLC Agents' lifecycle** — Multi-stage software delivery workflow (Init → Plan → Architect → Code → Review → Retro → Sync)
- **OpenSPDD's REASONS Canvas** — Structured design contract (Requirements, Entities, Approach, Structure, Operations, Safeguards)

This creates disciplined, repeatable workflows where AI agents operate against explicit contracts rather than generating code in isolation.

**Key Insight**: This framework works with any AI tool (Cursor, Copilot, Claude, ChatGPT) to bring structure and traceability to software delivery.

---

## Core Principles

### 1. REASONS Canvas Pattern

Every feature or spike starts with a **REASONS Canvas** — a structured design contract:

- **R (Requirements)** — User goal, business goal, acceptance criteria, non-goals, assumptions, open questions
- **E (Entities)** — Domain entities, services, controllers, clients, data models, external systems
- **A (Approach)** — Proposed solution, alternatives considered, trade-offs, risks, failure modes
- **S (Structure)** — File structure, artifacts to produce, directory layout, schema changes
- **O (Operations)** — Task breakdown by milestone/phase, acceptance criteria per task, dependencies
- **S (Safeguards)** — Security constraints, compliance rules, performance requirements
- Plus: **Success Metrics**, **Dependencies**, **Stakeholders**, **Approval Checklist**

### 2. Agent Context Pattern

Every project using SPDD gets an **agent-context/** directory:

```
agent-context/
  ├── memory/                           # Persistent knowledge
  │   ├── architecture-decisions.md     # ADRs (Architecture Decision Records)
  │   ├── project-memory.md             # Context, blockers, integration points
  │   ├── known-pitfalls.md             # Common mistakes + mitigations
  │   └── reusable-patterns.md          # Language/framework-specific patterns
  ├── harness/                          # Quality & validation gates
  │   ├── quality-gates.md              # Entry/exit criteria per milestone
  │   └── validation-rules.md           # Security, performance, compliance rules
  ├── playbooks/                        # Workflow scripts
  │   ├── [language]-[domain]-playbook.md  # Step-by-step implementation guides
  │   ├── pr-review-playbook.md         # Code review checklist
  │   └── bugfix-playbook.md            # Debugging patterns
  ├── features/                         # Feature tracking
  │   └── [FEAT-ID].md                  # Feature decision records
  └── spikes/                           # Spike tracking (optional)
      └── [SPIKE-ID].md                 # Spike decision records
```

This context gets included in Copilot prompts so the AI maintains consistency across conversations.

### 3. Task-Level Granularity

Each task in **Operations** should be granular and achievable:
- Clear acceptance criteria (checkboxes)
- Specific files affected
- Dependencies on other tasks
- Estimated hours
- Success indicators

### 4. Design Contract Enforcement

Before starting **any** implementation:
1. ✅ REASONS Canvas reviewed and approved
2. ✅ Architecture decisions logged (ADRs)
3. ✅ Quality gates defined (entry/exit per milestone)
4. ✅ Known pitfalls documented
5. ✅ Reusable patterns identified

Implementation follows the contract; don't skip this.

---

## When to Use This Framework

### ✅ Use SPDD When:
- **Planning a multi-milestone feature** (> 1 week of work)
- **Designing for reusability** (other teams will use this code)
- **Security-critical code** (auth, payments, PII)
- **Establishing team patterns** (new architecture layer, first OAuth2 implementation)
- **Spike evaluation** (should we adopt new framework/technology?)

### ⏹️ Skip SPDD When:
- **Bug fix** (< 4 hours, well-defined scope)
- **Localized refactoring** (one class, no architecture impact)
- **Documentation update** (internal README, inline comments)
- **Dependency upgrade** (minor version bump, no API changes)

**Rule of Thumb**: If you'd want architectural review + team knowledge capture, use SPDD.

---

## Workflows with Copilot

### Workflow 1: Planning a New Feature

**Step 1: Gather Requirements**
- Create `requirements/[FEAT-ID].md` with business context
- List acceptance criteria (test cases, edge cases)
- Identify external dependencies

**Step 2: Create REASONS Canvas**
- Start with `templates/feature-template.md` as base
- Fill in R-E-A-S-O-S sections incrementally
- Ask Copilot: *"Review this REASONS canvas for completeness. Are there missing entities, alternative approaches, or hidden dependencies?"*

**Step 3: Log Architecture Decisions (ADRs)**
- For each key decision, create entry in `agent-context/memory/architecture-decisions.md`
- Format: Decision ID (ADR-NNN), Context, Decision, Consequences, Alternatives
- Example: *"ADR-003: Email verification happens after provider authentication (not before), to avoid double API calls"*

**Step 4: Define Quality Gates**
- Add entry/exit criteria for each milestone to `agent-context/harness/quality-gates.md`
- Examples:
  - M1 Exit: "DEV environment running, Google OAuth2 configured, smoke test passing"
  - M2 Exit: "Email matching tested, state preservation validated, TC01-TC08 passing"
- Ask Copilot: *"Review these quality gates. Are they measurable and achievable?"*

**Step 5: Break Into Tasks**
- Fill Operations section with granular tasks
- Each task should be 4-8 hours, not weeks
- Link to architecture decisions, quality gates, and test cases

### Workflow 2: Implementing a Task

**Step 1: Load Context**
- Open REASONS Canvas (feature plan)
- Open relevant playbook (e.g., `agent-context/playbooks/java-spring-boot-playbook.md`)
- Open task definition from Operations section

**Step 2: Ask Copilot**
- *"Based on this task definition and the REASONS canvas, write the implementation for [specific task]. Reference architecture-decisions.md for design rationale."*
- Include task description, acceptance criteria, and related ADR IDs in prompt
- Copilot will maintain consistency with canvases and playbooks

**Step 3: Review Against Contract**
- Before submitting PR, check against quality gates
- Verify all acceptance criteria met
- Check PR description references ADR IDs and quality gate checkpoints

### Workflow 3: Design Review

**Step 1: Prepare Architecture Canvas**
- Summarize proposed design in REASONS Canvas format
- Highlight key decisions and trade-offs (Section A)
- List entities (Section E) — new services, controllers, tables

**Step 2: Ask Copilot**
- *"Review this architecture design against these quality gates. Identify risks, missing error handling, or security gaps."*
- Include quality-gates.md and known-pitfalls.md in context

**Step 3: Iterate**
- Copilot flags issues
- Update canvas / quality gates
- Re-run review until sign-off

### Workflow 4: Spike Evaluation

**Step 1: Create Spike Canvas**
- Use `templates/spike-template.md`
- Fill R-E-A-S-O-S for the question: *"Should we adopt framework X?"*
- Include experiment plan (what will we build and learn?)

**Step 2: Execute Spike Tasks**
- Narrow scope: 2-5 days max, ~40 hours max
- Document learnings in Operations section
- Update known-pitfalls.md with discoveries

**Step 3: Recommendation**
- Based on learnings, recommend: Go / No-go / Go with conditions
- Include risk assessment and alternative approaches

---

## Patterns for Different Languages

### Java / Spring Boot

**Playbook Location**: `agent-context/playbooks/java-spring-boot-playbook.md`

**Key Patterns**:
- Service → Repository → Entity (layered architecture)
- `@ConfigurationProperties` for externalized config
- `RestTemplate` or `WebClient` for HTTP calls
- `@Transactional` for data consistency
- Custom annotations for cross-cutting concerns (auth, logging, metrics)
- Test pyramid: Unit (70%), Integration (20%), E2E (10%)

**Example**: When implementing OAuth2 in Spring Boot:
1. Create `OAuthConfig.java` with `@Configuration`
2. Wire up `SecurityConfig` with `HttpSecurity.oauth2Login()`
3. Create `OAuthUserService` implementing `OAuth2UserService`
4. Test with `MockMvc` + `WithMockUser`

Ask Copilot: *"Create OAuth2 configuration following spring-boot-playbook.md patterns"* → Copilot will generate code consistent with project conventions.

### Python

**Playbook Location**: `agent-context/playbooks/python-playbook.md` (if project exists)

**Key Patterns**:
- Service classes as simple Python classes (no decorators needed)
- Protocol/ABC for interfaces (duck typing with validation)
- FastAPI for async, SQLAlchemy for ORM
- pytest fixtures for test setup
- type hints everywhere (Python 3.10+)

### TypeScript / Node.js

**Playbook Location**: `agent-context/playbooks/typescript-node-playbook.md`

**Key Patterns**:
- Class-based services, dependency injection (tsyringe, NestJS)
- Error classes extending `Error`
- `async/await` for async operations
- Jest for testing
- GraphQL or REST with typed responses

---

## Maintaining the Orchestrator

### Adding New Templates

When you discover a new pattern, templates go in `templates/`:

1. **Create template file**: `templates/my-pattern-template.md`
2. **Include sections**: R, E, A, S, O, S (and variations)
3. **Add examples**: Show filled-in templates for different domains
4. **Document in README**: When to use this template

Example: `templates/migration-template.md` for large refactorings or major upgrades.

### Updating Scripts

Scripts in `scripts/`:
- `init-project.sh` — Initialize new project (creates agent-context directories, runs stack detection)
- `detect-stack.sh` — Identify tech stack (Java, Node, Python, Docker, cloud provider)
- `validate.sh` — Check REASONS Canvas structure, file completeness
- `sync.sh` — Sync design docs with implementation reality

When updating scripts:
- Test on example projects first (`examples/`)
- Update documentation (`docs/`)
- Run validation on existing projects

### Contributing Examples

Examples in `examples/` show end-to-end workflows:
- `examples/spring-boot-order-api/` — Complete Spring Boot project with SPDD artifacts
- Add new example: `examples/my-stack-my-domain/`
- Include: Full REASONS canvas, completed implementation, test coverage

### Updating Documentation

Docs in `docs/`:
- `architecture.md` — System design, decision rationale
- `workflow.md` — Step-by-step usage guide
- `cursor-usage.md` — Cursor-specific commands (update if generalizing to other AIs)
- `design-decisions.md` — Rationale for framework choices

When updating docs:
- Keep consistent formatting
- Link to examples and templates
- Include before/after scenarios

---

## Common Questions for Copilot

### Planning Phase
- *"Review this REASONS canvas for completeness and feasibility"*
- *"What entities am I missing from the E section?"*
- *"Are these acceptance criteria testable and measurable?"*
- *"What risks did I miss in the A section?"*

### Architecture Phase
- *"Generate architecture decisions (ADRs) for these key design choices"*
- *"Create quality gates for each milestone in this plan"*
- *"What security constraints should I add to the Safeguards section?"*

### Implementation Phase
- *"Based on this task and the playbook, implement [component]. Reference ADRs in code comments."*
- *"Generate tests for this task using the test patterns in the playbook"*
- *"Review this implementation against the REASONS canvas. Are there gaps?"*

### Review Phase
- *"Check this PR against the quality gates and architecture decisions"*
- *"Does this implementation follow the patterns in [playbook]?"*
- *"Are there security or performance issues relative to the safeguards?"*

### Maintenance Phase
- *"Update known-pitfalls.md with what we learned from this feature"*
- *"Create an example project showing this pattern for future teams"*
- *"Extract reusable patterns from this implementation into the playbook"*

---

## File Organization Conventions

### Canvas Files
- Location: `spdd/canvas/` or `docs/planning/`
- Naming: `FEAT-{ID}-{description}.md` or `SPIKE-{ID}-{description}.md`
- Lifecycle: Draft → Review → Approved → Implemented → Archived
- Keep old versions in Git history for reference

### Task Files
- Location: `spdd/tasks/{FEAT-ID}/` or similar
- Naming: `T01-{task-name}.md`, `T02-{task-name}.md`, etc.
- Content: Acceptance criteria, affected files, dependencies
- Reference: Link to parent canvas and relevant ADRs

### Memory Files
- Location: `agent-context/memory/`
- Update frequency: As you learn (don't wait until end of project)
- Ownership: Entire team contributes
- Examples: *"We learned that X causes Y, use Z instead"*, *"Add to known-pitfalls.md"*

### Playbook Files
- Location: `agent-context/playbooks/`
- Naming: `{language}-{domain}-playbook.md`
- Content: Step-by-step patterns, code examples, anti-patterns
- Examples: `java-spring-boot-playbook.md`, `typescript-nestjs-playbook.md`

---

## Quality Gate Examples

### M0 (Foundation) Exit Criteria
- [ ] REASONS canvas complete and reviewed
- [ ] Architecture decisions (ADRs 1-N) documented
- [ ] Agent-context scaffolding created
- [ ] Quality gates defined for M1-M6
- [ ] Known pitfalls documented (3+)
- [ ] Playbook created (if new stack)
- [ ] Team trained on SPDD workflow

### M1 (Infrastructure) Exit Criteria
- [ ] DEV environment deployed and tested
- [ ] QA environment configured
- [ ] External provider setup complete (OAuth2, APIs, etc.)
- [ ] Smoke tests passing
- [ ] Documentation updated
- [ ] Team has access and understands setup

### M2-M5 (Feature) Exit Criteria
- [ ] Assigned test cases passing (100%)
- [ ] Code review approved by tech lead
- [ ] All ADRs referenced in PR description
- [ ] Known pitfalls checklist completed
- [ ] Coverage maintained (> 80%)
- [ ] Performance benchmarks met

### M6 (Integration) Exit Criteria
- [ ] All acceptance criteria met (15 test cases)
- [ ] All edge cases handled (7 edge cases)
- [ ] Security assessment clean (no high/critical)
- [ ] Performance load testing passed
- [ ] Runbook documented
- [ ] Team trained

---

## Anti-Patterns to Avoid

### ❌ Canvas Drift
- Writing canvas, then changing approach mid-implementation without updating canvas
- **Fix**: Update REASONS canvas before modifying approach; document rationale

### ❌ Missing ADRs
- Making major decisions without documenting in architecture-decisions.md
- **Fix**: For each decision in the A section, create corresponding ADR

### ❌ Skipping Quality Gates
- Implementing without checking entry criteria (dependencies ready? infrastructure ready?)
- **Fix**: Review quality-gates.md before starting each milestone

### ❌ Generic Playbooks
- Creating playbooks so generic they don't help (e.g., "write a function")
- **Fix**: Include concrete examples, anti-patterns, testing patterns specific to your stack

### ❌ Ignoring Known Pitfalls
- Hitting the same bugs that other teams already discovered
- **Fix**: Read known-pitfalls.md before starting work; add new pitfalls after solving them

### ❌ Canvas-Only (No Sync)
- Keeping beautiful canvases that drift from actual implementation
- **Fix**: Run sync.sh regularly or ask Copilot: "Are the canvases still accurate?" and update if needed

---

## Tips for Copilot Success

### 1. Load Context Upfront
Instead of: *"Create OAuth2 component"*
Do: *"Based on FEAT-ECQ-OAUTH2 canvas, ADR-001 (email verification strategy), and the java-spring-boot-playbook, implement the AccountLinkingService..."*

### 2. Reference Architecture Decisions
Include ADR IDs in Copilot prompts to maintain consistency:
- *"Following ADR-003 (state preservation), implement RedirectStateService..."*
- *"This implementation should follow patterns in ADR-002..."*

### 3. Use Playbooks for Pattern Consistency
Tell Copilot which playbook to follow:
- *"Generate tests using patterns from java-spring-boot-playbook.md"*
- *"Structure this service class following the patterns in the playbook"*

### 4. Review Canvas After Each Milestone
Ask Copilot: *"Compare our actual implementation to the REASONS canvas. Did we deviate? Should we update the canvas or did we discover a better approach?"*

### 5. Keep Known-Pitfalls Updated
After solving a novel bug: *"Add this pattern to known-pitfalls.md so we don't repeat it"*

---

## Links

- [Architecture](../../docs/architecture.md) — System design and reasoning
- [Workflow](../../docs/workflow.md) — Step-by-step usage guide
- [Design Decisions](../../docs/design-decisions.md) — Why this framework exists
- [Java/Spring Boot Usage](../../docs/java-spring-boot-usage.md) — Language-specific guide
- [Examples](../../examples/) — Reference projects

---

**Last Updated**: 2026-06-04  
**Version**: 1.0  
**For**: Copilot (Copilot Chat, Claude with VS Code)  
**Scope**: Project-level, team-shared instructions
