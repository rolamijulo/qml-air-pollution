A Comparative Analysis Of Classical And Quantum Machine Learning For Urban Air Quality Modeling In Baltimore
About This Project
    This repository contains the computational experiments for a Master of Science thesis at Morgan State University. The research evaluates classical and quantum machine learning models for neighborhood level nitrogen dioxide prediction. The project uses demographic percentages and historical redlining grades from Baltimore as input features.

Attribution and Background
    The data engineering scripts build upon an original repository created by prior researchers. The foundational visualization code aimed to recreate findings from the environmental justice study by Lane and colleagues. This thesis extends that descriptive work into a predictive learning framework using advanced quantum algorithms.

Repository Structure
    The classical machine learning baseline resides in the baltimore_ml.py Python file. The baltimore_qml.py script trains the primary variational quantum regressor for continuous pollution prediction. The baltimore_comparison.py file generates the unified performance table to contrast these distinct architectures.

Additional Experiments
    The baltimore_qml_kernel.py script executes the spatial classification experiment using a median pollution threshold. The baltimore_depth_test.py file evaluates how ansatz repetitions relate to the mean squared error. The utils.py file handles data ingestion and feature preparation for all the predictive models.

Execution Instructions
    Users must install the Qiskit software framework to simulate the quantum circuits accurately. The pipeline also requires standard data science libraries like Pandas and Scikit learn. Researchers can execute any of the primary experiment files directly from the command line to reproduce the thesis results.
