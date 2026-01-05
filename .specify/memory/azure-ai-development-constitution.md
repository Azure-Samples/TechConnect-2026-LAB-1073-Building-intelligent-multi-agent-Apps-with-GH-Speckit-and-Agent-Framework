# Azure Development Constitution

## Core Principles

### 0. Azure Development Prerequisites

**All Azure-related development MUST verify prerequisites before code generation or deployment**:

- Azure CLI MUST be installed and up-to-date (`az --version` to verify)
- User MUST be authenticated via `az login` with valid subscription access
- Azure MCP best practices tools MUST be invoked before:
  - Generating Azure-related code (invoke with resource=`general`, action=`code-generation`)
  - Deploying to Azure (invoke with resource=`general`, action=`deployment`)
  - Working with Azure Functions (invoke with resource=`azurefunctions`, action=`code-generation` or `deployment`)
  - Working with Azure Static Web Apps (invoke appropriate best practices tool)
- Azure AI Toolkit MCP tools (prefixed with `aitk-`) MUST be invoked for:
  - AI agent code generation (`aitk-get_agent_code_gen_best_practices`)
  - AI agent evaluation code (`aitk-get_evaluation_code_gen_best_practices`)
  - Agent runner setup (`aitk-evaluation_agent_runner_best_practices`)
  - AI model guidance (`aitk-get_ai_model_guidance`)
  - Tracing implementation (`aitk-get_tracing_code_gen_best_practices`)

**Rationale**: Azure MCP tools provide up-to-date official guidance that prevents common misconfigurations, security issues, and deployment failures. Azure AI Toolkit tools ensure agents follow Microsoft's latest patterns for Agent Framework, evaluation, and observability. Verifying prerequisites prevents wasted development time on environments that cannot authenticate or deploy.

### I. Service Discovery & Dynamic Configuration

**No hardcoded URLs or ports are permitted**. All service communication MUST use dynamic configuration mechanisms:

- Services MUST read connection strings and endpoints from environment variables
- Backend MUST read allowed origins from environment for CORS
- Use environment-aware URL schemes (http vs https based on deployment context)
- Configuration MUST support local development and Azure deployment without code changes

**Rationale**: Hardcoded configuration breaks when deploying to Azure Container Apps, App Services, or other managed services. Dynamic configuration ensures portability across environments without code changes.

### II. Authentication & Authorization

**All Azure services MUST use Microsoft Entra ID (Azure AD) authentication patterns**:

- Local development: `DefaultAzureCredential` with `az login`
- Azure deployment: Managed Identity (system-assigned or user-assigned)
- Never commit credentials, connection strings, or API keys to source control
- Use Azure Key Vault for secrets management in production
- Python services: Use `azure-identity` package with `DefaultAzureCredential`
- .NET services: Use `Azure.Identity` package with `DefaultAzureCredential`

**Rationale**: Credential-based authentication is a security vulnerability. Managed Identity provides secure, zero-credential authentication within Azure environments.

### III. AI Agent Architecture with Azure AI Foundry

**AI agents MUST use Microsoft Agent Framework with Azure AI Foundry integration**:

- MUST authenticate via `DefaultAzureCredential` (requires `az login` locally)
- MUST follow Azure best practices obtained via Azure MCP tools before code generation
- MUST invoke Azure AI Toolkit MCP tools (`aitk-get_agent_code_gen_best_practices`) before agent code generation
- MUST use Azure AI Foundry for model deployment and management
- MUST implement health check endpoints at `/health`
- Agent tools MUST be configured in Azure AI Foundry, not just code
- File search agents MUST pass `tool_resources` to thread creation

**Model Selection**:

- Use `aitk-get_ai_model_guidance` tool for model recommendations
- Consider GitHub Models for development (models.inference.ai.azure.com)
- Use Azure OpenAI Service for production deployments
- Document model choices and host preferences in architecture decisions

**Rationale**: Azure AI Foundry provides centralized agent management, model versioning, and observability. Agent Framework best practices prevent common pitfalls with tool configuration and file search.

### IV. Observability & Telemetry

**All Azure services MUST emit structured telemetry**:

