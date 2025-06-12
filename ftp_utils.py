from ftplib import FTP
import io
import datetime

def get_ca_info(ca_number: str):
    ftp = FTP('ftp.mtps.gov.br')
    ftp.login()
    ftp.cwd('/portal/fiscalizacao/seguranca-e-saude-no-trabalho/caepi')

    # Baixa o arquivo .txt diretamente em memória
    file_buffer = io.BytesIO()
    ftp.retrbinary('RETR tgg_export_caepi.txt', file_buffer.write)
    ftp.quit()

    # Decodifica para texto
    file_buffer.seek(0)
    lines = file_buffer.read().decode('latin-1').splitlines()

    # Pega o cabeçalho (opcional)
    header = lines[0].split(';')

    for line in lines[1:]:
        fields = line.split(';')
        if fields[0] == ca_number:
            nome = fields[1]  # Ajustar se for outro índice
            validade_str = fields[4]  # Ajustar se necessário
            try:
                validade = datetime.datetime.strptime(validade_str, "%d/%m/%Y").date()
                situacao = "Vencido" if validade < datetime.date.today() else "Válido"
            except:
                validade = validade_str
                situacao = "Desconhecido"
            return {
                "ca": ca_number,
                "nome": nome,
                "validade": validade_str,
                "situacao": situacao
            }

    return None