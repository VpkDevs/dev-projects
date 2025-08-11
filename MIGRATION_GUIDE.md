# Project Migration Guide

## 🔄 Phase 2: Moving Projects to Matrix Structure

Use this guide to migrate your existing projects to the new matrix structure.

## 📋 Migration Mapping

### From Current Structure → To Matrix Structure

#### Enterprise Level (Production-ready, high-stakes)
```
Current → New Location
───────────────────────────────────────────────────
mind-bridge → enterprise/web-platforms/
aiPromptLibrary (main) → enterprise/web-platforms/
screen-stream → enterprise/web-platforms/
market-oracle (main) → enterprise/data-systems/
crypto-arbitrage → enterprise/business-apps/
key-commander-pro → enterprise/infrastructure/
extension-almanac → enterprise/infrastructure/
aiPromptLibrary (.hai) → enterprise/ai-ml/
market-oracle (.hai) → enterprise/ai-ml/
metric-master → enterprise/analytics/
wealth-stream → enterprise/analytics/
```

#### Professional Level (Client/business ready)
```
Current → New Location
───────────────────────────────────────────────────
money-mentor → professional/web-platforms/
store-genie → professional/web-platforms/
truth-lens → professional/web-platforms/
smart-sort → professional/automation/
sort-wizard → professional/automation/
flow-master → professional/automation/
vape-value-pro → professional/analytics/
stock-sleuth → professional/analytics/
fetching → professional/integrations/
auction-scout → professional/integrations/
story-architect → professional/creative-tools/
template-gallery → professional/creative-tools/
dupe-detective → professional/business-apps/
tool-tracker → professional/business-apps/
```

#### Personal Level (Individual use, utilities)
```
Current → New Location
───────────────────────────────────────────────────
clarity-lens → personal/web-platforms/
pixel-perfect → personal/web-platforms/
web-canvas → personal/web-platforms/
key-commander → personal/automation/
passwordz → personal/automation/
window-wizard → personal/automation/
Most create/ projects → personal/creative-tools/
frame-master → personal/creative-tools/
pdf-mint → personal/creative-tools/
Most analyze/ projects → personal/analytics/
used-car-deal-finder → personal/business-apps/
vape-value → personal/business-apps/
Most core/ projects → personal/automation/
```

#### Experimental Level (R&D, proof-of-concept)
```
Current → New Location
───────────────────────────────────────────────────
Most ai-coding-projects/ → experimental/ai-ml/
prompt-forge variants → experimental/ai-ml/
Most unsorted/ projects → experimental/web-platforms/
infinity-loop → experimental/web-platforms/
games/ → experimental/creative-tools/
3dmodeller → experimental/creative-tools/
Most augment-projects/ → experimental/automation/
noCodeInventionBuilder → experimental/web-platforms/
```

#### Archived
```
Current → New Location
───────────────────────────────────────────────────
archived-projects/ → archived/by-category/
Deprecated projects → archived/by-status/
```

## 🛠️ Migration Commands

### PowerShell Migration Script Template
```powershell
# Example migration commands (run one at a time, verify before executing)

# Enterprise migrations
Move-Item "mind-bridge" "enterprise\web-platforms\mind-bridge"
Move-Item "aiPromptLibrary" "enterprise\web-platforms\aiPromptLibrary"
Move-Item "market-oracle" "enterprise\data-systems\market-oracle"

# Professional migrations  
Move-Item "money-mentor" "professional\web-platforms\money-mentor"
Move-Item "smart-sort" "professional\automation\smart-sort"
Move-Item "story-architect" "professional\creative-tools\story-architect"

# Personal migrations
Move-Item "key-commander" "personal\automation\key-commander"
Move-Item "clarity-lens" "personal\web-platforms\clarity-lens"

# Experimental migrations
Move-Item "ai-coding-projects\*" "experimental\ai-ml\"
Move-Item "unsorted\infinity-loop" "experimental\web-platforms\infinity-loop"

# Archived migrations
Move-Item "archived-projects\*" "archived\by-category\"
```

## ⚠️ Migration Best Practices

### 1. **Backup First**
```powershell
# Create backup before migration
Copy-Item "." "backup_$(Get-Date -Format 'yyyy-MM-dd_HH-mm')" -Recurse
```

### 2. **Migrate in Batches**
- Start with 5-10 projects
- Verify each migration
- Update any references/paths
- Test functionality

### 3. **Update References**
After moving projects, update:
- IDE workspace configurations
- Build scripts and deployment configs
- Documentation links
- Symbolic links or shortcuts

### 4. **Verify Structure**
```powershell
# Check if project moved successfully
Test-Path "enterprise\web-platforms\mind-bridge"
Test-Path "professional\automation\smart-sort"
```

## 📝 Migration Checklist

For each project migration:

- [ ] **Backup**: Project backed up or in version control
- [ ] **Move**: Project moved to correct matrix location
- [ ] **Verify**: Project structure intact after move
- [ ] **Update**: IDE/editor workspace updated
- [ ] **Test**: Project still builds/runs correctly
- [ ] **Document**: Update any documentation references
- [ ] **Clean**: Remove empty directories from old structure

## 🎯 Decision Framework

**Not sure where a project goes?**

### Complexity Level Decision:
1. **Enterprise**: 
   - ✅ Production/revenue generating
   - ✅ Mission-critical
   - ✅ Comprehensive testing/monitoring
   
2. **Professional**:
   - ✅ Client-ready quality
   - ✅ Well documented and tested
   - ✅ Business use case
   
3. **Personal**:
   - ✅ Individual use
   - ✅ Learning/utility focused
   - ✅ Basic functionality
   
4. **Experimental**:
   - ✅ Proof-of-concept
   - ✅ Research/exploration
   - ✅ Incomplete/prototype

### Category Decision:
- **web-platforms**: Full web apps, sites, platforms
- **data-systems**: APIs, databases, data processing  
- **infrastructure**: DevOps, deployment, system tools
- **ai-ml**: ML models, AI tools, data science
- **automation**: Scripts, workflows, task automation
- **analytics**: Dashboards, reporting, BI
- **integrations**: API connections, middleware
- **creative-tools**: Design, media, content creation
- **business-apps**: Domain-specific applications

## 📞 Next Steps

1. **Review this guide** and the main `MATRIX_STRUCTURE.md`
2. **Start with small batches** - migrate 5-10 projects at a time
3. **Test each migration** before proceeding to the next batch
4. **Update tooling** as you go (IDE configs, scripts, etc.)
5. **Document any issues** or adjustments needed

---

**Remember**: The matrix structure is flexible. Projects can be moved between complexity levels as they mature, and the categories can be adjusted if needed.
