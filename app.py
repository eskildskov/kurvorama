from flask import Flask, request, render_template, Response
from fpdf import FPDF
import textwrap, os

LARGE_FONT_SIZE = 10
SMALL_FONT_SIZE = 8

app = Flask(__name__)

@app.route("/", methods=('GET', 'POST'))
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

def create_pdf(faste_medisiner, behovsmedisiner) :
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', LARGE_FONT_SIZE)

    while faste_medisiner or behovsmedisiner:
        pdf.add_page()

        pos_y = 106.5 # Start faste medisiner
        pdf.set_xy(11, pos_y)

        i = 1
        while faste_medisiner and i <= 15 :
            medisin = faste_medisiner.pop(0)
            medisin = '→ ' + medisin

            if len(medisin) > 30 :
                pdf.set_font_size(SMALL_FONT_SIZE) # go small

                if len(medisin) > 40 : # go multi line!
                    medisin = textwrap.fill(medisin, 40)
                    medisin_lines = medisin.splitlines()

                    pos_y -= 2
                    pdf.set_xy(11, pos_y)
                    pdf.cell(10, 10, medisin_lines[0], 0)
                    pos_y += 3
                    pdf.set_xy(11, pos_y)
                    pdf.cell(10, 10, medisin_lines[1], 0)
                    pos_y = pos_y + 7.9

                else : # go single line
                    pdf.cell(10, 10, medisin, 0)
                    pos_y = pos_y + 8.9

                pdf.set_font_size(LARGE_FONT_SIZE)

            else :
                pdf.cell(40, 10, medisin, 0)
                pos_y = pos_y + 8.9

            pdf.set_xy(11, pos_y)
            i += 1

        pdf.add_page()
        pdf.set_auto_page_break(False)

        # Behovsmedisiner
        pdf.set_font_size(LARGE_FONT_SIZE)
        pos_y = 233
        pdf.set_xy(4, pos_y)

        i = 1
        while behovsmedisiner and i <= 10 :
            medisin = behovsmedisiner.pop(0)
            medisin = '→ ' + medisin

            pdf.cell(40, 10, medisin, 0)
            pos_y = pos_y + 5.5
            pdf.set_xy(4, pos_y)

            i += 1

    return pdf.output(name = 'kurve', dest = 'S').encode('latin-1')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)
