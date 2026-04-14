Biome-BGC-UI

User Interface of Biome-BGC Forest Growth Model (v. ZALF). This software provides visual tools for preparing the model, model execution, and model calibration.


**User Guide for Biome-BGC (version ZALF) Model User Interface 1.0**


**Part-One: Input Files**

**Part-Two: Model Execution and Output**

**1	Biome-BGC (version ZALF) Model Execution**

**1.1	Overview**

The module serves several purposes; first, module executes the Biome-BGC (version ZALF) model when the necessary model input files are ready. Second, new set of input files can be created modifying old input files. Third, using this module it is possible to compare the changes in different version of the input files. And finally, the model outputs using several version of input files can be compared graphically. The description of each functions are presented in the subsequent section.

<img width="940" height="485" alt="image" src="https://github.com/user-attachments/assets/c21b2420-fb50-4c96-a566-f5b8f2c15cb4" />
Figure 1.1: Main Window of Model Execution Module

Figure 1.1 displays the main window of the module; major segments of the window is highlighted using coloured boxes. The first segments contains one action button for loading the initial file of the base version while the second segment of the window controls the versioning options and action buttons for navigating through different versions. The third segment displays the list of input files in the current (input file) version, and contains action buttons for modifying input files, loading and creating new version of input files, and selecting simulation program. The fourth segment contains a tab-controlled view for presenting available options and functionalities which the fifth segment contains the action buttons for saving newly created input files, executing the simulation program, and closing the module. 

**1.2	The Base Version and Versioning Options**

The first version of input files loaded is considered as the base version and as the name reflects, all new versions created will receive the values in the base version as default values. The base version can be opened/loaded by pressing the action button in the first highlighted section of the main window (see Figure 1.1).

When the base version is loaded, the version number of the base version will be set 0 by default. However, the beginning version number can be controlled from the ‘version settings’ window that will appear if the ‘Settings’ action button (in the second highlighted section of the main window as shown in Figure 1.1) is clicked. Figure 1.2 shows the version setting window.

<img width="517" height="250" alt="image" src="https://github.com/user-attachments/assets/fb093925-5cb7-49cd-813f-f58ce6d7d63a" />

Figure 1.2: Version Settings Window

As shown in the figure, ‘start from zero’ is the default selected choice. If base version has a different version number (i.e., other than 0), ‘continue previous versioning’ option has to be selected. While the (second) option button is selected, the disabled check boxes will be enable. Two possible options are: choosing the version number from the name of the base initialization file or continue from a specific number. In case of finding version number from the initialization file, the system will consider the last two digit of filename (before extension) as the base or beginning version number. However, if version number cannot be retrieved from the filename, zero (0) will be considered as the beginning version number.

In case of continuing from a specific version number, please note that only numbers from 1 and 99 can be assigned. This restriction was imposed because while naming any input file, only two digits/characters are (usually) used for versioning purpose.

New filenames for new input file version can be generated either by adding the version number at the end of the base filename, or by replacing the last two digits of the base filename. File naming option is controlled by the option radio button in the ‘File Versioning Option’ section. At the bottom of the window, an example of the new filename for the initialization file is shown.

Every time a new version is created, the new version will receive a version number of latest version number incremented by one. That’s why version setting options are available until a new version is created or loaded into the system.

**1.3	Input Parameter-Files of Selected Version**

The parameter files of the selected version is displayed in third section of the main window of the model execution module (see Figure 1.1). In the table (view), all files linked to a (input file) version will be displayed. Theoretically, if any file listed in the table does not exist or the format of corresponding file is not consistent, the module cannot load the version. However, this notion is only partially realized in the current version of the user interface. That is, if the gis, veg, soil profile or the soil horizon file is missing, the system cannot load the version; otherwise, the version will be loaded in the system. For detailed description of each type of parameter file, please see the Biome-BGC (version ZALF) documentation.  

**1.4	Add/Create a New Version**

A new set (version) of the model input files can be added by pressing the ‘Load Version’ action button (in the third zone of the main window, see Figure 1.1). If the base version is already loaded, the newly added input file set will be treated as a new version. However, if there is no base version, the loaded version of input files will be treated as the base version.

A new version can be created pressing the ‘New Version’, only if the base version is loaded. In this case, a new copy of the base version will be created and considered as the new version (of input files). That is, all the (parameter/option) values in the base version will be used as the default values (for all parameters and/or options) in the new version. 

Please also be noted that when a new version (of input files) is created, the new version is created and saved in the (primary) memory at the run-time. Thus, any alteration will only be reflected at the run-time. In order to realize the changes, the newly created versions must be saved. However, once the version is saved, the parameter values cannot be modified in this module. If you want to modify a saved version, you must create a new version; the fact indeed reflects the idea of the necessity of creating multiple (model) input file versions. Of course, any saved parameter file can be modified using concerned module described in Part 1.

**1.5	Browse Through/Observe File Parameters**

