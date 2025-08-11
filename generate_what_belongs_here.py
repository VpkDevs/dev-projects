#!/usr/bin/env python3
"""
Generate what-belongs-here.md files for all category directories
"""

import json
import os
from datetime import datetime
from pathlib import Path


def load_category_mapping():
    """Load the category mapping data"""
    with open('category_mapping.json', 'r') as f:
        return json.load(f)


def load_template():
    """Load the markdown template"""
    with open('category_template.md', 'r') as f:
        return f.read()


def generate_markdown_for_category(category_data, template):
    """Generate markdown content for a specific category"""
    
    # Extract data with safe defaults
    name = category_data.get('name', 'Unknown')
    definition = category_data.get('definition', 'No definition provided')
    criteria = category_data.get('inclusion_criteria', [])
    examples = category_data.get('example_projects', [])
    counter_examples = category_data.get('counter_examples', [])
    relocation_advice = category_data.get('relocation_advice', '')
    
    # Start with the template
    content = template
    
    # Replace basic fields
    content = content.replace('{{CATEGORY_NAME}}', name.upper().replace('-', ' '))
    content = content.replace('{{CATEGORY_DEFINITION}}', definition)
    content = content.replace('{{LAST_UPDATED_DATE}}', datetime.now().strftime('%Y-%m-%d'))
    content = content.replace('{{TEMPLATE_VERSION}}', '1.0')
    
    # Handle criteria (pad with optional if fewer than 5)
    for i in range(5):
        if i < len(criteria):
            content = content.replace(f'{{{{CRITERION_{i+1}}}}}', criteria[i])
        else:
            # Remove optional criteria lines if not needed
            if i >= 3:  # Criteria 4 and 5 are marked as optional
                content = content.replace(f'- {{{{CRITERION_{i+1}}}}} *(optional)*', '')
            else:
                content = content.replace(f'{{{{CRITERION_{i+1}}}}}', 'To be determined')
    
    # Handle examples that belong
    example_descriptions = {
        # Analyze category
        'market-oracle': 'Financial market analysis and prediction tool',
        'truth-lens': 'Content verification and fact-checking system',
        'smart-sort': 'Intelligent data sorting and organization tool',
        
        # Create category
        'story-architect': 'Narrative design and story creation platform',
        'pixel-perfect': 'Precision design and image editing tool',
        'template-gallery': 'Collection of reusable project templates',
        
        # Core category
        'code-companion': 'AI-powered coding assistant for daily development',
        'dev-sanctuary': 'Development environment management system',
        'universal-hub': 'Central dashboard for all project resources',
        
        # Specialize category
        'auction-scout': 'Specialized tool for auction monitoring and bidding',
        'faith-stack': 'Domain-specific tools for faith-based applications',
        'night-shift': 'Tools optimized for night-time work patterns',
        
        # Personal category
        'note-ninja': 'Personal note-taking and organization system',
        'money-mentor': 'Personal finance tracking and advice tool',
        'key-commander': 'Personal keyboard shortcut management',
        
        # Experimental category
        'genesis-lab': 'Experimental workspace for new ideas',
        'temp-forge': 'Temporary project creation and testing',
        'workspace-alpha': 'Alpha version of new workspace concepts',
        
        # Archived category
        'legacy-vault': 'Storage for legacy codebases',
        'version-museum': 'Historical version preservation system',
        'archived-projects content': 'Previously active projects now deprecated',
        
        # Default examples
        'Would include production SaaS platforms': 'Full-featured SaaS applications in production',
        'Enterprise data warehouses': 'Large-scale data storage and analytics systems',
        'Mission-critical automation systems': 'Business-critical automated workflows',
        'Business web applications': 'Web apps designed for business operations',
        'Client reporting dashboards': 'Interactive dashboards for client data',
        'Custom business solutions': 'Tailored solutions for specific business needs',
        'Projects pending review': 'New projects awaiting categorization',
        'New imports': 'Recently imported projects from external sources',
        'Unclear purpose projects': 'Projects needing purpose clarification'
    }
    
    # Fill in examples that belong
    for i in range(5):
        if i < len(examples):
            example = examples[i]
            description = example_descriptions.get(example, 'Project in this category')
            content = content.replace(f'{{{{EXAMPLE_BELONG_{i+1}}}}}', example)
            content = content.replace(f'{{{{EXAMPLE_BELONG_{i+1}_DESCRIPTION}}}}', description)
        else:
            # Use placeholder examples
            content = content.replace(f'{{{{EXAMPLE_BELONG_{i+1}}}}}', f'Example {i+1}')
            content = content.replace(f'{{{{EXAMPLE_BELONG_{i+1}_DESCRIPTION}}}}', 'Future project in this category')
    
    # Handle counter examples (examples that don't belong)
    counter_ex_parsed = []
    for ce in counter_examples:
        if '(' in ce and ')' in ce:
            project = ce.split('(')[0].strip()
            rest = ce.split('(')[1].rstrip(')')
            if 'belongs in' in rest:
                parts = rest.split('belongs in')
                category = parts[1].split('-')[0].strip()
                reason = parts[1].split('-')[1].strip() if '-' in parts[1] else 'Different primary purpose'
                counter_ex_parsed.append({
                    'project': project,
                    'category': category,
                    'reason': reason
                })
    
    # Fill in counter examples
    for i in range(4):
        if i < len(counter_ex_parsed):
            ce = counter_ex_parsed[i]
            content = content.replace(f'{{{{EXAMPLE_NOT_BELONG_{i+1}}}}}', ce['project'])
            content = content.replace(f'{{{{EXAMPLE_NOT_BELONG_{i+1}_REASON}}}}', ce['reason'])
            content = content.replace(f'{{{{EXAMPLE_NOT_BELONG_{i+1}_CORRECT_CATEGORY}}}}', ce['category'])
        else:
            content = content.replace(f'{{{{EXAMPLE_NOT_BELONG_{i+1}}}}}', f'Misplaced Project {i+1}')
            content = content.replace(f'{{{{EXAMPLE_NOT_BELONG_{i+1}_REASON}}}}', 'Does not match category criteria')
            content = content.replace(f'{{{{EXAMPLE_NOT_BELONG_{i+1}_CORRECT_CATEGORY}}}}', 'To be determined')
    
    # Handle alternative categories based on relocation advice
    alternatives = []
    if 'analyze' in relocation_advice.lower():
        alternatives.append(('analyze', 'For analysis and monitoring tools'))
    if 'create' in relocation_advice.lower():
        alternatives.append(('create', 'For content creation and design tools'))
    if 'core' in relocation_advice.lower():
        alternatives.append(('core', 'For essential daily-use tools'))
    if 'specialize' in relocation_advice.lower():
        alternatives.append(('specialize', 'For domain-specific or niche tools'))
    if 'experimental' in relocation_advice.lower():
        alternatives.append(('experimental', 'For prototypes and proof-of-concepts'))
    if 'personal' in relocation_advice.lower():
        alternatives.append(('personal', 'For individual use projects'))
    if 'professional' in relocation_advice.lower():
        alternatives.append(('professional', 'For client-ready business solutions'))
    if 'enterprise' in relocation_advice.lower():
        alternatives.append(('enterprise', 'For production-grade mission-critical systems'))
    if 'archived' in relocation_advice.lower():
        alternatives.append(('archived', 'For deprecated or obsolete projects'))
    
    # Ensure we have at least 5 alternatives
    while len(alternatives) < 5:
        alternatives.append(('unsorted', 'For projects pending categorization'))
    
    # Fill in alternative categories
    for i in range(5):
        if i < len(alternatives):
            alt_name, alt_desc = alternatives[i]
            content = content.replace(f'{{{{ALTERNATIVE_CATEGORY_{i+1}}}}}', alt_name)
            content = content.replace(f'{{{{ALTERNATIVE_CATEGORY_{i+1}_DESCRIPTION}}}}', alt_desc)
    
    return content


