# finance/utils.py
import os
from django.template.loader import render_to_string
from django.conf import settings

def generate_fee_receipt_html(payment):
    """
    Generates structured HTML for a fee payment receipt that can be 
    printed or exported directly from the admin panel.
    """
    context = {
        'receipt_number': f"WATO-REC-{payment.id:05d}",
        'date': payment.payment_date,
        'student': payment.student_fee.student,
        'fee_category': payment.student_fee.fee_category.name,
        'amount_paid': payment.amount_paid,
        'payment_method': payment.get_payment_method_display(),
        'reference_number': payment.reference_number or 'N/A',
        'received_by': payment.received_by.get_full_name() if payment.received_by else 'Admin',
        'school_name': 'Wato Secondary School',
        'school_po_box': 'P.O. Box 123, Oromia, Ethiopia',
    }
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Fee Receipt - {context['receipt_number']}</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #1e293b; margin: 0; padding: 20px; }}
            .receipt-box {{ max-width: 700px; margin: auto; border: 2px solid #059669; border-radius: 8px; padding: 30px; background: #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
            .header {{ text-align: center; border-bottom: 2px solid #e2e8f0; padding-bottom: 15px; margin-bottom: 20px; }}
            .header h1 {{ color: #059669; font-size: 24px; margin: 0; }}
            .header p {{ font-size: 13px; color: #64748b; margin: 4px 0; }}
            .details-grid {{ display: flex; justify-content: space-between; margin-bottom: 20px; font-size: 14px; }}
            .details-grid div {{ width: 48%; }}
            .details-grid p {{ margin: 6px 0; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; }}
            th, td {{ border: 1px solid #cbd5e1; padding: 10px; text-align: left; }}
            th {{ background: #059669; color: white; }}
            .total-section {{ text-align: right; font-size: 16px; font-weight: bold; margin-top: 15px; color: #064e3b; }}
            .footer {{ margin-top: 40px; text-align: center; font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0; padding-top: 15px; }}
            .signature-box {{ display: flex; justify-content: space-between; margin-top: 50px; font-size: 14px; }}
            .signature-line {{ width: 200px; border-top: 1px solid #334155; text-align: center; padding-top: 5px; }}
        </style>
    </head>
    <body>
        <div class="receipt-box">
            <div class="header">
                <h1>{context['school_name']}</h1>
                <p>{context['school_po_box']}</p>
                <p><strong>OFFICIAL FEE PAYMENT RECEIPT</strong></p>
            </div>
            
            <div class="details-grid">
                <div>
                    <p><strong>Receipt No:</strong> {context['receipt_number']}</p>
                    <p><strong>Date:</strong> {context['date']}</p>
                    <p><strong>Payment Method:</strong> {context['payment_method']}</p>
                </div>
                <div>
                    <p><strong>Student Name:</strong> {context['student']}</p>
                    <p><strong>Reference / TxID:</strong> {context['reference_number']}</p>
                    <p><strong>Received By:</strong> {context['received_by']}</p>
                </div>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>Fee Category / Description</th>
                        <th>Status</th>
                        <th style="text-align: right;">Amount Paid (ETB)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{context['fee_category']}</td>
                        <td>Paid in Full / Verified</td>
                        <td style="text-align: right;">{context['amount_paid']:,.2f}</td>
                    </tr>
                </tbody>
            </table>

            <div class="total-section">
                Total Paid: ETB {context['amount_paid']:,.2f}
            </div>

            <div class="signature-box">
                <div>
                    <div class="signature-line">Student / Payer Signature</div>
                </div>
                <div>
                    <div class="signature-line">Authorized Cashier Stamp</div>
                </div>
            </div>

            <div class="footer">
                Thank you for your payment. This is a computer-generated official receipt from Wato IMS.
            </div>
        </div>
    </body>
    </html>
    """
    return html_content