Users can browse through the file parameter (and/or options) by selecting the type of parameter file from the drop-down list in the combo-box in ‘Vew Parameter’ tab of the tab-view (fourth highlighted area of the main window shown in Figure 1.1). As a default setting, parameters from all versions will be displayed in the ‘view’. However, if the ‘Show All Version’ option is checked off, only parameters of the ‘selected version’ will be displayed. Figure 1.3 displays the parameter (or option values) in initialization files in three different versions. In parameter-view of initialization file, output variable list will not be shown.

<img width="940" height="618" alt="image" src="https://github.com/user-attachments/assets/6704d4a3-b7b7-4456-af5e-0523d7717277" />

Figure 1.3: Parameter-View of Initialization Files in three file-versions

In Figure 1.3, “Initial Parameter” was chosen for displaying the parameter values. Although the active version, in this case, is 12 as shown in the figure, properties of all three versions are shown because the ‘Show All Versions’ option is checked on. In Figure 1.4 and Figure 1.5, parameter-view of the GIS File and Vegetation File are shown respectively.

<img width="940" height="539" alt="image" src="https://github.com/user-attachments/assets/ae7e79e8-5b01-4842-aa53-e846c0b7d094" />

Figure 1.4: Parameter-View of GIS Files in two versions

<img width="940" height="539" alt="image" src="https://github.com/user-attachments/assets/9b4a71f8-ce8b-48b1-9a14-1e75c93199d4" />

Figure 1.5: Parameter-View of Vegetation Files in two versions

Please note that a GIS File may contain description of several sites. Thus, in the GIS parameter-view, the Site-ID has been shown in the column name inside parentheses along with the Version-ID. On the other hand, inside a Vegetation-File, there may contain description of more than one vegetation layers. While showing the parameter values in Figure 1.5, thus, Vegetation Number is also displayed in the column names in addition to version-id, site-id. Vegetation number is shown in the parentheses after the site id separated by a colon (‘:’).

Figure 1.6 shows the parameter-view of epc-files in two versions of Biome-BGC input files. In the first version, there is only one EPC-file; however, the second version has two EPC-files. Thus the EPC-value column names include the site-ids and EPC-File-ID, generated automatically by the system, along with the version-id. 

Please also note that the ‘Show Reference Value’ option is only available for EPC parameter-view. When the option is checked on, all (reference) values in reference epc-files located in ‘/refvalue/epcfile/’ directory will be displayed for the shake of quick comparison.

<img width="940" height="546" alt="image" src="https://github.com/user-attachments/assets/0b047998-34e1-4ad2-bc7f-b8a077674505" />

Figure 1.6: Parameter-View of EPC-files in different versions

In case of soil parameter-view, the parameter values for each version are displayed horizontally as shown in Figure 1.7. 

<img width="940" height="546" alt="image" src="https://github.com/user-attachments/assets/28210b8d-946f-451d-b5f7-8eb994de7317" />

Figure 1.7: Parameter-View of Soil-files in different versions

**1.6	Modification of Parameter File**

Parameter files can be modified in one of the following two ways: first, pressing the ‘Modify File’ action button, only when the button is active, after the parameter file being selected in the list of parameter files; second, editing values inside the parameter-view table. In the first approach, a new window will appear and modifications can be done inside the fields of the concerning window. The modification will be realized after clicking of the ‘Update’ action button of the appeared window. However, if update action button is missing (for instance, in EPC window and Soil Window), any modification is realized immediately.

In the second approach i.e. modifying files in parameter view, modifications are realized instantly. Please be noted that in this approach the modification opportunities are limited to only displayed parameters. For instance, in case of initialization file, the output variable list cannot be altered.

However, as mentioned earlier, modification of a file is only possible until a new version is saved when a new version is being created using the base version. That is, when a version files are saved in the disk, parameter values in the version can no longer be altered. Nevertheless, when a version is loaded for the first time, the files of the version can be modified if it is the latest loaded version.

Please note that all modifications are temporarily realized in (primary) memory and thus for permanent realization (and later use) the version must be saved. During saving the files, the filenames will be decided automatically by the pre-set rules for file naming. The input files are inter-referenced using relative file paths, when they are saved in the disk, and every time a new version is created, the old parameter file is not replaced rather a new file is created with a new filename. Thus, modification of a single file may result chain modification in files and during the modification the file references are updated automatically along with assigning new names for modified files.

When an attempt is made to save the newly created (input file) version, only modified files are created with new names rather than creating copies of each file. 

**1.7	Comparison among (Input File) Versions**

Using this module, input file versions can be compared. Version comparison option is available inside ‘Compare Versions’ tab. In order to compare the versions, please enter the version numbers to be compared in the text box in the tab page. The version numbers must be separated by commas (,). After inserting the version numbers, if the ‘Compare’ action button is pressed, parameter values that are different in different versions will be displayed in a result table. Any number of versions can be compared. Figure 1.8 shows the result of the comparison between two file versions (i.e. 0th version and 1st version) of input files.

<img width="940" height="575" alt="image" src="https://github.com/user-attachments/assets/966006d6-ad3d-418e-a9f8-6a944da84547" />

