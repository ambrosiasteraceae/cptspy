import matplotlib.pyplot as plt
import subprocess
import os
from pylatex import Document, Section, Subsection, Command,\
    Tabular, Figure, NewPage, Head, MiniPage, StandAloneGraphic,\
    LargeText, PageStyle, MediumText, LineBreak, SmallText
from pylatex.utils import NoEscape, bold

from load.loading import load_cpt_header, load_mpa_cpt_file #CREATE cpt_file module
from calc.liquefaction import run_rw1997
from calc.summary import CPTSummary
from miscellaneous.figures import create_fos_and_index_plot, create_compactibilty_plot, \
    create_cpt_plots, create_massarasch_and_legend_plot

import io

paths = ['C:/Users/dragos/Documents/GitHub/cptspy/output/CPT_L21d.csv']
# import glob
# paths = glob.glob('D:/04_R&D/cptspy/read/roshna/post data/processed/' + '*.csv')
#

gpath = 'C:/Users/dragos/Documents/GitHub/cptspy/report/pdfs/'
if not os.path.exists(gpath):
    os.makedirs(gpath)
gpath = ''

def generate_table(_dict):
    table = Tabular('ll')
    table.add_hline()
    for i, (k, v) in enumerate(_dict.items()):
        if i % 2 == 0:

            table.append(NoEscape(r'\rowcolor{gray!25}'))
        table.add_row([k, v])
    table.add_hline()
    return table

