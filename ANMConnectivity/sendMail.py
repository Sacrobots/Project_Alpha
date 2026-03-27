import pythoncom
import win32com.client as win32
from LoadData import data

def sendOutlookMail(send_immediately: bool = True):

    # Validate required fields early
    required_keys = ["Env_No", "ANM_IP"]
    missing = [k for k in required_keys if k not in data or not str(data[k]).strip()]
    if missing:
        raise ValueError(f"Missing required data keys: {', '.join(missing)}")

    pythoncom.CoInitialize()
    try:

        outlook = win32.gencache.EnsureDispatch('Outlook.Application')
        mail = outlook.CreateItem(0)

        mail.To = "saisiddg@amdocs.com"
        env_no = str(data['Env_No']).strip() if 'Env_No' in data else ''
        mail.Subject = f"ENV-{env_no} | Add ANM Configuration Request"

        mail.HTMLBody = f"""\
                <!DOCTYPE html>
                <html>
                  <body style="margin:0; padding:0; background-color:#f4f6f8;">
                    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f6f8; padding:20px;">
                      <tr>
                        <td align="center">
                          <table width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff; border:1px solid #e1e4e8; border-radius:6px;">
                            <!-- Header -->
                            <tr>
                              <td style="padding:14px 24px; border-bottom:1px solid #e1e4e8;">
                                <span style="font-family:Segoe UI, Arial, sans-serif; font-size:16px; color:#1f2933; font-weight:600;">
                                  ANM Environment Connection Request
                                </span>
                              </td>
                            </tr>
                
                            <!-- Body -->
                            <tr>
                              <td style="padding:18px 24px; font-family:Segoe UI, Arial, sans-serif; font-size:14px; color:#333333; line-height:1.5;">
                                <p style="margin:0 0 8px 0;">Hi <strong>ANM Team</strong>,</p>
                                <br/>
                                <p style="margin:0 0 10px 0;">
                                  Could you please assist in connecting <strong>ANM</strong> to the environment detailed below
                                </p>
                
                                <p style="margin:8px 0; color:#9aa5b1;">------------------------------------------------------------------------</p>
                
                                <table cellpadding="4" cellspacing="0" style="border-collapse:collapse; font-family:Segoe UI, Arial, sans-serif; font-size:14px;">
                                  <tr>
                                    <td><strong>Environment No: {env_no}</strong></td>
                                  </tr>
                                  <tr>
                                    <td><strong>ANM IP: {data['ANM_IP']}</strong></td>
                                  </tr>
                                </table>
                
                                <p style="margin:8px 0; color:#9aa5b1;">------------------------------------------------------------------------</p>
                                <br/>
                
                                <p style="margin:0;">
                                  Thanks &amp; regards,<br/>
                                  <strong>Sai Siddharth</strong>
                                </p>
                              </td>
                            </tr>
                
                          </table>
                        </td>
                      </tr>
                    </table>
                  </body>
                </html>
                """


        if send_immediately:
            mail.Send()
        else:
            mail.Display(False)

    finally:
        pythoncom.CoUninitialize()
