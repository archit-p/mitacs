# Network-Based Malware Detection using Natural Language Processing

A network flow constitutes packets exchanged between two parties that have the same header fields. We propose a method that utilizes the ordering of these flows to classify malicious behaviours. These attributes are used to analyze malware packets in a lightweight and  privacy preserving way while also being resilient to encrypted packet payloads, while obtaining an accuracy of 95% on the [DeepTraffic](https://github.com/echowei/DeepTraffic) dataset.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The project is written in *python3*, ensure you have the latest version of *python3* and *pip3* [installed](https://www.python.org/downloads/). 
The project relies on *tshark* for pre-processing pcap files, and *p7zip* to extract zip files.

On Ubuntu, these can be installed using:
```
sudo apt-get install tshark p7zip
```
Besides these, the projects' dependencies can be installed using *pip3".
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
1. Generate a ngram file using *process.sh*. 
```
./process.sh [path-to-dataset] [n]
```
This creates a file called [n]_test.csv in the dataset folder.
2. Run *model.py* with the ngram file.
```
python3 model.py [path-to-test-csv]
```
This should print the results on the screen.
3. Automate tests using custom bash scripts, the ones included in the repo work on ComputeCanada servers.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [Mitacs Globalink](https://www.mitacs.ca/en/programs/globalink), [uOttawa](https://engineering.uottawa.ca/school-EECS) and [MHRD, India](https://mhrd.gov.in/) for funding the project.
* [Prof. David Knox](https://engineering.uottawa.ca/people/knox-david) at uOttawa for project supervision.
* [ComputeCanada](https://www.computecanada.ca/home/) for access to their servers to run tests.
