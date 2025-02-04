
# Network-Based Malware Detection using Natural Language Processing
This project illustrates a method that utilizes the ordering of network flows to classify malicious behavior. The approach is lightweight and privacy preserving while also being resilient to encrypted packet payloads.

## Getting Started

### Prerequisites

The project is written in *python3*, ensure you have the latest version of *python3* and *pip3* [installed](https://www.python.org/downloads/).
The project relies on *tshark* for pre-processing pcap files, and *p7zip* to extract zip files.

On Ubuntu, these can be installed using:
```
sudo apt-get install tshark p7zip
```
Besides these, other required packages can be installed using *pip3*.
```
pip3 install -r requirements.txt --user
```

### Directory Structure
```
.
+-- ml
|   +-- model.py (file with ml functions)
+-- preprocess
|   +-- process.py
|   +-- process.sh (pcap pre-processing)
|   +-- pcap-to-ngrams.py (pcap conversion to ngrams)
|   +-- f2nlib.py
|   +-- p2flib.py
+-- scripts
|   +-- run.sh (script to run tests on ComputeCanada servers)
|   +-- run_all.sh (automate test running)
+-- requirements.txt
+-- README.md
+-- LICENSE.md
```

### Running Tests
1. Grab the [USTC-TFC2016 DeepTraffic](https://github.com/echowei/DeepTraffic) dataset.
2. Generate a ngram file using *process.sh*.
3. Run *model.py* with the ngram file.
4. Automate tests using custom bash scripts, the ones included in the repository work on ComputeCanada servers.
```
./process.sh [path-to-dataset] [n]
```
This creates a file called [n]_test.csv in the dataset folder
```
python3 model.py [path-to-test-csv]
```
This should print the results on the screen.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [Mitacs Globalink](https://www.mitacs.ca/en/programs/globalink), [uOttawa](https://engineering.uottawa.ca/school-EECS) and [MHRD, India](https://mhrd.gov.in/) for funding the project.
* [Prof. David Knox](https://engineering.uottawa.ca/people/knox-david) at uOttawa for project supervision.
* [ComputeCanada](https://www.computecanada.ca/home/) for access to their servers to run tests.
