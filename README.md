# Analysis of Boolean Networks and Transitions 

## How to run the code?

### Prerequisites

<ul>
    <li>
        MatlibPlot
    </li>
    <li>
        NumPy
    </li>
</ul>

### Inputs

<ul>
    <li>
        If the input is a file containing a Boolean network, then move the file into the directory <code>Boolean/data/networks</code>. The type of the file should be **network**.
    </li>
    <li>
        If the input is a file containing transitions, then move the file into the directory <code>Boolean/data/transitions</code>. The type of the file should be **transitions**.
    </li>
</ul>

### Configuration

Under the path `Boolean/config`, open the file **\_\_init\_\_.py**. Edit parameters according to your requirements.

### Running

Open the terminal. Change its directory to `Boolean`. Run the command `python main.py`.

## What can the code do?

<ul>
    <li>
        Load a Boolean network. Generate complete transitions based on this Boolean network. Save them under the path <code>Boolean/data/transitions</code>. The complete transitions is saved as the name of the Boolean network with a suffix <strong>_complete</strong> and the file type <strong>transitions</strong>.
    </li>
</ul>
