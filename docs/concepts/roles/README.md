# Roles in Software Development

Understanding the different responsibilities in software development helps you work effectively with AI assistants.

## Why Roles Matter

Even in solo projects, these responsibilities exist. Understanding them helps you:
- Ask better questions to AI
- Structure your work logically
- Catch issues at the right time
- Communicate with teams

## The Core Roles

### Analyst

**Question**: What do we need to build?

**Responsibilities**:
- Understand business requirements
- Clarify ambiguous requests
- Define scope and boundaries
- Write user stories
- Set acceptance criteria

**Output**:
- Requirements document
- User stories
- Acceptance criteria

**In AI context**:
```
"Analyze this feature request. What are the requirements?
What questions should we clarify? What's in scope vs out?"
```

### Architect

**Question**: How should the system work?

**Responsibilities**:
- Design system structure
- Choose technologies
- Define component boundaries
- Ensure quality attributes (performance, security)
- Document decisions (ADRs)

**Output**:
- Architecture diagrams
- Component specifications
- Technology decisions
- ADRs

**In AI context**:
```
"Design the architecture for this feature.
What components are needed? How do they interact?
What are the trade-offs of this approach?"
```

### Tech Lead / Team Lead

**Question**: How do we organize the work?

**Responsibilities**:
- Break work into tasks
- Sequence tasks logically
- Identify dependencies
- Review code quality
- Coordinate team members

**Output**:
- Implementation plan
- Task breakdown
- Code review results

**In AI context**:
```
"Break this architecture into implementable tasks.
What order should we do them? What are the dependencies?"
```

### Developer

**Question**: How do we build it?

**Responsibilities**:
- Write code
- Write tests
- Follow patterns and standards
- Document code
- Fix bugs

**Output**:
- Production code
- Unit tests
- Code documentation

**In AI context**:
```
"Implement this component following TDD.
Write tests first, then implementation.
Follow the existing code patterns."
```

### QA / Quality Assurance

**Question**: Does it work correctly?

**Responsibilities**:
- Verify acceptance criteria
- Run test suites
- Check coverage
- Find edge cases
- Report bugs

**Output**:
- Test results
- Bug reports
- Coverage reports

**In AI context**:
```
"Review this implementation against the requirements.
Check all acceptance criteria. Run tests.
What edge cases are missing?"
```

### DevOps / Platform Engineer

**Question**: How do we deliver it?

**Responsibilities**:
- Set up CI/CD pipelines
- Configure environments
- Manage deployments
- Handle infrastructure
- Plan rollbacks

**Output**:
- Deployment scripts
- Pipeline configuration
- Infrastructure as code
- Runbooks

**In AI context**:
```
"Create a deployment plan for this feature.
Include rollback procedure.
What environment variables are needed?"
```

## Additional Roles

### Security Engineer

**Question**: Is it safe?

**Responsibilities**:
- Threat modeling
- Security review
- Penetration testing
- Auth/authz design
- Compliance verification

### SRE (Site Reliability Engineer)

**Question**: Is it reliable?

**Responsibilities**:
- Define SLOs/SLIs
- Set up monitoring
- Create alerts
- Write runbooks
- Incident response

### Data Engineer

**Question**: How do we handle data?

**Responsibilities**:
- Data modeling
- ETL pipelines
- Data quality
- Schema management

## How Roles Map to AI Modes

### Solo Mode
One AI handles all roles implicitly through conversation:
```
You: "Add password reset"
AI: [Analyst] What are the requirements?
AI: [Architect] Here's the design...
AI: [Developer] Here's the implementation...
AI: [QA] Tests pass, coverage is 85%...
```

### Structured Mode
You explicitly guide AI through commands:
```
/idea (Requirements): "Gather requirements interactively"
/design (Planning): "Design workstreams with architecture decisions"
/build (Implementation): "Implement with TDD"
/review (Quality): "Review and verify quality"
```

### Multi-Agent Mode (Legacy)
Different sessions/prompts for different roles (deprecated, use slash commands):
```
Session 1: Analyst prompt → requirements.md
Session 2: Architect prompt → architecture.md
Session 3: Developer prompt → code
...
```

**Note:** Current SDP uses slash commands (`/idea`, `/design`, `/build`, `/review`) instead of role-based prompts.

## Anti-patterns

### Skipping Analysis
```
# Bad
"Just write the code for user registration"

# Good
"Let's first understand: what fields are required?
What validation rules? What happens after registration?"
```

### Ignoring Architecture
```
# Bad
"Add this quick hack to make it work"

# Good
"How does this fit into the existing architecture?
Are we creating technical debt?"
```

### No Quality Check
```
# Bad
"Looks good, ship it"

# Good
"Let's verify: all acceptance criteria met?
Tests passing? Edge cases covered?"
```

## Practical Tips

1. **Use slash commands for role-based workflow**
   - `/idea` — Requirements gathering (Analyst role)
   - `/design` — Architecture planning (Architect role)
   - `/build` — Implementation (Developer role)
   - `/review` — Quality verification (QA role)

2. **Each command has role-specific focus**
   ```
   /design — Focus on Clean Architecture boundaries
   /build — Focus on TDD and code quality
   /review — Focus on acceptance criteria and coverage
   ```

3. **Use command-specific checklists**
   - /idea: Are requirements clear and testable?
   - /design: Are boundaries respected? Architecture decisions documented?
   - /build: Are tests written first? Coverage ≥80%?
   - /review: Are acceptance criteria met? All quality gates passed?
