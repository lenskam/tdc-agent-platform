import os
import json
import logging
from datetime import datetime
from langchain_core.tools import tool
from typing import Optional
from ..database.postgres import SessionLocal
from ..database.models import Project, Task

logger = logging.getLogger(__name__)

REPORTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)


class ReportingTool:
    @tool("generate_project_report")
    def generate_project_report(project_id: int) -> str:
        """
        Generates a text summary of the project status.
        """
        db = SessionLocal()
        try:
            project = db.query(Project).filter(Project.id == project_id).first()
            if not project:
                return "Project not found."
            
            tasks = db.query(Task).filter(Task.project_id == project_id).all()
            total = len(tasks)
            done = len([t for t in tasks if t.status.value == 'done'])
            
            report = f"""
# Project Status Report: {project.name}
**Client**: {project.client_name}
**Progress**: {done}/{total} Tasks Completed

## Tasks Detail
"""
            for t in tasks:
                 report += f"- {t.title}: {t.status.value}\n"
                 
            return report
        except Exception as e:
            return f"Error generating report: {e}"
        finally:
            db.close()

    @tool("generate_pdf_report")
    def generate_pdf_report(project_id: int) -> str:
        """
        Generates a PDF report for a project and saves it to the reports directory.
        Returns the file path to the generated PDF.
        """
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib import colors
        except ImportError:
            return "Error: reportlab not installed. Run: pip install reportlab"

        db = SessionLocal()
        try:
            project = db.query(Project).filter(Project.id == project_id).first()
            if not project:
                return "Project not found."

            tasks = db.query(Task).filter(Task.project_id == project_id).all()
            
            filename = f"project_{project_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = os.path.join(REPORTS_DIR, filename)
            
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            title = Paragraph(f"<b>Project Status Report: {project.name}</b>", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 12))
            
            info = Paragraph(
                f"<b>Client:</b> {project.client_name or 'N/A'}<br/>"
                f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                styles['Normal']
            )
            story.append(info)
            story.append(Spacer(1, 20))
            
            task_data = [['Task', 'Status', 'Priority', 'Assigned To']]
            for t in tasks:
                task_data.append([
                    t.title[:40] + '...' if len(t.title) > 40 else t.title,
                    t.status.value,
                    t.priority,
                    t.assigned_to or 'Unassigned'
                ])
            
            table = Table(task_data, colWidths=[250, 80, 60, 80])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(table)
            
            doc.build(story)
            logger.info(f"PDF report generated: {filepath}")
            
            return json.dumps({
                "success": True,
                "filepath": filepath,
                "filename": filename,
                "download_url": f"/reports/{filename}"
            })
            
        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            return json.dumps({"success": False, "error": str(e)})
        finally:
            db.close()


reporting_tools = [ReportingTool.generate_project_report, ReportingTool.generate_pdf_report]
