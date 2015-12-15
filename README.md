# ToneClimateJoLE

For the latest version, please see:
https://github.com/seannyD/ToneClimateJoLE

These are supplementary materials for Everett, Blasi & Roberts (2015): Climate and language: Has the discourse shifted?

# ANU_numTones_SpecificHumidity_GlottoFams.csv
The data used in the studies.  Columns are as follows:

- OID_   		ANU phonological database identifier code
- iso			Language iso code
- Language	Language name
- Family		Language family (ANU)
- gFam		Language family (Glottolog)
- Autotyp.area	Geographic area
- Region		Geographic region
- Number.of.tones	Number of contrasting tones
- specH.mean	Specific mean humidity

# AppendixResponseToHammarstrom.pdf
A description of the statistical tests carried out.

# MonteCarloByFamily2.py
Run the statistical tests (Python)

# MonteCarloByFamily_Results.txt
Results for MonteCarloByFamily2.py

# MonteCarloByFamily_andArea.py
Run the statistical tests, sampling languages that are independent in family AND area

# MonteCarloByFamily_andArea_Results.txt
Results for MonteCarloByFamily_andArea.py


# MonteCarloByFamily4.r
An implementation of some of the tests in R
# IndepResults.csv
Results from the R implementation

# IndependentSampleHist.r
Make a density plot, taking into account the relatedness of languages.