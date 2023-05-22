from pylatex import Document, Section, Subsection, Command, Tabular, Figure
from pylatex.utils import NoEscape
import liquepy as lq
from loading import load_cpt_header
from calc.liquefaction import run_rw1997
from calc.summary import CPTSummary
import matplotlib.pyplot as plt
from miscellaneous.figures import create_fos_and_index_plot, create_compactibilty_plot
import subprocess

path = 'D:/04_R&D/cptspy/output/CPT_L21d.csv'


paths = ['D:/04_R&D/cptspy/output/CPT_L21d.csv', 'D:/04_R&D/cptspy/output/CPT_K18b.csv', 'D:/04_R&D/cptspy/output/CPT_H15c.csv']
pga = 0.122
m_w = 6
gwl = 1

cpt = lq.field.load_mpa_cpt_file(path, delimiter=';')
rw_1997 = run_rw1997(cpt, pga=0.122, m_w=6, gwl=0)

cpth = load_cpt_header(path)
cpts = CPTSummary(rw_1997)

fig, sps = plt.subplots(nrows=1, ncols=3, figsize=(16, 8))
create_fos_and_index_plot(sps, rw_1997)

fig2, ax = plt.subplots(nrows=1, ncols=1, figsize=(4, 4))
create_compactibilty_plot(ax, rw_1997)
fig2.savefig(cpth.name + '_compactibility.png', bbox_inches='tight')

fig.savefig(cpth.name + '.png', bbox_inches='tight')

# Home
# logo_image_path = 'C:/Users/dragos/Documents/GitHub/cptspy/loading/nmdc.png'
# cpt_file_path = 'C:/Users/dragos/Documents/GitHub/cptspy/loading/CPT_H15c.csv.png'
# Work
logo_image_path = 'D:/04_R&D/cptspy/loading/nmdc.png'
cpt_file_path = 'D:/04_R&D/cptspy/loading/H15c.png'

#
# Create a new document
doc = Document()
doc.append(NoEscape(r'\vspace*{5cm}'))

geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
# Create a new document
doc = Document(geometry_options = geometry_options)

# Add the header with logo and company info
header = r'''
\usepackage{fancyhdr}
\usepackage{graphicx}

\pagestyle{fancy}
\fancyhf{}
\rhead{
    \begin{tabular}{@{}l@{}}
        \small National Marine Dredging Company \\
        \small Mussafah 16th \\
        \small Phone: +971 2 513 00 00  \\
        \small Email: jmn@nmdc.com
    \end{tabular}
}
\lhead{\raisebox{-1cm}{\includegraphics[width=3cm]{D:/04_R&D/cptspy/loading/nmdc.png}}}
\vspace{2cm}
\vspace{2cm}
'''
doc.preamble.append(NoEscape(header))

# Add vertical space after the header
header_space = r'''
\AtBeginDocument{
    \vspace*{3\baselineskip}
}
'''
doc.preamble.append(NoEscape(header_space))

section =Section(f'CPT-{cpth.name}')
doc.append(section)
# Create the first table
# Create the first table
table1 = Tabular('ll')
table1.add_hline()
for k,v in cpts.latex_dict.items():
    row = [k, v]
    table1.add_row(row)
table1.add_hline()

# Create the second tale
table2 = Tabular('ll')
table2.add_hline()
for k,v in cpth.latex_dict.items():
    row = [k, v]
    table2.add_row(row)
table2.add_hline()

mw_path = 'D:/04_R&D/cptspy/loading/mw.PNG'
pga_path = 'D:/04_R&D/cptspy/loading/acc.jpg'
gwl_path = 'D:/04_R&D/cptspy/loading/gwl.jpg'

table3 = Tabular('lll')
table3.add_hline()

table3.add_row([NoEscape(r'\includegraphics[width=0.95cm]{' + mw_path + r'}'),
                NoEscape(r'\raisebox{0cm}{Magnitude}'),
                NoEscape(r'\raisebox{0cm}{'+str(m_w)+r'}')])
table3.add_row([NoEscape(r'\includegraphics[width=0.95cm]{' + pga_path + r'}'),
                NoEscape(r'\raisebox{0.25cm}{PGA}'),
                NoEscape(r'\raisebox{0.25cm}{'+str(pga)+'g'+r'}')])

table3.add_row([NoEscape(r'\includegraphics[width=0.95cm]{' + gwl_path + r'}'),
                NoEscape(r'\raisebox{0.25cm}{GWL}'),
                NoEscape(r'\raisebox{0.25cm}{'+str(gwl)+'m'+r'}')])
table3.add_hline()


#add empty space
doc.append('\n\n\n\n\n')

# Combine the tables side by side with a distance of 2 cm between them
doc.append(NoEscape(r'\hspace{0cm}'))
doc.append(table2)
doc.append(NoEscape(r'\hspace{1cm}'))
doc.append(table1)
doc.append(NoEscape(r'\hspace{1cm}'))
doc.append(table3)
# Add a figure below the tables
with doc.create(Section('Output Figures')):
    with doc.create(Figure(position='h!')) as figure:
        figure.add_image(cpth.name + '.png', width='18.5cm')

# Save the generated LaTeX code to a file
# doc.generate_tex('trial')

# Generate PDF
try:
    doc.generate_pdf(cpth.name, clean_tex = True, clean = True)
except subprocess.CalledProcessError as e:
   pass