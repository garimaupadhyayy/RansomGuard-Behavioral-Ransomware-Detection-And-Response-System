"""
PDF incident report generator.
"""
import os
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def generate_incident_report(incident: dict, alerts: list, output_dir: str = "./reports_output") -> str:
    os.makedirs(output_dir, exist_ok=True)
    filename = f"incident_{incident.get('id', 'unknown')}_{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}.pdf"
    path = os.path.join(output_dir, filename)

    doc = SimpleDocTemplate(path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("RansomGuard Incident Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    info_rows = [
        ["Incident ID", str(incident.get("id", "N/A"))],
        ["Title", incident.get("title", "N/A")],
        ["Hostname", incident.get("hostname", "N/A")],
        ["User", incident.get("user", "N/A")],
        ["Status", incident.get("status", "N/A")],
        ["Started At", str(incident.get("started_at", "N/A"))],
        ["Resolved At", str(incident.get("resolved_at", "N/A"))],
    ]
    info_table = Table(info_rows, colWidths=[150, 350])
    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Alerts in this Incident", styles["Heading2"]))
    elements.append(Spacer(1, 8))

    alert_rows = [["Score", "Severity", "Process", "File", "MITRE", "Action Taken"]]
    for a in alerts:
        alert_rows.append([
            str(a.get("score", "")),
            a.get("severity", ""),
            a.get("process_name", "") or "-",
            a.get("file_path", "") or "-",
            a.get("mitre_techniques", "") or "-",
            a.get("action_taken", "") or "-",
        ])
    alert_table = Table(alert_rows, colWidths=[40, 55, 80, 130, 80, 100])
    alert_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
    ]))
    elements.append(alert_table)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Recommendations", styles["Heading2"]))
    elements.append(Paragraph(
        "Review the affected endpoint for persistence mechanisms, rotate any credentials "
        "that may have been exposed, confirm backup integrity, and update detection rules "
        "based on the observed technique(s) above.", styles["Normal"]
    ))

    doc.build(elements)
    return path
