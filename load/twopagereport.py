import subprocess
import os

from pylatex import *
from pylatex.utils import NoEscape, bold
from load.loading import load_cpt_header, load_mpa_cpt_file
from calc.liquefaction import run_rw1997
from calc.summary import CPTSummary
from miscellaneous.figures import *

#@TODO load_mpa_cpt_file (return both CPT and Header Classes)
#@TODO Add just plots, no need to save images
#@todo Add water table symbol to graph

# paths = ['D:/04_R&D/cptspy/output/CPT_H16d.csv']

# gpath = 'D:/04_R&D/cptspy/load/pdfs/'
# if not os.path.exists(gpath):
#     os.makedirs(gpath)
# gpath = ''

def generate_table(_dict):
    table = Tabular('ll')
    table.add_hline()
    for i, (k, v) in enumerate(_dict.items()):
        if i % 2 == 0:

            table.append(NoEscape(r'\rowcolor{gray!25}'))
        table.add_row([k, v])
    table.add_hline()
    return table


def generate_doc(path_choice, projreq , ffp):
#for path in paths:
    #get path
    #glob.glob(self.main.ffp.converted, '*.csv')
    import glob

    #path = np.random.choice(paths) #Get a random file from the folder

    pga = projreq['pga']
    m_w = projreq['m_w']
    GWL = projreq['gwl']
    scf = projreq['scf']

    cpt_name = os.path.basename(path_choice).split('.')[0]
    proj_name = projreq['proj_name']
    proj_num = projreq['proj_num']
    proj_loc = projreq['proj_loc']

    cpt = load_mpa_cpt_file(path_choice, scf=scf)
    gwl = cpt.elevation[0] - GWL

    rw_1997 = run_rw1997(cpt, pga=pga, m_w=m_w, gwl=gwl)
    cpth = load_cpt_header(path_choice)
    cpts = CPTSummary(rw_1997)

    saved_path = os.path.join(ffp.reports,cpth.name)
    print('Saved path is ', saved_path)

    fig, sps = plt.subplots(nrows=1, ncols=3, figsize=(16, 10))
    create_fos_and_index_plot(sps, rw_1997)
    fig.savefig(saved_path + '.png', bbox_inches='tight')

    fig2, ax = plt.subplots(nrows=1, ncols=1, figsize=(4, 4))
    create_compactibilty_plot(ax, rw_1997)
    fig2.savefig(saved_path + '_compactibility.png', bbox_inches='tight')

    fig3, axs = plt.subplots(1, 4, figsize=(16, 12), sharey=True)
    create_cpt_plots(axs, cpt)
    fig3.savefig(saved_path+ '_basicplot.png')

    fig4, axes = plt.subplots(1, 3, figsize=(16, 4))
    create_massarasch_and_legend_plot(axes, rw_1997)
    fig4.savefig(saved_path+'legends.png',bbox_inches='tight')

    #logo_image_path = 'nmdc.jpg'

    path = os.path.dirname(__file__) #path of module
    print('*'*50)
    print(path)
    print(path_choice)
    print('*'*50)

    logo_image_path = os.path.join(path + '\\nmdc.jpg').replace('\\', '/')

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
        'Project:': proj_name,
        'Project Number:': proj_num,
        'Location:': proj_loc,
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
            figure.add_image(saved_path + '_basicplot.png', width='18.5cm')


    #Second Page
    doc.append(NewPage())
    section2 = Section(f'Output')
    doc.append(section2)


    subsection_output1 = Subsection(f'CPT-{cpt_name} Summary')
    doc.append(subsection_output1)
    table2 = generate_table(cpts.latex_dict)


    # mw_path = 'D:/04_R&D/cptspy/load/mw.PNG'
    # pga_path = 'D:/04_R&D/cptspy/load/acc.jpg'

    mw_path = os.path.join(path + '\\mw_log.PNG').replace('\\', '/')
    pga_path = os.path.join(path + '\\acc.jpg').replace('\\', '/')

    gwl_path = os.path.join(path + '\\gwl.jpg').replace('\\', '/')
    scf_path = os.path.join(path + '\\shell_logo.jpg').replace('\\', '/')

    #gwl_path = 'gwl.jpg'
    #scf_path = 'shell_logo.jpg'

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
            figure.add_image(saved_path + '.png', width='18.5cm')

        with doc.create(Figure(position ='h!')) as figure:
            figure.add_image(saved_path+'legends.png', width='18.5cm')

    return doc

def create_pdf_from_doc(doc, path):

    # Generate PDF
    try:
        doc.generate_pdf(path, clean_tex = True, clean = True)
    except subprocess.CalledProcessError as e:
       pass




# os.system(f'{cpth.name}.pdf')