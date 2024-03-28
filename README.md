
# CPTsPy
![0](https://github.com/ambrosiasteraceae/cptspy/assets/66112305/c5333c58-d868-4cdf-9925-c7482f5fd03f)


## Overview of Works

 The mindmap represents the complete overview of works to be carried out for the project / library. 
•	It starts by defining multiple functions that first convert the raw input, often coming in .xlsx files, into a standardized format, solving the problem of dealing with multiple file formats
•	Multiple contractors have specific reporting systems, therefore, unfortunately, for each contractor, a convertor function has to be specifically written.
•	Algorithm cycles through each converter and tries to recognize the existing file format and then apply the conversion   - if the file is different to the expected existing format then the conversion will fail and another converter is        attempted
-	if successful, then the converter function name that was successful is returned
-	if unsuccessful, then 'NONE' is returned


##**What is CPT?**


A cone penetration test (CPT) is a method used in geotechnical engineering to assess the properties of soil. A cone is pushed against the soil and equipped with sensors that measure two resistances at small increments in depth (0.01m, 0.002m):
•	Tip/Cone resistance:  
•	Sleeve friction: The friction developed along the rod’s shaft as the cone is being pushed onto the ground
By analyzing the measurements we can gain valuable insights into various soil properties, including:
•	Soil type: Sand, clay, silt, etc.
•	Soil density: Loose, dense, or very dense.
•	Soil Strength and stiffness: 
The data obtained from a CPT is crucial for various applications in civil engineering, such as:
•	Designing safe and stable foundations for buildings and structures.
•	Evaluating the stability of slopes and embankments.
•	Assessing the risk of liquefaction (soil losing its strength and behaving like a liquid during an earthquake). 
•	Planning for underground construction projects.
•	Land Reclamation projects criteria

Current engineering practices manipulate the raw CPT data using Excel. For construction projects where the number of CPTs are above 1000 tests it becomes a burden specifically since VBA macros can only process 200 tests at a time, a process taking 30 minutes to compute.
In the case of cptspy I benchmarked against 10_000 tests, taking less than 3 minutes of computation time with room for optimization.
The library as a whole aims to automate the whole process and contain all the information stored in the main data for geotechnical analyses, while making use of the metadata to map the location & information of each CPT. This interaction is happening all throughout a graphical user interface written in PyQt.



•	When successful, the test is converted into a .csv file for later manipulation. We ensure this way, that the file will always be computable
•	A function then is called upon the .csvfile and converts it to a cpt object.
•	The cpt object is being fed as argument for all functions that perform calculations and geotechnical processing, easing the number of parameters being passed.
•	All plotting functions work with cpt objects.
•	Geotechnical Analyses output the results into a liquepy object
•	For later retrieval after performing calculations, each liquepy object is saved as numpy compressed format. The project spans multiple months with multiple uploading of files, therefore, we ensure a reliable way of loading the processed results so that we do not compute them repeatedly.
•	The project management and control together with the visualization module 

## Report
Report was made with Pylatex library and the reporting function is called on all cpt / liquepy objects that were successfully converted and calculated. A typical report looks like the following:
The first page, tells us information about the meta data it contains, followed by the basic plots of any cone penetration tests stored in the main data (cone resistance, friction sleeve, pore water pressure, etc).
Second page consists of multiple plots that tell us the safety factor against liquefaction (the probability of the soil to behave as a fluid during earthquake), the soil types as a continuous function across the CPT length and the compactibility chart (how dense or loose the soil is, and how fit for compaction the soil is). All plotting functions were generated with the matplotlib function

## Graphical User Interface

a)	Main Window Tab - We load or we create a new project. The moment we create a new project, separate folders are created and a custom class for file path manipulations takes care of all moving and deleting files from the project source location
b)	Project Settings – Information related to the project specifications and geotechnical settings saved in a .json file for all properties and shows it in a PyQtTree Widget.
c)	Convert Tab – Prompts the user to select a folder or single files containing raw .xlsx files waiting to be converted to the standardized format(.csv). If the converting algorithm fails, files are moved to a specific folder where either a new convert algorithm must be written or data must be manually altered. 
d)	Load Tab – Loads all .csv files into memory for computation
e)	Overview Tab – PyQtTable Views, it is useful for seeing what are we loading, containing either the metadata or the results if the files have been computed.
f)	Analysis Tab – Where the calculations are run and where reports can be generated.
g)	Plotting Module

## Plotting Module

Plotting Tab – A module for interactive manipulation of cpt files. It is still a work in progress, with many features missing, but so far, it allows for mapping plotting cpt as points, ability to select and view the information stored, to view passing tests or failed through two color gradients. A red & blue indicating, pass or fail (based on certain limiting criteria), and a normalized color map from green to red, showing how close or how much the tests have exceeded certain limits.

For any compaction works, the land reclamation area is divided into grids (aka grid compaction control areas) typically being 25x25m / 35x35m in size. CPT points are scattered across the land reclamation area, and are placed inside the grid compaction zones. For fast processing and retrieval I used the rtree module for indexing spatial information. Ability to select multiple grids, and plot a statistical plot of all tests contained in the selected grids is an implemented feature.

## Future Works
Due to extensive development efforts over a short period, several features remain to be implemented in the library. These include significant enhancements to the GUI, integration with Google Maps, adding useful features to the plotting module so we can highlight areas of interest.
But more importantly. given the current framework, incorporating machine learning techniques is a natural, logical and potentially powerful next step. I have identified some potential applications of machine learning in this context:
1.	Data Classification and Labeling: automatically classify and label the CPT data based on various parameters such as soil type, soil density, soil strength properties and liquefaction potential. This can automate the data processing pipeline and reduce the manual effort required for categorizing the data.
2.	Optimization: Machine learning optimization algorithms can be used for the placement of CPT points for optimal coverage, the design of compaction grids for maximum efficiency. If implemented, we could leverage these optimization algorithms reducing the number of tests, thus reducing cost and the project construction/delivery time.
3.	Pattern Recognition: can identify patterns and correlations in the CPT data that may not be apparent through traditional analysis methods. We could perhaps gain a deeper understanding of soil behaviour and the accuracy of  the geotechnical assessment
4.	Interpolation and Prediction: ML algorithms can be trained to interpolate between the CPT points to predict soil properties at unmeasured depths. Techniques such as regression, Gaussian processes, or neural networks can learn the relationship between depth and soil properties from the available data and generate predictions for other areas. 
5.	Data Fusion and Integration: CPT data with other sources of information, such as geological surveys, geophysical measurements, in-situ boreholes or historical data from similar projects providing a better understanding of the subsurface conditions.


