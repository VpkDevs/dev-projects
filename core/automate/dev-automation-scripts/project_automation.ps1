# Project Management Automation Script
$projects = @{
    "aiResourceDirectory" = "ResourceHub AI"
    "APPYness2" = "AppFlow Pro"
    "bigFaith" = "FaithConnect"
    "blackBoxAI" = "DeepMind Studio"
    "directoryStructureGenerator" = "StructGen Pro"
    "DuplicateCleanerPro" = "CleanSpace Pro"
    "dyadiaGame" = "Dyadia Quest"
    "ebayWebApp" = "AuctionMaster Pro"
    "eCommerceWizard" = "CommerceCore"
    "exclusionExtension" = "FilterShield"
    "Explainer" = "ClarityBot"
    "extensionListProject" = "ExtensionCentral"
    "financeApp" = "WealthTracker Pro"
    "functionCalls" = "APIBridge"
    "googleSearchExtension" = "SearchBoost Pro"
    "hotkeyManagementTool" = "KeyMaster Pro"
    "hotkeyManagementTool2" = "KeyMaster Elite"
    "IconIQ" = "IconIQ Studio"
    "inventoryFinder" = "StockSense Pro"
    "julia_anniversary_project_src" = "LoveKeeper"
    "marketSage" = "MarketSage AI"
    "microSaaS" = "MicroLaunch"
    "narrativeEngineReal" = "StoryForge AI"
    "nextGenProductvityPlatform" = "ProductivityMax"
    "noCodeAppBuilder" = "NoCodeStudio"
    "noCodeAppBuilderPromptLibraryAndSuite" = "NoCodeMaster Suite"
    "nokode" = "NoKode Engine"
    "noteApp" = "NoteVault Pro"
    "nyteOwls" = "NyteOwls Hub"
    "omni_organizer" = "OmniOrganizer Pro"
    "omniSort" = "SortGenius"
    "PassiveIncomeAutomator" = "IncomeFlow AI"
    "personalizedLearning" = "LearnSmart AI"
    "photoApp" = "PhotoMaster Pro"
    "portfolio-website" = "PortfolioForge"
    "project-tracker" = "ProjectPulse"
    "promptEnhancer" = "PromptCraft Pro"
    "promptEnhancer2" = "PromptCraft Elite"
    "puffsPerPenny" = "PuffsTracker"
    "puffsPerPenny 2.0" = "PuffsTracker Pro"
    "replit-mcp-server" = "MCP Connect"
    "saas-starter" = "SaaS Genesis"
    "screenpipe" = "ScreenPipe Pro"
    "Solemn" = "Solemn Studio"
    "Sorta" = "SortaTech"
    "textToPdfTool" = "PDFCraft Pro"
    "TrackStar" = "TrackStar Pro"
    "ultimateExtensionHub" = "ExtensionUniverse"
    "universalContentStudio" = "ContentForge Pro"
    "usefulToolSiteLog" = "ToolVault Pro"
    "v0-infiniterate-main" = "InfiniCode"
    "vscode-ai-assistant" = "CodeMind AI"
    "WorkFlowGenius" = "WorkFlowGenius Pro"
    "YouKnowSuno" = "SunoMaster"
    "YouShallPass" = "PassGuardian"
}

Write-Host "Starting project management automation..." -ForegroundColor Green

foreach ($folderName in $projects.Keys) {
    $projectPath = Join-Path $PWD $folderName
    $newName = $projects[$folderName]
    
    if (Test-Path $projectPath) {
        Write-Host "`nProcessing: $folderName -> $newName" -ForegroundColor Yellow
        
        # Enter project directory
        Push-Location $projectPath
        
        try {
            # Check if package.json exists and update name
            if (Test-Path "package.json") {
                $pkg = Get-Content "package.json" | ConvertFrom-Json
                $pkg.name = $newName.ToLower().Replace(" ", "-")
                $pkg | ConvertTo-Json -Depth 10 | Set-Content "package.json"
                Write-Host "  Updated package.json name to: $($pkg.name)" -ForegroundColor Cyan
            }
            
            # Check if git is initialized
            if (Test-Path ".git") {
                Write-Host "  Git repository exists" -ForegroundColor Green
                
                # Check git status
                $status = git status --porcelain
                if ($status) {
                    Write-Host "  Found changes, staging and committing..." -ForegroundColor Blue
                    git add .
                    git commit -m "Update project branding to $newName and organize codebase"
                    
                    # Try to push
                    try {
                        git push
                        Write-Host "  Successfully pushed to remote" -ForegroundColor Green
                    } catch {
                        Write-Host "  Failed to push (remote may not exist): $_" -ForegroundColor Red
                    }
                } else {
                    Write-Host "  No changes to commit" -ForegroundColor Gray
                }
            } else {
                Write-Host "  Initializing git repository..." -ForegroundColor Blue
                git init
                git add .
                git commit -m "Initial commit for $newName"
                Write-Host "  Git repository initialized and committed" -ForegroundColor Green
            }
            
        } catch {
            Write-Host "  Error processing $folderName : $_" -ForegroundColor Red
        } finally {
            Pop-Location
        }
    } else {
        Write-Host "  Project folder not found: $folderName" -ForegroundColor Red
    }
}

Write-Host "`nProject management automation completed!" -ForegroundColor Green