pga = 0.122
m_w = 6
GWL = 0.6
gwl = 0.6
scf = 1.30
my_list = []
for path in paths:
    cpt = load_mpa_cpt_file(path, scf=scf)
    gwl = cpt.elevation[0] - GWL
    my_list.append((path, gwl, cpt.elevation[0]))
    rw_1997 = run_rw1997(cpt, pga=pga, m_w=m_w, gwl=gwl)
    cpth = load_cpt_header(path)
    cpts = CPTSummary(rw_1997)


    #
    fig, sps = plt.subplots(nrows=1, ncols=3, figsize=(16, 10))
    create_fos_and_index_plot(sps, rw_1997)
    fig.savefig(gpath+cpth.name + '.png', bbox_inches='tight')

    fig2, ax = plt.subplots(nrows=1, ncols=1, figsize=(4, 4))
    create_compactibilty_plot(ax, rw_1997)
    fig2.savefig(gpath+cpth.name + '_compactibility.png', bbox_inches='tight')

    fig3, axs = plt.subplots(1, 4, figsize=(16, 12), sharey=True)
    create_cpt_plots(axs, cpt)
    fig3.savefig(gpath+cpth.name + '_basicplot.png')

    fig4, axes = plt.subplots(1, 3, figsize=(16, 4))
    create_massarasch_and_legend_plot(axes, rw_1997)
    fig4.savefig(gpath+'legends.png',bbox_inches='tight')

    logo_image_path = 'nmdc.jpg'
    cpt_file_path = '/load/H15c.png'

    path = os.path.dirname(__file__) #path of module
    # Create a new document
    doc = Document()

    geometry_options = {"tmargin": "0.75cm", "lmargin": "1cm", "bmargin": "0cm",
                        "includehead": True,
                        "head": "40pt"}
    # Create a new document
    doc = Document(geometry_options = geometry_options)

    first_page = PageStyle("firstpage")

    with first_page.create(Head('L')) as header_left:
        with header_left.create(MiniPage(width=NoEscape(r'0.49\textwidth'),
                                         pos='l')) as logo_wrapper:
            logo_wrapper.append(StandAloneGraphic(image_options="width=3.2cm", filename=logo_image_path))

    with first_page.create(Head('R')) as header_right:
        with header_right.create(MiniPage(width=NoEscape(r'0.49\textwidth'),
                                          pos='r', align='r')) as title_wrapper:
            title_wrapper.append(SmallText(bold('National Marine Dredging Company')))
            title_wrapper.append(LineBreak())
            title_wrapper.append(SmallText(bold(f'Mussafah {16}th')))
            title_wrapper.append(LineBreak())
            title_wrapper.append(SmallText('Phone: +971 2 513 00 00 '))


    doc.preamble.append(NoEscape(r'\usepackage[table]{xcolor}'))
    doc.preamble.append(first_page)

    doc.change_document_style("firstpage")



    section =Section(f'Input')
    doc.append(section)


    additional_info = {
        'Project:': 'Al Hudayriyat Island PDA Enabling Works',
        'Project Number:': 167,
        'Location:': 'Abu Dhabi - Al Hudayriyat Island',
    }

    #Header and Project Table
    table1 = generate_table(cpth.latex_dict)
    project_table = generate_table(additional_info)

    #Add sections
    subsection = Subsection('Project Info')
    doc.append(subsection)
    subsection.append(project_table)
    subsection.append(NoEscape(r'\vspace{1cm}'))
    subsection_2 = Subsection('CPT Information')
    doc.append(subsection_2)
    subsection_2.append(table1)

    #Add basic plots
    with doc.create(Subsection('CPT Plots')):
        with doc.create(Figure(position='h!')) as figure:
            figure.add_image(gpath+cpth.name + '_basicplot.png', width='18.5cm')


    #Second Page
    doc.append(NewPage())
    section2 = Section(f'Output')
    doc.append(section2)


    subsection_output1 = Subsection(f'CPT-{gpath+cpth.name} Summary')
    doc.append(subsection_output1)
    table2 = generate_table(cpts.latex_dict)


    # mw_path = 'D:/04_R&D/cptspy/load/mw.PNG'
    # pga_path = 'D:/04_R&D/cptspy/load/acc.jpg'

    mw_path = os.path.join(path + '\\mw_log.PNG').replace('\\', '/')
    pga_path = os.path.join(path + '\\acc.jpg').replace('\\', '/')



    gwl_path = 'gwl.jpg'
    scf_path = 'shell_logo.jpg'

    table3 = Tabular('lll')
    table3.add_hline()

    table3.add_row([
        # NoEscape(r'\includegraphics[width=0.65cm]{' + mw_path + r'}'),
                    NoEscape(r'\raisebox{-0.15cm}{\includegraphics[width=0.75cm]{' + mw_path + r'}}'),
                    NoEscape(r'\raisebox{0.1cm}{Magnitude}'),
                    NoEscape(r'\raisebox{0.1cm}{'+str(float(m_w))+r'}')])
    table3.add_row([NoEscape(r'\includegraphics[width=0.95cm]{' + pga_path + r'}'),
                    NoEscape(r'\raisebox{0.25cm}{P.G.A}'),
                    NoEscape(r'\raisebox{0.25cm}{'+str(pga)+'g'+r'}')])

    table3.add_row([NoEscape(r'\includegraphics[width=0.95cm]{' + gwl_path + r'}'),
                    NoEscape(r'\raisebox{0.25cm}{G.W.L}'),
                    NoEscape(r'\raisebox{0.25cm}{'+str(GWL)+'m'+r'}')])

    table3.add_row([NoEscape(r'\includegraphics[width=0.65cm]{' + scf_path + r'}'),
                    NoEscape(r'\raisebox{0.25cm}{S.C.F}'),
                    NoEscape(r'\raisebox{0.25cm}{' + str(float(scf)) + r'}')])

    table3.add_hline()

    # Combine the tables side by side with a distance of 1 cm between them

    doc.append(NoEscape(r'\hspace{1cm}'))
    doc.append(table2)
    doc.append(NoEscape(r'\hspace{1cm}'))
    doc.append(table3)

    # Add a figure below the tables
    with doc.create(Subsection('Figures')):
        with doc.create(Figure(position='h!')) as figure:
            figure.add_image(gpath+cpth.name + '.png', width='18.5cm')
            # figure.add

        with doc.create(Figure(position ='h!')) as figure:
            figure.add_image(gpath+'legends.png', width='18.5cm')


    # Generate PDF
    try:
        doc.generate_pdf(gpath+cpth.name, clean_tex = False, clean = True)
    except subprocess.CalledProcessError as e:
       pass

print(my_list)


# os.system(f'{cpth.name}.pdf')