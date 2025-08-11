# Advanced Project Management Automation Script
# Enhanced version with comprehensive error handling, logging, and features

param(
    [switch]$DryRun,
    [switch]$Verbose,
    [string]$LogPath = ".\project_automation_log.txt"
)

# Initialize logging
function Write-Log {
    param($Message, $Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] [$Level] $Message"
    Write-Host $logEntry -ForegroundColor $(switch($Level) {
        "ERROR" { "Red" }
        "WARNING" { "Yellow" }
        "SUCCESS" { "Green" }
        "INFO" { "Cyan" }
        default { "White" }
    })
    Add-Content -Path $LogPath -Value $logEntry
}

# Enhanced project mappings with categories and descriptions
$projects = @{
    "aiResourceDirectory" = @{
        name = "resourcehub-ai"
        displayName = "ResourceHub AI"
        category = "AI Tools"
        description = "Comprehensive AI resource management platform"
        keywords = @("ai", "resources", "directory", "platform")
    }
    "APPYness2" = @{
        name = "appflow-pro"
        displayName = "AppFlow Pro"
        category = "Development Tools"
        description = "Advanced application workflow management system"
        keywords = @("app", "workflow", "development", "automation")
    }
    "bigFaith" = @{
        name = "faithconnect-platform"
        displayName = "FaithConnect"
        category = "Social Platform"
        description = "Community platform for faith-based connections"
        keywords = @("faith", "community", "social", "platform")
    }
    "blackBoxAI" = @{
        name = "deepmind-studio"
        displayName = "DeepMind Studio"
        category = "AI Development"
        description = "Advanced AI development and experimentation platform"
        keywords = @("ai", "machine-learning", "development", "studio")
    }
    "directoryStructureGenerator" = @{
        name = "structgen-pro"
        displayName = "StructGen Pro"
        category = "Development Tools"
        description = "Intelligent directory structure generation tool"
        keywords = @("directory", "structure", "generator", "organization")
    }
    "DuplicateCleanerPro" = @{
        name = "cleanspace-pro"
        displayName = "CleanSpace Pro"
        category = "System Utilities"
        description = "Advanced duplicate file detection and cleanup system"
        keywords = @("duplicate", "cleaner", "system", "optimization")
    }
    "dyadiaGame" = @{
        name = "dyadia-quest"
        displayName = "Dyadia Quest"
        category = "Gaming"
        description = "Interactive adventure gaming platform"
        keywords = @("game", "adventure", "interactive", "quest")
    }
    "ebayWebApp" = @{
        name = "auctionmaster-pro"
        displayName = "AuctionMaster Pro"
        category = "E-commerce"
        description = "Professional eBay auction management platform"
        keywords = @("ebay", "auction", "e-commerce", "management")
    }
    "eCommerceWizard" = @{
        name = "commercecore-platform"
        displayName = "CommerceCore"
        category = "E-commerce"
        description = "Complete e-commerce solution platform"
        keywords = @("e-commerce", "platform", "retail", "online-store")
    }
    "exclusionExtension" = @{
        name = "filtershield-extension"
        displayName = "FilterShield"
        category = "Browser Extensions"
        description = "Advanced content filtering browser extension"
        keywords = @("filter", "extension", "browser", "security")
    }
    "Explainer" = @{
        name = "claritybot-ai"
        displayName = "ClarityBot AI"
        category = "AI Tools"
        description = "AI-powered explanation and clarification assistant"
        keywords = @("ai", "explanation", "clarification", "assistant")
    }
    "extensionListProject" = @{
        name = "extensioncentral-hub"
        displayName = "ExtensionCentral"
        category = "Browser Extensions"
        description = "Centralized browser extension management platform"
        keywords = @("extension", "browser", "management", "hub")
    }
    "financeApp" = @{
        name = "wealthtracker-pro"
        displayName = "WealthTracker Pro"
        category = "Finance"
        description = "Professional financial tracking and analytics platform"
        keywords = @("finance", "wealth", "tracking", "analytics")
    }
    "functionCalls" = @{
        name = "apibridge-toolkit"
        displayName = "APIBridge Toolkit"
        category = "Development Tools"
        description = "Advanced API integration and function call management"
        keywords = @("api", "integration", "functions", "toolkit")
    }
    "googleSearchExtension" = @{
        name = "searchboost-pro"
        displayName = "SearchBoost Pro"
        category = "Browser Extensions"
        description = "Enhanced Google search optimization extension"
        keywords = @("search", "google", "optimization", "extension")
    }
    "hotkeyManagementTool" = @{
        name = "keymaster-pro"
        displayName = "KeyMaster Pro"
        category = "System Utilities"
        description = "Advanced hotkey and keyboard shortcut management"
        keywords = @("hotkey", "keyboard", "shortcuts", "productivity")
    }
    "hotkeyManagementTool2" = @{
        name = "keymaster-elite"
        displayName = "KeyMaster Elite"
        category = "System Utilities"
        description = "Elite hotkey management with advanced features"
        keywords = @("hotkey", "keyboard", "shortcuts", "elite")
    }
    "IconIQ" = @{
        name = "iconiq-studio"
        displayName = "IconIQ Studio"
        category = "Design Tools"
        description = "Intelligent icon design and management studio"
        keywords = @("icon", "design", "studio", "graphics")
    }
    "inventoryFinder" = @{
        name = "stocksense-pro"
        displayName = "StockSense Pro"
        category = "Business Tools"
        description = "Intelligent inventory tracking and management system"
        keywords = @("inventory", "stock", "management", "business")
    }
    "julia_anniversary_project_src" = @{
        name = "lovekeeper-memories"
        displayName = "LoveKeeper"
        category = "Personal Tools"
        description = "Romantic anniversary and memory management app"
        keywords = @("anniversary", "memories", "romance", "personal")
    }
    "marketSage" = @{
        name = "marketsage-ai"
        displayName = "MarketSage AI"
        category = "Finance"
        description = "AI-powered market analysis and trading insights"
        keywords = @("market", "trading", "ai", "finance")
    }
    "microSaaS" = @{
        name = "microlaunch-platform"
        displayName = "MicroLaunch"
        category = "SaaS Tools"
        description = "Micro-SaaS development and launch platform"
        keywords = @("saas", "micro", "launch", "platform")
    }
    "narrativeEngineReal" = @{
        name = "storyforge-ai"
        displayName = "StoryForge AI"
        category = "AI Tools"
        description = "AI-powered narrative and story generation engine"
        keywords = @("story", "narrative", "ai", "content")
    }
    "nextGenProductvityPlatform" = @{
        name = "productivitymax-suite"
        displayName = "ProductivityMax"
        category = "Productivity"
        description = "Next-generation productivity enhancement platform"
        keywords = @("productivity", "platform", "efficiency", "suite")
    }
    "noCodeAppBuilder" = @{
        name = "nocodestudio-builder"
        displayName = "NoCodeStudio"
        category = "Development Tools"
        description = "Visual no-code application development platform"
        keywords = @("no-code", "builder", "visual", "development")
    }
    "noCodeAppBuilderPromptLibraryAndSuite" = @{
        name = "nocodemaster-suite"
        displayName = "NoCodeMaster Suite"
        category = "Development Tools"
        description = "Comprehensive no-code development suite with prompt library"
        keywords = @("no-code", "suite", "prompts", "development")
    }
    "nokode" = @{
        name = "nokode-engine"
        displayName = "NoKode Engine"
        category = "Development Tools"
        description = "Advanced no-code development engine"
        keywords = @("no-code", "engine", "development", "platform")
    }
    "noteApp" = @{
        name = "notevault-pro"
        displayName = "NoteVault Pro"
        category = "Productivity"
        description = "Professional note-taking and knowledge management"
        keywords = @("notes", "knowledge", "management", "productivity")
    }
    "nyteOwls" = @{
        name = "nyteowls-hub"
        displayName = "NyteOwls Hub"
        category = "Social Platform"
        description = "Night-time productivity and social hub"
        keywords = @("productivity", "social", "community", "hub")
    }
    "omni_organizer" = @{
        name = "omniorganizer-pro"
        displayName = "OmniOrganizer Pro"
        category = "Productivity"
        description = "Universal organization and task management system"
        keywords = @("organization", "tasks", "management", "productivity")
    }
    "omniSort" = @{
        name = "sortgenius-tool"
        displayName = "SortGenius"
        category = "System Utilities"
        description = "Intelligent file and data sorting utility"
        keywords = @("sorting", "files", "organization", "utility")
    }
    "PassiveIncomeAutomator" = @{
        name = "incomeflow-ai"
        displayName = "IncomeFlow AI"
        category = "Finance"
        description = "AI-powered passive income automation platform"
        keywords = @("passive-income", "automation", "ai", "finance")
    }
    "personalizedLearning" = @{
        name = "learnsmart-ai"
        displayName = "LearnSmart AI"
        category = "Education"
        description = "AI-driven personalized learning platform"
        keywords = @("learning", "education", "ai", "personalized")
    }
    "photoApp" = @{
        name = "photomaster-pro"
        displayName = "PhotoMaster Pro"
        category = "Media Tools"
        description = "Professional photo editing and management suite"
        keywords = @("photo", "editing", "management", "media")
    }
    "portfolio-website" = @{
        name = "portfolioforge-builder"
        displayName = "PortfolioForge"
        category = "Web Development"
        description = "Professional portfolio website builder"
        keywords = @("portfolio", "website", "builder", "professional")
    }
    "project-tracker" = @{
        name = "projectpulse-manager"
        displayName = "ProjectPulse"
        category = "Project Management"
        description = "Advanced project tracking and management platform"
        keywords = @("project", "tracking", "management", "productivity")
    }
    "promptEnhancer" = @{
        name = "promptcraft-pro"
        displayName = "PromptCraft Pro"
        category = "AI Tools"
        description = "AI prompt enhancement and optimization tool"
        keywords = @("prompt", "ai", "enhancement", "optimization")
    }
    "promptEnhancer2" = @{
        name = "promptcraft-elite"
        displayName = "PromptCraft Elite"
        category = "AI Tools"
        description = "Elite AI prompt crafting and enhancement suite"
        keywords = @("prompt", "ai", "crafting", "elite")
    }
    "puffsPerPenny" = @{
        name = "puffstracker-basic"
        displayName = "PuffsTracker"
        category = "Health & Wellness"
        description = "Personal consumption tracking application"
        keywords = @("tracking", "health", "consumption", "personal")
    }
    "puffsPerPenny 2.0" = @{
        name = "puffstracker-pro"
        displayName = "PuffsTracker Pro"
        category = "Health & Wellness"
        description = "Advanced consumption tracking with analytics"
        keywords = @("tracking", "health", "analytics", "professional")
    }
    "replit-mcp-server" = @{
        name = "mcp-connect-server"
        displayName = "MCP Connect"
        category = "Development Tools"
        description = "Model Context Protocol server implementation"
        keywords = @("mcp", "server", "protocol", "development")
    }
    "saas-starter" = @{
        name = "saas-genesis-kit"
        displayName = "SaaS Genesis"
        category = "SaaS Tools"
        description = "Complete SaaS application starter kit"
        keywords = @("saas", "starter", "kit", "development")
    }
    "screenpipe" = @{
        name = "screenpipe-pro"
        displayName = "ScreenPipe Pro"
        category = "System Utilities"
        description = "Advanced screen capture and processing pipeline"
        keywords = @("screen", "capture", "processing", "utility")
    }
    "Solemn" = @{
        name = "solemn-studio"
        displayName = "Solemn Studio"
        category = "Creative Tools"
        description = "Professional creative content studio"
        keywords = @("creative", "studio", "content", "professional")
    }
    "Sorta" = @{
        name = "sortatech-platform"
        displayName = "SortaTech"
        category = "Technology"
        description = "Innovative technology solutions platform"
        keywords = @("technology", "solutions", "platform", "innovation")
    }
    "textToPdfTool" = @{
        name = "pdfcraft-pro"
        displayName = "PDFCraft Pro"
        category = "Document Tools"
        description = "Professional text to PDF conversion tool"
        keywords = @("pdf", "conversion", "documents", "professional")
    }
    "TrackStar" = @{
        name = "trackstar-pro"
        displayName = "TrackStar Pro"
        category = "Analytics"
        description = "Professional tracking and analytics platform"
        keywords = @("tracking", "analytics", "professional", "data")
    }
    "ultimateExtensionHub" = @{
        name = "extensionuniverse-hub"
        displayName = "ExtensionUniverse"
        category = "Browser Extensions"
        description = "Ultimate browser extension management universe"
        keywords = @("extension", "browser", "universe", "management")
    }
    "universalContentStudio" = @{
        name = "contentforge-pro"
        displayName = "ContentForge Pro"
        category = "Content Creation"
        description = "Universal content creation and management studio"
        keywords = @("content", "creation", "management", "studio")
    }
    "usefulToolSiteLog" = @{
        name = "toolvault-pro"
        displayName = "ToolVault Pro"
        category = "Productivity"
        description = "Comprehensive tool discovery and management platform"
        keywords = @("tools", "discovery", "management", "productivity")
    }
    "v0-infiniterate-main" = @{
        name = "infinicode-platform"
        displayName = "InfiniCode"
        category = "Development Tools"
        description = "Infinite code generation and iteration platform"
        keywords = @("code", "generation", "iteration", "development")
    }
    "vscode-ai-assistant" = @{
        name = "codemind-ai"
        displayName = "CodeMind AI"
        category = "Development Tools"
        description = "AI-powered VS Code development assistant"
        keywords = @("vscode", "ai", "assistant", "development")
    }
    "WorkFlowGenius" = @{
        name = "workflowgenius-pro"
        displayName = "WorkFlowGenius Pro"
        category = "Productivity"
        description = "Intelligent workflow automation and optimization"
        keywords = @("workflow", "automation", "genius", "productivity")
    }
    "YouKnowSuno" = @{
        name = "sunomaster-platform"
        displayName = "SunoMaster"
        category = "Music Tools"
        description = "Advanced Suno AI music creation platform"
        keywords = @("suno", "music", "ai", "creation")
    }
    "YouShallPass" = @{
        name = "passguardian-security"
        displayName = "PassGuardian"
        category = "Security"
        description = "Advanced password and security management system"
        keywords = @("password", "security", "guardian", "protection")
    }
}

