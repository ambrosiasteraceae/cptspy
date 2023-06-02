#
# - GEnerate table first Parallelization: You have a loop where you perform
# operations on each CSV file independently. If the computations for different CSV files are not interdependent,
# you could use parallelization to speed things up. Python's multiprocessing module could be used to run computations
# for different CSV files simultaneously. However, be careful as the maximum speedup will be limited by the number of
# cores in your CPU, and adding parallelism can make the code more complex.
#
# Use of a Profiler: Use a profiler to find
# out where your program spends most of its time. Python's built-in cProfile module can help with this. Once you know
# where the bottlenecks are, you can focus on optimizing those parts of the code.
#
# Optimize File I/O: You might want
# to look into more efficient ways to store and read your data. Depending on the nature of your data and how it's
# being used, different file formats might be more appropriate. For example, if your data is purely numerical,
# binary file formats like HDF5 could offer faster I/O speeds. If you are reading CSV files multiple times,
# consider reading them once, processing, and storing the results for further use.
#
# Reduce the frequency of file operations: Each plot is being saved to a file individually, which might be
# time-consuming. If possible, consider gathering all plots and then saving them at once.
# Efficient Libraries:
# Consider using more efficient libraries for specific tasks. For example, Numba or Cython could speed up numerical
# computations, while Dask could be used for efficient parallel computations on larger-than-memory data. For the

# LaTeX document generation part, if it's taking significant time and you're generating similar documents in a loop,
# you might want to consider creating a template and filling it with the required data. This might be faster than
# creating each document from scratch. Remember, optimization should be a thoughtful process and can often lead to
# more complex and harder-to-maintain code. Always make sure to profile your code to identify bottlenecks and make
# sure that the parts you're optimizing are really the ones taking up most of the exec


#TEMPLATE IDEAS
from jinja2 import Template IDEAS
template = Template(r"""
\section{Input}
\subsection{Project Info}
{{ project_info_table }}
\subsection{CPT Header Information}
{{ header_info_table }}
\subsection{Basic Plots}
\includegraphics[width=18.5cm]{{ basic_plot_path }}
""")

for path in paths:
    # ... (perform the calculations and plot generation)

    # Generate tables as strings
    project_info_table_str = generate_table(project_info).dumps()
    header_info_table_str = generate_table(cpt_header_info).dumps()

    # Render the template with the generated data
    rendered = template.render(
        project_info_table=project_info_table_str,
        header_info_table=header_info_table_str,
        basic_plot_path=cpth.name + '_basicplot.png',
    )

    # Write the rendered template to a file
    with open(cpth.name + '.tex', 'w') as f:
        f.write(rendered)


#II
figs = []
for cpt in cpts:
    fig, sps = plt.subplots()
    create_basic_plot(sps, path)
    figs.append((fig, name))
    print(.....)

    for fig, name in figs:
        fig.savefig(cpt.name + '.png')
    plt.close('')


#Paralleziation III

from multiprocessing import Pool
def process_file(path):
    # ... all the processing for a single file
if __name__ == "__main__":
    pool = Pool()
    paths = ['D:/04_R&D/cptspy/output/CPT_L21d.csv']  # the list of all CSV files
    pool.map(process_file, paths)

#IV

#look to create a template file and fill afterwards?