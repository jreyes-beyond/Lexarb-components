from typing import Dict, List, Optional
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os

class TemplateEngine:
    def __init__(self, templates_dir: str = "templates/awards"):
        """
        Initialize the template engine with a templates directory.
        
        Args:
            templates_dir: Directory containing award templates
        """
        self.templates_dir = templates_dir
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def get_template_list(self) -> List[str]:
        """Get a list of available award templates."""
        return self.env.list_templates()

    def render_award_section(
        self,
        template_name: str,
        section_data: Dict,
        case_data: Optional[Dict] = None
    ) -> str:
        """
        Render a specific award section using a template.
        
        Args:
            template_name: Name of the template file
            section_data: Data specific to the section
            case_data: Optional case-wide data
            
        Returns:
            Rendered section content
        """
        template = self.env.get_template(template_name)
        context = {
            "section": section_data,
            "case": case_data or {},
            "now": datetime.utcnow()
        }
        return template.render(**context)

    def render_full_award(
        self,
        sections: List[Dict],
        case_data: Dict,
        template_name: str = "base_award.j2"
    ) -> str:
        """
        Render a complete award document with all sections.
        
        Args:
            sections: List of section data
            case_data: Case-wide data
            template_name: Base template name
            
        Returns:
            Complete rendered award document
        """
        template = self.env.get_template(template_name)
        context = {
            "sections": sections,
            "case": case_data,
            "now": datetime.utcnow()
        }
        return template.render(**context)

    def validate_template(self, template_name: str) -> bool:
        """
        Validate that a template exists and is properly formatted.
        
        Args:
            template_name: Name of template to validate
            
        Returns:
            True if template is valid
        """
        try:
            self.env.get_template(template_name)
            return True
        except Exception:
            return False