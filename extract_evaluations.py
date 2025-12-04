#!/usr/bin/env python3
"""
Performance Evaluation Extractor
Extracts structured data from webarchive evaluation files for LLM analysis
"""

import plistlib
import json
import re
from html import unescape
from pathlib import Path
from typing import Dict, List, Any
from bs4 import BeautifulSoup


class EvaluationExtractor:
    """Extract evaluation data from webarchive HTML files"""

    COMPETENCIES = ["TECH EXCELLENCE", "TEAMWORK", "CUSTOMER CHAMPION", "GROWTH MINDSET"]

    def __init__(self, webarchive_path: str):
        self.webarchive_path = Path(webarchive_path)
        self.html_content = None
        self.soup = None

    def extract_html_from_webarchive(self) -> str:
        """Extract HTML content from macOS webarchive file"""
        with open(self.webarchive_path, 'rb') as f:
            plist = plistlib.load(f)

        main_resource = plist.get('WebMainResource', {})
        html_data = main_resource.get('WebResourceData', b'')

        self.html_content = html_data.decode('utf-8')
        self.soup = BeautifulSoup(self.html_content, 'html.parser')
        return self.html_content

    def extract_employee_info(self) -> Dict[str, Any]:
        """Extract employee name, role, and overall metrics"""
        info = {}

        # Extract name
        name_elem = self.soup.find('b', class_='sender-name')
        info['name'] = name_elem.text.strip() if name_elem else "Unknown"

        # Extract role (next sibling span after name)
        if name_elem:
            parent = name_elem.find_parent()
            role_span = parent.find('span', style=lambda x: x and 'white-space' in x)
            info['role'] = role_span.text.strip() if role_span else "Unknown"

        # Extract total average
        avg_elem = self.soup.find('span', id='total_average_received')
        info['total_average'] = float(avg_elem.text.strip()) if avg_elem and avg_elem.text.strip() else None

        # Extract evaluation counts
        count_elem = self.soup.find('span', id='total-assessment-message')
        if count_elem:
            text = count_elem.text.strip()
            # Parse "Total Received 9, Total Given 5"
            received = re.search(r'Total Received (\d+)', text)
            given = re.search(r'Total Given (\d+)', text)
            info['evaluations_received'] = int(received.group(1)) if received else 0
            info['evaluations_given'] = int(given.group(1)) if given else 0

        return info

    def count_stars(self, star_container) -> int:
        """Count filled stars in a rating"""
        filled_stars = star_container.find_all('i', class_='fa-star',
                                               style=lambda x: x and '#ffd963' in x)
        return len(filled_stars)

    def extract_note(self, question_div) -> str:
        """Extract note from question if present"""
        note_span = question_div.find('span', class_='tooltip-behaviour-note')
        if note_span and 'data-content' in note_span.attrs:
            # Decode HTML entities
            encoded_content = note_span['data-content']
            decoded = unescape(encoded_content)
            # Remove HTML tags
            clean = re.sub(r'<[^>]+>', '', decoded)
            return clean.strip()
        return ""

    def extract_questions(self, category_div) -> List[Dict[str, Any]]:
        """Extract all questions and ratings from a competency category"""
        questions = []

        # Find all question blocks
        question_blocks = category_div.find_all('div', class_='assessment-behavior-description')

        i = 0
        while i < len(question_blocks):
            block = question_blocks[i]

            # Check if this is a question text block (has a <p> with the question)
            question_p = block.find('p', style=lambda x: x and 'padding-right' in x)

            if question_p and i + 1 < len(question_blocks):
                question_text = question_p.text.strip()

                # Next block should have the rating
                rating_block = question_blocks[i + 1]

                # Find stars
                star_div = rating_block.find('div', style=lambda x: x and 'font-size: 18px' in x)
                stars = self.count_stars(star_div) if star_div else 0

                # Find level description (bold text after stars)
                level_b = rating_block.find('b', style=lambda x: x and 'padding-left' in x)
                level_desc = level_b.text.strip() if level_b else ""

                # Extract note if present
                note = self.extract_note(rating_block)

                questions.append({
                    'question': question_text,
                    'stars': stars,
                    'level_description': level_desc,
                    'note': note
                })

                i += 2  # Skip to next question
            else:
                i += 1

        return questions

    def extract_competency_data(self, evaluation_div) -> Dict[str, List[Dict]]:
        """Extract all 4 competency categories from an evaluation"""
        competencies = {}

        for comp_name in self.COMPETENCIES:
            # Find the competency section
            comp_header = evaluation_div.find('p', string=lambda x: x and comp_name in x)
            if comp_header:
                comp_container = comp_header.find_parent('div', class_='rectangle-behavior')
                if comp_container:
                    questions = self.extract_questions(comp_container)
                    competencies[comp_name] = questions

        return competencies

    def extract_strengths_weaknesses(self, evaluation_div) -> Dict[str, List[str]]:
        """Extract strengths and weaknesses lists"""
        result = {'strengths': [], 'weaknesses': []}

        # Find Strengths section
        strengths_header = evaluation_div.find('p', string=lambda x: x and x.strip() == 'Strengths')
        if strengths_header:
            strengths_container = strengths_header.find_parent('div', class_='rectangle-behavior')
            if strengths_container:
                items = strengths_container.find_all('li', class_='assessment-name-in-list')
                result['strengths'] = [item.text.strip() for item in items]

        # Find Weaknesses section
        weaknesses_header = evaluation_div.find('p', string=lambda x: x and x.strip() == 'Weaknesses')
        if weaknesses_header:
            weaknesses_container = weaknesses_header.find_parent('div', class_='rectangle-behavior')
            if weaknesses_container:
                items = weaknesses_container.find_all('li', class_='assessment-name-in-list')
                result['weaknesses'] = [item.text.strip() for item in items]

        return result

    def extract_additional_thoughts(self, evaluation_div) -> str:
        """Extract additional thoughts section"""
        thoughts_header = evaluation_div.find('p', string=lambda x: x and 'Any additional thoughts' in x)
        if thoughts_header:
            thoughts_container = thoughts_header.find_parent('div', class_='rectangle-behavior')
            if thoughts_container:
                thoughts_p = thoughts_container.find('p', style=lambda x: x and 'word-break' in x)
                if thoughts_p:
                    return thoughts_p.text.strip()
        return ""

    def determine_evaluator_type(self, evaluator_name: str, employee_name: str, evaluator_role: str = "") -> str:
        """Determine if evaluator is self, peer, or client"""
        if evaluator_name.lower() == employee_name.lower():
            return "self"

        # Check if role contains "Client" keyword
        if evaluator_role and "client" in evaluator_role.lower():
            return "client"

        # Otherwise, mark as peer
        return "peer"

    def extract_single_evaluation(self, panel_div, employee_name: str) -> Dict[str, Any]:
        """Extract data from a single evaluation panel"""
        evaluation = {}

        # Extract evaluator info from panel heading
        heading = panel_div.find('div', class_='panel-heading')
        if heading:
            evaluator_name_elem = heading.find('span', class_='assessment-name-list')
            evaluator_role_elem = heading.find('span', class_='assessment-role-list')
            average_elem = heading.find('b', string=lambda x: x and 'average' in x)

            evaluation['evaluator_name'] = evaluator_name_elem.text.strip() if evaluator_name_elem else "Unknown"
            evaluation['evaluator_role'] = evaluator_role_elem.text.strip() if evaluator_role_elem else "Unknown"

            # Extract evaluation average
            if average_elem:
                avg_text = average_elem.text.strip()
                avg_match = re.search(r'([\d.]+)', avg_text)
                evaluation['evaluation_average'] = float(avg_match.group(1)) if avg_match else None

            # Determine evaluator type
            evaluation['evaluator_type'] = self.determine_evaluator_type(
                evaluation['evaluator_name'],
                employee_name,
                evaluation.get('evaluator_role', '')
            )

        # Extract panel body content
        body = panel_div.find('div', class_='panel-body')
        if body:
            evaluation['competencies'] = self.extract_competency_data(body)
            evaluation.update(self.extract_strengths_weaknesses(body))
            evaluation['additional_thoughts'] = self.extract_additional_thoughts(body)

        return evaluation

    def extract_all_evaluations(self) -> List[Dict[str, Any]]:
        """Extract all evaluations from the document"""
        evaluations = []

        # Get employee name for evaluator type determination
        employee_info = self.extract_employee_info()
        employee_name = employee_info['name']

        # Find all evaluation panels
        panels = self.soup.find_all('div', class_='panel panel-default',
                                    style=lambda x: x and 'border-color: transparent' in x)

        for panel in panels:
            # Check if this is an evaluation panel (has assessment data)
            panel_body = panel.find('div', class_='panel-body')
            if panel_body and panel_body.find('div', class_='assessment-capability-description'):
                evaluation = self.extract_single_evaluation(panel, employee_name)
                evaluations.append(evaluation)

        return evaluations

    def extract_all_data(self) -> Dict[str, Any]:
        """Extract complete evaluation data structure"""
        self.extract_html_from_webarchive()

        data = {
            'employee': self.extract_employee_info(),
            'evaluations': self.extract_all_evaluations()
        }

        return data


