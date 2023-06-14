import os
from weasyprint import HTML
from kpi_reunion.common.kpir_assets_config import KPIRAssetsConfig
from pf_py_file.pfpf_file_util import FileUtil


class PDFService:

    def generate_pdf(self, file_name, content):
        FileUtil.create_directories(KPIRAssetsConfig.pdf)
        content = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta http-equiv="content-type" content="text/html; charset=utf-8"> 
                    </head>
                        <body>
                            {content}    
                        </body>
                    </html>
                """
        file_path = os.path.join(KPIRAssetsConfig.pdf, f"{file_name}.pdf")
        # file_path = os.path.join(KPIRAssetsConfig.pdf, f"{file_name}.pdf")
        HTML(string=content, encoding="utf-8").write_pdf(file_path)
        # pdfkit.from_string(content, file_path)
        # print(content)
        # TextFileMan.write_text_to_file(os.path.join(KPIRAssetsConfig.pdf, f"{file_name}.html"), text_content=content)
        return file_path
