import datetime
from django.http import FileResponse

from fpdf import FPDF
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def create_pdf_report(serializer, request_params_serializer):
    pdf = FPDF("P", "mm", "A4")
    pdf.add_page()
    pdf.set_font("courier", "B", 16)
    pdf.cell(40, 10, "Booked room reports:", 0, 1)
    pdf.cell(40, 10, "", 0, 1)
    pdf.set_font("courier", "", 12)
    pdf.cell(200, 8, f"{'room'.ljust(32)} {'checking_date'.rjust(10)} {'checkout_date'.rjust(10)} {'owner'.rjust(10)}", 0, 1)
    pdf.line(10, 30, 190, 30)
    pdf.line(10, 38, 190, 38)
    for line in serializer.data:
        pdf.cell(
            200,
            8,
            f"{str(line['room']).ljust(32)} {line['checking_date'].rjust(10)} {line['checkout_date'].rjust(10)} {line['owner'].rjust(10)}",
            0,
            1,
        )
    start, end = request_params_serializer.get(
        "start_date"
    ), request_params_serializer.get("end_date")
    file_name = f"{str(datetime.datetime.now())}_{start}_{end}"
    pdf.output(f"{BASE_DIR}/reports/{file_name}.pdf", "F")

    return FileResponse(
        open(f"{BASE_DIR}/reports/{file_name}.pdf", "rb"),
        as_attachment=True,
        content_type="application/pdf",
    )
