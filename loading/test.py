from pylatex import Document, Section, Subsection, Command, Tabular, Figure
from pylatex.utils import NoEscape
import liquepy as lq
from image import load_cpt_header
from calc.liquefaction import  run_rw1997
from calc.summary import CPTSummary
path = 'C:/Users/dragos/Documents/GitHub/cptspy/calc/CPT_H15c.csv'
cpt = lq.field.load_mpa_cpt_file(path, delimiter=';')
cpth = load_cpt_header(path, delimiter = ';')
rw_1997 = run_rw1997(cpt, pga = 0.122, m_w = 6, gwl = 4)

cpts = CPTSummary(rw_1997)

logo_image_path = 'C:/Users/dragos/Documents/GitHub/cptspy/loading/nmdc.png'
cpt_file_path = 'C:/Users/dragos/Documents/GitHub/cptspy/loading/CPT_H15c.csv.png'


# Create a new document
doc = Document()
doc.append(NoEscape(r'\vspace*{5cm}'))
from pylatex import Document, Section, Subsection, Tabular, Figure
from pylatex.utils import NoEscape
geometry_options = {"tmargin": "1cm", "lmargin": "2cm"}
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
        \small Company Name \\
        \small Address \\
        \small Phone: +1 234 5678 \\
        \small Email: info@example.com
    \end{tabular}
}
\lhead{\includegraphics[width=2cm]{C:/Users/dragos/Documents/GitHub/cptspy/loading/nmdc.png}}
\vspace{2cm}
\vspace{2cm}
'''
doc.preamble.append(NoEscape(header))
doc.append(NoEscape(r'\vspace{3\baselineskip}'))

# doc.append(Command('multirow', '3', '*', r'\vspace{3\baselineskip}'))
# Create a minipage environment for side-by-side tables

section =Section('CPT Summary')
section.before_section ='\n\n\n\n\n\n\n\n\n\n'

doc.append(section)
# Create the first table
# Create the first table
table1 = Tabular('ll')
table1.add_hline()
for k in cpts.__dict__:
    row = [k, cpts.__dict__[k]]
    table1.add_row(row)
table1.add_hline()

# Create the second table
table2 = Tabular('ll')
table2.add_hline()
for k in cpth.__dict__:
    row = [k, cpth.__dict__[k]]
    table2.add_row(row)
table2.add_hline()

#add empty space
doc.append('\n\n\n\n\n')

# Combine the tables side by side with a distance of 2 cm between them
doc.append(NoEscape(r'\hspace{0cm}'))
doc.append(table1)
doc.append(NoEscape(r'\hspace{2cm}'))
doc.append(table2)

# Add a figure below the tables
with doc.create(Section('CPT Figures')):
    with doc.create(Figure(position='h!')) as figure:
        figure.add_image(cpt_file_path, width='15cm')

# Save the generated LaTeX code to a file
doc.generate_tex('trial')

# Generate PDF
doc.generate_pdf('trial.tex', clean_tex=False)
