---
name: Framework Enhancement
about: Improve SDLC-SPDD Orchestrator framework patterns, templates, or documentation
title: "[FRAMEWORK] "
labels: ["enhancement", "framework"]
assignees: ''

---

## Enhancement: Complete Language-Specific Playbooks & Examples

### Description

The orchestrator framework should provide complete, reusable playbooks and example projects that AI tools (Cursor, Copilot, Claude) can reference when using SPDD with different technology stacks.

### Motivation

Currently, the framework assumes Java/Spring Boot or requires users to create custom playbooks. This limits adoption and discoverability. Teams new to SPDD should be able to:
1. Pick their tech stack
2. Reference language-specific playbooks
3. See complete example projects
4. Understand Copilot/Cursor equivalents for key workflows

### Work Items

#### 1. Add Language-Specific Playbooks
- **Deliverable**: `agent-context/playbooks/` directory with templates for common stacks
- **Items**:
  - [ ] `java-spring-boot-playbook.md` (existing, may need enhancement)
  - [ ] `typescript-nestjs-playbook.md` (async, DI, testing patterns)
  - [ ] `python-fastapi-playbook.md` (async, SQLAlchemy, testing patterns)
  - [ ] `dotnet-aspnetcore-playbook.md` (.NET Core patterns)
  - [ ] `go-echo-playbook.md` (Go patterns, if applicable)
- **Content per playbook**:
  - Project structure conventions
  - Service layer patterns
  - Data access patterns
  - Error handling patterns
  - Testing pyramid (unit, integration, E2E)
  - Common configuration patterns
  - Logging & observability patterns
  - Authentication/Authorization patterns
  - Code review checklist specific to language

#### 2. Create Complete Example Projects
- **Deliverable**: `examples/` folder with end-to-end SPDD workflows
- **Items**:
  - [ ] **Spring Boot Example** (existing, audit for completeness)
    - REASONS canvas (FEAT-*.md)
    - Spike canvas (SPIKE-*.md)
    - Tasks (spdd/tasks/)
    - Completed implementation
    - Test coverage
    - Architecture decisions (ADRs)
  - [ ] **TypeScript/NestJS Example**
    - Same structure as Spring Boot
    - Auth service or API gateway pattern
    - REST + async patterns
  - [ ] **Python/FastAPI Example**
    - Data pipeline or ML service pattern
    - Async concurrency patterns
  - [ ] **Migration/Refactoring Example**
    - Large codebase refactoring SPDD canvas
    - Phased migration approach
    - Known pitfalls specific to refactoring

#### 3. Update Documentation for All AI Tools
- **Deliverable**: `docs/ai-tool-usage.md` (new, consolidates Cursor + Copilot + Claude)
- **Current**: `docs/cursor-usage.md` (Cursor-specific)
- **New**: Unified guide covering:
  - [ ] Cursor workflow with `/sdlc-spdd-*` commands
  - [ ] Copilot workflow (chat-based planning)
  - [ ] Claude/ChatGPT workflow (document-based)
  - [ ] Common patterns across tools
  - [ ] Tool-specific advantages/limitations
  - [ ] How to structure prompts for each tool

#### 4. Update Main Documentation
- **Deliverable**: Updated docs/ with clearer onboarding
- **Items**:
  - [ ] `docs/README.md` — Quick-start decision tree (What's my stack? → Link to playbook/example)
  - [ ] `docs/architecture.md` — Clarify framework design, REASONS Canvas rationale
  - [ ] `docs/workflow.md` — Generic workflow that applies to all stacks

#### 5. Version Control Integration
- **Deliverable**: CHANGELOG entry, Git commit history
- **Items**:
  - [ ] Update `CHANGELOG.md` with new playbooks & examples
  - [ ] Commit with message: `feat(framework): add language-specific playbooks and examples`
  - [ ] Tag release (e.g., `v1.1.0`)

### Acceptance Criteria

- [ ] Each playbook has 3+ concrete code examples specific to its language
- [ ] Each example project has complete SPDD artifacts (canvas, tasks, decisions, implementation)
- [ ] Documentation (README, workflow guides) is discoverable from root README
- [ ] AI tool usage guide covers Cursor, Copilot, and Claude equivalently
- [ ] No project-specific or company-specific examples (all generic/fictional)
- [ ] Test coverage exists for example projects (> 70%)
- [ ] README updated to link to new playbooks and examples

### Success Metrics

- Reduced time for new users to onboard (target: 30 min to first canvas)
- Increased number of technology stacks supported (target: 5+)
- Playbooks cited in user projects (measured by GitHub stars/forks)
- Fewer "How do I apply SPDD to my stack?" questions

### Non-Goals

- Supporting every possible technology stack (prioritize top 5)
- Replacing official framework documentation (e.g., Spring Docs)
- Creating production-grade example services (MVP scope is fine)

### Notes

- Examples should be intentionally simple (< 500 lines per service)
- Playbooks should reference official docs when language/framework-specific
- Keep examples in separate subdirectories: `examples/{language}-{framework}-{domain}/`
- Iterate playbooks based on user feedback

---

**Related**: None (foundational enhancement)  
**Priority**: Medium (nice-to-have, but significantly improves usability)  
**Estimated Effort**: 60-80 hours (could be split across multiple PRs)