function Test-GitRemote {
    param($ProjectPath)
    try {
        $remotes = git remote -v 2>$null
        return $remotes -ne $null -and $remotes.Length -gt 0
    } catch {
        return $false
    }
}

function Update-PackageJson {
    param($ProjectInfo, $ProjectPath)
    
    $packagePath = Join-Path $ProjectPath "package.json"
    if (Test-Path $packagePath) {
        try {
            $pkg = Get-Content $packagePath | ConvertFrom-Json
            $pkg.name = $ProjectInfo.name
            $pkg.description = $ProjectInfo.description
            
            # Add/update keywords
            if ($ProjectInfo.keywords) {
                $pkg.keywords = $ProjectInfo.keywords
            }
            
            # Add/update author if not present
            if (-not $pkg.author) {
                $pkg.author = "Development Team"
            }
            
            # Add/update version if not present
            if (-not $pkg.version) {
                $pkg.version = "1.0.0"
            }
            
            # Add/update license if not present
            if (-not $pkg.license) {
                $pkg.license = "MIT"
            }
            
            $pkg | ConvertTo-Json -Depth 10 | Set-Content $packagePath
            Write-Log "Updated package.json: $($ProjectInfo.name)" "SUCCESS"
            return $true
        } catch {
            Write-Log "Failed to update package.json: $_" "ERROR"
            return $false
        }
    }
    return $false
}