def process_webarchive(webarchive_path: str, output_json_path: str = None) -> Dict[str, Any]:
    """
    Process a webarchive file and extract all evaluation data

    Args:
        webarchive_path: Path to the .webarchive file
        output_json_path: Optional path to save JSON output

    Returns:
        Dictionary containing all extracted evaluation data
    """
    extractor = EvaluationExtractor(webarchive_path)
    data = extractor.extract_all_data()

    # Optionally save to JSON
    if output_json_path:
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to: {output_json_path}")

    return data


def process_directory(directory_path: str, output_dir: str = None):
    """
    Process all .webarchive files in a directory

    Args:
        directory_path: Directory containing .webarchive files
        output_dir: Optional directory to save JSON outputs
    """
    directory = Path(directory_path)
    webarchive_files = list(directory.glob("*.webarchive"))

    if not webarchive_files:
        print(f"No .webarchive files found in {directory_path}")
        return

    print(f"Found {len(webarchive_files)} webarchive file(s)")

    results = {}

    for webarchive_file in webarchive_files:
        print(f"\nProcessing: {webarchive_file.name}")

        try:
            # Generate output filename
            output_json = None
            if output_dir:
                output_dir_path = Path(output_dir)
                output_dir_path.mkdir(exist_ok=True)
                output_json = output_dir_path / f"{webarchive_file.stem}.json"

            # Extract data
            data = process_webarchive(str(webarchive_file),
                                     str(output_json) if output_json else None)

            employee_name = data['employee']['name']
            results[employee_name] = data

            print(f"  ✓ Extracted data for: {employee_name}")
            print(f"    - Role: {data['employee']['role']}")
            print(f"    - Total Average: {data['employee']['total_average']}")
            print(f"    - Evaluations: {len(data['evaluations'])}")

        except Exception as e:
            print(f"  ✗ Error processing {webarchive_file.name}: {e}")
            import traceback
            traceback.print_exc()

    return results


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python extract_evaluations.py <webarchive_file_or_directory> [output_json_or_directory]")
        print("\nExamples:")
        print("  python extract_evaluations.py 'Alan Reskin.webarchive'")
        print("  python extract_evaluations.py 'Alan Reskin.webarchive' 'alan_data.json'")
        print("  python extract_evaluations.py . json_output/")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    input_path_obj = Path(input_path)

    if input_path_obj.is_file():
        # Process single file
        data = process_webarchive(input_path, output_path)
        print(f"\n✓ Successfully extracted evaluation data for: {data['employee']['name']}")
    elif input_path_obj.is_dir():
        # Process directory
        results = process_directory(input_path, output_path)
        print(f"\n✓ Successfully processed {len(results)} employee evaluation(s)")
    else:
        print(f"Error: {input_path} is not a valid file or directory")
        sys.exit(1)