Figure 1.8: Results of (File) Version Comparison

In the result table, the deviated parameter values in different versions are shown under the concerning files or objects. The object or files are highlighted in the result. Please note that the id number (of belonging object) is used when necessary for distinguishing object properties. For instance, in the above example comparison shown in Figure 1.8, the ‘Ground water depth’ parameter of site-301 differs in GIS files in two version. At the same time, the pH value of horizon-Cv2 in profile-301 of site-301 differs in soil files between these versions. Also, ‘Starting Tree Age’ parameter of the 1st vegetation layer (or type) in site-301 differs in VEG file versions.

**1.8	Saving the Modified (input file) Version**

A modified version or newly created version can be saved pressing the action button ‘Save New Version’ in the 5th highlighted area of the main window of this module (see Figure 1.1). As mentioned earlier in section 1.6, filenames are generated automatically and thus no filename is asked from the user.


**1.9	Biome-BGC Model Execution**

The Biome-BGC model program is a distinct program at its own and thus the program cannot be controlled directly from the user-interface or any error in the model program cannot be handled by the user-interface. However, the program is executed by the user-interface with a system call. During the system call, the model program is provided the necessary arguments especially the relative address (from the program home directory) of the initialization file. Because the input files cannot be passed directly from the user interface, it is mandatory to save any (modified) version before executing the model program with a target version of input parameter files. If the version is not save, while executing the model, the user interface will ask the user if he/she agrees to save the (modified or newly created) input files.

The model can be executed by pressing the ‘Run Model’ action button. However, the model program must be selected prior to execution; there is no default model program to be run. The model program can be selected using the action button next to model program name textbox under the parameter filename table in the 3rd highlighted area on the main window (see Figure 1.1). During model execution a batch file will be created, which can be used later on for manually executing the model program. Users can choose the batch filename by entering the batch filename prefix in the textbox below the chosen model program textbox. If the batch file prefix is not provided, the user-interface program will create a temporary batch file for executing the model program. Please also note that, the model program can only be executed from the user-interface by executing the batch file. Inside the batch file the working directory must be pushed to the home directory of the model program.

When the model program finishes, the on-screen output of the model program will be saved in a temporary log file and users can view examine the log file. Figure 1.9 displays the log viewer.

<img width="940" height="646" alt="image" src="https://github.com/user-attachments/assets/72b026e7-88de-415b-b9ac-7c4e77649e74" />

Figure 1.9: Log-viewer in Biome-BGC Model Execution Module

**1.10	  Visual Comparison of Biome-BGC output using Different Input File Versions**

Using this module it is possible to visualize the model predictions with certain input version and compare predictions among different versions of input parameter files. The visualization options can be found in the ‘Graph’ tab. Figure 1.10 displays the options for visualization of model predictions and comparison of model predictions using different version of input parameter files. 

<img width="940" height="559" alt="image" src="https://github.com/user-attachments/assets/a056f54b-a4e8-4e8b-bca1-6e649e773bc8" />

Figure 1.10: Visualization of Biome-BGC Model Predictions

However, visualization is only possible when the graph templates are readily available in ‘/graphs/’ directory inside the (user-interface program) home directory. Details discussion about designing and creating graph templates are discussed in chapter 2.

The saved templates are loaded when the module is open and shown the in the drop-down list. When a graph template from the drop-down list is selected, the components of the graphs (i.e., plots and data-series) will be listed in the table below the drop-down list. From the list of graph components, the users can switch from model predictions using one version to the model predictions using another version.  

The table of graph components contains three columns: Graph Object, Version, and Change (see Figure 1.10). Initially in the version column, current or active version is selected by default for all data-series; meaning that, the data for according data-series would come from the Biome-BGC model output files using selected version of input parameter files. All loaded version numbers are included into the drop-down list for every data-series and use can select any loaded version. However, graphs can only be produced if the model has already been executed using the selected version of input parameter files. The user-interface application will provide notification if the selected version has been used in model execution previously.

After selecting the version from the drop-down list in the table, user must switch on the check-box in the concerning cell in the ‘Change’ column. Please also note that there is another option names ‘Show’ above the graph component table. If the option is checked off, the selected graph will not be produced. Before generating the graphs, such configuration is necessary. However, once the configuration is complete, the configuration can be saved and loaded in a future time and can be used readily. The ‘Save Configuration’ and the ‘Load Configuration’ action buttons below the table (see Figure 1.10) can be used for saving and loading the configuration respectively.

When the configuration of graphs is done, the graphs can be generated pressing on the ‘Show Graph(s)’ action button (see Figure 1.10). If the number of graphs is more than one, the navigation buttons at the right of the ‘Show Graph(s)’ action button can be used to browse through different graphs. The navigation buttons labelled ‘|<’ and ‘>|’ refer to the first and last graph buttons respectively; while the buttons labelled ‘<’ and ‘>’ refer to action buttons for displaying the ‘previous’ and the ‘next’ graph. However, using these navigation buttons, the graph of only the selected (or current) version can be browsed.