def main():
    """Main function to generate all what-belongs-here.md files"""
    
    # Load data
    mapping_data = load_category_mapping()
    template = load_template()
    
    # Track results
    results = {
        'created': [],
        'updated': [],
        'skipped': [],
        'errors': []
    }
    
    # Process each category
    for category in mapping_data['categories']:
        category_name = category['name']
        category_path = Path(category_name)
        
        # Check if directory exists
        if not category_path.exists():
            results['skipped'].append(f"{category_name} (directory does not exist)")
            print(f"⚠️  Skipping {category_name}: directory does not exist")
            continue
        
        # Generate markdown content
        try:
            markdown_content = generate_markdown_for_category(category, template)
            
            # Write to file
            output_file = category_path / 'what-belongs-here.md'
            
            # Check if file exists
            file_exists = output_file.exists()
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            if file_exists:
                results['updated'].append(str(output_file))
                print(f"✅ Updated: {output_file}")
            else:
                results['created'].append(str(output_file))
                print(f"✅ Created: {output_file}")
                
        except Exception as e:
            results['errors'].append(f"{category_name}: {str(e)}")
            print(f"❌ Error processing {category_name}: {e}")
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"✅ Created: {len(results['created'])} files")
    print(f"✅ Updated: {len(results['updated'])} files")
    print(f"⚠️  Skipped: {len(results['skipped'])} directories")
    print(f"❌ Errors: {len(results['errors'])} errors")
    
    if results['created']:
        print("\nCreated files:")
        for f in results['created']:
            print(f"  - {f}")
    
    if results['updated']:
        print("\nUpdated files:")
        for f in results['updated']:
            print(f"  - {f}")
    
    if results['skipped']:
        print("\nSkipped directories:")
        for f in results['skipped']:
            print(f"  - {f}")
    
    if results['errors']:
        print("\nErrors:")
        for e in results['errors']:
            print(f"  - {e}")


if __name__ == '__main__':
    main()