- **Development**: Use local observability tools (Aspire Dashboard, console logging)
- **Production**: Azure Application Insights MUST be enabled
- Use OpenTelemetry for instrumentation (portable across environments)
- Python services: Use standard `logging` module with structured output
- .NET services: Use `ILogger` with log levels
- Health check endpoints required: `/health` returning `{ Status, Timestamp }`
- Agents MUST log tool invocations and run steps for debugging

**Application Insights Requirements**:

- Connection string MUST be injected via environment variable
- Use `APPLICATIONINSIGHTS_CONNECTION_STRING` standard
- Configure sampling to control costs in high-traffic scenarios
- Enable distributed tracing for multi-service requests

**Rationale**: Distributed applications are impossible to debug without unified observability. Application Insights provides production-grade monitoring, alerting, and diagnostics.

### V. Environment-Aware Behavior

**Services MUST adapt behavior based on deployment environment**:

- **Development/Local**:
  - Mock data enabled for zero-dependency development
  - Detailed error messages and stack traces
  - Swagger/OpenAPI UI exposed
  - HTTP endpoints acceptable

- **Production/Azure**:
  - Mock data disabled
  - Generic error messages (log details to Application Insights)
  - OpenAPI only if explicitly required
  - HTTPS enforcement via Azure service configuration
  - Application Insights enabled
  - Managed Identity for authentication

**Configuration Strategy**:

- Use single environment flag or detection mechanism
- Avoid separate configuration files for each environment
- Leverage Azure App Configuration for dynamic settings

**Rationale**: Single-point environment control prevents configuration drift and ensures consistent behavior expectations. Developers cannot accidentally deploy development settings to production.

### VI. Bicep & Infrastructure as Code

**Azure resources MUST be defined using Bicep templates**:

- Use Azure Verified Modules (AVM) where available
- Invoke `azure_bicep-get_azure_verified_module` before writing raw Bicep
- Use `mcp_bicep_experim_get_bicep_best_practices` for authoring guidance
- Store Bicep templates in source control
- Use parameters and variables for environment-specific values
- Tag all resources with project, environment, and cost center metadata

**Deployment Strategy**:

- Production: Use CI/CD pipeline with `az deployment group create`
- Use Azure Resource Manager (ARM) parameter files for environment-specific values
- Implement resource naming conventions (e.g., `{project}-{service}-{environment}`)

**Rationale**: Bicep provides type-safe, declarative infrastructure that prevents manual configuration drift. Azure Verified Modules ensure best practices and security compliance.

### IX. Container Registry & Image Management

**Container images MUST follow Azure Container Registry (ACR) best practices**:

- Use ACR for private images (not Docker Hub for production)
- Enable ACR geo-replication for global deployments
- Use ACR Tasks for automated image builds
- Scan images for vulnerabilities using Defender for Cloud
- Use Managed Identity for ACR authentication (no admin credentials)
- Tag images with semantic versions and git commit SHAs

**Multi-stage Build Requirements**:

- Separate build and runtime stages
- Use minimal base images (alpine, distroless)
- Copy only necessary artifacts to final stage
- Set non-root user for container execution

**Rationale**: ACR provides secure, performant image storage with integrated security scanning. Multi-stage builds minimize attack surface and deployment size.

### X. Cost Management & Optimization

**Azure resource provisioning MUST consider cost optimization**:

- Use consumption-based pricing where possible (Azure Functions, Container Apps)
- Right-size compute resources (don't default to premium tiers)
- Use Azure Advisor recommendations for optimization
- Implement auto-scaling policies based on metrics
- Use Azure Reservations for predictable workloads (1-3 year commitments)
- Tag all resources for cost allocation and chargebacks
- Monitor spending with Azure Cost Management + Billing

**Development Cost Controls**:

- Use free tiers for development (App Service, Functions, Cosmos DB)
- Implement automatic shutdown for non-production environments
- Use shared resources across development environments where possible

**Rationale**: Azure costs can escalate without proper governance. Proactive cost management prevents budget overruns.

## Development Workflow

### Azure Prerequisites Checklist

Before ANY Azure-related development:

```bash
# Verify Azure CLI is installed
az --version

# Login to Azure
az login

# Verify subscription access
az account show

# Set default subscription (if multiple)
az account set --subscription "subscription-name-or-id"
```

### Azure Best Practices Invocation

Before code generation or deployment, invoke appropriate tools:

```bash
# General Azure code generation
# Invoke: mcp_azure_mcp_get_bestpractices
# Parameters: resource="general", action="code-generation"

# General Azure deployment
# Invoke: mcp_azure_mcp_get_bestpractices
# Parameters: resource="general", action="deployment"

# Azure Functions development
# Invoke: mcp_azure_mcp_get_bestpractices
# Parameters: resource="azurefunctions", action="code-generation|deployment"

# AI Agent development
# Invoke: aitk-get_agent_code_gen_best_practices

# AI Model guidance
# Invoke: aitk-get_ai_model_guidance
# Parameters: preferredHost=["GitHub"|"AzureAIFoundry"|"OpenAI"|etc]

# Evaluation code
# Invoke: aitk-get_evaluation_code_gen_best_practices

# Tracing implementation
# Invoke: aitk-get_tracing_code_gen_best_practices
```

### AI Agent Development on Azure

1. **Verify Azure prerequisites**: Run `az --version` and `az login`
2. **Invoke Azure AI Toolkit MCP tools**: Use `aitk-get_agent_code_gen_best_practices`
3. **Invoke Azure best practices**: Use Azure MCP tools for guidance
4. **Authentication**: Verify `az login` before testing
5. **Local testing**: Use orchestration tool or standalone testing as appropriate
6. **Deployment**: Build container, push to ACR, deploy to Container Apps/AKS

### Infrastructure Deployment

1. **Review Bicep best practices**: Invoke `mcp_bicep_experim_get_bicep_best_practices`
2. **Check for Azure Verified Modules**: Invoke `azure_bicep-get_azure_verified_module` for each resource type
3. **Write/update Bicep templates**: Use parameters for environment-specific values
4. **Validate templates**: `az deployment group validate`
5. **Preview changes**: `az deployment group what-if`
6. **Deploy**: `az deployment group create` or via CI/CD pipeline
7. **Verify**: Check Azure Portal and Application Insights

### Compliance Checks

Before Azure deployment, verify:

- [ ] Azure CLI installed and user authenticated (`az login`)
- [ ] Azure MCP best practices invoked for all Azure-related code/deployments
- [ ] Azure AI Toolkit MCP tools invoked for all agent code generation
- [ ] No hardcoded URLs, ports, or credentials in code
- [ ] Managed Identity configured for Azure service authentication
- [ ] Application Insights configured for production telemetry
- [ ] Health check endpoints implemented on all services
- [ ] Bicep templates use Azure Verified Modules where available
- [ ] Resources tagged with project, environment, cost center
- [ ] Python services use `uv` for dependencies
- [ ] Container images use multi-stage builds

## Governance

**This constitution defines mandatory Azure development patterns**. Deviations require:

1. Explicit justification documented in architecture decision records
2. Risk assessment for security, cost, and maintainability impacts
3. Approval from architecture/platform team

**Amendment Process**:

1. Propose change with rationale in architecture forum
2. Document impact on existing deployments and patterns
3. Update constitution version using semantic versioning:
   - **MAJOR**: Removes/redefines principle, breaks backward compatibility
   - **MINOR**: Adds principle, expands guidance, new mandatory section
   - **PATCH**: Clarifies wording, fixes typos, non-semantic refinements
4. Update related documentation and templates
5. Commit message: `docs: amend azure-constitution to vX.Y.Z (summary)`

**Compliance Verification**:

- Code reviews MUST validate constitution adherence
- Automated checks via CI/CD pipeline (linting, security scanning)
- Regular architecture audits of deployed resources
- No production deployment without compliance sign-off

**Related Documentation**:

- Official Azure best practices: Use `mcp_azure_mcp_get_bestpractices` tool
- Azure AI Toolkit guidance: Use `aitk-*` prefixed tools
- Microsoft Learn documentation: Use `mcp_microsoft_doc_microsoft_docs_search`
- Azure architecture patterns: Azure Architecture Center

**Version**: 1.0.0 | **Ratified**: 2025-11-18 | **Last Amended**: 2025-11-18