If the action button ‘Compare’ is pressed, a new window will appear like as shown in Figure 1.11. All graphs of the same version will be displayed in this window if ‘Show Graphs for Current Version’ option is selected. Otherwise, selected graph from the dropdown list from different versions will be displayed as shown in Figure 1.12.

<img width="940" height="499" alt="image" src="https://github.com/user-attachments/assets/db07f7d0-bc02-454e-84db-e29e06bf7f4c" />

Figure 1.11: Graph Compare Window

<img width="940" height="590" alt="image" src="https://github.com/user-attachments/assets/973c4143-915c-4c86-926a-dc5ba6f4668f" />

Figure 1.12: Selected Graph from Different Versions

All graphs, being shown in the (module) main window or in the graph compare window, are stored images which has been created and stored temporarily in the ‘temp’ directory inside the application home directory while generating the graphs. Because the graphs are first generated and saved as image file, the image quality is not very high. For generating high quality image, the ‘Original View’ action button in the main window (see Figure 1.10) can be used. If the button is pressed, the selected graph will be displayed in the built-in MatPlotLib window as shown in and the graphs can be exported with ultimate quality.

<img width="940" height="426" alt="image" src="https://github.com/user-attachments/assets/0c345164-be78-4765-b665-ba0cca37cf7c" />

Figure 1.13: Orinigal Built-in Graph Viewer

**1.11	Navigation of (Parameter File) Version**

The version navigation action buttons at the top of the module main window (see second highlighted section of Figure 1.1) can be used for navigating loaded version. When the current version is changed using the navigation buttons, the corresponding view of parameter file list, parameter-views, and graphs are updated instantly.

**2	Graph Design**

**2.1	Overview**

In order to generate/produce graphs using model predictions and observation data, Graph Module has been added to the user interface. The module implements the ‘MatPlotLib’ python package (www.matplotlib.org) which provides flexible functionalities for designing and producing quality graphs in a range of very simple to ultimate complex figures. However, in this (user-interface) implementation, rather than exploring all features of the package, the basic options for 2D-graphs have been included. The main objective of the Graph Module is to provide the uses the opportunity to design their own figures depending on their needs, rather than providing only (limited number of) built-in graphs and figures. Nevertheless, a number of useful graph-templates have been added which are readily available; the users, however, can modify those templates to meet their particular needs.

The graph-templates (or the GTM files) contain the description of the figures and their components. The templates can be created and/or modified using the Graph Design Module of the model user-interface or using a text editor. Once the template is ready, it can be used for producing graphs from a particular simulation results (ref section) or from results of subsequent simulation executions (ref section). 

The components of graph-templates or the graph-objects include the description of plots, which are the divisions of drawing area or the canvas, containing different types of data-series. That is, the figure canvas is sub-divided into plots; each plot may contain several data-series and the series can be presented in concerning plot-areas with different graphical representations. This technique enables the modellers to design figures with multiple plots and provides the opportunity to (visually) compare the data/results among plots. Figure 2.1 shows examples of several plots with different graphical representations (of data) in a single figure.

<img width="995" height="496" alt="image" src="https://github.com/user-attachments/assets/a87caf26-0e25-4cee-98aa-e2641902daf7" />

Figure 2.1: Example of a Figure having multiple Plots of different types

2.2	Graph Design Main Window

Figure 2.2 displays the main window of graph design module with segmented areas highlighted in different colours. Major segments include Graph Properties, Plot Properties, Data Series Options, Graph Preview, and Action Button for saving and loading templates.

<img width="1004" height="583" alt="image" src="https://github.com/user-attachments/assets/8f8aab18-d091-4725-9aeb-3bb6659812ef" />

Figure 2.2: User-interface for Graph Design

**2.3	Design Options**

**2.3.1	Figure and Its Properties**

Figure properties includes the title of the figure, number and orientation of subplots and some display properties. Please be noted, although number and orientation of subplots are figure properties, they are presented inside the plot property segment of the interface only for the sake of users’ comfort. Although any number of plots can be added in one figure, placing too many plots can make the figure overcrowded. The plots are depicted in a grid orientation and the drawing area will be divided into grid cells based on number of rows and columns defined in plot orientation fields. The display options will pop up in a (modal) window if the action button ‘Graph Property’ is clicked. Figure 2.3 displays the graph display property window and Table 2.1 summaries all graph properties.

<img width="620" height="417" alt="image" src="https://github.com/user-attachments/assets/1c6249c0-0614-446e-bec9-14e3e33d7aab" />

Table 2.1: Graph Properties

