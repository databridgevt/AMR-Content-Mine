# AMR-Content-Mine

## Note:
This version was last pushed Aug. 07. Master branch currently contains the most recent version of the AMR-Content-Mine


## Basic Usage
1. Download articles using the two following content mine commands:
  ```
  getpapers -q '(TITLE:"One health" OR TITLE:"One medicine" OR TITLE:"Animal" OR TITLE:"human" OR TITLE:"environment" OR TITLE:"ecosystem" OR TITLE:"ecohealth") AND (TITLE:"Antimicrobial resistance" OR TITLE:"antibiotic resistance" OR TITLE:"drug resistance" OR TITLE:"multi-drug resistance" OR TITLE:"resistance" OR TITLE:"AMR" OR TITLE:"ABR" OR TITLE:"AR" OR TITLE:"MDR") NOT (TITLE:"herbicide" OR TITLE:"pesticide" OR TITLE:"disease resistance" OR TITLE:"fungicide")' -o AmsContainer -p -f AmsContentMineLog
  ```
  ```
  getpapers -q '(ABSTRACT:"One health" OR ABSTRACT:"One medicine" OR ABSTRACT:"Animal" OR ABSTRACT:"human" OR ABSTRACT:"environment" OR ABSTRACT:"ecosystem" OR ABSTRACT:"ecohealth") AND (ABSTRACT:"Antimicrobial resistance" OR ABSTRACT:"antibiotic resistance" OR ABSTRACT:"drug resistance" OR ABSTRACT:"multi-drug resistance" OR ABSTRACT:"resistance" OR ABSTRACT:"AMR" OR ABSTRACT:"ABR" OR ABSTRACT:"AR" OR ABSTRACT:"MDR") NOT (ABSTRACT:"herbicide" OR ABSTRACT:"pesticide" OR ABSTRACT:"disease resistance" OR ABSTRACT:"fungicide")' -o AmsContainer -p -f AmsContentMineLog
  ```
2. Run the python parser.py script
  ```
  python parser.py
  ```
  - If you get an error saying `ImportError: No module named module_name` then install that module using `sudo pip install module_name`. 