function Create-ReadmeFile {
    param($ProjectInfo, $ProjectPath)
    
    $readmePath = Join-Path $ProjectPath "README.md"
    if (-not (Test-Path $readmePath)) {
        $readmeContent = @"
# $($ProjectInfo.displayName)

## Description
$($ProjectInfo.description)

## Category
$($ProjectInfo.category)

## Keywords
$($ProjectInfo.keywords -join ", ")

## Installation

\`\`\`bash
npm install
\`\`\`

## Usage

\`\`\`bash
npm start
\`\`\`

## Contributing
Please read our contributing guidelines before submitting pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Support
For support and questions, please open an issue in the GitHub repository.
"@
        
        Set-Content -Path $readmePath -Value $readmeContent
        Write-Log "Created README.md for $($ProjectInfo.displayName)" "SUCCESS"
        return $true
    }
    return $false
}

function Initialize-GitIgnore {
    param($ProjectPath)
    
    $gitignorePath = Join-Path $ProjectPath ".gitignore"
    if (-not (Test-Path $gitignorePath)) {
        $gitignoreContent = @"
# Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Build outputs
dist/
build/
*.tgz
*.tar.gz

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
logs
*.log

# Temporary files
tmp/
temp/
"@
        
        Set-Content -Path $gitignorePath -Value $gitignoreContent
        Write-Log "Created .gitignore" "SUCCESS"
        return $true
    }
    return $false
}

function Process-Project {
    param($FolderName, $ProjectInfo, $BasePath)
    
    $projectPath = Join-Path $BasePath $FolderName
    
    if (-not (Test-Path $projectPath)) {
        Write-Log "Project folder not found: $FolderName" "WARNING"
        return $false
    }
    
    Write-Log "Processing: $FolderName -> $($ProjectInfo.displayName)" "INFO"
    
    # Enter project directory
    Push-Location $projectPath
    
    try {
        $hasChanges = $false
        
        # Update package.json
        if (Update-PackageJson -ProjectInfo $ProjectInfo -ProjectPath $projectPath) {
            $hasChanges = $true
        }
        
        # Create README.md if it doesn't exist
        if (Create-ReadmeFile -ProjectInfo $ProjectInfo -ProjectPath $projectPath) {
            $hasChanges = $true
        }
        
        # Initialize .gitignore if it doesn't exist
        if (Initialize-GitIgnore -ProjectPath $projectPath) {
            $hasChanges = $true
        }
        
        # Git operations
        if (Test-Path ".git") {
            Write-Log "Git repository exists" "INFO"
            
            # Check git status
            $status = git status --porcelain 2>$null
            if ($status -or $hasChanges) {
                if (-not $DryRun) {
                    Write-Log "Staging and committing changes..." "INFO"
                    git add .
                    git commit -m "Update project branding to $($ProjectInfo.displayName) and enhance project structure

- Updated package.json with proper name, description, and metadata
- Added comprehensive README.md with project information
- Enhanced .gitignore for better file management
- Organized project structure for production readiness"
                    
                    # Try to push if remote exists
                    if (Test-GitRemote -ProjectPath $projectPath) {
                        try {
                            git push
                            Write-Log "Successfully pushed to remote repository" "SUCCESS"
                        } catch {
                            Write-Log "Failed to push to remote: $_" "WARNING"
                        }
                    } else {
                        Write-Log "No remote repository configured - skipping push" "WARNING"
                    }
                } else {
                    Write-Log "[DRY RUN] Would commit and push changes" "INFO"
                }
            } else {
                Write-Log "No changes to commit" "INFO"
            }
        } else {
            Write-Log "Initializing git repository..." "INFO"
            if (-not $DryRun) {
                git init
                Initialize-GitIgnore -ProjectPath $projectPath
                git add .
                git commit -m "Initial commit for $($ProjectInfo.displayName)

- Established project structure
- Added comprehensive documentation
- Configured development environment
- Set up version control"
                Write-Log "Git repository initialized and committed" "SUCCESS"
            } else {
                Write-Log "[DRY RUN] Would initialize git repository" "INFO"
            }
        }
        
        return $true
        
    } catch {
        Write-Log "Error processing $FolderName : $_" "ERROR"
        return $false
    } finally {
        Pop-Location
    }
}

# Main execution
Write-Log "=== Advanced Project Management Automation Started ===" "INFO"
Write-Log "Working Directory: $PWD" "INFO"
Write-Log "Dry Run Mode: $DryRun" "INFO"
Write-Log "Total Projects to Process: $($projects.Count)" "INFO"

$successCount = 0
$errorCount = 0
$startTime = Get-Date

foreach ($folderName in $projects.Keys) {
    $projectInfo = $projects[$folderName]
    
    if (Process-Project -FolderName $folderName -ProjectInfo $projectInfo -BasePath $PWD) {
        $successCount++
    } else {
        $errorCount++
    }
    
    if ($Verbose) {
        Write-Log "Progress: $($successCount + $errorCount)/$($projects.Count) projects processed" "INFO"
    }
}

$endTime = Get-Date
$duration = $endTime - $startTime

Write-Log "=== Project Management Automation Completed ===" "SUCCESS"
Write-Log "Successfully processed: $successCount projects" "SUCCESS"
Write-Log "Errors encountered: $errorCount projects" $(if ($errorCount -gt 0) { "WARNING" } else { "INFO" })
Write-Log "Total execution time: $($duration.TotalMinutes.ToString("F2")) minutes" "INFO"
Write-Log "Log file saved to: $LogPath" "INFO"

if ($errorCount -gt 0) {
    Write-Log "Please review the log file for details on any errors encountered." "WARNING"
}
