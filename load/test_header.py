import matplotlib.pyplot as plt
import subprocess
import os
from pylatex import Document, Section, Subsection, Command,\
    Tabular, Figure, NewPage, Head, MiniPage, StandAloneGraphic,\
    LargeText, PageStyle, LineBreak, Tabu, MediumText, SmallText
from pylatex.utils import NoEscape, bold




paths = ['D:/04_R&D/cptspy/output/CPT_L21d.csv']

# paths =['D:/04_R&D/cptspy/output/CPT_I18C.csv',
#         'D:/04_R&D/cptspy/output/CPT_J16c.csv',
#         'D:/04_R&D/cptspy/output/CPT_J17b.csv']



logo_image_path = '/load/nmdc.png'
cpt_file_path = '/load/H15c.png'

path = os.path.dirname(__file__) #path of module
print('Original Path is: ', path)
# Create a new document
doc = Document()
# doc.append(NoEscape(r'\vspace*{2.5cm}'))


geometry_options = {"tmargin": "1cm", "lmargin": "1cm", "bmargin" : "0cm",
                    "includehead" : True,
                    "head": "30pt"}
# Create a new document
doc = Document(geometry_options = geometry_options)

first_page = PageStyle("firstpage")

with first_page.create(Head('L')) as header_left:
    with header_left.create(MiniPage(width = NoEscape(r'0.3\textwidth'),
                                     pos = 'c'))  as logo_wrapper:

        logo_wrapper.append(StandAloneGraphic(image_options= "width=2cm", filename=logo_image_path))

with first_page.create(Head('R')) as header_right:
    with header_right.create(MiniPage(width = NoEscape(r'0.67\textwidth'),
                                     pos = 'c', align = 'r'))  as title_wrapper:
        title_wrapper.append(LargeText(bold('National Marine Dredging Company')))
        title_wrapper.append(LineBreak())
        title_wrapper.append(MediumText(bold(f'Mussafah {16}th')))
        title_wrapper.append(LineBreak())
        title_wrapper.append(SmallText('Phone: +971 2 513 00 00 '))

doc.preamble.append(first_page)

# doc.change_document_style("firstpage")
# doc.add_color(name="lightgray", model="gray", description="0.80")

# doc.append(NewPage())

section =Section(f'CPT-{123}')
doc.append(section)
doc.append(NewPage())
doc.append(section)
try:
    doc.generate_pdf('head', clean_tex=True, clean=True)
except subprocess.CalledProcessError as e:
    pass

path =os.path.dirname(__file__)
print(path)
os.system('head.pdf')
