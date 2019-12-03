# AMR Content Mine

Hey AMR Team,

It's Tanner, here. While working on multi-processing, I've made a few opinionated refactors to the scripts, local environment, and repository. If anything seems weird or out-of-place, feel free to rollback my commits, of course. `git reset --hard 3a21a71` should take you back to the "original"  repository. Alternatively, I put this "original" repository in another branch. `git checkout v1.0` will take you to that branch.

## Usage

### Downloading The Papers

In order to download all of the necessary PDFs from EuropePMC, we'll need to download a content miner from `npm`.

#### 1. Install Node.js

To check if you have Node.js installed on your computer, run:

```bash
which node
```

If Node.js is installed, then a path should be printed. If Node.js is not installed, here's a link to [Node.js's download page](https://nodejs.org/en/download/). Good Luck, Have Fun.

#### 2. Install `getpapers`

The Node Package Manager is a useful tool for downloading and using Node packages/libraries/frameworks published by other Node.js developers. To quickly download papers from the EuropePMC, we'll use the `getpapers` package from `npm`.

```bash
npm i -g getpapers
```

Bam. You're all set.

#### 3. Actually Downloading the Papers

Download articles using the two following content mine commands:

```bash
node --max_old_space_size=4000 $(which getpapers) -q '(TITLE:"One health" OR TITLE:"One medicine" OR TITLE:"Animal" OR TITLE:"human" OR TITLE:"environment" OR TITLE:"ecosystem" OR TITLE:"ecohealth") AND (TITLE:"Antimicrobial resistance" OR TITLE:"antibiotic resistance" OR TITLE:"drug resistance" OR TITLE:"multi-drug resistance" OR TITLE:"resistance" OR TITLE:"AMR" OR TITLE:"ABR" OR TITLE:"AR" OR TITLE:"MDR") NOT (TITLE:"herbicide" OR TITLE:"pesticide" OR TITLE:"disease resistance" OR TITLE:"fungicide")' -o AmsContainer -p -f AmsContentMineLog

node --max_old_space_size=4000 $(which getpapers) -q '(ABSTRACT:"One health" OR ABSTRACT:"One medicine" OR ABSTRACT:"Animal" OR ABSTRACT:"human" OR ABSTRACT:"environment" OR ABSTRACT:"ecosystem" OR ABSTRACT:"ecohealth") AND (ABSTRACT:"Antimicrobial resistance" OR ABSTRACT:"antibiotic resistance" OR ABSTRACT:"drug resistance" OR ABSTRACT:"multi-drug resistance" OR ABSTRACT:"resistance" OR ABSTRACT:"AMR" OR ABSTRACT:"ABR" OR ABSTRACT:"AR" OR ABSTRACT:"MDR") NOT (ABSTRACT:"herbicide" OR ABSTRACT:"pesticide" OR ABSTRACT:"disease resistance" OR ABSTRACT:"fungicide")' -o AmsContainer -p -f AmsContentMineLog
  ```

I should note, the `-g` switch tells npm that you want to install this package globally. This may require `sudo` privileges.

### Running The Parser

#### Recommended

There's now a `pipenv` for this project. This 'virtual environment' should make sure that everyone is using the same versions for our dependencies. To install `pipenv`, use `pip3 install --user pipenv`. Then to run the script, use:

```bash
pipenv run ./parser.py
```

#### Alternative

This script should support running straight from the command line. Just try,

```bash
./parser.py
```

If you get an error saying `ImportError: No module named module_name` then install that module using `sudo pip install module_name`.
