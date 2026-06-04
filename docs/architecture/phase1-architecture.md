PlanForge
Phase 1 Architecture
Document Status
Version 3.0
 
1. Architecture Objective
The objective of Phase 1 is to transform a business Epic into a validated and approved Feature Set while demonstrating organizational learning, workflow orchestration, and enterprise integration.
 
2. High-Level Workflow
User
↓
Epic Submission
↓
Knowledge Retrieval
↓
Feature Generation
↓
Feature Validation
↓
Feature Review
↓
Feature-Level Decisions
├── Approved Features │ │ Retain Current Version │ └── Rejected Features ↓ Capture Feedback ↓ Knowledge Retrieval ↓ Feature Regeneration
↓
Merge Approved Features + Revised Features
↓
All Features Approved?
├── No │ │ Return to Feature Review │ └── Yes ↓ Publish to Confluence ↓ Store Learning Artifacts ↓ End
 
3. Architectural Principles
Principle 1
Human approval is mandatory before publication.
Principle 2
Approved Features are never regenerated automatically.
Principle 3
Rejected Features require reviewer feedback.
Principle 4
All versions are retained.
Principle 5
The system continuously learns from approved and rejected artifacts.
Principle 6
Workflow state is centrally managed.
 
4. Technology Components
UI Layer
Streamlit
Responsibilities:
•	Epic entry
•	Feature review
•	Feedback capture
•	Approval workflow
 
Workflow Layer
LangGraph
Responsibilities:
•	State management
•	Routing
•	Approval loops
•	Version management
 
LLM Layer
OpenAI GPT
Responsibilities:
•	Feature generation
•	Feature regeneration
•	Feedback interpretation
 
Validation Layer
Pydantic
Responsibilities:
•	Schema validation
•	Output validation
 
Enterprise Publishing Layer
Confluence Integration
Responsibilities:
•	Publish approved Features
•	Maintain traceability
 
Organizational Learning Layer
ChromaDB
Responsibilities:
•	Store approved Feature Sets
•	Store approved Features
•	Store rejected Features
•	Store reviewer feedback
•	Similarity search
•	Retrieval support
 
5. LangGraph Nodes
Node 1
Epic Intake
Outputs:
•	Epic Object
 
Node 2
Knowledge Retrieval
Inputs:
•	Epic
•	Reviewer Feedback (optional)
Outputs:
•	Similar Approved Features
•	Similar Approved Feature Sets
•	Similar Rejected Features
•	Associated Feedback
 
Node 3
Feature Generation
Inputs:
•	Epic
•	Retrieved Context
Outputs:
•	Generated Feature Set
 
Node 4
Feature Validation
Inputs:
•	Generated Feature Set
Outputs:
•	Validated Feature Set
 
Node 5
Feature Review
Inputs:
•	Validated Feature Set
Outputs:
•	Feature Decisions
•	Reviewer Feedback
 
Node 6
Feature Regeneration
Inputs:
•	Rejected Features
•	Reviewer Feedback
•	Retrieved Context
Outputs:
•	Revised Features
 
Node 7
Confluence Publisher
Inputs:
•	Approved Feature Set
Outputs:
•	Published Artifact
 
Node 8
Organizational Learning Writer
Inputs:
•	Feature Set
•	Feature Decisions
•	Reviewer Feedback
•	Approval Outcome
Outputs:
•	Stored Artifacts
 
6. Artifact Model
Artifacts are the primary storage unit.
Each artifact contains:
•	Epic
•	Feature Set
•	Approval Status
•	Reviewer Feedback
•	Version Information
•	Metadata
 
7. Feature Model
Each Feature contains:
•	Feature ID
•	Feature Name
•	Description
•	Business Value
•	Acceptance Criteria
•	Approval Status
•	Reviewer Feedback
•	Version Number
 
8. Retrieval Strategy
New Epic Processing
Retrieve:
•	Similar Approved Feature Sets
•	Similar Approved Features
Purpose:
Improve initial generation quality.
 
Feature Regeneration
Retrieve:
•	Rejected Feature
•	Reviewer Feedback
•	Similar Approved Features
•	Similar Rejected Features and Feedback
Purpose:
Improve targeted revisions.
 
9. Workflow State
State contains:
•	Epic
•	Feature Set
•	Feature Decisions
•	Reviewer Feedback
•	Validation Results
•	Version History
•	Retrieved Context
•	Publication Status
 
10. Version Management
Feature-level versioning:
Feature A v1 → Approved
Feature B v1 → Approved
Feature C v1 → Rejected
Feature C v2 → Rejected
Feature C v3 → Approved
Feature Set version history is also maintained.
 
11. Observability
Track:
•	Node execution
•	State transitions
•	Retrieval activity
•	Validation outcomes
•	Approval decisions
•	Regeneration cycles
•	Publication events
 
12. Future Extensions
•	User Story generation
•	Backlog Item generation
•	Advanced RAG
•	Multi-reviewer workflows
•	Additional enterprise integrations