| Property | Description	| Data Type and Value |
|--------------------------|---------------------------------------------------------------------|------------------------------|
| graph_title	| Main title of the graph	| Text |
| no_of_plot	| Number of sub-plots in the graph	| Numeric (Integer) |
| plot_orientation_col	| Number of column in orientation grid	| Numeric (Integer) |
| plot_orientation_row	| Number of row in plot orientation grid	| Numeric (Integer) |
| edit_feature	| Graph display properties (OBJECT SPECIFIER)	|  |
| window_text	| Title of the graph window	| Text |
| faceColor	| Canvas Colour	| Text (html colour code) |
| width	| With of the graph window in Pixel	| Numeric (Integer) |
| height	| Height of the graph window in Pixel	| Numeric (Integer) |
| showMaximized	| Flag to decide if the graph window would be shown maximized	| Boolean (True/False) |
| show_figure_title	| Flag to decide if the title would be shown	| Boolean (True/False) |
| font_size	| Font size of the title	| Numeric (Float) |
| font_color	| Colour of the main title	| Text (html colour code) |
| show_bold	| Flag to decide if the title would be shown bold	| Boolean (True/False) |
| horizontal_alignment	| Alignment of the title	| Text (center/left/right) |

**2.3.2	Plot and Its Properties**

Plots are partitioned drawing areas on the canvas. Plots can be added by clicking on the plot add action button, marked as ‘+’, at the right of the plot list box. Maximum number of plots can be added is determined by the number of plots in the figure. When a plot is selected from the plot list box, the property of the plot including the containing list of data-series will be displayed in the form. The selected plot can be removed if the remove action button, marked as ‘-‘, below the plot add button is pressed.

A plot has numerous properties including title, plot position, axes label options, legend options, and grid options. Moreover, each plot must contain at least one data-series. The middle section of plot properties area in Figure 2.2 displays and controls the axes options, while the lower part of the plot property area of the main window displays the legend options. The display properties of the selected plot would be shown in a pop-up modal window if the ‘Plot Properties’ action button right below the plot list-box is pressed. Figure 2.4 shows the screen-shoot of the plot display property window.

<img width="608" height="477" alt="image" src="https://github.com/user-attachments/assets/e1e94416-47cb-4a54-af70-fa2be1fdfde1" />

Figure 2.4: Plot Display Property Window

**2.3.2.1	Plot Title**
Plot title specifies the plot specific title which is also used for naming (and referencing) plots. The plot-titles are shown in the plot list-box and therefore, it is recommended to give a valid title for each plot. However, displaying plot title on the graph is kept optional. The title displaying options can be found in the plot display property window (shown in Figure 2.4). 

**2.3.2.2	Plot Position**

The position of the plot determines the position in the plot grid. Figure 2.5 shows the position in the plot grid. The plot position can be changed dynamically on the run-time. 

<img width="702" height="442" alt="image" src="https://github.com/user-attachments/assets/4db06845-a93c-46eb-9ae7-6b71220f74a9" />

Figure 2.5: Plot position numbers in a 3X3 plot grid

**2.3.2.3	Plot Axes Options**

Plot axes options includes the axis labels, ticks, and limits of each axis. These options are available in the main graph design window. Axes labels are only shown if the concerning show flag is checked on. X-tick labels can be rotated in any angle specified in degrees. The axis-limits are calculated automatically when a new data-series is added to the plot. [However, the algorithm is not currently working properly and thus, users are requested to set their axis limits by their own. In the next release of the software, this limitation will be overcome.]

In addition to the axes options, the grid intervals are important for controlling the frequency of the axes ticks.

**2.3.2.4	Grid Options**

Grid options can be found in plot display property window as shown in Figure 2.4. Grid options include the grid intervals and displaying options. Both major and minor girds can be controlled using these options.

**2.3.2.5	Legend Options**

Legend options are available in the main (graph-design) window (Figure 2.2). In this version of the user interface, only limited options for legend displaying is available.

Table 2.2: Summary of Plot Properties

| Property | Description	| Data Type and Value |
|--------------------------|---------------------------------------------------------------------|------------------------------|
|plot_title	| Title of the plot	| Text|
|plot_position	| Plot position in the plot grid. The dimension of the grid is determined by the plot orientation variable in figure property	| Numeric (Integer) starts from 1 to the max. no. of plots allowed|
|show_x_label	| Flag determines if the x-axis label would be shown	| Boolean (True/False)|
|show_y_label	| Flag determines if the y-axis label would be shown	| Boolean (True/False)|
|x_label	| x-axis label	| Text|
|y_label	| y-axis label	| Text|
|show_x_ticks	| Flag determines if the tick marks (not the tick texts or tick labels) would be shown	| Boolean (True/False)|
|x_ticks_rotation	| Rotation of ticks (i.e. tick labels) in degree	| Numeric (Float)|
|show_legend	| Flag determines if the legend would be shown	| Boolean (True/False)|
|legend_vertical_position	| Vertical position (in the plot area) where the legend will be drawn	| Numeric (Integer); -1: Below, 0: Middle, +1: Top|
|legend_horizontal_position	| Horizontal position (in the plot area) where the legend will be drawn	| Numeric (Integer); -1: Left, 0: Middle, +1: Right|
|edit_feature	| Plot display options (OBJECT SPECIFIER)	| |
|backgroundColor	| Background colour of the drawing area	| Text (html colour code)|
|x_lim_max	| x-axis max limit or the end point	| Numeric (Float)|
|x_lim_min	| x-axis min limit or starting point	| Numeric (Float)|
|y_lim_max	| y-axis max limit	| Numeric (Float)|
|y_lim_min	| y-axis min limit	| Numeric (Float)|
|x_axis_major_interval	| Major grid interval of x-axis 	| Numeric (Float)|
|x_axis_minor_interval	| Minor grid interval of x-axis	| Numeric (Float)|
|y_axis_major_interval	| Major grid interval of y-axis	| Numeric (Float)|
|y_axis_minor_interval	| Minor grid interval of y-axis	| Numeric (Float)|
|grid_show	| Flag determines if the Grid-lines would be shown	| Boolean (True/False)|
|grid_axis_option	| Option determines grid-lines on which axis would be displayed	| Text (‘x’, ‘y’, or ‘both’)|
|grid_which_option	| Option determines which grid (i.e. major or minor) would be displayed	| Text (‘major’, ‘minor’, or ‘both’)|
|show_plot_title	| Flag determines if the title of the plot would be displayed	| Boolean (True/False)|
|title_font_size	| Font size of plot title	| Numeric (Float)|
|title_font_color	| Font colour of plot title	| Text (html colour code)|
|title_show_bold	| Flag determined if the plot title would be shown in bold font face	| Boolean (True/False)|
|horizontal_alignment	| Horizontal alignment of the plot title	| Text (‘left’, ‘center’, or ‘right’)|

