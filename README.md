
# CPTsPy
A large scale geotechnical analyses library for fast processing of cone penetration tests.

# Mind Map
![0](https://github.com/ambrosiasteraceae/cptspy/assets/66112305/c5333c58-d868-4cdf-9925-c7482f5fd03f)


# Overview of Works

 The mindmap represents the complete overview of works to be carried out for the project / library. 
•	It starts by defining multiple functions that first convert the raw input, often coming in .xlsx files, into a standardized format, solving the problem of dealing with multiple file formats
•	Multiple contractors have specific reporting systems, therefore, unfortunately, for each contractor, a convertor function has to be specifically written.
•	Algorithm cycles through each converter and tries to recognize the existing file format and then apply the conversion   - if the file is different to the expected existing format then the conversion will fail and another converter is        attempted
-	if successful, then the converter function name that was successful is returned
-	if unsuccessful, then 'NONE' is returned


## **What is CPT?**

![978-3-319-73568-9_3_Part_Fig1-67_HTML](https://github.com/ambrosiasteraceae/cptspy/assets/66112305/c45a0cb0-6445-4f43-8e7c-c2b433cfe0bc)

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

# Report

Report was made with Pylatex library and the reporting function is called on all cpt / liquepy objects that were successfully converted and calculated. A typical report looks like the following:
The first page, tells us information about the meta data it contains, followed by the basic plots of any cone penetration tests stored in the main data (cone resistance, friction sleeve, pore water pressure, etc).
Second page consists of multiple plots that tell us the safety factor against liquefaction (the probability of the soil to behave as a fluid during earthquake), the soil types as a continuous function across the CPT length and the compactibility chart (how dense or loose the soil is, and how fit for compaction the soil is). All plotting functions were generated with the matplotlib function

  ## Basic Plot
![1L-178_basicplot](https://github.com/ambrosiasteraceae/cptspy/assets/66112305/d5763edc-4b1a-40fc-810c-523bdf13c42f)

  ## Analysis Plot 
![1L-178](https://github.com/ambrosiasteraceae/cptspy/assets/66112305/8e76f884-dc31-43f7-9da7-4b0cbfe9092b)

  ## Compactibility Plot
![1L-178_compactibility](https://github.com/ambrosiasteraceae/cptspy/assets/66112305/205d4596-3def-48e4-ae13-ffcb6b50a8d1)

# Graphical User Interface

-	Main Window Tab - We load or we create a new project. The moment we create a new project, separate folders are created and a custom class for file path manipulations takes care of all moving and deleting files from the project source location
-	Project Settings – Information related to the project specifications and geotechnical settings saved in a .json file for all properties and shows it in a PyQtTree Widget.
-	Convert Tab – Prompts the user to select a folder or single files containing raw .xlsx files waiting to be converted to the standardized format(.csv). If the converting algorithm fails, files are moved to a specific folder where either a new convert algorithm must be written or data must be manually altered. 
-	Load Tab – Loads all .csv files into memory for computation
-	Overview Tab – PyQtTable Views, it is useful for seeing what are we loading, containing either the metadata or the results if the files have been computed.
-	Analysis Tab – Where the calculations are run and where reports can be generated.
-	Plotting Module

![7b](https://github.com/ambrosiasteraceae/cptspy/assets/66112305/dce868e7-9e48-464f-9513-d867aa276b53)
![6a](https://github.com/ambrosiasteraceae/cptspy/assets/66112305/acf7dc22-f3ab-4b89-b4bf-5638d1becdb2)
![5a](https://github.com/ambrosiasteraceae/cptspy/assets/66112305/7f0611c0-ee77-42e0-8d79-f5dfa2e35678)
![4c](https://github.com/ambrosiasteraceae/cptspy/assets/66112305/3550a55e-4f02-4f44-98e9-f88990f24a87)
![3](https://github.com/ambrosiasteraceae/cptspy/assets/66112305/bec1588c-571f-48bf-bc83-557f0d973674)
![2](https://github.com/ambrosiasteraceae/cptspy/assets/66112305/64481dc1-9cea-4fb0-b325-b0f0dce040a0)

# Plotting Module

Plotting Tab – A module for interactive manipulation of cpt files. It is still a work in progress, with many features missing, but so far, it allows for mapping plotting cpt as points, ability to select and view the information stored, to view passing tests or failed through two color gradients. A red & blue indicating, pass or fail (based on certain limiting criteria), and a normalized color map from green to red, showing how close or how much the tests have exceeded certain limits.

For any compaction works, the land reclamation area is divided into grids (aka grid compaction control areas) typically being 25x25m / 35x35m in size. CPT points are scattered across the land reclamation area, and are placed inside the grid compaction zones. For fast processing and retrieval I used the rtree module for indexing spatial information. Ability to select multiple grids, and plot a statistical plot of all tests contained in the selected grids is an implemented feature.


![G4](https://github.com/ambrosiasteraceae/cptspy/assets/66112305/a3a9ea26-aa85-4c8d-aa7d-0c21388f6e1d)
![G3](https://github.com/ambrosiasteraceae/cptspy/assets/66112305/9bd6057c-8e15-416d-9933-f666930482b1)
![G2](https://github.com/ambrosiasteraceae/cptspy/assets/66112305/98675d5c-5ac2-46c2-bcd8-8838d7052b7c)

# Future Works

Due to extensive development efforts over a short period, several features remain to be implemented in the library. These include significant enhancements to the GUI, integration with Google Maps, adding useful features to the plotting module so we can highlight areas of interest.
But more importantly. given the current framework, incorporating machine learning techniques is a natural, logical and potentially powerful next step. I have identified some potential applications of machine learning in this context:
- [ ] 1.	Data Classification and Labeling: automatically classify and label the CPT data based on various parameters such as soil type, soil density, soil strength properties and liquefaction potential. This can automate the data processing pipeline and reduce the manual effort required for categorizing the data.
- [ ] 2.	Optimization: Machine learning optimization algorithms can be used for the placement of CPT points for optimal coverage, the design of compaction grids for maximum efficiency. If implemented, we could leverage these optimization algorithms reducing the number of tests, thus reducing cost and the project construction/delivery time.
- [ ] 3.	Pattern Recognition: can identify patterns and correlations in the CPT data that may not be apparent through traditional analysis methods. We could perhaps gain a deeper understanding of soil behaviour and the accuracy of  the geotechnical assessment
- [ ] 4.	Interpolation and Prediction: ML algorithms can be trained to interpolate between the CPT points to predict soil properties at unmeasured depths. Techniques such as regression, Gaussian processes, or neural networks can learn the relationship between depth and soil properties from the available data and generate predictions for other areas. 
- [ ] 5.	Data Fusion and Integration: CPT data with other sources of information, such as geological surveys, geophysical measurements, in-situ boreholes or historical data from similar projects providing a better understanding of the subsurface conditions.


