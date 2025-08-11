#!/usr/bin/env python3
"""
Markdown File Linter for what-belongs-here.md files
Validates that each file contains required sections and follows content rules.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class Section(Enum):
    """Required sections in order"""
    CATEGORY_DEFINITION = "Category Definition"
    INCLUSION_CRITERIA = "Inclusion Criteria"
    EXAMPLES_BELONG = "Examples That Belong"
    EXAMPLES_NOT_BELONG = "Examples That Do NOT Belong"
    WHERE_TO_MOVE = "Where to Move Non-Matching Projects"


@dataclass
class ValidationResult:
    """Result of validating a single markdown file"""
    file_path: str
    is_valid: bool
    errors: List[str]
    warnings: List[str]


class MarkdownLinter:
    """Linter for what-belongs-here markdown files"""
    
    REQUIRED_SECTIONS = [
        Section.CATEGORY_DEFINITION,
        Section.INCLUSION_CRITERIA,
        Section.EXAMPLES_BELONG,
        Section.EXAMPLES_NOT_BELONG,
        Section.WHERE_TO_MOVE
    ]
    
    def __init__(self):
        self.results: List[ValidationResult] = []
    
    def find_markdown_files(self, root_dir: str = ".") -> List[Path]:
        """Find all what-belongs-here*.md files in the directory tree"""
        root_path = Path(root_dir)
        md_files = []
        
        try:
            for file_path in root_path.rglob("what-belongs-here*.md"):
                # Skip the generation report file
                if "generation-report" not in file_path.name:
                    md_files.append(file_path)
        except Exception as e:
            print(f"Error searching for files: {e}")
        
        return sorted(md_files)
    
    def extract_sections(self, content: str) -> Dict[str, Tuple[int, str]]:
        """Extract sections from markdown content"""
        sections = {}
        lines = content.split('\n')
        
        current_section = None
        current_content = []
        current_line_num = 0
        
        for i, line in enumerate(lines, 1):
            # Check for section headers (## Header)
            if line.strip().startswith('## '):
                # Save previous section if exists
                if current_section:
                    sections[current_section] = (current_line_num, '\n'.join(current_content))
                
                # Start new section
                header = line.strip()[3:].strip()
                current_section = header
                current_content = []
                current_line_num = i
            elif current_section:
                current_content.append(line)
        
        # Save last section
        if current_section:
            sections[current_section] = (current_line_num, '\n'.join(current_content))
        
        return sections
    
    def count_bullets_in_criteria(self, content: str) -> Tuple[int, int]:
        """Count bullets in criteria section, returns (required_count, optional_count)"""
        required_count = 0
        optional_count = 0
        
        for line in content.split('\n'):
            stripped = line.strip()
            if stripped.startswith('- '):
                if '*(optional)*' in stripped.lower():
                    optional_count += 1
                else:
                    required_count += 1
        
        return required_count, optional_count
    
    def check_examples_section(self, content: str) -> Tuple[bool, List[str]]:
        """Check if examples section has at least one example"""
        errors = []
        has_example = False
        
        # Look for numbered examples or bullet points with content
        for line in content.split('\n'):
            stripped = line.strip()
            # Check for numbered examples (1. **name**: description)
            if re.match(r'^\d+\.\s+\*\*[^*]+\*\*:', stripped):
                has_example = True
                break
            # Check for bullet examples (- **name**: description)
            elif re.match(r'^-\s+\*\*[^*]+\*\*:', stripped):
                has_example = True
                break
        
        if not has_example:
            errors.append("No properly formatted examples found (expected format: '1. **name**: description')")
        
        return has_example, errors
    
    def check_counter_examples_section(self, content: str) -> Tuple[bool, List[str]]:
        """Check if counter-examples section has at least one example with 'Should be in' note"""
        errors = []
        has_example = False
        has_should_be_in = False
        
        for line in content.split('\n'):
            stripped = line.strip()
            # Check for numbered examples
            if re.match(r'^\d+\.\s+\*\*[^*]+\*\*:', stripped):
                has_example = True
            # Check for "Should be in:" indication
            elif re.match(r'^-\s+\*Should be in:\*', stripped):
                has_should_be_in = True
        
        if not has_example:
            errors.append("No properly formatted counter-examples found")
        if has_example and not has_should_be_in:
            errors.append("Counter-examples should include 'Should be in:' notes")
        
        return has_example and has_should_be_in, errors
    
    def validate_file(self, file_path: Path) -> ValidationResult:
        """Validate a single markdown file"""
        errors = []
        warnings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return ValidationResult(
                file_path=str(file_path),
                is_valid=False,
                errors=[f"Failed to read file: {e}"],
                warnings=[]
            )
        
        # Extract sections
        sections = self.extract_sections(content)
        
        # Check 1: All required sections present and in order
        found_sections = []
        for section in self.REQUIRED_SECTIONS:
            if section.value in sections:
                found_sections.append(section.value)
            else:
                errors.append(f"Missing required section: '{section.value}'")
        
        # Check section order
        if len(found_sections) == len(self.REQUIRED_SECTIONS):
            section_positions = [sections[s.value][0] for s in self.REQUIRED_SECTIONS if s.value in sections]
            if section_positions != sorted(section_positions):
                errors.append("Sections are not in the required order")
        
        # Check 2: Inclusion Criteria has 3-5 bullets
        if Section.INCLUSION_CRITERIA.value in sections:
            criteria_content = sections[Section.INCLUSION_CRITERIA.value][1]
            required_bullets, optional_bullets = self.count_bullets_in_criteria(criteria_content)
            total_bullets = required_bullets + optional_bullets
            
            if total_bullets < 3:
                errors.append(f"Inclusion Criteria has {total_bullets} bullets, minimum is 3")
            elif total_bullets > 5:
                warnings.append(f"Inclusion Criteria has {total_bullets} bullets, recommended maximum is 5")
            
            if required_bullets < 3:
                errors.append(f"Inclusion Criteria should have at least 3 required criteria (found {required_bullets})")
        
        # Check 3: Examples section has at least one example
        if Section.EXAMPLES_BELONG.value in sections:
            examples_content = sections[Section.EXAMPLES_BELONG.value][1]
            has_examples, example_errors = self.check_examples_section(examples_content)
            if not has_examples:
                errors.extend([f"Examples That Belong: {e}" for e in example_errors])
        
        # Check 4: Counter-examples section has at least one example
        if Section.EXAMPLES_NOT_BELONG.value in sections:
            counter_content = sections[Section.EXAMPLES_NOT_BELONG.value][1]
            has_counter, counter_errors = self.check_counter_examples_section(counter_content)
            if not has_counter:
                errors.extend([f"Examples That Do NOT Belong: {e}" for e in counter_errors])
        
        # Additional validation: Check for placeholder text
        if 'Example 4' in content or 'Example 5' in content:
            warnings.append("File contains placeholder example text that should be replaced")
        if 'Misplaced Project' in content:
            warnings.append("File contains placeholder counter-example text that should be replaced")
        if 'To be determined' in content:
            warnings.append("File contains 'To be determined' text that should be updated")
        
        return ValidationResult(
            file_path=str(file_path),
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def lint_all_files(self, root_dir: str = ".") -> Tuple[int, int, int]:
        """Lint all markdown files and return counts of valid, invalid, and total files"""
        md_files = self.find_markdown_files(root_dir)
        
        if not md_files:
            print("No what-belongs-here*.md files found.")
            return 0, 0, 0
        
        print(f"Found {len(md_files)} markdown files to validate\n")
        print("=" * 80)
        
        for file_path in md_files:
            result = self.validate_file(file_path)
            self.results.append(result)
            
            # Print result for this file
            relative_path = os.path.relpath(file_path, root_dir)
            
            if result.is_valid and not result.warnings:
                print(f"✓ {relative_path} - VALID")
            elif result.is_valid and result.warnings:
                print(f"⚠ {relative_path} - VALID WITH WARNINGS")
                for warning in result.warnings:
                    print(f"  ⚠ {warning}")
            else:
                print(f"✗ {relative_path} - INVALID")
                for error in result.errors:
                    print(f"  ✗ {error}")
                if result.warnings:
                    for warning in result.warnings:
                        print(f"  ⚠ {warning}")
            print()
        
        # Summary
        valid_count = sum(1 for r in self.results if r.is_valid)
        invalid_count = sum(1 for r in self.results if not r.is_valid)
        warning_count = sum(1 for r in self.results if r.warnings)
        
        print("=" * 80)
        print("\nVALIDATION SUMMARY:")
        print(f"  Total files checked: {len(self.results)}")
        print(f"  ✓ Valid files: {valid_count}")
        print(f"  ✗ Invalid files: {invalid_count}")
        print(f"  ⚠ Files with warnings: {warning_count}")
        
        return valid_count, invalid_count, len(self.results)
    
    def generate_report(self, output_file: str = "lint_report.txt"):
        """Generate a detailed report of all validation results"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("MARKDOWN FILE VALIDATION REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            # Invalid files section
            invalid_results = [r for r in self.results if not r.is_valid]
            if invalid_results:
                f.write("FILES REQUIRING MANUAL REVIEW (INVALID):\n")
                f.write("-" * 40 + "\n\n")
                for result in invalid_results:
                    f.write(f"File: {result.file_path}\n")
                    f.write("Errors:\n")
                    for error in result.errors:
                        f.write(f"  - {error}\n")
                    if result.warnings:
                        f.write("Warnings:\n")
                        for warning in result.warnings:
                            f.write(f"  - {warning}\n")
                    f.write("\n")
            
            # Files with warnings
            warning_results = [r for r in self.results if r.is_valid and r.warnings]
            if warning_results:
                f.write("\nFILES WITH WARNINGS (VALID BUT COULD BE IMPROVED):\n")
                f.write("-" * 40 + "\n\n")
                for result in warning_results:
                    f.write(f"File: {result.file_path}\n")
                    f.write("Warnings:\n")
                    for warning in result.warnings:
                        f.write(f"  - {warning}\n")
                    f.write("\n")
            
            # Summary
            valid_count = sum(1 for r in self.results if r.is_valid)
            invalid_count = sum(1 for r in self.results if not r.is_valid)
            warning_count = sum(1 for r in self.results if r.warnings)
            
            f.write("\nSUMMARY:\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total files checked: {len(self.results)}\n")
            f.write(f"Valid files: {valid_count}\n")
            f.write(f"Invalid files: {invalid_count}\n")
            f.write(f"Files with warnings: {warning_count}\n")
        
        print(f"\nDetailed report saved to: {output_file}")


def main():
    """Main entry point"""
    linter = MarkdownLinter()
    
    # Get root directory from command line or use current directory
    root_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    
    # Run the linter
    valid, invalid, total = linter.lint_all_files(root_dir)
    
    # Generate detailed report if there are any issues
    if invalid > 0 or any(r.warnings for r in linter.results):
        linter.generate_report()
    
    # Exit with error code if any files are invalid
    sys.exit(0 if invalid == 0 else 1)


if __name__ == "__main__":
    main()