**2.3.3	Data-Series**

A plot may contain one or more data-series. Data-series can be added, deleted or edited pressing the respective ‘+’ (meaning ‘add’), ‘-‘ (meaning ‘remove’) or ‘E’ (meaning ‘edit’) action buttons in the data-series area of the main (graph-design) window as shown in Figure 2.2. In the list-box, the data-series names are listed while in the title box, title of the selected data-series is displayed. In the legend, series title would be shown. Data-Series properties are controlled by the Data-Series Window, displayed in Figure 2.6, which appears when add or edit action button is pressed.

<img width="667" height="654" alt="image" src="https://github.com/user-attachments/assets/75ef4bde-dac6-44c3-8754-ec318ba88e3c" />

Figure 2.6: Data-Series Window

**2.3.3.1	Data Source**

Each data-series must contain the information regarding the source of data from where data would be acquired during actual graph creation. The left half of the data-series window shows the data source options which includes easy accessibility tools for exploring variable in model output files and observation data files. The (radio) option buttons if new source will be assigned to the data-series or if the existing source will be modified. If the ‘Open’ action button below the option buttons is pressed, data-source options will be displayed in a pop-up frame as in Figure 2.7.

<img width="381" height="202" alt="image" src="https://github.com/user-attachments/assets/ba92832e-b40a-414c-ab58-7e46557ce16e" />

Figure 2.7: Data-Source Option

Data can be acquired either from simulation output files or from observation files. In case of model output file, the address of the (model) initialization file is required because the output variables are controlled by the initialization file. Moreover, because the (Biome-BGC) model produce many output files, the type (i.e., the extension, see model guidelines) of the output file must be provided. Also, if the observation data is used and have different units than their counter-part model variables, model predictions need to be adjusted (or converted) according to the data conversion plan (see section ref). Data-conversion is controlled by the ‘Convert Unit’ checkable option.

In case of observation data, only the address of the data-file is required; however, the data-file should be CSV formatted.

**2.3.3.2	Plotting Options and Styles**

Plotting option defines how the data will be plotted in the graph. Data can be plotted either as points, line, bars or as pies. [Scatter Plot and Stacked Bar options have been included but were not implemented in this version]. Please note that plotting option ‘pie’ cannot be selected if the plot already has other data-series; in other words, in case of pie plots, only one data-series can be added to the plot.

Plot option also controls the style properties of a data-series. That is, for each plotting option, different sets of display options (style options) are used. 

**(i)	Point Styles:**

Point styles properties include the point style, point face colour, colour of edge, size of the point and width of the edge. Point style can be one of the followings: None, Circle, Square, Diamond, Thin Diamond, Point, Star, Plus, Pentagon, Hexagon, Octagon, Triangle (Up, Down, Left, Right), Tick (Left, Right, Up, Down), Vertical Line. Figure 2.8 shows the style option frame for point series.

<img width="470" height="209" alt="image" src="https://github.com/user-attachments/assets/04f810fb-e256-483d-b620-ca64b13ec4b5" />

Figure 2.8: Style Options for Points

**(ii)	Line Styles:**

Style options for line includes style of the line, line colour, line width, point marker options including point style and point size. Line style can be either ‘solid’, ‘dashed’, ‘dotted’ or ‘dash dotted’. Marker style can be any of the point styles mentioned in the point style section above. Markers can be excluded by checking the ‘Show Marker’ option off. F displays the line style control frame.

<img width="486" height="245" alt="image" src="https://github.com/user-attachments/assets/e674eb18-f6da-4463-9fa8-f7399bbc1541" />

Figure 2.9: Style Option Frame for Lines

**(iii)	Bar Styles:**

