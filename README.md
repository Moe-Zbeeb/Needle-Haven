# Amazon-Industry-Program-3.0  
![image](https://github.com/zbeeb1/CHIC/assets/134772110/cd51daf4-080b-45d9-9485-2bd496250c7c)



## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Updating Requirements](#updating-requirements)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Prerequisites
Before you begin, ensure you have the following installed on your system:
- Git
- Python 3.6 or higher
- Virtual Environment (venv)

## Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/zbeeb1/CHIC.git
    ```

2. **Change the Directory**
    ```bash
    cd CHIC/
    ```

3. **Set Up Virtual Environment**

    **On Linux:**
    ```bash
    . venv/bin/activate
    ```
    
    **On Windows:**
    ```bash
    venv\Scripts\activate
    ```

4. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1. **Run the Application**
    ```bash
    flask --main_web flaskr run --debug
    ```

## Updating Requirements

After making changes to the code, update the dependencies by running:
```bash
pip freeze > requirements.txt
