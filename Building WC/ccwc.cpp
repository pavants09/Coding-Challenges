#include <iostream>
#include <fstream>
#include <sstream>

using namespace std;

// Count bytes
long count_bytes(istream &in) {
    in.seekg(0, ios::end);
    return in.tellg();
}

// Count lines
long count_lines(istream &in) {
    long count = 0;
    string line;
    while (getline(in, line)) count++;
    return count;
}

// Count words
long count_words(istream &in) {
    long count = 0;
    string word;
    while (in >> word) count++;
    return count;
}

// Count characters
long count_chars(istream &in) {
    long count = 0;
    char c;
    while (in.get(c)) count++;
    return count;
}

int main(int argc, char* argv[]) {
    ios::sync_with_stdio(false);

    string option = "";
    string filename = "";

    // Case 1: ccwc file.txt (default)
    if (argc == 2) {
        filename = argv[1];
    }
    // Case 2: ccwc -x file.txt
    else if (argc == 3) {
        option = argv[1];
        filename = argv[2];
    }
    // Case 3: stdin (pipe)
    else if (argc == 2 && string(argv[1]) == "-l") {
        option = argv[1];
    }
    else if (argc > 3) {
        cerr << "Usage:\n";
        cerr << "  ccwc -c|-l|-w|-m <file>\n";
        cerr << "  ccwc <file>\n";
        return 1;
    }

    if (filename == "") {
        if (option == "-l") {
            cout << count_lines(cin) << endl;
        } else if (option == "-w") {
            cout << count_words(cin) << endl;
        } else if (option == "-c") {
            cout << count_chars(cin) << endl;
        } else {
            cerr << "Invalid usage with stdin\n";
            return 1;
        }
        return 0;
    }

    ifstream file(filename, ios::binary);
    if (!file) {
        cerr << "Error opening file\n";
        return 1;
    }

    if (option == "-c") {
        file.seekg(0, ios::end);
        cout << file.tellg() << " " << filename << endl;
    }
    else if (option == "-l") {
        cout << count_lines(file) << " " << filename << endl;
    }
    else if (option == "-w") {
        cout << count_words(file) << " " << filename << endl;
    }
    else if (option == "-m") {
        cout << count_chars(file) << " " << filename << endl;
    }
    else if (option == "") {
        long lines = count_lines(file);

        file.clear();
        file.seekg(0);

        long words = count_words(file);

        file.clear();
        file.seekg(0);

        file.seekg(0, ios::end);
        long bytes = file.tellg();

        cout << lines << " " << words << " " << bytes << " " << filename << endl;
    }
    else {
        cerr << "Unsupported option\n";
        return 1;
    }

    return 0;
}