Style options for bars includes filling colour, edge style, colour and width, and hatch. Edge style can be one of the line styles mentioned in the previous section. Hatch option can be one of the followings: ‘None’, ‘//’, ‘\\’, ‘||’, ‘--', ‘++’, ‘xx’, ‘XX’, ‘oo’, ‘OO’, ‘..’, or ‘**’.

<img width="530" height="237" alt="image" src="https://github.com/user-attachments/assets/27bac311-8320-454e-9d60-19042982c278" />

Figure 2.10: Style Option Frame for Bars

**(iv)	Pie Styles:**

Colours of the pies are selected automatically by the ‘MatPlotLib’ package. [However, in the next version of the interface, pie colours could be chosen]. Other styling options include the radius of the pie, start angle, distance of label from the pie, whether or not the largest pie would explode and if so, how much, and shadowing option. Figure 2.11 displays the Pie Style control panel.

<img width="525" height="248" alt="image" src="https://github.com/user-attachments/assets/76edd04d-be0e-4201-93c5-ebc881b26e5c" />

Figure 2.11: Style Option Frame for Pie

**2.3.3.3	 Series and X-axis Variables**

Series variable specifies the data variable or the y-axis values. The series variable can be selected from the variable list appears in the list-box of the data-source section (see Figure 2.6). The x-axis variables specifies x-axis of the plot. When the x-axis variable is set, the application calculated the x-axis minimum and maximum from opened data-file and saves the axis limit. Thus, when the source of data is changed, the axis limits become inappropriate and it requires to fix the limits manually.

If x-axis variable is not provided, the series variable will be plotted against the number of data points in the series variable.

**2.3.3.4	Filtering Data**

The series data (or y-axis data) can be filtered. Because the Biome-BGC model produces time-series and most the filter is done using one of the time variable, any filter operation requires a filtering variable and the filter condition will be applied on the filtering variable. In the filter operation, the corresponding values of the (data) series variable will be selected if the corresponding values of the filter variable satisfy the filter condition. If only series data need to be filtered, the series variable name must be mention also as filter variable.

Filter condition can either be one of the following: equal, greater than, less than, greater than or equal, less than or equal, and between. In case of between, two values must be entered and the first value must specifies the lower limit.

Table 2.3: Summary of Bar Properties

| Property | Description	| Data Type and Value |
|--------------------------|---------------------------------------------------------------------|------------------------------|
|attribute_name	| Data series variable (i.e., y-axis variable)	| Array of numbers|
|series_title	| Title of the series	| Text|
|x_axis_variable	| x-axis variable name	| Text|
|filter_variable	| Name of the filtering variable	| Text|
|filter_condition	| Filter condition	| Text (‘>’, ‘<’, ‘=’, ‘>=’, ‘<=’ , ‘between’)|
|filter_first_value	| Filter value	| Numeric|
|filter_second_value	| Second filter value; required only the filter condition is ‘between’	| Numeric|
|plotting_option	| Plotting option	| Text (‘point’, ‘bar’, ‘line’, ‘pie’)|
|data_source	| (OBJECT SPECIFIER) Specifies data source	| Text (‘DataSource’)|
|edit_feature	| (OBJECT SPECIFIER) Specifies plotting style of data-series 	| Text (‘LineEditFeature’, ‘PointEditFeature’, ‘BarEditFeature’, ‘PieEditFeature’)|
|Data source properties: | | |
|source_type	|Flag determines if the source is a simulation output or observation data file 	| Numeric (integer); 0 = Simulation, 1 = Observation (CSV)|
|model_directory	| Home directory of the model program; required if source type is 0	| Text|
|initial_filename	| Model initialization filename; required if source type is 0	| Text|
|output_file_type	| Model output file type; required if source type is 0	| Text|
|unit_conversion_flag	| Flag determines if the unit conversion need to be applied; required if source type is 0 	| Boolean (True/False)|
|data_filename_csv	| Name of the observation data file; required only if source type is 1	| Text|
|Point Style Properties: | | |
|point_style	| Appearance of points	| Text (None = 'None', 'o' = 'Circle', 's' = 'Square', 'D' = 'Diamond', 'd' = 'Thin Diamond', '.' = 'Point', '*' = 'Star', '+' = 'Plus', 'p' = 'Pentagon', 'h' = 'Hexagon1', 'H' = 'Hexagon2', '8' = 'Octagon', '^' = 'Triangle Up', 'v' = 'Triangle Down', '>' = 'Triangle Left', '<' = 'Triangle Right', 0 = 'Tick Left', 1 = 'Tick Right', 2 = 'Tick Up', 3 = 'Tick Down', '|' = 'Verlicle Line') |
|face_color	| Colour of the points	| Text (html colour code)|
|size	| Point size	| Numeric (integer)|
|edge_color	| Edge colour of points	| Text (html colour code)|
|edge_line_width	| Line width of edge	| Numeric (integer)|
|Line Style Properties: | | |
|style	| Line style	| Text ('-' = 'Solid', '--' = 'Dashed', '.' = 'Dotted', '-. = 'Dash Dot'',  '' = 'No Line')|
|color	| Colour of the line	| Text (html colour code)|
|line_width	| Width of line	| Numeric (integer)|
|show_marker	| Flag determines if the marker on the line will be shown	| Boolean (True/False)|
|marker	| Style of marker	--same as point style-- | |
|marker_size	| Size of marker	| Numeric (integer)|
|Bar Style Properties: | ||
|color	| Bar Colour	| Text (html colour code)|
|edge_color	| Colour of bar edge	| Text (html colour code)|
|line_style	| Style of edge	--same as line style-- | |
|line_width	| Width of edge	| Numeric (integer)|
|hatch	| Hatch Style	| Text ('' = 'None', '/' = '////', '\\' = '\\\\', '|' = '|||', '-' = '----', '+' = '+++', 'x' = 'xxxx', 'o' = 'oooo', 'O' = 'OOOO', '.' = '....', '*' = '****')|
|Pie Style Properties: | | 
|color|		| Text (html colour code)|
|start_angle	| Starting angle	| Numeric (decimal degree)|
|shadow	| Flag determines if the pies would have shadow	| Boolean (True/False)|
|radius	| Pie radius	| Numeric (decimal)|
|explode	| Flag determines if any pie would explode	| Boolean (True/False)|
|explode_maximum	| Maximum exploding distance	| Numeric (decimal)|
|label_distance	| Distance of pie labels 	| Numeric (decimal)|
|show_value_label	| Flag determines if the labels would be shown	| Boolean (True/False)|

