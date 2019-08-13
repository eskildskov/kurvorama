from flask import Flask, request, render_template, Response
from fpdf import FPDF
import textwrap

application = Flask(__name__)

@application.route("/", methods=('GET', 'POST'))
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        faste = request.form['faste_medisiner'].splitlines()
        behov = request.form['behovsmedisiner'].splitlines()

        pdf = create_pdf(faste, behov)

        response = Response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=%s.pdf' % 'Kurve'
        return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)


def create_pdf(faste_medisiner, behovsmedisiner) :
    pdf = FPDF('P', 'mm', 'A4')

    while faste_medisiner or behovsmedisiner:
        pdf.add_page()
        pdf.set_font('Arial', '', 10)
        pos = 106.5 # Start faste medisiner
        pdf.set_xy(11, pos)

        i = 1
        while faste_medisiner and i <= 15 :
            medisin = faste_medisiner.pop(0)

            if len(medisin) > 30 :
                pdf.set_font('Arial', '', 8) # go small

                if len(medisin) > 40 : # go multi line!
                    medisin = textwrap.fill(medisin, 40)
                    medisin_lines = medisin.splitlines()

                    orig_pos = pos
                    pos -= 2
                    pdf.set_xy(11, pos)
                    pdf.cell(10, 10, medisin_lines[0], 0)
                    pos += 3
                    pdf.set_xy(11, pos)
                    pdf.cell(10, 10, medisin_lines[1], 0)
                    pos = pos + 7.9

                else : # go single line
                    pdf.cell(10, 10, medisin, 0)
                    pos = pos + 8.9

                pdf.set_font('Arial', '', 10)
                # pdf.set_xy(11, orig_pos)

            else :
                pdf.cell(40, 10, medisin, 0)
                pos = pos + 8.9

            pdf.set_xy(11, pos)
            i += 1

        pdf.add_page()
        pdf.set_auto_page_break(False)

        pdf.set_font('Arial', '', 10)
        pos = 233 # Start behovsmedisiner
        pdf.set_xy(4, pos)

        i = 1
        while behovsmedisiner and i <= 10 :
            medisin = behovsmedisiner.pop(0)
            pdf.cell(40, 10, medisin, 0)
            pos = pos + 5.5
            pdf.set_xy(4, pos)

            i += 1

    return pdf.output(name = 'kurve', dest = 'S').encode('latin-1')
