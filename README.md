# PrimeRAM

An advanced Android RAM parser designed for digital forensics professionals.

## Overview

PrimeRAM is a powerful tool that allows forensic analysts to parse and analyze RAM dumps from Android devices. It helps uncover crucial information stored in volatile memory, assisting in comprehensive digital investigations.

## Features

- **Efficient Parsing**: Quickly process large RAM dumps with optimized performance.
- **Data Extraction**: Retrieve sensitive information such as credentials, messages, and cached data.
- **File Recovery**: Recover deleted files and artifacts from memory.
- **User-Friendly Interface**: Intuitive command-line interface for seamless operation.
- **Cross-Platform Support**: Compatible with Windows, macOS, and Linux systems.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/0x06060606/PrimeRAM.git
   ```

2. **Navigate to the Project Directory**

   ```bash
   cd PrimeRAM
   ```

3. **Install Dependencies**

   Ensure you have Python 3.x installed.

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Obtain a RAM Dump**

   Extract a RAM dump from the target Android device using your preferred method.

2. **Run PrimeRAM**

   ```bash
   python primeram.py -f /path/to/ram_dump.bin
   ```

3. **Specify Output Directory (Optional)**

   ```bash
   python primeram.py -f /path/to/ram_dump.bin -o /path/to/output_directory
   ```

4. **View Results**

   Analyze the extracted data located in the specified output directory.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For inquiries or support, please contact [0x06060606](https://github.com/0x06060606).