The graph objects can be opened, modified and created using any text editor. However, special format must be followed during creating or modifying a graph with text editor. First, each object start with a ‘@@’ (i.e., a double at sign) following the type of the object or the property name. The object definition ends with a single at sign (i.e., ‘@’) following the starting keyword. Following table shows the list of objects and their start and end keywords.

Table 2.4: List of Object Identifiers
|Object	|Starting Keyword	|Ending Keyword|
|-----------------|----------------------------|-------------------------------|
|Graph	|@@model_graph	|@model_graph|
|Plot	|@@plot	|@plot|
|Series	|@@series	|@series|
|Data Source	|@@data_source	|@data_source|
|Display Option	|@@edit_feature	|@edit_feature|

Secondly, in case of dynamic objects, like display option or edit_feature object which can hold different specialized object, the type of the object be specified along with object identifying keyword; and the type is specified mentioning the type name after an equal sign (i.e., ‘=’). Table 2.5 shows assignment of different child objects using the same object identifier keywords.

Table 2.5: Object Specification with Type Assignment
|Object	|Object specifier with type|
|-----------------|-----------------------------------------------------------|
|Graph Display Option	|@@edit_feature = FigureEditFeature|
|Plot Display Option	|@@edit_feature = PlotEditFeature|
|Point Series Display Option	|@@edit_feature = PointEditFeature|
|Line Series Display Option	|@@edit_feature = LineEditFeature|
|Bar Series Display Option	|@@edit_feature = BarEditFeature|
|Pie Display Option	|@@edit_feature = PieEditFeature|

Thirdly, the object definitions follows a cascading styles. That is, inner object must be defined within the immediate parent object. The following box shows an example of cascading object definition where a graph has two plots and each plot has different numbers (1 and 2 respectively) of data series.

```
@@model_graph
…
@@plot
…
…
@@series
…
…
@series
@plot
@@plot
…
@@series
…
@series
@@series
…
@series
@plot
@model_graph
```

Example of Cascading Object Definition

Fourthly, the properties of an object must be defined using the property keyword and the value of a property must be provided after the equal sign (i.e., ‘=’) after the keyword. The value and the keyword must be on the same text line. No break (i.e., new line or carriage return) is allowed between keyword and value. The keywords must comply with the property names mentioned in Table 2.1, Table 2.2, and Table 2.3.

Finally, property values must not encoded with single or double quotation marks or signs.

**2.4	Graph Preview**

As highlighted in the fourth segment of the main window (see Figure 2.2), the preview of the graph will be shown every time the graph is updated. If the preview is not shown, the ‘Refresh Preview’ action button can be pressed. When the ‘Refresh Preview’ button is pressed, the application will try update the preview of the graph.

However, in this version of user interface, the graph preview will only be shown if the data is obtained in the source location as defined in the data source object definition. Usually during the design phase data is always available and thus the preview would be displayed. On the other hand, when a graph is loaded/opened from a saved template, the preview will not be displayed if data is not available. 

**2.5	Saving and Opening Graph Template**

The graph objects can be save as templates and can be used as readily available graphs. The templates can be modified later at another point of time. Pressing on the action buttons ‘Save template’ and ‘Open Template’ in the fifth highlighted area of the main window as shown in Figure 2.2 the graph can be saved as template or a graph can be loaded from a template. Please note that the templates are saved with ‘gtm’ file extension, but the ‘gtm’ files can be opened and modified with any text editor.

**Part-Three: Model Calibration**

(to be added soon!!)





